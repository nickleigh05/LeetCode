# Intervals

## How to use this README

Problems are split into three tiers: Blind 75 is the core set every interviewer expects you to know cold. NeetCode 150 adds the sweep-line and heap-based approaches needed for harder scheduling problems. NeetCode 250 pushes into full heap simulation with room allocation and deallocation. Work through tiers in order — almost every interval problem starts with the same first step (sort), so the Core Patterns section is structured to build from that foundation outward to sweep lines and heaps.

---

## Problems

### Blind 75
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved |
|-----------|------------|--------------|---------------|--------|
| 57 | Medium | Insert Interval | [Link](https://leetcode.com/problems/insert-interval/) | ☐ |
| 56 | Medium | Merge Intervals | [Link](https://leetcode.com/problems/merge-intervals/) | ☐ |
| 435 | Medium | Non-overlapping Intervals | [Link](https://leetcode.com/problems/non-overlapping-intervals/) | ☐ |
| 252 | Easy | Meeting Rooms | [Link](https://leetcode.com/problems/meeting-rooms/) | ☐ |
| 253 | Medium | Meeting Rooms II | [Link](https://leetcode.com/problems/meeting-rooms-ii/) | ☐ |

### NeetCode 150
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved |
|-----------|------------|--------------|---------------|--------|
| 1851 | Hard | Minimum Interval to Include Each Query | [Link](https://leetcode.com/problems/minimum-interval-to-include-each-query/) | ☐ |

### NeetCode 250
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved | Pattern |
|-----------|------------|--------------|---------------|--------|---------|
| 2402 | Hard | Meeting Rooms III | [Link](https://leetcode.com/problems/meeting-rooms-iii/) | ☐ | Heap simulation |

---

## Complexity Reference

| Pattern / Operation | Time | Space | Notes |
|---------------------|------|-------|-------|
| Sort intervals by start | O(n log n) | O(1) | Always the first step |
| Merge overlapping intervals | O(n log n) | O(n) | One pass after sorting |
| Insert interval (pre-sorted list) | O(n) | O(n) | Three-phase scan |
| Non-overlapping (greedy removal) | O(n log n) | O(1) | Sort by end, greedy keep |
| Sweep line (count concurrent) | O(n log n) | O(n) | Split into events, sort, scan |
| Min-heap (active intervals) | O(n log n) | O(n) | Push/pop by end time |
| Minimum interval per query | O((n+q) log n) | O(n+q) | Offline queries + sorted events |
| Meeting Rooms III simulation | O((n+m) log m) | O(m) | m rooms, two heaps |

---

## Data Structures

### Sorted Interval List

After sorting by start time, the list has the key property that any new interval's start is always >= all previous starts. This single invariant enables every merge and overlap-check algorithm.

```
Before sort:  [[3,5], [1,4], [6,8], [2,6]]
After sort:   [[1,4], [2,6], [3,5], [6,8]]
               ↑ start times are non-decreasing

Merge pass:   current = [1,4]
              [2,6]: 2 <= 4 → overlap → extend to [1,6]
              [3,5]: 3 <= 6 → overlap → [1,6] already covers it
              [6,8]: 6 <= 6 → overlap → extend to [1,8]
              result: [[1,8]]
```

**When it matters:** Every interval problem. Sort first; then decide whether to merge, count overlaps, or find gaps.

### Event / Sweep Line Array

For counting concurrent intervals, decompose each interval [s, e] into two events: a start event (+1 at s) and an end event (-1 at e). Sort all events, then scan with a running counter.

```
Intervals: [0,30], [5,10], [15,20]

Events (before sort):
  (0, +1), (30, -1), (5, +1), (10, -1), (15, +1), (20, -1)

Events (after sort — ends before starts at same time):
  (0,+1)  (5,+1)  (10,-1)  (15,+1)  (20,-1)  (30,-1)
count: 1     2       1        2        1         0

Max concurrent = 2  →  need 2 meeting rooms
```

**When it matters:** Meeting Rooms II (#253), any "maximum overlap at a point" problem. Tie-breaking: sort end events before start events at the same time (a room freed at time t is available for a meeting starting at t).

### Min-Heap of Active Intervals

Push intervals onto a heap keyed by end time. When processing a new interval, pop all intervals that have ended before the new one starts — they are no longer "active." The heap always contains only the currently overlapping intervals.

```
Intervals sorted by start: [[0,30],[5,10],[15,20]]

Process [0,30]:  heap = [(30, [0,30])]          active=1
Process [5,10]:  heap = [(10,[5,10]), (30,[0,30])]  active=2
Process [15,20]: pop [5,10] (10 < 15)
                 heap = [(20,[15,20]), (30,[0,30])]  active=2

Min rooms needed = max active size = 2
```

**When it matters:** Meeting Rooms II (alternative to sweep line), Minimum Interval to Include Each Query (#1851), Meeting Rooms III (#2402).

---

## Core Patterns

### Sort by Start Time
**When to use:** This is step one of almost every interval problem. Sort by the left endpoint so you can process intervals left to right.
**Complexity:** O(n log n) — the sort dominates
**Problems:** All interval problems
**Common mistake:** Sorting by end time when the problem actually needs start-time order (and vice versa for Non-overlapping Intervals — sort by end time there).

```python
intervals.sort(key=lambda x: x[0])   # sort by start
# Now for any i < j: intervals[i][0] <= intervals[j][0]
```

### Merge Overlapping Intervals
**When to use:** Combine all intervals that overlap into a single interval. Two intervals overlap if the start of the second is <= the end of the first (after sorting by start).
**Complexity:** O(n log n) time, O(n) space
**Problems:** Merge Intervals (#56), Insert Interval (#57)
**Common mistake:** Using `<` instead of `<=` — intervals that share a single point (e.g., [1,3] and [3,5]) should be merged into [1,5].

```python
intervals.sort(key=lambda x: x[0])
merged = [intervals[0]]
for start, end in intervals[1:]:
    if start <= merged[-1][1]:              # overlap: extend current interval
        merged[-1][1] = max(merged[-1][1], end)
    else:                                   # no overlap: start a new interval
        merged.append([start, end])
return merged
```

### Sweep Line (Count Concurrent Intervals)
**When to use:** Find the maximum number of intervals active at the same time (= minimum rooms needed).
**Complexity:** O(n log n) time, O(n) space
**Problems:** Meeting Rooms II (#253)
**Common mistake:** At the same timestamp, processing end events before start events — a room freed at time t is available for a new meeting starting at t, so ends should decrement the count first.

```python
events = []
for start, end in intervals:
    events.append((start, 1))    # +1 when a meeting starts
    events.append((end, -1))     # -1 when a meeting ends
events.sort(key=lambda x: (x[0], x[1]))  # sort by time; -1 before +1 at same time
count = max_count = 0
for _, delta in events:
    count += delta
    max_count = max(max_count, count)
return max_count
```

### Min-Heap for Active Intervals
**When to use:** You need to track which specific intervals are currently active, or you need to match new intervals against the earliest-ending active interval.
**Complexity:** O(n log n) time, O(n) space
**Problems:** Meeting Rooms II (#253), Minimum Interval to Include Each Query (#1851), Meeting Rooms III (#2402)
**Common mistake:** Forgetting to push the new interval onto the heap after cleaning up expired ones — the new interval itself becomes active.

```python
import heapq
intervals.sort()
heap = []   # min-heap of end times
for start, end in intervals:
    if heap and heap[0] <= start:
        heapq.heapreplace(heap, end)   # reuse a room that's now free
    else:
        heapq.heappush(heap, end)      # need a new room
return len(heap)                       # total rooms = heap size at end
```

---

## Syntax Reference

### Sorting Intervals

```python
intervals.sort()                           # sort by first element, break ties by second
intervals.sort(key=lambda x: x[0])        # sort by start only
intervals.sort(key=lambda x: x[1])        # sort by end (Non-overlapping Intervals)
intervals.sort(key=lambda x: (x[0], x[1]))  # explicit tuple sort
```

### Insert Interval (Three-Phase Scan)

```python
result = []
i, n = 0, len(intervals)

# Phase 1: add all intervals that end before new_interval starts
while i < n and intervals[i][1] < new_interval[0]:
    result.append(intervals[i])
    i += 1

# Phase 2: merge all overlapping intervals into new_interval
while i < n and intervals[i][0] <= new_interval[1]:
    new_interval[0] = min(new_interval[0], intervals[i][0])
    new_interval[1] = max(new_interval[1], intervals[i][1])
    i += 1
result.append(new_interval)

# Phase 3: add remaining intervals
result.extend(intervals[i:])
return result
```

### Non-overlapping Intervals (Greedy Removal)

```python
# Sort by end time; greedily keep intervals with earliest end
intervals.sort(key=lambda x: x[1])
removed = 0
prev_end = float('-inf')
for start, end in intervals:
    if start >= prev_end:     # no overlap — keep this interval
        prev_end = end
    else:                     # overlap — remove the one with later end (current)
        removed += 1
return removed
```

### heapq Patterns for Intervals

```python
import heapq

# Min-heap of end times (Meeting Rooms II)
heap = []
heapq.heappush(heap, end)
earliest_end = heapq.heappop(heap)   # O(log n)
earliest_end = heap[0]               # peek without removing — O(1)

# heapreplace: pop and push in one O(log n) operation
heapq.heapreplace(heap, new_end)     # only valid if heap is non-empty

# Two heaps (Meeting Rooms III: free rooms + busy rooms)
free = list(range(n))        # free room indices (min-heap)
heapq.heapify(free)
busy = []                    # (end_time, room_index) min-heap
heapq.heappush(busy, (end_time, room_idx))
end_time, room_idx = heapq.heappop(busy)
```

### Offline Query Pattern (Minimum Interval to Include Each Query)

```python
# Sort both intervals and queries; process with a sweep
queries_sorted = sorted(enumerate(queries), key=lambda x: x[1])
intervals.sort()
heap = []    # (size, end) — active intervals
i = 0
result = [-1] * len(queries)
for idx, q in queries_sorted:
    while i < len(intervals) and intervals[i][0] <= q:
        s, e = intervals[i]
        heapq.heappush(heap, (e - s + 1, e))   # push (size, end)
        i += 1
    while heap and heap[0][1] < q:   # remove intervals that have ended
        heapq.heappop(heap)
    if heap:
        result[idx] = heap[0][0]     # smallest active interval size
return result
```
