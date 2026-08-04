# 213. House Robber II

**Medium** · [LeetCode](https://leetcode.com/problems/house-robber-ii/)

[📖 13. 1-D Dynamic Programming lesson](../learning/14-dp-1d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 13. 1-D Dynamic Programming problems](../rmap-practice/13-dp-1d.md)

---

Solution: not yet solved in this repo.

Same as [198](#198-house-robber--medium), but houses are arranged in a circle (first and last are adjacent). Why does running the linear solution twice — once excluding the first house, once excluding the last — handle the wraparound?

<details>
<summary>Hint</summary>

Since the first and last houses can't both be robbed, run the [198](#198-house-robber--medium) [DP](../algorithms/dynamic-programming.md) twice: once on `houses[:-1]` (excluding the last), once on `houses[1:]` (excluding the first), and take the max of the two results.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def rob(self, nums: List[int]) -> int:

        if len(nums) == 1:
            return nums[0]

        def rob_linear(houses):
            prev, curr = 0, 0
            for num in houses:
                prev, curr = curr, max(curr, prev + num)
            return curr

        return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))
```

Building blocks: [list-slicing](../syntax/list-slicing.md) · [for-loop](../syntax/for-loop.md) · [comparison-operators](../syntax/comparison-operators.md) (`max()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — two linear passes over the houses.
**Space: O(1)** — only a couple of running variables per pass.
</details>

---
