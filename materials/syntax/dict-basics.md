# Dict Basics

```python
d = {}
d["a"] = 1              # insert/overwrite, O(1) avg
d["a"]                   # 1 — KeyError if "a" missing
"a" in d                 # True — O(1) avg, checks keys
len(d)                    # 1
del d["a"]                # remove key
```

A `dict` maps keys to values with O(1) average lookup/insert/delete, using a hash table under the hood. Keys must be hashable (immutable types: strings, numbers, tuples-of-hashables) — lists can't be keys. This O(1) lookup is the single biggest reason hashmaps beat nested loops.

**Related:** [dict-methods](dict-methods.md) · [set-basics](set-basics.md) · [dict-comprehension](dict-comprehension.md) · [defaultdict](defaultdict.md)
