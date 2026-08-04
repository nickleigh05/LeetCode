# 647. Palindromic Substrings

**Medium** · [LeetCode](https://leetcode.com/problems/palindromic-substrings/)

[📖 13. 1-D Dynamic Programming lesson](../learning/14-dp-1d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 13. 1-D Dynamic Programming problems](../rmap-practice/13-dp-1d.md)

---

Solution: not yet solved in this repo.

Count how many substrings of a string are palindromes. How does the same center-expansion idea from [5](#5-longest-palindromic-substring--medium) let you *count* instead of just find the longest?

<details>
<summary>Hint</summary>

Expand from every center (odd and even, same as [5](#5-longest-palindromic-substring--medium)), and count one palindrome for every successful expansion step rather than tracking the longest.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def countSubstrings(self, s: str) -> int:

        def count_expand(left, right):
            count = 0
            while left >= 0 and right < len(s) and s[left] == s[right]:
                count += 1
                left -= 1
                right += 1
            return count

        total = 0
        for i in range(len(s)):
            total += count_expand(i, i)
            total += count_expand(i, i + 1)

        return total
```

Building blocks: [while-loop](../syntax/while-loop.md) · [for-loop](../syntax/for-loop.md) · [arithmetic-operators](../syntax/arithmetic-operators.md) (`+=`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n²)** — n centers, each expansion up to O(n).
**Space: O(1)** — only a running counter.
</details>

---
