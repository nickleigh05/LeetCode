# 678. Valid Parenthesis String

**Medium** · [LeetCode](https://leetcode.com/problems/valid-parenthesis-string/)

[📖 15. Greedy lesson](../learning/16-greedy.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 15. Greedy problems](../rmap-practice/15-greedy.md)

---

Solution: not yet solved in this repo.

Determine if a string with `(`, `)`, and `*` (wildcard for `(`, `)`, or empty) can be valid parentheses. Why does tracking a *range* of possible open-parens counts, instead of one exact count, handle the wildcard's ambiguity?

<details>
<summary>Hint</summary>

Track `lo` (fewest possible open parens, treating `*` as `)` or empty when helpful) and `hi` (most possible open parens, treating `*` as `(`). If `hi` ever drops below 0, it's invalid; at the end, it's valid if `lo` can reach 0.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def checkValidString(self, s: str) -> bool:

        low = 0    # fewest possible unmatched open parens
        high = 0   # most possible unmatched open parens

        for char in s:
            if char == "(":
                low += 1
                high += 1
            elif char == ")":
                low -= 1
                high -= 1
            else:
                low -= 1
                high += 1

            if high < 0:
                return False
            low = max(low, 0)

        return low == 0
```

Building blocks: [for-loop](../syntax/for-loop.md) · [elif-else](../syntax/elif-else.md) · [comparison-operators](../syntax/comparison-operators.md) (`max()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — a single pass over the string.
**Space: O(1)** — two running variables.
</details>
