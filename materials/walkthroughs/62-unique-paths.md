# 62. Unique Paths

**Medium** · [LeetCode](https://leetcode.com/problems/unique-paths/) · [Solution file (no hints)](../../problems/0001-0499/62.py)

[📖 14. 2-D Dynamic Programming lesson](../learning/15-dp-2d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 14. 2-D Dynamic Programming problems](../rmap-practice/14-dp-2d.md)

---

Count paths from top-left to bottom-right of a grid, moving only right or down. Why does the number of ways to reach any cell equal the sum of the ways to reach the cell above it and the cell to its left?

<details>
<summary>Hint</summary>

[2-D DP](../algorithms/dynamic-programming.md): `paths(r, c) = paths(r-1, c) + paths(r, c-1)`, since the only two ways to arrive at a cell are from above or from the left. The first row and column are all 1 (only one way to travel in a straight line).
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:

        row = [1] * n

        for i in range(m - 1):
            new_row = [1] * n
            for j in range(n - 2, -1, -1):
                new_row[j] = new_row[j + 1] + row[j]
            row = new_row
        return row[0]
```

Building blocks: [list-basics](../syntax/list-basics.md) · [for-loop](../syntax/for-loop.md) (nested, reverse range) · [arithmetic-operators](../syntax/arithmetic-operators.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(m · n)** — every cell computed once.
**Space: O(n)** — one row kept at a time (space-optimized from an O(m·n) grid).
</details>

---
