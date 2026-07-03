# Set Operations

```python
a = {1, 2, 3}
b = {2, 3, 4}
a | b        # union: {1, 2, 3, 4}
a & b        # intersection: {2, 3}
a - b         # difference: {1}
a ^ b          # symmetric difference: {1, 4} — in one but not both
a <= b          # subset check
```

These mirror set theory directly and all run faster than manually looping with membership checks — the interpreter does the hashing work internally. `&` (intersection) is the one that comes up most: "which elements appear in both."

**Related:** [set-basics](set-basics.md) · [membership-operators](membership-operators.md)
