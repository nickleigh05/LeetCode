# Swap Without a Temp Variable

```python
a, b = b, a                            # variables
nums[i], nums[j] = nums[j], nums[i]     # list elements — the standard two-pointer swap
```

Python evaluates the entire right-hand side tuple `(b, a)` before assigning anything, so both values swap correctly in one line — no `temp = a; a = b; b = temp` needed. This is the idiom you'll type constantly in two-pointer and in-place array problems.

**Related:** [swap-tuple-assign](swap-tuple-assign.md) · [tuple-unpacking](tuple-unpacking.md)
