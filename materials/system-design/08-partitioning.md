# 08. Partitioning & Consistent Hashing

*When the data outgrows one machine, split it by key — and split it so you can keep growing.*

[← Prev](07-replication.md) · [🗺 Interview Roadmap](../../interview.md) · [Next →](09-consistency-consensus.md)

---

> **Builds on:** [Arrays & Hashing](../learning/01-arrays-hashing.md) — this is the flagship DSA↔SD bridge. `hash(key) % N` is *exactly* your LeetCode bucketing instinct, and watching it fail at scale is what motivates everything in this lesson. [Replication (07)](07-replication.md) copied the data; partitioning splits it — real systems do both.

[Replication](07-replication.md) put the same data on more machines, which scales reads — but every node still holds *everything*, so it caps total data size, and every write still hits one leader, so it caps write throughput. **Partitioning** (sharding) breaks the dataset into pieces and gives each node only a slice. It's the answer to "10 TB doesn't fit on one machine" and "one leader can't absorb 500K writes/sec." Junior loops accept "we'll shard it"; senior loops — and any loop where you claim distributed-systems experience — ask the three questions this lesson answers: *which key*, *what happens when you add a node*, and *what about the celebrity*.

## Concept

### Range vs Hash Partitioning

```
  RANGE: split by sorted key            HASH: split by hash(key)
  ┌──────────┬──────────┬─────────┐     ┌─────────┬─────────┬─────────┐
  │  A–H     │  I–P     │  Q–Z    │     │ bucket 0│ bucket 1│ bucket 2│
  │ shard 1  │ shard 2  │ shard 3 │     │ shard 1 │ shard 2 │ shard 3 │
  └──────────┴──────────┴─────────┘     └─────────┴─────────┴─────────┘
  scans work: "users I–K" = 1 shard     load spreads evenly (hash mixes)
  hot spots: today's timestamps all     scans die: "users I–K" hits
  land on the LAST shard                EVERY shard
```

**What it is:** The first fork in the road — assign each key a shard by *where it sorts* (range) or *where it hashes* (hash).

**Trade-offs:**

| | Range partitioning | Hash partitioning |
|---|---|---|
| Range scans ("all events this hour") | One shard — cheap | Every shard — scatter-gather |
| Load distribution | Hot spots on sequential keys | Even — hashing destroys locality on purpose |
| Classic failure | All new writes hit the newest shard | No cheap range queries, ever |
| Used by | HBase, Bigtable, Spanner | Cassandra, DynamoDB, Memcached clients |

**Use when:** Hash is the interview default — say it first. Reach for range only when range scans *are the workload* (time-series, leaderboards), and immediately name the hot-spot cost: keys arriving in sorted order (timestamps, auto-increment IDs) hammer one shard while the rest idle.

### Why `hash(key) % N` Breaks

```
  N = 3 nodes                N = 4 nodes (added ONE)
  key    hash   owner        key    hash   owner
  "ada"    17   17 % 3 = 2   "ada"    17   17 % 4 = 1   ← moved
  "bob"    42   42 % 3 = 0   "bob"    42   42 % 4 = 2   ← moved
  "cyd"    91   91 % 3 = 1   "cyd"    91   91 % 4 = 3   ← moved
  "dee"    12   12 % 3 = 0   "dee"    12   12 % 4 = 0   ← stayed (luck)

  Changing N remaps ~N/(N+1) of ALL keys — at N=4, ~80% move at once.
```

**What it is:** The LeetCode instinct — bucket by `hash(key) % N` — applied to machines. It works perfectly *until N changes*. Add or lose one node and nearly every key's owner changes simultaneously: a cache goes ~80% cold in one moment (the database eats the full load — a self-inflicted [stampede](02-caching.md)), or a database reshuffles most of its bytes over the network at once.

**Key Properties:**
- The problem isn't hashing — it's that **`% N` couples every key's placement to the cluster size**.
- **Resharding pain is the real cost of partitioning** — any scheme is judged by how much data moves when the cluster changes.
- The fix is to make placement depend on *where the key hashes*, not *how many nodes exist* — which is consistent hashing.

### Consistent Hashing — the Ring

```
                        0
                 D ●─────────● A
                ╱               ╲
               │                 │
               │    hash ring    x ← hash("user:42") lands here
               │   (0 … 2³²)     │
                ╲               ╱
                 C ●─────────● B

  Both nodes and keys hash onto the same ring.
  A key is owned by the first node CLOCKWISE from it → "user:42" → B.
  Node B dies  → only B's arc slides to C. Everyone else: untouched.
  Node E joins → it takes one arc from one neighbor. That's it.
```

**What it is:** Hash *nodes and keys into the same space*, arranged as a ring; each key belongs to the next node clockwise. Adding or removing a node moves only **K/N keys** (K keys, N nodes) — the theoretical minimum — instead of nearly all of them.

**Key Properties:**
- **Only neighbors are affected by membership changes** — the property the whole design exists for.
- Plain consistent hashing has two flaws: random node positions make **uneven arcs**, and a dying node dumps its whole arc on *one* neighbor. **Virtual nodes** fix both — each physical machine appears at ~100–200 points on the ring, so arcs average out and a dead node's load scatters across everyone.
- This is how Cassandra, DynamoDB, and every serious distributed cache place data. Saying "consistent hashing with virtual nodes" — and *why* — is the expected answer to "how do keys map to nodes?"

