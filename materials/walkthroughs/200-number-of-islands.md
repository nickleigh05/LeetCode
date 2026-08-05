# 200. Number of Islands

**Medium** · [LeetCode](https://leetcode.com/problems/number-of-islands/) · [Solution file (no hints)](../../problems/0001-0499/200.py)

[📖 11. Graphs lesson](../learning/11-graphs.md) · [📖 Grids primer](../learning/10b-grids-primer.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 11. Graphs problems](../rmap-practice/11-graphs.md)

---

Given an `m × n` 2-D grid of `'1'`s (land) and `'0'`s (water), return the **number of islands**.

An island is surrounded by water and formed by connecting adjacent lands **horizontally or vertically**. You may assume all four edges of the grid are surrounded by water.

```
grid = [["1","1","1","1","0"],          →  1
        ["1","1","0","1","0"],
        ["1","1","0","0","0"],
        ["0","0","0","0","0"]]

grid = [["1","1","0","0","0"],          →  3
        ["1","1","0","0","0"],
        ["0","0","1","0","0"],
        ["0","0","0","1","1"]]
```

**Constraints:** `1 <= m, n <= 300` · each cell is `'0'` or `'1'` (⚠️ **strings**, not integers)

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

This is the gateway problem for the unit. **The "scan every cell, flood-fill from each unvisited start" pattern you learn here recurs in half of Unit 11.**

| The statement says | Which really means |
|---|---|
| "**connected** adjacent lands" | ⚠️ This is a **connected components** problem — the core graph question |
| "horizontally or vertically" | 4-directional adjacency, not 8 (no diagonals) |
| "**number** of islands" | Count the components, don't measure them |
| edges surrounded by water | No wrap-around; out-of-bounds is just water |
| cells are `'1'`/`'0'` as **strings** | ⚠️ Compare against `"1"`, not `1` — a silent-failure trap |
| 300 × 300 = 90,000 cells | O(m·n) is expected |

**The reframe that makes this a graph problem.** There's no explicit graph here — no nodes, no edge list. But a grid *is* a graph:

- **Each cell is a node.**
- **Each cell has up to 4 edges**, to its orthogonal neighbours.

This is an **implicit graph** — the structure is defined by the rules of adjacency rather than stored anywhere. Recognizing that is the whole unlock, because it means every graph algorithm applies to grids.

**The counting insight.** An island is a connected component of land cells. So:

1. Scan every cell.
2. When you find **unvisited land**, you've discovered a new island — increment the count.
3. **Flood-fill** the entire island (via DFS or BFS), marking every cell visited.
4. Continue scanning.

The flood-fill is what makes the counting correct: after step 3, every cell of that island is marked, so the scan won't count any of them again. **Each island is discovered exactly once — at whichever of its cells the scan reaches first.**

🤔 **Before you open the next section:** what would happen to the count if you incremented on every land cell but forgot to mark the rest of the island?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Check each cell's neighbours only | Count land, subtract adjacencies | — | ❌ Doesn't capture transitive connectivity |
| **DFS flood-fill** | Recursively sink each island | **O(m·n)** | ✅ |
| **BFS flood-fill** | Queue-based sinking | O(m·n) | ✅ Equally valid |
| [Union-Find](../data-structures/union-find.md) | Union adjacent land cells, count roots | O(m·n·α) | ✅ Overkill here, essential when edges arrive dynamically |

**The decision: scan every cell, and DFS-flood-fill from each unvisited land cell.**

DFS and BFS are interchangeable for this problem — you're exploring *everything* reachable, so the order doesn't matter. **That's a useful thing to notice**: when a problem asks "what's connected?", either works; when it asks "what's the shortest path?", only BFS does. Contrast with [Rotting Oranges](994-rotting-oranges.md), where the level-by-level property is essential.

**Why a `visited` set rather than mutating the grid.** Two options:

| Approach | Cost | Note |
|---|---|---|
| `visited` set of `(row, col)` | **O(m·n)** space | Non-destructive |
| Overwrite land with `"0"` | **O(1)** space | ⚠️ Destroys the input |

The set version is used here and is the safer default. Sinking cells in place is a common optimization worth mentioning — but it mutates the caller's grid, which matters if it's reused.

⚠️ **The crucial contrast with [Word Search](79-word-search.md):** there, cells were marked *and then restored*, because a cell rejected by one path had to remain available to another. **Here, marking is permanent** — once a cell belongs to an island, no other exploration should ever revisit it. Backtracking would be actively wrong.

> **Backtracking un-marks; graph traversal doesn't.** The difference is whether you're exploring *alternative paths* or *reachability*.

**Why the base cases are checked inside the recursion.** Bounds and water checks happen at the top of `dfs` rather than before each call, which keeps the four recursive calls uniform — the same style as [Word Search](79-word-search.md).

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
rows = len(grid)
cols = len(grid[0])
visited = set()
islands = 0
```

Grid dimensions, a set of visited coordinates, and the component counter.

Storing `(row, col)` **tuples** in the set works because tuples are hashable — lists would not be.
→ [set-basics](../syntax/set-basics.md) · [nested-lists](../syntax/nested-lists.md) · [tuple-basics](../syntax/tuple-basics.md)

```python
def dfs(row, col):
    if row < 0 or row >= rows or col < 0 or col >= cols:
        return
```

**Bounds check.** Stepping off the grid is simply water — no wrap-around, per the problem statement.
→ [function-basics](../syntax/function-basics.md) · [closures](../syntax/closures.md) · [logical-operators](../syntax/logical-operators.md)

```python
    if grid[row][col] == "0" or (row, col) in visited:
        return
```

**Two stopping conditions**: water isn't part of an island, and an already-visited cell needs no re-exploration.

⚠️ **`"0"` with quotes** — the grid holds *strings*. Comparing against integer `0` silently never matches, so every cell looks like land and the whole grid becomes one island.
→ [membership-operators](../syntax/membership-operators.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
    visited.add((row, col))
    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        dfs(row + dr, col + dc)
```

**Mark, then explore all four neighbours.**

Marking **before** recursing is what prevents infinite recursion — otherwise two adjacent cells would call each other forever.

The direction list is the standard 4-neighbour idiom: down, up, right, left. See the [grids primer](../learning/10b-grids-primer.md).

**Note there's no un-marking.** Unlike [Word Search](79-word-search.md), the mark is permanent — this cell belongs to this island and must never be counted again.
→ [set-operations](../syntax/set-operations.md) · [tuple-unpacking](../syntax/tuple-unpacking.md) · [for-loop](../syntax/for-loop.md)

```python
for row in range(rows):
    for col in range(cols):
        if grid[row][col] == "1" and (row, col) not in visited:
            dfs(row, col)
            islands += 1
```

**The counting scan.** Finding unvisited land means discovering a **new** island — so flood-fill it entirely, then increment.

The order matters conceptually: `dfs` marks the whole island, so subsequent iterations skip all its other cells. **One increment per island, at whichever cell the scan hits first.**
→ [range-function](../syntax/range-function.md) · [if-return](../syntax/if-return.md)

```python
return islands
```

<details>
<summary>The whole thing together</summary>

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

</details>

**Trace it** — the 3-island example:

```
        col: 0  1  2  3  4
row 0:       1  1  0  0  0
row 1:       1  1  0  0  0
row 2:       0  0  1  0  0
row 3:       0  0  0  1  1
```

| Scan reaches | Land? | Visited? | Action | `islands` |
|---|---|---|---|---|
| (0,0) | ✅ | no | **DFS** floods (0,0),(0,1),(1,0),(1,1) | **1** |
| (0,1) | ✅ | **yes** | skip | 1 |
| (1,0),(1,1) | ✅ | **yes** | skip | 1 |
| (2,2) | ✅ | no | **DFS** floods (2,2) alone | **2** |
| (3,3) | ✅ | no | **DFS** floods (3,3),(3,4) | **3** |
| (3,4) | ✅ | **yes** | skip | 3 |

Answer: **3** ✅

The skips are the whole mechanism. Cell (0,1) is land, but the flood-fill from (0,0) already claimed it — so it doesn't start a new island. **Without the marking, this grid would report 7 islands** (one per land cell).

</details>

<details>
<summary><b>4 · Time complexity</b> — O(m · n)</summary>

**O(m · n)** — linear in the number of cells.

The nested scan alone is O(m·n), and the flood-fills look like they'd add more — but they don't:

> **Every cell is visited a constant number of times.** A cell is added to `visited` exactly once, and it can be *reached* at most 4 times (once from each neighbour), each of which is an O(1) set lookup that returns immediately.

So total work across all DFS calls is O(4·m·n) = **O(m·n)**.

At 300 × 300 = 90,000 cells, that's ~360,000 operations. Instant.

**The same amortized reasoning as the monotonic stacks** in Unit 04: don't count the nesting, count how many times each element can be touched.

**Optimal** — you must examine every cell to know whether it's land.

**BFS is identically O(m·n)**, enqueuing and dequeuing each cell once. **Union-Find** is O(m·n·α) where α is the inverse Ackermann function — effectively constant, so also linear, but with a larger constant and more machinery.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(m · n)</summary>

**O(m · n)**, from two sources:

| Component | Worst case |
|---|---|
| `visited` set | every cell → **O(m·n)** |
| **Recursion stack** | ⚠️ one frame per cell in the worst case → **O(m·n)** |

**The recursion depth is the real hazard.** A grid that's *entirely* land makes the DFS traverse all 90,000 cells in a single chain — **far past Python's default recursion limit of 1000**, raising `RecursionError`.

That's a legitimate answer to "what would break?", and the fix is **BFS**:

```python
from collections import deque
queue = deque([(row, col)])
while queue:
    r, c = queue.popleft()
    for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
        ...
```

BFS uses an explicit queue bounded by the **frontier** size — O(min(m,n)) for a typical grid, versus DFS's O(m·n) stack. **On large grids BFS is the safer choice**, and saying so shows you've thought past the happy path.

**The in-place alternative** drops the `visited` set to O(1) by overwriting land with `"0"`:

| Approach | Space | Note |
|---|---|---|
| `visited` set | O(m·n) | Non-destructive |
| Sink in place | **O(1)** | ⚠️ Mutates the input |

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "A grid is an implicit graph — each cell is a node with up to four edges to its orthogonal neighbours — so counting islands is counting connected components. I scan every cell, and whenever I find unvisited land I've discovered a new island: I flood-fill the whole component with DFS, marking every cell visited, then increment the count. The marking is what makes the count correct — every other cell of that island gets skipped by the scan. Note the marking is *permanent* here, unlike backtracking problems where you restore state; I'm exploring reachability, not alternative paths. Every cell is visited a constant number of times, so O(m·n) time and space. On a large all-land grid the recursion could blow Python's stack, so I'd switch to BFS."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why don't you un-mark cells like in Word Search?" | **The question.** There you explore alternative *paths*, so a rejected cell must stay available. Here you explore *reachability* — a cell belongs to exactly one island. |
| "What if the grid is huge and all land?" | DFS recursion overflows. Use BFS with an explicit queue, or an iterative DFS with your own stack. |
| "Avoid the `visited` set." | Sink land in place by overwriting with `"0"` — O(1) space, but it mutates the caller's grid. |
| "Return the **largest** island instead." | Have the DFS return an area rather than nothing — that's [Max Area of Island](695-max-area-of-island.md). |
| "What if diagonals counted as connected?" | Extend to 8 directions. Everything else is unchanged. |
| "Islands added one at a time, dynamically?" | Now Union-Find is genuinely better — you can merge components incrementally without re-scanning. LeetCode 305. |
| "BFS or DFS here?" | Either — you're exploring everything reachable, so order is irrelevant. It matters only for shortest-path questions. |

**Traps:**

- **Comparing against `0` instead of `"0"`.** The grid holds strings; the comparison silently never matches and the whole grid reads as one island.
- **Forgetting to mark cells visited** — infinite recursion between adjacent cells.
- **Marking *after* recursing** rather than before — same infinite recursion.
- **Un-marking on the way out.** Backtracking behaviour, wrong here: cells get counted into multiple islands.
- **Incrementing inside the DFS** rather than at the scan — you'd count land cells, not islands.
- **Assuming a non-empty grid** without checking `grid[0]` — fine given the constraints, worth a guard in general.

**This same move shows up in:** [Max Area of Island](695-max-area-of-island.md) (this DFS returning a size) · [Surrounded Regions](130-surrounded-regions.md) and [Pacific Atlantic Water Flow](417-pacific-atlantic-water-flow.md) (flood-fill from the borders instead) · [Rotting Oranges](994-rotting-oranges.md) (where BFS is *required*, for the level property) · [Word Search](79-word-search.md) (marking with restoration — the contrast) · [grids primer](../learning/10b-grids-primer.md).

</details>

---
