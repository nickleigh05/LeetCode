# Matrix Exponentiation

```python
MOD = 10**9 + 7

def mat_mult(A, B):
    n, m, p = len(A), len(B[0]), len(B)
    return [[sum(A[i][k] * B[k][j] for k in range(p)) % MOD
             for j in range(m)] for i in range(n)]

def mat_pow(M, k):                      # M^k by repeated squaring
    R = [[int(i == j) for j in range(len(M))] for i in range(len(M))]  # identity
    while k:
        if k & 1:
            R = mat_mult(R, M)
        M = mat_mult(M, M)
        k >>= 1
    return R

# fib(n): [[1,1],[1,0]]^n → top-right entry. n = 10^18? No problem.
```

Any [DP](dynamic-programming.md) whose state transition is a *fixed linear combination of the last few states* — Fibonacci, tiling counts, "strings of length n avoiding pattern X" — can be written as a vector times a **transition matrix**. Then computing step n is just raising that matrix to the n-th power, and [fast exponentiation](fast-exponentiation.md) does that in O(log n) multiplications: linear recurrences evaluated at n = 10¹⁸, which no loop can touch. The tell in the constraints: n absurdly huge, answer mod 10⁹+7. LeetCode brushes it rarely (Student Attendance Record II, Count Vowels Permutation as overkill); competitive programming leans on it constantly.

**Complexity:** O(d³ log n) for a d-state recurrence · O(d²) space.

**Related:** [fast-exponentiation](fast-exponentiation.md) · [dynamic-programming](dynamic-programming.md) · [modular-arithmetic](modular-arithmetic.md) · [nested-lists (syntax)](../syntax/nested-lists.md)
