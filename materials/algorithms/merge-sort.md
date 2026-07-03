# Merge Sort

```python
def merge_sort(nums):
    if len(nums) <= 1:
        return nums
    mid = len(nums) // 2
    left = merge_sort(nums[:mid])
    right = merge_sort(nums[mid:])
    return merge(left, right)

def merge(left, right):
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    return result + left[i:] + right[j:]
```

Splits the array in half recursively down to single elements (trivially sorted), then merges sorted halves back together in linear time — the merge step is why the whole algorithm is O(n log n): log n levels of splitting, O(n) work to merge at each level. **Stable** (equal elements keep their relative order), which matters for multi-key sorting.

**Complexity:** O(n log n) time, all cases · O(n) extra space for the merge buffers.

**Related:** [quicksort](quicksort.md) · [array (data-structures)](../data-structures/array.md) · [recursion-basics (syntax)](../syntax/recursion-basics.md)
