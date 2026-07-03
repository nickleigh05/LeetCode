# Quicksort

```python
def quicksort(nums):
    if len(nums) <= 1:
        return nums
    pivot = nums[len(nums) // 2]
    left = [x for x in nums if x < pivot]
    mid = [x for x in nums if x == pivot]
    right = [x for x in nums if x > pivot]
    return quicksort(left) + mid + quicksort(right)
```

Picks a **pivot**, partitions the array into "smaller than pivot" and "larger than pivot," then recursively sorts each side — unlike [merge sort](merge-sort.md), the partitioning does the real work and the recursion just applies it to smaller pieces. Average case is O(n log n), but a poorly chosen pivot on already-sorted (or adversarial) input degrades to O(n²); randomized or median-of-three pivot selection avoids that in practice. Not stable in typical in-place implementations.

**Complexity:** O(n log n) average, O(n²) worst case · O(log n) space (recursion) for the in-place version.

**Related:** [merge-sort](merge-sort.md) · [array (data-structures)](../data-structures/array.md)
