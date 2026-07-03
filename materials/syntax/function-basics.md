# Function Basics (`def` / `return`)

```python
def add(a, b):
    return a + b

result = add(2, 3)   # 5
```

`def` creates a reusable named block. `return` sends a value back to the caller and exits immediately; a function with no `return` implicitly returns `None`. Parameters are local names bound to whatever's passed in at call time.

**Related:** [default-arguments](default-arguments.md) · [args-kwargs](args-kwargs.md) · [type-hints](type-hints.md) · [if-return](if-return.md)
