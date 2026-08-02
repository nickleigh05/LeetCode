# 09. Consistency Models & Consensus

*What are readers promised — and how do machines that can't trust each other agree on anything?*

[← Prev](08-partitioning.md) · [🗺 Interview Roadmap](../../interview.md) · [Next →](10-delivery-semantics.md)

---

> **Builds on:** [Replication (07)](07-replication.md) — the moment you have two copies of a value, "what does a read return?" stops having an obvious answer. This lesson names the possible answers (consistency models), the vocabulary interviewers expect (CAP, quorums), and the algorithm that makes strong answers possible (Raft).

Copying data ([replication](07-replication.md)) and splitting data ([partitioning](08-partitioning.md)) both created the same debt: multiple machines now hold opinions about the same value, and those opinions can disagree. **Consistency models** are the contracts you can offer readers; **consensus** is the machinery that pays for the strong ones. This is the most senior material in the track — junior loops rarely go here, but senior/staff loops and infra roles absolutely do, and *anyone* who says "I'll use strong consistency for the balance" should expect the follow-up: "how?" This lesson is that answer, at whiteboard depth — no proofs, no Paxos archaeology.

## Concept

### The Consistency Spectrum

```
  STRONGER ◄──────────────────────────────────────────► WEAKER
  linearizable        causal              eventual
  "one copy,          "causes before      "replicas converge...
   real-time order"    effects"            eventually"
  expensive:          middle ground:      cheap: any replica
  coordination on     track what a read   answers immediately;
  every operation     depended on         readers may see the past
```

**What it is:** A consistency model is the promise a storage system makes about what reads return when writes are still propagating. One concrete scenario — Alice posts "I'm engaged!", then Bob comments "Congrats!" — separates the three levels:

- **Linearizable** — the system behaves as if there's exactly one copy, and every operation takes effect atomically at some instant between its start and finish. Once *any* client sees Alice's post, *every* subsequent read sees it. Carol can never see Bob's "Congrats!" without the post it replies to. This is what people mean by "strong consistency."
- **Causal** — operations that are causally related stay ordered: Bob *read* Alice's post before commenting, so no one ever sees the comment without the post. But two *unrelated* posts may appear in different orders on different replicas — and that's allowed.
- **Eventual** — the only promise is convergence: stop writing, wait, and all replicas agree. In between, Carol might see the comment, refresh, and watch it vanish. Cheap and fast — every replica answers locally — and fine for likes, view counts, and feeds.

**Key Properties:**
- Stronger models cost **coordination** — round-trips between replicas before acknowledging — which costs latency and availability. You're not picking a model; you're picking a price.
- Pick **per operation, not per system** — the payment ledger is linearizable, the "customers also bought" panel is eventual. Saying this split out loud is a senior signal.
- **Read-your-writes** is the eventual-consistency patch users actually notice: after Alice posts, route *her* reads to the leader (or a replica known to be caught up) so she sees her own post. Cheap to name, cheap to build.

**Use when:** Default to eventual and justify the exceptions. Reach for linearizable only where a stale read causes real harm — balances, inventory counts, uniqueness checks ("is this username taken?"), and lock/leader decisions.

### CAP & PACELC — Interview Vocabulary

**What it is:** **CAP**: when a network **P**artition happens, a distributed system must choose between **C**onsistency (refuse to answer rather than answer wrong) and **A**vailability (always answer, possibly stale). Partitions are not optional — networks fail — so the real statement is: *when* (not if) the network splits, pick C or P... pick C or A.

**PACELC** is the useful extension: if **P**artition, choose **A** or **C**; **E**lse (normal operation), choose **L**atency or **C**onsistency. It captures the everyday trade CAP misses — even with a healthy network, synchronous replication costs latency.

| | On partition | Normally | Example |
|---|---|---|---|
| PA/EL | Available | Fast | Dynamo-style stores, Cassandra (default) |
| PC/EC | Consistent | Consistent | Spanner, etcd, ZooKeeper |
| PC/EL | Consistent | Fast | MongoDB (roughly) |

