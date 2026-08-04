# 97. Interleaving String

**Medium** · [LeetCode](https://leetcode.com/problems/interleaving-string/)

[📖 14. 2-D Dynamic Programming lesson](../learning/15-dp-2d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 14. 2-D Dynamic Programming problems](../rmap-practice/14-dp-2d.md)

---

Solution: not yet solved in this repo.

Determine if `s3` can be formed by interleaving `s1` and `s2` while preserving each one's character order. At each pair of positions `(i, j)` in `s1` and `s2`, what determines whether you're still "on track" to build `s3`?

<details>
<summary>Hint</summary>

[2-D DP](../algorithms/dynamic-programming.md): `dp[i][j]` = can `s1[i:]` and `s2[j:]` interleave to form `s3[i+j:]`. It's True if either `s1[i]` matches `s3[i+j]` and `dp[i+1][j]` is True, or `s2[j]` matches and `dp[i][j+1]` is True.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:

        m = len(s1)
        n = len(s2)
        if m + n != len(s3):
            return False

        dp = [[False] * (n + 1) for _ in range(m + 1)]
        dp[m][n] = True

        for i in range(m, -1, -1):
            for j in range(n, -1, -1):
                if i < m and s1[i] == s3[i + j] and dp[i + 1][j]:
                    dp[i][j] = True
                if j < n and s2[j] == s3[i + j] and dp[i][j + 1]:
                    dp[i][j] = True

        return dp[0][0]
```

Building blocks: [nested-lists](../syntax/nested-lists.md) · [for-loop](../syntax/for-loop.md) (reverse range) · [logical-operators](../syntax/logical-operators.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(m · n)** — every cell computed once.
**Space: O(m · n)** — the DP grid.
</details>

---
