# List Slicing

```python
nums = [0, 1, 2, 3, 4, 5]
nums[1:4]      # [1, 2, 3]  — start:stop, stop excluded
nums[:3]        # [0, 1, 2]
nums[3:]        # [3, 4, 5]
nums[::2]       # [0, 2, 4]  — every other element
nums[::-1]      # [5, 4, 3, 2, 1, 0]  — reversed copy
```

A slice always returns a **new** list — the original is untouched. Slicing never raises an `IndexError` even with out-of-bounds indices; it just clamps to what exists. Slicing is O(k) where k is the slice length, since it copies.

**Related:** [list-basics](list-basics.md) · [string-join-slice](string-join-slice.md)
