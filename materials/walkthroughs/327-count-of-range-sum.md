# 327. Count of Range Sum

**Hard** · [LeetCode](https://leetcode.com/problems/count-of-range-sum/)

[📖 20. Segment Trees & Fenwick Trees lesson](../learning/20-segment-trees.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 20. Segment Trees & Fenwick Trees problems](../rmap-practice/20-segment-trees.md)

---

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
