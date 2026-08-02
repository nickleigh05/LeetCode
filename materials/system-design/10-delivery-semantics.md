# 10. Delivery Semantics & Idempotency

*Networks retry. Design so that doing it twice equals doing it once.*

[← Prev](09-consistency-consensus.md) · [🗺 Interview Roadmap](../../interview.md) · [Next →](11-specialized-infra.md)

---

> **Builds on:** [Queues & Streams (05)](05-queues-streams.md) — you put a queue between services to decouple them; this lesson is the fine print on the messages flowing through it. What happens when a message is delivered twice, or a service crashes between "write the order" and "publish the event"?

Every arrow you draw between two services hides the same question: what if the message is lost, or the sender times out and retries, or the receiver crashes mid-processing? Retries are not an edge case — they're the *normal* behavior of every HTTP client, queue consumer, and mobile app on a flaky network. This lesson is where payment, ordering, and notification designs are won or lost, and it's graded hard at senior loops — "the user taps Pay twice" is one of the most-planted probes in the industry. The punchline you'll use everywhere: **you can't prevent duplicates, so make duplicates harmless.**

## Concept

### At-Most-Once / At-Least-Once / Exactly-Once

```
  sender ──msg──► receiver ──ack──► sender

  AT-MOST-ONCE: send, don't retry.        AT-LEAST-ONCE: retry until acked.
  ack lost? sender assumes fine.          ack lost? sender resends —
  msg lost? GONE.                         receiver processes TWICE.
  ┌────────────────────────────────────────────────────────────┐
  │ The sender can never distinguish "message lost" from       │
  │ "ack lost" — so it must choose: drop (at-most-once) or     │
  │ duplicate (at-least-once). There is no third wire option.  │
  └────────────────────────────────────────────────────────────┘
```

**What it is:** The contract between sender and receiver about lost messages. **At-most-once** — fire and forget; failures drop messages. **At-least-once** — retry until acknowledged; failures duplicate messages. **Exactly-once delivery** — the thing everyone wants — is a lie the industry tells: over an unreliable network, a sender that times out cannot know whether the receiver processed the message, so it must retry (duplicating) or not (dropping).

**Key Properties:**
- What *is* achievable is **exactly-once processing**: at-least-once delivery + **idempotent** handling, so duplicates change nothing. When Kafka markets "exactly-once semantics," that's what's under the hood (transactions + dedup) — say this and the interviewer relaxes.
- **At-least-once is the default** for anything that matters; at-most-once is fine only for data you can afford to lose (metrics, presence pings, live cursors).
- The receiver-side crash matters too: process-then-ack = at-least-once (crash before ack → redelivery); ack-then-process = at-most-once (crash after ack → lost). Where you place the ack *is* the semantic.

**Use when:** Say it as a mantra whenever you draw a queue: "at-least-once delivery, so consumers must be idempotent." Then be ready for the follow-up — *how*?

### Idempotency Keys

```
  client generates key once, reuses it on EVERY retry:

  POST /payments  {amount: 50, idempotency_key: "ord-789-attempt"}
                        │
                        ▼
  server: SELECT result FROM idempotency WHERE key='ord-789-attempt'
    hit  → return the STORED response (no side effects — replay, don't redo)
    miss → process, then store (key, response) atomically with the work
```

**What it is:** The universal answer to "the user taps Pay twice." The **client** generates a unique key per logical operation (per *order*, not per HTTP attempt) and sends it on every retry. The server stores the key **with the result**; a duplicate returns the stored result instead of re-executing. This is how Stripe's API works — name it.

**Key Properties:**
- **Client-generated is the point** — only the client knows two requests are the same operation. Server-side dedup by payload hash confuses "retry" with "user legitimately bought the same thing twice."
- **Store the result, not just the key** — a seen-key set can say "duplicate!" but then can't answer the retry. Storing the response makes retries return the *original* outcome, even errors.
- Check-and-record must be **atomic with the side effect** (same DB transaction, or a unique constraint on the key) — otherwise a race between two concurrent retries executes twice anyway.
- **The dedup-window trade:** keys can't live forever — the table grows unboundedly — so you expire them (Stripe: 24h). A retry arriving *after* the window duplicates. Longer window = more storage + hotter lookups; shorter = a wider hole. Pick a window generously beyond your maximum retry horizon and say the trade out loud.

**Use when:** Every mutating endpoint that a client might retry — which is every mutating endpoint. Mandatory for payments, orders, transfers; volunteer it unprompted there.

### The Outbox Pattern

```
  THE BUG (dual write):                 THE FIX (outbox):
  1. INSERT order into DB   ✓           1. ONE transaction:
  2. publish OrderCreated   ✗ crash!         INSERT order
  → order exists, no event —                 INSERT event → outbox table
    downstream never ships it.          2. relay polls outbox (or tails the
  (Reverse the order? Then you             DB's change log / CDC) and
  can get event-without-order.)            publishes; marks sent after ack.
  No transactions across a DB           Crash anywhere → relay retries →
  and a broker — that's 2PC.            AT-LEAST-ONCE, never zero-or-maybe.
```

**What it is:** The standard fix for the **dual-write problem** — needing a database write and an event publish to happen together, without distributed transactions. Write the event into an **outbox table** *in the same local transaction* as the business row; a separate relay reads the outbox and publishes to the broker, retrying until acked.

