# Sparse Table

```python
import math

# build: st[k][i] = min of the 2^k elements starting at i
K = max(1, math.floor(math.log2(len(a))) + 1)
st = [a[:]] + [[0] * len(a) for _ in range(K - 1)]
for k in range(1, K):
    for i in range(len(a) - (1 << k) + 1):
        st[k][i] = min(st[k-1][i], st[k-1][i + (1 << (k-1))])

def query(l, r):                     # min of a[l..r] inclusive, O(1)
    k = (r - l + 1).bit_length() - 1
    return min(st[k][l], st[k][r - (1 << k) + 1])
```

Precompute answers for every power-of-two-length window; then any range `[l, r]` is covered by **two overlapping** power-of-two windows, and for *idempotent* operations (min, max, gcd — where counting an element twice is harmless) that overlap costs nothing. Result: O(1) range-min queries after O(n log n) build — faster querying than a [segment tree](segment-tree.md). The trade: the array must be **static**; one update invalidates the table. Sum doesn't work with the two-window trick (overlap double-counts) — that's [prefix sums](../learning/01b-prefix-sums.md)' job anyway.

**Complexity:** build O(n log n) time/space · query O(1) · updates not supported.

**Related:** [segment-tree](segment-tree.md) · [fenwick-tree](fenwick-tree.md) · [Prefix Sums lesson](../learning/01b-prefix-sums.md) · [bitwise-operators (syntax)](../syntax/bitwise-operators.md)
