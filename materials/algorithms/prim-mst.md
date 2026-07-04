# Prim's Algorithm (Minimum Spanning Tree)

```python
import heapq

def prim(n, adj):                      # adj[u] = [(weight, v), ...]
    total, seen = 0, set()
    heap = [(0, 0)]                    # (edge weight into node, node) — start anywhere
    while len(seen) < n:
        w, u = heapq.heappop(heap)
        if u in seen:
            continue                   # stale entry — u already connected
        seen.add(u)
        total += w
        for wv, v in adj[u]:
            if v not in seen:
                heapq.heappush(heap, (wv, v))
    return total
```

Grow the **minimum spanning tree** — the cheapest set of edges connecting all nodes — one node at a time: from everything connected so far, always absorb the outside node reachable by the cheapest edge. Structurally it *is* [Dijkstra](dijkstra.md) with one edit: the heap ranks by **single edge weight** rather than total path distance (a reliable interview probe: "what's the difference?"). Correctness rests on the *cut property* — the cheapest edge crossing any frontier is always safe to take. The canonical LeetCode appearance is Min Cost to Connect All Points (LC 1584). Prefer Prim on dense/implicit graphs; [Kruskal](kruskal-mst.md) when you're handed an edge list.

**Complexity:** O(E log E) with a heap · O(V + E) space.

**Related:** [kruskal-mst](kruskal-mst.md) · [dijkstra](dijkstra.md) · [heapq-module (syntax)](../syntax/heapq-module.md) · [Advanced Graphs lesson](../learning/13-advanced-graphs.md)
