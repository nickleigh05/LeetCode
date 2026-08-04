# 130. Surrounded Regions

**Medium** · [LeetCode](https://leetcode.com/problems/surrounded-regions/)

[📖 11. Graphs lesson](../learning/11-graphs.md) · [📖 Grids primer](../learning/10b-grids-primer.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 11. Graphs problems](../rmap-practice/11-graphs.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Given an `m × n` matrix `board` containing `'X'` and `'O'`, **capture all regions that are 4-directionally surrounded by `'X'`**.

A region is captured by flipping all `'O'`s into `'X'`s **in that surrounded region**. Modify the board **in place**.

```
before:  X X X X          after:  X X X X
         X O O X                  X X X X
         X X O X                  X X X X
         X O X X                  X O X X
                                    ↑ this O touches the border, so it survives
```

**Constraints:** `1 <= m, n <= 200` · each cell is `'X'` or `'O'`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**surrounded** by `'X'`" | Enclosed on all sides — no escape route to the edge |
| "capture… **in that region**" | ⚠️ It's all-or-nothing per **connected component**: if any cell escapes, the whole region survives |
| "modify **in place**" | Mutate `board`; return nothing |
| 200 × 200 | O(m·n) expected; recursion depth is a real concern |

**The definition worth restating.** A region of `'O'`s is captured **unless** some cell in it touches the border. One escape route saves the entire component.

**Why the direct approach is awkward.** For each `'O'` region, flood-fill it and check whether any cell is on the border. That works, but you must explore the whole region *before* deciding, then go back and flip it — two passes per region, with bookkeeping to remember which cells belonged to which region.

**The inversion that simplifies everything:** instead of finding what's *captured*, find what's **safe**.

> A cell is safe **iff** it's connected to a border `'O'`.

So flood-fill inward from every border `'O'`, marking everything reachable as safe. Then:

- Anything still `'O'` was **never reached** ⇒ it has no border connection ⇒ **capture it**.
- Anything marked safe ⇒ **restore it to `'O'`**.

**One pass, no region bookkeeping** — the mark itself carries the decision. Same reversal as [Pacific Atlantic Water Flow](417-pacific-atlantic-water-flow.md): *searching from the boundary is cheaper than testing every interior cell.*

**The three-state trick.** During the flood-fill you need to distinguish three things: captured `'O'`, safe `'O'`, and `'X'`. A temporary third symbol `'T'` marks the safe cells, and a final sweep converts:

```
'O' → 'X'    (surrounded — capture)
'T' → 'O'    (safe — restore)
'X' → 'X'    (unchanged)
```

🤔 **Before you open the next section:** why does the temporary marker have to be a *third* symbol, rather than just flipping safe cells to `'X'` and back?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Verdict |
|---|---|---|
| Flood-fill each region, check for a border cell | Explore, decide, then flip | ⚠️ Correct; needs to remember each region's cells |
| **Flood-fill from the borders, mark safe** | Invert the question | ✅ |
| [Union-Find](../data-structures/union-find.md) with a virtual "border" node | Union every border `'O'` to a sentinel; capture anything not connected to it | ✅ Elegant; more machinery |

**The decision: flood-fill inward from every border `'O'`, marking reachable cells `'T'`, then sweep.**

The three phases:

1. **Mark.** DFS from each `'O'` on any edge, converting reachable `'O'`s to `'T'`.
2. **Capture.** Every remaining `'O'` is surrounded → `'X'`.
3. **Restore.** Every `'T'` was safe → `'O'`.

**Why a third symbol is necessary.** You can't mark safe cells as `'X'` (you'd lose track of which were originally `'O'`), and you can't leave them as `'O'` (you couldn't distinguish them from captured ones). `'T'` gives the third state, and **the marker doubles as the visited set** — costing O(1) space instead of O(m·n).

That's the same in-place marking as [Rotting Oranges](994-rotting-oranges.md) and [Word Search](79-word-search.md) — with the key difference from Word Search that here **the mark is permanent** during the traversal, since you're computing reachability rather than exploring alternative paths.

**Why `board[row][col] != "O"` is the right stop condition.** It rejects three cases at once: `'X'` (a wall), `'T'` (already marked safe — the visited check), and out-of-range values. **One comparison handling both the wall rule and cycle prevention.**

