# 198. House Robber

**Medium** · [LeetCode](https://leetcode.com/problems/house-robber/) · [Solution file (no hints)](../../problems/0001-0499/198.py)

[📖 13. 1-D Dynamic Programming lesson](../learning/14-dp-1d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 13. 1-D Dynamic Programming problems](../rmap-practice/13-dp-1d.md)

---

Rob houses in a line, maximizing loot, without robbing two adjacent houses. At each house, what's the choice between "rob it" and "skip it," and what do you need to know to make that choice?

<details>
<summary>Hint</summary>

[DP](../algorithms/dynamic-programming.md): at each house, either skip it (carry forward the best so far) or rob it (this house's value plus the best from two houses back, since the adjacent one is off-limits).
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def rob(self, nums: List[int]) -> int:

        prev, curr = 0, 0
        for num in nums:
            prev, curr = curr, max(curr, prev + num)
        return curr
```

Building blocks: [for-loop](../syntax/for-loop.md) · [comparison-operators](../syntax/comparison-operators.md) (`max()`) · [swap-tuple-assign](../syntax/swap-tuple-assign.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — one pass over the houses.
**Space: O(1)** — only two running variables.
</details>

---
