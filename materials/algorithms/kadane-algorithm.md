# Kadane's Algorithm

```python
def max_subarray(nums):
    best = nums[0]
    current = nums[0]
    for num in nums[1:]:
        current = max(num, current + num)   # extend, or start fresh at num
        best = max(best, current)
    return best
```

Finds the maximum-sum contiguous subarray in one linear pass by tracking "best sum ending exactly at the current position" — at each step, either extend the previous running subarray or abandon it and start fresh at the current element, whichever gives a bigger sum. The moment `current` drops below the value of starting fresh, the old subarray is "worse than nothing" and gets discarded.

A specific instance of the general 1-D DP pattern: state = "best answer ending here," transition = "extend or restart."

**Complexity:** O(n) time, O(1) space.

**Related:** [array (data-structures)](../data-structures/array.md) · [for-loop (syntax)](../syntax/for-loop.md)
