# `defaultdict`

```python
from collections import defaultdict

groups = defaultdict(list)
groups["a"].append(1)     # no KeyError — auto-creates [] for missing "a" first
groups["a"].append(2)     # groups == {"a": [1, 2]}

counts = defaultdict(int)
counts["x"] += 1           # auto-creates 0 for missing "x", then increments
```

A `defaultdict` takes a factory function (`list`, `int`, `set`, ...) and calls it automatically to create a value the first time a missing key is accessed — eliminating the `if key not in d: d[key] = ...` boilerplate before every append/increment. Extremely common for grouping (anagrams, adjacency lists) and counting.

**Related:** [dict-basics](dict-basics.md) · [counter](counter.md) · [dict-methods](dict-methods.md)
