# Lambda Functions

```python
square = lambda x: x * x
square(5)                      # 25

sorted(words, key=lambda w: len(w))   # sort by length, no named function needed
```

A `lambda` is an anonymous, single-expression function — no `def`, no name, no `return` keyword (the expression's value is returned automatically). Most common as an inline `key=` for `sorted()`/`sort()`/`min()`/`max()` when writing a full function would be overkill.

**Related:** [sorting-key](sorting-key.md) · [function-basics](function-basics.md) · [map-filter](map-filter.md)
