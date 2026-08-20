# 06. Design a News Feed — Mid

The Design Ladder works like the DSA practice sets: attempt first, then peek. Work the design on paper against the [framework template](../appendix/templates/system-design/template.md) for a full 45 minutes before opening any step below — the struggle *is* the practice.

[← Back to the lesson](../system-design/02-caching.md) · [🗺 Interview Roadmap](../../interview.md)

---

## The prompt

> "Design a news feed — like Facebook or Twitter. Users follow each other and post; when a user opens the app they see a ranked feed merged from everyone they follow."

Typical follow-up constraints when you ask (and you should ask — that's Step 1):

- **~300M DAU**; read:write ratio around **100:1** — people scroll far more than they post.
- Feed load must feel instant: **< 200ms**.
- Follower counts are **power-law**: most users have hundreds of followers; celebrities have **tens of millions**.
- Near-real-time is fine — a post appearing in followers' feeds within seconds, not milliseconds.

Why this design? It's *the* canonical mid-level prompt, and it lives or dies on one decision — fan-out on write vs fan-out on read — that you must argue with numbers, because the power-law follower distribution breaks each pure strategy in a different place.

<details>
<summary>Step 1 — Requirements & API</summary>

**Functional:**
- Follow/unfollow users.
- Create a post (text; media via a separate blob path — confirm scope).
- Fetch the feed: a ranked, paginated merge of followees' recent posts.
- (Confirm scope) likes/comments, notifications, ads injection — usually out.

**Non-functional:**
- **Read-optimized**: 100:1 means almost everything you build serves the read path.
- Feed load < 200ms; post creation can take seconds to propagate.
- Eventual consistency is fine — two followers may briefly see different feeds; say so out loud.

**API sketch:**

```
POST /api/posts
  body: { "text": "hello" }
  returns 201: { "post_id": "p_88a1" }

GET /api/feed?cursor=p_87f0&limit=20
  returns 200: { "posts": [ ... ], "next_cursor": "p_86c2" }

POST /api/follows   body: { "followee_id": "u9" }
```

One decision worth saying out loud: **pagination is cursor-based, not offset-based.** The feed shifts under the reader as new posts arrive — `?page=2` with offsets re-serves or skips items when the underlying list moved. A cursor ("everything older than post p_87f0") is stable against insertion. Small API choice, direct consequence of the data being live.
</details>

<details>
<summary>Step 2 — Estimates</summary>

Keep it to one-significant-figure math (the [estimation recipes](../system-design/00e-estimation.md)):

- **Feed reads:** 300M DAU × ~10 feed loads/day = 3B/day ≈ **35K QPS**, peak ~100K/s.
- **Posts:** 100:1 ratio → ~30M posts/day ≈ **350 writes/s**. Tiny — the raw post writes are never the problem.
- **The fan-out multiplier is the problem:** 350 posts/s × ~200 followers average = **70K feed-cache writes/s** — fine. But one celebrity with 10M followers posting once = **10M writes for a single post**; at even 100K writes/s that's ~100 seconds of dedicated effort, and a burst of celebrity posts stampedes the cache tier.
- **Feed cache size:** store post *IDs*, not bodies — 300M users × 500 IDs × ~20 bytes ≈ **3 TB** of ID lists, sharded across a Redis fleet. Post bodies live once in a separate post cache (30M posts/day × 1 KB ≈ 30 GB/day) — normalization keeps the multiplied thing small.

The numbers just drew the battle line: average-case fan-out on write is cheap (70K/s), celebrity fan-out is catastrophic (10M per post) — which is precisely why the answer ends up hybrid.
</details>

<details>
<summary>Step 3 — High-level design</summary>

```
 POST /posts ──► ┌──────────┐    ┌───────────────┐
                 │ Post svc │───►│ Post store +  │
                 └────┬─────┘    │ post cache    │  id → content
                      │ event    └───────▲───────┘
                ┌─────▼──────┐           │ hydrate
                │ Fan-out    │  push post-id to each
                │ workers    │  follower's feed list
                │ (queue)    │  (skip celebrities)
                └─────┬──────┘
                ┌─────▼───────────────────────────┐
                │ Feed cache: user → [post ids]   │
                └─────▲───────────────────────────┘
 GET /feed ────► ┌────┴─────┐   pull path: fetch celebrity
                 │ Feed svc │◄─ followees' recent posts,
                 └──────────┘   heap-merge with pushed list
```

**THE decision — this comparison *is* the interview; do it with numbers:**

1. **Fan-out on write (push):** when a user posts, workers append the post ID to every follower's cached feed list. Reads are a single cache fetch — trivially fast, which suits 100:1. Cost: writes multiply by follower count. Average user: 200 cache appends — nothing. Celebrity: **one post = 10M cache writes** (Step 2), minutes of work and a write stampede. Also wasteful: most of the 10M followers who never log in this week got a write for nothing.
2. **Fan-out on read (pull):** store nothing per-follower; at read time, fetch each followee's recent posts and merge. Writes are one insert — celebrities cost nothing extra. Cost: a user following 500 people triggers ~500 lookups and a merge on *every* feed load, at 35K QPS — the 100:1 ratio means you've moved the multiplication onto the hot path. Latency budget dies.
3. **Hybrid (pick this):** push for normal users, pull for the few thousand accounts above a follower threshold (~100K–1M). At read time the feed service takes the user's precomputed pushed list, pulls recent posts from the handful of celebrities they follow, and **merges at read**. Push cost is capped (no single post fans to millions), pull cost is capped (nobody follows thousands of celebrities), and each strategy covers the other's worst case.

The merge is your DSA bridge: k small sorted-by-time lists merged with a heap — [merge-k-sorted-lists](../learning/10-heap-priority-queue.md) with infrastructure around it.

**Normalize the cache:** feed lists hold **post IDs only**; a separate post cache maps ID → content. An edited post is updated once, not in 10M materialized copies — Step 2 already showed why the multiplied structure must hold the small thing.

**Fan-out is async:** post creation writes the post, emits an event, returns 201. Workers consume from a [queue](../system-design/05-queues-streams.md) and do the pushing — post latency stays flat no matter the follower count.
</details>

<details>
<summary>Step 4 — Deep dives & what interviewers probe</summary>

**"Where does ranking happen?"** — The cached lists are chronological; ranking is a read-time step: feed service assembles ~200 candidate IDs (pushed + pulled), hydrates features, scores, returns the top 20. Ranking at write time would bake a stale model's opinion into 10M lists — at read time you rank only what one user actually sees, with the current model. Chronological storage, ranked serving.

**"A user deletes a post — it's already in a million feed lists."** — Don't chase the copies. Because lists hold only IDs, filter at read: hydration against the post cache fails-or-flags for deleted IDs and the feed service drops them. Lazy repair prunes dead IDs when a list is next read. Edits are even easier — content lives once in the post cache, so every feed sees the edit immediately. This probe is *why* normalization was the right call; connect it back.

**"New user follows 50 people — their feed cache is empty."** — Cold start: fall back to pull-and-merge for their first load (build the feed at read time from followees' recent posts), then backfill their cached list asynchronously. Same fallback covers cache eviction of dormant users — the pull path is your universal recovery story, another argument for the hybrid.

**"A celebrity posts and 10M followers refresh at once."** — The pull side saves the write stampede but creates a read hot spot: 10M feed loads all fetching the same celebrity's recent posts. Answer: that's one tiny, identical, hot value — replicate it across the post-cache fleet (or short-TTL it at the feed-service layer). Hot *reads* of one key are the easy problem; hot *writes* to 10M keys were the hard one — the hybrid deliberately traded the second for the first.

**Common mistakes at this design:**
- Picking pure push or pure pull without doing the celebrity/scroller arithmetic — the numbers, not taste, force the hybrid.
- Materializing full post bodies into feed lists — the delete/edit probe then has no good answer.
- Fanning out synchronously inside the POST request.
- Offset pagination on a list that shifts under the reader.
</details>

---

**Next on the ladder:** [Design a Chat System →](07-chat-system.md) — the first design where the server must push to the client, and stateless HTTP finally isn't enough.
