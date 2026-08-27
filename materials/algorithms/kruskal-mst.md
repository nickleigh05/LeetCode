# Kruskal's Algorithm (Minimum Spanning Tree)

```python
def kruskal(n, edges):                     # edges: [(w, u, v), ...]
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]  # path compression
            x = parent[x]
        return x

    total = used = 0
    for w, u, v in sorted(edges):          # cheapest edges first
        ru, rv = find(u), find(v)
        if ru != rv:                       # different components → no cycle
            parent[ru] = rv
            total += w
            used += 1
            if used == n - 1:              # tree complete
                break
    return total
```

The other MST classic: sort all edges by weight and greedily take each one **unless it closes a cycle** — where "would it close a cycle?" is exactly one [union-find](../data-structures/union-find.md) query. Same cut-property correctness as [Prim](prim-mst.md); different personality: Kruskal is edge-centric (natural when the input *is* an edge list, and for "which edges are critical?" analysis like LC 1489), Prim is node-centric. The greedy + union-find combination also solves non-MST problems shaped like "process cheapest first, merge components" — a pattern worth recognizing on its own.

**Complexity:** O(E log E) for the sort — the union-find work is effectively free after it · O(V) space.

**Related:** [prim-mst](prim-mst.md) · [union-find (data-structures)](../data-structures/union-find.md) · [Union-Find lesson](../learning/12-union-find.md) · [sorting-key (syntax)](../syntax/sorting-key.md)
