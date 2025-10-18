# Advanced Graph Algorithms

## Weighted Graph Algorithms

### Dijkstra's Algorithm (Shortest Path)

```
Find shortest path from source to all vertices in weighted graph.

Graph:
        2       3
    A ----- B ----- C
    |       |       |
   6|      8|      |4
    |       |       |
    D ----- E ----- F
        7       5

Find shortest paths from A:

Using Min Heap (Priority Queue):

Initial:
    distances = {A: 0, B: ∞, C: ∞, D: ∞, E: ∞, F: ∞}
    heap = [(0, A)]

Step 1: Process A (distance 0)
    A ----- B       C
    |       |       |
    D       E       F

    Update neighbors:
    - B: 0 + 2 = 2
    - D: 0 + 6 = 6

    distances = {A: 0, B: 2, C: ∞, D: 6, E: ∞, F: ∞}
    heap = [(2, B), (6, D)]

Step 2: Process B (distance 2)
    A ----- B       C
    |       |       |
    D       E       F

    Update neighbors:
    - A: skip (already processed)
    - C: 2 + 3 = 5
    - E: 2 + 8 = 10

    distances = {A: 0, B: 2, C: 5, D: 6, E: 10, F: ∞}
    heap = [(5, C), (6, D), (10, E)]

Step 3: Process C (distance 5)
    Update neighbors:
    - F: 5 + 4 = 9

    distances = {A: 0, B: 2, C: 5, D: 6, E: 10, F: 9}
    heap = [(6, D), (9, F), (10, E)]

Step 4: Process D (distance 6)
    Update neighbors:
    - E: 6 + 7 = 13 (worse than 10, skip)

    distances = {A: 0, B: 2, C: 5, D: 6, E: 10, F: 9}
    heap = [(9, F), (10, E)]

Step 5: Process F (distance 9)
    Update neighbors:
    - E: 9 + 5 = 14 (worse than 10, skip)

    distances = {A: 0, B: 2, C: 5, D: 6, E: 10, F: 9}
    heap = [(10, E)]

Step 6: Process E (distance 10)
    Done!

Final shortest paths from A:
    A → A: 0
    A → B: 2 (A → B)
    A → C: 5 (A → B → C)
    A → D: 6 (A → D)
    A → E: 10 (A → B → E)
    A → F: 9 (A → B → C → F)

Visualization:
        2       3
    A ===== B ===== C
    ✓       ✓       ✓
    |               ||
    |               ||4
    |               ||
    D       E ===== F
    ✓       ✓       ✓

Path reconstruction:
Store parent nodes:
    parent = {B: A, C: B, D: A, E: B, F: C}

Path to F: F ← C ← B ← A
Reverse: A → B → C → F

Time: O((V + E) log V) with min heap
Space: O(V)

Limitations:
✗ No negative weights
✓ Works on directed/undirected
✓ Single source shortest path
```

### Bellman-Ford Algorithm

```
Handles negative weights, detects negative cycles.

Graph:
    A --1--> B --(-3)--> C
    |        ^
    2        |
    |        |
    v        1
    D -------

Negative edge: B → C with weight -3

Algorithm:
Relax all edges V-1 times

Initial:
    dist = {A: 0, B: ∞, C: ∞, D: ∞}

Iteration 1: Relax all edges
    A → B: dist[B] = min(∞, 0 + 1) = 1
    A → D: dist[D] = min(∞, 0 + 2) = 2
    B → C: dist[C] = min(∞, 1 + (-3)) = -2
    D → B: dist[B] = min(1, 2 + 1) = 1

    dist = {A: 0, B: 1, C: -2, D: 2}

Iteration 2: Relax all edges
    (No changes)

    dist = {A: 0, B: 1, C: -2, D: 2}

Iteration 3: Check for negative cycles
    If any distance can still be reduced → negative cycle

Negative Cycle Detection:
    A --1--> B
    |        |
    2      (-3)
    |        |
    v        v
    D --1--> C --(-2)--> A

Cycle: A → B → C → A
Weight: 1 + (-3) + (-2) = -4 (negative!)

After V-1 iterations, if we can still reduce:
    dist[A] = 0
    A → B: dist[B] = 1
    B → C: dist[C] = -2
    C → A: dist[A] = -2 + (-2) = -4 (reduced!)

Negative cycle detected! ✗

Time: O(V * E)
Space: O(V)

Use when:
✓ Negative weights present
✓ Need to detect negative cycles
✗ Slower than Dijkstra for positive weights
```

### Floyd-Warshall Algorithm

