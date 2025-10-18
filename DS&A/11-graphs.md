# Graphs

## What is a Graph?
A graph is a non-linear data structure consisting of vertices (nodes) and edges that connect them. Graphs model relationships between objects and are used in social networks, maps, recommendation systems, and more.

## Graph Terminology

```
Basic Graph:
    A --- B
    |     |
    C --- D

Vertices (Nodes): A, B, C, D
Edges: (A,B), (A,C), (B,D), (C,D)
Degree: Number of edges connected to a vertex
- Degree(A) = 2
- Degree(B) = 2
- Degree(C) = 2
- Degree(D) = 2

Path: Sequence of vertices connected by edges
- Path from A to D: A → B → D or A → C → D

Cycle: Path that starts and ends at same vertex
- A → B → D → C → A

Connected Graph: Path exists between any two vertices
```

## Types of Graphs

### 1. Directed vs Undirected

```
Undirected Graph:
    A --- B
    |     |
    C --- D

Edges are bidirectional
(A,B) means A↔B

Directed Graph (Digraph):
    A --> B
    ↓     ↓
    C --> D

Edges have direction
(A,B) means A→B only

Example:
Social network: Undirected (friendship)
Twitter: Directed (follower relationship)
```

### 2. Weighted vs Unweighted

```
Unweighted:
    A --- B
    |     |
    C --- D

All edges equal weight

Weighted:
    A --5-- B
    |       |
    3       2
    |       |
    C --1-- D

Edges have weights/costs

Example:
- Road network: weighted (distance)
- Social network: unweighted
```

### 3. Cyclic vs Acyclic

```
Cyclic:
    A --> B
    ↑     ↓
    D <-- C

Contains cycles: A→B→C→D→A

Acyclic (DAG - Directed Acyclic Graph):
    A --> B
    ↓     ↓
    C --> D

No cycles

Example:
- Task dependencies: DAG
- General graph: may have cycles
```

### 4. Connected vs Disconnected

```
Connected:
    A --- B
    |     |
    C --- D

Path between any two vertices

Disconnected:
    A --- B    E
    |     |
    C --- D

No path from {A,B,C,D} to E

Strongly Connected (directed):
Path exists in both directions for all pairs
```

## Graph Representations

### 1. Adjacency Matrix

```
Graph:
    0 --- 1
    |     |
    2 --- 3

Matrix (2D array):
    0  1  2  3
0 [ 0  1  1  0 ]
1 [ 1  0  0  1 ]
2 [ 1  0  0  1 ]
3 [ 0  1  1  0 ]

matrix[i][j] = 1 if edge exists from i to j

Weighted Graph:
    0 --5-- 1
    |       |
    3       2
    |       |
    2 --1-- 3

Matrix:
    0  1  2  3
0 [ 0  5  3  0 ]
1 [ 5  0  0  2 ]
2 [ 3  0  0  1 ]
3 [ 0  2  1  0 ]

Pros:
✓ O(1) edge lookup
✓ Simple to implement
✓ Good for dense graphs

Cons:
✗ O(V²) space
✗ O(V) to find neighbors
✗ Inefficient for sparse graphs

Space: O(V²)
Edge lookup: O(1)
Find neighbors: O(V)
```

### 2. Adjacency List

```
Graph:
    0 --- 1
    |     |
    2 --- 3

List (array of lists/sets):
0: [1, 2]
1: [0, 3]
2: [0, 3]
3: [1, 2]

Weighted Graph:
    0 --5-- 1
    |       |
    3       2
    |       |
    2 --1-- 3

List with weights:
0: [(1, 5), (2, 3)]
1: [(0, 5), (3, 2)]
2: [(0, 3), (3, 1)]
3: [(1, 2), (2, 1)]

Pros:
✓ O(V + E) space
✓ O(degree) to find neighbors
✓ Efficient for sparse graphs

Cons:
✗ O(V) edge lookup worst case
✗ Slightly more complex

Space: O(V + E)
Edge lookup: O(degree)
Find neighbors: O(degree)

Implementation:
graph = {
    0: [1, 2],
    1: [0, 3],
    2: [0, 3],
    3: [1, 2]
}

Or with class:
graph = [[] for _ in range(n)]
graph[0].append(1)  # Edge 0→1
```

### 3. Edge List

