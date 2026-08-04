# 315. Count of Smaller Numbers After Self

**Hard** · [LeetCode](https://leetcode.com/problems/count-of-smaller-numbers-after-self/)

[📖 19. Segment Trees & Fenwick Trees lesson](../learning/20-segment-trees.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 19. Segment Trees & Fenwick Trees problems](../rmap-practice/19-segment-trees.md)

---

Solution: not yet solved in this repo.

For each element, count how many elements *to its right* are smaller. What can you maintain while sweeping right-to-left so that each count is a single range query?

<details>
<summary>Hint</summary>

Sweep from the right, keeping a frequency table of the values already seen. For each `x`, the answer is "how many seen values are `< x`" — a prefix count. A [Fenwick tree](../data-structures/fenwick-tree.md) over *value ranks* (sort the distinct values first — coordinate compression) answers that in O(log n). This is the worked trace in [the lesson](../learning/20-segment-trees.md#worked-trace--count-of-smaller-numbers-after-self).
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def countSmaller(self, nums: List[int]) -> List[int]:

        ranks = {val: i + 1 for i, val in enumerate(sorted(set(nums)))}
        tree = [0] * (len(ranks) + 1)

        def add(i):
            while i <= len(ranks):
                tree[i] += 1
                i += i & (-i)

        def prefix(i):
            total = 0
            while i > 0:
                total += tree[i]
                i -= i & (-i)
            return total

        result = []
        for num in reversed(nums):
            result.append(prefix(ranks[num] - 1))   # seen values strictly smaller
            add(ranks[num])
        return result[::-1]
```

Building blocks: [Fenwick tree](../data-structures/fenwick-tree.md) · [dict-comprehension](../syntax/dict-comprehension.md) · [set-basics](../syntax/set-basics.md) · [enumerate](../syntax/enumerate.md) · [list-slicing](../syntax/list-slicing.md) (`[::-1]`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n log n)** — one sort for compression, then one O(log n) query + update per element.
**Space: O(n)** — the rank map and the tree.
</details>

---
