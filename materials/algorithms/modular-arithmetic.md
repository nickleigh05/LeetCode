# Modular Arithmetic (mod 10⁹+7)

```python
MOD = 10**9 + 7

total = (a + b) % MOD                 # take % early and often — keeps numbers small
prod  = (a * b) % MOD
diff  = (a - b) % MOD                 # Python's % is always non-negative — safe!

pow(a, k, MOD)                        # a^k mod MOD, built-in fast exponentiation
inv_b = pow(b, MOD - 2, MOD)          # "division": modular inverse via Fermat
a_div_b = a * inv_b % MOD             # works because MOD is prime

# nCr mod p — the combinatorics workhorse:
# precompute fact[i], then C(n, r) = fact[n] * inv(fact[r]) * inv(fact[n-r]) % MOD
```

When a problem says *"return the answer modulo 10⁹+7,"* the true answer overflows everything, and you must do all arithmetic inside the modulus. Rules: `%` distributes over `+`, `-`, `×` (apply it after every operation), but **never over division** — divide by multiplying with the *modular inverse*, which exists because 10⁹+7 is prime (Fermat's little theorem: `b⁻¹ = b^(MOD−2)`). Python is uniquely comfortable here: ints never overflow (the % is for the *answer format*, and to keep numbers small enough to be fast), three-argument [`pow`](fast-exponentiation.md) is built in, and negative `%` already behaves correctly (unlike C++/Java — a real porting bug). Shows up in every counting-[DP](dynamic-programming.md) and combinatorics hard.

**Complexity:** all operations O(1)-ish (inverse costs O(log MOD)).

**Related:** [fast-exponentiation](fast-exponentiation.md) · [integer-division-modulo (syntax)](../syntax/integer-division-modulo.md) · [euclidean-gcd](euclidean-gcd.md) · [Math lesson](../learning/19-math-geometry.md)
