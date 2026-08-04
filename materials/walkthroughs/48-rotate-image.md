# 48. Rotate Image

**Medium** · [LeetCode](https://leetcode.com/problems/rotate-image/) · [Solution file (no hints)](../../problems/0001-0499/48.py)

[📖 17. Math & Geometry lesson](../learning/19-math-geometry.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 17. Math & Geometry problems](../rmap-practice/17-math-geometry.md)

---

Rotate an n×n matrix 90° clockwise in place. Why does "transpose, then reverse each row" produce exactly a 90° clockwise rotation?

<details>
<summary>Hint</summary>

Transposing (swap `matrix[i][j]` with `matrix[j][i]`) flips the matrix across its main diagonal; reversing each row afterward flips it left-right — combined, that's precisely a 90° clockwise turn.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:

        n = len(matrix)

        for i in range(n):
            for j in range(i + 1, n):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

        for row in matrix:
            row.reverse()
```

Building blocks: [nested-lists](../syntax/nested-lists.md) · [swap-tuple-assign](../syntax/swap-tuple-assign.md) · [list-methods](../syntax/list-methods.md) (`.reverse()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n²)** — every cell is touched a constant number of times.
**Space: O(1)** — rotated in place, no extra matrix.
</details>

---
