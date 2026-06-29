# 17. Intervals
*Sort first, then one linear pass to merge, count, or sweep.*

[← Prev](16-greedy.md) · [🗺 Roadmap](../roadmap.md) · [Next →](18-bit-manipulation.md)

---

> **Builds on:** sorting from [Lesson 05](05-binary-search.md). Every interval problem starts by sorting.

Interval problems — merging, inserting, counting overlaps, meeting rooms — almost always start the same way: **sort by start time**, then sweep once, comparing each interval to the last. Recognize the family and the solution is mechanical.

## The Pattern

### Merge Intervals

```
  Input: [[1,3],[2,6],[8,10],[15,18]]
  Sort by start time:

  Timeline:
  [1──────3]
       [2──────6]
                    [8───10]
                                  [15────18]

  Merge overlapping:
  current=[1,3], next=[2,6]: 2 ≤ 3 → overlap → merge to [1,6]
  current=[1,6], next=[8,10]: 8 > 6 → no overlap → save [1,6]
  current=[8,10], next=[15,18]: 15 > 10 → no overlap → save [8,10]
  Final: [[1,6],[8,10],[15,18]]

  Insert interval:
  existing=[[1,3],[6,9]], new=[2,5]
  → merge [1,3] and [2,5] → [1,5]
  → merge [1,5] and [6,9]? 6 > 5 → no
  Result: [[1,5],[6,9]]
```

**What it is:** Sort intervals by start time, then scan linearly, merging any interval that overlaps with the last merged interval.

**Use this when:**
- [ ] Merge overlapping intervals
- [ ] Insert a new interval into a sorted list
- [ ] Find minimum number of meeting rooms needed
- [ ] Find gaps between intervals
- [ ] Employee free time

**Python:**
```python
# Merge intervals
def merge(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = []
    for start, end in intervals:
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged

# Insert interval
def insert(intervals, new_interval):
    result = []
    i = 0
    n = len(intervals)
    # Add all intervals that end before new_interval starts
    while i < n and intervals[i][1] < new_interval[0]:
        result.append(intervals[i]); i += 1
    # Merge all overlapping intervals
    while i < n and intervals[i][0] <= new_interval[1]:
        new_interval[0] = min(new_interval[0], intervals[i][0])
        new_interval[1] = max(new_interval[1], intervals[i][1])
        i += 1
    result.append(new_interval)
    # Add remaining
    result.extend(intervals[i:])
    return result

# Meeting rooms II — minimum rooms needed
import heapq
def min_meeting_rooms(intervals):
    intervals.sort(key=lambda x: x[0])
    heap = []   # min-heap of end times
    for start, end in intervals:
        if heap and heap[0] <= start:
            heapq.heapreplace(heap, end)   # reuse a room
        else:
            heapq.heappush(heap, end)      # new room needed
    return len(heap)
```

**Complexity:** O(n log n) for sort, O(n) for merge scan.

**Blind 75 examples:** Merge Intervals · Insert Interval · Non-overlapping Intervals · Meeting Rooms · Meeting Rooms II

## The Template

The reusable code skeleton for this pattern lives in [`appendix/templates/intervals/`](../appendix/templates/intervals/). Read the README (when to reach for it, variations, common bugs), then type out [`template.py`](../appendix/templates/intervals/template.py) from memory before you drill problems.

## Practice

Work the matching set in the curated list: [**Intervals problems →**](../../lists/recommended.md#16-intervals-10-problems). Easy → hard, top to bottom. When the pattern feels automatic, move on — don't grind it forever.

## Check Yourself

- [ ] My reflex on an interval problem is "sort first" — by start or by end as the problem needs.
- [ ] I can write the merge-overlapping-intervals sweep from memory.
- [ ] I can use a heap to track active intervals (meeting rooms / minimum platforms).
- [ ] I solved a 🔴 Hard interval problem (e.g. Employee Free Time or Minimum Interval to Include Query).

---

**Up next:** [Bit Manipulation](18-bit-manipulation.md) — masks, shifts, and XOR cancellation in O(1).

[← Prev](16-greedy.md) · [🗺 Roadmap](../roadmap.md) · [Next →](18-bit-manipulation.md)

