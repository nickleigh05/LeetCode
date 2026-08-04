# 518. Coin Change II

**Medium** · [LeetCode](https://leetcode.com/problems/coin-change-ii/)

[📖 14. 2-D Dynamic Programming lesson](../learning/15-dp-2d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 14. 2-D Dynamic Programming problems](../rmap-practice/14-dp-2d.md)

---

Solution: not yet solved in this repo.

Count the number of ways to make up an amount using unlimited coins (order doesn't matter). Why does iterating coins in the *outer* loop (not the amount) prevent counting the same combination as multiple different permutations?

<details>
<summary>Hint</summary>

Classic unbounded-knapsack [DP](../algorithms/dynamic-programming.md): `ways[a] += ways[a - coin]`. Looping coins on the outside and amounts on the inside ensures each coin is only ever "added" in one relative order, so `[1,2]` and `[2,1]` aren't double-counted.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def change(self, amount: int, coins: List[int]) -> int:

        dp = [0] * (amount + 1)
        dp[0] = 1

        for coin in coins:   # coins on the outer loop so permutations aren't double-counted
            for a in range(coin, amount + 1):
                dp[a] += dp[a - coin]

        return dp[amount]
```

Building blocks: [list-basics](../syntax/list-basics.md) · [for-loop](../syntax/for-loop.md) (nested) · [arithmetic-operators](../syntax/arithmetic-operators.md) (`+=`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(amount · len(coins))** — for every coin, iterate over every amount.
**Space: O(amount)** — the DP array.
</details>

---
