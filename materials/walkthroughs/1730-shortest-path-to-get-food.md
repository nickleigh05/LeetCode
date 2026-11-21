# 1730. Shortest Path to Get Food

**Medium** · 🔒 Premium · [LeetCode](https://leetcode.com/problems/shortest-path-to-get-food/) · [Solution file (no hints)](../../problems/1500-1999/1730.py)

[📖 11. Graphs lesson](../learning/11-graphs.md) · [📖 Grids primer](../learning/10b-grids-primer.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 11. Graphs problems](../rmap-practice/11-graphs.md)

---

You're starving and want to eat as soon as possible. You're given an `m x n` character grid with these cells:

- `'*'`: your location. There is **exactly one** `'*'`.
- `'#'`: a food cell. There may be **several**.
- `'O'`: free space you can walk through.
- `'X'`: an obstacle you can't walk through.

You can move to any **adjacent** cell (north, east, south, west) that isn't an obstacle. Return the **length of the shortest path** to reach **any** food cell, or `-1` if no food is reachable.

```
grid = [["X","X","X","X","X","X"],
        ["X","*","O","O","O","X"],
        ["X","O","O","#","O","X"],
        ["X","X","X","X","X","X"]]           →  3

grid = [["X","X","X","X","X"],
        ["X","*","X","O","X"],
        ["X","O","X","#","X"],
        ["X","X","X","X","X"]]               →  -1   (food is walled off)
```

**Constraints:** `1 <= m, n <= 200` · `grid[row][col]` is `'*'`, `'X'`, `'O'` or `'#'` · exactly one `'*'`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**shortest path**" | Every step costs 1, so this is unweighted shortest path, which means **BFS** |
| reach **any** food | Stop at the **first** `'#'` you pop. BFS finds the nearest one first |
| exactly one `'*'` | One source. Find it with a scan first |
| `'X'` blocks movement | Skip obstacles when expanding |
| unreachable → `-1` | If the queue empties without finding food, return -1 |
| grid up to 200 × 200 | 40,000 cells. One BFS over them is fine |

**Why BFS, again.** BFS expands in rings of equal distance: everything 1 step away, then everything 2 steps away, and so on. So the first food cell you take off the queue is guaranteed to be a closest one. DFS gives no such guarantee. It might wander a long way before finding food and would have to keep searching.

**Single source, many targets.** You don't need the distance to every food cell, just the first one you reach. That means you can return as soon as you pop a `'#'`.

🤔 **Before you open the next section:** what do you need to store alongside each cell in the queue so you know its distance when you reach food?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| DFS, tracking the minimum | Explore every path, keep the best | Exponential without memo | O(m·n) | ❌ No ordering guarantee |
| BFS from each food cell | Search back to `'*'` from every `'#'` | O(F·m·n) | O(m·n) | ❌ Repeats work |
| **BFS from `'*'`** | Expand rings, stop at the first `'#'` | **O(m·n)** | O(m·n) | ✅ |
| Multi-source BFS from all food | Seed all `'#'`, stop on reaching `'*'` | O(m·n) | O(m·n) | ✅ Also fine |

**The decision: single-source [BFS](../algorithms/bfs.md) from your position, using a [queue](../data-structures/queue.md).**

There's one start and many targets, so starting from the start is the natural direction. Seeding from every food cell (like [01 Matrix](542-01-matrix.md)) also works, but it isn't needed.

**Carry the distance in the queue.** Store `(row, col, steps)` tuples. When you pop a food cell, `steps` is the answer. An alternative is to process the queue one level at a time and count levels, but carrying the distance is simpler.

**Mark visited when enqueuing.** Add a cell to `visited` at the moment you put it in the queue, so two neighbours can't both enqueue it.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
rows, cols = len(grid), len(grid[0])
for r in range(rows):
    for c in range(cols):
        if grid[r][c] == '*':
            start = (r, c)
```

**Find the start.** There's exactly one `'*'`, so a full scan always sets `start`. The scan is O(m·n), the same order as the BFS.
→ [range-function](../syntax/range-function.md) · [nested-lists](../syntax/nested-lists.md) · [tuple-basics](../syntax/tuple-basics.md)

```python
queue = deque([(start[0], start[1], 0)])
visited = {start}
directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
```

The queue begins with the start at distance 0. `visited` is a set of `(row, col)` tuples. Tuples are hashable, so they work as set members. `directions` lists the four moves.
→ [deque-basics](../syntax/deque-basics.md) · [set-basics](../syntax/set-basics.md)

```python
while queue:
    r, c, steps = queue.popleft()
    if grid[r][c] == '#':
        return steps
```

**Pop the oldest cell and check for food.** Because BFS processes cells in order of distance, the first food popped is the nearest. Return its distance immediately.
→ [while-loop](../syntax/while-loop.md) · [tuple-unpacking](../syntax/tuple-unpacking.md) · [if-return](../syntax/if-return.md)

```python
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if (0 <= nr < rows and 0 <= nc < cols
                and grid[nr][nc] != 'X' and (nr, nc) not in visited):
            visited.add((nr, nc))
            queue.append((nr, nc, steps + 1))
```

**Expand to valid neighbours.** A neighbour is valid if it's inside the grid, not an obstacle, and not already seen. Mark it visited and queue it one step further away.

The bounds check comes **first**, so `grid[nr][nc]` is never read out of range. Short-circuiting stops at the first false condition. The parentheses let the condition span two lines.
→ [chained-comparisons](../syntax/chained-comparisons.md) · [logical-operators](../syntax/logical-operators.md) · [membership-operators](../syntax/membership-operators.md)

```python
return -1
```

The queue emptied without popping any food, so every reachable cell was explored and none was food.

<details>
<summary>The whole thing together</summary>

```python
from collections import deque

class Solution:
    def getFood(self, grid: List[List[str]]) -> int:
        rows, cols = len(grid), len(grid[0])
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '*':
                    start = (r, c)

        queue = deque([(start[0], start[1], 0)])
        visited = {start}
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        while queue:
            r, c, steps = queue.popleft()
            if grid[r][c] == '#':
                return steps

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if (0 <= nr < rows and 0 <= nc < cols
                        and grid[nr][nc] != 'X' and (nr, nc) not in visited):
                    visited.add((nr, nc))
                    queue.append((nr, nc, steps + 1))

        return -1
```

</details>

**Trace it.** The first example, with the start at `(1,1)` and food at `(2,3)`:

| Ring (steps) | Cells popped | Food? |
|---|---|---|
| 0 | (1,1) | no |
| 1 | (2,1), (1,2) | no |
| 2 | (2,2), (1,3) | no |
| 3 | (2,3) … | **yes → return 3** ✅ |

The walls on every side are `'X'`, so the search stays inside the open area.

**The second example.** From `(1,1)` the only open neighbour is `(2,1)`, and every neighbour of that is a wall or already visited. The queue empties, so it returns **−1** ✅.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(m·n)</summary>

**O(m·n).**

- Finding `'*'` scans every cell once.
- Each cell is added to `visited` and the queue at most once, and each pop checks 4 neighbours.

In the worst case (no reachable food) every open cell is explored. With food nearby, the early return stops much sooner.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(m·n)</summary>

**O(m·n).** The `visited` set and the queue can each hold every open cell.

**A common space trick:** overwrite visited cells in the grid itself, for example setting them to `'X'`, and drop the `visited` set. That saves the set but changes the input. Ask before doing that in an interview.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "All moves cost 1, so the shortest path is BFS. I find the single start cell, then BFS outwards, storing each cell's distance in the queue. Because BFS processes cells in order of distance, the first food cell I pop is the nearest one, so I return its distance straight away. Obstacles and visited cells are skipped, and I mark cells visited when I enqueue them. If the queue empties, no food is reachable, so -1. O(m·n) time and space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Return the actual path?" | Store each cell's parent when you enqueue it, then walk back from the food cell to the start. |
| "Different costs per cell (e.g. mud)?" | Weighted shortest path, so use [Dijkstra](../algorithms/dijkstra.md) with a heap. |
| "Costs are only 0 or 1?" | 0-1 BFS: a deque where 0-cost moves go on the front and 1-cost moves on the back. |
| "Distance from every cell to its nearest food?" | Multi-source BFS seeded from all `'#'`, as in [01 Matrix](542-01-matrix.md). |
| "Huge open grid?" | Bidirectional BFS or A* with Manhattan distance can cut the search space. |

**Traps:**

- **Checking for food when enqueuing and returning `steps`.** Then you'd need `steps + 1`. Pick one place to check and be consistent.
- **Marking visited on dequeue.** Cells get enqueued many times.
- **Indexing before the bounds check.** `grid[nr][nc]` with `nr = -1` silently reads the last row in Python. That's a nasty bug, so always check the range first.
- **Using DFS.** It doesn't find the shortest path without exploring everything.

**This same move shows up in:** [01 Matrix](542-01-matrix.md) (the same grid BFS, multi-source) · [Rotting Oranges](994-rotting-oranges.md) (BFS rings counted as minutes) · [Walls and Gates](286-walls-and-gates.md) (BFS distances on a grid with obstacles) · [Minimum Knight Moves](1197-minimum-knight-moves.md) (BFS with a different move set).

</details>

---
