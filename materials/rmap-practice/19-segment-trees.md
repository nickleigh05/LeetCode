# 19. Segment Trees & Fenwick Trees — Practice

This is the mastery-track set: fewer problems, all of them about range queries on a changing array. If you want more volume after these, search LeetCode's "Binary Indexed Tree" and "Segment Tree" tags.

[← Back to the lesson](../learning/20-segment-trees.md) · [🗺 Roadmap](../../roadmap.md)

---

### 307. Range Sum Query — Mutable — Medium
[LeetCode](https://leetcode.com/problems/range-sum-query-mutable/)  
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

### 315. Count of Smaller Numbers After Self — Hard
[LeetCode](https://leetcode.com/problems/count-of-smaller-numbers-after-self/)  
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

### 493. Reverse Pairs — Hard
[LeetCode](https://leetcode.com/problems/reverse-pairs/)  
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

### 327. Count of Range Sum — Hard
[LeetCode](https://leetcode.com/problems/count-of-range-sum/)  
Solution: not yet solved in this repo.

Count subarrays whose sum lies in `[lower, upper]`. A subarray sum is a difference of two prefix sums — can you rewrite the condition as a range query over prefix sums you've already seen?

<details>
<summary>Hint</summary>

`lower <= S[j] - S[i] <= upper` means the earlier prefix `S[i]` must lie in `[S[j] - upper, S[j] - lower]`. Sweep the prefix sums in order, and for each `S[j]` count how many earlier prefixes fall in that window — a range count over a [Fenwick tree](../data-structures/fenwick-tree.md) built on the compressed prefix-sum values (don't forget to seed `S = 0` before the sweep).
</details>

<details>
<summary>Solution</summary>

```python
import bisect
from itertools import accumulate

class Solution:
    def countRangeSum(self, nums: List[int], lower: int, upper: int) -> int:

        prefixes = [0] + list(accumulate(nums))
        all_vals = sorted(set(prefixes))
        rank = {val: i + 1 for i, val in enumerate(all_vals)}
        tree = [0] * (len(all_vals) + 1)

        def add(i):
            while i <= len(all_vals):
                tree[i] += 1
                i += i & (-i)

        def count_leq(val):
            i = bisect.bisect_right(all_vals, val)
            total = 0
            while i > 0:
                total += tree[i]
                i -= i & (-i)
            return total

        count = 0
        for prefix_sum in prefixes:
            # earlier prefixes p with prefix_sum - upper <= p <= prefix_sum - lower
            count += count_leq(prefix_sum - lower) - count_leq(prefix_sum - upper - 1)
            add(rank[prefix_sum])
        return count
```

Building blocks: [Fenwick tree](../data-structures/fenwick-tree.md) · [prefix sums](../learning/01b-prefix-sums.md) · [itertools-basics](../syntax/itertools-basics.md) (`accumulate`) · [dict-comprehension](../syntax/dict-comprehension.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n log n)** — compression sort plus two O(log n) counts and one update per prefix.
**Space: O(n)** — prefix sums, rank map, tree.
</details>

---

[← Back to the lesson](../learning/20-segment-trees.md) · [🗺 Roadmap](../../roadmap.md)
