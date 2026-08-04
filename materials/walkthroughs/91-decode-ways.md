# 91. Decode Ways

**Medium** · [LeetCode](https://leetcode.com/problems/decode-ways/)

[📖 13. 1-D Dynamic Programming lesson](../learning/14-dp-1d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 13. 1-D Dynamic Programming problems](../rmap-practice/13-dp-1d.md)

---

Solution: not yet solved in this repo.

A digit string can decode to letters (1='A' ... 26='Z'); count the number of ways to decode it. At each position, when can you decode just one digit, and when can you also decode it paired with the previous digit?

<details>
<summary>Hint</summary>

[DP](../algorithms/dynamic-programming.md) from the end backward: `ways(i) = ways(i+1)` if `s[i] != "0"`, plus `ways(i+2)` if the two-digit number `s[i:i+2]` is between 10 and 26.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def numDecodings(self, s: str) -> int:

        n = len(s)
        dp_next = 1    # ways to decode s[i + 1:]
        dp_next2 = 0   # ways to decode s[i + 2:]

        for i in range(n - 1, -1, -1):
            if s[i] == "0":
                current = 0
            else:
                current = dp_next
                if i + 1 < n and 10 <= int(s[i:i + 2]) <= 26:
                    current += dp_next2

            dp_next2 = dp_next
            dp_next = current

        return dp_next
```

Building blocks: [range-function](../syntax/range-function.md) (reverse step) · [chained-comparisons](../syntax/chained-comparisons.md) · [type-conversion](../syntax/type-conversion.md) (`int()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — one backward pass over the digits.
**Space: O(1)** — only two running variables.
</details>

---
