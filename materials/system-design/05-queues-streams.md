# 05. Queues, Streams & Async Work

*Not everything has to happen now — the box that turns "do it" into "promise it's done."*

[← Prev](04-databases-at-scale.md) · [🗺 Interview Roadmap](../../interview.md) · [Next →](06-first-designs.md)

---

> **Builds on:** [Stacks & Queues](../learning/04-stack.md) — the FIFO [queue](../data-structures/queue.md) is literally this lesson's data structure, now with a network in the middle — and [Heaps](../learning/10-heap-priority-queue.md), because a delayed-job queue is a [priority queue](../data-structures/heap.md) ordered by run-at time.

Every design has work that doesn't belong on the request path: sending the email, resizing the video, fanning the post out to a million followers. Do it synchronously and the user waits, the spike hits your database raw, and one flaky downstream takes your whole endpoint down with it. The queue is how you say "accepted" in 10ms and do the real work in the background — and it's the box interviewers probe hardest, because everything interesting about it is a failure mode: retries, duplicates, poison messages, and consumers that can't keep up.

## Concept

### Why Async — The Three Wins

```
  SYNCHRONOUS                              ASYNC
  client ──► app ──► email svc (2s) ──►    client ──► app ──► queue ──► 200 "accepted"
  client waits 2s; email svc down                      │ 10ms          (10ms)
  = request fails                                      ▼
                                              workers drain the queue
                                              at their own pace
```

**What it is:** Putting a buffer between "the request arrived" and "the work happened." The producer writes a message and returns; consumers pull messages and do the work whenever they can.

**Key Properties:**
- **Decoupling** — the app server doesn't know or care whether the email service is up, slow, or being redeployed. It talks to the queue; the queue is always up.
- **Spike absorption** — traffic arrives at 10× your workers' pace for five minutes; the queue grows, then drains. You provisioned for the *average*, not the peak — this is the spike answer that [autoscaling](03-load-balancing.md) is too slow for.
- **Failure isolation** — a downstream dies for an hour; messages wait; nothing is lost and no user saw an error. The blast radius of a failure shrinks to "delayed," which is a much better word than "down."

**Use when:** the work's result isn't needed in the response. The litmus test to say out loud: *"does the user need this done before I return, or just done eventually?"* Eventually → queue.

### Message Queue vs Pub/Sub

```
  MESSAGE QUEUE (work distribution)        PUB/SUB (event broadcast)
  producer ──► [ ▢ ▢ ▢ ] ──► worker A      publisher ──► topic ──► subscriber A (email)
                        └──► worker B                        ├──► subscriber B (analytics)
  each message: consumed by EXACTLY                          └──► subscriber C (cache inval)
  ONE worker — they split the work         each event: EVERY subscriber gets a copy
```

**What it is:** The one distinction that sorts every messaging question. A **message queue** distributes *jobs* — each message is work, and exactly one consumer takes it (workers compete to drain the queue faster). **Pub/sub** broadcasts *events* — "user signed up" happened, and every subscriber that cares gets its own copy, doing independent things with it.

| | Message queue | Pub/sub |
|---|--------------|---------|
| A message is | a job to execute | a fact that occurred |
| Consumed by | exactly one worker | every subscriber |
| Add consumers to | drain faster (more workers) | do more things (new subscriber) |
| Canonical use | resize this image | notify email + analytics + cache |

**Use when:** ask "who needs this message?" One party doing the work → queue. Several independent parties reacting → pub/sub. Real systems use both, often chained: an event fans out via pub/sub, and each subscriber feeds its own work queue.

### Kafka vs RabbitMQ — At Interview Level

**What it is:** The two names you'll actually be asked about, and the one architectural difference that explains everything else. **RabbitMQ** is a *deleting broker*: it holds a message until a consumer acknowledges it, then it's gone — a classic job queue with rich routing. **Kafka** is a *replayable log*: messages append to a partitioned, ordered log and stay for a retention window (days); consumers are just **offsets** — cursors into the log that each consumer group advances independently.

**Key Properties:**
- Kafka's log means **replay**: a new analytics service can start from yesterday's data; a buggy consumer can rewind and reprocess. A deleted message can't be replayed.
- Kafka does pub/sub and queueing at once — each consumer *group* gets every message (pub/sub across groups), while workers *within* a group split partitions (queue within a group).
- RabbitMQ wins on **per-job semantics**: per-message acknowledgment, routing rules, priorities, and simpler operations at modest scale.
- The interview line: *"job-style work at moderate scale → RabbitMQ; high-throughput event streams that several systems consume, or anything you might replay → Kafka."* Don't say Kafka for 50 emails a minute — that's the [over-engineering anti-pattern](01-design-framework.md).

### Backpressure — When Consumers Fall Behind

**What it is:** Producers writing faster than consumers drain, for longer than a spike. The queue isn't a magic sink — it grows, latency-to-processing grows with it, and eventually the broker hits its limits. **Queue depth** (or Kafka consumer lag) is the metric; watching it is non-negotiable.

- **Scale the consumers** — the first answer: workers are stateless, so add more (the [stateless fleet](03-load-balancing.md), pointed at a queue). Kafka caps this at one worker per partition, so partition count is a capacity decision.
- **Shed or degrade** — drop what tolerates dropping (sample the analytics events), or serve a degraded result.
- **Push back** — slow or reject producers (rate limiting at the front door) so the overload stops at the edge instead of compounding in the middle.

**Use when:** volunteer it — "if consumers fall behind, I'll see it in queue depth; workers autoscale on that metric" is a strong unprompted Step-4 line.

### Retries, Backoff & Dead-Letter Queues

