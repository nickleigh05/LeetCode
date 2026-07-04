# The Coding Interview

*What actually happens in the room, what's being graded, and how to practice the part that isn't code.*

LeetCode skill and interview skill overlap about 70%. The other 30% — thinking out loud, collaborating, handling being stuck while watched — has to be practiced separately, and this repo's problems are the raw material.

## What's actually being graded

Interviewers typically score four things, roughly equally:

1. **Problem solving** — did you find a reasonable approach, and could you explain *why* it works?
2. **Coding** — clean, working code; sensible names; no flailing.
3. **Communication** — could they follow your thinking the whole way? Would they want to work with you?
4. **Verification** — did you test your own code unprompted, or declare victory and wait?

A silent perfect solution scores *worse* than a narrated good one. They can't grade thinking they can't hear.

## The choreography (45-minute loop)

1. **Restate the problem** and ask 2–3 clarifying questions (empty input? duplicates? sorted? expected sizes?). This is step 1 of [how-to-approach-a-problem](how-to-approach-a-problem.md), performed aloud.
2. **Propose the brute force with its complexity** *before* optimizing: "Naively I'd check all pairs — O(n²). Let me see if a hash map removes the inner loop." This proves baseline competence, banks partial credit, and often earns a hint.
3. **Get sign-off on the plan** — "I'll do one pass with a map from value to index; sound good?" — *then* code. Coding an unapproved plan wastes your only non-renewable resource: minutes.
4. **Narrate while coding**, at the level of intent ("storing the complement here so lookup is O(1)"), not syntax ("now a for loop").
5. **Test before they ask.** Trace one example and one edge case by hand, out loud. Finding your own bug is worth more than not having one.
6. **State final complexity** — time and space, with one sentence of why.

## When you're stuck (it's expected)

- Say what you're considering and why it fails — "DFS explores all paths but that's exponential; there's overlap, so maybe DP" *is* problem-solving, out loud. Silence reads as drowning.
- Return to the constraints and your worked example; both leak the pattern (see [constraints-cheatsheet](constraints-cheatsheet.md)).
- **Take hints gracefully.** A hint acted on quickly scores fine; a hint bounced off scores terribly. Interviewers *want* to hand you the rope.
- Out of time? Sketch the rest verbally: "I'd handle the duplicate case by X." Partial credit is real.

## How to practice this

- **Mock interviews** — the only way to train the performance layer. Pramp / interviewing.io / a friend with a problem you haven't seen. One mock per week once you're past [Phase 4 of the roadmap](../../roadmap.md).
- **Talk during solo practice** — literally narrate to your empty room for a few problems a week. Feels ridiculous, works.
- **Timebox** — 35 minutes per problem, then move on and study the gap. Interviews are timed; practice should sometimes be too.

## Logistics people forget

- **Language:** Python is fine everywhere (rare embedded/HFT exceptions). Say what you're using; don't ask permission.
- **Whiteboard / CoderPad without autocomplete:** practice writing 20 lines on paper occasionally — you'll discover you don't actually know [`heapq`'s](../syntax/heapq-module.md) argument order.
- **Behavioral questions are half the interview loop.** Prepare 4–5 stories (conflict, failure, proudest work, disagreement) in situation → action → result shape. Strong candidates fail loops on this half too.
- Ask the recruiter what the rounds are. "Two DSA + one system design + one behavioral" changes your prep allocation.

**Related:** [how-to-approach-a-problem](how-to-approach-a-problem.md) · [study-plan](study-plan.md) · [whats-next](whats-next.md)
