# Bellman-Ford

```python
def bellman_ford(n, edges, src):          # edges: [(u, v, w), ...]
    dist = [float('inf')] * n
    dist[src] = 0
    for _ in range(n - 1):                # n-1 rounds of relaxing every edge
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    for u, v, w in edges:                 # round n still improves something?
        if dist[u] + w < dist[v]:
            return None                   # → negative cycle reachable from src
    return dist
```

Single-source shortest paths that — unlike [Dijkstra](dijkstra.md) — survives **negative edge weights**, and detects negative *cycles* as a bonus. No priority queue, no greedy commitment: just relax every edge, n−1 times. Why that works: a shortest path uses at most n−1 edges, and round k guarantees all shortest paths of ≤ k edges are settled — so if a full extra round still finds an improvement, some cycle keeps paying, i.e. a negative cycle. The "at most k edges" view is the direct solution to Cheapest Flights Within K Stops (LC 787): run exactly k+1 rounds on a *copy* of dist per round. Slower than Dijkstra (O(V·E) vs O(E log V)) — only reach for it when negatives or edge-count limits are in play.

**Complexity:** O(V · E) time · O(V) space.

**Related:** [dijkstra](dijkstra.md) · [floyd-warshall](floyd-warshall.md) · [Advanced Graphs lesson](../learning/13-advanced-graphs.md)
