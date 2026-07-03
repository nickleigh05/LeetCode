# int / float Basics

```python
a = 5          # int, arbitrary precision (no overflow in Python)
b = 5.0        # float, 64-bit double — has precision limits
c = 5 / 2      # 2.5, "true division" always returns float
d = 5 // 2     # 2, floor division
```

Python integers grow as large as memory allows — there's no `int` overflow like in C/Java. Floats are IEEE-754 doubles, so they carry the usual rounding quirks.

**Related:** [type-conversion](type-conversion.md) · [integer-division-modulo](integer-division-modulo.md) · [float-precision-notes](float-precision-notes.md)
