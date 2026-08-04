# 494. Target Sum

**Medium** · [LeetCode](https://leetcode.com/problems/target-sum/)

[📖 14. 2-D Dynamic Programming lesson](../learning/15-dp-2d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 14. 2-D Dynamic Programming problems](../rmap-practice/14-dp-2d.md)

---

Solution: not yet solved in this repo.

Assign `+` or `-` to each number so the expression equals a target; count the ways. Why does memoizing on `(index, running_total)` collapse a tree of exponential branches into a manageable number of states?

<details>
<summary>Hint</summary>

[Backtrack](../algorithms/backtracking.md) trying both `+num` and `-num` at each index, but memoize on `(index, current_total)` — many different `+`/`-` choices can reach the same total at the same index, so memoization avoids recomputing them (see [Dynamic Programming](../algorithms/dynamic-programming.md)).
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:

        memo = {}

        def dfs(i, total):
            if i == len(nums):
                return 1 if total == target else 0
            if (i, total) in memo:
                return memo[(i, total)]

            memo[(i, total)] = dfs(i + 1, total + nums[i]) + dfs(i + 1, total - nums[i])
            return memo[(i, total)]

        return dfs(0, 0)
```

Building blocks: [dict-basics](../syntax/dict-basics.md) (memoization) · [recursion-basics](../syntax/recursion-basics.md) · [ternary-expression](../syntax/ternary-expression.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n · sum(nums))** — bounded by the number of distinct `(index, total)` states.
**Space: O(n · sum(nums))** — the memo table and recursion stack.
</details>

---