```
Graph:
    0 --- 1
    |     |
    2 --- 3

List of edges:
edges = [
    (0, 1),
    (0, 2),
    (1, 3),
    (2, 3)
]

Weighted:
edges = [
    (0, 1, 5),  # (from, to, weight)
    (0, 2, 3),
    (1, 3, 2),
    (2, 3, 1)
]

Pros:
✓ Simple
✓ Good for edge-centric algorithms
✓ Easy to sort by weight

Cons:
✗ O(E) to find neighbors
✗ Not efficient for traversal

Space: O(E)
```

## Graph Traversal

### 1. Depth-First Search (DFS)

```
Graph:
    0 --- 1
    |     |
    2 --- 3

DFS from 0:

Stack-based traversal:
Start: stack = [0], visited = {}

Step 1: Visit 0
    stack = [1, 2]
    visited = {0}

    0(✓)-- 1
    |      |
    2 ---- 3

Step 2: Visit 2 (top of stack)
    stack = [1, 3]
    visited = {0, 2}

    0(✓)-- 1
    |      |
    2(✓)-- 3

Step 3: Visit 3
    stack = [1]
    visited = {0, 2, 3}

    0(✓)-- 1
    |      |
    2(✓)-- 3(✓)

Step 4: Visit 1
    stack = []
    visited = {0, 1, 2, 3}

    0(✓)-- 1(✓)
    |      |
    2(✓)-- 3(✓)

Order: 0, 2, 3, 1

Recursive approach:
def dfs(node, visited):
    visited.add(node)
    print(node)

    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(neighbor, visited)

Tree visualization:
        0
       / \
      2   1
      |
      3

Time: O(V + E)
Space: O(V) for visited set + O(V) for stack
```

### 2. Breadth-First Search (BFS)

```
Graph:
    0 --- 1
    |     |
    2 --- 3

BFS from 0:

Queue-based traversal:
Start: queue = [0], visited = {0}

Level 0:
    0(✓)-- 1
    |      |
    2 ---- 3

    Visit 0, add neighbors
    queue = [1, 2]

Level 1:
    0(✓)-- 1(✓)
    |      |
    2(✓)-- 3

    Visit 1, add 3
    Visit 2 (already has 3)
    queue = [3]

Level 2:
    0(✓)-- 1(✓)
    |      |
    2(✓)-- 3(✓)

    Visit 3
    queue = []

Order: 0, 1, 2, 3 (level by level)

Level tree:
    0       Level 0
   / \
  1   2     Level 1
   \ /
    3       Level 2

Implementation:
from collections import deque

def bfs(start):
    queue = deque([start])
    visited = {start}

    while queue:
        node = queue.popleft()
        print(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

Time: O(V + E)
Space: O(V) for queue and visited

Use BFS when:
- Finding shortest path (unweighted)
- Level-order traversal
- Finding connected components
```

## Common Graph Algorithms

### 1. Find Connected Components

```
Graph:
    0 --- 1    4 --- 5
    |     |
    2 --- 3    6

Components: {0,1,2,3}, {4,5}, {6}

DFS approach:

def count_components(n, edges):
    # Build adjacency list
    graph = [[] for _ in range(n)]
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)

    visited = set()
    components = 0

    def dfs(node):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)

    for node in range(n):
        if node not in visited:
            dfs(node)
            components += 1

    return components

Visual execution:
Start: visited = {}, components = 0

Node 0: not visited
├─ DFS: visit {0,1,2,3}
└─ components = 1

Node 1: visited, skip
Node 2: visited, skip
Node 3: visited, skip

Node 4: not visited
├─ DFS: visit {4,5}
└─ components = 2

Node 5: visited, skip

Node 6: not visited
├─ DFS: visit {6}
└─ components = 3

Result: 3 components

Time: O(V + E)
Space: O(V)
```

### 2. Detect Cycle

