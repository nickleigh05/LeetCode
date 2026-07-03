# Heap / Priority Queue

```python
import heapq
heap = []
heapq.heappush(heap, 5)     # O(log n)
heapq.heappush(heap, 1)
heapq.heappush(heap, 3)
heapq.heappop(heap)           # 1 — always the smallest, O(log n)
```

A binary tree stored in an array, kept "heap-ordered": every parent is ≤ (min-heap) or ≥ (max-heap) both its children. That invariant guarantees the smallest (or largest) element is always at the root, retrievable in O(1) — but Python's `heapq` module only provides a **min-heap**; negate values on push/pop to simulate a max-heap.

Reach for a heap whenever a problem says "kth largest/smallest," "top K," or "always process the current minimum/maximum next" (Dijkstra's algorithm, merge k sorted lists).

**Complexity:** push/pop O(log n) · peek min/max O(1) · build from an existing list O(n) via `heapq.heapify`.

**Related:** [dijkstra](../algorithms/dijkstra.md) · [import-basics (syntax)](../syntax/import-basics.md)
