# 07. Replication & Failover

*Every byte on more than one machine — durability, read scale, and the ugly ten seconds after the leader dies.*

[← Prev](06-first-designs.md) · [🗺 Interview Roadmap](../../interview.md) · [Next →](08-partitioning.md)

---

> **Builds on:** [Databases 101](00d-databases-101.md) — one database as the source of truth — and [Load Balancing](03-load-balancing.md), where you cloned stateless servers behind one front door. This lesson clones the *stateful* box, which is where the real trouble lives.

Every design so far has one database, which means one disk failure loses everything and one machine caps your read throughput. **Replication** — the same data on several machines — buys you three things at once: **durability** (a dead disk is an inconvenience, not a data loss), **read scale** (more copies, more machines serving reads), and **availability** (the system survives a node dying). Junior loops stop at "add a read replica." Senior and staff loops — and any loop where you've claimed distributed-systems experience — live in the follow-ups: *what do reads see while replicas lag*, and *what exactly happens when the leader dies*. This lesson is those follow-ups.

## Concept

### Leader–Follower — the Default Picture

```
                          writes
             Client ────────────────► ┌────────┐
                                      │ Leader │   the ONLY box that accepts writes
                                      └───┬────┘
                          replication log │  (ordered stream of changes)
                            ┌─────────────┴──────────────┐
                            ▼                            ▼
                     ┌────────────┐               ┌────────────┐
         reads ────► │ Follower 1 │               │ Follower 2 │ ◄──── reads
                     └────────────┘               └────────────┘
```

**What it is:** One node — the **leader** (primary) — accepts all writes and streams an ordered log of changes to **followers** (replicas), which replay it. Writes have exactly one door; reads can go anywhere.

**Key Properties:**
- **One writer means no write conflicts** — ordering is trivial because the leader decides it. This is why leader–follower is the default answer.
- **Read throughput scales linearly** — need more reads, add followers. Write throughput does *not* scale — every write still lands on one leader (fixing that is [partitioning →](08-partitioning.md)).
- **Followers lag** — usually by milliseconds, but the lag is unbounded under load. Everything in the next two sections falls out of this.

**Use when:** Almost always — it's the default topology for Postgres, MySQL, MongoDB, Redis, Kafka. Say "leader–follower" first and deviate only with a reason.

### Sync vs Async — the Durability/Latency Trade

**What it is:** The question of *when the leader tells the client "your write is safe."* Before or after a follower has a copy?

**Trade-offs:**

| | Synchronous | Asynchronous |
|---|---|---|
| Leader acks when… | a follower confirmed the write | it's on the leader alone |
| If the leader dies now | write survives on the follower | recent writes **vanish** |
| Write latency | + a network round trip, gated on the slowest follower | leader-local, fast |
| If a follower dies | writes stall until it's replaced | nothing — nobody was waiting on it |

**Use when:** The interview default is **semi-synchronous** — one follower sync (so every acked write exists on two machines), the rest async. Fully sync across all followers means one slow replica stalls every write; fully async means telling the interviewer, out loud, that acked writes can be lost on failover. Match it to the data: async is fine for a feed, indefensible for payments.

### Replication Lag — the Bugs Users Actually See

**What it is:** A follower is always slightly behind. Two anomalies show up so often that interviewers probe them by name:

- **Read-your-own-writes violation** — you post a comment (write → leader), the page refreshes (read → lagging follower), your comment is *gone*. The user's mental model — "I just did that" — is broken. **Fix:** for a short window after a user writes, serve *that user's* reads from the leader (or from a replica known to be caught up past their write).
- **Monotonic reads violation** — refresh once and see the comment (fresh follower), refresh again and it's *vanished* (staler follower). Time ran backwards. **Fix:** **session stickiness** — pin each user's reads to one replica, so their view only ever moves forward.

Naming one of these *unprompted* when you add read replicas is a strong senior signal — it shows you know replicas aren't free reads.

### Failover — When the Leader Dies

```
  1. DETECT    followers miss heartbeats for a timeout (~10–30s)
               — is the leader dead, or just slow? you can't tell.
  2. PROMOTE   pick the follower with the freshest log → new leader
  3. REPOINT   clients + remaining followers follow the new leader

  what goes wrong:
  ├── async writes that never reached the new leader are LOST
  └── the old leader comes back and still thinks it's leader
      → two leaders accepting writes → SPLIT-BRAIN
```

