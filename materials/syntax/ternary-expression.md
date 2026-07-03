# Ternary (Conditional) Expression

```python
x = 5
label = "big" if x > 3 else "small"    # "big"

result = a if condition else b
```

A one-line `if/else` that evaluates to a value, rather than executing a statement branch. Reach for it when both branches just produce a value to assign or return; fall back to a full `if/else` block once either branch needs more than one line.

**Related:** [if-return](if-return.md) · [elif-else](elif-else.md)
