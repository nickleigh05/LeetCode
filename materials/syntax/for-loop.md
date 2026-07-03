# `for` Loop

```python
for num in nums:
    print(num)
```

Iterates once per element, binding it to `num` each pass — no manual index bookkeeping. Under the hood Python calls `iter(nums)` and repeatedly `next()`s until exhausted. Works on any iterable: lists, strings, dicts (iterates keys), sets, ranges.

**Related:** [range-function](range-function.md) · [enumerate](enumerate.md) · [break-continue](break-continue.md) · [while-loop](while-loop.md)
