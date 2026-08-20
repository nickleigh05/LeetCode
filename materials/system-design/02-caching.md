# 02. Caching

*Store the answer once, serve it a million times — the highest-leverage box in any design.*

[← Prev](01-design-framework.md) · [🗺 Interview Roadmap](../../interview.md) · [Next →](03-load-balancing.md)

---

> **Builds on:** [Hash Maps](../learning/01-arrays-hashing.md) — a cache *is* a hash map with a size limit and an expiry policy — and the [LRU Cache](../learning/07-linked-list.md) problem, which is the eviction algorithm you'll name in almost every design. Read [Estimation](00e-estimation.md) first if you haven't: cache decisions are justified with numbers.

Almost every system you design in an interview is read-heavy — feeds, profiles, product pages, short links. A database read costs milliseconds; a memory read costs microseconds. Caching is how you spend a little memory to buy back three orders of magnitude of latency, and it's usually the first deep dive an interviewer steers into. The concept is one line; the interview lives in the failure modes — staleness, stampedes, and hot keys.

## Concept

### The Cache Hierarchy

```
  Client ──► CDN ──► Load Balancer ──► App Server ──► Distributed Cache ──► Database
             │                          │              │                     │
             │ static assets,           │ in-process   │ Redis/Memcached:    │ the source
             │ full pages,              │ memory:      │ hot rows, sessions, │ of truth —
             │ ~10–100ms saved          │ ns reads,    │ computed results    │ protect it
             │ per request              │ per-server   │ ~1ms, shared        │
```

**What it is:** A hierarchy of "have I answered this before?" checks, each one closer and faster than the last. Every layer absorbs traffic so the layers behind it see less.

**Key Properties:**
- A cache is **smaller than the data it fronts** — something must be evicted, so you need a policy (LRU is the default answer).
- Cached data is **stale by definition** — the question is never "is it stale?" but "how stale is acceptable?"
- The **hit rate** decides everything: at 99% hits, the database sees 1% of traffic; at 90%, it sees 10× more than that.

**Where each layer wins:**

| Layer | Latency | Shared? | Typical contents |
|-------|---------|---------|------------------|
| Browser / device | ~0 (local) | No | Static assets, API responses with `Cache-Control` |
| CDN | ~10–50ms | Per region | Images, video, JS bundles, sometimes full pages |
| In-process (app memory) | ~100ns | No — per server | Config, feature flags, tiny hot lookups |
| Distributed (Redis/Memcached) | ~1ms | Yes | Hot DB rows, sessions, computed feeds, counters |

**Use when:**
- Reads heavily outnumber writes (10:1 or more — check with your [estimates](00e-estimation.md))
- The same keys are requested repeatedly (power-law access: a few keys get most of the traffic)
- Slightly stale data is acceptable — or you're prepared to pay for invalidation

### Write Strategies

```
  CACHE-ASIDE (lazy)                 WRITE-THROUGH                  WRITE-BACK (risky)
  read:  cache miss? → read DB       write: cache + DB together     write: cache only,
         → fill cache → return              (synchronous)                  flush to DB later
  write: write DB → invalidate key
  ┌─────┐  1. miss   ┌─────┐         ┌─────┐  write both  ┌─────┐   ┌─────┐  write   ┌─────┐
  │ App │───────────►│Cache│         │ App │─────────────►│Cache│   │ App │─────────►│Cache│
  └─────┘◄───────────└─────┘         └─────┘─────────────►│ DB  │   └─────┘          └──┬──┘
     │ 2. read DB, 3. fill                                └─────┘        async flush ▼
     ▼                                                                            ┌─────┐
  ┌─────┐                                                                         │ DB  │
  │ DB  │                                                                         └─────┘
  └─────┘
```

**What it is:** The contract between the cache and the source of truth. Who writes where, and when.

**Trade-offs:**

| Strategy | Read path | Write path | Failure mode |
|----------|-----------|------------|--------------|
| Cache-aside | Miss → DB → fill | DB, then invalidate | First read after write is a miss (fine) |
| Write-through | Always warm | Slower — two writes, synchronous | Write latency; caches data never read |
| Write-back | Always warm | Fast — cache only | **Data loss** if cache dies before flush |

**Use when:** Cache-aside is the default — say it first, deviate only with a reason. Write-through when reads-after-writes must hit warm data (user just edited their profile). Write-back almost never in an interview, except for things you can afford to lose (view counters, metrics).

