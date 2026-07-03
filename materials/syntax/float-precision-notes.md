# Float Precision Notes

```python
0.1 + 0.2                 # 0.30000000000000004 — not exactly 0.3
0.1 + 0.2 == 0.3            # False!
round(0.1 + 0.2, 2) == 0.3    # True — round before comparing
```

Floats are binary (base-2) approximations of decimal numbers, so many decimal values (like `0.1`) can't be represented exactly — small rounding errors accumulate. Never compare floats with `==` directly; round to a fixed number of decimals first, or compare `abs(a - b) < epsilon`.

**Related:** [int-float-basics](int-float-basics.md) · [comparison-operators](comparison-operators.md)
