# 268. Missing Number

**Easy** · [LeetCode](https://leetcode.com/problems/missing-number/) · [Solution file (no hints)](../../problems/0001-0499/268.py)

[📖 18. Bit Manipulation lesson](../learning/18-bit-manipulation.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 18. Bit Manipulation problems](../rmap-practice/18-bit-manipulation.md)

---

Given n distinct numbers from `[0, n]` with one missing, find it. Why does XOR-ing every index and every value together leave only the missing number?

<details>
<summary>Hint</summary>

XOR every index `0..n` together with every value in `nums` (see [bitwise operators](../syntax/bitwise-operators.md)). Every number that's present cancels with its matching index, leaving only the number that has no partner — the missing one.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def missingNumber(self, nums: List[int]) -> int:

        res = len(nums)   # accounts for index n, which has no matching nums index

        for i, num in enumerate(nums):
            res ^= i ^ num
        return res
```

Building blocks: [bitwise-operators](../syntax/bitwise-operators.md) (`^`) · [enumerate](../syntax/enumerate.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — a single pass over the array.
**Space: O(1)** — one running variable.
</details>

---
