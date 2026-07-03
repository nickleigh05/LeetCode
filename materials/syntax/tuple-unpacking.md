# Tuple Unpacking

```python
point = (3, 4)
x, y = point                  # x=3, y=4

for key, value in d.items():  # each item is a (key, value) tuple, unpacked per iteration
    print(key, value)

first, *rest = [1, 2, 3, 4]   # first=1, rest=[2, 3, 4] — see unpacking-star-expr.md
```

Assigns each element of a tuple (or any fixed-size iterable) to its own name in one line — the number of names on the left must match the number of values on the right (unless using `*` to catch the remainder).

**Related:** [tuple-basics](tuple-basics.md) · [unpacking-star-expr](unpacking-star-expr.md) · [swap-tuple-assign](swap-tuple-assign.md)
