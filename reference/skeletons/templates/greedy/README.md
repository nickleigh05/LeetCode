# Greedy

*Take the locally optimal choice and trust it's globally optimal. The code is short; proving the greedy choice is *correct* is the actual work.*

## Recognize this pattern when...

- The ask is **"minimum / maximum number of ..."** and a simple rule seems to work.
- You can make an irreversible **local decision** at each step without looking ahead.
- It smells like DP but the state space is huge, and there's an obvious "best move".
- **Interval scheduling**, **jump/reach**, or **"can you finish?"** style problems.
- Sorting the input by one key makes the right choice obvious at each position.

## Variations

1. **Running maximum (Kadane)** — extend or restart at each element. *(Maximum Subarray)*
2. **Reachability sweep** — track the furthest index reachable so far. *(Jump Game, Gas Station)*
3. **Interval scheduling** — sort by end, greedily keep compatible intervals. *(Non-overlapping Intervals)*
4. **Frequency / heap greedy** — always spend the most frequent / largest item first. *(Task Scheduler, Reorganize String)*
5. **Two-end greedy** — pair the largest remaining with the smallest. *(Boats to Save People)*

## Representative problems

| # | Difficulty | Problem |
|---|------------|---------|
| 1005 | Easy | Maximize Sum Of Array After K Negations |
| 53 | Medium | Maximum Subarray |
| 55 | Medium | Jump Game |
| 134 | Medium | Gas Station |
| 763 | Medium | Partition Labels |
| 45 | Medium | Jump Game II |

## Common bugs & traps

- **Greedy doesn't actually hold.** The biggest trap: the locally best move isn't globally optimal, and you need DP instead. Sanity-check with a small counterexample before trusting it.
- **Wrong sort key.** Scheduling by *start* instead of *end* breaks the classic interval greedy.
- **Skipping the exchange argument.** "It passed the examples" isn't a proof — greedy fails sneakily on edge cases.
- **Reset vs. running totals.** Gas Station needs both a *total* feasibility check and a *running* tank that resets the start index.
- **Off-by-one on reach.** You can only extend from index `i` if `i <= furthest_reachable`.
- **Initial value.** Seeding `best` with `nums[0]` (not `0` or `-inf`) matters when all values are negative.
