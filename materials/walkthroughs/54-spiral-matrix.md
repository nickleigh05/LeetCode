# 54. Spiral Matrix

**Medium** · [LeetCode](https://leetcode.com/problems/spiral-matrix/)

[📖 18. Math & Geometry lesson](../learning/18-math-geometry.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 18. Math & Geometry problems](../rmap-practice/18-math-geometry.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Given an `m × n` `matrix`, return **all its elements in spiral order** — starting at the top-left and moving right, then down, then left, then up, spiralling inward.

```
[[1,2,3],
 [4,5,6],     →  [1,2,3,6,9,8,7,4,5]
 [7,8,9]]

[[1, 2, 3, 4],
 [5, 6, 7, 8],   →  [1,2,3,4,8,12,11,10,9,5,6,7]
 [9,10,11,12]]
```

**Constraints:** `m == matrix.length` · `n == matrix[i].length` · `1 <= m, n <= 10` · `-100 <= matrix[i][j] <= 100`.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**all** its elements" | Every cell appears exactly once. So the output length is `m × n`, which is a useful invariant to check against |
| "spiral order" | A fixed cycle of directions — right, down, left, up — repeating inward |
| `m × n`, **not** necessarily square | Rectangular matrices are the source of every edge case here. A single row or single column is legal |
| `1 <= m, n <= 10` | Trivially small. **The difficulty is entirely boundary handling**, not performance |

The instinct is to simulate a walker: track a position and a direction, step forward, turn right when you hit a wall or a visited cell, and keep a `visited` grid. That works — but it needs O(m·n) extra space for the visited markers, and turning logic that's fiddly to get right.

**The cleaner model is to stop thinking about a walker and think about four shrinking walls.**

Keep `top`, `bottom`, `left`, `right` — the boundaries of the *unvisited rectangle*. Then one full loop of the spiral is four passes:

1. Walk **right** across row `top`, then **`top += 1`** — that row is consumed.
2. Walk **down** column `right`, then **`right -= 1`**.
3. Walk **left** across row `bottom`, then **`bottom -= 1`**.
4. Walk **up** column `left`, then **`left += 1`**.

After those four passes the unvisited region is a strictly smaller rectangle, and you repeat until the boundaries cross.

**No visited set is needed**, and that's the payoff: shrinking a boundary immediately after traversing it *is* the record of having visited it. The rectangle itself carries the state.

The subtlety — and it's where nearly all bugs in this problem live — is that after passes 1 and 2, the rectangle may have already collapsed. If only one row remained, pass 1 consumed it and pass 3 would walk it **again backwards**. So passes 3 and 4 each need a guard.

🤔 **Before you open the next section:** passes 3 and 4 have `if` guards but passes 1 and 2 don't. Why is the asymmetry correct rather than an oversight?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Walker + `visited` grid | Move in a direction, turn right on a wall or visited cell | O(m·n) | **O(m·n)** | ⚠️ Correct, but the visited grid is avoidable |
| Walker + direction vectors, mark cells in place | Overwrite visited cells with a sentinel | O(m·n) | O(1) | ❌ Destroys the input, and needs a value guaranteed absent |
| Peel the first row, rotate, recurse | Take the top row, rotate the rest counter-clockwise, repeat | O((m·n)²) | O(m·n) | ❌ Elegant but the rotations are expensive |
| **Four shrinking boundaries** | Traverse and consume one edge at a time | **O(m·n)** | **O(1)** | ✅ |

**The decision:** **four boundaries, shrinking inward.**

**Why the boundary model beats the walker.** A walker needs to know when to turn, and "when I'd step outside or onto something visited" requires either a visited grid (O(m·n) space) or destroying the input. The boundary model answers the same question **structurally**: the walls tell you exactly how far each pass goes, and shrinking a wall after a pass records the visit implicitly.

**That's the reusable idea: when a traversal has geometric structure, encode it in bounds rather than in visited state.** Same instinct as [Jump Game](55-jump-game.md), where reachability was an interval describable by one number instead of a set.

**Why the guards are asymmetric** — the answer to section 1's question, and the crux of the problem.

At the top of each loop iteration, the `while` condition has just confirmed `top <= bottom` and `left <= right`, so **passes 1 and 2 are guaranteed to have a valid row and column to walk.** No guard needed.

But pass 1 does `top += 1` and pass 2 does `right -= 1`. After those, the rectangle may be **empty**:

- If the remaining region had only **one row**, pass 1 consumed it and `top` now exceeds `bottom`. Pass 3 would walk that same row backwards, **duplicating every element**.
- If it had only **one column**, pass 2 consumed it and `right` is now below `left`. Pass 4 would walk that column again upward.

So passes 3 and 4 re-check the conditions their predecessors may have invalidated. **The asymmetry is exactly right: the first two passes are protected by the `while` condition, the last two are not.**

This is why a single-row input like `[[1,2,3]]` is the test case to try first — it's the minimal case where the missing guard shows up.

**Why not peel-and-rotate?** `result += matrix.pop(0)` then rotate the remainder counter-clockwise is a beautiful three-line solution, but each rotation is O(m·n), giving O((m·n)²) overall plus O(m·n) space. Cute; not the answer.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
result = []
top = 0
bottom = len(matrix) - 1
left = 0
right = len(matrix[0]) - 1
```
The four walls of the **unvisited rectangle**, initialized to the full matrix. All four are **inclusive** bounds — `matrix[top][left]` through `matrix[bottom][right]` is the region still to be visited.

Using inclusive bounds is what makes the `<=` comparisons and the `+ 1` in the ranges consistent throughout. Mixing inclusive and exclusive conventions is a reliable source of off-by-one errors here.
→ [list-basics](../syntax/list-basics.md) · [nested-lists](../syntax/nested-lists.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
while top <= bottom and left <= right:
```
**Continue while the unvisited rectangle is non-empty.** Both conditions are needed: rows can run out before columns or vice versa, depending on the shape.

`<=` rather than `<` because the bounds are inclusive — `top == bottom` means one row remains, which still needs visiting.
→ [while-loop](../syntax/while-loop.md) · [logical-operators](../syntax/logical-operators.md)

```python
    for col in range(left, right + 1):
        result.append(matrix[top][col])
    top += 1
```
**Pass 1 — walk right across the top row.** `right + 1` because [`range`](../syntax/range-function.md) excludes its endpoint and `right` is inclusive.

Then `top += 1` **consumes** that row. No guard is needed: the `while` condition just guaranteed `top <= bottom`, so this row exists.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md) · [list-methods](../syntax/list-methods.md)

```python
    for row in range(top, bottom + 1):
        result.append(matrix[row][right])
    right -= 1
```
**Pass 2 — walk down the right column.**

Note it starts at the **already-incremented** `top`, so it doesn't revisit the corner cell that pass 1 just took. That's automatic rather than a special case: the boundary shrank, and the range picks up the new value.

Then `right -= 1` consumes the column. Still no guard — `left <= right` was confirmed by the `while`.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md)

