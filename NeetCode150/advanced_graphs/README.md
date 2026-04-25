# Advanced Graphs

## 12. Advanced Graphs (6 problems)

| Problem # | Difficulty | Problem Name | LeetCode Link |
|-----------|------------|--------------|---------------|
| 332 | Hard | Reconstruct Itinerary | [Link](https://leetcode.com/problems/reconstruct-itinerary/) |
| 1584 | Medium | Min Cost to Connect All Points | [Link](https://leetcode.com/problems/min-cost-to-connect-all-points/) |
| 743 | Medium | Network Delay Time | [Link](https://leetcode.com/problems/network-delay-time/) |
| 778 | Hard | Swim in Rising Water | [Link](https://leetcode.com/problems/swim-in-rising-water/) |
| 269 | Hard | Alien Dictionary | [Link](https://leetcode.com/problems/alien-dictionary/) |
| 787 | Medium | Cheapest Flights Within K Stops | [Link](https://leetcode.com/problems/cheapest-flights-within-k-stops/) |

---

## Data Structures

### Weighted Graph (Adjacency List)
Each edge also carries a weight. `graph[u]` is a list of `(weight, v)` tuples. Used in Dijkstra's and Bellman-Ford.

### Min-Heap (Priority Queue)
Used in Dijkstra's algorithm to always process the unvisited node with the smallest current distance. Each heap entry is `(distance, node)`.

### Union-Find
Used in Kruskal's MST algorithm to efficiently check if adding an edge would create a cycle (i.e. if both endpoints are already in the same component).

---

## Core Patterns

### Dijkstra's Algorithm (Shortest Path, Non-Negative Weights)
Start with distance 0 for the source and infinity for all others. Use a min-heap. Pop the node with the smallest known distance, explore its neighbors, and update their distances if a shorter path is found. Each node is processed at most once. O((V + E) log V). Used in Network Delay Time, Swim in Rising Water.

### Bellman-Ford (Shortest Path, Negative Weights / K Stops)
Relax all edges V-1 times. Each iteration guarantees shortest paths using at most `i` edges. Using exactly K+1 rounds gives shortest paths with at most K+1 edges (K stops). O(V * E). Used in Cheapest Flights Within K Stops.

### Prim's Algorithm (Minimum Spanning Tree)
Start from any node. Use a min-heap of `(cost, node)`. Always add the cheapest edge that connects a new node to the already-built tree. Used in Min Cost to Connect All Points.

### Kruskal's Algorithm (Minimum Spanning Tree)
Sort all edges by weight. Use Union-Find to add edges greedily — skip any edge that would create a cycle. Stop when V-1 edges are added.

### Hierholzer's Algorithm (Eulerian Path)
An Eulerian path visits every edge exactly once. DFS from the start node, but only add a node to the result path after all its outgoing edges are exhausted. Reverse the result at the end. Used in Reconstruct Itinerary — lexicographically smallest path means use a min-heap for neighbor ordering.

### Topological Sort (Alien Dictionary)
Extract character ordering constraints from adjacent words (if `word[i]` comes before `word[i+1]`, the first differing character gives an edge). Build a graph and topological sort it. If a cycle exists, return "" (invalid).
