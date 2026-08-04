# 695. Max Area of Island

**Medium** · [LeetCode](https://leetcode.com/problems/max-area-of-island/)

[📖 11. Graphs lesson](../learning/11-graphs.md) · [📖 Grids primer](../learning/10b-grids-primer.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 11. Graphs problems](../rmap-practice/11-graphs.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

You're given an `m × n` binary matrix `grid`. An **island** is a group of `1`s connected **4-directionally** (horizontal or vertical). You may assume all four edges of the grid are surrounded by water.

The **area** of an island is the number of cells with value `1`. Return the **maximum area** of an island in `grid`, or `0` if there is no island.

```
grid = [[0,0,1,0,0],
        [0,0,1,0,0],       →  4      (the connected group of four 1s)
        [0,1,1,0,0],
        [0,0,0,0,1]]

grid = [[0,0,0,0,0]]  →  0
```

**Constraints:** `1 <= m, n <= 50` · each cell is `0` or `1` (⚠️ **integers** here, unlike [problem 200](200-number-of-islands.md))

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "connected **4-directionally**" | The same implicit grid graph as [Number of Islands](200-number-of-islands.md) |
| "the **area**" | ⚠️ Now you need each component's **size**, not just its existence |
| "the **maximum** area" | Take the best across all components — a running max |
| "`0` if there is no island" | An all-water grid returns 0, which falls out of initializing the max to 0 |
| cells are **integers** `0`/`1` | ⚠️ Compare against `0`, not `"0"` — the opposite of [problem 200](200-number-of-islands.md) |
| 50 × 50 | Small; O(m·n) is trivially fast |

**This is [Number of Islands](200-number-of-islands.md) with one change.** There, the flood-fill returned nothing — it just marked cells. Here it needs to **report how many cells it marked**.

The recursion becomes:

```
area of this component  =  1 (this cell)  +  areas of the four neighbours
```

Water and already-visited cells contribute **0**, which is exactly the right identity — it means the arithmetic works with no special cases.

**That's the same "return a value while traversing" shift** as [Maximum Depth of Binary Tree](104-maximum-depth-of-binary-tree.md) versus [Invert Binary Tree](226-invert-binary-tree.md): the traversal is unchanged, but the function now composes a result on the way back up.

**Why the double-counting worry doesn't apply.** Marking a cell **before** recursing means each cell is added to `visited` exactly once, and every later attempt to reach it returns 0. So each cell contributes exactly 1 to exactly one component's total.

🤔 **Before you open the next section:** the outer scan can now call `dfs` on *every* cell without checking whether it's land first. Why is that safe here, when [problem 200](200-number-of-islands.md) needed the check?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Count components, then re-measure each | Two passes | O(m·n) | ⚠️ Correct, but the first pass already had the information |
| **DFS returning an area** | Compose sizes on the way back up | **O(m·n)** | ✅ |
| BFS counting dequeues | Count cells as the queue drains | O(m·n) | ✅ Equally valid, and safer on deep grids |
| [Union-Find](../data-structures/union-find.md) with sizes | Track component sizes during unions | O(m·n·α) | ⚠️ Overkill unless edges arrive dynamically |

**The decision: the [Number of Islands](200-number-of-islands.md) flood-fill, with the DFS returning a count.**

Three small changes from that problem:

| | [200](200-number-of-islands.md) | **695** |
|---|---|---|
| Base cases return | *nothing* | **`0`** |
| After marking | recurse | `area = 1`, then **accumulate** neighbour areas |
| Outer scan | count components | **`best = max(best, dfs(...))`** |

**Why returning 0 from the base cases is exactly right.** Out of bounds, water, and already-visited all contribute nothing to the area — and 0 is the additive identity, so `area += 0` leaves the total untouched. **No branching needed**, the same trick as the `max(branch, 0)` clamp in [Binary Tree Maximum Path Sum](124-binary-tree-maximum-path-sum.md).

**Why the outer loop needs no land check.** [Problem 200](200-number-of-islands.md) had to test `grid[row][col] == "1"` before calling `dfs`, because calling it on water would have wrongly incremented the island count. Here, `dfs` on water simply returns **0**, and `max(best, 0)` changes nothing — so the guard is unnecessary.

That's a small but genuine simplification worth noticing: **when your function returns a value with a harmless identity, guard clauses often disappear.**

**Why `visited` still matters.** Without it, adjacent cells would recurse into each other forever. And since a cell belongs to exactly one island, the marking is **permanent** — not backtracked, exactly as in [problem 200](200-number-of-islands.md).

**BFS is equally valid**, counting cells as they're dequeued — and it avoids the recursion-depth risk on large grids.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
rows = len(grid)
cols = len(grid[0])
visited = set()
```

Same setup as [Number of Islands](200-number-of-islands.md) — dimensions and a set of visited coordinates.

There's no counter here; the answer is a running maximum computed in the scan below.
→ [set-basics](../syntax/set-basics.md) · [nested-lists](../syntax/nested-lists.md)

```python
def dfs(row, col):
    if row < 0 or row >= rows or col < 0 or col >= cols:
        return 0
    if grid[row][col] == 0 or (row, col) in visited:
        return 0
```

**The base cases now return `0`** — out of bounds, water, and already-visited cells all contribute nothing to an island's area.

Returning 0 rather than nothing is what lets the accumulation below work without special cases.

⚠️ **`== 0`, no quotes.** This grid holds integers, unlike [problem 200](200-number-of-islands.md)'s strings — an easy thing to carry over wrongly between the two.
→ [function-basics](../syntax/function-basics.md) · [membership-operators](../syntax/membership-operators.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
    visited.add((row, col))
    area = 1
```

**Mark first, then count this cell.**

Marking before recursing prevents infinite mutual recursion between neighbours, and guarantees each cell is counted into exactly one island.

`area = 1` is this cell's own contribution.
→ [set-operations](../syntax/set-operations.md)

```python
    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        area += dfs(row + dr, col + dc)
    return area
```

**Accumulate the four neighbours' areas.**

This is the change from [problem 200](200-number-of-islands.md): the recursion now *composes a value* rather than just marking. Water and visited neighbours return 0 and add nothing.

The result is the total size of the connected component reachable from this cell.
→ [tuple-unpacking](../syntax/tuple-unpacking.md) · [for-loop](../syntax/for-loop.md) · [recursion-basics](../syntax/recursion-basics.md)

```python
best = 0
for row in range(rows):
    for col in range(cols):
        best = max(best, dfs(row, col))
return best
```

**Scan every cell, keeping the running maximum.**

No land check is needed — `dfs` on water or a visited cell returns 0, and `max(best, 0)` is a no-op. That's why this loop is simpler than [problem 200](200-number-of-islands.md)'s.

`best = 0` also handles the all-water case: the loop runs, everything returns 0, and 0 is returned ✅
→ [min-max-key](../syntax/min-max-key.md) · [range-function](../syntax/range-function.md)

<details>
<summary>The whole thing together</summary>

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

</details>

**Trace it** — the example grid:

```
        col: 0  1  2  3  4
row 0:       0  0  1  0  0
row 1:       0  0  1  0  0
row 2:       0  1  1  0  0
row 3:       0  0  0  0  1
```

| Scan reaches | `dfs` returns | Why | `best` |
|---|---|---|---|
| (0,0)–(0,1) | **0** | water | 0 |
| **(0,2)** | **4** | floods (0,2),(1,2),(2,2),(2,1) | **4** |
| (0,3),(0,4) | 0 | water | 4 |
| (1,2) | **0** | already visited | 4 |
| (2,1),(2,2) | 0 | already visited | 4 |
| **(3,4)** | **1** | a lone land cell | 4 |

Answer: **4** ✅

The recursion at (0,2), unwinding:

| Cell | Own | Neighbour contributions | Returns |
|---|---|---|---|
| (2,1) | 1 | all water/visited → 0 | **1** |
| (2,2) | 1 | (2,1)=1, rest 0 | **2** |
| (1,2) | 1 | (2,2)=2, rest 0 | **3** |
| (0,2) | 1 | (1,2)=3, rest 0 | **4** ✅ |

Each cell counted exactly once, composed bottom-up — and the later visits to (1,2) and (2,2) from the outer scan correctly return 0.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(m · n)</summary>

**O(m · n)** — identical to [Number of Islands](200-number-of-islands.md).

Each cell is added to `visited` exactly once and can be *reached* at most 5 times (four neighbours plus the outer scan), each an O(1) set lookup that returns immediately.

Total work: O(5·m·n) = **O(m·n)**.

At 50 × 50 = 2,500 cells, that's ~12,500 operations.

**Note the outer scan calls `dfs` on every cell**, not just land — that's up to m·n extra calls compared to [problem 200](200-number-of-islands.md). Each returns in O(1) though, so the asymptotic cost is unchanged. **A slightly larger constant bought for simpler code**, which is the right trade here.

**Optimal** — every cell must be examined to know whether it's land.

**Versus a two-pass approach** (find components, then measure each): also O(m·n), but it re-traverses each island. The single pass gets the size for free because the recursion is already visiting every cell of the component — the same "the traversal already has the information" realization as [Diameter of Binary Tree](543-diameter-of-binary-tree.md).

</details>

<details>
<summary><b>5 · Space complexity</b> — O(m · n)</summary>

**O(m · n)**, from the `visited` set and the recursion stack.

| Component | Worst case |
|---|---|
| `visited` set | every cell → **O(m·n)** |
| Recursion stack | one frame per cell on an all-land grid → **O(m·n)** |

**At 50 × 50 the recursion depth maxes at 2,500** — which *does* exceed Python's default limit of 1000 on an all-land grid, raising `RecursionError`.

That's a real risk at these constraints (unlike, say, a 10-element array), and worth naming. **BFS avoids it entirely**, using a queue bounded by the frontier rather than a stack bounded by the component size:

```python
from collections import deque
queue = deque([(row, col)])
visited.add((row, col))
area = 0
while queue:
    r, c = queue.popleft()
    area += 1
    for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
        ...
```

**The in-place alternative** drops `visited` to O(1) by setting `grid[row][col] = 0` after counting it — the cell becomes water, so it's never revisited. Mutates the input, but halves the memory.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "This is Number of Islands with one change: instead of the flood-fill just marking cells, it returns how many it marked. So the recursion becomes 'this cell counts as 1, plus the areas of my four neighbours', and the base cases return 0 — out of bounds, water, and already-visited all contribute nothing, which is exactly the additive identity so no special casing is needed. Marking before recursing guarantees each cell is counted into exactly one island. The outer scan doesn't even need to check for land, because calling the DFS on water returns 0 and the running max ignores it. O(m·n) time and space. On a 50×50 all-land grid the recursion depth would be 2,500, past Python's limit, so I'd use BFS there."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "How does this differ from [Number of Islands](200-number-of-islands.md)?" | **The question.** The DFS returns an area instead of nothing; base cases return 0; the outer loop takes a max instead of counting. |
| "Why doesn't the outer loop check for land?" | `dfs` on water returns 0 and `max(best, 0)` is a no-op, so the guard is redundant here. |
| "What if the grid is all land?" | Recursion depth hits m·n — past Python's limit at these constraints. Use BFS or an iterative stack. |
| "Reduce the space." | Set each counted cell to 0 in the grid instead of using a `visited` set — O(1) space, mutates the input. |
| "Return the number of islands **and** the max area?" | One pass: count components in the outer loop while tracking the max returned area. |
| "What if you could flip one 0 to 1 to maximize the area?" | Label each island with an id and its size, then for each water cell sum the *distinct* neighbouring island sizes + 1. LeetCode 827. |
| "Count perimeter instead of area?" | Add 1 for each neighbour that's water or out of bounds, rather than counting cells. |

**Traps:**

- **Comparing `grid[row][col] == "0"`** — this grid holds **integers**. Carrying the string comparison over from [problem 200](200-number-of-islands.md) makes every cell look like land.
- **Base cases returning `None`** instead of `0` — `area += None` raises `TypeError`.
- **Marking after recursing** — infinite mutual recursion between neighbours.
- **Un-marking on the way out.** Backtracking behaviour; cells would be counted into several islands.
- **Initializing `area = 0`** and then adding neighbours — forgets to count the current cell.
- **`best = float('-inf')`** — an all-water grid should return 0, not negative infinity.

**This same move shows up in:** [Number of Islands](200-number-of-islands.md) (the same flood-fill, counting components) · [Maximum Depth of Binary Tree](104-maximum-depth-of-binary-tree.md) (a traversal that composes a value on the way back up) · [Pacific Atlantic Water Flow](417-pacific-atlantic-water-flow.md) (flood-fill with a different marking rule) · [grids primer](../learning/10b-grids-primer.md).

</details>
