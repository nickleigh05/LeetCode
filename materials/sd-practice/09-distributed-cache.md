# 09. Design a Distributed Cache — Senior

The Design Ladder works like the DSA practice sets: attempt first, then peek. Work the design on paper against the [framework template](../appendix/templates/system-design/template.md) for a full 45 minutes before opening any step below — the struggle *is* the practice.

[← Back to the lesson](../system-design/08-partitioning.md) · [🗺 Interview Roadmap](../../interview.md)

---

## The prompt

> "Design a distributed cache — Redis or Memcached as a service. Application teams across the company call GET/SET/DELETE with TTLs; you provide the fleet behind it."

Typical follow-up constraints when you ask (and you should ask — that's Step 1):

- ~1M ops/s aggregate, heavily read-skewed.
- Sub-millisecond p99 — that's the entire reason a cache exists.
- ~10 TB working set, so this doesn't fit on one machine.
- The cache is *not* the source of truth, but availability matters — a cold cache stampedes the databases behind it.
- Nodes must be added and removed without a mass miss event.

This is the "build the thing you've been using" design — every ladder rung so far *called* a cache; now you're on the other side of the API, and the [partitioning](../system-design/08-partitioning.md) and [replication](../system-design/07-replication.md) lessons stop being abstractions.

<details>
<summary>Step 1 — Requirements & API</summary>

**Functional:**
- `GET(key)`, `SET(key, value, ttl)`, `DELETE(key)`.
- TTL expiry — entries vanish on schedule without client action.
- (Confirm scope) atomic increment, batch multi-get? Nice-to-haves; nail the core three first.

**Non-functional:**
- **Latency is the product:** sub-ms p99 means everything lives in RAM and every request touches exactly one cache node — no multi-hop reads, no disk on the hot path.
- Availability over consistency — and say why: a cache is *allowed to be wrong* (miss or brief staleness), because the source of truth is behind it. That one sentence licenses every relaxed choice below.
- Elastic: adding node N+1 must not invalidate the world.
- Multi-tenant: one team's hot key shouldn't starve another's (namespacing + per-tenant quotas — mention, don't dwell).

**API sketch:**

```
GET    /cache/{key}                    → 200 value | 404 miss
PUT    /cache/{key}   body: { "value": ..., "ttl_s": 300 }
DELETE /cache/{key}
```

In practice this is a binary protocol over persistent TCP connections, not HTTP — at sub-ms budgets, HTTP header parsing is real money. Saying so is a cheap senior signal.
</details>

<details>
<summary>Step 2 — Estimates</summary>

One-significant-figure math (the [estimation recipes](../system-design/00e-estimation.md)):

- **Throughput per node:** an in-memory hash lookup is O(1) and cheap; a tuned cache node does ~100K ops/s comfortably. 1M ops/s → **~10 nodes for throughput**.
- **Memory per node:** 10 TB working set / ~100 GB usable RAM per node → **~100 nodes for storage**. Storage, not CPU, sizes this fleet — say that, it's the punchline.
- So: **~100 nodes**, each loafing at ~10K ops/s. Add replication (×2) → ~200 nodes.
- **Latency budget:** sub-ms p99 = one network round trip (~0.1–0.5 ms in-datacenter) + an in-memory lookup (~µs). There is no budget for a proxy hop *and* a disk read *and* a second hop — the math forbids multi-hop designs.
- **Key movement on resize:** with 100 nodes, adding one should move ~1/100th of keys (~100 GB), not 10 TB. That single expectation *is* the argument for consistent hashing.

The numbers just decided the architecture: ~100+ nodes (so partitioning is mandatory, not optional), one-hop routing (so clients must know the topology), and consistent hashing (so a resize moves 1% of keys instead of 100%).
</details>

<details>
<summary>Step 3 — High-level design</summary>

```
  App servers (cache client library)
  │  hash(key) → position on ring → node   (client-side routing)
  │
  ▼            the ring (consistent hashing, virtual nodes)
        n3•                 •n1
     ┌──────┐  key "user:42" hashes here ──┐
     │      •n7                            ▼
     n1•         each physical node       •n1  ← owner
     │           appears ~100× as         │
     └──• n2     virtual nodes ──────• n5─┘
                     │
            ┌────────▼────────┐   async ┌─────────────┐
            │  Cache node     │ ──────► │  Replica    │
            │  hash map + LRU │         │ (same shard)│
            └─────────────────┘         └─────────────┘
```

**Partitioning — walk the ring, it's the key decision.** Hash each node onto a circle; a key belongs to the first node clockwise from `hash(key)`. Compare the options:

