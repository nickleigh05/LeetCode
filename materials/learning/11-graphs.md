# 11. Graphs (BFS & DFS)
*BFS for shortest unweighted paths, DFS for connectivity.*

[← Prev](10-backtracking.md) · [🗺 Roadmap](../../roadmap.md) · [Next →](12-union-find.md)

---

> **Read first if rusty:** [Grids Primer](10b-grids-primer.md) — many problems here are grid flood-fills (Number of Islands, Rotting Oranges). The 2-D indexing, 4-neighbor, and bounds-check idioms live there.

A graph is just nodes and edges — and grids, course prerequisites, and friend networks are all graphs in disguise. Two traversals do most of the work: **BFS** explores level by level (shortest path in an unweighted graph), **DFS** dives deep (connectivity, cycles, flood fill). Build the adjacency list, pick the traversal, and most graph problems fall.

## Concept

### Graph

```
  Undirected Graph:           Directed Graph (DAG):
    1 ── 2                      1 ──→ 2
    │  ╲ │                      │     │
    │   ╲│                      ↓     ↓
    3    4                      3 ──→ 4

  Adjacency List (most common for sparse graphs):
  graph = {
      1: [2, 3, 4],
      2: [1, 4],
      3: [1],
      4: [1, 2]
  }

  Adjacency Matrix (for dense graphs / O(1) edge lookup):
       1  2  3  4
  1  [ 0, 1, 1, 1 ]
  2  [ 1, 0, 0, 1 ]
  3  [ 1, 0, 0, 0 ]
  4  [ 1, 1, 0, 0 ]

  Grid as graph (4-directional neighbors):
  directions = [(0,1),(0,-1),(1,0),(-1,0)]
```

**What it is:** A set of vertices (nodes) connected by edges. Can be directed or undirected, weighted or unweighted, cyclic or acyclic.

**Key Properties:**
- Adjacency list: O(V + E) space — standard for most LeetCode problems
- Adjacency matrix: O(V²) space — use only when edges are dense or O(1) edge lookup needed
- A grid is an implicit graph where each cell connects to its neighbors
- V = number of vertices, E = number of edges

**Complexity (Adjacency List):**

| Operation | Time |
|-----------|------|
| Add vertex | O(1) |
| Add edge | O(1) |
| Check edge (u, v) | O(degree of u) |
| Get neighbors | O(degree) |
| BFS / DFS traversal | O(V + E) |
| Space | O(V + E) |

**Use when:**
- Problems about connections, paths, or reachability
- Islands, clones, dependencies (course schedule), routes
- The problem involves nodes and relationships between them
- Grid traversal (number of islands, shortest path in maze)

**Python:**
```python
from collections import defaultdict, deque

# Build adjacency list
graph = defaultdict(list)
graph[1].append(2)
graph[2].append(1)   # undirected: add both directions

# Build from edge list
edges = [(1,2), (2,3), (3,4)]
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)  # omit for directed

# Grid traversal
def neighbors(r, c, rows, cols):
    for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
        nr, nc = r+dr, c+dc
        if 0 <= nr < rows and 0 <= nc < cols:
            yield nr, nc
```

## The Pattern

### BFS on Grid and Tree

```
  Shortest path in grid (0=open, 1=wall):
  ┌───┬───┬───┬───┐
  │ S │ 0 │ 1 │ 0 │   S = start (0,0)
  ├───┼───┼───┼───┤   E = end   (3,3)
  │ 0 │ 0 │ 1 │ 0 │
  ├───┼───┼───┼───┤
  │ 1 │ 0 │ 0 │ 0 │
  ├───┼───┼───┼───┤
  │ 0 │ 0 │ 0 │ E │
  └───┴───┴───┴───┘

  BFS expands level by level (each level = 1 more step):
  Level 0: {(0,0)}
  Level 1: {(0,1),(1,0)}
  Level 2: {(1,1),(2,1)}    ← (0,2) blocked by wall
  Level 3: {(2,2),(3,1)}
  Level 4: {(2,3),(3,2)}
  Level 5: {(3,3)} ✓  shortest path = 5 steps

  Tree level-order (BFS):
       1
      / \
     2   3       Level 0: [1]
    / \   \      Level 1: [2, 3]
   4   5   6     Level 2: [4, 5, 6]
```

