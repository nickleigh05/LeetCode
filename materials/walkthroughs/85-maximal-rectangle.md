# 85. Maximal Rectangle

**Hard** · [LeetCode](https://leetcode.com/problems/maximal-rectangle/) · [Solution file (no hints)](../../problems/0001-0499/85.py)

[📖 04. Stack lesson](../learning/04-stack.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 04. Stack problems](../rmap-practice/04-stack.md)

---

Given a `rows × cols` binary matrix filled with `'0'` and `'1'`, find the largest rectangle containing **only `1`s** and return its area.

```
matrix = [["1","0","1","0","0"],
          ["1","0","1","1","1"],
          ["1","1","1","1","1"],
          ["1","0","0","1","0"]]      →  6

matrix = [["0"]]  →  0
matrix = [["1"]]  →  1
```

**Constraints:** `1 <= rows, cols <= 200` · `matrix[i][j]` is `'0'` or `'1'`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "largest **rectangle** of 1s" | Axis-aligned, contiguous in both dimensions |
| binary matrix | Only two values, so "can I extend upward?" is a simple test |
| `rows, cols <= 200` | 4·10⁴ cells. O(rows · cols) = 4·10⁴ is ideal; O((rows·cols)²) = 1.6·10⁹ is not |
| entries are **strings** `'1'`, not ints | ⚠️ Easy to trip on — compare against `'1'`, or convert |
| `rows, cols >= 1` | Never empty, though `[["0"]]` must still return 0 |

The brute force — try every pair of corners and verify the rectangle is all 1s — is O(rows² · cols²) or worse. Far too slow, and it throws away all the structure.

**The reduction that solves it** — this is the entire insight:

> **Process the matrix row by row. For each row, treat it as the base of a histogram whose bar heights are the number of consecutive 1s directly above (including the current cell). Then the answer for that row is the largest rectangle in that histogram** — which is exactly [Largest Rectangle in Histogram](84-largest-rectangle-in-histogram.md).

Watch the heights build up:

```
matrix              heights (running column-wise counts)
1 0 1 0 0    row 0:  1 0 1 0 0
1 0 1 1 1    row 1:  2 0 2 1 1
1 1 1 1 1    row 2:  3 1 3 2 2   ← largest histogram rectangle here = 6
1 0 0 1 0    row 3:  4 0 0 3 0
```

At row 2 the histogram is `[3,1,3,2,2]`, and its largest rectangle spans the last three bars at height 2 — area `2 × 3 = 6`. That's the answer.

**Why the reduction is valid:** every rectangle of 1s in the matrix has a bottom row. When you process that row, the rectangle appears as a rectangle in that row's histogram. So considering every row as a base covers every possible rectangle exactly once (at its bottom).

**The height update rule:** `height[c] = height[c] + 1` if the cell is `'1'`, else **reset to 0**. A zero breaks the vertical run entirely — you can't have a rectangle of 1s spanning it.

🤔 **Before you open the next section:** if a cell is `'0'`, why must its column height reset to 0 rather than just stop growing?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

Let `R = rows`, `C = cols`.

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Brute force corners | Every corner pair, verify all 1s | O(R²·C²·RC) | O(1) | ❌ Hopeless |
| Prefix sums + corner pairs | O(1) rectangle checks, still all pairs | O(R²·C²) | O(RC) | ❌ 1.6·10⁹ |
| DP per row (left/right/height) | Track boundaries per column | O(R·C) | O(C) | ✅ Correct, more state to juggle |
| **Row histograms + monotonic stack** | Reduce each row to [problem 84](84-largest-rectangle-in-histogram.md) | **O(R·C)** | **O(C)** | ✅ |

**The decision: build a running height array per row, then run the histogram algorithm on it.**

The value here is **reduction** — recognizing that a Hard 2-D problem is `R` repetitions of a Medium 1-D problem you already know. That's a more valuable skill than any individual trick, and it's what the problem is really testing.

**The histogram sub-algorithm** ([Largest Rectangle in Histogram](84-largest-rectangle-in-histogram.md)) in brief: use a monotonic **increasing** stack of indices. When a bar shorter than the stack top arrives, the top bar can extend no further right — pop it and compute its area, where the width runs from just after the new stack top to just before the current index.

**Why a sentinel `0` helps.** Appending a virtual zero-height bar at the end forces every remaining stack entry to pop and be measured, removing the need for a separate drain loop. Small trick, meaningfully less code to get wrong.

**Why the width calculation is `i - stack[-1] - 1`.** After popping index `p`, the bar at `p` can extend left until the new stack top (the nearest shorter bar to the left) and right until `i` (the nearest shorter bar to the right). The span strictly between those bounds is `i - stack[-1] - 1`. When the stack empties, the bar extends all the way to the left edge, so the width is just `i`.

**Why not the left/right-boundary DP?** It's a legitimate O(R·C) alternative — maintain, per column, the leftmost and rightmost extent of the current run — but it requires three arrays and careful boundary resets. The histogram reduction reuses a solution you can already justify.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
if not matrix or not matrix[0]:
    return 0

cols = len(matrix[0])
heights = [0] * cols
max_area = 0
```

`heights[c]` is the count of consecutive `'1'`s ending at the current row in column `c` — the histogram bar for that column.

It persists **across rows**, accumulating downward. That's what makes the whole thing O(R·C) rather than recomputing heights each row.
→ [list-basics](../syntax/list-basics.md)

```python
for row in matrix:
    for c in range(cols):
        heights[c] = heights[c] + 1 if row[c] == '1' else 0
```

**Update the histogram for this row.**

- `'1'` → the vertical run extends by one
- `'0'` → **reset to 0**, because a zero severs the column entirely; no all-1s rectangle can cross it

Note `row[c] == '1'` — comparing against the **string** `'1'`, since the matrix holds characters.
→ [ternary-expression](../syntax/ternary-expression.md) · [for-loop](../syntax/for-loop.md)

```python
    max_area = max(max_area, self.largestRectangleArea(heights))
```

Run the 1-D histogram algorithm on this row's bars and keep the best across all rows.
→ [min-max-key](../syntax/min-max-key.md)

---

**The histogram helper — the monotonic stack**

```python
def largestRectangleArea(self, heights):
    stack = []
    best = 0
    extended = heights + [0]
```

`extended` appends a sentinel zero-height bar, guaranteeing every real bar is eventually popped and measured — no separate drain loop needed.
→ [list-basics](../syntax/list-basics.md)

```python
    for i, h in enumerate(extended):
        while stack and extended[stack[-1]] > h:
            height = extended[stack.pop()]
            width = i - stack[-1] - 1 if stack else i
            best = max(best, height * width)
        stack.append(i)
    return best
```

**The core.** The stack holds indices of bars in **increasing** height order.

When bar `h` is shorter than the stack top, that taller bar cannot extend past `i` — so pop it and finalize its rectangle:

- **height** — the popped bar's own height
- **width** — from just after the new stack top (nearest shorter bar on the left) to just before `i` (nearest shorter bar on the right), i.e. `i - stack[-1] - 1`
- if the stack is now **empty**, that bar was the shortest so far and extends to the left edge → width is `i`

`while`, not `if` — one short bar can close out many taller ones at once.
→ [while-loop](../syntax/while-loop.md) · [enumerate](../syntax/enumerate.md) · [list-methods](../syntax/list-methods.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def maximalRectangle(self, matrix: List[List[str]]) -> int:

        if not matrix or not matrix[0]:
            return 0

        cols = len(matrix[0])
        heights = [0] * cols
        max_area = 0

        for row in matrix:
            for c in range(cols):
                heights[c] = heights[c] + 1 if row[c] == '1' else 0

            max_area = max(max_area, self.largestRectangleArea(heights))

        return max_area

    def largestRectangleArea(self, heights: List[int]) -> int:

        stack = []
        best = 0
        extended = heights + [0]

        for i, h in enumerate(extended):
            while stack and extended[stack[-1]] > h:
                height = extended[stack.pop()]
                width = i - stack[-1] - 1 if stack else i
                best = max(best, height * width)
            stack.append(i)

        return best
```

</details>

**Trace the heights** — for the example matrix:

| Row | Matrix row | `heights` after update | Best rectangle in this histogram |
|---|---|---|---|
| 0 | `1 0 1 0 0` | `[1,0,1,0,0]` | 1 |
| 1 | `1 0 1 1 1` | `[2,0,2,1,1]` | 3 (bars 2–4 at height 1) |
| 2 | `1 1 1 1 1` | `[3,1,3,2,2]` | **6** ⭐ (bars 2–4 at height 2) |
| 3 | `1 0 0 1 0` | `[4,0,0,3,0]` | 4 |

Answer **6** ✅

**Trace the histogram** on row 2's `heights = [3,1,3,2,2]`, with sentinel → `[3,1,3,2,2,0]`:

| `i` | `h` | Stack (indices) | Pops → area | `best` |
|---|---|---|---|---|
| 0 | 3 | `[]` → `[0]` | — | 0 |
| 1 | 1 | `[0]` | pop 0: h=3, stack empty → w=1 → **3** | 3 |
| | | → `[1]` | | |
| 2 | 3 | `[1]` → `[1,2]` | none (1 < 3) | 3 |
| 3 | 2 | `[1,2]` | pop 2: h=3, w=`3-1-1`=1 → 3 | 3 |
| | | → `[1,3]` | | |
| 4 | 2 | `[1,3]` → `[1,3,4]` | none (2 = 2, not >) | 3 |
| 5 | 0 | `[1,3,4]` | pop 4: h=2, w=`5-3-1`=1 → 2 | 3 |
| | | | pop 3: h=2, w=`5-1-1`=3 → **6** ⭐ | **6** |
| | | | pop 1: h=1, stack empty → w=5 → 5 | 6 |

Returns **6** ✅ — the starred step is the 2×3 rectangle spanning columns 2–4 at height 2.

Note the sentinel `0` at `i = 5` is what triggered the final three pops, including the winning one.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(rows · cols)</summary>

**O(R · C)** — linear in the number of cells, which is optimal since every cell must be read.

Per row:

- Height update: O(C)
- Histogram scan: **O(C)** — each index is pushed once and popped at most once, so the inner `while` is amortized

Across `R` rows: **O(R · C)** = 4·10⁴ at the limits. Instant.

**The amortized argument for the histogram**, which is the part worth defending:

> Each of the `C` indices is pushed exactly once and popped at most once, so the total inner-loop work per row is O(C), not O(C²).

Same accounting as [Next Greater Element I](496-next-greater-element-i.md) and [Online Stock Span](901-online-stock-span.md) — a nested loop with a global budget.

**Compare to brute force:** checking all corner pairs is O(R²·C²) = 1.6·10⁹ even with O(1) prefix-sum verification. The reduction to `R` histogram problems is what makes this tractable.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(cols)</summary>

**O(C).**

- `heights` — one integer per column, **reused across rows** rather than rebuilt
- `stack` — at most `C + 1` indices
- `extended` — a copy of `heights` plus the sentinel, O(C)

No 2-D auxiliary structure is needed, which is worth noting: a naive DP might allocate an `R × C` table, but here each row's histogram is consumed immediately and only the running heights carry forward.

**The generalizable idea:**

> **When a 2-D problem decomposes into independent 1-D problems along one axis, you only need O(one dimension) of state** — process and discard row by row.

The same reasoning appears in 2-D DP problems that get rolled down to a single row of state, and in the "fix a pair of rows, collapse to 1-D" technique for [submatrix sum problems](560-subarray-sum-equals-k.md).

You could avoid the `extended` copy by handling the drain explicitly after the loop; that saves a constant factor, not an order.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The key is a reduction. Every rectangle of 1s has a bottom row, so if I process the matrix row by row and, for each row, build a histogram whose bar heights are the count of consecutive 1s above each column, then the largest rectangle with that row as its base is exactly the largest rectangle in that histogram — which is Largest Rectangle in Histogram. Heights carry over between rows: add one on a `'1'`, reset to zero on a `'0'`, since a zero severs the column. Then I run a monotonic increasing stack per row: when a shorter bar arrives, the taller bars on the stack can't extend further right, so I pop and measure them, with the width running between the nearest shorter bars on each side. Appending a sentinel zero flushes the stack at the end. O(rows × cols) time and O(cols) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Largest **square** instead of rectangle?" | Much simpler — classic DP: `dp[i][j] = min(up, left, diag) + 1`. [Maximal Square](221-maximal-square.md), O(R·C). |
| "Why does the histogram reduction work?" | Every rectangle has a bottom row; processing each row as a base covers every rectangle exactly once. |
| "Why reset the height to 0 on a `'0'`?" | An all-1s rectangle can't span a zero, so the vertical run is severed, not merely paused. |
| "Why the sentinel zero?" | It forces every remaining bar to pop and be measured, replacing a separate drain loop. |
| "Explain the width formula." | After popping `p`, its rectangle extends between the nearest shorter bars on each side: `i - stack[-1] - 1`, or `i` if the stack is empty. |
| "Return the rectangle's coordinates?" | Record the row, the popped height, and the left/right bounds whenever `best` improves. |
| "Solve it without the histogram?" | Per-column left/right boundary DP — also O(R·C), three arrays, fiddlier resets. |

**Traps:**

- **Comparing against `1` instead of `'1'`.** The matrix holds **strings**. `row[c] == 1` is always `False`, and you'll return 0 for everything.
- **Not resetting the height on a `'0'`.** Rectangles then illegally span zeros.
- **Rebuilding `heights` from scratch each row.** Correct but O(R²·C); the running update is the point.
- **Wrong width formula.** `i - stack[-1] - 1` vs `i - stack[-1]` — the off-by-one silently under- or over-counts.
- **Forgetting the empty-stack case in the width.** When the stack empties, the width is `i`, not `i - something`.
- **Using `>=` in the pop condition.** With `>`, equal-height bars are handled correctly by the later bar; `>=` also works but you must be consistent — mixing them breaks the width logic.
- **Forgetting the drain.** Without the sentinel, bars left on the stack at the end are never measured.

**This same move shows up in:** [Largest Rectangle in Histogram](84-largest-rectangle-in-histogram.md) (the 1-D sub-problem this reduces to — solve that first) · [Maximal Square](221-maximal-square.md) (the same matrix, squares only, solved by simple DP) · [Next Greater Element I](496-next-greater-element-i.md) (the monotonic-stack primitive) · [Online Stock Span](901-online-stock-span.md) (accumulating a quantity while popping).

</details>

---
