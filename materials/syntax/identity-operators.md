# Identity Operators (`is` / `is not`)

```python
a = [1, 2]
b = [1, 2]
a == b     # True  — same value
a is b     # False — different objects in memory
a is a     # True

x = None
x is None      # True — the correct way to check for None
```

`is` checks whether two names point to the *same object*, not whether they hold equal values. Always use `is`/`is not` for `None` checks; use `==` for value comparisons.

**Related:** [none-type](none-type.md) · [comparison-operators](comparison-operators.md)
