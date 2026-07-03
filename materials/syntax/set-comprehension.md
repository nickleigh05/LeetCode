# Set Comprehension

```python
unique_lengths = {len(w) for w in words}     # dedupes automatically
evens = {x for x in range(10) if x % 2 == 0}
```

Same syntax as a list comprehension but with `{}` instead of `[]` — builds a set, so duplicate results collapse automatically. Useful when you want the *distinct* transformed values, not every value.

**Related:** [set-basics](set-basics.md) · [list-comprehension](list-comprehension.md) · [dict-comprehension](dict-comprehension.md)
