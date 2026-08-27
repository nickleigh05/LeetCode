# Selection Sort

```python
def selection_sort(nums):
    n = len(nums)
    for i in range(n):
        m = i                          # find the min of the unsorted remainder…
        for j in range(i + 1, n):
            if nums[j] < nums[m]:
                m = j
        nums[i], nums[m] = nums[m], nums[i]   # …and swap it into slot i
```

For each position, scan the rest for the smallest remaining element and swap it in. Always Θ(n²) — no lucky best case, since the scan happens regardless — but it makes the **fewest swaps** of any comparison sort (≤ n−1), its once-useful niche when writes were expensive. Pedagogically it's the cleanest possible loop-invariant example ("slots 0..i are final and sorted"), and the mental stepping stone to [heapsort](heapsort.md), which is selection sort with the linear scan replaced by an O(log n) [heap](../data-structures/heap.md) extraction.

**Complexity:** Θ(n²) time always · O(1) space · not stable (the long-range swap reorders equals).

**Related:** [heapsort](heapsort.md) · [bubble-sort](bubble-sort.md) · [insertion-sort](insertion-sort.md) · [Sorting lesson](../learning/05b-sorting.md)
