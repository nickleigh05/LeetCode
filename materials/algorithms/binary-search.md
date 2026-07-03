# Binary Search

```python
def binary_search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

Repeatedly halves a **sorted** search space by comparing the middle element to the target and discarding the half that can't contain it — each step cuts the remaining candidates in half, giving O(log n) instead of O(n) for a linear scan.

Generalizes beyond arrays to "binary search on the answer": if a yes/no question has a monotonic boundary (everything below some threshold is "no," everything above is "yes"), you can binary-search that threshold directly, even without an explicit sorted array.

**Complexity:** O(log n) time · O(1) space (iterative).

**Related:** [array (data-structures)](../data-structures/array.md) · [binary-search-tree (data-structures)](../data-structures/binary-search-tree.md) · [chained-comparisons (syntax)](../syntax/chained-comparisons.md)
