# 73. Set Matrix Zeroes

**Medium** · [LeetCode](https://leetcode.com/problems/set-matrix-zeroes/)

[📖 17. Math & Geometry lesson](../learning/19-math-geometry.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 17. Math & Geometry problems](../rmap-practice/17-math-geometry.md)

---

Solution: not yet solved in this repo.

If a cell is 0, set its entire row and column to 0 — in O(1) extra space. Why can the matrix's own first row and first column be reused as the "which rows/cols need zeroing" markers?

<details>
<summary>Hint</summary>

Use the first row and first column of the matrix itself as marker flags. Track separately whether the first row/column originally contained a 0 (since they double as markers and would otherwise be overwritten). Two passes: mark, then apply.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:

        rows = len(matrix)
        cols = len(matrix[0])
        first_row_zero = any(matrix[0][col] == 0 for col in range(cols))
        first_col_zero = any(matrix[row][0] == 0 for row in range(rows))

        for row in range(1, rows):
            for col in range(1, cols):
                if matrix[row][col] == 0:
                    matrix[row][0] = 0
                    matrix[0][col] = 0

        for row in range(1, rows):
            for col in range(1, cols):
                if matrix[row][0] == 0 or matrix[0][col] == 0:
                    matrix[row][col] = 0

        if first_row_zero:
            for col in range(cols):
                matrix[0][col] = 0
        if first_col_zero:
            for row in range(rows):
                matrix[row][0] = 0
```

Building blocks: [generator-expressions](../syntax/generator-expressions.md) (`any(... for ...)`) · [for-loop](../syntax/for-loop.md) (nested) · [nested-lists](../syntax/nested-lists.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(rows · cols)** — a constant number of passes over the matrix.
**Space: O(1)** — the matrix's own first row/column are reused as markers.
</details>

---
