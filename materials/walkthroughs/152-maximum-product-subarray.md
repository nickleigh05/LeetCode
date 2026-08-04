# 152. Maximum Product Subarray

**Medium** · [LeetCode](https://leetcode.com/problems/maximum-product-subarray/)

[📖 13. 1-D Dynamic Programming lesson](../learning/14-dp-1d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 13. 1-D Dynamic Programming problems](../rmap-practice/13-dp-1d.md)

---

Solution: not yet solved in this repo.

Find the contiguous subarray with the largest product. Why must you track both the running max *and* running min product, unlike [Kadane's algorithm](../algorithms/kadane-algorithm.md) for sums?

<details>
<summary>Hint</summary>

A negative number can turn the smallest (most negative) running product into the largest one. Track both `cur_max` and `cur_min` at each step, since either could become the new max after multiplying by a negative number.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def maxProduct(self, nums: List[int]) -> int:

        result = max(nums)
        cur_max = 1
        cur_min = 1

        for num in nums:
            if num == 0:
                cur_max = 1
                cur_min = 1
                continue

            tmp = cur_max * num
            cur_max = max(num, tmp, cur_min * num)
            cur_min = min(num, tmp, cur_min * num)
            result = max(result, cur_max)

        return result
```

Building blocks: [for-loop](../syntax/for-loop.md) · [break-continue](../syntax/break-continue.md) · [comparison-operators](../syntax/comparison-operators.md) (`max()`, `min()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — one pass over the array.
**Space: O(1)** — a few running variables.
</details>

---
