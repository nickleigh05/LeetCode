# `math` Module Basics

```python
import math
math.sqrt(16)         # 4.0
math.floor(3.7)         # 3
math.ceil(3.2)           # 4
math.gcd(12, 18)          # 6
math.inf                  # float('inf') — useful as a starting "worst case" value
math.log2(8)               # 3.0
```

Standard-library math functions beyond the basic operators — `math.inf`/`-math.inf` are the idiomatic way to initialize a running min/max before any real comparisons happen (e.g. `best = math.inf` before a min-tracking loop).

**Related:** [arithmetic-operators](arithmetic-operators.md) · [int-float-basics](int-float-basics.md)