```
All-pairs shortest paths.

Graph:
    1 --3--> 2
    |        |
    2        1
    |        |
    v        v
    3 --1--> 4

Adjacency Matrix:
    1  2  3  4
1 [ 0  3  2  ∞ ]
2 [ ∞  0  ∞  1 ]
3 [ ∞  ∞  0  1 ]
4 [ ∞  ∞  ∞  0 ]

Algorithm: Try all intermediate vertices

k = 0 (no intermediate):
    Same as initial matrix

k = 1 (via vertex 1):
For each pair (i, j), check:
    dist[i][j] vs dist[i][1] + dist[1][j]

    1  2  3  4
1 [ 0  3  2  ∞ ]
2 [ ∞  0  ∞  1 ]
3 [ ∞  ∞  0  1 ]
4 [ ∞  ∞  ∞  0 ]

k = 2 (via vertex 2):
    3→4 via 2: 3→2→4 = ∞ + 1 = ∞ (no improvement)

    1  2  3  4
1 [ 0  3  2  4 ]  ← 1→2→4
2 [ ∞  0  ∞  1 ]
3 [ ∞  ∞  0  1 ]
4 [ ∞  ∞  ∞  0 ]

k = 3 (via vertex 3):
    1→4 via 3: 1→3→4 = 2 + 1 = 3 < 4

    1  2  3  4
1 [ 0  3  2  3 ]  ← 1→3→4
2 [ ∞  0  ∞  1 ]
3 [ ∞  ∞  0  1 ]
4 [ ∞  ∞  ∞  0 ]

k = 4 (via vertex 4):
    No improvements

Final:
    1  2  3  4
1 [ 0  3  2  3 ]
2 [ ∞  0  ∞  1 ]
3 [ ∞  ∞  0  1 ]
4 [ ∞  ∞  ∞  0 ]

Shortest paths:
1 → 2: 3 (direct)
1 → 3: 2 (direct)
1 → 4: 3 (via 3)
2 → 4: 1 (direct)
3 → 4: 1 (direct)

Time: O(V³)
Space: O(V²)

Use when:
✓ Need all-pairs shortest paths
✓ Dense graph
✓ Can handle negative weights
✗ Expensive for large graphs
```

### A* Search Algorithm

```
Optimized shortest path with heuristic.

Graph (grid):
    S . . . .
    # # . # .
    . . . # .
    . # . # .
    . . . . G

S = Start, G = Goal, # = Obstacle

Cost function: f(n) = g(n) + h(n)
- g(n): actual cost from start
- h(n): heuristic estimate to goal

Heuristic: Manhattan distance
h(n) = |x_n - x_goal| + |y_n - y_goal|

Execution:
Priority queue sorted by f(n)

Start: S at (0,0), G at (4,4)

Step 1: At S (0,0)
    g(S) = 0
    h(S) = |0-4| + |0-4| = 8
    f(S) = 0 + 8 = 8

    Expand: (1,0), (0,1)

Step 2: Choose (1,0) [f = 1 + 7 = 8]
    g = 1
    h = 7
    f = 8

    Grid:
    S → . . . .
    # # . # .
    . . . # .
    . # . # .
    . . . . G

Step 3: Continue expanding...
    Always choose lowest f(n)

Final path:
    S → → → ↓ .
    # # . ↓ .
    . . . ↓ .
    . # . ↓ .
    . . . → G

Properties:
✓ Optimal if heuristic is admissible (never overestimates)
✓ Faster than Dijkstra with good heuristic
✓ Complete (finds solution if exists)

Common heuristics:
- Manhattan distance: |x1-x2| + |y1-y2|
- Euclidean distance: √((x1-x2)² + (y1-y2)²)
- Diagonal distance: max(|x1-x2|, |y1-y2|)

Time: O(b^d) where b = branching factor, d = depth
Space: O(b^d)

Better than Dijkstra when:
✓ Have good heuristic
✓ Goal-directed search
✓ Large search space
```

## Minimum Spanning Tree (MST)

### Kruskal's Algorithm