**Why seeding only the borders is sufficient.** Any safe region *must* contain a border cell by definition, so starting from every border `'O'` reaches every safe cell. Interior regions with no border contact are never touched — which is exactly what identifies them as captured.

**The Union-Find alternative** connects every border `'O'` to a virtual node, unions adjacent `'O'`s, and captures anything not sharing a root with that node. Elegant, and the natural choice if the board changed dynamically — but heavier for a one-shot pass.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
rows = len(board)
cols = len(board[0])
```

Dimensions for the bounds checks. Note the function returns `None` — the board is modified in place, as the problem requires.
→ [nested-lists](../syntax/nested-lists.md) · [list-basics](../syntax/list-basics.md)

```python
def dfs(row, col):
    if row < 0 or row >= rows or col < 0 or col >= cols:
        return
    if board[row][col] != "O":
        return
```

Bounds check, then the stop condition.

**`!= "O"` covers three cases in one test:** `'X'` is a wall, `'T'` means already marked (the visited check), and anything else is invalid. No separate `visited` structure is needed.
→ [function-basics](../syntax/function-basics.md) · [closures](../syntax/closures.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
    board[row][col] = "T"   # temporary mark: connected to the border, safe
    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        dfs(row + dr, col + dc)
```

**Mark as safe, then spread.** Writing `'T'` before recursing is what prevents infinite recursion between adjacent `'O'`s — the mark *is* the visited flag.

The four-direction list is the standard grid idiom from the [grids primer](../learning/10b-grids-primer.md).

**No un-marking** — unlike [Word Search](79-word-search.md), this is permanent. A cell reachable from the border is safe, full stop.
→ [tuple-unpacking](../syntax/tuple-unpacking.md) · [for-loop](../syntax/for-loop.md) · [recursion-basics](../syntax/recursion-basics.md)

```python
for row in range(rows):
    dfs(row, 0)
    dfs(row, cols - 1)
for col in range(cols):
    dfs(0, col)
    dfs(rows - 1, col)
```

**Seed from all four borders** — left and right columns, then top and bottom rows.

Calling `dfs` on an `'X'` border cell is harmless: the stop condition returns immediately. So there's no need to check for `'O'` first.

Corners get called twice; the second call finds `'T'` and returns.
→ [range-function](../syntax/range-function.md)

```python
for row in range(rows):
    for col in range(cols):
        if board[row][col] == "O":
            board[row][col] = "X"
        elif board[row][col] == "T":
            board[row][col] = "O"
```

**The final sweep, converting both states:**

- Still `'O'` ⇒ never reached from any border ⇒ **surrounded** ⇒ capture as `'X'`.
- `'T'` ⇒ reached ⇒ **safe** ⇒ restore to `'O'`.