```
  attempt 1 ──fail──► wait 1s ──► attempt 2 ──fail──► wait 2s ──► attempt 3 ──fail──►
  wait 4s (+ jitter) ──► attempt 4 ──fail──► ┌──────────────────┐
                                             │ DEAD-LETTER QUEUE │ → alert + human/tooling
                                             └──────────────────┘
```

**What it is:** What happens when processing a message fails. Retrying is mandatory — most failures are transient — but *how* you retry decides whether you recover or dig the hole deeper.

**Key Properties:**
- **Exponential backoff with jitter** — wait 1s, 2s, 4s, 8s between attempts, each ± random noise. Immediate retries hammer a struggling downstream exactly when it can least afford it; jitter stops thousands of failed messages retrying in one synchronized wave (the same herd logic as [jittered TTLs](02-caching.md)).
- **Cap the attempts, then dead-letter** — after N failures, move the message to a **dead-letter queue (DLQ)**: a side queue for messages that will never succeed on their own (malformed payload, deleted user). Without a DLQ, one **poison message** retries forever, clogging a worker and burying the alert in noise. The DLQ gets monitoring and a human.

**Use when:** every consumer you draw. "Retries with exponential backoff and jitter, three attempts, then the DLQ" is one sentence and covers the whole failure path.

### Delivery Semantics — At-Least-Once & Idempotency

**What it is:** The question hiding under every queue: how many times might a message be processed? **Exactly-once is (practically) a myth** — a worker can finish the job and crash *before* acknowledging, and the broker, seeing no ack, redelivers. Your real choices: **at-most-once** (ack before processing — crash loses the job) or **at-least-once** (ack after — crash duplicates the job).

- **At-least-once is the practical default** — lost work is usually worse than repeated work, *provided* you make repetition safe.
- Which means: **consumers must be idempotent** — processing the same message twice must equal processing it once. Standard moves: a natural key with upsert semantics ("set status = sent" is safely re-runnable), or a dedup check on a unique message ID before doing the side effect.
- Say the pair as one unit: *"at-least-once delivery, so consumers are idempotent — the email worker checks a sent-log keyed by message ID before sending."* The full treatment — and where exactly-once claims come from — is [Delivery Semantics →](10-delivery-semantics.md).

### Delayed & Scheduled Jobs

**What it is:** "Send the reminder in 24 hours"; "retry this in 4s." A plain FIFO queue can't express *later* — a delayed queue is really a **priority queue ordered by run-at time**: exactly the [heap](../learning/10-heap-priority-queue.md), peek-min until `run_at <= now`, then execute.

**Python** (the mental model):
```python
import heapq, time

jobs = []                                    # min-heap by run_at
heapq.heappush(jobs, (time.time() + 86400, "send_reminder", user_id))

while jobs and jobs[0][0] <= time.time():    # anything due?
    _, task, arg = heapq.heappop(jobs)
    enqueue(task, arg)                       # hand to the normal work queue
```

In production the heap is Redis (a sorted set scored by timestamp, polled by a scheduler that feeds the real queue) or a broker's native delay feature — but "it's a priority queue on run-at time" is the sentence that shows you see the structure.

## The Pattern — Accept, Enqueue, Drain

The async moves, in the order you make them on any [ladder](../../interview.md#the-design-ladder) design:

1. **Split the work** — for each write, ask what must happen before the response and what can happen after. Move the "after" behind a queue and return early.
2. **Pick the shape** — one consumer doing the job → message queue; many independent reactions → pub/sub; name Kafka or RabbitMQ with the one-line reason.
3. **Draw the workers** — a stateless consumer fleet, scaled on queue depth.
4. **Name the failure path** — retries with exponential backoff + jitter, capped, then the DLQ. One sentence.
5. **Say the semantics** — at-least-once, therefore idempotent consumers, with the concrete dedup mechanism.

The invariant to protect: **once the queue accepts a message, the work eventually happens exactly-once *in effect*** — never silently lost (acks + retries + DLQ) and never harmfully duplicated (idempotency). Every mechanism in this lesson defends one half of that sentence.

## The Template

The design-interview worksheet lives in [`appendix/templates/system-design/`](../appendix/templates/system-design/). Read the README (when to reach for each component, common traps), then work designs against [`template.md`](../appendix/templates/system-design/template.md) — the queue is a Step-3 box ("async work" on the spine), and retries/semantics are among the best Step-4 dives to volunteer.

## Practice

[**Design a Notification System →**](../sd-practice/05-notification-system.md) is this lesson end to end — pub/sub fan-out to channel-specific work queues, retries, DLQs, and idempotency so nobody gets the same push twice. [**Design a Web Crawler →**](../sd-practice/08-web-crawler.md) makes the queue the *center* of the design: the URL frontier is a queue with politeness rules, and backpressure is the whole game. Both live on the [ladder](../../interview.md#the-design-ladder).

## Check Yourself

- [ ] I can name the three wins of async and apply the "now or eventually?" litmus test to any write path.
- [ ] I can explain message queue vs pub/sub in one sentence each, and say when I'd chain them.
- [ ] I can give the Kafka-vs-RabbitMQ answer — replayable log vs deleting broker — and pick one for a given prompt.
- [ ] I can recite the failure path — backoff, jitter, attempt cap, DLQ — and explain why at-least-once forces idempotent consumers.

---

**Up next:** [Putting It Together — Your First Design](06-first-designs.md) — lessons 01–05 are the toolkit; now watch one full design run start to finish, then climb the ladder yourself.

[← Prev](04-databases-at-scale.md) · [🗺 Interview Roadmap](../../interview.md) · [Next →](06-first-designs.md)