```
Build MST by adding edges in weight order.

Graph:
    A --2-- B --3-- C
    |       |       |
    6       8       4
    |       |       |
    D --7-- E --5-- F

Edges sorted by weight:
(A,B,2), (B,C,3), (C,F,4), (E,F,5), (A,D,6), (D,E,7), (B,E,8)

Using Union-Find:

Initial: Each vertex is separate set
    {A} {B} {C} {D} {E} {F}

Step 1: Add (A,B,2)
    MST edges: {(A,B)}
    Sets: {A,B} {C} {D} {E} {F}

    A === B     C

    D     E     F

Step 2: Add (B,C,3)
    MST edges: {(A,B), (B,C)}
    Sets: {A,B,C} {D} {E} {F}

    A === B === C

    D     E     F

Step 3: Add (C,F,4)
    MST edges: {(A,B), (B,C), (C,F)}
    Sets: {A,B,C,F} {D} {E}

    A === B === C
                ||
    D     E     F

Step 4: Add (E,F,5)
    MST edges: {(A,B), (B,C), (C,F), (E,F)}
    Sets: {A,B,C,E,F} {D}

    A === B === C
                ||
    D     E === F

Step 5: Add (A,D,6)
    MST edges: {(A,B), (B,C), (C,F), (E,F), (A,D)}
    Sets: {A,B,C,D,E,F}

    A === B === C
    ||          ||
    D     E === F

Step 6: Skip (D,E,7) - would create cycle
Step 7: Skip (B,E,8) - would create cycle

MST complete!
Total weight: 2 + 3 + 4 + 5 + 6 = 20

Visual:
    A --2-- B --3-- C
    |               |
    6               4
    |               |
    D       E --5-- F

Properties:
✓ V-1 edges in MST
✓ Greedy algorithm
✓ Optimal solution

Time: O(E log E) for sorting + O(E α(V)) for union-find
Space: O(V)
```

### Prim's Algorithm

```
Build MST by growing from single vertex.

Graph:
    A --2-- B --3-- C
    |       |       |
    6       8       4
    |       |       |
    D --7-- E --5-- F

Using Min Heap:

Start at A:
    MST = {A}
    heap = [(2,A,B), (6,A,D)]

Step 1: Add edge (A,B,2)
    MST = {A,B}
    Add B's edges: (3,B,C), (8,B,E)
    heap = [(2,A,B)✓, (3,B,C), (6,A,D), (8,B,E)]

    A === B     C

    D     E     F

Step 2: Add edge (B,C,3)
    MST = {A,B,C}
    Add C's edges: (4,C,F)
    heap = [(3,B,C)✓, (4,C,F), (6,A,D), (8,B,E)]

    A === B === C

    D     E     F

Step 3: Add edge (C,F,4)
    MST = {A,B,C,F}
    Add F's edges: (5,F,E)
    heap = [(4,C,F)✓, (5,F,E), (6,A,D), (8,B,E)]

    A === B === C
                ||
    D     E     F

Step 4: Add edge (F,E,5)
    MST = {A,B,C,E,F}
    Add E's edges: (7,E,D), (8,E,B)
    heap = [(5,F,E)✓, (6,A,D), (7,E,D), (8,B,E)]

    A === B === C
                ||
    D     E === F

Step 5: Add edge (A,D,6)
    MST = {A,B,C,D,E,F}
    All vertices included!

    A === B === C
    ||          ||
    D     E === F

Total weight: 2 + 3 + 4 + 5 + 6 = 20

Time: O((V + E) log V) with min heap
Space: O(V)

Prim vs Kruskal:
- Prim: Better for dense graphs
- Kruskal: Better for sparse graphs
- Both produce same MST weight
```

## Union-Find (Disjoint Set Union)

```
Efficient structure for tracking connected components.

Operations:
- Find: Which set does element belong to?
- Union: Merge two sets

Visual:
Initial: {0} {1} {2} {3} {4}

Union(0, 1):
    {0, 1} {2} {3} {4}

    0
    |
    1

Union(2, 3):
    {0, 1} {2, 3} {4}

    0       2
    |       |
    1       3

Union(0, 2):
    {0, 1, 2, 3} {4}

    0
    |
    1   2
        |
        3

Find(3):
    3 → 2 → 0
    Parent of 3 is 0

Optimizations:

1. Union by Rank:
   Attach smaller tree to larger

   Before union(0, 2):
        0       2       (ranks: 0=1, 2=1)
        |       |
        1       3

   After:
        0               (rank 0 = 2)
       / \
      1   2
          |
          3

2. Path Compression:
   Make nodes point directly to root

   Before Find(3):
        0
       / \
      1   2
          |
          3

   After Find(3):
        0
       /|\
      1 2 3

Implementation with optimizations:

parent = [i for i in range(n)]
rank = [0] * n

def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])  # Path compression
    return parent[x]

def union(x, y):
    px, py = find(x), find(y)

    if px == py:
        return False  # Already connected

    # Union by rank
    if rank[px] < rank[py]:
        parent[px] = py
    elif rank[px] > rank[py]:
        parent[py] = px
    else:
        parent[py] = px
        rank[px] += 1

    return True

Time: O(α(n)) ≈ O(1) amortized per operation
α(n) = inverse Ackermann function (very slow growing)

Use cases:
- Kruskal's MST
- Cycle detection
- Connected components
- Network connectivity
```

