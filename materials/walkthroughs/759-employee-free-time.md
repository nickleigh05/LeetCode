# 759. Employee Free Time

**Hard** · 🔒 Premium · [LeetCode](https://leetcode.com/problems/employee-free-time/) · [Solution file (no hints)](../../problems/0500-0999/759.py)

[📖 16. Intervals lesson](../learning/17-intervals.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 16. Intervals problems](../rmap-practice/16-intervals.md)

---

You're given `schedule`, a list of employees' working hours. Each employee has a list of **non-overlapping** `Interval`s, **sorted** by start time.

Return the list of **finite intervals** of time that are **free for all employees**, sorted. Free time before everyone starts or after everyone finishes is infinite, so it isn't included. Intervals of zero length (like `[5, 5]`) aren't included either.

```
schedule = [[[1,2],[5,6]], [[1,3]], [[4,10]]]
→ [[3,4]]

Employee 1:  [1,2]       [5,6]
Employee 2:  [1,──3]
Employee 3:              [4,──────────10]
Free:            [3,4]

schedule = [[[1,3],[6,7]], [[2,4]], [[2,5],[9,12]]]
→ [[5,6], [7,9]]
```

`Interval` objects have `.start` and `.end` attributes, so `schedule[0][0].start = 1`. The output is also a list of `Interval` objects.

**Constraints:** `1 <= schedule.length, schedule[i].length <= 50` · `0 <= start < end <= 10⁸`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| free for **all** employees | A time is free only if **nobody** is working, so it's the complement of everyone's busy time combined |
| **finite** intervals only | Ignore the time before the earliest start and after the latest end |
| each employee's list is sorted and non-overlapping | A hint that a k-way merge is possible, but not required |
| `Interval` objects | Use `.start` and `.end`, not `[0]` and `[1]` |

**The key reframe: who works with whom doesn't matter.** Free time for everyone = the gaps in the **union** of all busy intervals. So:

1. **Pool** every employee's intervals into one list.
2. **Sort** them by start.
3. Sweep through, tracking how far the busy time currently reaches (`busy_until`).
4. Whenever an interval **starts after** `busy_until`, there's a gap. That gap is free time.

This is [Merge Intervals](56-merge-intervals.md), except that instead of outputting the merged blocks, you output the **gaps between them**.

```
sorted:  [1,2] [1,3] [4,10] [5,6]
busy until: 2 → 3 →  gap (3,4)!  → 10 → 10
```

🤔 **Before you open the next section:** if an interval starts exactly at `busy_until`, say busy until 3 and the next one starts at 3, is there a gap?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Mark every time unit | A boolean array over the time range | O(T) | O(T) | ❌ T up to 10⁸ |
| **Flatten, sort, sweep** | Pool all intervals, sort by start, record gaps | **O(N log N)** | O(N) | ✅ Simplest |
| Heap k-way merge | Merge the k sorted lists with a heap | O(N log k) | O(k) | ✅ Faster when k is small |
| Line sweep on events | +1 at each start, −1 at each end; free where the count is 0 | O(N log N) | O(N) | ✅ Also works |

Here N is the total number of intervals and k the number of employees.

**The decision: flatten, [sort](../learning/05b-sorting.md), and sweep, exactly the [Merge Intervals](56-merge-intervals.md) pass**, recording gaps instead of merged blocks.

**The heap alternative.** Each employee's list is already sorted, so you could merge them like [Merge k Sorted Lists](23-merge-k-sorted-lists.md), always taking the earliest-starting interval from a [heap](../data-structures/heap.md). That's O(N log k) instead of O(N log N). With N ≤ 2500, it makes no practical difference, but it's a good follow-up answer.

**Strict `>` for a gap.** If the next interval starts **exactly** at `busy_until`, there's no free time between them, just a zero-length touch. Only a start **strictly after** `busy_until` makes a real gap.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
intervals = []
for employee in schedule:
    for iv in employee:
        intervals.append(iv)
```

**Pool everyone's busy time.** Who the interval belongs to doesn't matter for "free for all." A comprehension would do the same: `[iv for employee in schedule for iv in employee]`.
→ [nested-lists](../syntax/nested-lists.md) · [for-loop](../syntax/for-loop.md)

```python
intervals.sort(key=lambda iv: iv.start)
```

**Sort by start time.** The key function reads the attribute. `Interval` objects can't be compared directly.
→ [sorting-key](../syntax/sorting-key.md) · [lambda-functions](../syntax/lambda-functions.md)

```python
result = []
busy_until = intervals[0].end
```

**Start the sweep.** `busy_until` is the latest end time seen so far, the edge of the current merged busy block. Starting from the first interval means time before it, which is infinite, is never reported.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
for iv in intervals[1:]:
    if iv.start > busy_until:
        result.append(Interval(busy_until, iv.start))
    busy_until = max(busy_until, iv.end)
```

**Sweep.** For each interval, in start order:
- If it starts **after** the busy block ends, everything between is free. Record `[busy_until, iv.start]`.
- Either way, extend `busy_until` to cover this interval. Use `max`, because a short interval inside a longer one mustn't pull the edge back.

`intervals[1:]` skips the first interval, which was used to initialise `busy_until`.
→ [list-slicing](../syntax/list-slicing.md) · [min-max-key](../syntax/min-max-key.md) · [class-basics](../syntax/class-basics.md)

```python
return result
```

Gaps were recorded left to right, so the result is already sorted. Time after the last interval is infinite and is never recorded.

<details>
<summary>The whole thing together</summary>

```python
"""
# Definition for an Interval.
class Interval:
    def __init__(self, start: int = None, end: int = None):
        self.start = start
        self.end = end
"""

class Solution:
    def employeeFreeTime(self, schedule: '[[Interval]]') -> '[Interval]':
        intervals = []
        for employee in schedule:
            for iv in employee:
                intervals.append(iv)

        intervals.sort(key=lambda iv: iv.start)

        result = []
        busy_until = intervals[0].end
        for iv in intervals[1:]:
            if iv.start > busy_until:
                result.append(Interval(busy_until, iv.start))
            busy_until = max(busy_until, iv.end)

        return result
```

</details>

**Trace it.** Example 2. All intervals sorted by start: `[1,3] [2,4] [2,5] [6,7] [9,12]`:

| Interval | `start > busy_until`? | Gap recorded | `busy_until` after |
|---|---|---|---|
| [1,3] | (initial) | | 3 |
| [2,4] | 2 > 3? no | | 4 |
| [2,5] | 2 > 4? no | | 5 |
| [6,7] | 6 > 5? **yes** | **[5, 6]** | 7 |
| [9,12] | 9 > 7? **yes** | **[7, 9]** | 12 |

Result **`[[5,6], [7,9]]`** ✅.

**Why `max` matters.** In example 1, sorted: `[1,2] [1,3] [4,10] [5,6]`. After `[4,10]`, `busy_until = 10`. Then `[5,6]` doesn't start after 10, so there's no gap, and `max(10, 6)` keeps it at 10. Without `max`, it would drop to 6.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(N log N)</summary>

**O(N log N)**, where N is the total number of intervals.

- Flattening: O(N).
- Sorting: O(N log N), which dominates.
- Sweeping: O(N).

**The heap merge gives O(N log k)** by using the fact that each employee's list is already sorted. Push each employee's first interval, then repeatedly pop the earliest and push that employee's next interval.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(N)</summary>

**O(N)** for the flattened list (and the sort's working space). The output holds at most N − 1 gaps.

The heap version only keeps k entries in the heap, so O(k) extra besides the output.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Free for everyone means nobody's working, so I only care about the union of all busy intervals. Who they belong to doesn't matter. I flatten them into one list, sort by start, and sweep the way Merge Intervals does, tracking how far busy time reaches. When an interval starts strictly after that point, the gap between is free time, so I record it. I always extend the edge with max, so nested intervals don't pull it back. O(N log N) for the sort. A heap k-way merge would make it O(N log k)."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Use the fact that each list is sorted?" | A heap merge across employees: O(N log k). The same idea as [Merge k Sorted Lists](23-merge-k-sorted-lists.md). |
| "Free time for at least m employees?" | A line sweep with +1 at each start and −1 at each end. Report stretches where the busy count is at most `k − m`. |
| "Within working hours, like 9 to 5?" | Start `busy_until` at 9, and add a final gap up to 5 if the last block ends earlier. Clip everything to that window. |
| "Find a meeting slot of length d?" | Return the first gap with `end − start >= d`. |
| "Why strict `>`?" | Touching intervals (`[1,3]`, `[3,5]`) leave no free time between them. |

**Traps:**

- **Sorting `Interval` objects directly.** Python can't compare them. Sort with `key=lambda iv: iv.start`.
- **Overwriting `busy_until` with `iv.end`.** A nested interval would shrink the busy block and report false gaps.
- **`>=` for the gap test.** It reports zero-length gaps like `[3,3]`.
- **Including infinite time.** Don't add a gap before the first interval or after the last.
- **Treating employees separately.** You need the combined busy time, not per-employee gaps.

**This same move shows up in:** [Merge Intervals](56-merge-intervals.md) (the same sort-and-sweep, outputting the merged blocks) · [Insert Interval](57-insert-interval.md) (a sweep with a running edge) · [Interval List Intersections](986-interval-list-intersections.md) (combining two people's schedules) · [Meeting Rooms II](253-meeting-rooms-ii.md) (sweeping start and end events).

</details>

---
