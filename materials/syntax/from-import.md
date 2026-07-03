# `from ... import ...`

```python
from collections import deque, Counter, defaultdict
from heapq import heappush, heappop

q = deque()
heappush(heap, 5)
```

Pulls specific names directly out of a module into the current namespace, so you call `deque()` instead of `collections.deque()`. Preferred in interview code for brevity when you only need a couple of names from a module.

**Related:** [import-basics](import-basics.md)
