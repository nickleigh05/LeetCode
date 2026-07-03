# 13. Advanced Graphs (Dijkstra & Topological Sort)
*Weighted shortest paths and dependency ordering.*

[← Prev](12-union-find.md) · [🗺 Roadmap](../../roadmap.md) · [Next →](14-dp-1d.md)

---

> **Builds on:** plain BFS/DFS from [Lesson 11 — Graphs](11-graphs.md). Here we add edge weights and ordering constraints.

When edges carry weights, BFS isn't enough — **Dijkstra** finds shortest paths with a priority queue. When tasks have prerequisites, **topological sort** produces a valid order (and detects impossible cycles). These are the heavyweight graph tools interviewers reach for to separate candidates.

## The Pattern

### Topological Sort

```
  Prerequisites: 0→2, 1→2, 1→3, 2→4, 3→4
  (read: must complete 0 before 2, etc.)

  Build in-degree map:
  in_degree = {0:0, 1:0, 2:2, 3:1, 4:2}

  Queue all nodes with in_degree=0: [0,1]

  Process 0: decrement neighbor 2 → in_degree[2]=1
  Process 1: decrement 2 → in_degree[2]=0 ✓ add to queue
             decrement 3 → in_degree[3]=0 ✓ add to queue
  Queue: [2,3]
  Process 2: decrement 4 → in_degree[4]=1
  Process 3: decrement 4 → in_degree[4]=0 ✓ add to queue
  Queue: [4]
  Process 4: done.
  Order: [0,1,2,3,4]

  If any node was never processed → CYCLE (impossible ordering)
```

**What it is:** Produces a valid ordering of tasks with dependencies. Uses Kahn's algorithm (BFS on in-degrees) or DFS with a post-order stack. Also detects cycles in directed graphs.

**Use this when:**
- [ ] Course prerequisites / task scheduling
- [ ] Build order with dependencies
- [ ] "Is it possible to complete all tasks?" (cycle detection in directed graph)
- [ ] Ordering of compilation units
- [ ] Alien dictionary (derive character order)

**Python:**
```python
from collections import defaultdict, deque

# Kahn's BFS — detect cycle + return order
def topo_sort(num_nodes, prerequisites):
    graph = defaultdict(list)
    in_degree = [0] * num_nodes

    for a, b in prerequisites:  # b must come before a
        graph[b].append(a)
        in_degree[a] += 1

    queue = deque(i for i in range(num_nodes) if in_degree[i] == 0)
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # If len(order) < num_nodes → cycle exists → no valid ordering
    return order if len(order) == num_nodes else []

# Course Schedule (can we finish all courses?)
def can_finish(num_courses, prerequisites):
    return len(topo_sort(num_courses, prerequisites)) == num_courses

# Course Schedule II (return one valid ordering)
def find_order(num_courses, prerequisites):
    return topo_sort(num_courses, prerequisites)
```

**Complexity:** O(V + E) time and space.

**Blind 75 examples:** Course Schedule · Course Schedule II · Alien Dictionary

## Algorithm Deep-Dive

### Dijkstras Algorithm

```
  Weighted graph (all non-negative weights):
       A
     2/ \5
     B   C
    1\   /3
       D

  Start at A. Min-heap: [(cost, node)]
  Init:  heap=[(0,A)],  dist={A:0, B:∞, C:∞, D:∞}

  Pop (0,A):  update neighbors:
    B: 0+2=2 < ∞ → dist[B]=2, push (2,B)
    C: 0+5=5 < ∞ → dist[C]=5, push (5,C)
  heap=[(2,B),(5,C)]

  Pop (2,B):  update neighbors:
    D: 2+1=3 < ∞ → dist[D]=3, push (3,D)
  heap=[(3,D),(5,C)]

  Pop (3,D):  update neighbors:
    C: 3+3=6 > 5 → no update
  heap=[(5,C)]

  Pop (5,C):  done
  Final: dist={A:0, B:2, C:5, D:3}
```

**What it does:** Finds the shortest path from a source to all other nodes in a weighted graph with non-negative edge weights. Uses a min-heap to always process the cheapest unvisited node next.

**Recognition signals:**
- Shortest path in a weighted graph
- Minimum cost to reach a destination
- Graph has non-negative edge weights
- "Network delay time", "cheapest flights", "path with minimum effort"

**Limitation:** Does NOT work with negative edge weights (use Bellman-Ford instead).