```
Undirected Graph:
    0 --- 1
    |     |
    2 --- 3

Has cycle: 0→1→3→2→0

DFS approach:

def has_cycle(graph):
    visited = set()

    def dfs(node, parent):
        visited.add(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:
                # Visited and not parent = cycle!
                return True

        return False

    for node in graph:
        if node not in visited:
            if dfs(node, -1):
                return True

    return False

Visual execution:
Start at 0, parent = -1

    0(✓)-- 1
    |      |
    2 ---- 3

Go to 1, parent = 0
    0(✓)-- 1(✓)
    |      |
    2 ---- 3

Go to 3, parent = 1
    0(✓)-- 1(✓)
    |      |
    2 ---- 3(✓)

From 3, see 2 (unvisited), go to 2
    0(✓)-- 1(✓)
    |      |
    2(✓)-- 3(✓)

From 2, see 0 (visited, not parent)
CYCLE DETECTED! ✓

Directed Graph Cycle Detection:
Use "currently visiting" state

States: white (unvisited), gray (visiting), black (done)

def has_cycle_directed(graph):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * len(graph)

    def dfs(node):
        color[node] = GRAY

        for neighbor in graph[node]:
            if color[neighbor] == GRAY:
                return True  # Back edge = cycle
            if color[neighbor] == WHITE:
                if dfs(neighbor):
                    return True

        color[node] = BLACK
        return False

    for node in range(len(graph)):
        if color[node] == WHITE:
            if dfs(node):
                return True

    return False

Example:
    0 --> 1
    ↑     ↓
    3 <-- 2

DFS from 0:
0: GRAY → 1: GRAY → 2: GRAY → 3: GRAY
3 sees 0 (GRAY) → CYCLE! ✓

Time: O(V + E)
Space: O(V)
```

### 3. Topological Sort (DAG)

```
DAG:
    0 --> 1 --> 3
    ↓     ↓
    2 --> 4

Valid orderings:
- 0, 1, 2, 3, 4
- 0, 2, 1, 3, 4
- 0, 2, 1, 4, 3
etc.

DFS approach (reverse postorder):

def topological_sort(graph):
    visited = set()
    stack = []

    def dfs(node):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)
        stack.append(node)  # Add after visiting children

    for node in graph:
        if node not in visited:
            dfs(node)

    return stack[::-1]  # Reverse

Visual execution:
Start DFS from 0:

Visit 0
├─ Visit 1
│  ├─ Visit 3 (leaf)
│  │  └─ Add 3 to stack: [3]
│  ├─ Visit 4 (leaf)
│  │  └─ Add 4 to stack: [3, 4]
│  └─ Add 1 to stack: [3, 4, 1]
├─ Visit 2
│  ├─ 4 already visited
│  └─ Add 2 to stack: [3, 4, 1, 2]
└─ Add 0 to stack: [3, 4, 1, 2, 0]

Reverse: [0, 2, 1, 4, 3] ✓

Kahn's Algorithm (BFS approach):

def topological_sort_kahn(graph):
    # Calculate in-degrees
    in_degree = [0] * len(graph)
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1

    # Start with nodes having in-degree 0
    queue = deque([i for i in range(len(graph)) if in_degree[i] == 0])
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)

        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return result if len(result) == len(graph) else []  # Check for cycle

Visual:
    0 --> 1 --> 3
    ↓     ↓
    2 --> 4

In-degrees: [0, 1, 1, 1, 2]
Queue: [0]

Step 1: Process 0
    Remove edges: 0→1, 0→2
    In-degrees: [-, 0, 0, 1, 2]
    Queue: [1, 2]
    Result: [0]

Step 2: Process 1
    Remove edges: 1→3, 1→4
    In-degrees: [-, -, 0, 0, 1]
    Queue: [2, 3]
    Result: [0, 1]

Step 3: Process 2
    Remove edges: 2→4
    In-degrees: [-, -, -, 0, 0]
    Queue: [3, 4]
    Result: [0, 1, 2]

Step 4: Process 3, 4
    Result: [0, 1, 2, 3, 4]

Time: O(V + E)
Space: O(V)

Use cases:
- Task scheduling
- Build dependencies
- Course prerequisites
```

### 4. Shortest Path (Unweighted)

