# Integer Division & Modulo

```python
7 // 2      # 3   — floor division
7 % 2        # 1   — remainder
-7 // 2       # -4  — floors toward negative infinity, not toward zero
-7 % 2         # 1   — Python's % always matches the sign of the divisor
```

`//` rounds *down* (toward negative infinity), not toward zero — this differs from languages like C/Java where integer division truncates toward zero. This matters for negative numbers: `-7 // 2` is `-4` in Python, not `-3`.

**Related:** [arithmetic-operators](arithmetic-operators.md) · [int-float-basics](int-float-basics.md)
