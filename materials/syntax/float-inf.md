# float('inf') — the Infinity Sentinel

```python
INF = float('inf')

best = INF                    # running MIN: start above everything
for cost in costs:
    best = min(best, cost)

float('-inf')                 # running MAX seed
INF > 10**100                 # True — bigger than any number
INF + 1 == INF                # True — arithmetic saturates
math.inf                      # same value, import math spelling

dist = [INF] * n              # Dijkstra / DP: "unreached / impossible yet"
```

Infinity is the standard "worse than anything real" seed for running minimums, unreachable distances in [Dijkstra](../algorithms/dijkstra.md), and impossible states in [DP](../learning/14-dp-1d.md) (e.g. Coin Change). Two cautions: it's a *float*, so `INF // 2` and mixing with huge ints get float semantics — and if an "impossible" answer must be reported as `-1`, remember to translate (`return ans if ans != INF else -1`). `float('nan')` is a different beast (not equal even to itself); you won't want it here.

**Related:** [int-float-basics](int-float-basics.md) · [min-max-key](min-max-key.md) · [float-precision-notes](float-precision-notes.md)
