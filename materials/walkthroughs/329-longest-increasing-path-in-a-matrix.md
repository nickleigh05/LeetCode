# 329. Longest Increasing Path in a Matrix

**Hard** · [LeetCode](https://leetcode.com/problems/longest-increasing-path-in-a-matrix/)

[📖 14. 2-D Dynamic Programming lesson](../learning/15-dp-2d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 14. 2-D Dynamic Programming problems](../rmap-practice/14-dp-2d.md)

---

Solution: not yet solved in this repo.

Find the longest strictly increasing path through a matrix, moving to any of the 4 neighbors. Why does memoizing "longest path starting at this cell" turn an exponential DFS into a linear one?

<details>
<summary>Hint</summary>

Run [DFS](../algorithms/dfs.md) from each cell, only moving to neighbors with a *strictly greater* value, and memoize each cell's answer — since neighbors are shared across many starting cells, memoization avoids exponential recomputation (see [Dynamic Programming](../algorithms/dynamic-programming.md)).
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:

        rows = len(matrix)
        cols = len(matrix[0])
        memo = {}

        def dfs(row, col):
            if (row, col) in memo:
                return memo[(row, col)]

            best = 1
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                r = row + dr
                c = col + dc
                if 0 <= r < rows and 0 <= c < cols and matrix[r][c] > matrix[row][col]:
                    best = max(best, 1 + dfs(r, c))

            memo[(row, col)] = best
            return best

        return max(dfs(row, col) for row in range(rows) for col in range(cols))
```

Building blocks: [dict-basics](../syntax/dict-basics.md) (memoization) · [recursion-basics](../syntax/recursion-basics.md) · [generator-expressions](../syntax/generator-expressions.md) (`max(... for ...)`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(rows · cols)** — each cell's answer is computed once thanks to memoization.
**Space: O(rows · cols)** — the memo table and recursion stack.
</details>

---
