# `map()` / `filter()`

```python
nums = [1, 2, 3, 4]
list(map(str, nums))                    # ['1', '2', '3', '4']
list(map(lambda x: x * 2, nums))         # [2, 4, 6, 8]
list(filter(lambda x: x % 2 == 0, nums))  # [2, 4]
```

`map(func, iterable)` applies `func` to every element, lazily; `filter(func, iterable)` keeps only elements where `func` returns truthy. Both return lazy iterators — wrap in `list()` to see all results at once. A list/dict comprehension usually reads more clearly for the same job.

**Related:** [lambda-functions](lambda-functions.md) · [list-comprehension](list-comprehension.md) · [generator-expressions](generator-expressions.md)