1. **`hash(key) mod N`** — trivial, but N changing from 100→101 remaps ~99% of keys. One scale-out event = a cold cache = a database stampede. Disqualified by the resize requirement.
2. **Consistent hashing** — when a node joins or leaves, only **~K/N keys move** (~1% here); everyone else's entries are untouched. This is the [partitioning lesson](../system-design/08-partitioning.md) cashing out.
3. **Central directory (lookup service maps key-range → node)** — flexible, but it puts a hop or a coordination service on a sub-ms hot path. Overkill for a cache; the right tool for a database, not here.

Pick **consistent hashing with virtual nodes** — each physical node appears ~100–200 times on the ring, so load spreads evenly and a departing node's keys scatter across *all* survivors instead of dogpiling one clockwise neighbor.

**Routing — who computes the ring position?** Three options: a **proxy tier** (extra hop — eats the latency budget), **gossip among cache nodes** with any-node routing (extra internal hop), or **smart clients** — the client library holds the ring topology (fetched from a small config service, watched for changes) and talks straight to the owner. Pick smart clients: zero extra hops, and topology changes are rare and push-able. Cost: every client language needs a library — real, and worth saying.

**Inside one node: the LRU you already built.** Each node is a **hash map + doubly linked list** — O(1) get, O(1) set, O(1) evict-least-recent, exactly the [LRU cache](../data-structures/lru-cache.md) from the [linked-list lesson](../learning/06-linked-list.md). This is the best DSA-to-systems bridge on the ladder — take the ten seconds to draw it. Memory is managed with **slab allocation** (namecheck: fixed-size chunks per size class, so long-running processes don't fragment).

**TTL vs eviction — two different removals:** *expiry* is lazy (check timestamp on read, return miss if dead) plus a periodic sampling sweep to reclaim memory from keys nobody reads; *eviction* is the LRU kicking out live entries under memory pressure. Different triggers, different mechanisms — conflating them is a common flub.

**Replication — cache semantics make it easy.** One **async replica per partition** ([replication lesson](../system-design/07-replication.md)): writes go to the primary and stream to the replica with no ack wait. Losing the primary loses a few in-flight writes — which in a cache are just *future misses*, not lost data. The source of truth refills them. This is availability-over-consistency chosen *because the domain permits it* — the senior move is naming why it's safe here and wouldn't be for the payment system three rungs up.
</details>

<details>
<summary>Step 4 — Deep dives & what interviewers probe</summary>

**"A node dies and its replica is cold or absent — what happens to the databases behind you?"** — The **thundering herd**: 1% of keys miss at once and every app server independently queries the DB for the same hot keys. Defenses, in order: replicas take over warm (the main answer); **request coalescing** in the client — one flight per key per app server, everyone else waits on that future; and jittered TTLs so mass expiry never synchronizes. Naming the herd before the interviewer does is the strongest signal in this design.

**"After a failover, a replica serves a value the dead primary had overwritten. Is that OK?"** — Yes, *bounded*: it's stale, staleness is the documented cache contract, and **TTL is the ceiling** on how long the lie lives. If a team can't tolerate that, their fix is read-through versioning or shorter TTLs — not a consensus protocol in the cache. Turn the question back to the contract.

**"Why not make it strongly consistent?"** — Because strong consistency means synchronous coordination (quorum waits or a consensus round) on every write — and you'd spend multiple round trips defending data whose source of truth is *elsewhere*. You'd build a slow, expensive, worse database and lose the sub-ms point of the cache. The cache contract is allowed-to-be-wrong-briefly; charging latency to prevent a harmless wrongness is a bad trade. This answer, delivered plainly, is the senior mark for the whole design.

**"One celebrity key gets 200K reads/s — more than any single node can serve."** — Consistent hashing puts each key on exactly one node, so hot keys defeat partitioning by design. Two escapes: **detect and replicate the hot key** to several nodes (client picks one at random for reads; writes fan out with TTL as the staleness bound), or an **in-process minicache** in the client library — a tiny local LRU with a seconds-long TTL absorbs the flood one hop earlier. Detection is a cheap top-k frequency sketch on each node.

**"How do you add 20 nodes without a visible miss spike?"** — Consistent hashing already caps movement at ~1/6th of keys; go further by adding nodes gradually (virtual nodes let you ramp a node's share up), and optionally warm new owners by dual-reading (new node misses fall through to the old owner during the transition window).

**Common mistakes at this design:**
- `mod N` partitioning — instantly falsified by the "add a node" follow-up.
- A proxy hop plus a disk touch in a sub-ms budget — the Step 2 math already forbade it.
- Building synchronous quorum replication for data that is, by contract, disposable.
- Conflating TTL expiry with LRU eviction.
- Never mentioning the thundering herd — the failure mode the whole service exists to prevent.
</details>

---

**Next on the ladder:** [Design a Video Platform →](10-video-platform.md) — the numbers get three orders of magnitude bigger, and blob storage plus CDNs stop being footnotes.
