# Stack

```python
stack = []
stack.append(1)     # push, O(1)
stack.append(2)
stack.pop()           # 2 — pop, O(1), LIFO: last in, first out
```

A LIFO (last-in-first-out) structure — the most recently added element is always the first one removed. A plain Python `list` used with only `.append()`/`.pop()` (both from the end) *is* a stack: both operations are O(1) since nothing shifts.

Reach for a stack whenever you need "undo the most recent thing" behavior: matching parentheses, tracking the call chain in [recursion](../syntax/recursion-basics.md), or a monotonic stack for next-greater-element style problems.

**Complexity:** push/pop/peek O(1).

**Related:** [list-methods (syntax)](../syntax/list-methods.md) · [queue](queue.md) · [recursion-basics (syntax)](../syntax/recursion-basics.md)
