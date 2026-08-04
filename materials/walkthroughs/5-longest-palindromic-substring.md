# 5. Longest Palindromic Substring

**Medium** · [LeetCode](https://leetcode.com/problems/longest-palindromic-substring/)

[📖 13. 1-D Dynamic Programming lesson](../learning/14-dp-1d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 13. 1-D Dynamic Programming problems](../rmap-practice/13-dp-1d.md)

---

Solution: not yet solved in this repo.

Find the longest palindromic substring. Why does expanding outward from each possible *center* (single character or between two characters) cover every possible palindrome?

<details>
<summary>Hint</summary>

For each index, expand outward with two pointers while characters match, once treating the index as an odd-length center and once as an even-length center (pairing it with the next index). Track the longest expansion seen.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def longestPalindrome(self, s: str) -> str:

        def expand(left, right):
            while left >= 0 and right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
            return s[left + 1:right]

        best = ""
        for i in range(len(s)):
            odd = expand(i, i)
            even = expand(i, i + 1)
            best = max(best, odd, even, key=len)

        return best
```

Building blocks: [while-loop](../syntax/while-loop.md) · [for-loop](../syntax/for-loop.md) · [sorting-key](../syntax/sorting-key.md) (`max(..., key=len)`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n²)** — n centers, each expansion up to O(n).
**Space: O(1)** extra beyond the returned substring.
</details>

---
