# 312. Burst Balloons

**Hard** · [LeetCode](https://leetcode.com/problems/burst-balloons/)

[📖 14. 2-D Dynamic Programming lesson](../learning/15-dp-2d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 14. 2-D Dynamic Programming problems](../rmap-practice/14-dp-2d.md)

---

Solution: not yet solved in this repo.

Burst all balloons for max coins, where bursting balloon `i` earns `left * nums[i] * right` using its *current* neighbors. Why does thinking about which balloon bursts *last* in a range (rather than first) make the subproblems independent?

<details>
<summary>Hint</summary>

Pad `nums` with 1s on both ends. For every range `(l, r)`, try every balloon `i` as the *last* one burst in that range — its neighbors at that point are guaranteed to be `nums[l-1]` and `nums[r+1]` (see [Dynamic Programming](../algorithms/dynamic-programming.md)), so the left and right sub-ranges can be solved independently.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def maxCoins(self, nums: List[int]) -> int:

        balloons = [1] + nums + [1]
        n = len(balloons)
        memo = {}

        def dp(left, right):
            if left + 1 == right:
                return 0
            if (left, right) in memo:
                return memo[(left, right)]

            best = 0
            for i in range(left + 1, right):   # try every balloon as the last one burst
                coins = balloons[left] * balloons[i] * balloons[right]
                coins += dp(left, i) + dp(i, right)
                best = max(best, coins)

            memo[(left, right)] = best
            return best

        return dp(0, n - 1)
```

Building blocks: [list-basics](../syntax/list-basics.md) (padding with `+`) · [dict-basics](../syntax/dict-basics.md) (memoization) · [recursion-basics](../syntax/recursion-basics.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n³)** — O(n²) ranges, each trying up to O(n) "last burst" choices.
**Space: O(n²)** — the memo table.
</details>

---
