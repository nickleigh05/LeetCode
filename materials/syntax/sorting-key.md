# Sorting with `key=`

```python
nums = [3, 1, 2]
sorted(nums)                          # [1, 2, 3] — new sorted list
nums.sort()                            # sorts nums in place, returns None

words = ["ccc", "a", "bb"]
sorted(words, key=len)                 # ['a', 'bb', 'ccc']
sorted(words, key=lambda w: -len(w))   # descending, longest first
sorted(nums, reverse=True)              # [3, 2, 1]
```

`sorted()` returns a new list and works on any iterable; `.sort()` only exists on lists and sorts in place. `key=` takes a function applied to each element to determine sort order — pair it with a `lambda` for one-off keys.

**Related:** [lambda-functions](lambda-functions.md) · [list-methods](list-methods.md)