**What it is:** BFS guarantees the shortest path in unweighted graphs and grids, and processes tree nodes level by level. Use when you need the minimum distance/steps or want to process nodes by distance from the source.

**Use this when:**
- [ ] Shortest path in an unweighted grid or graph
- [ ] "Minimum steps/moves to reach X"
- [ ] Level-order traversal of a binary tree
- [ ] Multi-source BFS (start from all sources at once)
- [ ] "Rotting oranges" style — spread from multiple origins
- [ ] 0-1 BFS (use deque: 0-weight edges go to front, 1-weight go to back)

**Python:**
```python
from collections import deque

# Grid BFS — shortest path
def shortest_path(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    q = deque([(start[0], start[1], 0)])
    visited = {start}
    dirs = [(0,1),(0,-1),(1,0),(-1,0)]

    while q:
        r, c, steps = q.popleft()
        if (r, c) == end:
            return steps
        for dr, dc in dirs:
            nr, nc = r+dr, c+dc
            if 0<=nr<rows and 0<=nc<cols and (nr,nc) not in visited and grid[nr][nc]==0:
                visited.add((nr, nc))
                q.append((nr, nc, steps+1))
    return -1

# Multi-source BFS (rotting oranges)
def oranges_rotting(grid):
    rows, cols = len(grid), len(grid[0])
    q = deque()
    fresh = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2: q.append((r, c, 0))
            elif grid[r][c] == 1: fresh += 1
    minutes = 0
    while q:
        r, c, t = q.popleft()
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nr, nc = r+dr, c+dc
            if 0<=nr<rows and 0<=nc<cols and grid[nr][nc]==1:
                grid[nr][nc] = 2
                fresh -= 1
                minutes = t + 1
                q.append((nr, nc, t+1))
    return minutes if fresh == 0 else -1

# Tree level-order
def level_order(root):
    if not root: return []
    q, result = deque([root]), []
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left: q.append(node.left)
            if node.right: q.append(node.right)
        result.append(level)
    return result
```

**Complexity:** O(V + E) for graphs, O(r·c) for grids, O(n) for trees.

**Blind 75 examples:** Binary Tree Level Order Traversal · Number of Islands (BFS variant) · Course Schedule (BFS topo sort)

## Algorithm Deep-Dive

### Breadth-First Search

```
  Graph/Tree:          BFS order (starting from A):
      A                Level 0: A
     / \               Level 1: B, C
    B   C              Level 2: D, E, F
   / \   \
  D   E   F

  Queue evolution:
  Start:  [A]
  Pop A:  process A, enqueue B, C  → [B, C]
  Pop B:  process B, enqueue D, E  → [C, D, E]
  Pop C:  process C, enqueue F     → [D, E, F]
  Pop D:  process D (leaf)         → [E, F]
  Pop E:  process E (leaf)         → [F]
  Pop F:  process F (leaf)         → []

  BFS guarantees: first time you reach a node = shortest path
  (in unweighted graphs)
```

**What it does:** Explores all neighbors of the current node before moving deeper. Uses a queue (FIFO). Guarantees the shortest path in an unweighted graph.

**Recognition signals:**
- Shortest path in an unweighted graph or grid
- Level-order tree traversal
- "Minimum steps to reach X"
- Multi-source BFS (start with multiple nodes simultaneously)
- Check if a graph is bipartite

**Python:**
```python
from collections import deque

# Graph BFS (shortest path / connected components)
def bfs(graph, start):
    visited = {start}
    q = deque([start])
    distance = {start: 0}

    while q:
        node = q.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                distance[neighbor] = distance[node] + 1
                q.append(neighbor)
    return distance

# Grid BFS (shortest path in 2D grid)
def bfs_grid(grid, start_r, start_c):
    rows, cols = len(grid), len(grid[0])
    q = deque([(start_r, start_c, 0)])  # (row, col, steps)
    visited = {(start_r, start_c)}
    dirs = [(0,1),(0,-1),(1,0),(-1,0)]

    while q:
        r, c, steps = q.popleft()
        for dr, dc in dirs:
            nr, nc = r+dr, c+dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr,nc) not in visited:
                if grid[nr][nc] == 0:  # passable
                    visited.add((nr, nc))
                    q.append((nr, nc, steps + 1))

# Multi-source BFS (e.g., rotting oranges: all rotten start at once)
q = deque()
for r in range(rows):
    for c in range(cols):
        if grid[r][c] == ROTTEN:
            q.append((r, c, 0))
```

