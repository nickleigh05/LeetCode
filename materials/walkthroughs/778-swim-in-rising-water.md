# 778. Swim in Rising Water

**Hard** · [LeetCode](https://leetcode.com/problems/swim-in-rising-water/)

[📖 12. Advanced Graphs lesson](../learning/13-advanced-graphs.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 12. Advanced Graphs problems](../rmap-practice/12-advanced-graphs.md)

---

Solution: not yet solved in this repo.

Water rises over time; find the minimum time to swim from top-left to bottom-right (you can only move to cells whose elevation is `<=` current time). Why does always expanding the *lowest-elevation* reachable cell next (a min-heap) find the minimum time needed?

<details>
<summary>Hint</summary>

This is Dijkstra-flavored: use a min-[heap](../data-structures/heap.md) keyed by "max elevation encountered so far on this path." Always expand the cell that keeps that max the smallest; the answer is that max when you reach the bottom-right cell.
</details>

<details>
<summary>Solution</summary>

```python
import heapq

class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:

        n = len(grid)
        visited = set()
        min_heap = [(grid[0][0], 0, 0)]   # (max elevation on path so far, row, col)

        while min_heap:
            time, row, col = heapq.heappop(min_heap)
            if (row, col) in visited:
                continue
            visited.add((row, col))

            if row == n - 1 and col == n - 1:
                return time

            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                r = row + dr
                c = col + dc
                if 0 <= r < n and 0 <= c < n and (r, c) not in visited:
                    heapq.heappush(min_heap, (max(time, grid[r][c]), r, c))
```

Building blocks: [heap](../data-structures/heap.md) · [set-basics](../syntax/set-basics.md) · [while-loop](../syntax/while-loop.md) · [comparison-operators](../syntax/comparison-operators.md) (`max()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n² log n)** — n² cells, each heap operation O(log n²) = O(log n).
**Space: O(n²)** — the visited set and heap.
</details>

---
