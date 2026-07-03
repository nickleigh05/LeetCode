# Fast Exponentiation (Binary Exponentiation)

```python
def power(base, exp):
    result = 1
    while exp > 0:
        if exp % 2 == 1:          # current bit is 1 — fold base into result
            result *= base
        base *= base                # square the base for the next bit
        exp //= 2
    return result
```

Computes `base ** exp` in O(log exp) instead of O(exp) by repeated squaring — halving the exponent each step is the same "cut the problem in half" idea as [binary search](binary-search.md), just applied to multiplication instead of comparisons. Multiplying `base` by itself doubles the effective exponent it represents at each step, so only log₂(exp) squarings are needed to cover the full exponent.

**Complexity:** O(log exp) time.

**Related:** [bitwise-operators (syntax)](../syntax/bitwise-operators.md) · [binary-search](binary-search.md)
