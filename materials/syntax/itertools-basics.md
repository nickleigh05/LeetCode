# `itertools` Basics

```python
from itertools import combinations, permutations, product

list(combinations([1, 2, 3], 2))    # [(1,2), (1,3), (2,3)] — order doesn't matter
list(permutations([1, 2, 3], 2))     # [(1,2), (1,3), (2,1), (2,3), (3,1), (3,2)] — order matters
list(product([0, 1], repeat=2))       # [(0,0), (0,1), (1,0), (1,1)] — cartesian product
```

`itertools` provides combinatorics generators so you don't hand-write nested loops for "all pairs," "all orderings," or "all combinations of choices." `combinations` gives unordered subsets, `permutations` gives every ordering, `product` gives every combination across independent choices.

**Related:** [generator-expressions](generator-expressions.md) *(a backtracking-pattern cross-link will go here once `roadmap/patterns/` is built)*
