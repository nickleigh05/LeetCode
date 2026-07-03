# Counting Sort

```python
def counting_sort(nums, max_val):
    counts = [0] * (max_val + 1)
    for num in nums:
        counts[num] += 1

    result = []
    for val, count in enumerate(counts):
        result.extend([val] * count)
    return result
```

Sorts by counting how many times each value occurs, then reading the counts back out in order — skips comparisons entirely, so it beats the O(n log n) floor that comparison-based sorts ([merge sort](merge-sort.md), [quicksort](quicksort.md)) are stuck with. Only works when values are integers in a known, reasonably small range — the count array is sized to the value range, not the input length, so it wastes memory (or breaks) on sparse/huge ranges.

**Complexity:** O(n + k) time and space, where k is the value range.

**Related:** [merge-sort](merge-sort.md) · [enumerate (syntax)](../syntax/enumerate.md)
