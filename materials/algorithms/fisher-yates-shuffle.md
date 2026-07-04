# Fisher-Yates Shuffle

```python
import random

def shuffle(nums):
    for i in range(len(nums) - 1, 0, -1):
        j = random.randint(0, i)               # j ∈ [0, i] — inclusive!
        nums[i], nums[j] = nums[j], nums[i]    # settle position i
    return nums
```

The one correct way to shuffle: walk from the back, swapping each position with a uniformly random index **at or before it**. Each element ends up in each slot with probability exactly 1/n — provable by induction, and it's what `random.shuffle` does internally. The classic *wrong* version, `j = randint(0, n - 1)` every time, looks more random but isn't: it generates nⁿ equally likely swap sequences that must map onto n! orderings, and nⁿ isn't divisible by n!, so some orderings come up measurably more often. Appears on LeetCode as Shuffle an Array (LC 384), and in interviews as "shuffle a deck — and *prove* it's fair."

**Complexity:** O(n) time · O(1) extra space · uniform over all n! permutations.

**Related:** [random-module (syntax)](../syntax/random-module.md) · [reservoir-sampling](reservoir-sampling.md) · [swap-tuple-assign (syntax)](../syntax/swap-tuple-assign.md)
