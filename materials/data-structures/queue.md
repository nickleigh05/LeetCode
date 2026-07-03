# Queue

```python
from collections import deque
q = deque()
q.append(1)         # enqueue, O(1)
q.append(2)
q.popleft()           # 1 — dequeue, O(1), FIFO: first in, first out
```

A FIFO (first-in-first-out) structure — the earliest-added element is the first one removed. Don't use a plain `list` for this: `list.pop(0)` is O(n) because everything shifts left. `collections.deque` gives O(1) operations on *both* ends, which is why it's the standard choice for queues in Python.

Reach for a queue whenever processing must happen in the order things arrived — most notably [BFS](../algorithms/bfs.md), where the queue holds "discovered but not yet visited" nodes level by level.

**Complexity:** enqueue/dequeue O(1) (with `deque`).

**Related:** [deque](deque.md) · [bfs](../algorithms/bfs.md) · [stack](stack.md)
