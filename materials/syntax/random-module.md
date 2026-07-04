# random Module

```python
import random

random.randint(1, 6)        # int in [1, 6] — BOTH ends inclusive
random.random()             # float in [0.0, 1.0)
random.choice(nums)         # one element, uniformly
random.shuffle(nums)        # permute a list in place (Fisher-Yates inside)
random.sample(nums, k=3)    # k distinct elements, order randomized

random.seed(42)             # same "random" sequence every run — reproducible tests
```

Pseudo-randomness for the design-flavored problems that ask for it: Shuffle an Array ([Fisher-Yates](../algorithms/fisher-yates-shuffle.md)), Random Pick with Weight (`random.random()` + [binary search](../algorithms/binary-search.md) over prefix sums), [reservoir sampling](../algorithms/reservoir-sampling.md), and randomized-pivot [quickselect](../algorithms/quickselect.md). Also handy off-judge for generating stress-test inputs when [testing locally](../guides/testing-locally.md). Note `randint` is inclusive on both ends — unlike [range](range-function.md) — a reliable off-by-one source.

**Related:** [fisher-yates-shuffle (algorithms)](../algorithms/fisher-yates-shuffle.md) · [reservoir-sampling (algorithms)](../algorithms/reservoir-sampling.md) · [range-function](range-function.md)
