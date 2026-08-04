# 139. Word Break

**Medium** · [LeetCode](https://leetcode.com/problems/word-break/)

[📖 13. 1-D Dynamic Programming lesson](../learning/14-dp-1d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 13. 1-D Dynamic Programming problems](../rmap-practice/13-dp-1d.md)

---

Solution: not yet solved in this repo.

Determine if a string can be segmented into words from a dictionary. Why does "can `s[i:]` be segmented" only depend on trying every possible first word and checking if the *rest* can also be segmented?

<details>
<summary>Hint</summary>

[DP](../algorithms/dynamic-programming.md) from the end backward: `can_break(i)` is True if some `word` in the dictionary matches `s[i:i+len(word)]` *and* `can_break(i + len(word))` is also True.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:

        word_set = set(wordDict)
        n = len(s)
        dp = [False] * (n + 1)
        dp[n] = True   # empty remainder is always breakable

        for i in range(n - 1, -1, -1):
            for word in word_set:
                if i + len(word) <= n and s[i:i + len(word)] == word and dp[i + len(word)]:
                    dp[i] = True
                    break

        return dp[0]
```

Building blocks: [set-basics](../syntax/set-basics.md) · [list-basics](../syntax/list-basics.md) · [range-function](../syntax/range-function.md) (reverse step) · [break-continue](../syntax/break-continue.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n² · m)** — n string positions, each trying up to m dictionary words with O(n) slicing/comparison.
**Space: O(n + total dictionary size)** — the DP array and the word set.
</details>

---
