# Study Plan & Retention

*How to schedule the grind so topics stick — spaced repetition, the 30-minute rule, and what a realistic week looks like.*

The failure mode isn't "not smart enough"; it's binging 15 array problems in a weekend, moving on, and remembering nothing three weeks later. Retention is a scheduling problem.

## The core loop (per topic)

The [roadmap](../../roadmap.md) already defines it: read the lesson → type out the [template](../appendix/templates/README.md) from memory → drill the practice set easy → hard → pass the lesson's check-yourself boxes. Two rules make it stick:

- **The 30-minute rule.** Stuck for 30 minutes with no viable idea? Read a hint or the first bit of the editorial, close it, implement from memory. Never scroll a full solution *while* your editor is open — copying compiles to nothing.
- **Solved-with-help ≠ solved.** If you needed the editorial, the problem goes back in the queue for a from-scratch re-solve in ~3 days. It only counts when you've done it cold.

## Spaced repetition, concretely

Re-derive material at growing intervals — each successful recall roughly doubles how long you keep it:

- **Topic level:** after finishing a topic, re-type its template from memory at +3 days, +1 week, +1 month. Five minutes each time.
- **Problem level:** keep a "redo list" of every problem that beat you. Retry cold after 3 days, then a week later. Two clean solves = it graduates.
- **Rolling warm-up:** start each session with one random problem from *any earlier topic* (10–15 min). This single habit prevents the "I forgot sliding window while learning graphs" decay, because DSA is cumulative.

A text file with dates works fine. So does Anki with problem names as cards ("LC 875 — what's the approach?" → "binary search on the answer"). Tool doesn't matter; the schedule does.

## A realistic week (~1 hr/day)

| Day | Session |
|-----|---------|
| Mon–Thu | Warm-up redo (15 min) + current-topic lesson/problems (45 min) |
| Fri | Redo-list day: only past failures, cold |
| Sat | Longer block: finish the topic, or one mock interview ([interview-guide](interview-guide.md)) |
| Sun | Off, or template re-typing (light) |

At that pace the full roadmap through Phase 6 is roughly **3–5 months** — slower than the "Blind 75 in 30 days" posts promise, and unlike them, it sticks. Doubling daily hours doesn't halve the time; consolidation needs the nights in between.

## Plateaus and morale

- **Quality over count.** 150 problems *understood* (could re-solve, could explain the why) beats 500 pattern-matched. If you can't say *why* the technique applies, you haven't finished the problem.
- **Plateaus are normal** — usually they mean the current topic's prerequisite is shaky. Feeling lost in [DP](../learning/14-dp-1d.md)? The gap is usually [recursion](../learning/04b-recursion.md). Go back one layer; it's faster than pushing forward.
- **Post-solve ritual (2 min):** state the pattern, the complexity, and the one insight that unlocked it ("sorted input → two pointers"). Saying it is what indexes it for recall.
- **Streaks measure attendance, not learning.** A missed day costs nothing; quitting over a broken streak costs everything. Track "problems I can re-solve cold" instead.

**Related:** [how-to-approach-a-problem](how-to-approach-a-problem.md) · [interview-guide](interview-guide.md) · [glossary](glossary.md) · [Roadmap](../../roadmap.md)
