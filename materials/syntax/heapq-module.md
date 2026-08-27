# heapq Module

```python
import heapq

h = []
heapq.heappush(h, 5)          # add, O(log n)
heapq.heappush(h, 1)
smallest = heapq.heappop(h)   # remove & return the MIN, O(log n) → 1
peek = h[0]                   # look at the min without removing, O(1)

nums = [5, 1, 8, 3]
heapq.heapify(nums)           # turn a list into a heap in-place, O(n)

heapq.nlargest(3, nums)       # top-3 biggest (also nsmallest), O(n log k)
```

`heapq` treats a plain list as a **min-heap** — the smallest element is always at index 0. There is no max-heap version: **negate on the way in, negate on the way out** (`heappush(h, -x)` … `-heappop(h)`). For "sort by priority, carry data along," push tuples — `(dist, node)` — which compare by first element; add an index tiebreaker `(dist, i, node)` if the payloads aren't comparable.

**Complexity:** push/pop O(log n) · peek O(1) · heapify O(n).

**Related:** [heap (data-structures)](../data-structures/heap.md) · [tuple-basics](tuple-basics.md) · [import-basics](import-basics.md) · [Heaps lesson](../learning/09-heap-priority-queue.md)
