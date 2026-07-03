# Logical Operators

```python
True and False   # False
True or False    # True
not True          # False
```

`and`/`or` **short-circuit**: `a and b` returns `a` immediately if `a` is falsy (never evaluates `b`); `a or b` returns `a` immediately if `a` is truthy. This is why `x and x.value` is a safe pattern when `x` might be `None`.

**Related:** [boolean-basics](boolean-basics.md) · [truthy-falsy-values](truthy-falsy-values.md) · [comparison-operators](comparison-operators.md)
