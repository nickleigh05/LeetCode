# 20. Segment Trees & Fenwick Trees

*Range queries with point updates in O(log n). The upgrade from prefix sums when the array changes.*

[← Prev](19-math-geometry.md) · [🗺 Roadmap](../roadmap.md)

---

> **Mastery track.** This lesson is optional for standard SWE interviews — you can skip it and still solve ~95% of interview problems. Add it when you're targeting hard-level competitive problems, system design involving range aggregation, or companies known for algorithm-heavy interviews.
>
> **Builds on:** [prefix sums (01b)](01b-prefix-sums.md) for the motivation, [trees (07)](07-trees.md) for tree traversal, and [recursion (04b)](04b-recursion.md) for the segment tree build/query recursion.

A prefix sum answers range sum queries in O(1) — but only if the array *never changes*. The moment you need to handle point updates between queries, rebuilding the prefix array costs O(n) per update. Segment trees and Fenwick trees reduce *both* queries and updates to O(log n).

## Concept

### When prefix sums aren't enough

```
  Problem: given an array, handle many interleaved:
    (a) update arr[i] = val         ← array changes!
    (b) query sum(l, r)

  Prefix sum: query O(1), but update forces O(n) rebuild → too slow.
  Segment tree: both operations O(log n).
  Fenwick tree: both O(log n), simpler code, but less general.
```

### Segment Tree

A segment tree is a binary tree where:
- Each **leaf** stores one array element.
- Each **internal node** stores an aggregate (sum, min, max) over its subtree's range.
- A complete tree for `n` elements has height O(log n) and ≤ 4n nodes.

```
  arr = [3, 1, 4, 1, 5]

  Segment tree (sum):
                [14]             ← root: sum of [0..4]
              /       \
          [8]           [6]      ← [0..2]  [3..4]
         /   \         /   \
       [4]   [4]     [1]   [5]   ← [0..1] [2..2] [3..3] [4..4]
       / \
      [3] [1]                    ← [0..0] [1..1]

  Query sum(1, 3):
  → [1..1]=1, [2..2]=4, [3..3]=1  → 6  (only visit O(log n) nodes)

  Update arr[2] = 7:
  → update the leaf [2..2]=7, propagate up: [2..2]=7, [0..2]=4+7=11, [14+3=17]
```

**Build:**
```python
class SegmentTree:
    def __init__(self, nums):
        self.n = len(nums)
        self.tree = [0] * (4 * self.n)
        self._build(nums, 0, 0, self.n - 1)

    def _build(self, nums, node, start, end):
        if start == end:
            self.tree[node] = nums[start]
        else:
            mid = (start + end) // 2
            self._build(nums, 2*node+1, start, mid)
            self._build(nums, 2*node+2, mid+1, end)
            self.tree[node] = self.tree[2*node+1] + self.tree[2*node+2]

    def update(self, idx, val, node=0, start=None, end=None):
        if start is None: start, end = 0, self.n - 1
        if start == end:
            self.tree[node] = val
        else:
            mid = (start + end) // 2
            if idx <= mid:
                self.update(idx, val, 2*node+1, start, mid)
            else:
                self.update(idx, val, 2*node+2, mid+1, end)
            self.tree[node] = self.tree[2*node+1] + self.tree[2*node+2]

    def query(self, l, r, node=0, start=None, end=None):
        if start is None: start, end = 0, self.n - 1
        if r < start or end < l:    # completely outside
            return 0
        if l <= start and end <= r: # completely inside
            return self.tree[node]
        mid = (start + end) // 2    # partially inside — recurse both sides
        return (self.query(l, r, 2*node+1, start, mid) +
                self.query(l, r, 2*node+2, mid+1, end))
```

**Complexity:** O(n) build, O(log n) update, O(log n) query. Space: O(n).

**To support min/max instead of sum:** change the `+` in `_build` and `update` to `min`/`max`, and change the identity return in `query` from 0 to `float('inf')` / `float('-inf')`.

### Fenwick Tree (Binary Indexed Tree / BIT)

A Fenwick tree stores a compressed representation of prefix sums that allows O(log n) updates. It's harder to derive from first principles but the code is tiny:

