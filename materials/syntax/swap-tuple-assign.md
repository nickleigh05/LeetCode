# Swap via Tuple Assignment

```python
a, b = 1, 2
a, b = b, a          # a=2, b=1 — no temp variable needed
nums[i], nums[j] = nums[j], nums[i]   # same trick for list elements
```

The right side `b, a` builds a temporary tuple `(b, a)` *before* any assignment happens, then unpacks it into `a, b` — that's why both values swap correctly instead of the classic "first assignment overwrites the value the second one needed" bug.

**Related:** [tuple-basics](tuple-basics.md) · [tuple-unpacking](tuple-unpacking.md) · [swap-without-temp](swap-without-temp.md)
