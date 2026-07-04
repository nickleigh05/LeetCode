# functools: @cache & friends

```python
from functools import cache, lru_cache

@cache                          # memoize: remember every (args) -> result
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

fib(300)                        # instant — each n computed once, then cached

@lru_cache(maxsize=1000)        # same idea, bounded memory (evicts least-recent)
def expensive(x, y): ...

fib.cache_clear()               # reset between test cases if state must not leak
```

One decorator line turns exponential recursion into top-down [DP](../algorithms/dynamic-programming.md) — arguments become dict keys, so they must be hashable ([tuples](tuple-basics.md) yes, lists no). `@cache` (3.9+) is `lru_cache(maxsize=None)` with less typing. Also in `functools`: `reduce` (fold a list to one value) and `cmp_to_key` (adapt an old-style compare function for [sorted's key=](sorting-key.md) — the trick behind Largest Number).

**Complexity:** each distinct argument tuple computed once; lookups O(1) average.

**Related:** [decorators-basics](decorators-basics.md) · [recursion-basics](recursion-basics.md) · [DP lesson](../learning/14-dp-1d.md) · [dict-basics](dict-basics.md)
