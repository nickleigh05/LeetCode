# Multiple Return Values

```python
def min_max(nums):
    return min(nums), max(nums)     # actually returns one tuple: (min, max)

low, high = min_max([3, 1, 4])       # unpacked immediately
```

Python functions only ever return one object — `return a, b` packs `a` and `b` into a tuple behind the scenes. The caller then unpacks that tuple into separate names in one line, which is why it *feels* like returning two values.

**Related:** [tuple-basics](tuple-basics.md) · [tuple-unpacking](tuple-unpacking.md) · [function-basics](function-basics.md)