```
Graph:
    0 --- 1 --- 4
    |     |
    2 --- 3

Shortest path from 0 to 4:

BFS finds shortest path in unweighted graph:

def shortest_path(graph, start, end):
    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        node, path = queue.popleft()

        if node == end:
            return path

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None  # No path

Visual execution:
Start: queue = [(0, [0])], visited = {0}

Level 0:
    0(✓)-- 1 --- 4
    |      |
    2 ---- 3

Process 0:
    Add (1, [0,1]) and (2, [0,2])
    queue = [(1, [0,1]), (2, [0,2])]

Level 1:
    0(✓)-- 1(✓)-- 4
    |      |
    2(✓)-- 3

Process 1:
    Add (4, [0,1,4]) and (3, [0,1,3])
    queue = [(2, [0,2]), (4, [0,1,4]), (3, [0,1,3])]

Process 2:
    3 already in queue
    queue = [(4, [0,1,4]), (3, [0,1,3])]

Level 2:
    0(✓)-- 1(✓)-- 4(✓)
    |      |
    2(✓)-- 3(✓)

Process 4:
    node == end, return [0, 1, 4] ✓

Shortest path: 0 → 1 → 4 (length 2)

Distance only:
def shortest_distance(graph, start, end):
    queue = deque([(start, 0)])
    visited = {start}

    while queue:
        node, dist = queue.popleft()

        if node == end:
            return dist

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))

    return -1

Time: O(V + E)
Space: O(V)
```

### 5. Bipartite Check

```
Bipartite: Can color graph with 2 colors
(no adjacent nodes same color)

Graph:
    0 --- 1
    |     |
    2 --- 3

Bipartite! Color:
Red:  {0, 3}
Blue: {1, 2}

    R --- B
    |     |
    B --- R

Not Bipartite:
    0 --- 1
    |   / |
    | /   |
    2 --- 3

Triangle: cannot 2-color

BFS Approach:

def is_bipartite(graph):
    n = len(graph)
    color = [-1] * n

    for start in range(n):
        if color[start] != -1:
            continue

        queue = deque([start])
        color[start] = 0

        while queue:
            node = queue.popleft()

            for neighbor in graph[node]:
                if color[neighbor] == -1:
                    color[neighbor] = 1 - color[node]
                    queue.append(neighbor)
                elif color[neighbor] == color[node]:
                    return False

    return True

Visual:
    0 --- 1
    |     |
    2 --- 3

Start at 0, color = 0 (Red)
    0(R)-- 1
    |      |
    2 ---- 3

Color neighbors of 0 with 1 (Blue)
    0(R)-- 1(B)
    |      |
    2(B)-- 3

Color neighbors of 1 with 0 (Red)
    0(R)-- 1(B)
    |      |
    2(B)-- 3(R)

Color neighbors of 2 with 0 (Red)
    0(R)-- 1(B)
    |      |
    2(B)-- 3(R)

Check: 0 and 3 both Red, but not adjacent ✓
Result: Bipartite!

Non-bipartite example:
    0 --- 1
    |   /
    | /
    2

0: Red
1: Blue (neighbor of 0)
2: Blue (neighbor of 0)
But 1 and 2 are neighbors and both Blue! ✗

Time: O(V + E)
Space: O(V)
```

## Time and Space Complexity

```
Graph Representation:
                  Space      Edge Lookup   Find Neighbors
Adjacency Matrix  O(V²)      O(1)          O(V)
Adjacency List    O(V + E)   O(degree)     O(degree)
Edge List         O(E)       O(E)          O(E)

Graph Algorithms:
                      Time        Space
DFS                   O(V + E)    O(V)
BFS                   O(V + E)    O(V)
Connected Components  O(V + E)    O(V)
Cycle Detection       O(V + E)    O(V)
Topological Sort      O(V + E)    O(V)
Bipartite Check       O(V + E)    O(V)

Where:
V = number of vertices
E = number of edges
```

## Python Implementation

