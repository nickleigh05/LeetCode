# Dict Insertion Order

```python
d = {}
d["z"] = 1
d["a"] = 2
list(d.keys())     # ['z', 'a'] — insertion order preserved, not sorted
```

Since Python 3.7, regular `dict` guarantees it preserves insertion order when iterated — you no longer need `collections.OrderedDict` just for ordering (it still exists for its extra move-to-end/reorder methods, but isn't required for basic order preservation).

**Related:** [dict-basics](dict-basics.md)
