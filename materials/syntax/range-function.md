# `range()`

```python
range(5)          # 0, 1, 2, 3, 4
range(2, 5)        # 2, 3, 4
range(0, 10, 2)     # 0, 2, 4, 6, 8 — step of 2
range(5, 0, -1)      # 5, 4, 3, 2, 1 — counting down
```

Produces a lazy sequence of integers — `stop` is always excluded, matching slice semantics. Doesn't build a full list in memory; values are generated one at a time as you iterate, so `range(10**9)` costs almost nothing until you loop over it.

**Related:** [for-loop](for-loop.md) · [list-slicing](list-slicing.md)
