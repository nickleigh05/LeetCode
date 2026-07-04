# Tarjan's Algorithm (SCCs & Bridges)

```python
def find_bridges(n, adj):                  # LC 1192, Critical Connections
    disc = [-1] * n                        # discovery time of each node
    low = [0] * n                          # lowest disc reachable from subtree
    bridges, timer = [], 0

    def dfs(u, parent):
        nonlocal timer
        disc[u] = low[u] = timer; timer += 1
        for v in adj[u]:
            if v == parent:
                continue
            if disc[v] != -1:                   # back-edge to an ancestor
                low[u] = min(low[u], disc[v])
            else:
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]:            # subtree can't climb past u
                    bridges.append((u, v))      # → (u,v) is a bridge
    dfs(0, -1)
    return bridges
```

One [DFS](dfs.md) with two timestamps per node — `disc` (when first visited) and `low` (earliest ancestor its subtree can reach via any back-edge) — answers deep structural questions: **bridges** (edges whose removal disconnects the graph — `low[v] > disc[u]`), **articulation points** (same idea on nodes), and **strongly connected components** in directed graphs (the full Tarjan: a stack + "root of SCC when `low[u] == disc[u]`"). The mental model: a back-edge is an escape ladder; a subtree with no ladder climbing above its entry edge is hanging by that edge alone. Mastery-tier — LC 1192 is the one mainstream appearance — but the `disc`/`low` trick is the gateway to a whole family of competitive-programming graph tools (2-SAT, condensation graphs).

**Complexity:** O(V + E) time · O(V) space (recursion — mind the [depth limit](../syntax/recursion-limit.md)).

**Related:** [dfs](dfs.md) · [topological-sort](topological-sort.md) · [union-find (data-structures)](../data-structures/union-find.md) · [Advanced Graphs lesson](../learning/13-advanced-graphs.md)
