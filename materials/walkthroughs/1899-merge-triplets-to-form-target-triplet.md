# 1899. Merge Triplets to Form Target Triplet

**Medium** · [LeetCode](https://leetcode.com/problems/merge-triplets-to-form-target-triplet/)

[📖 15. Greedy lesson](../learning/16-greedy.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 15. Greedy problems](../rmap-practice/15-greedy.md)

---

Solution: not yet solved in this repo.

Given triplets, determine if some subset can be merged (taking the max of each position) to form a target triplet. Why must you discard any triplet with a value exceeding the target in *any* position, no exceptions?

<details>
<summary>Hint</summary>

Any triplet with a component greater than the target's matching component can never be used — merging only takes maxes, so it would overshoot. Filter to only "safe" triplets, then check whether each target position is matched by at least one of them.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def mergeTriplets(self, triplets: List[List[int]], target: List[int]) -> bool:

        good = set()

        for triplet in triplets:
            if triplet[0] > target[0] or triplet[1] > target[1] or triplet[2] > target[2]:
                continue

            for i in range(3):
                if triplet[i] == target[i]:
                    good.add(i)

        return len(good) == 3
```

Building blocks: [set-basics](../syntax/set-basics.md) · [for-loop](../syntax/for-loop.md) · [break-continue](../syntax/break-continue.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — one pass over the triplets.
**Space: O(1)** — the `good` set is capped at 3 elements.
</details>

---