```python
from collections import deque, defaultdict

# Graph representation
class Graph:
    def __init__(self, n, directed=False):
        self.n = n
        self.directed = directed
        self.adj_list = [[] for _ in range(n)]

    def add_edge(self, u, v, weight=1):
        self.adj_list[u].append((v, weight))
        if not self.directed:
            self.adj_list[v].append((u, weight))

    def get_neighbors(self, u):
        return self.adj_list[u]


# DFS - Recursive
def dfs_recursive(graph, start):
    visited = set()
    result = []

    def dfs(node):
        visited.add(node)
        result.append(node)

        for neighbor, _ in graph.get_neighbors(node):
            if neighbor not in visited:
                dfs(neighbor)

    dfs(start)
    return result


# DFS - Iterative
def dfs_iterative(graph, start):
    stack = [start]
    visited = set([start])
    result = []

    while stack:
        node = stack.pop()
        result.append(node)

        for neighbor, _ in graph.get_neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)

    return result


# BFS
def bfs(graph, start):
    queue = deque([start])
    visited = set([start])
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)

        for neighbor, _ in graph.get_neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return result


# Connected Components
def count_components(n, edges):
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = set()

    def dfs(node):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)

    count = 0
    for node in range(n):
        if node not in visited:
            dfs(node)
            count += 1

    return count


# Cycle Detection - Undirected
def has_cycle_undirected(graph):
    visited = set()

    def dfs(node, parent):
        visited.add(node)

        for neighbor, _ in graph.get_neighbors(node):
            if neighbor not in visited:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:
                return True

        return False

    for node in range(graph.n):
        if node not in visited:
            if dfs(node, -1):
                return True

    return False


# Cycle Detection - Directed
def has_cycle_directed(graph):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * graph.n

    def dfs(node):
        color[node] = GRAY

        for neighbor, _ in graph.get_neighbors(node):
            if color[neighbor] == GRAY:
                return True
            if color[neighbor] == WHITE and dfs(neighbor):
                return True

        color[node] = BLACK
        return False

    for node in range(graph.n):
        if color[node] == WHITE:
            if dfs(node):
                return True

    return False


# Topological Sort - DFS
def topological_sort_dfs(graph):
    visited = set()
    stack = []

    def dfs(node):
        visited.add(node)
        for neighbor, _ in graph.get_neighbors(node):
            if neighbor not in visited:
                dfs(neighbor)
        stack.append(node)

    for node in range(graph.n):
        if node not in visited:
            dfs(node)

    return stack[::-1]


# Topological Sort - Kahn's
def topological_sort_kahn(graph):
    in_degree = [0] * graph.n

    for node in range(graph.n):
        for neighbor, _ in graph.get_neighbors(node):
            in_degree[neighbor] += 1

    queue = deque([i for i in range(graph.n) if in_degree[i] == 0])
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)

        for neighbor, _ in graph.get_neighbors(node):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return result if len(result) == graph.n else []


# Shortest Path - Unweighted
def shortest_path_unweighted(graph, start, end):
    queue = deque([(start, [start])])
    visited = set([start])

    while queue:
        node, path = queue.popleft()

        if node == end:
            return path

        for neighbor, _ in graph.get_neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None


# Bipartite Check
def is_bipartite(graph):
    color = [-1] * graph.n

    for start in range(graph.n):
        if color[start] != -1:
            continue

        queue = deque([start])
        color[start] = 0

        while queue:
            node = queue.popleft()

            for neighbor, _ in graph.get_neighbors(node):
                if color[neighbor] == -1:
                    color[neighbor] = 1 - color[node]
                    queue.append(neighbor)
                elif color[neighbor] == color[node]:
                    return False

    return True


# Clone Graph
def clone_graph(node):
    if not node:
        return None

    clones = {}

    def dfs(node):
        if node in clones:
            return clones[node]

        clone = Node(node.val)
        clones[node] = clone

        for neighbor in node.neighbors:
            clone.neighbors.append(dfs(neighbor))

        return clone

    return dfs(node)


# All Paths from Source to Target
def all_paths(graph, start, end):
    result = []

    def dfs(node, path):
        if node == end:
            result.append(path[:])
            return

        for neighbor, _ in graph.get_neighbors(node):
            path.append(neighbor)
            dfs(neighbor, path)
            path.pop()

    dfs(start, [start])
    return result
```

## Key Takeaways

1. **Structure**: Vertices connected by edges
2. **Types**:
   - Directed/Undirected
   - Weighted/Unweighted
   - Cyclic/Acyclic (DAG)
   - Connected/Disconnected

3. **Representations**:
   - Adjacency Matrix: O(V²) space, O(1) lookup
   - Adjacency List: O(V+E) space, best for sparse
   - Edge List: Simple, good for edge operations

4. **Traversal**:
   - DFS: Stack-based, explores deep
   - BFS: Queue-based, explores level-by-level

5. **Common Algorithms**:
   - Connected components
   - Cycle detection
   - Topological sort (DAG)
   - Shortest path (unweighted)
   - Bipartite check

6. **Time Complexity**: Most algorithms O(V + E)
7. **Space Complexity**: O(V) for visited/queue/stack

8. **When to Use**:
   - Modeling relationships
   - Network analysis
   - Pathfinding
   - Dependency resolution
   - Social networks

9. **DFS vs BFS**:
   - DFS: Path finding, cycle detection, topological sort
   - BFS: Shortest path, level-order, minimum steps