## Advanced Graph Problems

### Network Flow (Ford-Fulkerson)

```
Maximum flow from source to sink.

Network:
        10      10
    S --→-- A --→-- T
    |       |       |
   10↓    10↓      ↑20
    |       |       |
    B --→-- C --→--
        10      10

Capacity on edges, find max flow S → T.

Augmenting paths:

Path 1: S → A → T (capacity 10)
    Flow: 10
    Residual:
        0       0
    S --→-- A --→-- T
    |←10    |←10   ↑20
   10↓    10↓      ↑
    |       |       |
    B --→-- C --→--
        10      10

Path 2: S → B → C → T (capacity 10)
    Flow: 10 + 10 = 20
    Final residual graph

Max flow: 20

Saturated edges: S→A, A→T, S→B, B→C, C→T

Time: O(E * max_flow) for Ford-Fulkerson
Time: O(V * E²) for Edmonds-Karp (BFS-based)
```

### Tarjan's Algorithm (Strongly Connected Components)

```
Find SCCs in directed graph.

Graph:
    0 → 1 → 2
    ↑   ↓   ↓
    3 ← 4   5
        ↓
        6

SCCs: {0,1,3,4}, {2}, {5}, {6}

DFS with low-link values:

Discovery time and low-link:
    disc[v] = time when discovered
    low[v] = lowest disc reachable

Execution:
    0(0,0) → 1(1,0) → 2(2,2)
    ↑        ↓
    3(4,0) ← 4(3,0)

Stack: [0, 1, 4, 3]

When low[v] == disc[v]:
    Pop stack until v → that's an SCC

Time: O(V + E)
Space: O(V)
```

## Time and Space Complexity Summary

```
Algorithm              Time            Space    Use Case
Dijkstra               O((V+E) log V)  O(V)     Shortest path, positive weights
Bellman-Ford           O(V*E)          O(V)     Negative weights, detect cycles
Floyd-Warshall         O(V³)           O(V²)    All-pairs shortest path
A*                     O(b^d)          O(b^d)   Heuristic shortest path
Kruskal's MST          O(E log E)      O(V)     Sparse graph MST
Prim's MST             O((V+E) log V)  O(V)     Dense graph MST
Union-Find             O(α(n))         O(n)     Connected components
Ford-Fulkerson         O(E * max_flow) O(V)     Max flow
Tarjan's SCC           O(V + E)        O(V)     Strongly connected components
```

## Python Implementation

