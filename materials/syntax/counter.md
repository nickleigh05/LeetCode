# `Counter`

```python
from collections import Counter

freq = Counter([1, 1, 2, 3, 3, 3])   # Counter({3: 3, 1: 2, 2: 1})
freq[1]                                # 2
freq[99]                                # 0 — missing keys return 0, never KeyError
freq.most_common(2)                      # [(3, 3), (1, 2)] — top 2 by count

Counter("hello")                          # Counter({'l': 2, 'h': 1, 'e': 1, 'o': 1})
```

`Counter` is a `dict` subclass purpose-built for frequency counting — pass it any iterable and it tallies occurrences in one call, no manual loop needed. `.most_common(k)` returns the top-k items sorted by count, descending.

**Related:** [defaultdict](defaultdict.md) · [dict-basics](dict-basics.md)
