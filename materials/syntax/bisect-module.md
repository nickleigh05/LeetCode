# bisect Module

```python
import bisect

a = [10, 20, 20, 30]
bisect.bisect_left(a, 20)    # 1 — first index where 20 could go (before equals)
bisect.bisect_right(a, 20)   # 3 — after equals (alias: bisect.bisect)
bisect.insort(a, 25)         # insert keeping sorted order → [10, 20, 20, 25, 30]

# count of values < x  →  bisect_left(a, x)
# count of values <= x →  bisect_right(a, x)
# does x exist?        →  i = bisect_left(a, x); i < len(a) and a[i] == x
```

Binary search over a **sorted** list, pre-written and bug-free. `bisect_left` vs `bisect_right` only differ when the target already exists: left lands *before* the run of equals, right lands *after*. Both take `lo`/`hi` bounds and a `key=` function. Caveat: the *search* is O(log n) but `insort`'s insertion still shifts elements — O(n) — so repeated insertions want a [sorted-list](../data-structures/sorted-list.md) structure instead.

**Complexity:** bisect O(log n) · insort O(n) per insert.

**Related:** [binary-search (algorithms)](../algorithms/binary-search.md) · [Binary Search lesson](../learning/05-binary-search.md) · [sorting-key](sorting-key.md)