**Key Properties:**
- The single local transaction makes DB-write and event-record **atomic**; the relay converts "recorded" into "published" with at-least-once guarantees.
- The relay may publish duplicates (crash after publish, before mark-sent) — which is fine, because your consumers are already idempotent. The two halves of this lesson lock together here.
- The polling relay is the simple answer; **CDC** (change data capture — tailing the DB's replication log, e.g. Debezium) is the production-grade name-drop for the same idea.

**Use when:** Any design where a state change must trigger downstream work — order placed → charge card, user signed up → send email. If you draw "write DB, then publish event" as two arrows, the interviewer will ask what happens between them; outbox is the answer.

### Sagas vs Two-Phase Commit

**What it is:** One user action spanning *multiple services* — book flight + reserve hotel + charge card — with no shared database to give you a transaction.

- **Two-phase commit (2PC)** — a coordinator asks all participants to *prepare* (lock resources, vote), then tells everyone to *commit*. Real atomicity, but the coordinator is a blocking single point of failure: if it dies after prepare, participants sit **locked, waiting**, unable to commit or abort. Across independently-owned services, 2PC is the answer you name to reject.
- **Saga** — a sequence of *local* transactions, each publishing an event that triggers the next; on failure, run **compensating actions** to undo completed steps (cancel the flight, refund the charge). No global lock — but also no isolation: intermediate states are visible ("flight booked, hotel pending"), and a compensation is a *new action*, not a rollback (a refund isn't an un-charge).

| | 2PC | Saga |
|---|---|---|
| Atomicity | Real — all or nothing | Eventual — via compensations |
| Availability | Blocks on coordinator failure | Each step commits locally, keeps moving |
| Isolation | Yes (locks held) | No — intermediate states leak |
| Fit | Single admin domain, short transactions | Cross-service workflows — the microservices default |

**Use when:** Sagas are the interview default for multi-service workflows; say **orchestration** (one coordinator service drives the steps — easier to reason about and debug) vs **choreography** (each service reacts to events — no central brain, harder to trace) and pick orchestration for anything money-shaped. Design every step — and every *compensation* — to be idempotent, because the saga engine retries too.

### Ordering Guarantees

**What it is:** "Are messages processed in order?" **Per-partition order is what Kafka gives you** — messages with the same partition key (same user, same order ID) land in one partition and are consumed in sequence. Across partitions: no promise. **Global order costs parallelism** — one totally-ordered stream means one partition means one consumer; you've built a very durable bottleneck.

**Key Properties:**
- The move: **choose a partition key so that the order you need is per-key** — all events for `order:789` share a key, so "created → paid → shipped" is sequential for that order, while millions of orders proceed in parallel. This is the [partitioning](08-partitioning.md) key decision wearing a queue costume.
- Retries can still reorder (a failed message redelivered after its successors) — for state updates, carry a **version/sequence number** and have consumers ignore stale ones.

**Use when:** Volunteer the per-key answer whenever an interviewer asks about ordering; asking "do we need order *globally*, or per user/order?" back at them is exactly the right move.

## The Pattern — Assume Retries, Design for Duplicates

This material shows up the moment your Step-3 diagram has a queue or a cross-service call. The moves, in order:

1. **Declare the semantic at every arrow** — "the queue is at-least-once; consumers ack after processing." Name what's allowed to be at-most-once (metrics), and why.
2. **Make every consumer and endpoint idempotent** — idempotency keys on client-facing mutations; natural idempotence (versioned upserts, "set state to X") inside.
3. **Kill the dual write with an outbox** — any DB-write-plus-publish pair goes through one transaction and a relay/CDC.
4. **Multi-service workflow? Saga with orchestration** — name 2PC, reject it for the blocking coordinator, and specify one compensating action concretely.
5. **Answer ordering with a partition key** — order where it matters (per key), parallelism everywhere else, sequence numbers to survive redelivery.

The invariant to protect: **every side effect happens exactly once *in effect*, no matter how many times its trigger is delivered.** Charge the card once, send the email once, ship the order once — under duplicates, crashes, and replays. Any path where a redelivered message re-executes a side effect is the bug the interviewer is hunting for.

## The Template

The design-interview worksheet lives in [`appendix/templates/system-design/`](../appendix/templates/system-design/). Read the README (when to reach for each component, common traps), then work designs against [`template.md`](../appendix/templates/system-design/template.md) — delivery semantics are the Step-4 deep dive behind every queue you drew in Step 3.

## Practice

This lesson *is* [**Design a Payment System →**](../sd-practice/12-payment-system.md) — idempotency keys, the outbox, and a saga for the multi-step flow are the entire skeleton — and it carries [**Design a Notification System →**](../sd-practice/05-notification-system.md), where "never send the same push twice" meets "never drop a critical alert." Work them back-to-back on the [ladder](../../interview.md#the-design-ladder); the second will feel like a replay of the first, which is the point.

## Check Yourself

- [ ] I can explain why exactly-once *delivery* is impossible and what "exactly-once" actually means in practice.
- [ ] I can design an idempotency-key flow — who generates it, what's stored, why the check must be atomic, and the dedup-window trade.
- [ ] I can draw the dual-write bug and fix it with an outbox table + relay/CDC.
- [ ] I can compare sagas and 2PC in three sentences and name a concrete compensating action.

---

**Up next:** [Specialized Infrastructure](11-specialized-infra.md) — the grab-bag that unlocks specific designs: blob storage, CDNs, search indexes, geo-queries, and the probabilistic structures behind "have I seen this URL before?"

[← Prev](09-consistency-consensus.md) · [🗺 Interview Roadmap](../../interview.md) · [Next →](11-specialized-infra.md)
