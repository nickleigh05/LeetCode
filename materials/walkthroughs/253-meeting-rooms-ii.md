# 253. Meeting Rooms II

**Medium** · [LeetCode](https://leetcode.com/problems/meeting-rooms-ii/)

[📖 16. Intervals lesson](../learning/17-intervals.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 16. Intervals problems](../rmap-practice/16-intervals.md)

---

Solution: not yet solved in this repo.

Find the minimum number of meeting rooms needed. Why does treating starts and ends as separate sorted "events" let you track the number of rooms in use as a running count, rather than simulating actual room assignments?

<details>
<summary>Hint</summary>

Sort all start times and all end times separately (see [Intervals](../learning/17-intervals.md)). Walk both lists with two pointers: whenever a start occurs before the earliest pending end, a new room is needed; otherwise a room frees up first.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:

        starts = sorted(interval[0] for interval in intervals)
        ends = sorted(interval[1] for interval in intervals)

        start_ptr = 0
        end_ptr = 0
        rooms = 0
        max_rooms = 0

        while start_ptr < len(starts):
            if starts[start_ptr] < ends[end_ptr]:
                rooms += 1
                start_ptr += 1
                max_rooms = max(max_rooms, rooms)
            else:
                rooms -= 1
                end_ptr += 1

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
