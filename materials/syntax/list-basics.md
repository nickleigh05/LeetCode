# List Basics

```python
nums = [1, 2, 3]
nums[0]           # 1
nums[-1]          # 3 — negative index counts from the end
len(nums)          # 3
nums[0] = 99       # mutable — in-place assignment works
```

A `list` is an ordered, mutable, index-accessible sequence — unlike strings/tuples, you can change elements in place. Index access is O(1); searching for a value (`in`, `.index()`) is O(n).

**Related:** [list-slicing](list-slicing.md) · [list-methods](list-methods.md) · [nested-lists](nested-lists.md)
