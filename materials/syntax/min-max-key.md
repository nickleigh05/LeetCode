# min / max / sum (and key=)

```python
min(3, 7)                     # two+ args directly
max(nums)                     # or one iterable
sum(nums)                     # add everything (numbers only — not strings)
sum(nums, 10)                 # optional starting value → 10 + total

max(words, key=len)                    # longest word — compare BY something
min(points, key=lambda p: p[0]**2 + p[1]**2)   # closest to origin
max(counts, key=counts.get)            # dict key with the biggest value ★

max(nums, default=0)          # empty-safe: default instead of ValueError
best = float('-inf')          # running max: start below everything
```

The three workhorse reducers, each a full O(n) scan. `key=` makes them compare elements by a computed property while **returning the original element** (not the key value) — `max(counts, key=counts.get)` is the one-liner for "most frequent element." On ties, the *first* winner is returned. `min`/`max` on an empty iterable raise `ValueError` — hence `default=`, or seed running extremes with [float('-inf')](float-inf.md).

**Related:** [sorting-key](sorting-key.md) · [lambda-functions](lambda-functions.md) · [float-inf](float-inf.md) · [python-operation-costs (guides)](../guides/python-operation-costs.md)
