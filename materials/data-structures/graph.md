# Graph

```python
# Adjacency list — the standard interview representation
graph = {
    "A": ["B", "C"],
    "B": ["A", "D"],
    "C": ["A"],
    "D": ["B"],
}
```

A set of nodes connected by edges — more general than a [tree](binary-tree.md) (no single root, cycles allowed, a node can have any number of neighbors). Represented as an **adjacency list** (dict/list mapping each node to its neighbors — compact when edges are sparse, the interview default) or an **adjacency matrix** (2-D grid of connections — simpler for dense graphs, O(V²) space).

A 2-D grid (like an image or maze) is itself a graph in disguise — each cell is a node, its up/down/left/right neighbors are edges — which is why grid problems use the exact same [bfs](../algorithms/bfs.md)/[dfs](../algorithms/dfs.md) toolkit as explicit graphs.

**Complexity:** adjacency list space O(V + E) · adjacency matrix space O(V²).

**Related:** [bfs](../algorithms/bfs.md) · [dfs](../algorithms/dfs.md) · [union-find](union-find.md) · [dijkstra](../algorithms/dijkstra.md) · [dict-basics (syntax)](../syntax/dict-basics.md)
