# 11. Graphs — Practice

The Roadmap follows a curated list called the NeetCode 150 for practice problems. If you want more or fewer problems, check the other lists in [lists/](../../lists/).

← Back to the lessons: [Graphs](../learning/11-graphs.md) / [Union Find](../learning/12-union-find.md) · [🗺 Roadmap](../../roadmap.md)

---

### 200. Number of Islands — Medium
[LeetCode](https://leetcode.com/problems/number-of-islands/)  
[Solution file (no hints)](../../problems/0001-0499/200.py)

Count the number of islands (connected groups of `"1"`s) in a grid. Why does sinking (marking visited) every land cell you touch during one island's exploration guarantee you never count it twice?

<details>
<summary>Hint</summary>

Treat the grid as an implicit [graph](../data-structures/graph.md). Scan every cell; whenever you find unvisited land, run [DFS](../algorithms/dfs.md) (or [BFS](../algorithms/bfs.md)) to mark the whole connected island visited, and count that as one island.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:

        rows = len(grid)
        cols = len(grid[0])
        visited = set()
        islands = 0

        def dfs(row, col):
            if row < 0 or row >= rows or col < 0 or col >= cols:
                return
            if grid[row][col] == "0" or (row, col) in visited:
                return

            visited.add((row, col))
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                dfs(row + dr, col + dc)

        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == "1" and (row, col) not in visited:
                    dfs(row, col)
                    islands += 1

        return islands
```

Building blocks: [set-basics](../syntax/set-basics.md) · [nested-lists](../syntax/nested-lists.md) · [recursion-basics](../syntax/recursion-basics.md) · [for-loop](../syntax/for-loop.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(rows · cols)** — every cell is visited a constant number of times.
**Space: O(rows · cols)** — the visited set (and recursion stack) in the worst case.
</details>

---

### 133. Clone Graph — Medium
[LeetCode](https://leetcode.com/problems/clone-graph/)  
[Solution file (no hints)](../../problems/0001-0499/133.py)

Deep-copy a connected undirected [graph](../data-structures/graph.md). Since the graph may have cycles, how does a hashmap from original node -> cloned node prevent infinite recursion?

<details>
<summary>Hint</summary>

Run [DFS](../algorithms/dfs.md) from the given node; before recursing into a neighbor, check a `old -> clone` [hashmap](../data-structures/hashmap.md) — if already cloned, reuse that clone instead of recursing again (this is what breaks cycles).
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def cloneGraph(self, node: Optional[Node]) -> Optional[Node]:

        if node is None:
            return None

        old_to_new = {}

        def dfs(current_node):
            if current_node in old_to_new:
                return old_to_new[current_node]

            copy_node = Node(current_node.val)
            old_to_new[current_node] = copy_node

            for neighbor in current_node.neighbors:
                copy_node.neighbors.append(dfs(neighbor))

            return copy_node

        return dfs(node)
```

Building blocks: [dict-basics](../syntax/dict-basics.md) · [recursion-basics](../syntax/recursion-basics.md) · [for-loop](../syntax/for-loop.md) · [identity-operators](../syntax/identity-operators.md) (`is None`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(V + E)** — every node and edge is visited once.
**Space: O(V)** — the hashmap holds every original->clone mapping.
</details>

---

### 695. Max Area of Island — Medium
[LeetCode](https://leetcode.com/problems/max-area-of-island/)  
Solution: not yet solved in this repo.

Find the largest island's area in a grid of 0s and 1s. How does the sink-and-count DFS from [200](#200-number-of-islands--medium) change to also return a size?

<details>
<summary>Hint</summary>

Same sinking [DFS](../algorithms/dfs.md) as [200](#200-number-of-islands--medium), but instead of just marking cells visited, have it return `1 + sum of neighbor areas` so each island's total area is computed directly.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:

        rows = len(grid)
        cols = len(grid[0])
        visited = set()

        def dfs(row, col):
            if row < 0 or row >= rows or col < 0 or col >= cols:
                return 0
            if grid[row][col] == 0 or (row, col) in visited:
                return 0

            visited.add((row, col))
            area = 1
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                area += dfs(row + dr, col + dc)
            return area

        best = 0
        for row in range(rows):
            for col in range(cols):
                best = max(best, dfs(row, col))
        return best
```

Building blocks: [set-basics](../syntax/set-basics.md) · [recursion-basics](../syntax/recursion-basics.md) · [comparison-operators](../syntax/comparison-operators.md) (`max()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(rows · cols)** — every cell is visited a constant number of times.
**Space: O(rows · cols)** — the visited set in the worst case.
</details>

---

### 417. Pacific Atlantic Water Flow — Medium
[LeetCode](https://leetcode.com/problems/pacific-atlantic-water-flow/)  
Solution: not yet solved in this repo.

Find cells where water can flow to both the Pacific and Atlantic oceans (flow only goes to equal-or-lower height). Why is it far cheaper to flow *backward* from each ocean's border inward than to test every cell's forward path?

<details>
<summary>Hint</summary>

Run [DFS](../algorithms/dfs.md) from every Pacific-border cell and every Atlantic-border cell separately, moving to a neighbor only if it's equal or *higher* (reverse of the real flow direction). The answer is every cell reachable from both.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:

        rows = len(heights)
        cols = len(heights[0])
        pacific = set()
        atlantic = set()

        def dfs(row, col, visited, prev_height):
            if row < 0 or row >= rows or col < 0 or col >= cols:
                return
            if (row, col) in visited or heights[row][col] < prev_height:
                return

            visited.add((row, col))
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                dfs(row + dr, col + dc, visited, heights[row][col])

        for col in range(cols):
            dfs(0, col, pacific, heights[0][col])
            dfs(rows - 1, col, atlantic, heights[rows - 1][col])

        for row in range(rows):
            dfs(row, 0, pacific, heights[row][0])
            dfs(row, cols - 1, atlantic, heights[row][cols - 1])

        result = []
        for row in range(rows):
            for col in range(cols):
                if (row, col) in pacific and (row, col) in atlantic:
                    result.append([row, col])
        return result
```

Building blocks: [set-basics](../syntax/set-basics.md) · [recursion-basics](../syntax/recursion-basics.md) · [for-loop](../syntax/for-loop.md) · [membership-operators](../syntax/membership-operators.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(rows · cols)** — each DFS visits each cell a constant number of times.
**Space: O(rows · cols)** — the two visited sets.
</details>

---

### 130. Surrounded Regions — Medium
[LeetCode](https://leetcode.com/problems/surrounded-regions/)  
Solution: not yet solved in this repo.

Flip every `"O"` surrounded by `"X"`s to `"X"`, except regions connected to the border. Why is it easier to mark the *safe* (border-connected) regions first, then flip everything else?

<details>
<summary>Hint</summary>

Run [DFS](../algorithms/dfs.md) from every border `"O"`, temporarily marking reachable cells safe (e.g. `"T"`). Anything still `"O"` afterward is fully surrounded and gets flipped to `"X"`; the marked-safe cells flip back to `"O"`.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def solve(self, board: List[List[str]]) -> None:

        rows = len(board)
        cols = len(board[0])

        def dfs(row, col):
            if row < 0 or row >= rows or col < 0 or col >= cols:
                return
            if board[row][col] != "O":
                return

            board[row][col] = "T"   # temporary mark: connected to the border, safe
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                dfs(row + dr, col + dc)

        for row in range(rows):
            dfs(row, 0)
            dfs(row, cols - 1)
        for col in range(cols):
            dfs(0, col)
            dfs(rows - 1, col)

        for row in range(rows):
            for col in range(cols):
                if board[row][col] == "O":
                    board[row][col] = "X"
                elif board[row][col] == "T":
                    board[row][col] = "O"
```

Building blocks: [nested-lists](../syntax/nested-lists.md) · [recursion-basics](../syntax/recursion-basics.md) · [for-loop](../syntax/for-loop.md) · [elif-else](../syntax/elif-else.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(rows · cols)** — every cell is visited a constant number of times.
**Space: O(rows · cols)** — recursion stack in the worst case.
</details>

---

### 994. Rotting Oranges — Medium
[LeetCode](https://leetcode.com/problems/rotting-oranges/)  
Solution: not yet solved in this repo.

Each minute, rotten oranges rot their fresh neighbors. Find the minutes until no fresh orange remains. Why does starting BFS from *all* initially rotten oranges at once correctly simulate simultaneous spread, minute by minute?

<details>
<summary>Hint</summary>

Multi-source [BFS](../algorithms/bfs.md): seed a [queue](../data-structures/queue.md) with every initially rotten orange, then process level by level (each level = one minute), rotting fresh neighbors and counting minutes until the queue empties.
</details>

<details>
<summary>Solution</summary>

```python
from collections import deque

class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:

        rows = len(grid)
        cols = len(grid[0])
        queue = deque()
        fresh = 0

        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == 2:
                    queue.append((row, col))
                elif grid[row][col] == 1:
                    fresh += 1

        minutes = 0
        while queue and fresh > 0:
            for _ in range(len(queue)):
                row, col = queue.popleft()

                for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    r = row + dr
                    c = col + dc
                    if 0 <= r < rows and 0 <= c < cols and grid[r][c] == 1:
                        grid[r][c] = 2
                        fresh -= 1
                        queue.append((r, c))
            minutes += 1

        return minutes if fresh == 0 else -1
```

Building blocks: [deque](../data-structures/deque.md) · [while-loop](../syntax/while-loop.md) · [for-loop](../syntax/for-loop.md) · [if-return](../syntax/if-return.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(rows · cols)** — each cell enters the queue at most once.
**Space: O(rows · cols)** — the queue in the worst case.
</details>

---

### 286. Walls and Gates — Medium
[LeetCode](https://leetcode.com/problems/walls-and-gates/)  
Solution: not yet solved in this repo.

Fill each empty room with the distance to its nearest gate. Why does starting a multi-source BFS from every gate simultaneously guarantee each room gets its *shortest* distance?

<details>
<summary>Hint</summary>

Same shape as [994](#994-rotting-oranges--medium): multi-source [BFS](../algorithms/bfs.md) from every gate at once using a [queue](../data-structures/queue.md), so the first time a room is reached is guaranteed to be via the shortest path.
</details>

<details>
<summary>Solution</summary>

```python
from collections import deque

class Solution:
    def wallsAndGates(self, rooms: List[List[int]]) -> None:

        rows = len(rooms)
        cols = len(rooms[0])
        queue = deque()

        for row in range(rows):
            for col in range(cols):
                if rooms[row][col] == 0:
                    queue.append((row, col))

        empty = 2147483647

        while queue:
            row, col = queue.popleft()

            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                r = row + dr
                c = col + dc
                if 0 <= r < rows and 0 <= c < cols and rooms[r][c] == empty:
                    rooms[r][c] = rooms[row][col] + 1
                    queue.append((r, c))
```

Building blocks: [deque](../data-structures/deque.md) · [while-loop](../syntax/while-loop.md) · [for-loop](../syntax/for-loop.md) · [chained-comparisons](../syntax/chained-comparisons.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(rows · cols)** — each cell enters the queue at most once.
**Space: O(rows · cols)** — the queue in the worst case.
</details>

---

### 207. Course Schedule — Medium
[LeetCode](https://leetcode.com/problems/course-schedule/)  
[Solution file (no hints)](../../problems/0001-0499/207.py)

Given prerequisite pairs, determine if it's possible to finish all courses (i.e., no cycle). Why does a cycle in the prerequisite graph make finishing all courses impossible?

<details>
<summary>Hint</summary>

Build an adjacency list, then either run cycle detection with a "visiting/visited" DFS state, or compute a [topological sort](../algorithms/topological-sort.md) (Kahn's algorithm) — if it can't include every course, a cycle exists.
</details>

<details>
<summary>Solution</summary>

```python
from collections import deque

class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:

        graph = [[] for _ in range(numCourses)]
        indegree = [0] * numCourses

        for course, prereq in prerequisites:
            graph[prereq].append(course)
            indegree[course] += 1

        queue = deque()
        for i in range(numCourses):
            if indegree[i] == 0:
                queue.append(i)

        visited_count = 0
        while queue:
            node = queue.popleft()
            visited_count += 1
            for neighbor in graph[node]:
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    queue.append(neighbor)

        return visited_count == numCourses
```

Building blocks: [deque](../data-structures/deque.md) · [from-import](../syntax/from-import.md) · [list-comprehension](../syntax/list-comprehension.md) (`[[] for _ in ...]`) · [while-loop](../syntax/while-loop.md) · [for-loop](../syntax/for-loop.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(V + E)** — every course and prerequisite edge is processed once.
**Space: O(V + E)** — the adjacency list and indegree array.
</details>

---

### 210. Course Schedule II — Medium
[LeetCode](https://leetcode.com/problems/course-schedule-ii/)  
Solution: not yet solved in this repo.

Same setup as [207](#207-course-schedule--medium), but return a valid course order (or empty if impossible). What does the order in which Kahn's algorithm dequeues nodes directly give you?

<details>
<summary>Hint</summary>

Run the same [topological sort](../algorithms/topological-sort.md) as [207](#207-course-schedule--medium), but record the dequeue order — that order *is* a valid course schedule (or return `[]` if not every course got visited).
</details>

<details>
<summary>Solution</summary>

```python
from collections import deque

class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:

        graph = [[] for _ in range(numCourses)]
        indegree = [0] * numCourses

        for course, prereq in prerequisites:
            graph[prereq].append(course)
            indegree[course] += 1

        queue = deque()
        for i in range(numCourses):
            if indegree[i] == 0:
                queue.append(i)

        order = []
        while queue:
            node = queue.popleft()
            order.append(node)
            for neighbor in graph[node]:
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    queue.append(neighbor)

        return order if len(order) == numCourses else []
```

Building blocks: [deque](../data-structures/deque.md) · [from-import](../syntax/from-import.md) · [list-comprehension](../syntax/list-comprehension.md) (`[[] for _ in ...]`) · [while-loop](../syntax/while-loop.md) · [ternary-expression](../syntax/ternary-expression.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(V + E)** — every course and prerequisite edge is processed once.
**Space: O(V + E)** — the adjacency list and indegree array.
</details>

---

### 684. Redundant Connection — Medium
[LeetCode](https://leetcode.com/problems/redundant-connection/)  
Solution: not yet solved in this repo.

Given a tree with one extra edge added (creating a cycle), find that redundant edge. Why does trying to union the two endpoints of each edge, in order, immediately reveal the edge that closes a cycle?

<details>
<summary>Hint</summary>

Process edges in order with [union-find](../data-structures/union-find.md). For each edge, if its two endpoints are already connected (same root), that edge is the one creating the cycle — return it immediately.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:

        parent = list(range(len(edges) + 1))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]   # path compression
                x = parent[x]
            return x

        def union(x, y):
            root_x = find(x)
            root_y = find(y)
            if root_x == root_y:
                return False
            parent[root_x] = root_y
            return True

        for a, b in edges:
            if not union(a, b):
                return [a, b]
```

Building blocks: [union-find](../data-structures/union-find.md) · [while-loop](../syntax/while-loop.md) · [for-loop](../syntax/for-loop.md) · [if-return](../syntax/if-return.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n · α(n))** — n edges, each union/find nearly O(1) with path compression.
**Space: O(n)** — the parent array.
</details>

---

### 323. Number of Connected Components in an Undirected Graph — Medium
[LeetCode](https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/)  
[Solution file (no hints)](../../problems/0001-0499/323.py)

Count the connected components in an undirected graph. How does either DFS-marking each unvisited node, or union-find merging every edge, both arrive at the same count?

<details>
<summary>Hint</summary>

Build an adjacency list and DFS (see [DFS](../algorithms/dfs.md)) from every unvisited node, incrementing a counter each time you start a fresh DFS — equivalently, use [union-find](../data-structures/union-find.md) and count distinct roots.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:

        graph = [[] for _ in range(n)]
        for a, b in edges:
            graph[a].append(b)
            graph[b].append(a)

        visited = set()

        def dfs(node):
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    dfs(neighbor)

        count = 0
        for i in range(n):
            if i not in visited:
                visited.add(i)
                dfs(i)
                count += 1

        return count
```

Building blocks: [list-comprehension](../syntax/list-comprehension.md) (`[[] for _ in ...]`) · [set-basics](../syntax/set-basics.md) · [recursion-basics](../syntax/recursion-basics.md) · [for-loop](../syntax/for-loop.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(V + E)** — every node and edge is visited once.
**Space: O(V + E)** — the adjacency list and visited set.
</details>

---

### 261. Graph Valid Tree — Medium
[LeetCode](https://leetcode.com/problems/graph-valid-tree/)  
Solution: not yet solved in this repo.

Given n nodes and a list of edges, determine if they form a valid tree. Why must a valid tree have *exactly* `n - 1` edges *and* be fully connected — and why isn't one condition enough on its own?

<details>
<summary>Hint</summary>

A tree needs exactly `n - 1` edges and no cycles — check the edge count first (a cheap early exit), then confirm full connectivity with [DFS](../algorithms/dfs.md)/[BFS](../algorithms/bfs.md) or [union-find](../data-structures/union-find.md) (if every union succeeds and all nodes end up connected, it's a tree).
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:

        if len(edges) != n - 1:
            return False

        parent = list(range(n))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]   # path compression
                x = parent[x]
            return x

        def union(x, y):
            root_x = find(x)
            root_y = find(y)
            if root_x == root_y:
                return False
            parent[root_x] = root_y
            return True

        for a, b in edges:
            if not union(a, b):
                return False

        return True
```

Building blocks: [union-find](../data-structures/union-find.md) · [if-return](../syntax/if-return.md) · [for-loop](../syntax/for-loop.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n · α(n))** — n edges, each union/find nearly O(1) with path compression.
**Space: O(n)** — the parent array.
</details>

---

### 127. Word Ladder — Hard
[LeetCode](https://leetcode.com/problems/word-ladder/)  
Solution: not yet solved in this repo.

Find the shortest transformation sequence length from `beginWord` to `endWord`, changing one letter at a time through valid words. Why is this "shortest path" framing exactly what BFS is built for?

<details>
<summary>Hint</summary>

Treat every word as a graph node, connected to words one letter apart. Run [BFS](../algorithms/bfs.md) from `beginWord` with a [queue](../data-structures/queue.md) — the level at which `endWord` is found is the answer. Generate neighbors by trying every letter at every position rather than precomputing the whole adjacency list.
</details>

<details>
<summary>Solution</summary>

```python
from collections import deque
from string import ascii_lowercase

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:

        word_set = set(wordList)
        if endWord not in word_set:
            return 0

        queue = deque([(beginWord, 1)])
        visited = {beginWord}

        while queue:
            word, steps = queue.popleft()
            if word == endWord:
                return steps

            for i in range(len(word)):
                for letter in ascii_lowercase:
                    candidate = word[:i] + letter + word[i + 1:]
                    if candidate in word_set and candidate not in visited:
                        visited.add(candidate)
                        queue.append((candidate, steps + 1))

        return 0
```

Building blocks: [deque](../data-structures/deque.md) · [string-methods](../syntax/string-methods.md) (`ascii_lowercase`) · [for-loop](../syntax/for-loop.md) · [set-basics](../syntax/set-basics.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n · L² · 26)** — n words of length L, each generating L·26 candidate neighbors.
**Space: O(n · L)** — the word set and visited set.
</details>