**The honest caveat — say it:** real systems are more nuanced than the triangle. "CP vs AP" is a spectrum per operation, not a badge per database; most systems are tunable (Cassandra with `QUORUM` reads behaves very differently than with `ONE`). Use CAP as one sentence of framing — "under partition I'd rather this endpoint be unavailable than wrong" — not as a taxonomy you defend.

**Use when:** Answering "why not just make everything strongly consistent?" — PACELC's *else* clause is the answer: you'd pay coordination latency on every request, all the time, not just during failures.

### Quorums — N, R, W

```
  N = 3 replicas, W = 2, R = 2          R + W > N  →  overlap guaranteed

  write x=5 ──► [A: x=5] [B: x=5] [C: x=old]   (C lagging — write acked at 2/3)
  read x    ──► ask any 2 … {B, C} → {x=5, x=old}
                                       └─ versions/timestamps pick the newer: 5
  Any R-set intersects any W-set in ≥1 node → every read touches ≥1 fresh copy.
```

**What it is:** Instead of one leader deciding, write to **W** of **N** replicas and read from **R**. If **R + W > N**, every read set overlaps every write set in at least one node, so a read always *sees* the latest acknowledged write — using per-key versions to tell newest from stale.

**Key Properties:**
- Tune the dials: **W=N, R=1** — slow writes, fast reads. **W=1, R=N** — the reverse. **W=R=2, N=3** — the balanced default to say in an interview.
- **What the overlap buys:** reads observe the latest *completed* write, and you tolerate N−W node failures for writes, N−R for reads.
- **What it doesn't:** strict quorums alone are **not linearizability** — concurrent writes, partial failures (a write that reached 1 of 3 then died), and sloppy quorums all create windows where reads disagree. Say "quorum reads/writes give me strong-*ish* consistency; for true linearizability I need consensus." That one sentence is the depth check.

**Use when:** Leaderless/Dynamo-style stores, and any time the interviewer asks "how do you read your writes with replicas?" without wanting a full Raft discussion.

### Leases & Fencing Tokens

**What it is:** Distributed locks are how consensus leaks into ordinary designs — "only one worker processes this job." A **lease** is a lock with an expiry: the holder must renew it, so a crashed holder can't wedge the system forever. But expiry creates the classic bug: the holder pauses (GC, network stall), the lease expires, a *new* holder is granted, then the old one wakes up and writes — **two writers, both convinced they own the lock**.

**The fix — fencing tokens:** the lock service hands out a monotonically increasing token with each grant (33, then 34...). The protected resource (the storage layer) **rejects writes with a token older than the highest it has seen**. The zombie's write with token 33 bounces off a store that already saw 34.

**Key Properties:**
- The insight to say out loud: **you can't fix this on the client side** — a paused client cannot know it's paused. The *resource* must enforce ordering.
- This is why "just use a Redis lock" gets a raised eyebrow at senior loops — without fencing, a lease-based lock protects against politeness failures, not correctness failures.

### Raft — Whiteboard Depth

```
  TERM 3: node B is leader                    Log replication:
                                              client ─► leader B: append "x=5"
    A (follower) ◄── heartbeats ──┐           B writes to its log (uncommitted)
    B (LEADER, term 3) ───────────┤           B ─► A, C: AppendEntries("x=5")
    C (follower) ◄────────────────┘           A acks. 2/3 = MAJORITY → committed
                                              B applies, replies to client,
  B dies → A's election timer fires:          tells A, C to apply.
  A becomes candidate, term 4,
  requests votes; majority → A is leader.     C was down? It catches up from
  C also ran? Split vote → randomized         the leader's log when it returns.
  timeouts retry; someone wins next round.
```

**What it is:** Consensus — getting a cluster to agree on one value (or one *log* of values) despite crashes — is the foundation under every linearizable claim. **Raft** is the one to know: an elected **leader** owns a **replicated log**, and an entry is **committed once a majority has it**.

