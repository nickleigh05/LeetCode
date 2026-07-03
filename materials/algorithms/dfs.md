# Depth-First Search (DFS)

```python
def dfs(node, graph, visited):
    if node in visited:
        return
    visited.add(node)
    for neighbor in graph[node]:
        dfs(neighbor, graph, visited)
```

Explores a [graph](../data-structures/graph.md) by diving as deep as possible down one path before backtracking — implemented either with recursion (the call [stack](../data-structures/stack.md) does the bookkeeping implicitly) or an explicit stack. Doesn't guarantee shortest paths like [bfs](bfs.md) does, but is the natural fit for connectivity questions, cycle detection, and any tree/graph problem shaped like "process this node, then recurse into its children."

**Complexity:** O(V + E) time, O(V) space (recursion depth / explicit stack, worst case).

**Related:** [bfs](bfs.md) · [recursion-basics (syntax)](../syntax/recursion-basics.md) · [tree-traversal-orders](tree-traversal-orders.md) · [backtracking](backtracking.md)
