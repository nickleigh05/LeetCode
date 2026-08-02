# 13. Design a Distributed Message Queue — Senior

The Design Ladder works like the DSA practice sets: attempt first, then peek. Work the design on paper against the [framework template](../appendix/templates/system-design/template.md) for a full 45 minutes before opening any step below — the struggle *is* the practice.

[← Back to the lesson](../system-design/05-queues-streams.md) · [🗺 Interview Roadmap](../../interview.md)

---

## The prompt

> "Design a distributed message queue — Kafka-lite. Producers publish messages to named topics; consumer groups subscribe and process them. Messages must be durable, and consumers must be able to replay history."

Typical follow-up constraints when you ask (and you should ask — that's Step 1):

- ~1M messages/s aggregate across all topics.
- Ordering matters *within* a partition (e.g., all events for one user, in order).
- At-least-once delivery — no message may be silently lost.
- Days of retention: a new consumer can start from the past and replay.
- Consumers come and go; the system rebalances work among them.

This is the capstone on purpose: every rung below *used* a queue, and building one composes the entire Mastery track — [queues & streams](../system-design/05-queues-streams.md) (the product), [replication](../system-design/07-replication.md) (durability), [partitioning](../system-design/08-partitioning.md) (scale and ordering), [consistency & consensus](../system-design/09-consistency-consensus.md) (who's the leader), and [delivery semantics](../system-design/10-delivery-semantics.md) (the contract) — into one design. If you can defend this one, you can defend the lessons.

<details>
<summary>Step 1 — Requirements & API</summary>

**Functional:**
- `publish(topic, key, message)` — durable once acknowledged.
- Consumer groups: each group gets every message once-ish; *within* a group, work is split across members.
- Replay: consume from any retained offset, not just "now."
- (Confirm scope) delayed delivery, priorities, per-message ack/redelivery queues — classic *task-queue* features; this is a *log*, and saying which one you're building is itself a Step 1 win.

**Non-functional:**
- Durability: an acked message survives machine loss — producers are *trusting you with their only copy*.
- Per-partition ordering guaranteed; cross-partition ordering explicitly not.
- At-least-once floor; leave the door open to effectively-once.
- Horizontal scale on all three axes: producers, brokers, consumers.

**API sketch:**

```
POST /topics/{topic}/messages
  body: { "key": "user-42", "value": ... }        # key → partition → order
  returns 200 { "partition": 3, "offset": 182004 } once durable (per acks level)

GET  /topics/{topic}/partitions/{p}/messages?offset=182000&max=500   # pull!
POST /groups/{group}/offsets    body: { "topic", "partition": 3, "offset": 182500 }
GET  /groups/{group}/assignments                  # which member owns which partition
```

Two shapes to point at: consumption is **pull** (consumers fetch at their own pace — defended in Step 4), and "consumed" is just a **committed offset** — messages are never deleted per-consumer; the group merely records how far it has read. That reframing — consumption as a cursor over an immutable log — is the design's central idea.
</details>

<details>
<summary>Step 2 — Estimates</summary>

One-significant-figure math (the [estimation recipes](../system-design/00e-estimation.md)):

- **Ingest:** 1M msgs/s × ~1 KB average ≈ **1 GB/s** aggregate. A disk doing *sequential* writes sustains ~200–500 MB/s — so a handful of machines can absorb the firehose **if and only if writes are sequential**. Random I/O would need 100× the fleet; this single line justifies the append-only log.
- **Storage:** 1 GB/s × 7 days retention ≈ **~600 TB** live (before replication ×3 ≈ 2 PB). Big but boring: it's cold, sequential, cheap disk — retention is a disk-budget dial, not an architecture problem.
- **Partitions:** one partition ≈ one disk's sequential stream, ~50–100 MB/s comfortably → **~20–50 partitions minimum** for the hot topics; hundreds across the cluster. Consumers scale only up to partition count (Step 4), so provision headroom — say ~3× — above today's need.
- **Brokers:** 1 GB/s in + replication traffic (2×) + consumer reads out — a **10–20 broker** cluster with fast disks and 10–25 GbE carries it.
- **Consumer side:** at-least-once means downstream must handle ~1M/s *plus redeliveries* — their problem, but your API's idempotency story is what makes it tractable.

The numbers just decided the core: sequential I/O is non-negotiable (hence the append-only log), retention is cheap enough to default generous (hence replayability), and partition count — not machine count — is the real capacity knob.
</details>

<details>
<summary>Step 3 — High-level design</summary>

```
 Producers                    topic "orders", partition by key
    │  hash(key) % P    ┌────────────────────────────────────────┐
    ├──────────────────►│ p0: [0|1|2|3|4|5|6|7|8|9|...]──append──│► leader: broker A
    ├──────────────────►│ p1: [0|1|2|3|4|...]                    │► leader: broker B
    └──────────────────►│ p2: [0|1|2|...]                        │► leader: broker C
                        └────────────────────────────────────────┘
                          each partition: leader + ISR followers
                          A(p0 leader) ──replicate──► B, C (p0 followers)

 Consumer group "billing"          Consumer group "analytics"
   c1 ◄─ owns p0 (offset 182500)     d1 ◄─ owns p0, p1   (independent
   c2 ◄─ owns p1, p2                 d2 ◄─ owns p2        offsets)
        ▲ pull + commit offsets           ▲ can replay from offset 0
```

**The log — why this thing is fast.** Each partition is an **append-only sequence of segment files** on disk. Writes only ever append to the tail; reads are sequential scans from an offset. That's the whole storage engine — no B-tree, no random updates — and it's *why* a message queue outruns a database at this job: it does the one thing disks are great at (Step 2's arithmetic). An **offset** is simply a message's position in its partition — dense, ordered, and doubling as the consumer's cursor. Retention is dropping whole expired segments from the head: O(1), no compaction on the hot path.

**Topics → partitions — the unit of everything.** A topic is split into P partitions, and the partition is simultaneously the unit of **parallelism** (different partitions live on different brokers, are written and read independently) and the unit of **ordering** (one partition = one strictly ordered log; across partitions, no promises). Producers control placement: **partition-by-key** (`hash(key) % P` — the [partitioning lesson](../system-design/08-partitioning.md)) puts all of `user-42`'s events in one partition, in order — per-key ordering is *the* reason keys exist; keyless messages round-robin for pure load spreading. Trade-off to name: a hot key makes a hot partition, and no amount of brokers fixes that — the fix is a better key.

**Consumer groups — parallelism with a coordination catch.** Within a group, **each partition is owned by exactly one consumer** — that invariant is what preserves per-partition order while spreading work. A **group coordinator** (a broker role) tracks membership via heartbeats and runs **rebalancing** when members join or die, reassigning partitions. Progress is a **committed offset** per (group, partition), stored durably in the cluster itself — a consumer that crashes and returns resumes from its last commit. Different groups don't share offsets at all: billing and analytics each read the whole stream at their own pace — one log, many readers, which is the fan-out the [queues lesson](../system-design/05-queues-streams.md) promised.

**Replication — the key decision: what does an ack mean?** Each partition has a **leader** (all reads/writes) and followers that replicate its log; followers keeping up form the **ISR — the in-sync replica set** ([replication](../system-design/07-replication.md)). The producer's `acks` level is the durability/latency dial, and it's the decision to compare out loud:

1. **acks=0** (fire and forget) — fastest, loses acked-ish data on any hiccup. For metrics nobody cries over.
2. **acks=leader** — leader persisted it; a leader crash before followers copy it loses acked messages. Tempting middle, quietly dangerous.
3. **acks=quorum/all-ISR** — ack only when the in-sync set has it; an acked message survives leader loss. One replication round-trip of extra latency (~few ms).

Default **quorum for anything that matters** — a queue's one job is not losing acked messages, so buy durability with milliseconds. Per-topic configurability is the honest answer to "it depends." Broker/leader failure is handled by a **controller** (elected via the cluster's [consensus](../system-design/09-consistency-consensus.md) machinery) promoting an ISR follower — covered in Step 4.

**Delivery semantics — the contract, stated precisely** ([delivery semantics](../system-design/10-delivery-semantics.md)): the default is **at-least-once** — consumers commit offsets *after* processing, so a crash between the two means redelivery, and downstream handlers must be **idempotent**. "Exactly-once" is available as *effectively-once*: **producer idempotency** (per-producer sequence numbers let the leader drop duplicate appends from retries) plus **transactional offset commits** (process-and-commit as one atomic unit, for read-process-write pipelines). Name it as engineered atop at-least-once, not as magic — that's the whole lesson in one sentence.

**Backpressure — free, by construction.** Consumption is **pull**: a slow consumer just fetches less often while the log holds its place; nothing pushes into a drowning process, nothing buffers unboundedly in flight. Retention is the backstop — fall more than N days behind and you finally lose data, loudly, at a known boundary.
</details>

<details>
<summary>Step 4 — Deep dives & what interviewers probe</summary>

**"A consumer processes 400 of a 500-message batch and dies. What happens?"** — Its last committed offset is from *before* the batch, so after rebalancing the partition's new owner re-reads all 500 — the ~400 already-processed messages are **redelivered**. That's at-least-once working exactly as specified, and it's why the consumer contract says *idempotent handlers* (dedup by message key, upserts, or the payment-system trick of idempotency keys — rung 12 was training for this). The wrong fix is committing *before* processing — that converts duplicates into **silent loss**, strictly worse. Commit-after + idempotency is the canonical pairing.

**"How many partitions should a topic have? Can I change it later?"** — Partition count is the **parallelism ceiling**: a group can't use more consumers than partitions, so it must exceed peak consumer count. But each partition costs real overhead — file handles, replication fetchers, leader-election work, slower failovers — so thousands-per-topic isn't free. And the trap: partitions are easy to *add* but **effectively impossible to shrink**, and even adding them breaks key→partition mappings (`hash(key) % P` changes, so a key's *new* messages land in a different partition than its history — per-key ordering across the boundary is gone). So: provision ~3× expected peak consumers up front, and treat repartitioning as a migration, not a config change.

**"The leader for partition 3 dies. Walk me through it."** — Heartbeats time out; the **controller** — itself kept singular by [consensus](../system-design/09-consistency-consensus.md), because two controllers is how you get two leaders — promotes a follower **from the ISR**: it has every acked message (that's what quorum acks bought), so nothing acked is lost; producers and consumers re-resolve metadata and continue; total gap ~seconds. The sharp edge: if the *whole ISR* is gone, you choose between **unclean election** (promote a stale replica — available now, acked messages lost) and **waiting** (unavailable until an ISR member returns — nothing lost). That's CAP made concrete, it's a per-topic policy, and the default for data that matters is *wait*. Naming this trade-off unprompted is the capstone moment.

**"Why do consumers pull? Push would be lower latency."** — Push forces the broker to guess every consumer's capacity and to buffer or drop when it guesses wrong — with thousands of heterogeneous consumers, that's an unwinnable flow-control problem living in your most critical component. Pull inverts it: each consumer *is* its own flow control (fetch when ready), slow consumers degrade only themselves, replay is trivially natural (a fetch from an old offset is just... a fetch), and long-poll fetches ("hold the request until data or timeout") recover push-like latency. Batching comes free too — a pull drains everything pending in one round trip. For a durable log with diverse consumers, pull wins on every axis except a few milliseconds you can buy back.

**"1M msgs/s through one cluster — where does the time actually go?"** — Mostly avoided, and the techniques are worth listing: **sequential appends** (the log), **batching** end-to-end (producers send batches, the log stores them, consumers fetch them — per-message overhead amortized to near zero), **zero-copy** from page cache to socket on the read path (a tailing consumer never touches the disk), and compression per batch. The theme to state: the design never fights the hardware — it's fast because every hot path is the thing disks, RAM, and NICs already do best.

**Common mistakes at this design:**
- Designing per-message acks and deletion (a task queue) when the requirements — replay, groups, ordering, retention — all say *log*. The Step 1 distinction, missed.
- Promising global ordering across a topic — one partition = ordered; the topic = never. Global order means one partition means no parallelism.
- acks=leader everywhere, then acting surprised when a leader crash loses "durable" messages.
- Two consumers in one group reading one partition "for speed" — you just destroyed both ordering and the offset story.
- Skipping the redelivery conversation — at-least-once without consumer idempotency is a duplicate factory, not a delivery guarantee.
</details>

---

**Top of the ladder.** Thirteen designs, every one built from the same framework and the same handful of primitives — which is the actual lesson. Head back to the [Interview Roadmap](../../interview.md#the-design-ladder) and re-run any rung where you had to open the steps: the design you can rebuild cold, unaided, on paper is the one you own in the room.
