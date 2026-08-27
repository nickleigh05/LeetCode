# A* Search

```python
import heapq

def a_star(start, goal, neighbors, h):     # h(n) = optimistic guess of n→goal cost
    g = {start: 0}                         # true cost from start so far
    heap = [(h(start), start)]             # ranked by f = g + h
    while heap:
        f, u = heapq.heappop(heap)
        if u == goal:
            return g[u]
        for v, w in neighbors(u):
            if g[u] + w < g.get(v, float('inf')):
                g[v] = g[u] + w
                heapq.heappush(heap, (g[v] + h(v), v))
    return -1
```

[Dijkstra](dijkstra.md) with a sense of direction: rank the frontier not by distance-so-far `g`, but by `g + h`, where the **heuristic** `h` estimates remaining distance to the goal. Dijkstra expands a circle; A* stretches that circle into an ellipse pointed at the target, skipping work in the wrong direction. Guaranteed optimal as long as `h` never *over*estimates (admissible) — for grids that's Manhattan distance `|dr| + |dc|`, for coordinates Euclidean distance, and `h = 0` degrades gracefully back into Dijkstra. Rarely *required* on LeetCode (plain [BFS](bfs.md)/Dijkstra passes), but it can turn a slow Shortest Path in Binary Matrix into a fast one, it's the standard pathfinding answer in game/robotics interviews, and it's a genuinely satisfying upgrade to understand.

**Complexity:** O(E log V) worst case like Dijkstra — the heuristic cuts the constant, not the bound.

**Related:** [dijkstra](dijkstra.md) · [bfs](bfs.md) · [Grids primer](../learning/10b-grids-primer.md) · [heapq-module (syntax)](../syntax/heapq-module.md)
