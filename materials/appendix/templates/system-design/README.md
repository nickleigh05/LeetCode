# System Design

*The four-step framework is the template. There's no code to memorize — the reusable skeleton is a conversation structure, and you drill it exactly like a code template: type it from memory, then run designs through it.*

## Recognize this pattern when...

- The prompt is **"design X"** where X is a product or a piece of infrastructure — not a function with inputs and outputs.
- There is **no correct answer**, only defended ones — the grading axis is trade-offs stated aloud.
- The problem is **too big to finish** — scoping it down *is* the first deliverable, not a failure.
- You're asked **"how would this scale?"** about something you just built in a coding round — the mini design question hiding inside other rounds.

## Variations

1. **Infra-flavored** — "design a rate limiter / message queue / cache." Grades component internals: algorithms, data placement, failure handling. *(Rate Limiter, Distributed Cache, Distributed Queue)*
2. **Product-flavored** — "design Instagram / WhatsApp / Uber." Grades decomposition: turning a product into services, then applying the components. *(News Feed, Chat, Ride Sharing)*
3. **Junior emphasis** — fundamentals and structure: a sensible API, one database, a cache with a reason, clear data flow. Depth is a bonus, not the bar.
4. **Senior emphasis** — the deep dives dominate: replication, partitioning, consistency, failure modes. You're expected to *drive* — volunteer the hard parts before being asked.

## The worksheet

[`template.md`](template.md) is the type-out-from-memory skeleton: the four steps with timeboxes, the prompt questions to ask yourself at each one, an estimation scratchpad, and the final trade-offs checklist. Full teaching version: [Lesson 01 — The Design Interview Framework](../../../system-design/01-design-framework.md).

## Representative designs

| # | Tier | Design |
|---|------|--------|
| 01 | Entry | [URL Shortener](../../../sd-practice/01-url-shortener.md) |
| 02 | Entry | [Rate Limiter](../../../sd-practice/02-rate-limiter.md) |
| 06 | Mid | [News Feed](../../../sd-practice/06-news-feed.md) |
| 07 | Mid | [Chat System](../../../sd-practice/07-chat-system.md) |
| 09 | Senior | [Distributed Cache](../../../sd-practice/09-distributed-cache.md) |
| 13 | Senior | [Distributed Message Queue](../../../sd-practice/13-distributed-queue.md) |

The full ladder lives on the [Interview Roadmap](../../../../interview.md#the-design-ladder).

## Common bugs & traps

- **Schema before requirements.** Designing tables for a product you haven't scoped is the #1 opener mistake — it reads as "codes before thinking."
- **Numberless design.** A cache, shard, or queue justified by vibes instead of the Step-2 estimates. The math is 30 seconds and it's what separates you.
- **Over-engineering below the scale.** If your own estimates say 400 QPS and 3 TB, proposing twelve microservices and Kafka reads worse than one Postgres box. Match the architecture to the numbers.
- **Monologuing.** Ten silent-partner minutes at the whiteboard without a check-in ("does this scope match what you had in mind?") wastes your only feedback channel.
- **Answering deep dives you weren't asked.** Follow the interviewer's steer in Step 4 — they're grading a specific competency; fighting the steer hides it.
- **Claiming guarantees you can't defend.** Say "exactly-once" or "strongly consistent" only if you can survive the follow-up "how?" — see [Delivery Semantics](../../../system-design/10-delivery-semantics.md) and [Consistency](../../../system-design/09-consistency-consensus.md).
---

*See also: [Lesson 01 →](../../../system-design/01-design-framework.md) · [🎯 Interview Roadmap](../../../../interview.md) · [the Design Ladder](../../../../interview.md#the-design-ladder)*
