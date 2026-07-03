# Chained Comparisons

```python
0 <= i < len(nums)          # same as: 0 <= i and i < len(nums)
a < b < c                    # same as: a < b and b < c
```

Python lets you chain comparison operators directly, reading naturally like a math inequality — evaluated as if each pair were joined by `and`, short-circuiting the same way. Very common for bounds checks in binary search and array indexing.

**Related:** [comparison-operators](comparison-operators.md) · [logical-operators](logical-operators.md)
