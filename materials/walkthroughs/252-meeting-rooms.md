# 252. Meeting Rooms

**Easy** · [LeetCode](https://leetcode.com/problems/meeting-rooms/)

[📖 16. Intervals lesson](../learning/17-intervals.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 16. Intervals problems](../rmap-practice/16-intervals.md)

---

Solution: not yet solved in this repo.

Determine if a person can attend all meetings (no overlaps). Why does sorting by start time turn "any overlap anywhere" into a simple adjacent-pair check?

<details>
<summary>Hint</summary>

Sort by start time (see [Intervals](../learning/17-intervals.md)). After sorting, any overlap must occur between *adjacent* meetings, so just check that each meeting starts at or after the previous one ends.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def canAttendMeetings(self, intervals: List[List[int]]) -> bool:

        intervals.sort(key=lambda interval: interval[0])

        for i in range(1, len(intervals)):
            if intervals[i][0] < intervals[i - 1][1]:
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
