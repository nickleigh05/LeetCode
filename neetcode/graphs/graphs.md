# Graphs

## How to use this README

Problems are split into three tiers: Blind 75 is the core set every interviewer expects you to know cold. NeetCode 150 introduces multi-source BFS, topological sort, and Union-Find for cycle detection. NeetCode 250 adds harder graph transformations, weighted BFS, reachability queries, and account merging. Work through tiers in order — the Core Patterns and Syntax Reference sections below map directly to the problems in each table. When you see a new graph problem, first classify it: is it a grid or adjacency list? Do you need shortest path, connectivity, or ordering? That classification tells you which pattern to reach for.

---

## Problems

### Blind 75
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved |
|-----------|------------|--------------|---------------|--------|
| 200 | Medium | Number of Islands | [Link](https://leetcode.com/problems/number-of-islands/) | ☐ |
| 133 | Medium | Clone Graph | [Link](https://leetcode.com/problems/clone-graph/) | ☐ |
| 417 | Medium | Pacific Atlantic Water Flow | [Link](https://leetcode.com/problems/pacific-atlantic-water-flow/) | ☐ |
| 207 | Medium | Course Schedule | [Link](https://leetcode.com/problems/course-schedule/) | ☐ |
| 261 | Medium | Graph Valid Tree | [Link](https://leetcode.com/problems/graph-valid-tree/) | ☐ |
| 323 | Medium | Number of Connected Components in an Undirected Graph | [Link](https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/) | ☐ |

### NeetCode 150
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved |
|-----------|------------|--------------|---------------|--------|
| 695 | Medium | Max Area of Island | [Link](https://leetcode.com/problems/max-area-of-island/) | ☐ |
| 130 | Medium | Surrounded Regions | [Link](https://leetcode.com/problems/surrounded-regions/) | ☐ |
| 994 | Medium | Rotting Oranges | [Link](https://leetcode.com/problems/rotting-oranges/) | ☐ |
| 286 | Medium | Walls and Gates | [Link](https://leetcode.com/problems/walls-and-gates/) | ☐ |
| 210 | Medium | Course Schedule II | [Link](https://leetcode.com/problems/course-schedule-ii/) | ☐ |
| 684 | Medium | Redundant Connection | [Link](https://leetcode.com/problems/redundant-connection/) | ☐ |
| 127 | Hard | Word Ladder | [Link](https://leetcode.com/problems/word-ladder/) | ☐ |

### NeetCode 250
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved | Pattern |
|-----------|------------|--------------|---------------|--------|---------|
| 463 | Easy | Island Perimeter | [Link](https://leetcode.com/problems/island-perimeter/) | ☐ | Grid traversal |
| 953 | Easy | Verifying an Alien Dictionary | [Link](https://leetcode.com/problems/verifying-an-alien-dictionary/) | ☐ | Topological ordering |
| 997 | Easy | Find the Town Judge | [Link](https://leetcode.com/problems/find-the-town-judge/) | ☐ | In/out degree |
| 752 | Medium | Open the Lock | [Link](https://leetcode.com/problems/open-the-lock/) | ☐ | BFS shortest path |
| 1462 | Medium | Course Schedule IV | [Link](https://leetcode.com/problems/course-schedule-iv/) | ☐ | Reachability (BFS/Floyd) |
| 721 | Medium | Accounts Merge | [Link](https://leetcode.com/problems/accounts-merge/) | ☐ | Union-Find |
| 399 | Medium | Evaluate Division | [Link](https://leetcode.com/problems/evaluate-division/) | ☐ | Weighted graph BFS |
| 310 | Medium | Minimum Height Trees | [Link](https://leetcode.com/problems/minimum-height-trees/) | ☐ | Topological leaf trimming |

---

## Complexity Reference

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| DFS (adjacency list) | O(V+E) | O(V) | Visits every vertex and edge once |
| BFS (adjacency list) | O(V+E) | O(V) | Queue holds at most V nodes |
| DFS / BFS (grid m×n) | O(m*n) | O(m*n) | Each cell visited once |
| Topological sort (Kahn's) | O(V+E) | O(V) | BFS variant, tracks in-degrees |
| Topological sort (DFS) | O(V+E) | O(V) | Postorder DFS |
| Union-Find find (path compression) | O(α(n)) ≈ O(1) | O(n) | α is inverse Ackermann |
| Union-Find union (rank + compression) | O(α(n)) ≈ O(1) | O(n) | Practically constant |
| Build adjacency list from edge list | O(E) | O(V+E) | One pass over edges |
| Connected components count | O(V+E) | O(V) | DFS/BFS or Union-Find |
| Cycle detection (undirected) | O(V+E) | O(V) | DFS with parent tracking or Union-Find |
| Cycle detection (directed) | O(V+E) | O(V) | DFS with three-color marking |

---

## Data Structures

### Adjacency List

An adjacency list maps each node to a list of its neighbors. In Python this is a `dict` (or `defaultdict(list)`). It uses O(V+E) space — proportional to the actual number of edges, not V² — making it the standard representation for sparse graphs. DFS and BFS both traverse the list in O(V+E) total.

```
Graph edges: 0-1, 0-2, 1-3, 2-3

Adjacency list:
{
  0: [1, 2],
  1: [0, 3],
  2: [0, 3],
  3: [1, 2]
}

Traversal: start at 0 → visit 1, 2
           from 1 → visit 3 (0 already seen)
           from 2 → 0 seen, 3 seen → done
```

**When it matters:** Default choice for almost all graph problems. Iterating over neighbors is O(degree), and the total work across all nodes is O(E). Use an adjacency matrix only when you need O(1) edge-existence queries or the graph is dense (E close to V²).

### Adjacency Matrix

An n×n boolean (or weight) grid where `matrix[i][j]` is True/non-zero if there's an edge from i to j. O(V²) space regardless of edge count. Edge lookup is O(1). Iterating over all neighbors of a node is O(V).

```
Same graph (0-1, 0-2, 1-3, 2-3), n=4:

     0  1  2  3
  0 [0, 1, 1, 0]
  1 [1, 0, 0, 1]
  2 [1, 0, 0, 1]
  3 [0, 1, 1, 0]

matrix[0][1] = 1 → edge exists
matrix[0][3] = 0 → no edge
```

**When it matters:** Use when the graph is dense, when you need to check whether a specific edge exists in O(1), or when the problem gives you a grid that is itself the graph.

### Union-Find (Disjoint Set Union)

An array of parent pointers. Each element starts as its own parent. `find(x)` follows parent pointers to the root, applying path compression so future calls are faster. `union(x, y)` merges two sets by pointing one root to the other, using rank to keep the tree shallow.

```
Initial (each node its own set):
parent: [0, 1, 2, 3, 4]

union(0, 1):  parent[1] = 0  →  [0, 0, 2, 3, 4]
union(2, 3):  parent[3] = 2  →  [0, 0, 2, 2, 4]
union(0, 2):  parent[2] = 0  →  [0, 0, 0, 2, 4]

find(3): 3 → parent[3]=2 → parent[2]=0 → root is 0
         path compression: parent[3] = 0 directly
```

**When it matters:** Counting connected components, detecting cycles in undirected graphs, and merging groups incrementally (Accounts Merge #721, Redundant Connection #684). Faster than repeated DFS when you have many union queries.

---

## Core Patterns

### DFS on Graph

**When to use:** Explore all reachable nodes from a source, detect cycles, or count components. Works on both adjacency lists and grids.
**Complexity:** O(V+E) time, O(V) space (recursion stack)
**Problems:** Number of Islands (#200), Clone Graph (#133), Pacific Atlantic Water Flow (#417), Max Area of Island (#695)
**Common mistake:** Not marking a node as visited before recursing — causes infinite loops on cycles. Mark visited as soon as you decide to visit, not when you finish.

```python
def dfs(graph, start):
    visited = set()
    def explore(node):
        if node in visited:
            return
        visited.add(node)
        for neighbor in graph[node]:
            explore(neighbor)
    explore(start)
    return visited
```

### BFS Shortest Path

**When to use:** Find the shortest path (minimum hops) in an unweighted graph or grid. BFS processes all nodes at distance d before any node at distance d+1, guaranteeing shortest paths.
**Complexity:** O(V+E) time, O(V) space
**Problems:** Word Ladder (#127), Open the Lock (#752), Rotting Oranges (#994), Walls and Gates (#286)
**Common mistake:** Adding neighbors to `visited` when you dequeue them instead of when you enqueue them — this allows the same node to be enqueued multiple times and inflates runtime.

```python
from collections import deque

def bfs_shortest(graph, start, target):
    visited = {start}
    q = deque([(start, 0)])    # (node, distance)
    while q:
        node, dist = q.popleft()
        if node == target:
            return dist
        for nei in graph[node]:
            if nei not in visited:
                visited.add(nei)   # mark when enqueuing, not when dequeuing
                q.append((nei, dist + 1))
    return -1
```

### Multi-Source BFS

**When to use:** You want the shortest distance from ANY of several sources to every other node. Start BFS with all sources already in the queue.
**Complexity:** O(V+E) time, O(V) space
**Problems:** Rotting Oranges (#994), Walls and Gates (#286), Pacific Atlantic Water Flow (#417)
**Common mistake:** Running separate BFS from each source individually — O(S * (V+E)) instead of O(V+E). Multi-source BFS gets all distances in one pass.

```python
from collections import deque

def multi_source_bfs(grid, sources):
    rows, cols = len(grid), len(grid[0])
    q = deque()
    visited = set()
    for r, c in sources:
        q.append((r, c, 0))
        visited.add((r, c))
    dirs = [(0,1),(0,-1),(1,0),(-1,0)]
    while q:
        r, c, dist = q.popleft()
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                visited.add((nr, nc))
                q.append((nr, nc, dist + 1))
```

### Topological Sort (Kahn's Algorithm)

**When to use:** Order nodes in a DAG so every node appears before its dependencies. Detect cycles (if not all nodes are output, a cycle exists).
**Complexity:** O(V+E) time, O(V) space
**Problems:** Course Schedule (#207), Course Schedule II (#210), Minimum Height Trees (#310)
**Common mistake:** Not checking whether all nodes were included in the output — if `len(order) != numNodes`, there was a cycle.

```python
from collections import deque, defaultdict

def topo_sort(n, edges):
    graph = defaultdict(list)
    indegree = [0] * n
    for u, v in edges:
        graph[u].append(v)
        indegree[v] += 1
    q = deque(i for i in range(n) if indegree[i] == 0)
    order = []
    while q:
        node = q.popleft()
        order.append(node)
        for nei in graph[node]:
            indegree[nei] -= 1
            if indegree[nei] == 0:
                q.append(nei)
    return order if len(order) == n else []   # empty list = cycle detected
```

### Union-Find

**When to use:** Determine if two nodes are in the same connected component, count components, or detect if adding an edge creates a cycle.
**Complexity:** O(α(n)) ≈ O(1) per operation after O(n) setup
**Problems:** Number of Connected Components (#323), Graph Valid Tree (#261), Redundant Connection (#684), Accounts Merge (#721)
**Common mistake:** Forgetting path compression in `find` — without it, the tree can degenerate to O(n) depth and each find becomes O(n).

```python
parent = list(range(n))
rank = [0] * n

def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])   # path compression
    return parent[x]

def union(x, y):
    px, py = find(x), find(y)
    if px == py:
        return False   # already connected — adding this edge creates a cycle
    if rank[px] < rank[py]:
        px, py = py, px
    parent[py] = px
    if rank[px] == rank[py]:
        rank[px] += 1
    return True
```

---

## Syntax Reference

### BFS boilerplate

```python
from collections import deque

q = deque([start])
visited = {start}
while q:
    node = q.popleft()
    for nei in graph[node]:
        if nei not in visited:
            visited.add(nei)
            q.append(nei)
```

### DFS iterative (stack)

```python
stack = [start]
visited = {start}
while stack:
    node = stack.pop()
    for nei in graph[node]:
        if nei not in visited:
            visited.add(nei)
            stack.append(nei)
```

### Grid directions

```python
dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]   # right, left, down, up

for dr, dc in dirs:
    nr, nc = r + dr, c + dc
    if 0 <= nr < rows and 0 <= nc < cols:
        # valid cell
```

### Build adjacency list from edge list

```python
from collections import defaultdict

graph = defaultdict(list)
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)   # omit this line for directed graphs
```

### Topological sort (DFS postorder)

```python
visited = set()
cycle_check = set()   # nodes in current DFS path
order = []

def dfs(node):
    if node in cycle_check: return False   # cycle detected
    if node in visited: return True
    cycle_check.add(node)
    for nei in graph[node]:
        if not dfs(nei): return False
    cycle_check.remove(node)
    visited.add(node)
    order.append(node)   # append after all descendants are done
    return True
```

### Union-Find (minimal)

```python
parent = list(range(n))

def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])
    return parent[x]

def union(x, y):
    parent[find(x)] = find(y)
```

### Count connected components with Union-Find

```python
components = n
for u, v in edges:
    if union(u, v):      # union returns True if they were in different sets
        components -= 1
```
