# 16. Intervals — Practice

The Roadmap follows a curated list called the NeetCode 150 for practice problems. If you want more or fewer problems, check the other lists in [lists/](../../lists/).

---

### 57. Insert Interval — Medium
[LeetCode](https://leetcode.com/problems/insert-interval/)  
Solution: not yet solved in this repo.

Insert a new interval into a sorted, non-overlapping list of intervals, merging as needed. Why does the input already being sorted let you handle this in three clean phases — before, overlapping, after — in one linear pass?

<details>
<summary>Hint</summary>

Walk the intervals once (see [Intervals](../learning/17-intervals.md)): copy every interval that ends before the new one starts, merge every interval that overlaps the new one (expanding its bounds), then copy the rest.
</details>

<details>
<summary>Solution</summary>

```python
res = []
i = 0
n = len(intervals)

while i < n and intervals[i][1] < newInterval[0]:  # phase 1: entirely before, no overlap
    res.append(intervals[i])
    i += 1

while i < n and intervals[i][0] <= newInterval[1]:  # phase 2: overlaps, merge into newInterval
    newInterval = [min(newInterval[0], intervals[i][0]), max(newInterval[1], intervals[i][1])]
    i += 1
res.append(newInterval)

while i < n:                                        # phase 3: entirely after, no overlap
    res.append(intervals[i])
    i += 1

return res
```

Building blocks: [while-loop](../syntax/while-loop.md) · [list-methods](../syntax/list-methods.md) (`.append()`) · [comparison-operators](../syntax/comparison-operators.md) (`min()`, `max()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — a single pass over the intervals.
**Space: O(n)** — the result list.
</details>

---

### 56. Merge Intervals — Medium
[LeetCode](https://leetcode.com/problems/merge-intervals/)  
[Solution file (no hints)](../../problems/0001-0499/56.py)

Merge all overlapping intervals. Why does sorting by start time guarantee that any interval overlapping the current merged one must come *immediately* next?

<details>
<summary>Hint</summary>

Sort intervals by start (see [Intervals](../learning/17-intervals.md)). Walk through them, and if the current interval's start is `<=` the last merged interval's end, extend that merged interval's end; otherwise start a new merged interval.
</details>

<details>
<summary>Solution</summary>

```python
intervals.sort(key=lambda x: x[0])       # sort by start time
res = [intervals[0]]

for start, end in intervals[1:]:           # for loop over the rest
    if start <= res[-1][1]:                  # overlaps the last merged interval: extend it
        res[-1][1] = max(res[-1][1], end)
    else:                                     # no overlap: start a new merged interval
        res.append([start, end])

return res
```

Building blocks: [sorting-key](../syntax/sorting-key.md) · [lambda-functions](../syntax/lambda-functions.md) · [for-loop](../syntax/for-loop.md) · [comparison-operators](../syntax/comparison-operators.md) (`max()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n log n)** — dominated by the sort; the merge pass is O(n).
**Space: O(n)** — the result list (plus O(log n)/O(n) for the sort itself).
</details>

---

### 435. Non-overlapping Intervals — Medium
[LeetCode](https://leetcode.com/problems/non-overlapping-intervals/)  
Solution: not yet solved in this repo.

Find the minimum number of intervals to remove so the rest don't overlap. Why is sorting by *end* time (not start) the key that makes a greedy "keep the earliest-ending interval" strategy correct?

<details>
<summary>Hint</summary>

Sort by end time (see [Intervals](../learning/17-intervals.md)). Greedily keep an interval if it starts at or after the last kept interval's end; otherwise it overlaps and must be removed — ending earliest always leaves the most room for future intervals.
</details>

<details>
<summary>Solution</summary>

```python
intervals.sort(key=lambda x: x[1])       # sort by end time
removed = 0
prev_end = float("-inf")

for start, end in intervals:               # for loop over sorted intervals
    if start >= prev_end:                    # no overlap: keep this interval
        prev_end = end
    else:                                     # overlaps: must remove one (the later-ending one)
        removed += 1

return removed
```

Building blocks: [sorting-key](../syntax/sorting-key.md) · [lambda-functions](../syntax/lambda-functions.md) · [for-loop](../syntax/for-loop.md) · [int-float-basics](../syntax/int-float-basics.md) (`float("-inf")`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n log n)** — dominated by the sort; the scan afterward is O(n).
**Space: O(1)** extra beyond the sort's own space.
</details>

---

### 252. Meeting Rooms — Easy
[LeetCode](https://leetcode.com/problems/meeting-rooms/)  
Solution: not yet solved in this repo.

Determine if a person can attend all meetings (no overlaps). Why does sorting by start time turn "any overlap anywhere" into a simple adjacent-pair check?

<details>
<summary>Hint</summary>

Sort by start time (see [Intervals](../learning/17-intervals.md)). After sorting, any overlap must occur between *adjacent* meetings, so just check that each meeting starts at or after the previous one ends.
</details>

<details>
<summary>Solution</summary>

```python
intervals.sort(key=lambda x: x[0])       # sort by start time

for i in range(1, len(intervals)):         # for loop checking each adjacent pair
    if intervals[i][0] < intervals[i - 1][1]:   # this meeting starts before the last one ends
        return False

return True
```

Building blocks: [sorting-key](../syntax/sorting-key.md) · [lambda-functions](../syntax/lambda-functions.md) · [for-loop](../syntax/for-loop.md) · [if-return](../syntax/if-return.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n log n)** — dominated by the sort; the scan afterward is O(n).
**Space: O(1)** extra beyond the sort's own space.
</details>

---

### 253. Meeting Rooms II — Medium
[LeetCode](https://leetcode.com/problems/meeting-rooms-ii/)  
Solution: not yet solved in this repo.

Find the minimum number of meeting rooms needed. Why does treating starts and ends as separate sorted "events" let you track the number of rooms in use as a running count, rather than simulating actual room assignments?

<details>
<summary>Hint</summary>

Sort all start times and all end times separately (see [Intervals](../learning/17-intervals.md)). Walk both lists with two pointers: whenever a start occurs before the earliest pending end, a new room is needed; otherwise a room frees up first.
</details>

<details>
<summary>Solution</summary>

```python
starts = sorted(i[0] for i in intervals)
ends = sorted(i[1] for i in intervals)

s, e = 0, 0
rooms = 0
max_rooms = 0

while s < len(starts):                    # while loop, two pointers over starts/ends
    if starts[s] < ends[e]:                  # a meeting starts before the earliest one ends
        rooms += 1
        s += 1
        max_rooms = max(max_rooms, rooms)
    else:                                     # a meeting ends first, freeing up a room
        rooms -= 1
        e += 1

return max_rooms
```

Building blocks: [generator-expressions](../syntax/generator-expressions.md) (`sorted(... for ...)`) · [while-loop](../syntax/while-loop.md) · [comparison-operators](../syntax/comparison-operators.md) (`max()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n log n)** — dominated by sorting the starts and ends.
**Space: O(n)** — the separate starts and ends arrays.
</details>

---

### 1851. Minimum Interval to Include Each Query — Hard
[LeetCode](https://leetcode.com/problems/minimum-interval-to-include-each-query/)  
Solution: not yet solved in this repo.

For each query point, find the size of the smallest interval that contains it. Why does processing queries in sorted order, adding newly-eligible intervals to a min-heap keyed by size, let stale (too-small) intervals be discarded lazily instead of tracked explicitly?

<details>
<summary>Hint</summary>

Sort intervals by start and queries by value. Sweep through sorted queries, pushing every interval whose start is `<=` the query onto a min-[heap](../data-structures/heap.md) keyed by `(size, end)`. Pop off intervals whose `end` is too small for the current query (lazy deletion) — the heap's root is then the smallest valid interval.
</details>

<details>
<summary>Solution</summary>

```python
import heapq

intervals.sort()                          # sort by start
sorted_queries = sorted(range(len(queries)), key=lambda i: queries[i])

heap = []                                  # (size, end)
res = [0] * len(queries)
i = 0

for q_idx in sorted_queries:                # for loop over queries in ascending order
    q = queries[q_idx]

    while i < len(intervals) and intervals[i][0] <= q:  # newly-eligible intervals
        l, r = intervals[i]
        heapq.heappush(heap, (r - l + 1, r))
        i += 1

    while heap and heap[0][1] < q:            # discard intervals that end before this query
        heapq.heappop(heap)

    res[q_idx] = heap[0][0] if heap else -1

return res
```

Building blocks: [sorting-key](../syntax/sorting-key.md) · [heap](../data-structures/heap.md) · [while-loop](../syntax/while-loop.md) (nested) · [for-loop](../syntax/for-loop.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O((n + q) log n)** — n intervals and q queries, each heap push/pop O(log n).
**Space: O(n)** — the heap holds up to all intervals at once.
</details>
