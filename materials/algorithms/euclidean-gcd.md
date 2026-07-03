# Euclidean Algorithm (GCD)

```python
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return a * b // gcd(a, b)
```

Finds the greatest common divisor by repeatedly replacing `(a, b)` with `(b, a % b)` until `b` hits 0 — relies on the fact that `gcd(a, b) == gcd(b, a % b)`, shrinking the problem each step far faster than checking every candidate divisor. LCM (least common multiple) falls out of GCD directly: `lcm(a, b) = a * b / gcd(a, b)`.

**Complexity:** O(log(min(a, b))) time.

**Related:** [integer-division-modulo (syntax)](../syntax/integer-division-modulo.md) · [math-module-basics (syntax)](../syntax/math-module-basics.md)
