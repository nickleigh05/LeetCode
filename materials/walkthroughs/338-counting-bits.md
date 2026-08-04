# 338. Counting Bits

**Easy** · [LeetCode](https://leetcode.com/problems/counting-bits/) · [Solution file (no hints)](../../problems/0001-0499/338.py)

[📖 18. Bit Manipulation lesson](../learning/18-bit-manipulation.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 18. Bit Manipulation problems](../rmap-practice/18-bit-manipulation.md)

---

For every number from 0 to n, count its set bits. Why does the set-bit count of `i` equal the set-bit count of `i` with its lowest bit removed, plus 1?

<details>
<summary>Hint</summary>

[DP](../algorithms/dynamic-programming.md) building on smaller answers: `bits(i) = bits(i >> 1) + (i & 1)` (equivalently `bits(i // 2) + i % 2`) — dropping the lowest bit, then adding it back in if it was a 1.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def countBits(self, n: int) -> List[int]:

        ans = [0] * (n + 1)

        for i in range(1, n + 1):
            ans[i] = ans[i // 2] + (i % 2)
        return ans
```

Building blocks: [list-basics](../syntax/list-basics.md) · [integer-division-modulo](../syntax/integer-division-modulo.md) (`//`, `%`) · [for-loop](../syntax/for-loop.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — each answer computed in O(1) from a smaller one.
**Space: O(n)** — the output array.
</details>

---