**Complexity:**

| | Time | Space |
|-|------|-------|
| Graph | O(V + E) | O(V) |
| Grid (r×c) | O(r·c) | O(r·c) |

**Data structures it uses:**
Queue and Deque · Graph · Binary Tree

### Depth-First Search

```
  Graph:    DFS from A (pre-order):
    A         Visit A → push B, C
   / \        Visit B → push D, E
  B   C       Visit D (leaf, backtrack)
 / \   \      Visit E (leaf, backtrack)
D   E   F     Visit C → push F
              Visit F (leaf, backtrack)
  DFS order: A, B, D, E, C, F

  Call stack visualization:
  dfs(A)
   └─ dfs(B)
       ├─ dfs(D)   ← returns
       └─ dfs(E)   ← returns
   └─ dfs(C)
       └─ dfs(F)   ← returns

  Cycle detection (directed graph):
  WHITE = unvisited, GRAY = in current path, BLACK = done
  If you reach a GRAY node → cycle!
```

**What it does:** Explores as far as possible along each branch before backtracking. Can be implemented recursively (using the call stack) or iteratively (with an explicit stack). Foundational for almost all tree problems.

**Recognition signals:**
- Exploring all paths (permutations, combinations, subsets)
- Connected components in a graph
- Cycle detection
- Topological sort (DFS-based)
- Tree traversals (inorder, preorder, postorder)
- Path sum / max path problems on trees

**Python:**
```python
# Recursive DFS (graph)
def dfs(node, graph, visited):
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(neighbor, graph, visited)

# Iterative DFS (graph) — use when recursion depth is large
def dfs_iter(start, graph):
    visited = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                stack.append(neighbor)

# Tree DFS (recursive) — inorder
def inorder(root):
    if not root: return
    inorder(root.left)
    process(root.val)      # swap order for pre/postorder
    inorder(root.right)

# Grid DFS (flood fill / number of islands)
def dfs_grid(grid, r, c, visited):
    if r < 0 or r >= len(grid) or c < 0 or c >= len(grid[0]):
        return
    if (r, c) in visited or grid[r][c] == 0:
        return
    visited.add((r, c))
    for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
        dfs_grid(grid, r+dr, c+dc, visited)
```

**Complexity:**

| | Time | Space |
|-|------|-------|
| Graph | O(V + E) | O(V) call stack |
| Grid | O(r·c) | O(r·c) |
| Tree | O(n) | O(h) where h = height |

**Data structures it uses:**
Stack · Graph · Binary Tree · Trie

## The Template

The reusable code skeleton for this pattern lives in [`appendix/templates/graphs/`](../appendix/templates/graphs/). Read the README (when to reach for it, variations, common bugs), then type out [`template.py`](../appendix/templates/graphs/template.py) from memory before you drill problems.

## Practice

Work the guided set with hints & solutions: [**Graphs (BFS & DFS) — Practice →**](../rmap-practice/11-graphs.md). Easy → hard, top to bottom; when the pattern feels automatic, move on — don’t grind it forever. Want more volume? See the [recommended list](../../lists/recommended.md#11-graphs-23-problems).

## Check Yourself

- [ ] I can build an adjacency list from an edge list and run BFS *and* DFS from memory.
- [ ] I can explain why BFS gives shortest paths in an *unweighted* graph but DFS does not.
- [ ] I can detect a cycle and count connected components.
- [ ] I solved a 🔴 Hard graph problem (e.g. Word Ladder or Alien Dictionary).

---

**Up next:** [Union-Find (Disjoint Set Union)](12-union-find.md) — near-O(1) connectivity and cycle detection under merges.

[← Prev](10-backtracking.md) · [🗺 Roadmap](../../roadmap.md) · [Next →](12-union-find.md)

