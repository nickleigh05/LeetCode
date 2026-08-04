# 72. Edit Distance

**Hard** · [LeetCode](https://leetcode.com/problems/edit-distance/)

[📖 14. 2-D Dynamic Programming lesson](../learning/15-dp-2d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 14. 2-D Dynamic Programming problems](../rmap-practice/14-dp-2d.md)

---

Solution: not yet solved in this repo.

Find the minimum insert/delete/replace operations to turn one word into another. When characters match, why is no operation needed there — and when they don't, why take the best of all three operations plus 1?

<details>
<summary>Hint</summary>

[2-D DP](../algorithms/dynamic-programming.md): `dp[i][j]` = edit distance between `word1[i:]` and `word2[j:]`. If `word1[i] == word2[j]`, no cost, move diagonally; otherwise `1 + min(insert, delete, replace)` using the three neighboring subproblems.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def minDistance(self, word1: str, word2: str) -> int:

        m = len(word1)
        n = len(word2)

        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for j in range(n + 1):
            dp[m][j] = n - j   # word1 exhausted: insert the rest of word2
        for i in range(m + 1):
            dp[i][n] = m - i   # word2 exhausted: delete the rest of word1

        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                if word1[i] == word2[j]:
                    dp[i][j] = dp[i + 1][j + 1]
                else:
                    dp[i][j] = 1 + min(
                        dp[i + 1][j],       # delete word1[i]
                        dp[i][j + 1],       # insert word2[j]
                        dp[i + 1][j + 1],   # replace word1[i] with word2[j]
                    )

        return dp[0][0]
```

Building blocks: [nested-lists](../syntax/nested-lists.md) · [for-loop](../syntax/for-loop.md) (reverse range) · [comparison-operators](../syntax/comparison-operators.md) (`min()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(m · n)** — every cell computed once.
**Space: O(m · n)** — the DP grid.
</details>

---
