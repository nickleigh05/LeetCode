# `zip()`

```python
names = ["a", "b", "c"]
ages = [1, 2, 3]
for name, age in zip(names, ages):
    print(name, age)          # a 1 / b 2 / c 3

list(zip(names, ages))         # [('a', 1), ('b', 2), ('c', 3)]
```

Pairs up elements from multiple iterables index-by-index, stopping at the shortest one. Used whenever you need to walk two lists in lockstep instead of indexing both manually.

**Related:** [for-loop](for-loop.md) · [tuple-unpacking](tuple-unpacking.md)
