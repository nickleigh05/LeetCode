# 787. Cheapest Flights Within K Stops

**Medium** · [LeetCode](https://leetcode.com/problems/cheapest-flights-within-k-stops/)

[📖 12. Advanced Graphs lesson](../learning/13-advanced-graphs.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 12. Advanced Graphs problems](../rmap-practice/12-advanced-graphs.md)

---

Solution: not yet solved in this repo.

Find the cheapest price from `src` to `dst` using at most `k` stops. Why does plain Dijkstra fail here, and why does Bellman-Ford (relaxing all edges exactly `k+1` times) respect the stop limit correctly?

<details>
<summary>Hint</summary>

Dijkstra doesn't track *how many edges* were used to reach the cheapest price, so it can miss valid cheaper routes constrained by stops. Instead run a Bellman-Ford-style relaxation for exactly `k + 1` rounds, using a *snapshot* of prices from the previous round each time so effects don't leak within a round.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:

        prices = [float("inf")] * n
        prices[src] = 0

        for _ in range(k + 1):
            tmp_prices = prices[:]   # snapshot so updates don't leak within a round

            for u, v, w in flights:
                if prices[u] != float("inf") and prices[u] + w < tmp_prices[v]:
                    tmp_prices[v] = prices[u] + w

            prices = tmp_prices

        return prices[dst] if prices[dst] != float("inf") else -1
```

Building blocks: [list-slicing](../syntax/list-slicing.md) (snapshot copy) · [for-loop](../syntax/for-loop.md) · [int-float-basics](../syntax/int-float-basics.md) (`float("inf")`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(k · E)** — k+1 rounds, each relaxing every edge once.
**Space: O(n)** — the prices array (and its snapshot).
</details>
