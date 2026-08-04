# 309. Best Time to Buy and Sell Stock with Cooldown

**Medium** · [LeetCode](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/)

[📖 14. 2-D Dynamic Programming lesson](../learning/15-dp-2d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 14. 2-D Dynamic Programming problems](../rmap-practice/14-dp-2d.md)

---

Solution: not yet solved in this repo.

Maximize profit from unlimited buy/sell transactions, with a mandatory 1-day cooldown after selling. What two states (holding a stock, or not) do you need to track each day, and how does the cooldown affect the transition into "not holding"?

<details>
<summary>Hint</summary>

[DP](../algorithms/dynamic-programming.md) over `(day, holding)` state: if holding, you either keep holding or sell (moving to not-holding, but you can't buy again tomorrow); if not holding, you either wait or buy (moving to holding).
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def maxProfit(self, prices: List[int]) -> int:

        memo = {}

        def dfs(i, holding):
            if i >= len(prices):
                return 0
            if (i, holding) in memo:
                return memo[(i, holding)]

            cooldown = dfs(i + 1, holding)
            if holding:
                sell = prices[i] + dfs(i + 2, False)   # selling forces a cooldown day
                best = max(cooldown, sell)
            else:
                buy = -prices[i] + dfs(i + 1, True)
                best = max(cooldown, buy)

            memo[(i, holding)] = best
            return best

        return dfs(0, False)
```

Building blocks: [dict-basics](../syntax/dict-basics.md) (memoization) · [recursion-basics](../syntax/recursion-basics.md) · [comparison-operators](../syntax/comparison-operators.md) (`max()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — each `(day, holding)` state is computed once thanks to memoization.
**Space: O(n)** — the memo table and recursion stack.
</details>

---
