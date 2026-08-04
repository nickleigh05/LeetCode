# 136. Single Number

**Easy** · [LeetCode](https://leetcode.com/problems/single-number/) · [Solution file (no hints)](../../problems/0001-0499/136.py)

[📖 18. Bit Manipulation lesson](../learning/18-bit-manipulation.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 18. Bit Manipulation problems](../rmap-practice/18-bit-manipulation.md)

---

Every number appears twice except one; find that one in O(1) space. Why does XOR-ing everything together cancel out all the pairs and leave only the single number?

<details>
<summary>Hint</summary>

XOR is its own inverse: `a ^ a = 0` and `a ^ 0 = a` (see [bitwise operators](../syntax/bitwise-operators.md)). XOR-ing every number together cancels every pair to 0, leaving only the number that appears once.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def singleNumber(self, nums: List[int]) -> int:

        res = 0
        for num in nums:
            res ^= num
        return res
```

Building blocks: [bitwise-operators](../syntax/bitwise-operators.md) (`^`) · [for-loop](../syntax/for-loop.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — a single pass over the array.
**Space: O(1)** — one running variable.
</details>

---
