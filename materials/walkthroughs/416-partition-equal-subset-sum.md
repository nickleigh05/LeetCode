# 416. Partition Equal Subset Sum

**Medium** · [LeetCode](https://leetcode.com/problems/partition-equal-subset-sum/)

[📖 13. 1-D Dynamic Programming lesson](../learning/14-dp-1d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 13. 1-D Dynamic Programming problems](../rmap-practice/13-dp-1d.md)

---

Solution: not yet solved in this repo.

Determine if an array can be split into two subsets with equal sums. Why does this reduce to "does some subset sum to exactly half the total" — a classic 0/1 knapsack shape?

<details>
<summary>Hint</summary>

If the total sum is odd, it's impossible. Otherwise this is 0/1 knapsack (see [Dynamic Programming](../algorithms/dynamic-programming.md)): track which sums are achievable using a [hashset](../data-structures/hashset.md), adding each number to every currently-achievable sum.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def canPartition(self, nums: List[int]) -> bool:

        total = sum(nums)
        if total % 2:
            return False

        target = total // 2
        achievable = {0}

        for num in nums:
            new_sums = {s + num for s in achievable if s + num <= target}
            achievable |= new_sums

        return target in achievable
```

Building blocks: [set-comprehension](../syntax/set-comprehension.md) · [for-loop](../syntax/for-loop.md) · [set-operations](../syntax/set-operations.md) (`|=`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n · target)** — n numbers, each potentially extending up to `target` achievable sums.
**Space: O(target)** — the achievable-sums set is bounded by the target value.
</details>
