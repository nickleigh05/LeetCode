# Graphs

## 11. Graphs (13 problems)

| Problem # | Difficulty | Problem Name | LeetCode Link |
|-----------|------------|--------------|---------------|
| 200 | Medium | Number of Islands | [Link](https://leetcode.com/problems/number-of-islands/) |
| 133 | Medium | Clone Graph | [Link](https://leetcode.com/problems/clone-graph/) |
| 695 | Medium | Max Area of Island | [Link](https://leetcode.com/problems/max-area-of-island/) |
| 417 | Medium | Pacific Atlantic Water Flow | [Link](https://leetcode.com/problems/pacific-atlantic-water-flow/) |
| 130 | Medium | Surrounded Regions | [Link](https://leetcode.com/problems/surrounded-regions/) |
| 994 | Medium | Rotting Oranges | [Link](https://leetcode.com/problems/rotting-oranges/) |
| 286 | Medium | Walls and Gates | [Link](https://leetcode.com/problems/walls-and-gates/) |
| 207 | Medium | Course Schedule | [Link](https://leetcode.com/problems/course-schedule/) |
| 210 | Medium | Course Schedule II | [Link](https://leetcode.com/problems/course-schedule-ii/) |
| 684 | Medium | Redundant Connection | [Link](https://leetcode.com/problems/redundant-connection/) |
| 323 | Medium | Number of Connected Components | [Link](https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/) |
| 261 | Medium | Graph Valid Tree | [Link](https://leetcode.com/problems/graph-valid-tree/) |
| 127 | Hard | Word Ladder | [Link](https://leetcode.com/problems/word-ladder/) |

---

## Data Structures

### Adjacency List
A hash map (or array) where `graph[node]` is a list of its neighbors. Most efficient for sparse graphs. Built from an edge list in O(V + E).

### Visited Set
A set of already-visited nodes. Prevents revisiting nodes and infinite loops in cyclic graphs. Can also be a boolean array if nodes are integers.

### Queue (for BFS)
A `deque` used to process nodes level by level. BFS explores all neighbors at the current distance before going deeper — naturally finds shortest paths in unweighted graphs.

### Union-Find (Disjoint Set Union)
Tracks which nodes belong to the same connected component. `find(x)` returns the root of x's component. `union(x, y)` merges two components. With path compression and union by rank, both operations are nearly O(1). Used in Redundant Connection, Number of Connected Components.

---

## Core Patterns

### DFS on Grid
Treat a 2D grid as a graph — each cell connects to its 4 neighbors. DFS from a starting cell and mark visited cells. Count connected components or accumulate area. Used in Number of Islands, Max Area of Island.

### Multi-Source BFS
Enqueue all starting nodes at once (not just one). BFS naturally propagates outward in layers, so all sources expand simultaneously — gives the shortest distance from any source to any cell. Used in Rotting Oranges, Walls and Gates.

### Reverse BFS / DFS (Boundary to Interior)
Instead of going from interior to boundary (hard to track what's "escaped"), go from the boundary inward. Mark everything reachable from the boundary as safe, then flip the remaining cells. Used in Pacific Atlantic Water Flow and Surrounded Regions.

### Cycle Detection (DFS with 3 colors)
Track node state: unvisited (0), in current DFS path (1), fully processed (2). If you reach a node that's currently in the path (state 1), there's a cycle. Used in Course Schedule.

### Topological Sort (Kahn's Algorithm / BFS)
Compute in-degrees for all nodes. Add nodes with in-degree 0 to a queue. Pop a node, decrement its neighbors' in-degrees, and enqueue any that hit 0. If all nodes are processed, the order is valid. If any node is never processed, there's a cycle. Used in Course Schedule II.

### Clone Graph (DFS + Hash Map)
Use a hash map from original node → clone. When you first visit a node, create its clone and add it to the map. Then recursively clone all neighbors. The map prevents re-cloning already-visited nodes.

### BFS Shortest Path (Word Ladder)
Build a graph implicitly — two words are connected if they differ by one letter. BFS from the start word to the end word. The first time you reach the end word, the BFS depth is the shortest path length.
