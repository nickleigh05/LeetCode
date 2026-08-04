# 435. Non-overlapping Intervals

**Medium** · [LeetCode](https://leetcode.com/problems/non-overlapping-intervals/)

[📖 16. Intervals lesson](../learning/17-intervals.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 16. Intervals problems](../rmap-practice/16-intervals.md)

---

Solution: not yet solved in this repo.

Find the minimum number of intervals to remove so the rest don't overlap. Why is sorting by *end* time (not start) the key that makes a greedy "keep the earliest-ending interval" strategy correct?

<details>
<summary>Hint</summary>

Sort by end time (see [Intervals](../learning/17-intervals.md)). Greedily keep an interval if it starts at or after the last kept interval's end; otherwise it overlaps and must be removed — ending earliest always leaves the most room for future intervals.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:

        intervals.sort(key=lambda interval: interval[1])
        removed = 0
        prev_end = float("-inf")

        for start, end in intervals:
            if start >= prev_end:
                prev_end = end
            else:
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