```python
    if top <= bottom:
        for col in range(right, left - 1, -1):
            result.append(matrix[bottom][col])
        bottom -= 1
```
**Pass 3 — walk left across the bottom row, but only if a row remains.**

**The guard is essential.** Pass 1 incremented `top`; if the region had a single row, `top` now exceeds `bottom` and this row was already emitted. Without the check, `[[1,2,3]]` would produce `[1,2,3,3,2,1]`.

The [reverse range](../syntax/range-function.md) `range(right, left - 1, -1)` walks from `right` down to `left` **inclusive** — the `left - 1` stop is exclusive, so `left` itself is included. Getting this to `left` instead of `left - 1` silently drops the leftmost cell.
→ [if-return](../syntax/if-return.md) · [range-function](../syntax/range-function.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
    if left <= right:
        for row in range(bottom, top - 1, -1):
            result.append(matrix[row][left])
        left += 1
```
**Pass 4 — walk up the left column, but only if a column remains.**

Same reasoning mirrored: pass 2 decremented `right`, so if the region had a single column it's already been emitted and `right` is now below `left`.

The range runs from the **already-decremented** `bottom` up to `top` inclusive, again avoiding the corners the previous passes consumed.
→ [if-return](../syntax/if-return.md) · [range-function](../syntax/range-function.md)

```python
return result
```
Every cell visited exactly once, in spiral order. `len(result)` will equal `m × n` — a good invariant to assert while debugging.
→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:

        result = []
        top = 0
        bottom = len(matrix) - 1
        left = 0
        right = len(matrix[0]) - 1

        while top <= bottom and left <= right:
            for col in range(left, right + 1):
                result.append(matrix[top][col])
            top += 1

            for row in range(top, bottom + 1):
                result.append(matrix[row][right])
            right -= 1

            if top <= bottom:
                for col in range(right, left - 1, -1):
                    result.append(matrix[bottom][col])
                bottom -= 1

            if left <= right:
                for row in range(bottom, top - 1, -1):
                    result.append(matrix[row][left])
                left += 1

        return result
```
</details>

**Trace it** — the 3×3 matrix

Start: `top=0, bottom=2, left=0, right=2`

**Iteration 1:**

| pass | range | cells emitted | boundary update |
|---|---|---|---|
| 1 · right | cols 0→2 of row 0 | **1, 2, 3** | `top = 1` |
| 2 · down | rows 1→2 of col 2 | **6, 9** | `right = 1` |
| 3 · left | `top(1) <= bottom(2)` ✓, cols 1→0 of row 2 | **8, 7** | `bottom = 1` |
| 4 · up | `left(0) <= right(1)` ✓, rows 1→1 of col 0 | **4** | `left = 1` |

State: `top=1, bottom=1, left=1, right=1` — a single cell left.

**Iteration 2:**

| pass | range | cells emitted | boundary update |
|---|---|---|---|
| 1 · right | cols 1→1 of row 1 | **5** | `top = 2` |
| 2 · down | rows 2→1 — **empty range** | — | `right = 0` |
| 3 · left | `top(2) <= bottom(1)` **✗ skipped** | — | — |
| 4 · up | `left(1) <= right(0)` **✗ skipped** | — | — |

`while` condition now fails (`2 <= 1` is false). Return **[1,2,3,6,9,8,7,4,5]** ✅

Iteration 2 shows both mechanisms: pass 2's range came out empty naturally (no guard needed — an empty `range` just doesn't iterate), while passes 3 and 4 were skipped by their explicit guards. **Without those guards, the 5 would have been emitted three times.**

