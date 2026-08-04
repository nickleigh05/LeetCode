# 115. Distinct Subsequences

**Hard** · [LeetCode](https://leetcode.com/problems/distinct-subsequences/)

[📖 14. 2-D Dynamic Programming lesson](../learning/15-dp-2d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 14. 2-D Dynamic Programming problems](../rmap-practice/14-dp-2d.md)

---

Solution: not yet solved in this repo.

Count how many distinct subsequences of `s` equal `t`. When `s[i] == t[j]`, why do you have *two* choices (use this character, or skip it), while a mismatch leaves only one?

<details>
<summary>Hint</summary>

[2-D DP](../algorithms/dynamic-programming.md): `dp[i][j]` = ways `s[i:]` forms `t[j:]`. If `s[i] == t[j]`, add the ways using this match (`dp[i+1][j+1]`) plus the ways skipping `s[i]` entirely (`dp[i+1][j]`); if not, only the skip option applies.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def numDistinct(self, s: str, t: str) -> int:

        m = len(s)
        n = len(t)

        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            dp[i][n] = 1   # an empty t is always formed exactly one way

        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                dp[i][j] = dp[i + 1][j]
                if s[i] == t[j]:
                    dp[i][j] += dp[i + 1][j + 1]

        return dp[0][0]
```

Building blocks: [nested-lists](../syntax/nested-lists.md) · [for-loop](../syntax/for-loop.md) (reverse range) · [arithmetic-operators](../syntax/arithmetic-operators.md) (`+=`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(m · n)** — every cell computed once.
**Space: O(m · n)** — the DP grid.
</details>

---
