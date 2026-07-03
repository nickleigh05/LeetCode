# Segment Tree

```python
# Conceptually: a binary tree over array indices,
# each node summarizes a range [l, r] of the underlying array.
#           [0,3]
#          /      \
#      [0,1]      [2,3]
#      /   \       /   \
#   [0,0] [1,1] [2,2] [3,3]
```

Built over an array to answer range queries (sum/min/max over `[l, r]`) **and** support point updates, both in O(log n) — a plain prefix-sum array answers range-sum queries in O(1) but costs O(n) to update after any single element changes. A segment tree trades that O(1) query for O(log n) query in exchange for O(log n) updates, which wins whenever the underlying array actually changes.

Each internal node stores the combined result (sum/min/max) of its range; a query or update touches only the O(log n) nodes along the relevant root-to-leaf paths.

**Complexity:** build O(n) · range query O(log n) · point update O(log n).

**Related:** [array](array.md) · [binary-tree](binary-tree.md)