**What it is:** Promotion of a follower to leader when the leader fails — the automated part everyone gets, plus the two failure modes that separate candidates:

**Key Properties:**
- **Lost writes** — with async replication, writes the dead leader acked but never shipped are gone. If the old leader later revives, its extra writes usually get discarded. Say this cost out loud when you choose async.
- **Split-brain** — the old leader wasn't dead, just partitioned or GC-paused. Now two nodes accept writes and the data diverges irreconcilably. The fix is **fencing**: before the new leader takes over, forcibly revoke the old one's power — cut its network, kill the process, or have storage reject its writes ([fencing tokens →](09-consistency-consensus.md) make this precise).
- **The detection dilemma** — a short timeout triggers needless failovers on every hiccup; a long one extends the outage. There's no right answer; naming the tension is the point.

**Use when:** Any design with an availability requirement — which is every design. The interviewer's "what if the database dies?" is this section.

### Multi-Leader & Quorums — the Two Escapes

**What it is:** Two ways out of the single-leader bottleneck, each buying something and costing something.

- **Multi-leader** — one leader *per region*, replicating to each other asynchronously. Users write locally (fast), but now the same row can be written on two continents at once → **write conflicts**. Last-write-wins silently drops data; real resolution needs app-level merge logic. Mention it for multi-region designs, then mention the conflict cost in the same breath.
- **Leaderless / quorum replication** — no leader at all (the Dynamo/Cassandra model). Write to N replicas, call it done at **W** acks; read from **R**. If **R + W > N**, every read set overlaps every write set in at least one node — so a reader sees the latest acked write. What that overlap buys, and what it *doesn't*, is the opening act of [Consistency & Consensus →](09-consistency-consensus.md).

## The Pattern — Leader–Follower with Honest Failover

When a design needs the database to scale reads or survive failures — which is Step 4 of nearly every [ladder](../../interview.md#the-design-ladder) design — the moves, in order:

1. **Justify replicas with numbers** — "reads outnumber writes 100:1, so one leader, two read replicas" (from your Step-2 estimates).
2. **Route explicitly** — writes to the leader, reads to followers. Draw both arrows; interviewers notice when all arrows point at one box.
3. **Name the replication mode and its cost** — "async to followers, so on failover we can lose the last few seconds of writes — acceptable for posts, not for payments, so payments get semi-sync."
4. **Name a lag anomaly and its fix** — read-your-own-writes from the leader, or session stickiness. Unprompted.
5. **Walk the failover** — heartbeat detection, promote the freshest follower, and *fence the old leader* against split-brain. Step 5 is the one that reads as senior.

The invariant to protect: **at most one node accepts writes at any moment.** Every failover mechanism exists to defend it, split-brain is the name for breaking it, and fencing is how you make it hold even when the old leader refuses to believe it's been replaced.

## The Template

The design-interview worksheet lives in [`appendix/templates/system-design/`](../appendix/templates/system-design/). Read the README (when to reach for each component, common traps), then work designs against [`template.md`](../appendix/templates/system-design/template.md) — replication decisions land in Step 3 (high-level) and failover is a Step-4 deep dive interviewers steer into deliberately.

## Practice

Replication is the load-bearing wall of [**Design a Distributed Cache →**](../sd-practice/09-distributed-cache.md) (replicas as both durability and hot-key relief) and [**Design a Distributed Queue →**](../sd-practice/13-distributed-queue.md) (a message acked but not replicated is a message lost — the sync/async trade with teeth). Every other design on the [ladder](../../interview.md#the-design-ladder) will ask "what if this node dies?" — this lesson is the answer's skeleton.

## Check Yourself

- [ ] I can draw leader–follower replication and explain why writes get one door and reads get many.
- [ ] I can state the sync vs async trade and pick semi-sync with a reason.
- [ ] I can describe a read-your-own-writes violation and two fixes for lag anomalies.
- [ ] I can walk a failover end to end — detection, promotion, repointing — and explain split-brain and why you fence the old leader.

---

**Up next:** [Partitioning & Consistent Hashing](08-partitioning.md) — replication copies the data; partitioning *splits* it. The flagship bridge from your hash-map instincts to distributed systems.

[← Prev](06-first-designs.md) · [🗺 Interview Roadmap](../../interview.md) · [Next →](08-partitioning.md)
