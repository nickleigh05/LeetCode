# List Comprehension

```python
squares = [x * x for x in range(5)]              # [0, 1, 4, 9, 16]
evens = [x for x in range(10) if x % 2 == 0]      # [0, 2, 4, 6, 8]
pairs = [(x, y) for x in range(2) for y in range(2)]  # nested loops
```

A compact way to build a list by looping and (optionally) filtering in a single expression: `[expression for item in iterable if condition]`. Equivalent to a `for` loop that appends to a list, just denser — reach for it when the loop body is a single expression.

**Related:** [for-loop](for-loop.md) · [list-basics](list-basics.md) · [dict-comprehension](dict-comprehension.md) · [generator-expressions](generator-expressions.md)
