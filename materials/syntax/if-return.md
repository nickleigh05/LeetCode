# `if` / `return`

```python
def is_positive(n):
    if n > 0:
        return True
    return False
```

`if` runs its block only when the condition is truthy. `return` immediately exits the function with a value — code after it in the same call never runs. Returning early on a condition (a "guard clause") avoids nesting the rest of the function inside an `else`.

**Related:** [elif-else](elif-else.md) · [ternary-expression](ternary-expression.md) · [function-basics](function-basics.md)
