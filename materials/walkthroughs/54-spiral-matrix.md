# 54. Spiral Matrix

**Medium** · [LeetCode](https://leetcode.com/problems/spiral-matrix/)

[📖 17. Math & Geometry lesson](../learning/19-math-geometry.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 17. Math & Geometry problems](../rmap-practice/17-math-geometry.md)

---

Solution: not yet solved in this repo.

Return all elements of a matrix in spiral order. Why do four shrinking boundaries (top, bottom, left, right) naturally trace a spiral without needing to track visited cells?

<details>
<summary>Hint</summary>

Maintain `top`, `bottom`, `left`, `right` boundaries. Walk right across the top row, down the right column, left across the bottom row, up the left column — shrinking each boundary after its pass — until they cross.
</details>

<details>
<summary>Solution</summary>

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

Building blocks: [while-loop](../syntax/while-loop.md) · [for-loop](../syntax/for-loop.md) (reverse range) · [list-methods](../syntax/list-methods.md) (`.append()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(rows · cols)** — every cell is visited exactly once.
**Space: O(1)** extra beyond the output list.
</details>

---
