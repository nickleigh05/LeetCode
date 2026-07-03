# Dijkstra's Algorithm

```python
import heapq

def dijkstra(graph, start):
    dist = {start: 0}
    pq = [(0, start)]           # (distance, node)
    while pq:
        d, node = heapq.heappop(pq)
        if d > dist.get(node, float("inf")):
            continue              # stale entry, skip
        for neighbor, weight in graph[node]:
            nd = d + weight
            if nd < dist.get(neighbor, float("inf")):
                dist[neighbor] = nd
                heapq.heappush(pq, (nd, neighbor))
    return dist
```

Finds shortest paths from a start node to every other node in a weighted graph with **non-negative** edge weights, by always expanding the closest not-yet-finalized node next — a [heap](../data-structures/heap.md) makes "closest unvisited node" retrievable in O(log n) instead of scanning. Generalizes [BFS](bfs.md) (which is really just Dijkstra where every edge weight is 1).

Doesn't work with negative edge weights — a node's shortest distance could be "finalized" too early, before a negative edge elsewhere lowers it further.

**Complexity:** O((V + E) log V) with a binary heap.

**Related:** [heap (data-structures)](../data-structures/heap.md) · [bfs](bfs.md) · [graph (data-structures)](../data-structures/graph.md)
