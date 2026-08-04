# 1584. Min Cost to Connect All Points

**Medium** · [LeetCode](https://leetcode.com/problems/min-cost-to-connect-all-points/)

[📖 12. Advanced Graphs lesson](../learning/13-advanced-graphs.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 12. Advanced Graphs problems](../rmap-practice/12-advanced-graphs.md)

---

Solution: not yet solved in this repo.

Connect all points with edges weighted by Manhattan distance, minimizing total edge cost. Why does greedily adding the cheapest edge that connects a *new* point (Prim's algorithm) guarantee a minimum spanning tree?

<details>
<summary>Hint</summary>

Prim's algorithm: grow a tree from any point, always adding the cheapest edge that connects an unvisited point, using a min-[heap](../data-structures/heap.md) of `(cost, point)` to always pick that edge efficiently.
</details>

<details>
<summary>Solution</summary>

```python
import heapq

class Solution:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:

        n = len(points)
        visited = set()
        min_heap = [(0, 0)]   # (cost, point index)
        total = 0

        while len(visited) < n:
            cost, i = heapq.heappop(min_heap)
            if i in visited:
                continue
            visited.add(i)
            total += cost

            for j in range(n):
                if j not in visited:
                    dist = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])
                    heapq.heappush(min_heap, (dist, j))

        return total
```

Building blocks: [heap](../data-structures/heap.md) · [set-basics](../syntax/set-basics.md) · [while-loop](../syntax/while-loop.md) · [comparison-operators](../syntax/comparison-operators.md) (`abs()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n² log n)** — n points, each pushing up to n edges onto the heap.
**Space: O(n²)** — the heap can hold up to n² edges in the worst case.
</details>

---
