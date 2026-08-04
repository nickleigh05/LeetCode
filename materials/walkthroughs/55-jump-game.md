# 55. Jump Game

**Medium** · [LeetCode](https://leetcode.com/problems/jump-game/)

[📖 15. Greedy lesson](../learning/16-greedy.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 15. Greedy problems](../rmap-practice/15-greedy.md)

---

Solution: not yet solved in this repo.

Given max-jump distances at each index, determine if you can reach the last index. Why does tracking only the farthest reachable index — rather than every possible path — settle this in one pass?

<details>
<summary>Hint</summary>

Greedily track `farthest` reachable so far. Walking left to right, if the current index ever exceeds `farthest`, you're stuck; otherwise extend `farthest` to `max(farthest, i + nums[i])`.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def canJump(self, nums: List[int]) -> bool:

        farthest = 0

        for i, num in enumerate(nums):
            if i > farthest:
                return False
            farthest = max(farthest, i + num)

        return True
```

Building blocks: [enumerate](../syntax/enumerate.md) · [if-return](../syntax/if-return.md) · [comparison-operators](../syntax/comparison-operators.md) (`max()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — a single pass over the array.
**Space: O(1)** — one running variable.
</details>

---
