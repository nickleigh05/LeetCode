# Floyd-Warshall

```python
def floyd_warshall(n, edges):             # ALL-pairs shortest paths
    INF = float('inf')
    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, w in edges:
        dist[u][v] = min(dist[u][v], w)
    for k in range(n):                    # k = intermediate node — OUTERMOST!
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist
```

Shortest paths between **every pair** of nodes in three lines of loops. It's [DP](dynamic-programming.md) in disguise: after iteration k, `dist[i][j]` is the shortest path using only nodes 0..k as stopovers — each round asks "does routing through k help?" The k-loop must be outermost (it's the DP stage, not a coordinate). Handles negative edges; a negative diagonal (`dist[i][i] < 0`) afterwards reveals a negative cycle. With V ≤ ~400 this is *the* lazy correct answer for multi-query distance problems (Find the City, LC 1334) — simpler than V runs of [Dijkstra](dijkstra.md) and impossible to get wrong. Same three loops with `or`/`and` instead of `min`/`+` compute pure reachability (transitive closure).

**Complexity:** O(V³) time · O(V²) space — fine to ~400 nodes.

**Related:** [dijkstra](dijkstra.md) · [bellman-ford](bellman-ford.md) · [dynamic-programming](dynamic-programming.md) · [Advanced Graphs lesson](../learning/13-advanced-graphs.md)
