# Tuple Basics

```python
point = (3, 4)
point[0]           # 3
x, y = point        # unpacking — see tuple-unpacking.md
point[0] = 99        # TypeError — tuples are immutable
```

A `tuple` is like a list but **immutable** — once created, it can't be resized or have elements reassigned. That immutability makes tuples hashable (usable as dict keys / set elements) as long as everything inside them is also hashable, which lists are not.

**Related:** [tuple-unpacking](tuple-unpacking.md) · [list-basics](list-basics.md) · [dict-basics](dict-basics.md)
