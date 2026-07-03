# `enumerate()`

```python
nums = ["a", "b", "c"]
for i, val in enumerate(nums):
    print(i, val)          # 0 a / 1 b / 2 c

for i, val in enumerate(nums, start=1):   # start counting from 1
    print(i, val)
```

Wraps an iterable so each pass yields `(index, value)` instead of just `value` — avoids manually tracking `i` with a separate counter or `range(len(nums))`.

**Related:** [for-loop](for-loop.md) · [tuple-unpacking](tuple-unpacking.md) · [range-function](range-function.md)
