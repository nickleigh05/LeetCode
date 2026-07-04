# Iterators & Iterables

```python
it = iter([10, 20, 30])     # iterable → iterator (a one-way cursor)
next(it)                    # 10
next(it)                    # 20
next(it, None)              # 30, then None forever (default instead of StopIteration)

first = next(iter(my_set))  # ★ grab "any one element" from a set/dict, O(1)

# what a for-loop actually does:
# it = iter(thing); loop next(it) until StopIteration
```

An **iterable** is anything a [for loop](for-loop.md) can walk (lists, strings, dicts, sets, [generators](yield-generators.md), files). An **iterator** is the cursor doing the walking: `next()` pulls one item, and it's exhausted after one pass — which explains the classic gotchas: a generator you loop twice is silently empty the second time, and [`zip`](zip-function.md)/[`map`](map-filter.md) results vanish after first use (wrap in `list()` to keep them). Iterators are *lazy* — values are produced on demand, so `iter(huge_range)` costs nothing until you pull.

**Related:** [for-loop](for-loop.md) · [yield-generators](yield-generators.md) · [generator-expressions](generator-expressions.md) · [zip-function](zip-function.md)
