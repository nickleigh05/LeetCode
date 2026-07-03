# `elif` / `else`

```python
if n > 0:
    sign = "positive"
elif n < 0:
    sign = "negative"
else:
    sign = "zero"
```

Python checks branches top to bottom and runs the **first** one that's truthy, skipping the rest — `elif` chains are not independent `if`s. `else` catches everything not matched above it.

**Related:** [if-return](if-return.md) · [ternary-expression](ternary-expression.md) · [match-statement](match-statement.md)
