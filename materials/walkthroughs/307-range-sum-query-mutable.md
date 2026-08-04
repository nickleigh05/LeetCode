# 307. Range Sum Query — Mutable

**Medium** · [LeetCode](https://leetcode.com/problems/range-sum-query-mutable/)

[📖 19. Segment Trees & Fenwick Trees lesson](../learning/20-segment-trees.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 19. Segment Trees & Fenwick Trees problems](../rmap-practice/19-segment-trees.md)

---

Solution: not yet solved in this repo.

Support two operations on an array: update one element, and return the sum of a range `[left, right]` — both called many times. Why does a plain prefix-sum array make one of these O(n), and what structure makes both O(log n)?

<details>
<summary>Hint</summary>

A prefix-sum array answers range sums in O(1) but a single update invalidates every prefix after it — O(n) to rebuild. A [Fenwick tree](../data-structures/fenwick-tree.md) (or [segment tree](../data-structures/segment-tree.md)) stores partial sums so both `update` and `query` touch only O(log n) nodes. For updates, pass the *delta* `val - nums[i]`, not the new value.
</details>

<details>
<summary>Solution</summary>

```python
class NumArray:

    def __init__(self, nums: List[int]):
        self.n = len(nums)
        self.nums = nums[:]
        self.tree = [0] * (self.n + 1)   # 1-indexed Fenwick tree

        for i, val in enumerate(nums):
            self._add(i + 1, val)

    def _add(self, i: int, delta: int) -> None:
        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)   # climb to the next responsible node

    def _prefix(self, i: int) -> int:
        total = 0
        while i > 0:
            total += self.tree[i]
            i -= i & (-i)   # strip the lowest set bit
        return total

    def update(self, index: int, val: int) -> None:
        self._add(index + 1, val - self.nums[index])
        self.nums[index] = val

    def sumRange(self, left: int, right: int) -> int:
        return self._prefix(right + 1) - self._prefix(left)
```

Building blocks: [Fenwick tree](../data-structures/fenwick-tree.md) · [class-basics](../syntax/class-basics.md) · [init-method](../syntax/init-method.md) · [bitwise-operators](../syntax/bitwise-operators.md) (`i & -i`) · [while-loop](../syntax/while-loop.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(log n)** per update and per range query; O(n log n) to build.
**Space: O(n)** — the tree array.
</details>

---
