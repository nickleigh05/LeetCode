# 45. Jump Game II

**Medium** · [LeetCode](https://leetcode.com/problems/jump-game-ii/)

[📖 15. Greedy lesson](../learning/16-greedy.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 15. Greedy problems](../rmap-practice/15-greedy.md)

---

Solution: not yet solved in this repo.

Same setup as [55](#55-jump-game--medium), but find the minimum number of jumps to reach the end. Why does tracking "the farthest reachable within the current jump" versus "the farthest reachable within the next jump" let you count jumps without simulating every path?

<details>
<summary>Hint</summary>

This is a greedy BFS-by-levels idea: track the boundary of the current jump's reach, and a running "farthest reachable" seen while scanning it. Once you scan past the current boundary, that's a new jump, and the boundary advances to the farthest seen.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def jump(self, nums: List[int]) -> int:

        jumps = 0
        current_end = 0   # farthest index reachable within the current jump
        farthest = 0      # farthest index reachable seen so far

        for i in range(len(nums) - 1):
            farthest = max(farthest, i + nums[i])

            if i == current_end:
                jumps += 1
                current_end = farthest

        return jumps
```

Building blocks: [for-loop](../syntax/for-loop.md) · [comparison-operators](../syntax/comparison-operators.md) (`max()`) · [arithmetic-operators](../syntax/arithmetic-operators.md) (`+=`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — a single pass over the array.
**Space: O(1)** — a few running variables.
</details>

---
