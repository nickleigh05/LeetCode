# 12. Advanced Graphs — Practice

The Roadmap follows a curated list called the NeetCode 150 for practice problems. If you want more or fewer problems, check the other lists in [lists/](../../lists/).

[← Back to the lesson](../learning/13-advanced-graphs.md) · [🗺 Roadmap](../../roadmap.md)

---

### 332. Reconstruct Itinerary — Hard
[LeetCode](https://leetcode.com/problems/reconstruct-itinerary/)  
Solution: not yet solved in this repo.

Given airline tickets, reconstruct the itinerary that uses all tickets in order, starting from "JFK", choosing the lexicographically smallest route when there's a choice. Why does this become an Eulerian-path problem, and why must you add nodes to the result *after* exhausting their edges (post-order)?

<details>
<summary>Hint</summary>

Build an adjacency list sorted so the smallest destinations are tried first, then run [DFS](../algorithms/dfs.md), consuming (removing) each edge as you use it. Append to the result in post-order (after recursion returns) — this "Hierholzer's algorithm" trick handles dead ends correctly by placing them last.
</details>

<details>
<summary>Solution</summary>

```python
from collections import defaultdict

class Solution:
    def findItinerary(self, tickets: List[List[str]]) -> List[str]:

        graph = defaultdict(list)
        for src, dst in sorted(tickets, reverse=True):   # reverse-sorted so .pop() gives smallest
            graph[src].append(dst)

        route = []

        def dfs(airport):
            while graph[airport]:
                dfs(graph[airport].pop())
            route.append(airport)

        dfs("JFK")
        return route[::-1]
```

Building blocks: [defaultdict](../syntax/defaultdict.md) · [sorting-key](../syntax/sorting-key.md) (`reverse=True`) · [recursion-basics](../syntax/recursion-basics.md) · [list-slicing](../syntax/list-slicing.md) (`[::-1]`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(E log E)** — dominated by sorting the tickets; the DFS itself is O(E).
**Space: O(E)** — the adjacency list holds every ticket.
</details>

---

### 1584. Min Cost to Connect All Points — Medium
[LeetCode](https://leetcode.com/problems/min-cost-to-connect-all-points/)  
Solution: not yet solved in this repo.

Connect all points with edges weighted by Manhattan distance, minimizing total edge cost. Why does greedily adding the cheapest edge that connects a *new* point (Prim's algorithm) guarantee a minimum spanning tree?

<details>
<summary>Hint</summary>

Prim's algorithm: grow a tree from any point, always adding the cheapest edge that connects an unvisited point, using a min-[heap](../data-structures/heap.md) of `(cost, point)` to always pick that edge efficiently.
</details>

<details>
<summary>Solution</summary>

```python
import heapq

class Solution:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:

        n = len(points)
        visited = set()
        min_heap = [(0, 0)]   # (cost, point index)
        total = 0

        while len(visited) < n:
            cost, i = heapq.heappop(min_heap)
            if i in visited:
                continue
            visited.add(i)
            total += cost

            for j in range(n):
                if j not in visited:
                    dist = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])
                    heapq.heappush(min_heap, (dist, j))

        return total
```

Building blocks: [heap](../data-structures/heap.md) · [set-basics](../syntax/set-basics.md) · [while-loop](../syntax/while-loop.md) · [comparison-operators](../syntax/comparison-operators.md) (`abs()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n² log n)** — n points, each pushing up to n edges onto the heap.
**Space: O(n²)** — the heap can hold up to n² edges in the worst case.
</details>

---

### 743. Network Delay Time — Medium
[LeetCode](https://leetcode.com/problems/network-delay-time/)  
Solution: not yet solved in this repo.

Given a weighted directed graph, find the time for a signal from node `k` to reach every node (or -1 if impossible). Why is this exactly what Dijkstra's algorithm computes?

<details>
<summary>Hint</summary>

Run [Dijkstra's algorithm](../algorithms/dijkstra.md) from `k`: always expand the closest not-yet-finalized node using a min-[heap](../data-structures/heap.md) of `(time, node)`, relaxing neighbor distances as you go.
</details>

<details>
<summary>Solution</summary>

```python
import heapq
from collections import defaultdict

class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:

        graph = defaultdict(list)
        for u, v, w in times:
            graph[u].append((v, w))

        dist = {}
        min_heap = [(0, k)]   # (time so far, node)

        while min_heap:
            time, node = heapq.heappop(min_heap)
            if node in dist:
                continue
            dist[node] = time

            for neighbor, weight in graph[node]:
                if neighbor not in dist:
                    heapq.heappush(min_heap, (time + weight, neighbor))

        if len(dist) != n:
            return -1
        return max(dist.values())
```

Building blocks: [defaultdict](../syntax/defaultdict.md) · [heap](../data-structures/heap.md) · [while-loop](../syntax/while-loop.md) · [dict-methods](../syntax/dict-methods.md) (`.values()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(E log V)** — each edge relaxation involves a heap push/pop.
**Space: O(V + E)** — the adjacency list, distance map, and heap.
</details>

---

### 778. Swim in Rising Water — Hard
[LeetCode](https://leetcode.com/problems/swim-in-rising-water/)  
Solution: not yet solved in this repo.

Water rises over time; find the minimum time to swim from top-left to bottom-right (you can only move to cells whose elevation is `<=` current time). Why does always expanding the *lowest-elevation* reachable cell next (a min-heap) find the minimum time needed?

<details>
<summary>Hint</summary>

This is Dijkstra-flavored: use a min-[heap](../data-structures/heap.md) keyed by "max elevation encountered so far on this path." Always expand the cell that keeps that max the smallest; the answer is that max when you reach the bottom-right cell.
</details>

<details>
<summary>Solution</summary>

```python
import heapq

class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:

        n = len(grid)
        visited = set()
        min_heap = [(grid[0][0], 0, 0)]   # (max elevation on path so far, row, col)

        while min_heap:
            time, row, col = heapq.heappop(min_heap)
            if (row, col) in visited:
                continue
            visited.add((row, col))

            if row == n - 1 and col == n - 1:
                return time

            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                r = row + dr
                c = col + dc
                if 0 <= r < n and 0 <= c < n and (r, c) not in visited:
                    heapq.heappush(min_heap, (max(time, grid[r][c]), r, c))
```

Building blocks: [heap](../data-structures/heap.md) · [set-basics](../syntax/set-basics.md) · [while-loop](../syntax/while-loop.md) · [comparison-operators](../syntax/comparison-operators.md) (`max()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n² log n)** — n² cells, each heap operation O(log n²) = O(log n).
**Space: O(n²)** — the visited set and heap.
</details>

---

### 269. Alien Dictionary — Hard
[LeetCode](https://leetcode.com/problems/alien-dictionary/)  
Solution: not yet solved in this repo.

Given words sorted according to an unknown alien alphabet, derive a valid character ordering. Why does comparing each pair of adjacent words letter-by-letter give you edges for a character-ordering graph, and why does a topological sort turn that into an alphabet?

<details>
<summary>Hint</summary>

For each pair of adjacent words, find the first differing character — that gives an edge `earlier_char -> later_char`. Build this graph over all 26 possible letters, then run a [topological sort](../algorithms/topological-sort.md); a cycle (or word being a prefix of an earlier word incorrectly) means no valid ordering exists.
</details>

<details>
<summary>Solution</summary>

```python
from collections import deque

class Solution:
    def alienOrder(self, words: List[str]) -> str:

        graph = {char: set() for word in words for char in word}

        for w1, w2 in zip(words, words[1:]):
            min_len = min(len(w1), len(w2))
            if w1[:min_len] == w2[:min_len] and len(w1) > len(w2):
                return ""
            for c1, c2 in zip(w1, w2):
                if c1 != c2:
                    graph[c1].add(c2)
                    break

        indegree = {char: 0 for char in graph}
        for char in graph:
            for neighbor in graph[char]:
                indegree[neighbor] += 1

        queue = deque([char for char in graph if indegree[char] == 0])
        order = []

        while queue:
            char = queue.popleft()
            order.append(char)
            for neighbor in graph[char]:
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    queue.append(neighbor)

        return "".join(order) if len(order) == len(graph) else ""
```

Building blocks: [dict-comprehension](../syntax/dict-comprehension.md) · [zip-function](../syntax/zip-function.md) · [deque](../data-structures/deque.md) · [while-loop](../syntax/while-loop.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(C)** — C is the total length of all words (building edges), plus O(V + E) for the topological sort over the alphabet.
**Space: O(1)** — bounded by 26 letters for the graph and indegree map.
</details>

---

### 787. Cheapest Flights Within K Stops — Medium
[LeetCode](https://leetcode.com/problems/cheapest-flights-within-k-stops/)  
Solution: not yet solved in this repo.

Find the cheapest price from `src` to `dst` using at most `k` stops. Why does plain Dijkstra fail here, and why does Bellman-Ford (relaxing all edges exactly `k+1` times) respect the stop limit correctly?

<details>
<summary>Hint</summary>

Dijkstra doesn't track *how many edges* were used to reach the cheapest price, so it can miss valid cheaper routes constrained by stops. Instead run a Bellman-Ford-style relaxation for exactly `k + 1` rounds, using a *snapshot* of prices from the previous round each time so effects don't leak within a round.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:

        prices = [float("inf")] * n
        prices[src] = 0

        for _ in range(k + 1):
            tmp_prices = prices[:]   # snapshot so updates don't leak within a round

            for u, v, w in flights:
                if prices[u] != float("inf") and prices[u] + w < tmp_prices[v]:
                    tmp_prices[v] = prices[u] + w

            prices = tmp_prices

        return prices[dst] if prices[dst] != float("inf") else -1
```

Building blocks: [list-slicing](../syntax/list-slicing.md) (snapshot copy) · [for-loop](../syntax/for-loop.md) · [int-float-basics](../syntax/int-float-basics.md) (`float("inf")`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(k · E)** — k+1 rounds, each relaxing every edge once.
**Space: O(n)** — the prices array (and its snapshot).
</details>
