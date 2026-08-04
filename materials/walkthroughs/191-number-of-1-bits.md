# 191. Number of 1 Bits

**Easy** · [LeetCode](https://leetcode.com/problems/number-of-1-bits/) · [Solution file (no hints)](../../problems/0001-0499/191.py)

[📖 18. Bit Manipulation lesson](../learning/18-bit-manipulation.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 18. Bit Manipulation problems](../rmap-practice/18-bit-manipulation.md)

---

Count the number of 1 bits in an integer's binary representation. Why does `n & (n - 1)` always clear exactly the lowest set bit — and how does repeating that let you count set bits in a number of steps equal to their count?

<details>
<summary>Hint</summary>

Brian Kernighan's trick: `n & (n - 1)` (see [bitwise operators](../syntax/bitwise-operators.md)) clears the lowest set bit each time. Count how many times you can do that before `n` becomes 0.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def hammingWeight(self, n: int) -> int:

        count = 0
        while n:
            n &= n - 1   # clears the lowest set bit
            count += 1
        return count
```

Building blocks: [bitwise-operators](../syntax/bitwise-operators.md) (`&`) · [while-loop](../syntax/while-loop.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(k)** — k is the number of set bits (at most 32 for a standard integer).
**Space: O(1)** — one running counter.
</details>

---
