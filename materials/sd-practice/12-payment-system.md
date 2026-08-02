# 12. Design a Payment System — Senior

The Design Ladder works like the DSA practice sets: attempt first, then peek. Work the design on paper against the [framework template](../appendix/templates/system-design/template.md) for a full 45 minutes before opening any step below — the struggle *is* the practice.

[← Back to the lesson](../system-design/10-delivery-semantics.md) · [🗺 Interview Roadmap](../../interview.md)

---

## The prompt

> "Design the payment system for a marketplace. Buyers pay by card through an external payment provider — think Stripe — we track everyone's balances, and we pay sellers out on a schedule."

Typical follow-up constraints when you ask (and you should ask — that's Step 1):

- ~10M payments/day.
- Money is never lost and never moved twice — full stop.
- The external provider (PSP) fails, times out, and rate-limits you; that's a normal Tuesday.
- Every cent must be explainable end-to-end — auditors and regulators will read this system's output.

Why this design near the top of the ladder? It inverts everything below it: the scale is *tiny* and every hard problem is **correctness under partial failure** — [delivery semantics](../system-design/10-delivery-semantics.md) with money on the line. Senior candidates are separated here by what they do when a request neither succeeds nor fails.

<details>
<summary>Step 1 — Requirements & API</summary>

**Functional:**
- Charge a buyer for an order via the PSP.
- Record the money movement: platform fee to us, the rest owed to the seller.
- Track seller balances; pay out on schedule (or on demand).
- Refunds, and (confirm scope) disputes/chargebacks — at least leave room in the model.

**Non-functional:**
- **Correctness over availability** — the only ladder design where this is the right order, and say so: a payment API that's briefly down is an incident; one that double-charges is a lawsuit. Refuse or delay before you guess.
- Idempotent everywhere: clients retry, *we* retry the PSP, and none of it may move money twice.
- Auditable: every balance must decompose into the individual movements that produced it.
- Durable before responsive — no acknowledged payment may ever be forgotten.

**API sketch:**

```
POST /payments
  headers: Idempotency-Key: <client-generated UUID>
  body: { "order_id", "amount_minor": 4999, "currency": "USD", "payment_method": ... }
  returns 201 { "payment_id", "status": "pending" }        # same key → same response, always

GET  /payments/{id}                    → status: pending | succeeded | failed
POST /payouts   (internal/scheduled)   → moves seller balance → bank transfer via PSP
POST /psp/webhooks                     → PSP tells us what actually happened
```

Two things to say out loud: amounts are **integers in minor units** (4999 cents — never floats, never `49.99`), and the response is `pending`, not `succeeded` — the truthful status until the PSP confirms. A synchronous "success" you can't guarantee is the first bug of this design.
</details>

<details>
<summary>Step 2 — Estimates</summary>

One-significant-figure math (the [estimation recipes](../system-design/00e-estimation.md)):

- **Throughput:** 10M/day ≈ 10M / 90K seconds ≈ **~100 payments/s**, peak a few hundred. Small! A single well-run PostgreSQL handles this without noticing — and *saying* "this is not a scale problem, it's a correctness problem" is itself the Step 2 deliverable here.
- **Storage:** each payment produces a handful of ledger entries, ~1 KB total → 10M × 1 KB ≈ **10 GB/day, ~4 TB/year** — and it's append-only, so it only grows. Years of history in one database plus cheap archives. Fine.
- **PSP ceiling:** the *external provider's* rate limits (and their 99.9-ish availability) bound your throughput long before your hardware does. Your real capacity problem is queueing and retry behavior when they slow down, not your own QPS.
- **Reconciliation batch:** 10M records/day diffed against the PSP's daily report — a nightly batch job on one machine. Minutes.

The numbers just decided the *shape* of the effort: zero exotic infrastructure — a boringly reliable relational database with real transactions — and all engineering budget spent on failure handling, idempotency, and audit. If your design has sharding in it, you sized the wrong problem.
</details>

<details>
<summary>Step 3 — High-level design</summary>

```
 Buyer ──► ┌─────────────┐  1. persist intent   ┌──────────────────────┐
           │ Payment API │ ───────────────────► │  Payments DB         │
           │ (idempotency│                      │  payment: pending    │
           │  key check) │  2. charge (same key)│  + idempotency table │
           └──────┬──────┘ ──────────────┐      └──────────┬───────────┘
                  │                      ▼                 │ 3. on confirm
                  │               ┌────────────┐           ▼
      webhooks ──►│◄───────────── │  PSP       │   ┌──────────────────┐
      + polling   │               │ (external) │   │  LEDGER (append- │
                  │               └────────────┘   │  only, double-   │
                  ▼                                │  entry)          │
           ┌─────────────┐    daily PSP report    └────────┬─────────┘
           │ Reconciler  │◄──────────────────────          │ derived
           └──────┬──────┘   diff vs ledger                ▼
                  ▼                                 balances (snapshot
           discrepancy queue (humans)               + entries since)
```

**Idempotency keys, end-to-end — the spine of the design.** The client generates a key per payment attempt; the API stores `key → (request-hash, response)` and replays the stored response on any retry — a retried `POST /payments` can never create a second charge. The *same* key travels **onward to the PSP** on their idempotency header, so *your* retries against them are also safe. One key, one money movement, no matter how many times any network hiccups — this is [delivery semantics](../system-design/10-delivery-semantics.md) applied where it matters most: at-least-once retries made safe by idempotent effects.

**The double-entry ledger — the source of truth.** Every movement is a **balanced pair of entries** — debit one account, credit another, summing to zero:

```
buyer_receivable   -49.99   │  A $49.99 sale = two balanced pairs:
platform_cash      +49.99   │  money in from buyer,
platform_cash       -44.99  │  then the seller's share moved
seller_payable      +44.99  │  to what we owe them (fee stays).
```

Rules worth stating as rules: the ledger is **append-only** — corrections are new reversing entries, never edits (immutability *is* the audit trail); **balances are derived, not mutated** — a balance is the sum of an account's entries, so it can always be rebuilt and always explained; every entry carries the `payment_id` it came from, so any cent traces to its cause.

**PSP integration — the key decision is the order of operations:**

1. **Call the PSP first, persist on success** — if you crash between the two, you charged a card *and have no record of it*. The unforgivable version.
2. **Persist intent first, then charge** — a `pending` payment row exists *before* any external call. Crash after the PSP call? The pending row is a visible loose end that recovery and webhooks will resolve. Nothing can be charged without a trace.
3. **Two-phase commit across your DB and the PSP** — impossible: Stripe's API is not a transaction participant; there is no prepare/vote/commit to enroll them in. Name this and move on — wishing for distributed transactions across company boundaries is the trap.

Pick **2**, always. The general pattern: **persist intent → side effect → persist outcome**, with every `pending` row owned by a recovery process. Since there's no 2PC, multi-step flows (charge → ledger → notify; payout: reserve balance → bank transfer → confirm) run as a **saga** — a sequence of local transactions with **compensating actions** for backing out (refund the charge, release the reservation) when a later step fails permanently.

**Webhooks + polling:** the PSP's webhook ("charge succeeded") is how most payments leave `pending` — verify its signature, process it idempotently (they redeliver), and *also* poll the PSP for stale pending payments, because webhooks get lost. Two independent paths to the truth.

**Reconciliation — the safety net under everything.** Nightly: diff the PSP's settlement report against your ledger, entry by entry. Matches confirm; mismatches (a charge they have and you don't, an amount that differs) go to a **discrepancy queue** for automated then human resolution. Reconciliation is what turns "we believe the system is correct" into "we verify it against external reality every day" — say that sentence.
</details>

