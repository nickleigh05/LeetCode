# Deque (Double-Ended Queue)

```python
from collections import deque
dq = deque([1, 2, 3])
dq.append(4)          # add to right, O(1)
dq.appendleft(0)        # add to left, O(1)
dq.pop()                  # remove from right, O(1)
dq.popleft()                # remove from left, O(1)
```

A `deque` supports O(1) push/pop at *both* ends, unlike a `list` (which is O(1) only at the end, O(n) at the front). It doubles as a [stack](stack.md) (use one end) or a [queue](queue.md) (use both ends) — and is also the backbone of the sliding-window-maximum monotonic deque technique.

**Complexity:** append/pop/appendleft/popleft O(1) · arbitrary index access O(n) (unlike a list).

**Related:** [queue](queue.md) · [stack](stack.md) · [from-import (syntax)](../syntax/from-import.md)
