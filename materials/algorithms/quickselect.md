# Quickselect

```python
import random

def quickselect(nums, k):                  # k-th smallest, 0-indexed
    pivot = random.choice(nums)
    lo  = [x for x in nums if x < pivot]
    eq  = [x for x in nums if x == pivot]
    hi  = [x for x in nums if x > pivot]
    if k < len(lo):
        return quickselect(lo, k)
    if k < len(lo) + len(eq):
        return pivot                       # k lands in the equal block
    return quickselect(hi, k - len(lo) - len(eq))
```

[Quicksort](quicksort.md) that only recurses into the **one side containing the answer** — partition around a pivot, see which block index k falls in, discard the rest. Halving (in expectation) instead of splitting gives n + n/2 + n/4 + … = **O(n) average**, the fastest known route to "k-th smallest/largest" (LC 215) and the alternative the interviewer is fishing for after your [heap](../learning/09-heap-priority-queue.md) solution. The random pivot matters: it makes the O(n²) worst case a lottery loss rather than something a sorted input triggers deterministically. The in-place two-pointer partition version saves the list copies; same idea, more index bookkeeping.

**Complexity:** O(n) average, O(n²) worst (random pivot makes it vanishingly unlikely) · this version O(n) space, in-place version O(1).

**Related:** [quicksort](quicksort.md) · [heapsort](heapsort.md) · [random-module (syntax)](../syntax/random-module.md) · [Heap lesson](../learning/09-heap-priority-queue.md)