<details>
<summary>Step 4 — Deep dives & what interviewers probe</summary>

**"You call the PSP to charge $50 and the request times out. What do you do?"** — The crown jewel; get this right and the interview is won. A timeout is **not a failure — it's the unknown state**: the charge may or may not have happened. Never treat it as "failed" and never retry with a *fresh* idempotency key — that's the double charge. The answer: retry with **the SAME idempotency key** — if the first attempt landed, the PSP returns the original result; if it didn't, the charge happens once now. Meanwhile the payment sits honestly in `pending` (persisted *before* the call — Step 3's ordering paying off), and webhooks/polling/reconciliation are three independent ways the truth eventually arrives. Distinguishing *unknown* from *failed* is the whole senior skill this design tests.

**"So do you deliver payments exactly-once?"** — No one does, and say so plainly: exactly-once *delivery* is an illusion over lossy networks ([delivery semantics](../system-design/10-delivery-semantics.md)). What you build is at-least-once attempts + idempotent effects = **exactly-once *outcome***. Every layer repeats the pattern: client→API (idempotency table), API→PSP (their idempotency key), PSP→you (webhook redelivery + idempotent handlers), ledger (unique constraint on `(payment_id, entry_type)` as the final backstop).

**"Two concurrent payout runs read a seller's $100 balance and both send $100. Or: a refund lands mid-payout and the balance goes negative."** — Serialize per account: money-moving operations on one account must not interleave. Mechanisms, any one of which works at 100/s: a `SELECT ... FOR UPDATE` on the account row inside the transaction, **optimistic versioning** (retry on version conflict), or a **single-writer** design (route each account's movements through one worker). Plus the invariant check *inside* the same transaction: reserve-then-pay, and a reservation that would take the balance negative fails. The ledger makes violations detectable; serialization makes them impossible.

**"Every payment touches the platform's cash account — isn't that row a bottleneck?"** — The hot-account problem, and the ledger's structure answers it: you never `UPDATE` a balance row — you **append entries** (inserts don't contend) and maintain balances as **periodic snapshots + sum of entries since**. The platform account's "balance" is computed, not a lock everyone queues on. If appends themselves ever grew hot, sub-accounts summing to the parent — but at 100/s, they won't.

**"Why integer minor units? And what about currencies?"** — Floats can't represent 0.1 exactly; accumulate a few million payments of binary rounding error and reconciliation lights up with phantom cents. Integers in the currency's minor unit (cents, pence, yen-with-zero-decimals — the exponent varies, store it) make every amount exact. Rounding (fee percentages, FX) happens at explicitly chosen points with a documented rule, and the rounding remainder is *itself booked* to a rounding account — the ledger must balance to zero even for the fractions.

**Common mistakes at this design:**
- Retrying a timed-out charge with a new idempotency key — the double charge, straight to the headline.
- Mutable `balance` column updated in place — no audit trail, no way to explain a number, hot-row contention as a bonus.
- Treating timeout as failure (or as success) instead of as *unknown*.
- Proposing 2PC with the PSP — their API is not your transaction participant.
- Designing for imaginary scale — sharding a 100 QPS system while hand-waving the failure paths that actually matter.
</details>

---

**Next on the ladder:** [Design a Distributed Message Queue →](13-distributed-queue.md) — the capstone: build the infrastructure every design on this ladder has been quietly leaning on.
