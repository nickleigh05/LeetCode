# 542. 01 Matrix

**Medium** · [LeetCode](https://leetcode.com/problems/01-matrix/) · [Solution file (no hints)](../../problems/0500-0999/542.py)

[📖 11. Graphs lesson](../learning/11-graphs.md) · [📖 Grids primer](../learning/10b-grids-primer.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 11. Graphs problems](../rmap-practice/11-graphs.md)

---

Given an `m x n` binary matrix `mat`, return a matrix of the same size where each cell holds the **distance to the nearest `0`**. Two cells sharing an edge are distance 1 apart.

```
mat = [[0,0,0],        →   [[0,0,0],
       [0,1,0],             [0,1,0],
       [0,0,0]]             [0,0,0]]

mat = [[0,0,0],        →   [[0,0,0],
       [0,1,0],             [0,1,0],
       [1,1,1]]             [1,2,1]]
```

**Constraints:** `1 <= m, n <= 10⁴` · `1 <= m * n <= 10⁴` · `mat[i][j]` is `0` or `1` · there is **at least one `0`**

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "distance to the **nearest** 0" | A shortest-path question on an unweighted grid. Unweighted shortest path means **BFS** |
| sharing an edge | 4-directional moves, each costing 1 |
| for **every** cell | Not one source and one target. You need the answer at every cell at once |
| at least one 0 | Every cell has an answer, so no "unreachable" case |
| `m·n ≤ 10⁴` | One BFS per cell would be up to 10⁸, too slow. Aim for O(m·n) |

**The obvious idea, and why it's slow.** For each `1`, BFS outwards until you hit a `0`. That's correct but repeats a huge amount of work: neighbouring cells explore nearly identical regions. Up to 10⁴ BFS runs × 10⁴ cells is too much.

**The reversal that fixes it.** Don't search *from each 1 for a 0*. Search **from all the 0s at once** outwards. Put every `0` in the queue at distance 0 before you start. The BFS frontier then expands in rings: first every cell at distance 1 from *some* zero, then distance 2, and so on. The first time the wave reaches a cell, that's its distance to the **nearest** zero, because BFS visits cells in order of distance.

This is **multi-source BFS**. It's the same technique as [Rotting Oranges](994-rotting-oranges.md) and [Walls and Gates](286-walls-and-gates.md).

🤔 **Before you open the next section:** if the queue starts with every `0`, why does the first visit to a `1` give you the distance to the *nearest* zero, rather than just some zero?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| BFS from every `1` | Search outwards until a 0 is found | O((m·n)²) | O(m·n) | ❌ Repeated work |
| Brute distance | For each cell, check every zero's Manhattan distance | O((m·n)²) | O(1) | ❌ Same blow-up |
| **Multi-source BFS** | Seed the queue with all zeros, expand once | **O(m·n)** | O(m·n) | ✅ |
| Two-pass DP | Top-left pass then bottom-right pass, min over neighbours | O(m·n) | O(1) extra | ✅ Clever alternative |

**The decision: multi-source [BFS](../algorithms/bfs.md) with a [queue](../data-structures/queue.md).**

Each cell enters the queue once and is processed once, so the total work is proportional to the grid.

**Why BFS and not DFS?** DFS doesn't explore in order of distance. It can reach a cell along a long winding path first, and you'd have to keep revisiting to correct it. BFS reaches every cell for the first time by a shortest path, so you can finalise its distance on that first visit.

**The DP alternative, briefly.** A cell's distance is `1 + min(neighbours' distances)`. One pass from the top-left handles paths coming from above and the left. A second pass from the bottom-right handles below and the right. It's also O(m·n) and uses no queue. It's worth mentioning as a follow-up, but BFS is easier to justify.

**The visited trick:** initialise the result with `-1` for every `1`. A `-1` means "not reached yet," so the result grid doubles as the visited set.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
rows, cols = len(mat), len(mat[0])
dist = [[-1] * cols for _ in range(rows)]
queue = deque()
```

`dist` is the answer grid, and `-1` marks "not reached yet." Build it with a [comprehension](../syntax/list-comprehension.md), **not** `[[-1] * cols] * rows`, which would make every row the *same* list object.

`deque` gives O(1) `popleft`. A plain list's `pop(0)` is O(n).
→ [nested-lists](../syntax/nested-lists.md) · [list-comprehension](../syntax/list-comprehension.md) · [deque-basics](../syntax/deque-basics.md)

```python
for r in range(rows):
    for c in range(cols):
        if mat[r][c] == 0:
            dist[r][c] = 0
            queue.append((r, c))
```

**Seed every source.** Every zero is distance 0 from a zero (itself) and goes into the queue before the search begins. This is the line that makes it *multi*-source. All zeros start the wave at the same moment.
→ [range-function](../syntax/range-function.md) · [tuple-basics](../syntax/tuple-basics.md)

```python
directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
```

The four neighbours: down, up, right, left. Keeping them in a list means the neighbour loop is a single `for` instead of four copied blocks.
→ [list-basics](../syntax/list-basics.md)