```python
import heapq
from collections import defaultdict

# Dijkstra's Algorithm
def dijkstra(graph, start):
    """
    Shortest path from start to all vertices.
    Time: O((V+E) log V), Space: O(V)
    """
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    heap = [(0, start)]
    visited = set()

    while heap:
        dist, node = heapq.heappop(heap)

        if node in visited:
            continue

        visited.add(node)

        for neighbor, weight in graph[node]:
            new_dist = dist + weight

            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))

    return distances


# Dijkstra with path reconstruction
def dijkstra_with_path(graph, start, end):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    parent = {start: None}
    heap = [(0, start)]
    visited = set()

    while heap:
        dist, node = heapq.heappop(heap)

        if node == end:
            # Reconstruct path
            path = []
            while node is not None:
                path.append(node)
                node = parent[node]
            return distances[end], path[::-1]

        if node in visited:
            continue

        visited.add(node)

        for neighbor, weight in graph[node]:
            new_dist = dist + weight

            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                parent[neighbor] = node
                heapq.heappush(heap, (new_dist, neighbor))

    return float('inf'), []


# Bellman-Ford Algorithm
def bellman_ford(graph, start, n):
    """
    Shortest path with negative weights.
    Time: O(V*E), Space: O(V)
    Returns: (distances, has_negative_cycle)
    """
    distances = [float('inf')] * n
    distances[start] = 0

    # Relax edges V-1 times
    for _ in range(n - 1):
        for u in range(n):
            for v, weight in graph[u]:
                if distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight

    # Check for negative cycle
    for u in range(n):
        for v, weight in graph[u]:
            if distances[u] + weight < distances[v]:
                return distances, True  # Negative cycle

    return distances, False


# Floyd-Warshall Algorithm
def floyd_warshall(graph):
    """
    All-pairs shortest paths.
    Time: O(V³), Space: O(V²)
    """
    n = len(graph)
    dist = [[float('inf')] * n for _ in range(n)]

    # Initialize
    for i in range(n):
        dist[i][i] = 0
        for j, weight in graph[i]:
            dist[i][j] = weight

    # Try all intermediate vertices
    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

    return dist


# A* Search
def a_star(grid, start, goal):
    """
    A* pathfinding on grid.
    Time: O(b^d), Space: O(b^d)
    """
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def neighbors(pos):
        r, c = pos
        for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != '#':
                yield (nr, nc)

    heap = [(0, start)]
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    parent = {start: None}

    while heap:
        _, current = heapq.heappop(heap)

        if current == goal:
            # Reconstruct path
            path = []
            while current:
                path.append(current)
                current = parent[current]
            return path[::-1]

        for neighbor in neighbors(current):
            tentative_g = g_score[current] + 1

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                parent[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(heap, (f_score[neighbor], neighbor))

    return None


# Kruskal's MST
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)

        if px == py:
            return False

        if self.rank[px] < self.rank[py]:
            self.parent[px] = py
        elif self.rank[px] > self.rank[py]:
            self.parent[py] = px
        else:
            self.parent[py] = px
            self.rank[px] += 1

        return True


def kruskal(n, edges):
    """
    Minimum Spanning Tree.
    Time: O(E log E), Space: O(V)
    """
    edges.sort(key=lambda x: x[2])  # Sort by weight
    uf = UnionFind(n)
    mst = []
    total_weight = 0

    for u, v, weight in edges:
        if uf.union(u, v):
            mst.append((u, v, weight))
            total_weight += weight

            if len(mst) == n - 1:
                break

    return mst, total_weight


# Prim's MST
def prim(graph, start):
    """
    Minimum Spanning Tree.
    Time: O((V+E) log V), Space: O(V)
    """
    mst = []
    visited = {start}
    heap = [(weight, start, neighbor) for neighbor, weight in graph[start]]
    heapq.heapify(heap)

    while heap and len(visited) < len(graph):
        weight, u, v = heapq.heappop(heap)

        if v in visited:
            continue

        visited.add(v)
        mst.append((u, v, weight))

        for neighbor, w in graph[v]:
            if neighbor not in visited:
                heapq.heappush(heap, (w, v, neighbor))

    total_weight = sum(w for _, _, w in mst)
    return mst, total_weight


# Network connectivity with Union-Find
def is_connected(n, edges):
    """Check if graph is connected."""
    uf = UnionFind(n)

    for u, v in edges:
        uf.union(u, v)

    root = uf.find(0)
    return all(uf.find(i) == root for i in range(n))


# Tarjan's SCC
def tarjan_scc(graph):
    """
    Find strongly connected components.
    Time: O(V+E), Space: O(V)
    """
    n = len(graph)
    disc = [-1] * n
    low = [-1] * n
    on_stack = [False] * n
    stack = []
    time = [0]
    sccs = []

    def dfs(u):
        disc[u] = low[u] = time[0]
        time[0] += 1
        stack.append(u)
        on_stack[u] = True

        for v in graph[u]:
            if disc[v] == -1:
                dfs(v)
                low[u] = min(low[u], low[v])
            elif on_stack[v]:
                low[u] = min(low[u], disc[v])

        if low[u] == disc[u]:
            scc = []
            while True:
                v = stack.pop()
                on_stack[v] = False
                scc.append(v)
                if v == u:
                    break
            sccs.append(scc)

    for i in range(n):
        if disc[i] == -1:
            dfs(i)

    return sccs
```

## Key Takeaways

1. **Shortest Path**:
   - Dijkstra: Positive weights, single source
   - Bellman-Ford: Negative weights, detect cycles
   - Floyd-Warshall: All pairs
   - A*: Heuristic optimization

2. **MST**:
   - Kruskal: Sort edges, union-find
   - Prim: Grow from vertex, min heap

3. **Union-Find**:
   - Path compression
   - Union by rank
   - Nearly O(1) operations

4. **When to Use**:
   - Dijkstra: GPS, network routing
   - MST: Network design, clustering
   - A*: Game pathfinding, robotics
   - Union-Find: Dynamic connectivity

5. **Optimization**:
   - Choose right algorithm for graph type
   - Dense vs sparse affects choice
   - Heuristics improve search
   - Data structures matter (heap, union-find)
