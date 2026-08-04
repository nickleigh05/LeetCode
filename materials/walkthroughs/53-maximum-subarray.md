# 53. Maximum Subarray

**Medium** · [LeetCode](https://leetcode.com/problems/maximum-subarray/) · [Solution file (no hints)](../../problems/0001-0499/53.py)

[📖 15. Greedy lesson](../learning/16-greedy.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 15. Greedy problems](../rmap-practice/15-greedy.md)

---

Find the contiguous subarray with the largest sum. Why does a running sum reset to 0 the moment it goes negative — what would carrying a negative sum forward ever gain you?

<details>
<summary>Hint</summary>

This is [Kadane's algorithm](../algorithms/kadane-algorithm.md): at each element, the best subarray ending here either extends the previous running sum or starts fresh at this element — a negative prefix can only hurt any subarray that follows it.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:

        max_sum = nums[0]
        cur_sum = nums[0]

        for i in range(1, len(nums)):
            cur_sum = max(nums[i], cur_sum + nums[i])
            max_sum = max(max_sum, cur_sum)

        return max_sum
```

Building blocks: [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md) · [comparison-operators](../syntax/comparison-operators.md) (`max()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — a single pass over the array.
**Space: O(1)** — two running variables.
</details>

---