`'X'` cells match neither branch and are left untouched.
→ [elif-else](../syntax/elif-else.md) · [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

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

</details>

**Trace it** — the example board:

```
initial:      X X X X
              X O O X
              X X O X
              X O X X
```

**Phase 1 — flood-fill from the borders.** The only border `'O'` is at **(3,1)**:

| Seed | Reaches | Result |
|---|---|---|
| (3,1) | itself; neighbours (2,1)=`X`, (3,0)=`X`, (3,2)=`X` | only (3,1) → `'T'` |

Every other border cell is `'X'`, so the DFS returns immediately.

```
after marking:  X X X X
                X O O X       ← these O's were never reached
                X X O X
                X T X X       ← safe
```

**Phase 2 — the sweep:**

| Cell | Was | Becomes |
|---|---|---|
| (1,1), (1,2), (2,2) | `'O'` | **`'X'`** — surrounded |
| (3,1) | `'T'` | **`'O'`** — restored |
| all others | `'X'` | unchanged |

```
final:   X X X X
         X X X X
         X X X X
         X O X X      ✅
```

The interior region `{(1,1), (1,2), (2,2)}` was fully enclosed and got captured; `(3,1)` touched the bottom edge and survived.

**Note what never happened:** no region was explored to "check if it touches the border". The interior region was simply *never visited*, and that absence is the answer.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(m · n)</summary>

**O(m · n)**.

| Phase | Cost |
|---|---|
| Border seeding | O(m + n) calls, each O(1) to reject or the start of a flood-fill |
| All flood-fills combined | each cell marked `'T'` at most once → **O(m·n)** |
| Final sweep | O(m·n) |

**O(m·n)** total. At 200 × 200 = 40,000 cells, ~10⁵ operations.

**Every cell is visited a constant number of times.** A cell becomes `'T'` once; later attempts to reach it hit `!= "O"` and return immediately. With up to 4 neighbours plus the seeding, that's a small constant.

**Versus flood-filling each region and checking for border membership:** also O(m·n), but it needs to *remember* each region's cells to flip them afterwards — an extra O(m·n) structure and a second pass per region. **Inverting the question removes that bookkeeping entirely.**

**Optimal** — every cell must be examined to know whether it's an `'O'` and whether it's reachable.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(m · n)</summary>

**O(m · n)** in the worst case — entirely from the **recursion stack**.

| Component | Size |
|---|---|
| `'T'` marking | **O(1)** — reuses the board |
| Recursion stack | up to m·n frames on a board that's all `'O'` → **O(m·n)** |

**The in-place marking is the space win.** A `visited` set would cost O(m·n); the third symbol costs nothing, because the board already has room for the information. **That's why a *temporary* marker is used rather than a separate structure.**

⚠️ **The recursion depth is a genuine risk here.** A 200 × 200 board that's entirely `'O'` gives a single connected region of 40,000 cells — **far past Python's default recursion limit of 1000**.

**BFS is the safe implementation at these constraints:**

```python
from collections import deque
def bfs(r, c):
    if board[r][c] != "O": return
    queue = deque([(r, c)])
    board[r][c] = "T"
    while queue:
        row, col = queue.popleft()
        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == "O":
                board[nr][nc] = "T"
                queue.append((nr, nc))
```

Same O(m·n), but the queue holds only the frontier instead of the whole path.
→ [recursion-limit](../syntax/recursion-limit.md)

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "A region is captured unless some cell in it touches the border, so rather than exploring each region and then deciding, I invert it: flood-fill inward from every border `'O'` and mark everything reachable as safe. Anything still `'O'` afterwards was never reached, which means it has no escape route — so it gets captured. I use a temporary third symbol `'T'` for the safe cells, because I need to distinguish captured `'O'`s from safe ones, and the marker doubles as the visited set so it costs no extra space. Then one sweep converts: remaining `'O'` to `'X'`, and `'T'` back to `'O'`. That avoids tracking which cells belong to which region. O(m·n) time — and at 200×200 I'd write it as BFS, since an all-`'O'` board would blow the recursion limit."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why search from the borders?" | **The question.** Safety is defined by border connection, so marking what's safe is direct — while checking each region requires exploring it before deciding. |
| "Why a third symbol?" | You must distinguish safe `'O'`s from captured ones. `'X'` would lose the information; leaving them `'O'` would make them indistinguishable. |
| "What if the board is all `'O'`?" | One 40,000-cell region — DFS recursion overflows. Use BFS. |
| "Solve it with Union-Find." | Union every `'O'` with its `'O'` neighbours, and union border `'O'`s to a virtual node. Capture anything not sharing that root. |
| "What if `'T'` could appear in the input?" | Pick a marker outside the alphabet, or use an explicit `visited` set at O(m·n) space. |
| "Could you avoid the third symbol?" | Yes — with a `visited` set instead. Same result, O(m·n) extra space. |
| "How does this relate to [Pacific Atlantic](417-pacific-atlantic-water-flow.md)?" | Same inversion: flood-fill from the boundary rather than testing every interior cell. |

**Traps:**

- **Flipping safe cells to `'X'`** during the flood-fill — you'd lose track of which were originally `'O'`.
- **Forgetting the final restore pass** — safe regions stay marked `'T'` and the board is corrupted.
- **Marking after recursing** instead of before — infinite recursion between adjacent `'O'`s.
- **Seeding only interior cells**, or scanning all cells rather than just the borders — wasteful, and it defeats the inversion.
- **Un-marking on the way out.** Backtracking behaviour; wrong here, since safety is permanent.
- **Returning a new board.** The problem requires in-place modification.

**This same move shows up in:** [Pacific Atlantic Water Flow](417-pacific-atlantic-water-flow.md) (the same border-inward inversion) · [Number of Islands](200-number-of-islands.md) (the flood-fill skeleton) · [Rotting Oranges](994-rotting-oranges.md) (in-place marking during traversal) · [Word Search](79-word-search.md) (marking *with* restoration — the contrast) · [grids primer](../learning/10b-grids-primer.md).

</details>
