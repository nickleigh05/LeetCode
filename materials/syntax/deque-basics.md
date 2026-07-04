# collections.deque

```python
from collections import deque

q = deque([1, 2, 3])
q.append(4)         # right end   → deque([1, 2, 3, 4])
q.appendleft(0)     # left end    → deque([0, 1, 2, 3, 4])
q.pop()             # from right  → 4
q.popleft()         # from left   → 0        ← the queue superpower
q[0], q[-1]         # peek both ends, O(1)

window = deque(maxlen=3)   # bonus: fixed size, old items auto-drop off the far end
q2 = deque("abc"); q2.rotate(1)   # deque(['c', 'a', 'b'])
```

The syntax for Python's double-ended queue: O(1) push/pop at **both** ends, where a list's `pop(0)`/`insert(0, …)` are O(n). Use it for every BFS queue (`popleft`), and both ends for the monotonic-deque trick. Full concept page: [deque (data-structures)](../data-structures/deque.md).

**Complexity:** append/pop either end O(1) · index into the middle O(n).

**Related:** [deque (data-structures)](../data-structures/deque.md) · [queue (data-structures)](../data-structures/queue.md) · [from-import](from-import.md) · [bfs (algorithms)](../algorithms/bfs.md)
