"""
Intervals — Sort-First Merge and Sweep-Line Skeletons

Interval problems almost always begin the same way: sort, then make one linear
pass. Sorting imposes an order that lets a single comparison — "does this
interval touch the last one?" — decide everything.

  1. MERGE / sort by START — walk left to right, extending or closing the current
                             run. For merging, inserting, counting non-overlaps.
  2. SWEEP LINE            — treat each start as +1 and each end as -1, sort the
                             events, and track a running count (max concurrency).

Invariant (merge): `merged` holds disjoint intervals sorted by start, so the
LAST one is the only candidate the next interval can possibly overlap.
"""

from typing import List


def merge_intervals(intervals: List[List[int]]) -> List[List[int]]:
    """Merge all overlapping intervals into a minimal disjoint set.

    Time:      O(n log n) — the sort dominates; the scan is O(n).
    Space:     O(n) for the output (O(1) extra beyond it).
    Invariant: because the input is sorted by start, only the last merged
               interval can overlap the one we're about to add — so one
               comparison suffices.
    """

    if not intervals:
        return []

    # Sort by start so any overlapping intervals become adjacent.
    intervals.sort(key=lambda interval: interval[0])

    merged: List[List[int]] = [intervals[0]]

    for start, end in intervals[1:]:
        last_end = merged[-1][1]

        # TODO: problem-specific overlap test. `start <= last_end` treats
        # touching intervals ([1,2],[2,3]) as overlapping; use `<` to keep them
        # separate.
        if start <= last_end:
            # Overlap: stretch the current run to cover both (max, since the
            # incoming interval may be fully nested inside the current one).
            merged[-1][1] = max(last_end, end)
        else:
            # Disjoint: close the current run and open a new one.
            merged.append([start, end])

    return merged


def max_concurrent(intervals: List[List[int]]) -> int:
    """Sweep line: the most intervals overlapping at any single instant.

    This is the "minimum meeting rooms" shape.

    Time:      O(n log n) to sort the two endpoint arrays.
    Space:     O(n)
    Invariant: scanning starts and ends in time order, `active` is exactly how
               many intervals are currently open; its running max is the answer.
    """

    starts = sorted(interval[0] for interval in intervals)
    ends = sorted(interval[1] for interval in intervals)

    start_index = 0
    end_index = 0
    active = 0
    best = 0

    while start_index < len(starts):
        # If the next start happens before the next end, a new interval opens.
        # `<` lets an interval ending exactly when another starts free the room;
        # flip to `<=` if that should count as a conflict.
        if starts[start_index] < ends[end_index]:
            active += 1
            best = max(best, active)
            start_index += 1
        else:
            # An interval closes before (or as) the next one opens.
            active -= 1
            end_index += 1

    return best
