# Dynamic Programming

```python
# Top-down (memoized recursion)
def fib(n, memo={}):
    if n <= 1: return n
    if n not in memo:
        memo[n] = fib(n - 1, memo) + fib(n - 2, memo)
    return memo[n]

# Bottom-up (tabulation)
def fib_tab(n):
    if n <= 1: return n
    dp = [0, 1]
    for i in range(2, n + 1):
        dp.append(dp[i - 1] + dp[i - 2])
    return dp[n]
```

Solves a problem by breaking it into overlapping subproblems, solving each one **once**, and reusing the stored answer instead of recomputing it — plain [recursion](../syntax/recursion-basics.md) on `fib(n)` recomputes the same smaller values exponentially many times; caching those results (memoization, top-down) or building them up iteratively (tabulation, bottom-up) collapses that to linear or polynomial time.

Every DP problem comes down to three questions: what's the **state** (what varies between subproblems), what's the **transition** (how a state's answer is built from smaller states' answers), and what's the **base case**.

**Complexity:** depends on the problem — typically (number of distinct states) × (work per state); turns exponential brute force into polynomial time.

**Related:** [recursion-basics (syntax)](../syntax/recursion-basics.md) · [kadane-algorithm](kadane-algorithm.md) · [decorators-basics (syntax)](../syntax/decorators-basics.md)
