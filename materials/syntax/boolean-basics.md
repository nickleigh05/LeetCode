# bool Basics

```python
t = True
f = False
bool(1)     # True
bool(0)     # False
bool("")    # False
bool("x")   # True
```

`bool` is a subclass of `int` — `True == 1` and `False == 0` both evaluate to `True`. This is why `sum(x > 0 for x in nums)` works: each `True` counts as 1.

**Related:** [truthy-falsy-values](truthy-falsy-values.md) · [comparison-operators](comparison-operators.md) · [logical-operators](logical-operators.md)
