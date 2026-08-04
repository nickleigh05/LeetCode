# 56. Merge Intervals

**Medium** · [LeetCode](https://leetcode.com/problems/merge-intervals/) · [Solution file (no hints)](../../problems/0001-0499/56.py)

[📖 16. Intervals lesson](../learning/17-intervals.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 16. Intervals problems](../rmap-practice/16-intervals.md)

---

Merge all overlapping intervals. Why does sorting by start time guarantee that any interval overlapping the current merged one must come *immediately* next?

<details>
<summary>Hint</summary>

Sort intervals by start (see [Intervals](../learning/17-intervals.md)). Walk through them, and if the current interval's start is `<=` the last merged interval's end, extend that merged interval's end; otherwise start a new merged interval.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:

        intervals.sort(key=lambda interval: interval[0])
        merged = []

        for interval in intervals:
            if len(merged) == 0:
                merged.append(interval)
            else:
                last_interval = merged[-1]
                if interval[0] <= last_interval[1]:
                    last_interval[1] = max(last_interval[1], interval[1])
                else:
                    merged.append(interval)
        return merged
```

Building blocks: [sorting-key](../syntax/sorting-key.md) · [lambda-functions](../syntax/lambda-functions.md) · [for-loop](../syntax/for-loop.md) · [comparison-operators](../syntax/comparison-operators.md) (`max()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n log n)** — dominated by the sort; the merge pass is O(n).
**Space: O(n)** — the result list (plus O(log n)/O(n) for the sort itself).
</details>

---
