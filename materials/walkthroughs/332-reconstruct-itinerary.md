# 332. Reconstruct Itinerary

**Hard** · [LeetCode](https://leetcode.com/problems/reconstruct-itinerary/)

[📖 12. Advanced Graphs lesson](../learning/13-advanced-graphs.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 12. Advanced Graphs problems](../rmap-practice/12-advanced-graphs.md)

---

Solution: not yet solved in this repo.

Given airline tickets, reconstruct the itinerary that uses all tickets in order, starting from "JFK", choosing the lexicographically smallest route when there's a choice. Why does this become an Eulerian-path problem, and why must you add nodes to the result *after* exhausting their edges (post-order)?

<details>
<summary>Hint</summary>

Build an adjacency list sorted so the smallest destinations are tried first, then run [DFS](../algorithms/dfs.md), consuming (removing) each edge as you use it. Append to the result in post-order (after recursion returns) — this "Hierholzer's algorithm" trick handles dead ends correctly by placing them last.
</details>

<details>
<summary>Solution</summary>

```python
from collections import defaultdict

class Solution:
    def findItinerary(self, tickets: List[List[str]]) -> List[str]:

        graph = defaultdict(list)
        for src, dst in sorted(tickets, reverse=True):   # reverse-sorted so .pop() gives smallest
            graph[src].append(dst)

        route = []

        def dfs(airport):
            while graph[airport]:
                dfs(graph[airport].pop())
            route.append(airport)

        dfs("JFK")
        return route[::-1]
```

Building blocks: [defaultdict](../syntax/defaultdict.md) · [sorting-key](../syntax/sorting-key.md) (`reverse=True`) · [recursion-basics](../syntax/recursion-basics.md) · [list-slicing](../syntax/list-slicing.md) (`[::-1]`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(E log E)** — dominated by sorting the tickets; the DFS itself is O(E).
**Space: O(E)** — the adjacency list holds every ticket.
</details>

---
