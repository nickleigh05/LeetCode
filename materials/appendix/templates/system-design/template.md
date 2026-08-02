# The Design Interview Worksheet

*Copy this structure onto your paper/whiteboard at the start of every design — practice and real. The timeboxes assume a 45-minute round; scale for 60. Type it from memory before drilling the [ladder](../../../../interview.md#the-design-ladder), same as any code template.*

---

## Step 1 — Requirements & API  ⏱ ~5 min

Ask before you draw. The invariant: **never design a feature you didn't scope.**

```
FUNCTIONAL (what it does)              NON-FUNCTIONAL (how well)
- core action 1: ____________          - read-heavy or write-heavy? ____
- core action 2: ____________          - latency target on hot path: ____
- explicitly OUT of scope: ___         - availability vs consistency bias: ____
                                       - scale hints (DAU, data size): ____
```

Questions to fire at the interviewer:
- "Who are the users and roughly how many?"
- "Is [obvious adjacent feature] in scope?"
- "Which matters more here — latency or consistency?"

Then sketch the API — 2–4 endpoints, one line each:

```
POST /______        body: ______________      returns: ______
GET  /______        returns: ______________
```

## Step 2 — Estimates  ⏱ ~5 min

One-significant-figure math ([recipes](../../../system-design/00e-estimation.md)). The invariant: **every later decision cites a number from here.**

```
QPS:      ____ DAU × ____ actions/day ÷ 100K sec/day  ≈ ____ /s   (×3 peak ≈ ____)
Reads:    ____ : 1 read:write ratio  →  read QPS ≈ ____
Storage:  ____ items/day × ____ bytes  ≈ ____ /day  →  ____ /year
Bandwidth (if media): ____ × ____  ≈ ____ /s
```

Close the step out loud: *"So this is [small enough for one DB / read-heavy → cache / write-heavy → queue or LSM / too big for one machine → partition]."*

## Step 3 — High-level design  ⏱ ~15 min

Boxes and arrows, then **walk one request through the diagram end to end, out loud**. The invariant: **every box earns its place with a sentence.**

```
                       ┌──────────────┐      ┌──────────────┐
  client ──────────►   │              │ ───► │              │
                       │              │      │              │
                       └──────┬───────┘      └──────────────┘
                              │
                       ┌──────▼───────┐
                       │              │
                       └──────────────┘
```

Standard boxes to consider (add only what the numbers justify):
`client → LB → stateless app servers → cache → database`, plus a `queue → workers` lane for anything async, blob storage + CDN for anything large.

Name THE key decision for this design (there's always one — ID generation, fan-out strategy, index type…), give 2–3 options, pick one **with a reason**, and check in: *"Does this match the scope you had in mind, or should I go deeper on something?"*

## Step 4 — Deep dives  ⏱ ~15 min

Follow the interviewer's steer; if none comes, volunteer the sharpest edge. The invariant: **every answer is a trade-off, not a feature.**

Prompts to run through:
- [ ] What breaks first at 10× the load, and what's the fix?
- [ ] What happens when [database / cache / queue / a whole node] dies?
- [ ] Where is the data stale, and why is that acceptable (or how is it bounded)?
- [ ] What's the hot key / hot partition / celebrity here?
- [ ] Any retry path that could double-apply? ([idempotency](../../../system-design/10-delivery-semantics.md))

## Final sweep  ⏱ ~5 min buffer

- [ ] Restate the design in three sentences.
- [ ] Name the biggest weakness yourself — *"the first thing I'd revisit is ____"* (this scores, hiding it doesn't).
- [ ] Tie one decision back to a Step-2 number.

---

*See also: [the framework lesson](../../../system-design/01-design-framework.md) · [README](README.md) — when to reach for what, and the classic traps · [🎯 Interview Roadmap](../../../../interview.md)*
