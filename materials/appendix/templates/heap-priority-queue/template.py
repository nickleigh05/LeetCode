"""
Heap / Priority Queue — Top-K and Streaming Skeletons

A binary heap hands you the smallest (or largest) element in O(1) and does
insert / extract in O(log n). Whenever a problem says "top K", "k-th largest",
"k closest", or "running median", a heap is almost certainly the tool.

Python's heapq is a MIN-heap. To keep the K *largest* elements, hold them in a
min-heap of size K: the smallest of your current best K sits at the root, ready
to be evicted the instant something bigger arrives.

Invariant (size-K min-heap): after processing each element, the heap holds the K
largest elements seen so far, and heap[0] is the smallest of those K.
"""

import heapq
from typing import List


def k_largest(nums: List[int], k: int) -> List[int]:
    """Return the k largest elements using a bounded min-heap.

    Time:      O(n log k) — n pushes/pops, each on a heap of size <= k.
    Space:     O(k) — the heap never grows past k.
    Invariant: the heap holds the best k elements seen so far; its root is the
               weakest of them and the first to be kicked out.
    """

    min_heap: List[int] = []

    for value in nums:
        # TODO: problem-specific priority. For "k closest", push a tuple like
        # (distance, value) so heap ordering ranks by distance first.
        heapq.heappush(min_heap, value)

        # Once we exceed k, drop the smallest — it cannot be in the top k.
        if len(min_heap) > k:
            heapq.heappop(min_heap)

    # Whatever survives is the answer (unordered).
    return min_heap


def heapify_and_combine(nums: List[int]) -> int:
    """Build a heap in O(n), then repeatedly combine the best elements.

    This is the shape behind Last Stone Weight, merge-k-lists, task scheduling,
    and Dijkstra's frontier: pull the extreme element(s), do work, push results.

    Time:      O(n) to build + O(n log n) over all combine steps.
    Space:     O(n) for the heap.
    Invariant: heap[0] is always the current extreme; every push/pop restores
               that property for the remaining elements.
    """

    # heapq has no max-heap, so negate values to simulate one.
    max_heap = [-value for value in nums]
    heapq.heapify(max_heap)  # in place, O(n) — cheaper than n individual pushes

    while len(max_heap) > 1:
        # Pull the two largest (remember the values are negated).
        largest = -heapq.heappop(max_heap)
        second = -heapq.heappop(max_heap)

        # TODO: problem-specific combine, then push the result back if non-trivial.
        if largest != second:
            heapq.heappush(max_heap, -(largest - second))

    # Negate back when reading the final value out.
    return -max_heap[0] if max_heap else 0