**Python:**
```python
def get_user(user_id):
    user = cache.get(f"user:{user_id}")      # ~1ms
    if user is None:                          # miss
        user = db.query_user(user_id)         # ~10ms
        cache.set(f"user:{user_id}", user, ttl=3600)
    return user

def update_user(user_id, fields):
    db.update_user(user_id, fields)           # source of truth first
    cache.delete(f"user:{user_id}")           # invalidate — next read refills
```

Invalidate, don't update, on write — updating the cache from two places invites race conditions where the cache ends up holding the older value forever.

### Eviction & Expiry

**What it is:** The cache is full, or the data is old. Eviction picks a victim when space runs out; TTL (time-to-live) expires entries on a clock.

**Key Properties:**
- **LRU** (least recently used) is the default eviction policy — it's literally [the LeetCode problem](../learning/07-linked-list.md): hash map + doubly linked list, O(1) everything. **LFU** (least frequently used) resists one-off scans flushing your hot set but is more bookkeeping.
- **TTL** is your staleness ceiling *and* your invalidation safety net: even if an invalidation is missed, the entry dies within one TTL.
- Short TTL = fresher data, more DB load. Long TTL = better hit rate, staler data. Say the trade-off out loud; pick a number ("5 minutes for a profile page") and move on.

### Invalidation, Stampedes & Hot Keys

**What it is:** The three failure modes interviewers actually probe. Naming them unprompted is a strong senior signal.

- **Stale data after writes** — cache-aside + invalidate-on-write covers most of it; TTL catches the leaks. If a design truly can't tolerate staleness for some read, don't cache that read.
- **Cache stampede (thundering herd)** — a hot key expires and 10,000 concurrent requests all miss and hit the database at once. Fixes: **per-key locking** (first miss rebuilds, the rest wait), **stale-while-revalidate** (serve the old value while one request refreshes), or **jittered TTLs** so keys don't expire in synchronized waves.
- **Hot keys** — one celebrity's profile gets 100× the traffic of everything else and overwhelms the single cache node holding it. Fixes: replicate the hot key across nodes, or add a tiny in-process cache in front of the distributed one. (How keys map to nodes is [consistent hashing →](08-partitioning.md).)
- **Cold start** — a freshly restarted cache has a 0% hit rate and the database eats the full load. Mention cache warming for planned restarts.

## The Pattern — Cache-Aside with Invalidation

Nearly every design on the [ladder](../../interview.md#the-design-ladder) caches the same way. The moves, in order:

1. **Justify it with numbers** — "100:1 read:write ratio, so I'll cache reads" (from your Step-2 estimates).
2. **Place the box** — a distributed cache (name Redis) between app servers and the database.
3. **Name the strategy** — cache-aside; writes invalidate.
4. **Name eviction + TTL** — LRU, plus a TTL matched to acceptable staleness.
5. **Volunteer one failure mode** — stampede or hot keys, with its fix. This is the step that separates candidates.

The invariant to protect: **the database is the source of truth; the cache is always allowed to be wrong for at most TTL seconds.** Any design where the cache is the only copy of something is a write-back cache, and you should say the data-loss risk out loud.

## The Template

The design-interview worksheet lives in [`appendix/templates/system-design/`](../appendix/templates/system-design/). Read the README (when to reach for each component, common traps), then work designs against [`template.md`](../appendix/templates/system-design/template.md) — caching decisions land in Step 3 (high-level) and get probed in Step 4 (deep dives).

## Practice

Caching is the star of [**Design a Distributed Cache →**](../sd-practice/09-distributed-cache.md) (you build the thing itself) and does heavy lifting in [**Typeahead →**](../sd-practice/03-typeahead.md) and [**Design a URL Shortener →**](../sd-practice/01-url-shortener.md). Every other design on the [ladder](../../interview.md#the-design-ladder) will ask you to place a cache and defend the choice.

## Check Yourself

- [ ] I can draw the four cache layers and say what lives at each one.
- [ ] I can explain cache-aside vs write-through vs write-back and pick one with a reason.
- [ ] I can describe a cache stampede and name two fixes.
- [ ] Given "100M reads/day, 1M writes/day," I can justify a cache with numbers and pick a TTL.

---

**Up next:** [Load Balancing & Horizontal Scaling](03-load-balancing.md) — many copies of your server, one front door.

[← Prev](01-design-framework.md) · [🗺 Interview Roadmap](../../interview.md) · [Next →](03-load-balancing.md)