**Use when:** Any partitioned system where nodes join and leave — which is all of them. It's *the* named algorithm of system design interviews; know it the way you know binary search.

### Hot Keys — the Celebrity Problem

**What it is:** Hashing spreads *keys* evenly, not *load*. Every read of `user:justinbieber` still lands on the one shard that owns the key — 100× anyone else's traffic, and no rebalancing helps because it's a single key.

**Fixes to name:**
- **Cache in front** — a tiny in-process cache on every app server absorbs the celebrity reads before they reach the shard ([caching](02-caching.md) again).
- **Replicate the hot key** across several nodes and pick one at random per read.
- **Salt the key for writes** — split `bieber:likes` into `bieber:likes:0..9` on ten shards, sum on read. Costs a scatter-gather read; only worth it for genuinely hot *write* keys.

**Use when:** Volunteer this whenever your design has power-law access — social, feeds, anything with celebrities. Interviewers plant this probe deliberately.

### Request Routing — Who Knows the Map?

```
  1. routing tier            2. smart client           3. coordinator + gossip
  client → proxy → shard     client knows the ring     any node accepts, forwards;
  (extra hop; clients        (no hop; every client     membership spreads by gossip
   stay dumb)                 must stay in sync)       (Cassandra) or lives in a
                                                       config service (→ lesson 09)
```

**What it is:** *Something* has to know key→shard. A **routing tier/proxy** keeps clients simple at the cost of a hop; a **smart client** embeds the ring and skips the hop; **any-node-coordinates** lets clients connect anywhere. The mapping itself — small, critical, must-be-consistent — typically lives in a coordination service like ZooKeeper/etcd, which is [consensus's](09-consistency-consensus.md) job. One sentence in the interview; knowing all three options is the depth.

### Secondary Indexes Across Shards

**What it is:** You sharded users by `user_id` — now find all users in Toronto. The index has to live somewhere too:

- **Local index** — each shard indexes *its own* rows. Writes stay one-shard (cheap); the Toronto query must **scatter-gather** every shard and merge (expensive reads).
- **Global index** — the index is itself partitioned *by the indexed value* (all Toronto entries together). Reads hit one index shard (cheap); every write now updates its data shard *and* a different index shard (expensive, and consistent only [eventually](09-consistency-consensus.md)).

**Use when:** Say the rule: **local = cheap writes + scatter-gather reads; global = cheap reads + multi-shard writes.** Pick by which side of the workload dominates — and only when asked; don't volunteer index topology unprompted.

## The Pattern — Pick the Key, Then Defend It

Partitioning shows up in Step 3 of every large [ladder](../../interview.md#the-design-ladder) design. The moves, in order:

1. **Justify it with numbers** — "10 TB and 200K writes/sec won't fit one machine, so I'll shard" (from your Step-2 estimates). Don't shard 50 GB; that fits in RAM.
2. **Pick the partition key** — the field most queries filter by, so requests stay one-shard. This choice *is* the design decision; say the runner-up key and why you rejected it.
3. **Pick hash vs range with a reason** — hash by default; range if scans are the workload, plus the hot-spot caveat.
4. **Name consistent hashing with virtual nodes** — the answer to "what happens when you add a node?", with the K/N argument.
5. **Volunteer the hot-key story** — celebrity key, and one fix. The unprompted step that separates candidates.

The invariant to protect: **every key has exactly one home, and every router agrees on it — even mid-reshard.** Two nodes both believing they own a key is how you serve stale data and drop writes; this is why the ring/mapping lives in one strongly-consistent place and why membership changes are the part you walk through slowly.

## The Template

The design-interview worksheet lives in [`appendix/templates/system-design/`](../appendix/templates/system-design/). Read the README (when to reach for each component, common traps), then work designs against [`template.md`](../appendix/templates/system-design/template.md) — the partition key is a Step-3 decision, and "what happens when a node joins?" is a Step-4 deep dive.

## Practice

Partitioning is the centerpiece of [**Design a Distributed Cache →**](../sd-practice/09-distributed-cache.md) — consistent hashing is the first thing the interviewer probes — and [**Design a Distributed Queue →**](../sd-practice/13-distributed-queue.md), where the partition count caps your consumer parallelism. Every design past mid-[ladder](../../interview.md#the-design-ladder) will make you pick a shard key and defend it.

## Check Yourself

- [ ] I can explain why `hash(key) % N` fails when N changes, with the ~N/(N+1) argument.
- [ ] I can draw the consistent-hashing ring, walk a node join/leave, and say what virtual nodes fix.
- [ ] I can state the range-vs-hash trade and pick one for a given workload.
- [ ] I can name the celebrity problem and two fixes, and the local-vs-global index trade in one sentence each.

---

**Up next:** [Consistency Models & Consensus](09-consistency-consensus.md) — you've copied data and split data; now the hard question: what are readers *promised*, and how do machines agree on anything?

[← Prev](07-replication.md) · [🗺 Interview Roadmap](../../interview.md) · [Next →](09-consistency-consensus.md)
