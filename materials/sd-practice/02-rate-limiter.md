# 02. Design a Rate Limiter — Entry

The Design Ladder works like the DSA practice sets: attempt first, then peek. Work the design on paper against the [framework template](../appendix/templates/system-design/template.md) for a full 45 minutes before opening any step below — the struggle *is* the practice.

[← Back to the lesson](../system-design/06-first-designs.md) · [🗺 Interview Roadmap](../../interview.md)

---

## The prompt

> "Design a rate limiter for our public API — say, 100 requests per user per minute. It should work as middleware or a shared service that any of our app servers can call before handling a request."

Typical follow-up constraints when you ask (and you should ask — that's Step 1):

- ~10M users; different endpoints may want different limits.
- The check must add **< 1ms** of latency — it runs on *every* request.
- Many app servers behind a load balancer; the limit is global per user, not per server.
- Rejected requests get a **429** plus headers telling the client its remaining quota and when to retry.

Why this design? It's the infrastructure cousin of your [sliding-window](../learning/03-sliding-window.md) drilling — the same "count events in a moving window" pattern, except now the counter lives in Redis and the failure modes are distributed. It also has a genuinely rich algorithm choice for such a small system.

<details>
<summary>Step 1 — Requirements & API</summary>

**Functional:**
- Allow or reject a request based on a per-user (or per-IP, or per-API-key) count against a configured limit.
- Return 429 with `Retry-After` and `X-RateLimit-Remaining` / `X-RateLimit-Limit` headers on rejection.
- Rules configurable per endpoint (login endpoints stricter than read endpoints).

**Non-functional:**
- **< 1ms added latency** — this sits in the hot path of every single request.
- Accurate *enough*: a few percent over-admission during a race is acceptable; silently blocking legitimate users is not.
- Highly available — and you must decide what happens when the limiter itself is down (fail-open vs fail-closed, Step 4).

**API sketch:**

```
# As middleware, the "API" is a function call:
allow(key="user:42", rule="api-default")  →  { allowed: true, remaining: 37, reset_at: 1720000060 }

# On rejection, the client sees:
HTTP 429 Too Many Requests
Retry-After: 23
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
```

One decision worth saying out loud: **what's the key?** Per-user needs authentication first (rate-limit *after* auth); per-IP catches unauthenticated abuse but punishes users behind a shared NAT; per-API-key suits B2B. Real systems layer several — say that, then design one and note the key is pluggable.
</details>

<details>
<summary>Step 2 — Estimates</summary>

Keep it to one-significant-figure math (the [estimation recipes](../system-design/00e-estimation.md)):

- **Check QPS = total API QPS.** 10M users, say 1M active per hour making ~30 requests each → 30M/hour ≈ **10K checks/s**, peak maybe 30K/s. Every one of these hits the counter store.
- **Storage per counter:** a key (~40 bytes) plus a count and timestamp (~20 bytes) ≈ 60–100 bytes. 10M users × ~100 bytes ≈ **1 GB** — trivially fits in one Redis instance's memory.
- **A sliding window *log*** (store every request timestamp) would instead cost 100 timestamps × 8 bytes × 10M users ≈ **8 GB and growing with the limit** — the estimate itself argues against that algorithm at this scale.
- **Latency budget:** one Redis round trip on the same network ≈ 0.5ms. One trip fits the < 1ms budget; two don't — so whatever algorithm you pick must resolve in a **single atomic operation**.

The numbers just decided two things: counters (not logs) for memory, and one-round-trip atomicity for latency.
</details>

<details>
<summary>Step 3 — High-level design</summary>

```
 client ──► ┌─────────────┐      ┌──────────────────┐
            │ API Gateway │ ───► │   App Servers    │
            │  / middle-  │      │  (the real work) │
            │    ware     │      └──────────────────┘
            └──────┬──────┘
                   │ allow(key)?  — one atomic op
            ┌──────▼──────┐
            │    Redis    │  key: user:42:bucket → { tokens, last_refill }
            │ (counters)  │  rules cached in-process at the gateway
            └─────────────┘
       429 + headers ◄── if not allowed
```

**Where it sits:** at the gateway/middleware layer, *before* requests reach app servers — rejecting early is the whole point. Rules (limits per endpoint) are config, cached in-process and refreshed periodically; only the counters need shared state.

**The algorithm decision** — the heart of this design; compare at least three:

1. **Fixed window** — one counter per user per minute (`user:42:12:05 → 87`). Dead simple, but suffers the **boundary burst**: 100 requests at 12:05:59 and 100 more at 12:06:01 is 200 requests in two seconds, all allowed.
2. **Sliding window log** — store every request timestamp, count those within the last 60s. Perfectly accurate, but memory scales with the limit (Step 2 said ~8 GB vs ~1 GB) and each check touches many entries.
3. **Sliding window counter** — current window's count plus a weighted fraction of the previous window's. One counter pair, approximately accurate, fixes the boundary burst. A solid answer.
4. **Token bucket** — each user has a bucket of 100 tokens refilling at 100/min; a request spends a token. Same memory as a counter, and it **allows short bursts** up to bucket size while enforcing the average rate — usually what APIs actually want (a client retrying a batch shouldn't be treated like an attacker).

Pick **token bucket**: counter-sized memory, burst tolerance as a feature not a bug, and it degrades gracefully into "sliding-ish window" behavior. Say when you'd switch — hard regulatory caps ("never more than 100 in any 60s, period") push you to the sliding window log despite the memory.

**Making it atomic:** store `{tokens, last_refill}` per key and run refill-then-decrement as a **Lua script in Redis** (or `INCR` + `EXPIRE` for the counter variants). One script, one round trip, no read-modify-write race between gateways.
</details>

<details>
<summary>Step 4 — Deep dives & what interviewers probe</summary>

**"Two gateways check the same user at the same instant — do you over-admit?"** — Only if the check is read-then-write across two round trips. The Lua script (or atomic `INCR`) makes the whole refill-and-spend a single serialized operation inside Redis, so concurrent checks queue up correctly. If you shard Redis later, a user's key lives on exactly one shard, so atomicity survives sharding.

**"Redis is down. Now what?"** — The probe favorite, because it's a product decision wearing an ops costume. **Fail-open** (let everything through) keeps the API alive but drops your abuse protection; **fail-closed** (reject everything) turns a limiter outage into a full outage. Default answer: fail-open for general API limits, fail-closed for the endpoints where the limit *is* the security control (login attempts, OTP sends) — and alert loudly either way. Bonus: a small in-process local limiter as a degraded backstop.

**"Does every request really need a Redis round trip?"** — At 10K–30K/s, Redis handles it comfortably (single instance does ~100K ops/s). If you outgrow that: shard by user key, or move to a local-counter-with-async-sync scheme — each gateway limits against `limit / N` locally and reconciles — trading accuracy for zero network hops. Name the trade-off; don't pretend it's free.

**"How does the client know to back off?"** — The 429 alone trains clients to hammer-and-retry. `Retry-After` and the `X-RateLimit-*` headers let well-behaved clients pace themselves — cheap to add, and mentioning them signals you've been on the client side of one of these.

**Common mistakes at this design:**
- Read-modify-write across two Redis calls — the race the interviewer is fishing for.
- Picking sliding window log without owning its memory cost (Step 2 already told you).
- No answer for the limiter's own failure — fail-open vs fail-closed *is* the senior-signal question.
- Putting the limiter after the app servers, where rejecting a request no longer saves any work.
</details>

---

**Next on the ladder:** [Design Typeahead / Autocomplete →](03-typeahead.md) — the trie you built in DSA practice meets a latency budget measured per keystroke.
