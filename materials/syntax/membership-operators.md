# Membership Operators (`in` / `not in`)

```python
3 in [1, 2, 3]        # True — O(n) for list
3 in {1, 2, 3}        # True — O(1) avg for set
"a" in "cat"          # True — substring check for strings
3 not in [1, 2]       # True
```

`in` on a `list` scans element by element (O(n)); `in` on a `set`/`dict` hashes the value for O(1) average lookup. This difference is the whole reason hashsets exist — swapping a list for a set turns an O(n²) double loop into O(n).

**Related:** [set-basics](set-basics.md) · [list-basics](list-basics.md) · [dict-basics](dict-basics.md)
