# Walrus Operator (`:=`)

```python
if (n := len(nums)) > 10:
    print(f"list has {n} items")   # n usable here too

while (chunk := read_next()) is not None:
    process(chunk)
```

`:=` assigns a value **and** produces it as an expression result in one step, avoiding a separate assignment line before a condition. Useful in `while` loops that repeatedly compute a value to test, or in comprehensions that reuse a computed value.

**Related:** [if-return](if-return.md) · [while-loop](while-loop.md)