**Key Properties — the whiteboard script:**
- **Terms** are logical clocks: each election starts a new term; a node seeing a higher term steps down instantly. Terms are how Raft prevents two leaders acting at once — a deposed leader's writes can't commit because the majority has moved on.
- **Leader election:** followers expect heartbeats; a follower that times out becomes a candidate, increments the term, and requests votes. Majority of votes → leader. **Randomized election timeouts** break split-vote ties — that's the whole trick.
- **Log replication:** all writes go through the leader; committed = replicated on a **majority**. Majorities overlap, so any future leader must be elected by at least one node holding every committed entry — Raft only elects candidates with up-to-date logs — so **committed entries survive leader changes**.
- **Majority (⌈(N+1)/2⌉) is why clusters are 3 or 5 nodes**: tolerate 1 or 2 failures respectively. An even count adds cost without adding fault tolerance.

**What you're expected to say vs not:** Expected — the three bullets above, plus "this is what etcd/ZooKeeper run, and it's where cluster metadata, shard maps, and leader locks live." Not expected — the safety proof, log-matching edge cases, snapshotting, or Paxos vs Raft trivia. Nobody wants the proof; they want to know you understand *majority commit* and *why terms prevent split-brain*. Also say the cost: every write is a majority round-trip — consensus is for **coordination data** (small, critical), not the data path.

**Use when:** You said "strongly consistent" or "distributed lock" or "leader election" anywhere in your design. Raft (via etcd/ZooKeeper) is the standard non-hand-wavy answer to "how?"

## The Pattern — Name the Promise, Then Pay For It

Consistency questions arrive as Step-4 deep dives ("what if a replica is stale?", "two workers grab the same job — what happens?"). The moves, in order:

1. **Split the design by consistency need** — walk your operations: "the ledger needs linearizable; the feed is fine eventual." Never one blanket answer.
2. **Name the mechanism per tier** — eventual: async replication, done. Read-your-writes: pin the writer to the leader. Linearizable: leader writes with majority ack, or quorum R/W with the caveat.
3. **Deploy the vocabulary once** — one CAP/PACELC sentence to frame the trade, with the "real systems are tunable" caveat. Then stop; don't lecture.
4. **If locks/leader-election appear, say leases + fencing tokens** — and that the resource enforces the token. This is a planted probe at senior loops.
5. **If pressed on "how does strong consistency actually work," give the Raft script** — terms, election, majority commit, 3-or-5 nodes — and scope it: consensus for metadata and locks, not for every user write.

The invariant to protect: **no operation is acknowledged under a promise the system can't keep.** If you ack a write before a majority has it and call it "strongly consistent," a leader failover silently loses it — that's the lie interviewers are listening for.

## The Template

The design-interview worksheet lives in [`appendix/templates/system-design/`](../appendix/templates/system-design/). Read the README (when to reach for each component, common traps), then work designs against [`template.md`](../appendix/templates/system-design/template.md) — consistency requirements belong in Step 1 (they're *requirements*), and the mechanism is a Step-4 deep dive.

## Practice

Consensus carries [**Design a Distributed Queue →**](../sd-practice/13-distributed-queue.md) — who owns each partition, and what happens when the owner dies, is a leader-election question — and [**Design a Payment System →**](../sd-practice/12-payment-system.md), where "the balance must be right" forces you to say linearizable and defend the cost. Every senior rung of the [ladder](../../interview.md#the-design-ladder) has one operation that needs a stronger promise than the rest; finding it is the exercise.

## Check Yourself

- [ ] I can walk the Alice/Bob/Carol scenario at all three consistency levels and say what each level forbids.
- [ ] I can state R + W > N, what the overlap guarantees, and why it still isn't full linearizability.
- [ ] I can explain the zombie-lock-holder bug and how fencing tokens fix it — including *where* the token is enforced.
- [ ] I can give the Raft whiteboard script — terms, randomized election timeouts, majority commit, why 3 or 5 nodes — in under two minutes.

---

**Up next:** [Delivery Semantics & Idempotency](10-delivery-semantics.md) — consensus made machines agree on state; now make messages between services survive retries without double-charging anyone.

[← Prev](08-partitioning.md) · [🗺 Interview Roadmap](../../interview.md) · [Next →](10-delivery-semantics.md)
