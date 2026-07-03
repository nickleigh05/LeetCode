# Union-Find (Disjoint Set Union)

```python
parent = list(range(n))

def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])   # path compression
    return parent[x]

def union(a, b):
    ra, rb = find(a), find(b)
    if ra != rb:
        parent[ra] = rb
```

Tracks a collection of disjoint (non-overlapping) groups and answers "are these two elements in the same group" and "merge these two groups" both in near-O(1) — far faster than re-running a [graph](graph.md) traversal after every merge. `find(x)` walks up to the group's representative "root"; `union(a, b)` links one root to the other. **Path compression** (flattening the chain during `find`) plus **union by rank/size** together give the near-constant amortized time.

Used for connectivity questions under repeated merges: counting connected components, cycle detection while building a graph edge-by-edge, Kruskal's MST.

**Complexity:** find/union O(α(n)) amortized (α = inverse Ackermann, effectively constant) with both optimizations · O(log n) with only one.

**Related:** [graph](graph.md) · [recursion-basics (syntax)](../syntax/recursion-basics.md)
