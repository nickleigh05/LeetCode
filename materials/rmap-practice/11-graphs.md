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
rows, cols = len(grid), len(grid[0])
visited = set()
islands = 0

def dfs(r, c):
    if (r < 0 or r >= rows or c < 0 or c >= cols or
            grid[r][c] == "0" or (r, c) in visited):
        return                              # out of bounds, water, or already visited
    visited.add((r, c))
    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:  # explore 4 neighbors
        dfs(r + dr, c + dc)

for r in range(rows):
    for c in range(cols):
        if grid[r][c] == "1" and (r, c) not in visited:
            dfs(r, c)                        # sink the whole island
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
old_to_new = {}

def dfs(node):
    if node in old_to_new:                # already cloned: reuse it, breaks cycles
        return old_to_new[node]

    copy = Node(node.val)
    old_to_new[node] = copy                 # register before recursing into neighbors
    for neighbor in node.neighbors:
        copy.neighbors.append(dfs(neighbor))

    return copy

return dfs(node) if node else None
```

Building blocks: [dict-basics](../syntax/dict-basics.md) · [recursion-basics](../syntax/recursion-basics.md) · [for-loop](../syntax/for-loop.md) · [ternary-expression](../syntax/ternary-expression.md)
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
rows, cols = len(grid), len(grid[0])
visited = set()

def dfs(r, c):
    if (r < 0 or r >= rows or c < 0 or c >= cols or
            grid[r][c] == 0 or (r, c) in visited):
        return 0                            # contributes no area
    visited.add((r, c))
    area = 1
    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        area += dfs(r + dr, c + dc)
    return area

best = 0
for r in range(rows):
    for c in range(cols):
        best = max(best, dfs(r, c))
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
rows, cols = len(heights), len(heights[0])
pacific, atlantic = set(), set()

def dfs(r, c, visited, prev_height):
    if (r < 0 or r >= rows or c < 0 or c >= cols or
            (r, c) in visited or heights[r][c] < prev_height):
        return                              # can't flow backward into a lower cell
    visited.add((r, c))
    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        dfs(r + dr, c + dc, visited, heights[r][c])

for c in range(cols):                      # top row touches Pacific, bottom row touches Atlantic
    dfs(0, c, pacific, heights[0][c])
    dfs(rows - 1, c, atlantic, heights[rows - 1][c])
for r in range(rows):                      # left col touches Pacific, right col touches Atlantic
    dfs(r, 0, pacific, heights[r][0])
    dfs(r, cols - 1, atlantic, heights[r][cols - 1])

return [[r, c] for r in range(rows) for c in range(cols) if (r, c) in pacific and (r, c) in atlantic]
```

Building blocks: [set-basics](../syntax/set-basics.md) · [recursion-basics](../syntax/recursion-basics.md) · [list-comprehension](../syntax/list-comprehension.md) (nested)
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
rows, cols = len(board), len(board[0])

def dfs(r, c):
    if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != "O":
        return
    board[r][c] = "T"                      # temporarily mark as safe
    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        dfs(r + dr, c + dc)

for r in range(rows):                     # DFS from every border cell
    dfs(r, 0)
    dfs(r, cols - 1)
for c in range(cols):
    dfs(0, c)
    dfs(rows - 1, c)

for r in range(rows):                     # flip surrounded O's to X, safe T's back to O
    for c in range(cols):
        if board[r][c] == "O":
            board[r][c] = "X"
        elif board[r][c] == "T":
            board[r][c] = "O"
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

rows, cols = len(grid), len(grid[0])
q = deque()
fresh = 0

for r in range(rows):                     # seed the queue, count fresh oranges
    for c in range(cols):
        if grid[r][c] == 2:
            q.append((r, c))
        elif grid[r][c] == 1:
            fresh += 1

minutes = 0
while q and fresh > 0:                     # while loop, one minute per level
    for _ in range(len(q)):                  # process exactly this minute's rotten oranges
        r, c = q.popleft()
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                grid[nr][nc] = 2                # this orange rots now
                fresh -= 1
                q.append((nr, nc))
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

rows, cols = len(rooms), len(rooms[0])
q = deque()

for r in range(rows):                     # seed the queue with every gate
    for c in range(cols):
        if rooms[r][c] == 0:
            q.append((r, c))

