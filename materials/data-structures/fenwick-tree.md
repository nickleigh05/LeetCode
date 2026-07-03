# Fenwick Tree (Binary Indexed Tree)

```python
tree = [0] * (n + 1)

def update(i, delta):
    while i <= n:
        tree[i] += delta
        i += i & (-i)         # move to next responsible index

def prefix_sum(i):
    total = 0
    while i > 0:
        total += tree[i]
        i -= i & (-i)          # move to parent range
    return total
```

A more compact alternative to a [segment tree](segment-tree.md), specialized for prefix-sum-style range queries (sum of a range = difference of two prefix sums) and point updates — same O(log n) for both operations, but implemented as a single array with bit-trick index jumps (`i & (-i)` isolates the lowest set bit) instead of an explicit tree structure.

Reach for a Fenwick tree when the query is specifically "sum up to index i" or "sum of range [l, r]" with updates in between; reach for a full segment tree when you need min/max or more general range operations.

**Complexity:** build O(n) · update O(log n) · prefix-sum query O(log n).

**Related:** [segment-tree](segment-tree.md) · [bitwise-operators (syntax)](../syntax/bitwise-operators.md) · [array](array.md)
