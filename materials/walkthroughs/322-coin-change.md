# 322. Coin Change

**Medium** · [LeetCode](https://leetcode.com/problems/coin-change/) · [Solution file (no hints)](../../problems/0001-0499/322.py)

[📖 13. 1-D Dynamic Programming lesson](../learning/14-dp-1d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 13. 1-D Dynamic Programming problems](../rmap-practice/13-dp-1d.md)

---

Find the fewest coins needed to make up an amount (or -1 if impossible). Why does building up the answer for every amount from 0 to target, using already-solved smaller amounts, beat trying every combination of coins directly?

<details>
<summary>Hint</summary>

Bottom-up [DP](../algorithms/dynamic-programming.md): `min_coins(amount) = 1 + min(min_coins(amount - coin) for every coin)`. Build an array indexed by amount, starting from 0.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:

        dp = [0] + [float("inf")] * amount

        for i in range(1, amount + 1):
            for coin in coins:
                if coin <= i:
                    dp[i] = min(dp[i], dp[i - coin] + 1)

        return dp[amount] if dp[amount] != float("inf") else -1
```

Building blocks: [list-basics](../syntax/list-basics.md) · [for-loop](../syntax/for-loop.md) (nested) · [comparison-operators](../syntax/comparison-operators.md) (`min()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(amount · len(coins))** — for every amount, try every coin.
**Space: O(amount)** — the DP array.
</details>

---
