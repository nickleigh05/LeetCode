# Bitwise Operators

```python
5 & 3       # 1   — AND, bit set only where both have 1
5 | 3        # 7   — OR, bit set where either has 1
5 ^ 3         # 6   — XOR, bit set where exactly one has 1
~5             # -6  — NOT, flips all bits (two's complement)
5 << 1          # 10  — left shift, multiplies by 2
5 >> 1           # 2   — right shift, divides by 2 (floor)
```

Operates on the binary representation of integers directly. XOR (`^`) is the standout for interviews: XOR-ing a number with itself gives 0, and XOR-ing with 0 gives the number back — the basis for "find the single non-duplicate" tricks.

**Related:** [arithmetic-operators](arithmetic-operators.md)
