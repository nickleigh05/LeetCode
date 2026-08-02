# 04. Design a Top-K Leaderboard — Mid

The Design Ladder works like the DSA practice sets: attempt first, then peek. Work the design on paper against the [framework template](../appendix/templates/system-design/template.md) for a full 45 minutes before opening any step below — the struggle *is* the practice.

[← Back to the lesson](../system-design/05-queues-streams.md) · [🗺 Interview Roadmap](../../interview.md)

---

## The prompt

> "Design a real-time leaderboard for an online game — show the global top 10, and let any player see their own current rank."

Typical follow-up constraints when you ask (and you should ask — that's Step 1):

- **~50M DAU** submitting score updates as they play.
- The top 10 should be near-real-time — a score change shows up within seconds.
- A player's *own* rank may lag slightly; nobody notices if rank #23,481,932 is a minute stale.
- (Ask!) Is the key space bounded — 50M known players — or unbounded, like "top trending hashtags"? The answer changes the design.

Why this design? Top-K is the [heap pattern](../learning/09-heap-priority-queue.md) wearing infrastructure clothes — and it's a rare prompt where the pragmatic answer is a single well-chosen data structure, so the interview becomes about knowing *when* that stops being enough.

<details>
<summary>Step 1 — Requirements & API</summary>

**Functional:**
- Update a player's score (increment or set).
- Read the global top 10 (with names and scores).
- Read a specific player's rank and score on demand.
- (Confirm scope) time-windowed boards — daily/weekly — and friends-only boards.

**Non-functional:**
- Top-10 reads are the hot path and must be fast and fresh (seconds).
- Own-rank reads can be slightly stale — say this out loud; it's the relaxation that makes the design tractable.
- Score updates must not be lost — a player who earns points and doesn't see them files a support ticket.

**API sketch:**

```
POST /api/scores
  body: { "player_id": "p42", "delta": 150 }
  returns 202

GET /api/leaderboard/top?n=10
  returns 200: { "entries": [ { "rank": 1, "player": "...", "score": 982431 }, ... ] }

GET /api/leaderboard/rank/p42
  returns 200: { "rank": 1042387, "score": 8210 }
```

One decision worth saying out loud: **increments vs absolute scores.** Increments (`delta`) make retries dangerous — a replayed request double-counts — so pair them with an idempotency key, or submit absolute scores where the game server is the source of truth. Small API detail, real correctness consequence.
</details>

<details>
<summary>Step 2 — Estimates</summary>

Keep it to one-significant-figure math (the [estimation recipes](../system-design/00e-estimation.md)):

- **Write QPS:** 50M DAU, each submitting ~10 score updates/day → 500M/day ≈ **6K writes/s**, peak ~20K/s.
- **Read QPS:** top-10 is displayed constantly — assume similar order, ~10K reads/s; but it's *one identical answer for everyone*, so a 1-second cache turns 10K/s into 1/s at the source. Own-rank reads are per-player and can't be shared, but tolerate staleness.
- **Storage:** 50M members × (~10-byte ID + 8-byte score + overhead) ≈ 30 bytes each in a sorted-set encoding → **~1.5–5 GB with overhead**. Fits in one Redis instance's memory, comfortably.
- **Throughput check:** 20K peak writes/s against a single Redis doing ~100K ops/s — fine, with headroom.

The numbers just said something important: at 50M *bounded* members and 20K writes/s, this fits in one in-memory sorted structure. Don't shard what fits.
</details>

<details>
<summary>Step 3 — High-level design</summary>

```
 game servers ──► ┌─────────────┐    ┌──────────────────────┐
  (score events)  │ Score       │───►│ Redis sorted set     │
                  │ service     │    │ ZINCRBY board p42 150│
                  └─────────────┘    │ ZREVRANGE board 0 9  │
                                     │ ZREVRANK board p42   │
 GET /top ──────► ┌─────────────┐    └──────────▲───────────┘
 GET /rank ─────► │ Leaderboard │───────────────┘
                  │ service +   │    ┌──────────────────────┐
                  │ 1s top-10   │    │ Durable store (SQL/  │
                  │ cache       │    │ NoSQL): score history│
                  └─────────────┘    └──────────────────────┘
```

**The core decision** — exact vs sharded vs approximate; compare all three, pick per variant:

1. **A single Redis sorted set** — the pragmatic answer for a bounded key space. `ZINCRBY` on write, `ZREVRANGE 0 9` for top-10, `ZREVRANK` for own rank — every operation is O(log N) in one round trip, and 50M members fit in memory (Step 2). This *is* a balanced-tree/skip-list keyed by score — the heap pattern's big sibling, maintained server-side. Redis persists (AOF) but treat it as the serving copy; the durable store holds score history and can rebuild the set.
2. **Sharded aggregation + periodic merge** — when members or write volume outgrow one node: shard players across K sorted sets, each shard reports its local top 10, a merger takes the true global top 10 from K×10 candidates (correct because a global top-10 member is necessarily in its own shard's top 10 — the merge-k-lists heap argument). Global *rank* gets harder: sum of per-shard ranks, computed lazily.
3. **Count-min sketch + heap** — for *unbounded* key spaces (trending hashtags, hot URLs) where you can't hold every key: a count-min sketch approximates each key's count in fixed memory; a small min-heap of size K tracks the current top-K, updated as events stream past — literally the [heap lesson's](../learning/09-heap-priority-queue.md) top-K pattern, made probabilistic. Approximate counts, tiny memory, no rank-for-arbitrary-key.

For this prompt — 50M bounded players — pick the **sorted set**, and name the switching conditions: shard when memory or write throughput outgrows one node; go sketch+heap when the key space is unbounded and approximation is acceptable.

**Top-10 serving:** cache the `ZREVRANGE` result for ~1 second in the leaderboard service. Freshness requirement met, and the sorted set never feels the read load.
</details>

<details>
<summary>Step 4 — Deep dives & what interviewers probe</summary>

**"What's the exact rank of player #23,481,932 — and does it need to be exact?"** — Push back on the requirement first: deep ranks are cosmetic. `ZREVRANK` gives it exactly and cheaply here, but in the sharded design exact deep rank means summing across shards — expensive. The standard relaxation is **order-of-magnitude bucketing**: maintain a histogram of score ranges (players with score 8,000–8,999: 1.2M), locate the player's bucket, interpolate — "roughly #23.5M" computed from a few hundred counters, refreshed every minute. Nobody at rank 23M can tell the difference.

**"Daily and weekly boards?"** — Per-window keys, not one mutable board: `board:2026-07-15`, `board:2026-W29`. Writes `ZINCRBY` into every active window; each key gets a TTL a bit past its window so old boards expire themselves. Reset bugs disappear because nothing ever resets — new window, new key.

**"One player's score updates 1,000 times a second — hot key?"** — A single member updating fast is actually fine for a sorted set (each op is O(log N)), but if event volume itself is the problem, batch: aggregate deltas per player in the score service for ~1 second and issue one `ZINCRBY` with the sum. Trades a second of freshness for a 1,000× write reduction — and the requirements already granted that second.

**"Redis dies. Where did the leaderboard go?"** — Two-part answer: replica failover for availability ([replication](../system-design/07-replication.md)), and the durable score store as the source of truth from which the sorted set is rebuilt (a scan-and-`ZADD` job). The sorted set is a serving index, not the system of record — that framing is the senior signal.

**Common mistakes at this design:**
- Reaching for sharded stream processing when Step 2 said 5 GB and 20K/s fit in one sorted set — over-engineering the exact case.
- Not asking whether the key space is bounded — the fork that decides exact vs approximate.
- Treating Redis as the only copy of scores with no rebuild path.
- Recomputing the top 10 by scanning a SQL table per request — the "no index on the pattern" smell.
</details>

---

**Next on the ladder:** [Design a Notification System →](05-notification-system.md) — the first design where queues stop being a bullet point and become the whole architecture.