**Python:**
```python
import heapq
from collections import defaultdict

def dijkstra(graph, start):
    # graph[u] = [(weight, v), ...]
    dist = defaultdict(lambda: float('inf'))
    dist[start] = 0
    heap = [(0, start)]   # (cost, node)

    while heap:
        cost, node = heapq.heappop(heap)
        if cost > dist[node]:
            continue       # stale entry, skip
        for weight, neighbor in graph[node]:
            new_cost = cost + weight
            if new_cost < dist[neighbor]:
                dist[neighbor] = new_cost
                heapq.heappush(heap, (new_cost, neighbor))

    return dist

# Grid variant: min cost path
def dijkstra_grid(grid):
    rows, cols = len(grid), len(grid[0])
    dist = [[float('inf')] * cols for _ in range(rows)]
    dist[0][0] = grid[0][0]
    heap = [(grid[0][0], 0, 0)]

    while heap:
        cost, r, c = heapq.heappop(heap)
        if cost > dist[r][c]: continue
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < rows and 0 <= nc < cols:
                nc_cost = cost + grid[nr][nc]
                if nc_cost < dist[nr][nc]:
                    dist[nr][nc] = nc_cost
                    heapq.heappush(heap, (nc_cost, nr, nc))
    return dist[rows-1][cols-1]
```

**Complexity:**

| | Time | Space |
|-|------|-------|
| With binary heap | O((V + E) log V) | O(V) |

**Data structures it uses:**
Heap and Priority Queue · Graph · Hash Map and Hash Set

### Topological Sort

```
  DAG (Directed Acyclic Graph):
  Courses: 0→2, 1→2, 1→3, 2→4, 3→4

  0 ──→ 2 ──→ 4
  1 ──→ 3 ──↗

  In-degrees: {0:0, 1:0, 2:2, 3:1, 4:2}

  Kahn's BFS method:
  Queue starts with all in-degree=0: [0, 1]
  Pop 0: process, decrement neighbors → 2's in-degree: 2→1
  Pop 1: process, decrement 2→0, 3→0 → queue: [2, 3]
  Pop 2: process, decrement 4→1
  Pop 3: process, decrement 4→0 → queue: [4]
  Pop 4: process

  Order: [0, 1, 2, 3, 4]  ← one valid topological ordering
  If queue empties before all nodes processed → CYCLE exists!
```

**What it does:** Produces a linear ordering of vertices in a Directed Acyclic Graph (DAG) such that for every directed edge u→v, u appears before v. Two methods: Kahn's (BFS) and DFS-based.

**Recognition signals:**
- Task scheduling with prerequisites
- Course schedule (must take A before B)
- Build order (dependencies)
- Detecting cycles in directed graphs
- Any "ordering" problem with directed constraints

**Python:**
```python
from collections import defaultdict, deque

# Kahn's Algorithm (BFS) — detects cycle if output length < n
def topo_sort_bfs(n, prerequisites):
    graph = defaultdict(list)
    in_degree = [0] * n

    for a, b in prerequisites:  # b → a (must take b before a)
        graph[b].append(a)
        in_degree[a] += 1

    queue = deque([i for i in range(n) if in_degree[i] == 0])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return order if len(order) == n else []   # [] if cycle

# DFS-based Topological Sort
def topo_sort_dfs(n, graph):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n
    result = []
    has_cycle = [False]

    def dfs(node):
        if has_cycle[0]: return
        color[node] = GRAY
        for neighbor in graph[node]:
            if color[neighbor] == GRAY:
                has_cycle[0] = True; return
            if color[neighbor] == WHITE:
                dfs(neighbor)
        color[node] = BLACK
        result.append(node)   # add to result AFTER processing all neighbors

    for i in range(n):
        if color[i] == WHITE:
            dfs(i)

    return [] if has_cycle[0] else result[::-1]
```

**Complexity:**

| | Time | Space |
|-|------|-------|
| Kahn's BFS | O(V + E) | O(V + E) |
| DFS | O(V + E) | O(V) |

**Data structures it uses:**
Graph · Queue and Deque · Stack (DFS version)

## The Template

The reusable code skeleton for this pattern lives in [`appendix/templates/advanced-graphs/`](../appendix/templates/advanced-graphs/). Read the README (when to reach for it, variations, common bugs), then type out [`template.py`](../appendix/templates/advanced-graphs/template.py) from memory before you drill problems.

## Practice

Work the matching set in the curated list: [**Advanced Graphs (Dijkstra & Topological Sort) problems →**](../../lists/recommended.md#12-advanced-graphs-11-problems). Easy → hard, top to bottom. When the pattern feels automatic, move on — don't grind it forever.

## Check Yourself

- [ ] I can write Dijkstra with a heap from memory and explain why it fails on negative edges.
- [ ] I can produce a topological order (Kahn's or DFS) and use it to detect a cycle in a DAG.
- [ ] I know which algorithm fits: BFS vs. Dijkstra vs. topo sort vs. MST.
- [ ] I solved a 🔴 Hard advanced-graph problem (e.g. Cheapest Flights or Swim in Rising Water).

---

**Up next:** [1-D Dynamic Programming](14-dp-1d.md) — state + transition + base case over one axis.

[← Prev](12-union-find.md) · [🗺 Roadmap](../../roadmap.md) · [Next →](14-dp-1d.md)

