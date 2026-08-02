# 01. Design a URL Shortener — Entry

The Design Ladder works like the DSA practice sets: attempt first, then peek. Work the design on paper against the [framework template](../appendix/templates/system-design/template.md) for a full 45 minutes before opening any step below — the struggle *is* the practice.

[← Back to the lesson](../system-design/06-first-designs.md) · [🗺 Interview Roadmap](../../interview.md)

---

## The prompt

> "Design a URL shortener — like bit.ly. Users submit a long URL and get back a short one; anyone who opens the short link gets redirected to the original."

Typical follow-up constraints when you ask (and you should ask — that's Step 1):

- 100M new URLs per month; a read:write ratio around 10:1.
- Short links should be as short as possible and must not collide.
- Redirects should feel instant. Creation can be slower.
- Links live for years. Custom aliases and click analytics are nice-to-haves — confirm whether they're in scope.

Why this design first? It's the classic opener: small enough to finish, but it forces every fundamental — an API, an ID-generation choice, a SQL-vs-NoSQL call, a cache with real numbers behind it — which is why interviewers keep using it.

<details>
<summary>Step 1 — Requirements & API</summary>

**Functional:**
- Shorten: given a long URL, return a unique short URL.
- Redirect: given a short URL, send the user to the long one.
- (Confirm scope) custom aliases, expiration, click counts.

**Non-functional:**
- Redirects are the hot path: low latency (< 100ms) and high availability — a broken redirect is a broken link on someone else's site.
- Short codes must never collide; two users can shorten the same long URL independently.
- Read-heavy: design for the 10:1 ratio.

**API sketch:**

```
POST /api/urls
  body: { "long_url": "https://example.com/some/very/long/path" }
  returns 201: { "short_url": "https://sho.rt/a8Xk2Pq" }

GET /{code}
  returns 301/302 redirect → long_url
```

One decision worth saying out loud: **301 (permanent) vs 302 (temporary) redirect.** 301 lets browsers cache the redirect — less load on you, but you lose analytics because repeat clicks never reach your servers. If click counts matter, use 302. This tiny question is a favorite interviewer probe precisely because it connects a product requirement to an infrastructure consequence.
</details>

<details>
<summary>Step 2 — Estimates</summary>

Keep it to one-significant-figure math (the [estimation recipes](../system-design/00e-estimation.md)):

- **Write QPS:** 100M / month ≈ 100M / 2.6M seconds ≈ **40 writes/s**, call peak ~100/s.
- **Read QPS:** 10:1 → **400 reads/s**, peak ~1,000/s. Modest — a handful of servers, not a Google problem. Saying "this is actually small" is a good look.
- **Storage:** ~500 bytes per row (long URL, code, timestamps, user) × 100M/month ≈ **50 GB/month → ~3 TB over 5 years**. Fits comfortably in one well-indexed database with room to spare.
- **Code length:** base62 (`a–z A–Z 0–9`). 62⁷ ≈ 3.5 × 10¹² — seven characters covers trillions of URLs. Six (62⁶ ≈ 57B) is enough for years at this rate, but 7 is the safe answer.

The estimates just earned their keep: they tell you sharding is unnecessary, a cache is justified (read-heavy), and 7 characters is provably sufficient — three design decisions from thirty seconds of arithmetic.
</details>

<details>
<summary>Step 3 — High-level design</summary>

```
                        ┌──────────────┐
   POST /api/urls ────► │              │        ┌───────────────┐
                        │ App Servers  │ ─────► │   Database    │
   GET /{code} ───────► │ (stateless,  │        │ code → long   │
        │               │  behind LB)  │        │ URL (indexed) │
        │               └──────┬───────┘        └───────────────┘
        │                      │ cache-aside
        │               ┌──────▼───────┐
        └── 301/302 ◄── │ Redis cache  │  hot codes → long URL
                        └──────────────┘
```

**The write path (shorten):** app server generates a code, stores `code → long_url`, returns the short URL.

**The code-generation decision** — the heart of this design; name at least two options and pick one:

1. **Hash the long URL** (MD5, take first 7 base62 chars) — same URL always gives the same code, but collisions need probing (append a counter and re-hash), and two users shortening the same URL share a code (bad if links are per-user).
2. **Auto-increment counter, base62-encode it** — collision-free by construction, trivially simple. Codes are predictable/enumerable (`a8Xk2Pq` tells you roughly how many URLs exist); fine unless links must be unguessable. Single counter is a bottleneck at scale — fixable with ranged allocation (each server leases a block of 10,000 IDs).
3. **Pre-generated key pool** — a background job fills a table of unused random codes; servers claim one per write. Collision-free *and* unguessable, at the cost of one more moving part.

Counter + base62 is the clean default answer at this scale; say when you'd switch (unguessability requirement → key pool).

**The read path (redirect):** look up the code in Redis (cache-aside); on miss, read the DB, fill the cache, redirect. With power-law link popularity, a cache holding the top ~20% of codes absorbs the vast majority of the 400 reads/s.

**Database choice:** this is a single-table key-value lookup — no joins, no transactions across rows. Anything works, so say *that*, then pick: PostgreSQL with an index on `code` is entirely sufficient for 3 TB / 1,000 QPS; a key-value store (DynamoDB) is the answer if the interviewer pushes scale 100×.
</details>

<details>
<summary>Step 4 — Deep dives & what interviewers probe</summary>

**"What happens at 100× the scale?"** — The single database is the first thing to break. Answers, in order: read replicas (reads scale out; the [replication lesson](../system-design/07-replication.md)), then partition by code ([consistent hashing](../system-design/08-partitioning.md)) when writes or storage outgrow one machine. Because codes are random-ish, hash partitioning distributes evenly — no hot shard.

**"How do click analytics work without slowing redirects?"** — Don't write a counter synchronously in the redirect path (a hot link would hammer one row). Emit an event to a [queue](../system-design/05-queues-streams.md) and aggregate asynchronously; redirects stay fast, counts are eventually consistent — and say that trade-off out loud.

**"What about expired or deleted links?"** — TTL column checked on read (return 410), plus a lazy background sweep. Cheap and honest; nobody expects a distributed cron masterpiece here.

**"Can the cache serve a stale redirect?"** — Only if URLs are mutable (edit/delete). Invalidate on write, TTL as the backstop — the exact pattern from the [caching lesson](../system-design/02-caching.md).

**Common mistakes at this design:**
- Jumping straight to sharding/Kafka/microservices — the estimates say one database is fine; over-engineering reads worse than under-engineering.
- Hand-waving code generation ("just hash it") without owning collisions.
- Forgetting the 301-vs-302 consequence for analytics.
- Never using the numbers from Step 2 to justify anything.
</details>

---

**Next on the ladder:** [Design a Rate Limiter →](02-rate-limiter.md) — your sliding-window drilling pays off in infrastructure form.
