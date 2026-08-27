# 493. Reverse Pairs

**Hard** · [LeetCode](https://leetcode.com/problems/reverse-pairs/)

[📖 19. Segment Trees & Fenwick Trees lesson](../learning/20-segment-trees.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 19. Segment Trees & Fenwick Trees problems](../rmap-practice/19-segment-trees.md)

---

Solution: not yet solved in this repo.

Count pairs `i < j` with `nums[i] > 2 * nums[j]`. It's Count-of-Smaller with a twist: the value you *query* isn't the value you *insert*. What two coordinate sets do you need to compress together?

<details>
<summary>Hint</summary>

Sweep left-to-right: before inserting `nums[j]`, count how many already-seen values are `> 2 * nums[j]`. Compress the union of all `v` and all `2*v` into one rank space so both the query key and the insert key have positions in the same [Fenwick tree](../data-structures/fenwick-tree.md). (A merge-sort count — see [merge sort](../algorithms/merge-sort.md) — is the classic alternative.)
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def reversePairs(self, nums: List[int]) -> int:

        all_vals = sorted({v for num in nums for v in (num, 2 * num)})
        rank = {val: i + 1 for i, val in enumerate(all_vals)}
        tree = [0] * (len(all_vals) + 1)

        def add(i):
            while i <= len(all_vals):
                tree[i] += 1
                i += i & (-i)

        def prefix(i):
            total = 0
            while i > 0:
                total += tree[i]
                i -= i & (-i)
            return total

        seen = 0
        count = 0
        for num in nums:
            count += seen - prefix(rank[2 * num])   # seen values > 2 * num form pairs
            add(rank[num])
            seen += 1
        return count
```

Building blocks: [Fenwick tree](../data-structures/fenwick-tree.md) · [set-comprehension](../syntax/set-comprehension.md) · [dict-comprehension](../syntax/dict-comprehension.md) · [sorting-key](../syntax/sorting-key.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n log n)** — compression sort plus O(log n) tree work per element.
**Space: O(n)** — the compressed rank space and the tree.
</details>

---
