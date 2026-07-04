# any() & all()

```python
any(x > 10 for x in nums)      # True if AT LEAST ONE passes (a chain of `or`)
all(x > 0 for x in nums)       # True if EVERY one passes    (a chain of `and`)

all(a <= b for a, b in zip(nums, nums[1:]))   # "is the list sorted?"
any(v == target for row in grid for v in row) # search a 2-D grid

any([]) # False    all([]) # True   ← empty-input conventions worth memorizing
```

One-line existence and for-all checks over a [generator expression](generator-expressions.md) — the Pythonic replacement for a flag-variable loop. Both **short-circuit**: `any` stops at the first True, `all` at the first False, so put the cheap/likely-deciding condition first. The empty cases follow logic-class convention ("vacuously true"): no elements means `all` has nothing to fail and `any` has nothing to succeed.

**Related:** [generator-expressions](generator-expressions.md) · [logical-operators](logical-operators.md) · [truthy-falsy-values](truthy-falsy-values.md) · [zip-function](zip-function.md)
