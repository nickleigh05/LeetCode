# 867. Transpose Matrix

**Easy** · [LeetCode](https://leetcode.com/problems/transpose-matrix/) · [Solution file (no hints)](../../problems/0500-0999/867.py)

[📖 17. Math & Geometry lesson](../learning/19-math-geometry.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 17. Math & Geometry problems](../rmap-practice/17-math-geometry.md)

---

Given a 2D integer array `matrix`, return its **transpose**: flip the matrix over its main diagonal, so the **rows become columns** and the **columns become rows**. The matrix does **not** have to be square.

```
matrix = [[1, 2, 3],        →  [[1, 4, 7],
          [4, 5, 6],             [2, 5, 8],
          [7, 8, 9]]             [3, 6, 9]]

matrix = [[1, 2, 3],        →  [[1, 4],
          [4, 5, 6]]             [2, 5],
                                 [3, 6]]
```

**Constraints:** `1 <= m, n <= 1000` · `1 <= m * n <= 10⁵` · `-10⁹ <= matrix[i][j] <= 10⁹`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "flip over the main diagonal" | `result[c][r] = matrix[r][c]` for every cell |
| "rows become columns" | An `m × n` input gives an **`n × m`** output |
| "does not have to be square" | **You can't transpose in place** in general. The shape changes, so build a **new** matrix |
| `m * n <= 10⁵` | Visiting every cell once is fine |

The rule is one line: the cell at `(r, c)` moves to `(c, r)`. The only real decision is the output's size: swap the dimensions. Allocate `n` rows of `m` zeros, then copy each cell across.

🤔 **Before you open the next section:** for a `2 × 3` input, how many rows and columns does the output have? Which input index runs along the output's rows?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Time | Space | Verdict |
|---|---|---|---|
| **Allocate `n × m`, copy `result[c][r] = matrix[r][c]`** | O(m·n) | O(m·n) | ✅ Works for any shape |
| `list(zip(*matrix))` | O(m·n) | O(m·n) | ✅ A one-liner: rows come back as tuples, so convert with `list` |
| In-place swap across the diagonal | O(m·n) | O(1) | ⚠️ **Square matrices only** |

**The decision: build a new matrix with nested loops.** It's the clearest code and handles rectangles. The in-place diagonal swap (`matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]` for `j > i`) is the answer only when the matrix is square: it's the first step of [Rotate Image](48-rotate-image.md).

Name the `zip(*matrix)` one-liner as the Pythonic version.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
rows, cols = len(matrix), len(matrix[0])
```

The input's dimensions: `rows` is `m`, `cols` is `n`.
→ [tuple-unpacking](../syntax/tuple-unpacking.md) · [list-basics](../syntax/list-basics.md)

```python
result = [[0] * rows for _ in range(cols)]
```

The output has **`cols` rows**, each holding **`rows` entries**: the dimensions swap. A comprehension makes a separate list per row (`[[0] * rows] * cols` would share one row `cols` times).
→ [nested-lists](../syntax/nested-lists.md) · [list-comprehension](../syntax/list-comprehension.md) · [mutable-default-arg-pitfall](../syntax/mutable-default-arg-pitfall.md)

```python
for r in range(rows):
    for c in range(cols):
        result[c][r] = matrix[r][c]
return result
```

Every input cell `(r, c)` lands at `(c, r)`. The indices in `result[c][r]` are the *reverse* of those in `matrix[r][c]`, and that reversal is the whole operation.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def transpose(self, matrix: List[List[int]]) -> List[List[int]]:
        rows, cols = len(matrix), len(matrix[0])
        result = [[0] * rows for _ in range(cols)]

        for r in range(rows):
            for c in range(cols):
                result[c][r] = matrix[r][c]

        return result
```

A one-liner alternative: `return [list(row) for row in zip(*matrix)]`.
→ [zip-function](../syntax/zip-function.md) · [unpacking-star-expr](../syntax/unpacking-star-expr.md)

</details>

**Trace it.** `matrix = [[1, 2, 3], [4, 5, 6]]` (`rows = 2`, `cols = 3`) gives `result` of size `3 × 2`:

| `(r, c)` | `matrix[r][c]` | writes to `result[c][r]` |
|---|---|---|
| (0, 0) | 1 | `result[0][0]` |
| (0, 1) | 2 | `result[1][0]` |
| (0, 2) | 3 | `result[2][0]` |
| (1, 0) | 4 | `result[0][1]` |
| (1, 1) | 5 | `result[1][1]` |
| (1, 2) | 6 | `result[2][1]` |

`result = [[1, 4], [2, 5], [3, 6]]` ✅.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(m · n)</summary>

**O(m · n):** every cell is read and written once.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(m · n)</summary>

**O(m · n)** for the output matrix. That's unavoidable for a non-square input: the answer has a different shape from the input, so it can't reuse the same storage.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The transpose sends the cell at row r, column c to row c, column r. The matrix isn't necessarily square, so the output has the dimensions swapped and I can't do it in place. I allocate an n-by-m result and copy each cell across with swapped indices. That's O(m·n) time and space. In Python it's also `zip(*matrix)`. For a square matrix I could swap across the diagonal in place in O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "In place?" | Only for square matrices: swap `matrix[i][j]` with `matrix[j][i]` for `j > i` |
| "Rotate the matrix 90°?" | [Rotate Image](48-rotate-image.md): transpose, then reverse each row |
| "Why can't a rectangle be transposed in place?" | The shape changes (`m × n` to `n × m`), so the flat positions don't map onto themselves in a simple swap |
| "Memory-tight on huge matrices?" | Return a lazy view (like NumPy's `.T`) that swaps the indices on access, with no copy |
| "Related?" | [Spiral Matrix](54-spiral-matrix.md) · [Set Matrix Zeroes](73-set-matrix-zeroes.md) |

**Traps:**

- **Allocating `m × n` instead of `n × m`.** An index error for rectangles.
- **`[[0] * rows] * cols`.** Every row is the same list.
- **Writing `result[r][c] = matrix[c][r]`.** Reversed, and it only works for squares.
- **Swapping in place across the whole matrix** (not just `j > i`). It undoes itself.

**This same move shows up in:** [Rotate Image](48-rotate-image.md) · [Spiral Matrix](54-spiral-matrix.md) · [Valid Sudoku](36-valid-sudoku.md) (columns as transposed rows).

</details>

---
