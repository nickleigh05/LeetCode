# Generator Expressions

```python
squares = (x * x for x in range(1000000))   # note: () not []
sum(x * x for x in range(10))                # 285 — no intermediate list built

any(x > 5 for x in nums)                      # True if any element satisfies
all(x > 0 for x in nums)                       # True if every element satisfies
```

Same syntax as a list comprehension but with `()` — produces values lazily, one at a time, instead of building the whole list in memory upfront. Pairs naturally with `sum()`, `any()`, `all()`, `max()` when you only need to consume the values once and never need the full list.

**Related:** [list-comprehension](list-comprehension.md) · [yield-generators](yield-generators.md)