```python
while queue:
    r, c = queue.popleft()
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
```

Standard BFS: take the oldest cell and look at its four neighbours. Because the queue is first in, first out, every distance-`d` cell is processed before any distance-`d+1` cell.
→ [while-loop](../syntax/while-loop.md) · [tuple-unpacking](../syntax/tuple-unpacking.md)

```python
        if 0 <= nr < rows and 0 <= nc < cols and dist[nr][nc] == -1:
            dist[nr][nc] = dist[r][c] + 1
            queue.append((nr, nc))
```

**Two checks in one line:** the neighbour is inside the grid, and it hasn't been reached yet. If both hold, its distance is one more than the current cell's.

**Mark it when you enqueue it, not when you dequeue it.** Setting `dist` here stops the same cell from being added to the queue twice by two different neighbours. The chained comparison `0 <= nr < rows` is Python's readable bounds check.
→ [chained-comparisons](../syntax/chained-comparisons.md) · [logical-operators](../syntax/logical-operators.md)

```python
return dist
```

<details>
<summary>The whole thing together</summary>

```python
from collections import deque

class Solution:
    def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:
        rows, cols = len(mat), len(mat[0])
        dist = [[-1] * cols for _ in range(rows)]
        queue = deque()

        for r in range(rows):
            for c in range(cols):
                if mat[r][c] == 0:
                    dist[r][c] = 0
                    queue.append((r, c))

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        while queue:
            r, c = queue.popleft()
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and dist[nr][nc] == -1:
                    dist[nr][nc] = dist[r][c] + 1
                    queue.append((nr, nc))

        return dist
```

</details>

**Trace it.** The second example: zeros fill the top two rows except the centre.

```
After seeding (-1 = unreached):     After ring 1:          After ring 2:
 0  0  0                             0  0  0                0  0  0
 0 -1  0                             0  1  0                0  1  0
-1 -1 -1                             1 -1  1                1  2  1
```

- **Ring 1:** the zeros at `(1,0)`, `(0,1)`, `(1,2)` reach `(1,1)`, `(2,0)`, `(2,2)`, which all get distance 1.
- **Ring 2:** `(2,1)` is reached from `(1,1)` or `(2,0)`, both at distance 1, so it gets **2**.

Result `[[0,0,0],[0,1,0],[1,2,1]]` ✅.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(m·n)</summary>

**O(m·n).**

- Seeding scans the grid once.
- Each cell is enqueued **at most once**, because the `dist == -1` check stops repeats, and dequeued once.
- Each dequeue checks 4 neighbours, which is constant work.

So the total is a few constant-size operations per cell.

**Why the per-cell BFS is so much worse:** it's O(m·n) *per* `1`, so O((m·n)²) overall. At 10⁴ cells that's the difference between 10⁴ and 10⁸ operations.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(m·n)</summary>

**O(m·n).**

- `dist` is the output, the same size as the input.
- The queue can hold up to O(m·n) cells. If almost everything is a zero, they're all seeded at once.

**Can you do better?** The two-pass DP needs no queue. If you're allowed to overwrite `mat`, it uses O(1) extra space beyond the output. Mention it if asked.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "This is unweighted shortest distance, so BFS. Running a BFS from every 1 would repeat work, so I flip it: I put every 0 into the queue at distance 0 and expand outwards once. BFS reaches cells in order of distance, so the first time the wave reaches a cell is the distance to its nearest zero. I use the result grid with -1 as the visited marker, and I set a cell's distance when I enqueue it so nothing is queued twice. O(m·n) time and space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Do it without a queue." | Two-pass DP: top-left to bottom-right using up/left neighbours, then bottom-right to top-left using down/right. Each cell is `1 + min` of the relevant neighbours. |
| "Diagonal moves allowed?" | Add the 4 diagonal directions. BFS still works because every step still costs 1. |
| "Different costs per move?" | Now it's weighted, so you'd switch to [Dijkstra](../algorithms/dijkstra.md). |
| "Distance to the nearest 1 instead?" | Seed with the 1s instead. Nothing else changes. |

**Traps:**

- **BFS from each 1.** Correct but O((m·n)²), and a timeout at the upper constraint.
- **Marking visited on dequeue.** Cells get queued multiple times. It still gives correct distances but wastes time and memory.
- **`[[-1] * cols] * rows`.** All rows alias one list, so writing one cell writes the whole column.
- **Using DFS.** DFS doesn't visit in distance order, so first-visit distances are wrong.
- **`list.pop(0)` as the queue.** O(n) per pop, which quietly makes the search quadratic.

**This same move shows up in:** [Rotting Oranges](994-rotting-oranges.md) (multi-source BFS where the rings are minutes) · [Walls and Gates](286-walls-and-gates.md) (multi-source from every gate, almost identical code) · [Shortest Path to Get Food](1730-shortest-path-to-get-food.md) (single-source BFS on a grid) · [Pacific Atlantic Water Flow](417-pacific-atlantic-water-flow.md) (searching inwards from the borders instead of outwards from each cell).

</details>

---
