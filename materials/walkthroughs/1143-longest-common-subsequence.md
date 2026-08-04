# 1143. Longest Common Subsequence

**Medium** · [LeetCode](https://leetcode.com/problems/longest-common-subsequence/) · [Solution file (no hints)](../../problems/1000-1499/1143.py)

[📖 14. 2-D Dynamic Programming lesson](../learning/15-dp-2d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 14. 2-D Dynamic Programming problems](../rmap-practice/14-dp-2d.md)

---

Find the length of the longest subsequence common to two strings. When the current characters of both strings match, why does the answer extend the diagonal neighbor; when they don't, why take the best of the two adjacent cells?

<details>
<summary>Hint</summary>

Build a 2-D [DP](../algorithms/dynamic-programming.md) grid where `dp[i][j]` = LCS of the prefixes `text1[:i]` and `text2[:j]`. If `text1[i-1] == text2[j-1]`, extend the diagonal (`dp[i-1][j-1] + 1`); otherwise take the best of skipping a character from either string.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:

        m = len(text1)
        n = len(text2)

        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        return dp[m][n]
```

Building blocks: [nested-lists](../syntax/nested-lists.md) · [for-loop](../syntax/for-loop.md) (nested) · [comparison-operators](../syntax/comparison-operators.md) (`max()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(m · n)** — every cell computed once.
**Space: O(m · n)** — the DP grid (can be optimized to O(n) with two rows).
</details>

---
