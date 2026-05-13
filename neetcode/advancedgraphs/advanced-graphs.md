# Advanced Graphs

## How to use this README

Problems are split into three tiers: Blind 75 is the core set every interviewer expects you to know cold. NeetCode 150 introduces the weighted graph algorithms that dominate advanced graph interviews — Dijkstra, Bellman-Ford, Prim, and Hierholzer. NeetCode 250 adds harder variants that combine multiple algorithms or require recognizing non-obvious graph reductions. Work through tiers in order — the Core Patterns and Syntax Reference sections below map directly to the problems in each table. When you see an advanced graph problem, first ask: is there a weight or cost on edges? Are negative weights possible? Do you need a minimum spanning tree or shortest path? Those three questions determine the algorithm.

---

## Problems

### Blind 75
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved |
|-----------|------------|--------------|---------------|--------|
| 269 | Hard | Alien Dictionary | [Link](https://leetcode.com/problems/alien-dictionary/) | ☐ |

### NeetCode 150
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved |
|-----------|------------|--------------|---------------|--------|
| 332 | Hard | Reconstruct Itinerary | [Link](https://leetcode.com/problems/reconstruct-itinerary/) | ☐ |
| 1584 | Medium | Min Cost to Connect All Points | [Link](https://leetcode.com/problems/min-cost-to-connect-all-points/) | ☐ |
| 743 | Medium | Network Delay Time | [Link](https://leetcode.com/problems/network-delay-time/) | ☐ |
| 778 | Hard | Swim in Rising Water | [Link](https://leetcode.com/problems/swim-in-rising-water/) | ☐ |
| 787 | Medium | Cheapest Flights Within K Stops | [Link](https://leetcode.com/problems/cheapest-flights-within-k-stops/) | ☐ |

### NeetCode 250
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved | Pattern |
|-----------|------------|--------------|---------------|--------|---------|
| 1631 | Medium | Path with Minimum Effort | [Link](https://leetcode.com/problems/path-with-minimum-effort/) | ☐ | Dijkstra / binary search |
| 1489 | Hard | Find Critical and Pseudo-Critical Edges in MST | [Link](https://leetcode.com/problems/find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree/) | ☐ | MST + edge analysis |
| 2392 | Hard | Build a Matrix With Conditions | [Link](https://leetcode.com/problems/build-a-matrix-with-conditions/) | ☐ | Topological sort |
| 2709 | Hard | Greatest Common Divisor Traversal | [Link](https://leetcode.com/problems/greatest-common-divisor-traversal/) | ☐ | Union-Find + math |

---

## Complexity Reference

| Algorithm | Time | Space | Notes |
|-----------|------|-------|-------|
| Dijkstra (binary heap) | O((V+E) log V) | O(V) | Non-negative weights only |
| Dijkstra (Fibonacci heap) | O(E + V log V) | O(V) | Theoretical; not used in interviews |
| Bellman-Ford | O(V*E) | O(V) | Handles negative weights; detects negative cycles |
| Bellman-Ford (k stops) | O(k*E) | O(V) | Run k+1 relaxation passes for k hops |
| Prim's MST (binary heap) | O(E log V) | O(V) | Better for dense graphs |
| Kruskal's MST | O(E log E) | O(V) | Dominated by edge sort; better for sparse graphs |
| Hierholzer (Eulerian path) | O(E) | O(E) | Linear in number of edges |
| Topological sort | O(V+E) | O(V) | For DAGs; detects cycles |
| Floyd-Warshall (all-pairs) | O(V³) | O(V²) | All pairs shortest paths; handles negative weights |

---

## Data Structures

### Weighted Adjacency List

A dict mapping each node to a list of `(neighbor, weight)` tuples. Required for Dijkstra and Bellman-Ford because edge weights determine which path to take. Space is O(V+E).

```
Graph with weights:
  0 --3-- 1
  |       |
  4       2
  |       |
  2 --1-- 3

Weighted adjacency list:
{
  0: [(1, 3), (2, 4)],
  1: [(0, 3), (3, 2)],
  2: [(0, 4), (3, 1)],
  3: [(1, 2), (2, 1)]
}

Shortest path 0→3: 0→2→3, cost = 4+1 = 5
                   (not 0→1→3, cost = 3+2 = 5, same here)
```

**When it matters:** Any problem that mentions costs, times, distances, or prices on edges. Without weights, plain BFS suffices; with weights, you need Dijkstra or Bellman-Ford.

### Min-Heap for Dijkstra

Dijkstra's algorithm always processes the currently-cheapest unfinished node next. A min-heap of `(distance, node)` tuples gives O(log V) extract-min and O(log V) decrease-key (by pushing a new entry and skipping stale ones).

```
State of heap during Dijkstra from node 0:
(distances: 0→0, 1→inf, 2→inf, 3→inf)

Push (0, 0):  heap = [(0, 0)]
Pop (0, 0):   relax neighbors → push (3,1) and (4,2)
              heap = [(3, 1), (4, 2)]
Pop (3, 1):   relax neighbors → push (5, 3)
              heap = [(4, 2), (5, 3)]
Pop (4, 2):   relax neighbors → dist[3]=5 already, no improvement
Pop (5, 3):   target reached, dist[3] = 5
```

**When it matters:** The heap is the engine of Dijkstra. The "skip stale entries" trick (`if d > dist[u]: continue`) avoids maintaining a complex decrease-key operation — just push a new tuple and ignore old ones when popped.

### Union-Find for Kruskal's MST

Kruskal's builds the MST by greedily adding the cheapest edge that doesn't form a cycle. Union-Find makes the cycle check O(α(n)) per edge, which is essentially constant. The MST is complete when V-1 edges have been added.

```
Edges sorted by weight: (1,2,1), (0,1,3), (1,3,2), (0,2,4)
n=4 nodes, need 3 edges for MST

Add (1,2,1): find(1)=1, find(2)=2 — different sets → add edge, union(1,2)
Add (1,3,2): find(1)=root, find(3)=3 — different → add edge, union(1,3)
Add (0,1,3): find(0)=0, find(1)=root — different → add edge, union(0,1)
             3 edges added → MST complete, total cost = 1+2+3 = 6
```

**When it matters:** Kruskal's is often simpler to code than Prim's when you're given an explicit edge list. If the graph is dense or given as a coordinate set (Min Cost to Connect All Points #1584), Prim's may be more natural.

---

## Core Patterns

### Dijkstra (Shortest Path, Non-Negative Weights)

**When to use:** Single-source shortest path where all edge weights are non-negative. The constraint is critical — Dijkstra is incorrect with negative weights.
**Complexity:** O((V+E) log V) time, O(V) space
**Problems:** Network Delay Time (#743), Swim in Rising Water (#778), Path with Minimum Effort (#1631), Cheapest Flights Within K Stops (#787) — modified version
**Common mistake:** Not skipping stale heap entries. When you pop `(d, u)` and `d > dist[u]`, a cheaper path was already found — skip this entry. Without this check, you do redundant work.

```python
import heapq

def dijkstra(graph, src, n):
    dist = {i: float('inf') for i in range(n)}
    dist[src] = 0
    h = [(0, src)]                    # (distance, node)
    while h:
        d, u = heapq.heappop(h)
        if d > dist[u]:
            continue                  # stale entry — skip
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(h, (dist[v], v))
    return dist
```

### Bellman-Ford (Negative Weights / Bounded Hops)

**When to use:** Shortest path with possible negative edge weights, or when you need the shortest path using at most k edges (Cheapest Flights Within K Stops).
**Complexity:** O(V*E) time, O(V) space — slower than Dijkstra, use only when necessary
**Problems:** Cheapest Flights Within K Stops (#787)
**Common mistake:** Updating `dist` in-place during a pass — this can use updates from the current pass rather than the previous pass, violating the "at most k hops" invariant. Use a copy of `dist` for the next iteration.

```python
def bellman_ford(n, edges, src):
    dist = [float('inf')] * n
    dist[src] = 0
    for _ in range(n - 1):           # relax all edges n-1 times
        temp = dist[:]               # copy to avoid using same-pass updates
        for u, v, w in edges:
            if dist[u] + w < temp[v]:
                temp[v] = dist[u] + w
        dist = temp
    return dist

# For "at most k stops" variant: run exactly k+1 passes
```

### Prim's MST

**When to use:** Find the minimum spanning tree of an undirected weighted graph. Prim's grows the MST one node at a time, always adding the cheapest edge connecting the MST to a new node.
**Complexity:** O(E log V) with a min-heap
**Problems:** Min Cost to Connect All Points (#1584)
**Common mistake:** Adding a node to the MST multiple times — mark nodes as "in MST" when they are popped from the heap, not when they are pushed.

```python
import heapq
from collections import defaultdict

def prims_mst(n, edges):
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((w, v))
        graph[v].append((w, u))
    in_mst = set()
    h = [(0, 0)]                      # (cost, node), start from node 0
    total_cost = 0
    while h and len(in_mst) < n:
        cost, u = heapq.heappop(h)
        if u in in_mst:
            continue                  # already in MST
        in_mst.add(u)
        total_cost += cost
        for w, v in graph[u]:
            if v not in in_mst:
                heapq.heappush(h, (w, v))
    return total_cost if len(in_mst) == n else -1
```

### Kruskal's MST

**When to use:** Find the MST when you have an explicit sorted (or sortable) edge list. Simpler than Prim's when edges are given directly.
**Complexity:** O(E log E) dominated by sorting
**Problems:** Min Cost to Connect All Points (#1584), Find Critical and Pseudo-Critical Edges (#1489)
**Common mistake:** Forgetting to stop early once V-1 edges have been added. You can also detect a disconnected graph: if fewer than V-1 edges were added, the graph has no spanning tree.

```python
def kruskal_mst(n, edges):
    edges.sort(key=lambda e: e[2])    # sort by weight
    parent = list(range(n))
    rank = [0] * n

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        px, py = find(x), find(y)
        if px == py: return False
        if rank[px] < rank[py]: px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]: rank[px] += 1
        return True

    total, count = 0, 0
    for u, v, w in edges:
        if union(u, v):
            total += w
            count += 1
            if count == n - 1: break  # MST complete
    return total if count == n - 1 else -1
```

### Eulerian Path (Hierholzer's Algorithm)

**When to use:** Find a path (or circuit) that visits every EDGE exactly once. Classic "Chinese postman" style — traverse all edges.
**Complexity:** O(E) time, O(E) space
**Problems:** Reconstruct Itinerary (#332)
**Common mistake:** Confusing Eulerian path (every edge once) with Hamiltonian path (every vertex once) — they're different problems with different algorithms. Hierholzer works by greedily following edges and backtracking when stuck, building the path in reverse.

```python
from collections import defaultdict

def find_itinerary(tickets):
    graph = defaultdict(list)
    for src, dst in sorted(tickets, reverse=True):  # sort reverse so we pop smallest first
        graph[src].append(dst)
    route = []
    def dfs(airport):
        while graph[airport]:
            dfs(graph[airport].pop())
        route.append(airport)        # append after all outgoing edges are exhausted
    dfs("JFK")
    return route[::-1]              # reverse because we built it in postorder
```

---

## Syntax Reference

### Dijkstra template

```python
import heapq

dist = [float('inf')] * n
dist[src] = 0
h = [(0, src)]
while h:
    d, u = heapq.heappop(h)
    if d > dist[u]: continue        # skip stale entries
    for v, w in graph[u]:
        if dist[u] + w < dist[v]:
            dist[v] = dist[u] + w
            heapq.heappush(h, (dist[v], v))
```

### Bellman-Ford template

```python
dist = [float('inf')] * n
dist[src] = 0
for _ in range(n - 1):
    for u, v, w in edges:
        if dist[u] + w < dist[v]:
            dist[v] = dist[u] + w
# check for negative cycle: if any dist[v] still decreases after n-1 passes, cycle exists
```

### Kruskal's sort by edge weight

```python
edges.sort(key=lambda e: e[2])      # weight is the third element
```

### Build weighted adjacency list

```python
from collections import defaultdict
graph = defaultdict(list)
for u, v, w in edges:
    graph[u].append((v, w))
    graph[v].append((u, w))         # omit for directed graph
```

### Modified Dijkstra for "at most k hops" (Cheapest Flights)

```python
# heap stores (cost, node, hops_remaining)
import heapq
h = [(0, src, k)]
dist = {}
while h:
    cost, u, hops = heapq.heappop(h)
    if u == dst: return cost
    if hops == 0: continue
    if (u, hops) in dist: continue
    dist[(u, hops)] = cost
    for v, w in graph[u]:
        heapq.heappush(h, (cost + w, v, hops - 1))
return -1
```

### Prim's MST starting from node 0

```python
import heapq
in_mst = set()
h = [(0, 0)]    # (cost, node)
total = 0
while h:
    cost, u = heapq.heappop(h)
    if u in in_mst: continue
    in_mst.add(u)
    total += cost
    for w, v in graph[u]:
        if v not in in_mst:
            heapq.heappush(h, (w, v))
```