while q:                                  # while loop, standard BFS
    r, c = q.popleft()
    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and rooms[nr][nc] == 2147483647:
            rooms[nr][nc] = rooms[r][c] + 1     # one step farther than the current cell
            q.append((nr, nc))
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
from collections import defaultdict, deque

graph = defaultdict(list)
indegree = [0] * numCourses

for course, prereq in prerequisites:        # build the graph and count indegrees
    graph[prereq].append(course)
    indegree[course] += 1

q = deque([c for c in range(numCourses) if indegree[c] == 0])   # courses with no prereqs
visited = 0

while q:                                   # while loop, Kahn's topological sort
    node = q.popleft()
    visited += 1
    for nxt in graph[node]:
        indegree[nxt] -= 1
        if indegree[nxt] == 0:               # all of nxt's prereqs are now done
            q.append(nxt)

return visited == numCourses               # every course reachable means no cycle
```

Building blocks: [defaultdict](../syntax/defaultdict.md) · [deque](../data-structures/deque.md) · [list-comprehension](../syntax/list-comprehension.md) · [while-loop](../syntax/while-loop.md)
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
from collections import defaultdict, deque

graph = defaultdict(list)
indegree = [0] * numCourses

for course, prereq in prerequisites:
    graph[prereq].append(course)
    indegree[course] += 1

q = deque([c for c in range(numCourses) if indegree[c] == 0])
order = []

while q:
    node = q.popleft()
    order.append(node)                       # dequeue order is a valid schedule
    for nxt in graph[node]:
        indegree[nxt] -= 1
        if indegree[nxt] == 0:
            q.append(nxt)

return order if len(order) == numCourses else []
```

Building blocks: [defaultdict](../syntax/defaultdict.md) · [deque](../data-structures/deque.md) · [while-loop](../syntax/while-loop.md) · [ternary-expression](../syntax/ternary-expression.md)
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
parent = list(range(len(edges) + 1))

def find(x):
    while parent[x] != x:                    # walk up to the root
        parent[x] = parent[parent[x]]           # path compression
        x = parent[x]
    return x

def union(x, y):
    root_x, root_y = find(x), find(y)
    if root_x == root_y:                       # already connected: this edge is redundant
        return False
    parent[root_x] = root_y
    return True

for a, b in edges:                          # for loop over edges in given order
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
from collections import defaultdict

graph = defaultdict(list)
for a, b in edges:
    graph[a].append(b)
    graph[b].append(a)

visited = set()

def dfs(node):
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(neighbor)

count = 0
for node in range(n):                       # for loop over every node
    if node not in visited:                    # unvisited: it's a new component
        dfs(node)
        count += 1

return count
```

Building blocks: [defaultdict](../syntax/defaultdict.md) · [set-basics](../syntax/set-basics.md) · [recursion-basics](../syntax/recursion-basics.md) · [for-loop](../syntax/for-loop.md)
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
if len(edges) != n - 1:                    # a tree has exactly n-1 edges
    return False

parent = list(range(n))

def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x

def union(x, y):
    root_x, root_y = find(x), find(y)
    if root_x == root_y:                     # this edge would create a cycle
        return False
    parent[root_x] = root_y
    return True

for a, b in edges:                          # for loop over every edge
    if not union(a, b):
        return False

return True                                 # n-1 edges + no cycle = connected tree
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

word_set = set(wordList)
if endWord not in word_set:
    return 0

q = deque([(beginWord, 1)])                # (word, steps taken so far)
visited = {beginWord}

while q:                                    # while loop, BFS level by level
    word, steps = q.popleft()
    if word == endWord:
        return steps

    for i in range(len(word)):                # try changing each letter position
        for ch in ascii_lowercase:
            candidate = word[:i] + ch + word[i + 1:]
            if candidate in word_set and candidate not in visited:
                visited.add(candidate)
                q.append((candidate, steps + 1))

return 0
```

Building blocks: [deque](../data-structures/deque.md) · [string-methods](../syntax/string-methods.md) (`ascii_lowercase`) · [for-loop](../syntax/for-loop.md) · [set-basics](../syntax/set-basics.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n · L² · 26)** — n words of length L, each generating L·26 candidate neighbors.
**Space: O(n · L)** — the word set and visited set.
</details>