**And the single-row case** — `matrix = [[1,2,3]]`, where `top=bottom=0`, `left=0`, `right=2`:

| pass | what happens | emitted | boundaries |
|---|---|---|---|
| 1 · right | cols 0→2 of row 0 | **1, 2, 3** | `top = 1` |
| 2 · down | rows 1→0 — empty | — | `right = 1` |
| 3 · left | `top(1) <= bottom(0)` **✗ skipped** | — | — |
| 4 · up | `left(0) <= right(1)` ✓, rows 0→1 — **empty range** | — | `left = 1` |

Return **[1,2,3]** ✅

**This is the case that proves the guards matter.** Without the pass-3 guard, it would walk row 0 backwards and emit `[1,2,3,3,2,1]` — twice the required length.

**And a single column** — `matrix = [[1],[2],[3]]`, `top=0, bottom=2, left=right=0`:

| pass | emitted | boundaries |
|---|---|---|
| 1 · right | **1** (just col 0 of row 0) | `top = 1` |
| 2 · down | **2, 3** | `right = -1` |
| 3 · left | `top(1) <= bottom(2)` ✓, `range(-1, -1, -1)` — **empty** | `bottom = 1` |
| 4 · up | `left(0) <= right(-1)` **✗ skipped** | — |

Return **[1,2,3]** ✅ — here pass 3's guard passes but its range is empty, and pass 4's guard is what prevents the duplication.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(m · n)</summary>

**O(m · n)** — every cell is appended exactly once.

- Across all iterations, the four passes together cover each cell of the matrix precisely one time; the shrinking boundaries guarantee no overlap and no gaps.
- Each append is amortized **O(1)**.
- Total: **O(m · n)**.

At the limits, 10 × 10 = **100** cells. Instant.

**The invariant worth naming:** `len(result) == m * n` at the end. That's both a correctness check and the proof of the complexity — the loop can't do more work than emitting each cell once, because a cell can only be emitted when it's inside the current rectangle, and every pass immediately shrinks that rectangle past the cells it just emitted.

**Against the alternatives:** the walker with a visited grid is also O(m·n) time but pays O(m·n) space. The peel-and-rotate approach is **O((m·n)²)**, because each of the O(m+n) rotations costs O(m·n).

**Faster?** No. Every element must appear in the output, so **Ω(m·n)** is a lower bound — you can't produce m·n values in less than m·n time.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1) extra</summary>

**O(1)** beyond the output — four boundary integers and two loop variables, regardless of matrix size.

