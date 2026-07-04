# Heapsort

```python
import heapq

def heapsort(nums):                    # the honest Python version
    heapq.heapify(nums)                # O(n)
    return [heapq.heappop(nums) for _ in range(len(nums))]   # n × O(log n)
```

[Selection sort](selection-sort.md)'s smart sibling: repeatedly extract the minimum — but from a [heap](../data-structures/heap.md), where extraction is O(log n) instead of an O(n) scan. The textbook in-place version builds a *max*-heap inside the array itself, then repeatedly swaps the root to the end and sifts down — O(n log n) guaranteed with O(1) extra space, the only mainstream sort with both properties (quicksort risks O(n²), merge sort takes O(n) space).

In practice it loses to both on real hardware (cache-hostile jumps, no adaptivity), so its interview value is conceptual: it *is* the "use a heap" pattern — and when a problem only needs the k smallest items, stopping after k pops turns heapsort into the O(n + k log n) [top-K technique](../learning/09-heap-priority-queue.md).

**Complexity:** O(n log n) time guaranteed · O(1) space (in-place version) · not stable.

**Related:** [heap (data-structures)](../data-structures/heap.md) · [heapq-module (syntax)](../syntax/heapq-module.md) · [selection-sort](selection-sort.md) · [quicksort](quicksort.md)
