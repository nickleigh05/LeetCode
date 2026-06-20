# Intervals

*Sort first — almost always by start, sometimes by end. Merge, count, or query; the pattern is the sort plus one linear pass.*

## Recognize this pattern when...

- The input is a list of **`[start, end]`** pairs (meetings, ranges, segments).
- The ask involves **overlap**: merge them, count conflicts, remove the fewest.
- You need the **maximum number overlapping at once** (rooms, CPUs, arrows).
- You're **inserting** a new interval into a sorted set, or **intersecting** two sets.
- "Minimum number of X to cover / hit all intervals."

## Variations

1. **Merge overlapping** — sort by start, extend or append. *(Merge Intervals)*
2. **Insert into sorted intervals** — emit those before, merge the overlapping run, emit those after. *(Insert Interval)*
3. **Greedy non-overlap** — sort by *end*, keep an interval iff it starts after the last kept end. *(Non-overlapping Intervals, Minimum Arrows)*
4. **Sweep line / max concurrency** — separate sorted starts & ends, +1/−1 counter. *(Meeting Rooms II)*
5. **Two-pointer intersection** — walk two sorted lists, overlap is `[max(starts), min(ends)]`. *(Interval List Intersections)*

## Representative problems

| # | Difficulty | Problem |
|---|------------|---------|
| 252 | Easy | Meeting Rooms |
| 56 | Medium | Merge Intervals |
| 57 | Medium | Insert Interval |
| 435 | Medium | Non-overlapping Intervals |
| 253 | Medium | Meeting Rooms II |
| 1851 | Hard | Minimum Interval to Include Each Query |

## Common bugs & traps

- **Forgetting to sort** — or sorting by the wrong key. Merging sorts by *start*; greedy scheduling sorts by *end*.
- **`<=` vs `<` on touching intervals.** Whether `[1,2]` and `[2,3]` overlap is problem-specific — read the statement.
- **Extending with the new end instead of `max`.** A nested interval (`[1,10]` then `[2,3]`) would wrongly shrink the run.
- **Greedy by start, not end.** "Keep the most non-overlapping intervals" only works greedily when you sort by finish time.
- **Sweep line losing pairing.** Sorting starts and ends separately is fine for *counting*, but if you need *which* interval, keep `(time, +1/-1)` events instead.
- **Empty input.** Return `[]` / `0` before indexing `intervals[0]`.