| Component | Space | Why |
|---|---|---|
| `result` | **O(m·n)** *output* | Every cell must appear — unavoidable, and it's the return value |
| `top`, `bottom`, `left`, `right` | **O(1)** | Four integers |
| Loop variables | O(1) | Two integers |

So: **O(1) auxiliary, O(m·n) including the output.**

**The comparison that makes the case for this approach:**

| Approach | Auxiliary space | Why |
|---|---|---|
| Walker + `visited` grid | **O(m·n)** | A boolean per cell |
| Walker marking cells in place | O(1) | But destroys the input, and needs an unused sentinel value |
| **Four boundaries** | **O(1)** | The rectangle *is* the visited state |

**That's the structural point:** the visited set would store m·n booleans to answer "have I been here?" — but the answer is always derivable from four numbers, because the visited region is always exactly "everything outside the current rectangle." **A shape with structure compresses to its bounds**, the same reduction seen in [Jump Game](55-jump-game.md) and [Valid Parenthesis String](678-valid-parenthesis-string.md).

**The input is never modified**, which is worth noting as a genuine advantage over the mark-in-place walker — some callers care.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Rather than simulating a walker that turns when it hits something visited — which needs an O(m·n) visited grid — I'll track four boundaries of the unvisited rectangle: top, bottom, left, right. One loop of the spiral is four passes: walk right across the top row and increment `top`, down the right column and decrement `right`, left across the bottom and decrement `bottom`, up the left column and increment `left`. Shrinking the boundary right after traversing it *is* the record of having visited it, so no visited set is needed. The one subtlety is that passes 3 and 4 need guards but passes 1 and 2 don't: the while condition guarantees a valid row and column at the top of the iteration, but pass 1 and pass 2 have already shrunk the rectangle by then, so it may be empty. Without the guard, a single-row matrix would emit its row forwards and then backwards. O(m·n) time, O(1) extra space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why do passes 3 and 4 need guards but not 1 and 2?" | The `while` condition validates the rectangle at the top of each iteration, so passes 1 and 2 are safe. But they then shrink `top` and `right`, so by pass 3 the rectangle may have collapsed. |
| "What input catches the missing guard?" | `[[1,2,3]]` — a single row. Without the pass-3 guard it emits `[1,2,3,3,2,1]`. A single column catches the pass-4 guard. |
| "Why no visited set?" | The visited region is always exactly "outside the current rectangle," which four integers describe completely. |
| "Solve it with direction vectors instead." | Keep `(dr, dc)` cycling through right/down/left/up, step forward, and turn when the next cell is out of bounds or visited. It needs a visited grid or in-place marking. |
| "Generate a spiral matrix instead of reading one." | [Spiral Matrix II](https://leetcode.com/problems/spiral-matrix-ii/) — the identical boundary loop, writing `1..n²` instead of appending. |
| "What about a single element?" | `[[7]]` — pass 1 emits it, pass 2's range is empty, passes 3 and 4 are guarded off. Returns `[7]`. |
| "Can you avoid the guards entirely?" | Yes — track a count of emitted cells and stop at `m*n`, checking after every append. It trades the two guards for a check in the innermost loop. |
| "Does this modify the input?" | No — and that's an advantage over the mark-in-place walker. |

**Traps:**
- **Omitting the guards on passes 3 and 4.** Duplicates rows or columns on any matrix with an odd number of rows or columns in the final layer. The defining bug.
- **`range(right, left, -1)`** instead of `range(right, left - 1, -1)` — silently drops the leftmost cell of each bottom pass.
- **Forgetting `+ 1`** in `range(left, right + 1)` — drops the rightmost cell.
- Starting pass 2 at the original `top` rather than the incremented one — re-emits the corner.
- Mixing inclusive and exclusive boundary conventions. Pick inclusive and keep every comparison `<=` and every range `+1`/`-1`.
- Assuming the matrix is square. `m` and `n` differ, and rectangular shapes are where the edge cases live.

**This same move shows up in:** [Rotate Image](48-rotate-image.md) (careful 2-D index management, in place) · [Set Matrix Zeroes](73-set-matrix-zeroes.md) (avoiding auxiliary space by exploiting the matrix's own structure) · [Jump Game](55-jump-game.md) (replacing a set of visited/reachable positions with a couple of bounds) · [Binary Search](704-binary-search.md) (shrinking inclusive `lo`/`hi` boundaries until they cross).

</details>

---
