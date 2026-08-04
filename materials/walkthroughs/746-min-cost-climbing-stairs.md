# 746. Min Cost Climbing Stairs

**Easy** · [LeetCode](https://leetcode.com/problems/min-cost-climbing-stairs/) · [Solution file (no hints)](../../problems/0500-0999/746.py)

[📖 13. 1-D Dynamic Programming lesson](../learning/14-dp-1d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 13. 1-D Dynamic Programming problems](../rmap-practice/13-dp-1d.md)

---

Given a cost at each step, find the minimum cost to reach the top (starting from step 0 or 1). Why does the cheapest way to reach step i only depend on the cheapest ways to reach steps i-1 and i-2?

<details>
<summary>Hint</summary>

[DP](../algorithms/dynamic-programming.md): `cost_to_reach(i) = cost[i] + min(cost_to_reach(i-1), cost_to_reach(i-2))`. Build this bottom-up, then the answer is the min of the two ways to step past the last stair.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:

        n = len(cost)
        one_back = 0
        two_back = 0

        for i in range(2, n + 1):
            current = min(one_back + cost[i - 1], two_back + cost[i - 2])
            two_back = one_back
            one_back = current
        return one_back
```

Building blocks: [for-loop](../syntax/for-loop.md) · [comparison-operators](../syntax/comparison-operators.md) (`min()`) · [variables-assignment](../syntax/variables-assignment.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — one pass over the steps.
**Space: O(1)** — only two running variables.
</details>

---
