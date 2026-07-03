# Set Basics

```python
s = set()
s.add(5)              # O(1) avg
5 in s                 # True — O(1) avg membership check
s.discard(5)            # remove if present, no error if missing
s.remove(5)              # remove, raises KeyError if missing
len(s)                    # size
```

A `set` is a hashmap that only stores keys, no values — unordered, no duplicates, O(1) average membership check. Whenever a problem needs "have I seen this before" without caring about a value, reach for a set instead of a dict.

**Related:** [dict-basics](dict-basics.md) · [set-operations](set-operations.md) · [set-comprehension](set-comprehension.md) · [membership-operators](membership-operators.md)
