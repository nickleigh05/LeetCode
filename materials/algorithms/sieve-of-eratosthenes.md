# Sieve of Eratosthenes

```python
def primes_up_to(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(n ** 0.5) + 1):
        if is_prime[p]:
            for multiple in range(p * p, n + 1, p):   # start at p² — smaller
                is_prime[multiple] = False            # multiples already crossed
    return [i for i, ok in enumerate(is_prime) if ok]
```

Find **all** primes up to n by elimination instead of testing: assume everything prime, then each prime crosses off its multiples. Two classic optimizations baked in: stop the outer loop at √n (any composite ≤ n has a factor ≤ √n) and start crossing at p² (products with smaller factors are already gone). The harmonic-ish sum of the work gives the famous O(n log log n) — effectively linear, versus O(n√n) for trial-dividing each number. This is the tool whenever a problem needs primality for *a range* (Count Primes LC 204, prime-factor DP); for a *single* big number, plain trial division to √n is the right size. Variant worth knowing: store each number's *smallest prime factor* instead of a boolean, and you can factorize any m ≤ n in O(log m) afterwards.

**Complexity:** O(n log log n) time · O(n) space.

**Related:** [euclidean-gcd](euclidean-gcd.md) · [modular-arithmetic](modular-arithmetic.md) · [Math lesson](../learning/19-math-geometry.md)
