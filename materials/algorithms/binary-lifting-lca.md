# Binary Lifting & LCA

```python
LOG = 17                                   # ceil(log2(max n))
up = [[0] * n for _ in range(LOG)]         # up[k][v] = 2^k-th ancestor of v
# build: up[0][v] = parent[v], then up[k][v] = up[k-1][ up[k-1][v] ]

def kth_ancestor(v, k):                    # LC 1483 — jump k steps in O(log k)
    for bit in range(LOG):
        if k >> bit & 1:                   # decompose k into powers of two
            v = up[bit][v]
    return v

# LCA(a, b): lift the deeper node to the same depth, then binary-search upward —
# jump both by 2^k whenever their ancestors still differ; their parents then meet.
```

Precompute every node's 2ᵏ-th ancestor (each row built from the previous: "jump 8 = jump 4, then 4 again"), and any k-step upward jump becomes ~log k table hops — the same power-of-two decomposition as [fast exponentiation](fast-exponentiation.md), applied to trees. Two headline uses: **k-th ancestor queries** (LC 1483, where the naive walk TLEs) and **lowest common ancestor** in O(log n) per query after O(n log n) prep — which in turn unlocks "distance between two tree nodes" via depths. Note the contrast with the [LeetCode LCA problem](../learning/07-trees.md) (LC 236): that's one query, plain DFS wins; binary lifting is for *many* queries on a big static tree — firmly mastery-track/competitive territory.

**Complexity:** build O(n log n) · each ancestor/LCA query O(log n).

**Related:** [fast-exponentiation](fast-exponentiation.md) · [binary-tree (data-structures)](../data-structures/binary-tree.md) · [sparse-table (data-structures)](../data-structures/sparse-table.md) · [bitwise-operators (syntax)](../syntax/bitwise-operators.md)
