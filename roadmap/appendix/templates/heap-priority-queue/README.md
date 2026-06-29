# Heap / Priority Queue

*Whenever you hear "top K", "k-th largest", or "running median", reach for a heap. O(log n) to insert or pull the extreme, and the extreme is always at the root.*

## Recognize this pattern when...

- The ask is **"top K"**, **"k-th largest / smallest"**, or **"k closest"**.
- You need a **running / streaming** statistic (median, max so far) as elements arrive.
- You repeatedly need the **most / least extreme** element and the set keeps changing.
- You're **merging k sorted** sequences, or scheduling by priority.
- A full sort is O(n log n) but you only need the extreme few — a bounded heap gets you O(n log k).

## Variations

1. **Bounded size-K min-heap** — keep only the best k; root is the eviction candidate. *(Kth Largest Element in an Array / in a Stream)*
2. **Heapify + combine** — pull the extreme(s), do work, push the result back. *(Last Stone Weight)*
3. **Tuple priorities** — push `(key, item)` so the heap ranks by `key`. *(K Closest Points to Origin)*
4. **Two heaps for median** — a max-heap for the low half, min-heap for the high half, kept balanced. *(Find Median from Data Stream)*
5. **Heap of list heads** — one entry per source list, pop the smallest and push its successor. *(Merge k Sorted Lists)*
6. **Max-heap via negation / greedy schedule** — negate for max behaviour; reschedule by remaining count. *(Task Scheduler)*

## Representative problems

| # | Difficulty | Problem |
|---|------------|---------|
| 1046 | Easy | Last Stone Weight |
| 703 | Easy | Kth Largest Element in a Stream |
| 215 | Medium | Kth Largest Element in an Array |
| 973 | Medium | K Closest Points to Origin |
| 621 | Medium | Task Scheduler |
| 295 | Hard | Find Median from Data Stream |

## Common bugs & traps

- **heapq is a min-heap.** For a max-heap, push `-value` (or `(-key, item)`) and negate back when you read it out — sign-flip bugs are the #1 mistake here.
- **Not bounding the heap.** For "k largest", evict once size exceeds k; otherwise you're back to O(n log n).
- **Tuple comparison blowups.** If two priorities tie, Python compares the next tuple element — add a unique counter (`(key, count, item)`) so it never tries to compare un-orderable objects.
- **Two-heap imbalance.** After every insert, rebalance so the heap sizes differ by at most 1, or the median read is wrong.
- **`heapify` vs n pushes.** Building from a list is O(n) with `heapify`; n separate pushes is O(n log n).
- **Reading the root without checking emptiness.** `heap[0]` on an empty heap raises — guard with `if heap`.
---

*See also: [Lesson 09 →](../../../learning/09-heap-priority-queue.md) · [🗺 Roadmap](../../../roadmap.md) · [problem lists](../../../../lists/)*
