# 371. Sum of Two Integers

**Medium** · [LeetCode](https://leetcode.com/problems/sum-of-two-integers/)

[📖 18. Bit Manipulation lesson](../learning/18-bit-manipulation.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 18. Bit Manipulation problems](../rmap-practice/18-bit-manipulation.md)

---

Solution: not yet solved in this repo.

Add two integers without using `+` or `-`. Why does XOR give you the "sum without carrying," while AND-then-shift gives you exactly the carry to add in next?

<details>
<summary>Hint</summary>

`a ^ b` (see [bitwise operators](../syntax/bitwise-operators.md)) adds bits without carrying; `(a & b) << 1` computes the carry that resulted. Repeat — treating the XOR as the new sum and the shifted AND as the new "b" to add — until there's no carry left.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def getSum(self, a: int, b: int) -> int:

        mask = 0xFFFFFFFF   # keep results within 32 bits

        while b & mask:
            carry = (a & b) << 1
            a = (a ^ b) & mask
            b = carry & mask

        if a > 0x7FFFFFFF:   # reinterpret as a negative 32-bit signed number
            a = ~(a ^ mask)

        return a
```

Building blocks: [bitwise-operators](../syntax/bitwise-operators.md) (`^`, `&`, `<<`, `~`) · [while-loop](../syntax/while-loop.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(1)** — bounded by 32 bit positions.
**Space: O(1)** — a few running variables.
</details>

---
