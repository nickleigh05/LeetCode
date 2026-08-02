# 05. Design a Notification System — Mid

The Design Ladder works like the DSA practice sets: attempt first, then peek. Work the design on paper against the [framework template](../appendix/templates/system-design/template.md) for a full 45 minutes before opening any step below — the struggle *is* the practice.

[← Back to the lesson](../system-design/05-queues-streams.md) · [🗺 Interview Roadmap](../../interview.md)

---

## The prompt

> "Design a notification service — a single system that other teams call to send push notifications (APNs/FCM), emails, and SMS to users."

Typical follow-up constraints when you ask (and you should ask — that's Step 1):

- **~100M notifications/day** — ~1K/s average, but **~10K/s peaks** when a marketing blast fires.
- Notifications must not be lost — **at-least-once** delivery into each channel.
- But retries must not double-send — an OTP arriving twice is confusing; a marketing email arriving twice is a spam report.
- Users have **preferences** (opt-outs per channel/category) and **quiet hours**.
- The third-party providers (APNs, FCM, SES, Twilio) rate-limit you and *will* have outages.

Why this design? It's the [queues lesson](../system-design/05-queues-streams.md) as a whole system — every classic queue concept (buffering, retries, backoff, DLQs, idempotency, backpressure) shows up load-bearing rather than decorative.

<details>
<summary>Step 1 — Requirements & API</summary>

**Functional:**
- Accept a send request from an internal service: recipient, channel(s), template + data, priority.
- Resolve user preferences and quiet hours *before* sending — an opt-out must actually stop the message.
- Render templates per channel (push payload vs email HTML vs 160-char SMS).
- Track delivery status (accepted → sent → delivered/failed) queryable by the caller.

**Non-functional:**
- **At-least-once** into each channel — accepted means it will eventually send or land somewhere visible (DLQ), never silently vanish.
- **No duplicates from our retries** — idempotency end to end.
- Absorb the 10× peak without dropping anything: accept fast, deliver asynchronously.
- Provider failures are routine, not exceptional — the design must assume them.

**API sketch:**

```
POST /api/notifications
  headers: Idempotency-Key: order-svc:order-9812:shipped
  body: {
    "user_id": "u42",
    "channels": ["push", "email"],
    "template": "order_shipped",
    "data": { "order_id": "9812" },
    "priority": "transactional"     # vs "marketing"
  }
  returns 202: { "notification_id": "n_7f3a" }

GET /api/notifications/n_7f3a
  returns 200: { "push": "delivered", "email": "sent" }
```

One decision worth saying out loud: the API returns **202 Accepted, not 200 Sent**. The caller hands off responsibility and moves on; delivery is asynchronous behind the queue. That single status code *is* the architecture.
</details>

<details>
<summary>Step 2 — Estimates</summary>

Keep it to one-significant-figure math (the [estimation recipes](../system-design/00e-estimation.md)):

- **Throughput:** 100M/day ≈ **1K/s average, 10K/s peak**. Both are modest for a queue (Kafka-class systems do millions/s) — the queue isn't there for throughput, it's there to decouple your peak from the providers' ceilings.
- **The mismatch that justifies everything:** a marketing blast wants 10K/s; your SMS provider allows, say, 200/s. Without a buffer you drop 98% of the burst. With one, a 10-minute blast of 6M sends drains through SMS over hours — the queue converts a spike into a steady drip.
- **Storage:** ~1 KB per notification record (payload + status + timestamps) × 100M/day ≈ **100 GB/day** — keep 30 days hot (~3 TB), archive the rest.
- **Queue depth during a provider outage:** 1 hour down at 1K/s = **3.6M messages queued** ≈ 4 GB. Trivial for any real broker — an outage is a delay, not a loss.

The numbers just decided the shape: queues for burst-vs-provider impedance matching (not throughput), sized retention, and proof that an hour-long outage is absorbable.
</details>

<details>
<summary>Step 3 — High-level design</summary>

```
 order-svc ──► ┌────────────┐   ┌─────────────────┐
 auth-svc  ──► │ Notif API  │──►│ Preference/     │
 mktg-svc  ──► │ (validate, │   │ quiet-hours     │
               │ dedupe,    │   │ check           │
               │ persist)   │   └─────────────────┘
               └─────┬──────┘
                     │ fan-out per channel
        ┌────────────┼────────────────┐
   ┌────▼────┐  ┌────▼────┐     ┌─────▼────┐
   │ push q  │  │ email q │     │  sms q   │   (+ separate priority
   └────┬────┘  └────┬────┘     └─────┬────┘    lanes per channel)
   ┌────▼────┐  ┌────▼────┐     ┌─────▼────┐
   │ push    │  │ email   │     │ sms      │  workers: render template,
   │ workers │  │ workers │     │ workers  │  call provider, record status
   └────┬────┘  └────┬────┘     └─────┬────┘
   ┌────▼────┐  ┌────▼────┐     ┌─────▼─────┐
   │APNs/FCM │  │ SES /   │     │ Twilio →  │  provider adapters
   │ adapter │  │ adapter │     │ failover  │  (retry + backoff + DLQ)
   └─────────┘  └─────────┘     └───────────┘
```

**The flow:** producer calls the API with an idempotency key → validate, check preferences/quiet hours, persist the record, dedupe → **fan out one message per requested channel onto that channel's queue** → channel workers pull at each provider's sustainable rate, render the template, call the provider adapter, record the outcome.

**The key structural decision — one queue or one per channel?**

1. **Single shared queue** — simplest, but the channels' failure domains merge: a Twilio outage backs up messages that only needed APNs, and head-of-line blocking punishes every channel for the slowest one.
2. **Queue per channel** (pick this) — each channel drains at its own provider's pace, fails independently, and scales its workers independently. The extra queues cost nothing; the isolation is the whole point.
3. Per-channel *and* per-priority — the refinement Step 4 demands (OTP vs marketing); same argument one level down.

**Reliability plumbing, worker-side:** ack the queue message only after the provider accepts; on provider error, retry with **exponential backoff + jitter**; after N attempts, park it in a **dead-letter queue** with the error attached — visible and replayable, never silently dropped. That ack-late discipline is what makes the at-least-once guarantee real (the full semantics story is the [delivery-semantics lesson](../system-design/10-delivery-semantics.md)).

**Provider abstraction:** workers call an adapter interface, not Twilio's SDK. Run two SMS providers behind it; health-check and fail over when one degrades. Same for email. (APNs/FCM have no substitutes — for those, "failover" means queue-and-wait.)
</details>

<details>
<summary>Step 4 — Deep dives & what interviewers probe</summary>

**"Your SMS provider is down for an hour. Walk me through it."** — Workers see failures, back off, stop pulling; the SMS queue absorbs (~3.6M messages/hour ≈ 4 GB — Step 2 already sized it). Other channels are untouched because the queues are separate. Meanwhile the adapter's health check fails over to the second provider for new sends. When the primary recovers, drain the backlog *rate-limited* — blasting an hour of backlog at full speed just triggers the provider's rate limiter and a second incident. If the queue ever approaches real limits, apply **backpressure** at the API: reject new *marketing* enqueues first, keep accepting transactional.

**"A user got the same notification twice. Where's your bug?"** — Trace both layers. Layer 1: the producer retried the API call — caught by the **Idempotency-Key** on the write path (dedupe against recent keys before enqueueing). Layer 2: a worker sent, then crashed before acking; the message redelivered — caught by a per-`(notification_id, channel)` sent-marker checked before calling the provider. At-least-once delivery *plus* idempotent processing is how you fake exactly-once — name that framing explicitly.

**"A marketing blast of 5M is queued and a user requests a password-reset OTP. When does it arrive?"** — If they share a queue: after the blast — unacceptable. And "priority fields" inside one queue don't help; most brokers won't reorder. The answer is **separate queues as priority lanes**: `sms-transactional` and `sms-marketing`, with transactional workers always provisioned and marketing workers throttled first. The OTP jumps the line because it was never in the same line.

**"Where do preferences and quiet hours get enforced?"** — At enqueue time for opt-outs (don't queue what you'll never send) — but quiet hours are trickier: a message queued at 9pm for a quiet-hours user should be *scheduled* for 8am, not dropped and not sent at 2am when the queue drains. Delayed delivery / scheduled messages, and marketing respects quiet hours while an OTP overrides them — a product rule the design must encode.

**Common mistakes at this design:**
- Synchronous sending — the API calls Twilio inline and the 202-vs-200 distinction never happens; the first blast takes the API down.
- One queue for everything — merged failure domains, and no answer to the OTP-behind-the-blast probe.
- Retries with no idempotency — at-least-once quietly becomes at-least-twice.
- No DLQ — the poison message that can never send blocks or vanishes, and "none lost" was the requirement.
</details>

---

**Next on the ladder:** [Design a News Feed →](06-news-feed.md) — the fan-out you just built per channel comes back per *follower*, and one celebrity breaks it.
