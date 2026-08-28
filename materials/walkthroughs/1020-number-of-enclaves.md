# 1020. Number of Enclaves

**Medium** · [LeetCode](https://leetcode.com/problems/number-of-enclaves/) · [Solution file (no hints)](../../problems/1000-1499/1020.py)

[📖 11. Graphs lesson](../learning/11-graphs.md) · [📖 Grids primer](../learning/10b-grids-primer.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 11. Graphs problems](../rmap-practice/11-graphs.md)

---

In a binary grid (`1` = land, `0` = sea), return the number of land cells from which you **cannot** walk off the boundary, moving 4-directionally between land cells.

```
grid = [[0,0,0,0],          →  3      the three 1s in the middle are enclosed
        [1,0,1,0],
        [0,1,1,0],
        [0,0,0,0]]

grid = [[0,1,1,0],          →  0      all land connects to the boundary
        [0,0,1,0],
        [0,0,1,0],
        [0,0,0,0]]
```

**Constraints:** `1 <= m, n <= 500`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "walking **off the boundary**" | A cell escapes if its component touches any edge of the grid |
| "**cannot** walk off" | ⚠️ You want the **complement** — count what *doesn't* escape |
| "count land **cells**" | Cells, not components (unlike [Number of Islands](200-number-of-islands.md)) |
| 4-directionally | No diagonals |
| `m, n <= 500` | ⚠️ 250,000 cells. A component can be that large — **recursion depth is a real risk** |

**The inversion that makes this easy.** The direct reading — "for each land cell, can it reach the border?" — invites running a search per cell: O((m·n)²) in the worst case. Don't.

**Flip it.** Instead of asking which cells escape, **remove everything that escapes**, then count what's left:

```
1. Flood-fill from every land cell ON the border, sinking each component to 0
2. Whatever 1s remain are, by definition, unable to reach the border
3. Sum them
```

Every component either touches the border or it doesn't. Step 1 deletes exactly the touching ones, so the survivors are exactly the answer. **One pass over the border, one pass to count — no per-cell searching.**

```
grid = [[0,0,0,0],        border land cells: (1,0)
        [1,0,1,0],
        [0,1,1,0],        sink the component containing (1,0):
        [0,0,0,0]]           it's isolated → just that one cell

after: [[0,0,0,0],        remaining 1s: (1,2), (2,1), (2,2)  →  3 ✅
        [0,0,1,0],
        [0,1,1,0],
        [0,0,0,0]]
```

**Note the middle blob does touch cell (1,2), (2,1), (2,2)** — three connected land cells, none on the border, so none escapes. The lone `1` at `(1,0)` is on the left edge, so it's removed.

**This "seed from the border" pattern is the whole idea**, and it's the same one as [Surrounded Regions](130-surrounded-regions.md) and [Pacific Atlantic Water Flow](417-pacific-atlantic-water-flow.md). Whenever a problem asks about cells that *can't* reach an edge, search **from** the edge rather than toward it:

| Problem | Seed from the border | Then |
|---|---|---|
| [Surrounded Regions](130-surrounded-regions.md) | mark `O`s reachable from the edge | flip the unmarked ones |
| [Pacific Atlantic](417-pacific-atlantic-water-flow.md) | mark cells reachable from each ocean | intersect |
| **Number of Enclaves** | **sink land reachable from the edge** | **count what's left** |

🤔 **Before you open the next section:** why seed the search from the border rather than from each land cell? How many searches does each approach need?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Per-cell escape check | For each land cell, search for the border | O((m·n)²) | ❌ 6·10¹⁰ at 500×500 |
| Component-wise check | Flood each component, note whether it touched the edge | O(m·n) | ✅ Correct; two-phase, more bookkeeping |
| **Sink from the border, then count** | Remove escaping land, sum the rest | **O(m·n)** | ✅ ← |
| Union-Find with a virtual "outside" node | Union border land to a sentinel | O(m·n·α) | ✅ Works, heavier |

**The decision: flood-fill from every border land cell, then count the survivors.**

**Why it beats the component-wise version**, which is also O(m·n): that one must traverse each component while tracking a "did I touch the edge?" flag, then either re-traverse to count or accumulate cells in a list to conditionally add. The border-seeded version needs **no flag and no second decision** — escaping cells are simply gone, so `sum` is the entire counting step.

**Marking by mutation.** Setting escaping land to `0` does three jobs at once:

| Job | How |
|---|---|
| Records "visited" | A `0` fails the `!= 1` test, so the search won't re-enter |
| Records "escapes" | It's no longer land, so it can't be counted |
| Enables the final count | `sum(sum(row))` counts exactly the survivors |

No `visited` set is needed — the same trick as [Flood Fill](733-flood-fill.md) and [Number of Islands](200-number-of-islands.md). ⚠️ **It destroys the input**, which matters if the caller needs the grid afterwards.

**Seeding the border correctly** — note the deliberate overlap:

```python
for r in range(rows):
    sink(r, 0); sink(r, cols - 1)        # left and right columns
for c in range(cols):
    sink(0, c); sink(rows - 1, c)        # top and bottom rows
```

The four corners are each visited twice. **Harmless** — the second call finds a `0` and returns immediately. Writing fiddly range arithmetic to avoid the overlap adds bugs and saves four O(1) calls.

⚠️ **Single-row or single-column grids** are covered by this too: at `rows == 1`, `sink(0, c)` and `sink(rows-1, c)` are the same call, and every cell is a border cell — so the answer is correctly **0**.

**⚠️ The recursion-depth concern is real here.** At 500×500 a solid land grid is one component of **250,000 cells**, and recursive DFS can nest that deep — 250× Python's default limit of 1,000. Unlike [Flood Fill](733-flood-fill.md) (max 2,500 cells) this isn't marginal.

| Approach | Depth risk at 500×500 |
|---|---|
| Recursive DFS | ⚠️ **250,000 frames** |
| **BFS with a deque** | ✅ Heap-allocated queue |
| Iterative DFS | ✅ Heap-allocated stack |

The recursive version below is the clearest expression of the idea and usually passes because the recursion snakes rather than nesting maximally — but **say the concern out loud and name BFS as the fix.**
→ [recursion-limit](../syntax/recursion-limit.md)

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
rows, cols = len(grid), len(grid[0])
```

Dimensions hoisted out of the recursion. `grid[0]` is safe — constraints guarantee at least one row.
→ [nested-lists](../syntax/nested-lists.md) · [multiple-return-values](../syntax/multiple-return-values.md)

```python
def sink(r, c):
    if r < 0 or r >= rows or c < 0 or c >= cols:
        return
    if grid[r][c] != 1:
        return
```

**Two guards, bounds first.**

⚠️ The bounds check **must** precede the indexing. Python's negative indexing means `grid[-1][c]` silently reads the **last row** instead of raising — so a missing `r < 0` check makes the fill wrap around the grid and quietly delete land it shouldn't. **Silent wrong answers, not crashes**, which is what makes this the dangerous omission in every grid problem.

`grid[r][c] != 1` rejects sea **and** already-sunk cells in one test — the mutation is the visited mark.
→ [comparison-operators](../syntax/comparison-operators.md) · [logical-operators](../syntax/logical-operators.md)

```python
    grid[r][c] = 0
    sink(r+1, c); sink(r-1, c); sink(r, c+1); sink(r, c-1)
```

**Sink it and recurse into all four neighbours.** No bounds checks at the call sites — the callee's first line handles them.
→ [recursion-basics](../syntax/recursion-basics.md)

```python
for r in range(rows):
    sink(r, 0)
    sink(r, cols - 1)

for c in range(cols):
    sink(0, c)
    sink(rows - 1, c)
```

**Seed from every border cell.** The two loops cover left/right columns and top/bottom rows respectively.

`sink` returns immediately on sea cells, so seeding *every* border cell rather than only the land ones costs nothing and removes a condition.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md)

```python
return sum(sum(row) for row in grid)
```

**Count the survivors.** Since land is `1` and everything else is `0`, summing the grid counts remaining land — and every remaining land cell is, by construction, unable to reach the border.

The inner `sum(row)` totals a row; the generator feeds those to the outer `sum`.
→ [generator-expressions](../syntax/generator-expressions.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def numEnclaves(self, grid: List[List[int]]) -> int:

        rows, cols = len(grid), len(grid[0])

        def sink(r, c):
            if r < 0 or r >= rows or c < 0 or c >= cols:
                return
            if grid[r][c] != 1:
                return
            grid[r][c] = 0
            sink(r + 1, c)
            sink(r - 1, c)
            sink(r, c + 1)
            sink(r, c - 1)

        for r in range(rows):
            sink(r, 0)
            sink(r, cols - 1)

        for c in range(cols):
            sink(0, c)
            sink(rows - 1, c)

        return sum(sum(row) for row in grid)
```

</details>

<details>
<summary>The BFS version, safe at 500×500</summary>

```python
class Solution:
    def numEnclaves(self, grid: List[List[int]]) -> int:

        rows, cols = len(grid), len(grid[0])
        queue = deque()

        for r in range(rows):
            for c in (0, cols - 1):
                if grid[r][c] == 1:
                    grid[r][c] = 0
                    queue.append((r, c))
        for c in range(cols):
            for r in (0, rows - 1):
                if grid[r][c] == 1:
                    grid[r][c] = 0
                    queue.append((r, c))

        while queue:
            r, c = queue.popleft()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 0
                    queue.append((nr, nc))

        return sum(sum(row) for row in grid)
```

Same O(m·n), no stack-depth risk. Note `0 <= nr < rows` — a **chained comparison**, which reads better than two clauses.
→ [chained-comparisons](../syntax/chained-comparisons.md) · [deque-basics](../syntax/deque-basics.md)

</details>

**Trace it** — Example 1, `grid = [[0,0,0,0],[1,0,1,0],[0,1,1,0],[0,0,0,0]]`:

**Phase 1 — seed the border.** The only border cell holding land is `(1,0)`:

| Seeded cell | Value | Action |
|---|---|---|
| `(0,0)`, `(0,3)`, `(2,0)`, `(3,0)`, `(3,3)`, … | `0` | sea → return immediately |
| **`(1,0)`** | **`1`** | **sink it**, then recurse |
| ↳ `(2,0)`, `(0,0)`, `(1,1)` | `0` | all sea → return |

Only one cell is removed — `(1,0)`'s component is just itself.

**Grid after phase 1:**

```
before                after
0 0 0 0               0 0 0 0
1 0 1 0      →        0 0 1 0      ← the border 1 is gone
0 1 1 0               0 1 1 0
0 0 0 0               0 0 0 0
```

**Phase 2 — count.** Remaining 1s: `(1,2)`, `(2,1)`, `(2,2)` → **3** ✅

**The surviving blob never touches an edge.** Rows 0 and 3 and columns 0 and 3 are all sea around it, so no border seed can reach it — which is exactly the definition of an enclave.

**Example 2** (`[[0,1,1,0],[0,0,1,0],[0,0,1,0],[0,0,0,0]]`): the land at `(0,1)` and `(0,2)` sits on the **top row**, so those are border seeds. Sinking `(0,2)` cascades down the column through `(1,2)` and `(2,2)`. Every land cell is connected to the top edge, so all are removed → **0** ✅

**A one-cell grid** `[[1]]` returns **0**: the single cell is on the border (all four edges at once), gets sunk in phase 1, and nothing remains. Correct — you can step off the boundary from it immediately.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(m · n)</summary>

**O(m · n)**.

| Phase | Cost |
|---|---|
| Seed the border | **O(m + n)** calls, each O(1) to reject or the start of a flood |
| All flood-fills combined | **O(m·n)** — each cell sunk at most once |
| Final sum | **O(m·n)** |
| **Total** | **O(m·n)** |

At 500×500 that's 250,000 cells — a few hundred thousand operations.

**The flood-fills don't compound.** Border seeding may launch many searches, but a cell can only be sunk once — after that it's `0` and every later search rejects it in O(1). So the *total* work across all floods is bounded by the grid size, not by (number of seeds) × (grid size).

**This is optimal**: every cell must be examined, since any one could be an unexamined enclave. **Ω(m·n) is the lower bound.**

**Versus the per-cell approach**, O((m·n)²): a search from each of up to 250,000 land cells, each potentially scanning 250,000 cells ≈ **6·10¹⁰ operations**. Completely infeasible.

**The saving comes from the inversion.** Searching *from* the border needs O(m+n) seeds covering every escaping component exactly once; searching *toward* the border needs one search per cell and re-derives the same connectivity over and over. **Same graph, same traversal — the direction of the question is what changes the complexity.** That's the transferable lesson.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(m · n) worst case</summary>

**O(m · n)** in the worst case, from the traversal structure — **not** from any `visited` set.

| Component | Size |
|---|---|
| `visited` structure | **none** — mutation is the mark → **O(1)** |
| **Recursion stack / BFS queue** | up to the size of one component → **O(m·n)** |
| Output | one integer → **O(1)** |

**No `visited` set** is the win from mutating the grid — 250,000 entries saved at 500×500. The cost is that **the input is destroyed**, which is worth stating: if the caller needs the grid, copy it first (O(m·n)) or track a separate `visited` set.

⚠️ **The recursive version's O(m·n) lives on the call stack**, and at 500×500 that's up to **250,000 frames — 250× Python's default limit of 1,000.** This is not marginal:

| Approach | Where the O(m·n) lives | Risk at 500×500 |
|---|---|---|
| Recursive DFS | **call stack** | ⚠️ **RecursionError** |
| BFS with a deque | heap | ✅ None |
| Iterative DFS | heap | ✅ None |

Same asymptotic space, entirely different failure behaviour. **A fully-land 500×500 grid is a legal input**, so BFS is the defensible choice here even though the recursive version reads more clearly.

**Compare [Flood Fill](733-flood-fill.md)**, where the grid is at most 50×50 = 2,500 cells: the same concern exists but is far milder. **The constraint decides, not the algorithm** — check it every time.
→ [recursion-limit](../syntax/recursion-limit.md)

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The direct reading is 'for each land cell, can it reach the border?', which would be a search per cell and quadratic. So I invert it: I flood-fill inward from every land cell on the border, sinking each escaping component to sea, and then whatever 1s remain are exactly the cells that can't get out — I just sum them. Setting cells to 0 doubles as the visited mark, so no visited set is needed, though it does destroy the input. Seeding all four edges lets the corners get visited twice, which is harmless since the second call sees sea and returns. O(m·n) time, because each cell is sunk at most once no matter how many seeds there are, and it's optimal since every cell must be examined. The one caveat is depth: at 500×500 a solid land grid is a single 250,000-cell component, which would recurse far past Python's limit — so I'd use BFS with a deque rather than recursion."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why search from the border?" | **The question.** O(m+n) seeds cover every escaping component once. Searching from each cell re-derives the same connectivity — O((m·n)²). |
| "Why is the total still O(m·n) with many seeds?" | A cell can be sunk only once; afterwards every search rejects it in O(1). The floods can't compound. |
| "What breaks at 500×500?" | Recursive DFS — a solid grid is one 250,000-cell component, 250× Python's stack limit. Use BFS. |
| "Can you avoid mutating the input?" | Use a `visited` set of coordinates — O(m·n) extra space — or copy the grid first. |
| "Corners seeded twice?" | Harmless: the second call sees `0` and returns. Avoiding it costs clarity for no gain. |
| "1×n or m×1 grids?" | Every cell is a border cell, so the answer is always 0. The code handles it without a special case. |
| "Count *components* instead of cells?" | Same phase 1, then run [Number of Islands](200-number-of-islands.md) on the survivors. |
| "Relation to [Surrounded Regions](130-surrounded-regions.md)?" | Identical technique — that one flips survivors to `X`, this one counts them. |
| "8-directional movement?" | Add the four diagonals to the neighbour list. Everything else is unchanged. |

**Traps:**

- **Searching from each land cell** toward the border — correct but O((m·n)²), infeasible here.
- **Omitting the `r < 0` / `c < 0` bounds checks.** Python's negative indexing wraps to the far edge, so land is deleted from the wrong side **with no error**.
- **Checking `grid[r][c]` before the bounds test** — `IndexError` on the high side, silent wrap on the low side.
- **Recursing on a 500×500 grid** without considering depth.
- **Forgetting that both the first and last row/column are borders** — seeding only the top and left misses half the escape routes.
- **Counting before sinking** — the phases are ordered; sum last.
- **Adding a `visited` set on top of the mutation** — redundant.
- **Assuming the grid is square** — `rows` and `cols` are independent; mixing them up passes the square examples and fails on rectangles.

**This same move shows up in:** [Surrounded Regions](130-surrounded-regions.md) (the same border-seeded flood, flipping instead of counting) · [Pacific Atlantic Water Flow](417-pacific-atlantic-water-flow.md) (seeded from two borders, then intersected) · [Number of Islands](200-number-of-islands.md) and [Max Area of Island](695-max-area-of-island.md) (the same sink-as-you-go traversal) · [Flood Fill](733-flood-fill.md) (the underlying template) · [dfs](../algorithms/dfs.md) · [bfs](../algorithms/bfs.md) · [graph](../data-structures/graph.md).

</details>

---
