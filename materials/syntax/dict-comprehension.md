# Dict Comprehension

```python
squares = {x: x * x for x in range(5)}          # {0:0, 1:1, 2:4, 3:9, 4:16}
counts = {word: len(word) for word in words}
inverted = {v: k for k, v in d.items()}           # swap keys/values
```

Same idea as a list comprehension, but builds a dict: `{key_expr: value_expr for item in iterable}`. Common for building a lookup table from a list in one line instead of a `for` loop with manual `d[key] = value`.

**Related:** [dict-basics](dict-basics.md) · [list-comprehension](list-comprehension.md)
