# Breadth-First Search (BFS)

```python
from collections import deque

def bfs(start, graph):
    visited = {start}
    q = deque([start])
    while q:
        node = q.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                q.append(neighbor)
```

Explores a [graph](../data-structures/graph.md) level by level, using a [queue](../data-structures/queue.md) to always process the earliest-discovered node next — this guarantees the *first* time you reach any node is via a shortest path, when all edges have equal weight. Mark nodes visited **at the moment you enqueue them**, not when you dequeue — otherwise the same node can be queued multiple times before it's ever processed.

Reach for BFS specifically when the problem asks for shortest path / minimum steps in an unweighted graph or grid.

**Complexity:** O(V + E) time, O(V) space for the visited set and queue.

**Related:** [dfs](dfs.md) · [graph (data-structures)](../data-structures/graph.md) · [queue (data-structures)](../data-structures/queue.md)
