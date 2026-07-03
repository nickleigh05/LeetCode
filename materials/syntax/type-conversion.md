# Type Conversion

```python
int("42")        # 42
int(3.9)         # 3 (truncates toward zero, doesn't round)
float("3.14")    # 3.14
str(42)          # "42"
list("abc")      # ['a', 'b', 'c']
```

Conversion functions (`int`, `float`, `str`, `list`, `set`, `tuple`) build a *new* object of that type from the input — they don't mutate anything. `int()` on a float truncates rather than rounds; use `round()` if you need rounding.

**Related:** [int-float-basics](int-float-basics.md) · [string-basics](string-basics.md) · [list-basics](list-basics.md)