```
  The key trick: index i is "responsible for" a range whose length
  is determined by the lowest set bit of i.

  i = 6 = 0b0110  →  lowest bit = 0b0010 = 2  →  responsible for 2 elements
  i = 8 = 0b1000  →  lowest bit = 0b1000 = 8  →  responsible for 8 elements

  Update at index i: propagate up by adding the lowest set bit.
  Prefix query up to i: sum by subtracting the lowest set bit.
```

```python
class FenwickTree:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)   # 1-indexed

    def update(self, i, delta):     # add delta to position i (1-indexed)
        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)           # move to next responsible node

    def prefix_sum(self, i):        # sum of [1..i]
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)           # move to parent
        return s

    def range_sum(self, l, r):      # sum of [l..r] (1-indexed)
        return self.prefix_sum(r) - self.prefix_sum(l - 1)

    def build(self, nums):          # O(n log n) build from list (1-indexed input)
        for i, v in enumerate(nums, 1):
            self.update(i, v)
```

**Complexity:** O(n log n) build, O(log n) update, O(log n) prefix query. Space: O(n).

## Segment Tree vs Fenwick Tree

| | Segment Tree | Fenwick Tree |
|---|---|---|
| Code complexity | ~40 lines | ~15 lines |
| Range query | Any aggregate (sum, min, max) | Sum only (or XOR) |
| Point update | ✓ | ✓ |
| Range update | ✓ (with lazy propagation) | ✓ (with difference array trick) |
| Flexibility | Higher | Lower |

**Rule of thumb:** reach for Fenwick first (simpler) when you only need range sums. Use segment tree when you need min/max queries or range updates.

## Worked Trace — Count of Smaller Numbers After Self

A classic application: given `nums`, for each element count how many elements to its *right* are smaller.

```
  nums = [5, 2, 6, 1]
  answer = [2, 1, 1, 0]

  Approach: scan right to left; use a Fenwick tree over the value space.
  1. Coordinate-compress values to [1..n].
  2. For each element (right to left): query prefix_sum(val-1) = count of
     smaller values already inserted. Then update(val, 1).

  Values: 5→3, 2→2, 6→4, 1→1  (rank after sorting: [1,2,5,6] → [1,2,3,4])

  Process 1 (rank 1): query(0)=0, insert rank 1.  answer[3]=0
  Process 6 (rank 4): query(3)=1, insert rank 4.  answer[2]=1
  Process 2 (rank 2): query(1)=1, insert rank 2.  answer[1]=1
  Process 5 (rank 3): query(2)=2, insert rank 3.  answer[0]=2
```

## Recognition Signals

| Problem signal | Tool |
|----------------|------|
| Range sum/min/max, no updates | Prefix sum (01b) |
| Range sum, with point updates | Fenwick tree |
| Range min/max, with point updates | Segment tree |
| "Count elements in range [l, r] smaller than x" | Fenwick + coordinate compression |
| Range updates + range queries | Segment tree with lazy propagation |

## Practice

| # | Difficulty | Problem |
|---|------------|---------|
| 307 | Medium | [Range Sum Query — Mutable](https://leetcode.com/problems/range-sum-query-mutable/) |
| 315 | Hard | [Count of Smaller Numbers After Self](https://leetcode.com/problems/count-of-smaller-numbers-after-self/) |
| 493 | Hard | [Reverse Pairs](https://leetcode.com/problems/reverse-pairs/) |
| 327 | Hard | [Count of Range Sum](https://leetcode.com/problems/count-of-range-sum/) |

Start with 307 (the direct "update + query" problem that forces you off prefix sums), then 315.

## Check Yourself

- [ ] I can explain why prefix sums fail when the array changes, and why a segment tree fixes it.
- [ ] I can write the Fenwick tree `update` and `prefix_sum` methods from memory, including the `i & (-i)` trick.
- [ ] I can build a segment tree for range sum, and modify it for range min/max.
- [ ] I know when to use Fenwick vs segment tree.
- [ ] I can solve "Range Sum Query — Mutable" (LC 307) from scratch.

---

[← Prev](19-math-geometry.md) · [🗺 Roadmap](../roadmap.md)
