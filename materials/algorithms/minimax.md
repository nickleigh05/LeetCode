# Minimax & Game Theory

```python
from functools import cache

def stone_game(piles):                     # LC 877 family: optimal two-player play
    @cache
    def best_margin(i, j):                 # my best (my score − yours), piles[i..j]
        if i > j:
            return 0
        take_left  = piles[i] - best_margin(i + 1, j)   # their optimal turn is
        take_right = piles[j] - best_margin(i, j - 1)   # subtracted — they play
        return max(take_left, take_right)               # perfectly too
    return best_margin(0, len(piles) - 1) > 0           # True → first player wins
```

"Both players play optimally" means recursion where the players alternate: I maximize, and whatever state I hand over, **my opponent's optimal result gets subtracted from mine** (the score-margin trick above collapses separate max/min layers into one negation — same idea as chess engines' negamax). Overlapping states make it [DP](dynamic-programming.md) — add [`@cache`](../syntax/functools-cache.md) and done. The other family is **Nim-style math games** (LC 292: losing positions are multiples of 4 — find the pattern by brute-forcing small n and staring). Full minimax with alpha-beta pruning runs game AIs; LeetCode only ever needs the memoized skeleton plus the "subtract their best" insight.

**Complexity:** O(#states × moves per state) with memoization — O(n²)·O(1) for interval games like Stone Game.

**Related:** [dynamic-programming](dynamic-programming.md) · [functools-cache (syntax)](../syntax/functools-cache.md) · [backtracking](backtracking.md) · [DP lesson](../learning/14-dp-1d.md)
