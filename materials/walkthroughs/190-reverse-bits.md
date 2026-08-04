# 190. Reverse Bits

**Easy** · [LeetCode](https://leetcode.com/problems/reverse-bits/) · [Solution file (no hints)](../../problems/0001-0499/190.py)

[📖 18. Bit Manipulation lesson](../learning/18-bit-manipulation.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 18. Bit Manipulation problems](../rmap-practice/18-bit-manipulation.md)

---

Reverse the bits of a 32-bit unsigned integer. Why does building the result bit by bit — shifting the result left and pulling each source bit off the right — naturally reverse the order?

<details>
<summary>Hint</summary>

Process 32 times: shift the result left to make room, then OR in the lowest bit of `n` (see [bitwise operators](../syntax/bitwise-operators.md)); shift `n` right to move to its next bit. Building the result this way reverses the bit order.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def reverseBits(self, n: int) -> int:

        result = 0

        for i in range(32):
            bit = (n >> i) & 1
            result = result | (bit << (31 - i))
        return result
```

Building blocks: [bitwise-operators](../syntax/bitwise-operators.md) (`>>`, `<<`, `&`, `|`) · [for-loop](../syntax/for-loop.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(1)** — always exactly 32 iterations.
**Space: O(1)** — one running result variable.
</details>

---
