# 57. Insert Interval

**Medium** · [LeetCode](https://leetcode.com/problems/insert-interval/)

[📖 16. Intervals lesson](../learning/17-intervals.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 16. Intervals problems](../rmap-practice/16-intervals.md)

---

Solution: not yet solved in this repo.

Insert a new interval into a sorted, non-overlapping list of intervals, merging as needed. Why does the input already being sorted let you handle this in three clean phases — before, overlapping, after — in one linear pass?

<details>
<summary>Hint</summary>

Walk the intervals once (see [Intervals](../learning/17-intervals.md)): copy every interval that ends before the new one starts, merge every interval that overlaps the new one (expanding its bounds), then copy the rest.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:

        result = []
        i = 0
        n = len(intervals)

        while i < n and intervals[i][1] < newInterval[0]:
            result.append(intervals[i])
            i += 1

        while i < n and intervals[i][0] <= newInterval[1]:
            newInterval = [
                min(newInterval[0], intervals[i][0]),
                max(newInterval[1], intervals[i][1]),
            ]
            i += 1
        result.append(newInterval)

        while i < n:
            result.append(intervals[i])
            i += 1

        return result
```

Building blocks: [while-loop](../syntax/while-loop.md) · [list-methods](../syntax/list-methods.md) (`.append()`) · [comparison-operators](../syntax/comparison-operators.md) (`min()`, `max()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — a single pass over the intervals.
**Space: O(n)** — the result list.
</details>

---
