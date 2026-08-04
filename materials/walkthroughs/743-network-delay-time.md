# 743. Network Delay Time

**Medium** · [LeetCode](https://leetcode.com/problems/network-delay-time/)

[📖 12. Advanced Graphs lesson](../learning/13-advanced-graphs.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 12. Advanced Graphs problems](../rmap-practice/12-advanced-graphs.md)

---

Solution: not yet solved in this repo.

Given a weighted directed graph, find the time for a signal from node `k` to reach every node (or -1 if impossible). Why is this exactly what Dijkstra's algorithm computes?

<details>
<summary>Hint</summary>

Run [Dijkstra's algorithm](../algorithms/dijkstra.md) from `k`: always expand the closest not-yet-finalized node using a min-[heap](../data-structures/heap.md) of `(time, node)`, relaxing neighbor distances as you go.
</details>

<details>
<summary>Solution</summary>

```python
import heapq
from collections import defaultdict

class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:

        graph = defaultdict(list)
        for u, v, w in times:
            graph[u].append((v, w))

        dist = {}
        min_heap = [(0, k)]   # (time so far, node)

        while min_heap:
            time, node = heapq.heappop(min_heap)
            if node in dist:
                continue
            dist[node] = time

            for neighbor, weight in graph[node]:
                if neighbor not in dist:
                    heapq.heappush(min_heap, (time + weight, neighbor))

        if len(dist) != n:
            return -1
        return max(dist.values())
```

Building blocks: [defaultdict](../syntax/defaultdict.md) · [heap](../data-structures/heap.md) · [while-loop](../syntax/while-loop.md) · [dict-methods](../syntax/dict-methods.md) (`.values()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(E log V)** — each edge relaxation involves a heap push/pop.
**Space: O(V + E)** — the adjacency list, distance map, and heap.
</details>

---
