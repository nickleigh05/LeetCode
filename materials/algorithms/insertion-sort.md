# Insertion Sort

```python
def insertion_sort(nums):
    for i in range(1, len(nums)):
        key = nums[i]                       # next card to place
        j = i - 1
        while j >= 0 and nums[j] > key:     # shift bigger elements right
            nums[j + 1] = nums[j]
            j -= 1
        nums[j + 1] = key                   # drop into the gap
```

Sort the way you sort a hand of cards: take the next element and slide it left into its place among the already-sorted prefix. Quadratic in general, but with two properties that keep it genuinely relevant: it's **O(n + inversions)** — near-linear on nearly-sorted data — and it's the fastest thing alive on tiny arrays, which is why Timsort (Python's [sorted](../syntax/sorting-key.md)) and quicksort implementations hand small slices to insertion sort. Also the model for "insert into a sorted [linked list](../data-structures/linked-list.md)" problems (LC 147).

**Complexity:** O(n²) worst · O(n) on nearly-sorted input · O(1) space · stable.

**Related:** [bubble-sort](bubble-sort.md) · [merge-sort](merge-sort.md) · [Sorting lesson](../learning/05b-sorting.md) · [bisect-module (syntax)](../syntax/bisect-module.md)
