# Bubble Sort

```python
def bubble_sort(nums):
    n = len(nums)
    for i in range(n):
        swapped = False
        for j in range(n - 1 - i):          # last i items already settled
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
                swapped = True
        if not swapped:                     # a clean pass = already sorted
            break
```

Repeatedly sweep the array, swapping adjacent out-of-order pairs — each pass "bubbles" the largest remaining element to the end. Nobody uses it in production; it's here because it's the classic first sorting algorithm, the simplest correctness argument you'll ever write (after pass i, the last i elements are final), and a fair baseline for appreciating why [merge sort](merge-sort.md) was worth inventing. The `swapped` early-exit gives O(n) on already-sorted input.

**Complexity:** O(n²) time (O(n) best case with early exit) · O(1) space · stable.

**Related:** [insertion-sort](insertion-sort.md) · [selection-sort](selection-sort.md) · [Sorting lesson](../learning/05b-sorting.md) · [swap-tuple-assign (syntax)](../syntax/swap-tuple-assign.md)
