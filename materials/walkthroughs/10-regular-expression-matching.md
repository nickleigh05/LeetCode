# 10. Regular Expression Matching

**Hard** · [LeetCode](https://leetcode.com/problems/regular-expression-matching/)

[📖 14. 2-D Dynamic Programming lesson](../learning/15-dp-2d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 14. 2-D Dynamic Programming problems](../rmap-practice/14-dp-2d.md)

---

Solution: not yet solved in this repo.

Implement regex matching supporting `.` (any char) and `*` (zero or more of the preceding char). Why does a `*` force you to consider *two* very different possibilities — using zero of the preceding char, or one-plus?

<details>
<summary>Hint</summary>

[2-D DP](../algorithms/dynamic-programming.md)/memoized recursion on `(i, j)` positions in `s` and `p`. On a plain character (or `.`), match one and advance both. On seeing a `*` next in `p`, either skip the "`char*`" pair entirely (zero occurrences) or, if the current characters match, consume one character of `s` and stay at the same position in `p` (one more occurrence).
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def isMatch(self, s: str, p: str) -> bool:

        memo = {}

        def dp(i, j):
            if (i, j) in memo:
                return memo[(i, j)]
            if j == len(p):
                return i == len(s)

            match = i < len(s) and p[j] in (s[i], ".")

            if j + 1 < len(p) and p[j + 1] == "*":
                result = dp(i, j + 2) or (match and dp(i + 1, j))   # skip "char*", or consume one char
            else:
                result = match and dp(i + 1, j + 1)

            memo[(i, j)] = result
            return result

        return dp(0, 0)
```

Building blocks: [dict-basics](../syntax/dict-basics.md) (memoization) · [recursion-basics](../syntax/recursion-basics.md) · [logical-operators](../syntax/logical-operators.md) (`and`, `or`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(m · n)** — bounded by the number of distinct `(i, j)` states.
**Space: O(m · n)** — the memo table and recursion stack.
</details>
