# 10b. Working with 2D Grids

*The mechanics every grid problem assumes you already know.*

[← Prev](10-backtracking.md) · [🗺 Roadmap](../roadmap.md) · [Next →](11-graphs.md)

---

> **Builds on:** arrays from [Lesson 01](01-arrays-hashing.md) (a grid is just a list of lists) and recursion from [Lesson 04b](04b-recursion.md) (DFS on a grid is recursion with coordinate state).

Lessons 11 (Graphs), 15 (2-D DP), and 19 (Math & Geometry) all treat grid mechanics as assumed knowledge. This primer closes that gap. It's short — the ideas are simple — but skipping it means re-deriving the same boilerplate in every grid problem.

## Concept

### Grid indexing

A grid is a **list of lists** in Python: `grid[row][col]`, where row 0 is the top.

```
grid = [
  [1, 2, 3],    # row 0: grid[0][0]=1, grid[0][1]=2, grid[0][2]=3
  [4, 5, 6],    # row 1
  [7, 8, 9],    # row 2
]

rows = len(grid)        # 3
cols = len(grid[0])     # 3
```

Always derive `rows` and `cols` from the grid itself — never hardcode them.

### Neighbor generation — the 4-directional idiom

Most grid problems move **up, down, left, right**. Store these as direction deltas:

```python
DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]   # right, left, down, up

for dr, dc in DIRS:
    nr, nc = r + dr, c + dc
    # nr, nc is a neighbor of (r, c)
```

For 8-directional problems (diagonals too):

```python
DIRS8 = [(-1,-1),(-1,0),(-1,1),
         ( 0,-1),        (0,1),
         ( 1,-1),( 1,0),( 1,1)]
```

### Bounds checking — always validate before accessing

Accessing `grid[nr][nc]` with out-of-range indices crashes in Python (unlike C, there's no silent wrap-around — but negative indices *do* silently wrap in Python, which is a bug waiting to happen). Always check:

```python
def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

for dr, dc in DIRS:
    nr, nc = r + dr, c + dc
    if not in_bounds(nr, nc, rows, cols):
        continue
    # safe to access grid[nr][nc]
```

The one-liner version (common in interviews):
```python
if 0 <= nr < rows and 0 <= nc < cols:
    ...
```

### Visited tracking — two approaches

When traversing (BFS or DFS), you must prevent revisiting cells. Two patterns:

**Option 1: external visited set (non-destructive)**
```python
visited = set()

def dfs(r, c):
    if (r, c) in visited:
        return
    visited.add((r, c))
    for dr, dc in DIRS:
        nr, nc = r + dr, c + dc
        if in_bounds(nr, nc, rows, cols):
            dfs(nr, nc)
```

Use when the grid must remain unchanged (or when you need the visited set outside).

**Option 2: in-place marking (space-efficient)**
```python
def dfs(r, c):
    if not in_bounds(r, c, rows, cols) or grid[r][c] != '1':
        return
    grid[r][c] = '#'        # mark visited by mutating the grid
    for dr, dc in DIRS:
        dfs(r + dr, c + dc)
```

Use when the problem allows mutation and you want O(1) extra space (the input grid becomes the visited map). Remember to restore values if the grid needs to remain intact.

### The standard grid traversal skeleton

Most grid problems — number of islands, shortest path, reachable area — use one of these:

```python
# DFS (flood fill / connected component)
def dfs(r, c):
    if not in_bounds(r, c, rows, cols) or visited[r][c] or grid[r][c] == blocked:
        return
    visited[r][c] = True
    for dr, dc in DIRS:
        dfs(r + dr, c + dc)

count = 0
for r in range(rows):
    for c in range(cols):
        if not visited[r][c] and grid[r][c] == target:
            dfs(r, c)
            count += 1       # one connected component found


# BFS (shortest path — processes in order of distance)
from collections import deque

def bfs(start_r, start_c):
    queue = deque([(start_r, start_c, 0)])   # (row, col, distance)
    visited = set([(start_r, start_c)])
    while queue:
        r, c, dist = queue.popleft()
        if grid[r][c] == target:
            return dist
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if in_bounds(nr, nc, rows, cols) and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append((nr, nc, dist + 1))
    return -1   # not reachable
```

**BFS gives the shortest path in an unweighted grid; DFS gives reachability.**

## Common Grid Patterns at a Glance

| Problem type | Traversal | Visited tracking |
|---|---|---|
| Count connected components | DFS or BFS | In-place or set |
| Shortest path (unweighted) | BFS | Set |
| Flood fill (paint region) | DFS | In-place |
| Detect a cycle | DFS with state | Color marking |
| Multi-source shortest path | Multi-source BFS | Set |

## In-Lesson Exercises

<details>
<summary><strong>Exercise 1 — neighbor generation</strong></summary>

Write a function that returns all valid 4-directional neighbors of cell `(r, c)` in a grid with `rows` rows and `cols` columns.

```python
def neighbors(r, c, rows, cols):
    DIRS = [(0,1),(0,-1),(1,0),(-1,0)]
    return [(r+dr, c+dc) for dr,dc in DIRS
            if 0 <= r+dr < rows and 0 <= c+dc < cols]
```
</details>

<details>
<summary><strong>Exercise 2 — count islands (trace)</strong></summary>

Trace the DFS flood-fill approach on this grid. How many islands?

```
1 1 0
0 1 0
0 0 1
```

**Answer:** 2 islands. First DFS from `(0,0)` marks `(0,0)`, `(0,1)`, `(1,1)`. Second DFS from `(2,2)` marks `(2,2)`. This is [LeetCode 200](https://leetcode.com/problems/number-of-islands/).
</details>

<details>
<summary><strong>Exercise 3 — why BFS for shortest path?</strong></summary>

Why does BFS find the shortest path in an unweighted grid but DFS doesn't?

**Answer:** BFS explores cells in order of their distance from the source (level by level). The first time it reaches the target, it's guaranteed to have taken the fewest steps. DFS dives deep along one path and might reach the target via a long route before discovering a shorter one.
</details>

## Practice

Work these in order — they directly test grid mechanics:

- [LeetCode 200 — Number of Islands](https://leetcode.com/problems/number-of-islands/) 🟡 (DFS flood fill)
- [LeetCode 733 — Flood Fill](https://leetcode.com/problems/flood-fill/) 🟢 (in-place DFS)
- [LeetCode 994 — Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) 🟡 (multi-source BFS)
- [LeetCode 1091 — Shortest Path in Binary Matrix](https://leetcode.com/problems/shortest-path-in-binary-matrix/) 🟡 (BFS, 8-directional)

## Check Yourself

- [ ] I can generate all 4 valid neighbors of any cell with a single `DIRS` list and an in-bounds check — no if-elif chains.
- [ ] I know when to use in-place marking vs. an external visited set, and I know the trade-off.
- [ ] I can explain why BFS finds the shortest path but DFS does not.
- [ ] I can write the standard DFS flood-fill and BFS shortest-path grid skeletons from memory.

---

**Up next:** [Graphs (BFS & DFS)](11-graphs.md) — BFS for shortest unweighted paths, DFS for connectivity. Grids are just a special case of graphs.

[← Prev](10-backtracking.md) · [🗺 Roadmap](../roadmap.md) · [Next →](11-graphs.md)
