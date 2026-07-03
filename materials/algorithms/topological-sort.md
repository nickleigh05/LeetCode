# Topological Sort

```python
from collections import deque

def topo_sort(n, edges):            # edges: a -> b means a must come before b
    graph = {i: [] for i in range(n)}
    indegree = [0] * n
    for a, b in edges:
        graph[a].append(b)
        indegree[b] += 1

    q = deque([i for i in range(n) if indegree[i] == 0])
    order = []
    while q:
        node = q.popleft()
        order.append(node)
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                q.append(neighbor)

    return order if len(order) == n else []   # empty = cycle detected, no valid order
```

Orders the nodes of a **DAG** (directed acyclic graph) so every edge `a -> b` places `a` before `b` — the classic use case is "course scheduling," where an edge means "prerequisite before course." This version (Kahn's algorithm) repeatedly peels off nodes with no remaining incoming edges, using a [queue](../data-structures/queue.md); if any nodes are left un-orderable, the graph has a cycle and no valid ordering exists.

**Complexity:** O(V + E) time.

**Related:** [bfs](bfs.md) · [graph (data-structures)](../data-structures/graph.md) · [queue (data-structures)](../data-structures/queue.md)
