# Dict Methods

```python
d = {"a": 1}
d.get("a")            # 1
d.get("z")             # None — no KeyError
d.get("z", 0)           # 0 — custom default
d.keys()                # view of keys
d.values()               # view of values
d.items()                 # view of (key, value) pairs
d.setdefault("z", [])     # returns d["z"], creating it with [] if missing
d.pop("a")                 # removes "a", returns its value
```

`.get()` is the safe alternative to `d[key]` when the key might not exist. `.setdefault()` is useful for "insert if missing, then use it" in one call — e.g. `d.setdefault(char, []).append(i)` for grouping. `.items()` is what you iterate with `for k, v in d.items()`.

**Related:** [dict-basics](dict-basics.md) · [defaultdict](defaultdict.md) · [tuple-unpacking](tuple-unpacking.md)
