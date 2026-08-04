# 134. Gas Station

**Medium** · [LeetCode](https://leetcode.com/problems/gas-station/)

[📖 15. Greedy lesson](../learning/16-greedy.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 15. Greedy problems](../rmap-practice/15-greedy.md)

---

Solution: not yet solved in this repo.

Find the starting gas station that lets you complete a full circuit (or -1 if none). Why does the first station where your running tank never goes negative, after any earlier attempt already failed, have to be the answer?

<details>
<summary>Hint</summary>

If the total gas is less than total cost, no solution exists. Otherwise greedily track a running tank total; whenever it goes negative, the current start is invalid, so reset the candidate start to the *next* station and reset the running tank — the total-gas check guarantees some start works.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:

        if sum(gas) < sum(cost):
            return -1

        total = 0
        start = 0

        for i in range(len(gas)):
            total += gas[i] - cost[i]
            if total < 0:
                start = i + 1
                total = 0

        return start
```

Building blocks: [for-loop](../syntax/for-loop.md) · [if-return](../syntax/if-return.md) · [comparison-operators](../syntax/comparison-operators.md) (`sum()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — a single pass over the stations.
**Space: O(1)** — a couple of running variables.
</details>

---
