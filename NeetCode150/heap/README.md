# Heap / Priority Queue

## 9. Heap / Priority Queue (7 problems)

| Problem # | Difficulty | Problem Name | LeetCode Link |
|-----------|------------|--------------|---------------|
| 703 | Easy | Kth Largest Element in a Stream | [Link](https://leetcode.com/problems/kth-largest-element-in-a-stream/) |
| 1046 | Easy | Last Stone Weight | [Link](https://leetcode.com/problems/last-stone-weight/) |
| 973 | Medium | K Closest Points to Origin | [Link](https://leetcode.com/problems/k-closest-points-to-origin/) |
| 215 | Medium | Kth Largest Element in an Array | [Link](https://leetcode.com/problems/kth-largest-element-in-an-array/) |
| 621 | Medium | Task Scheduler | [Link](https://leetcode.com/problems/task-scheduler/) |
| 355 | Medium | Design Twitter | [Link](https://leetcode.com/problems/design-twitter/) |
| 295 | Hard | Find Median from Data Stream | [Link](https://leetcode.com/problems/find-median-from-data-stream/) |

---

## Data Structures

### Min-Heap
A complete binary tree where every parent is ≤ its children. The minimum element is always at the root. Push and pop are O(log n). In Python, `heapq` is a min-heap — `heappush(heap, x)` and `heappop(heap)`.

### Max-Heap
Same as min-heap but the maximum is at the root. Python's `heapq` doesn't have a built-in max-heap, so negate values: push `-x` to simulate a max-heap.

### Two Heaps (Median Tracking)
Use a max-heap for the lower half and a min-heap for the upper half. Balance them so they differ in size by at most 1. The median is either the top of the larger heap or the average of both tops. Used in Find Median from Data Stream.

---

## Core Patterns

### Kth Largest (Min-Heap of Size K)
Maintain a min-heap of size k. For each new element, push it. If the heap grows beyond k, pop the minimum. After processing all elements, the heap's minimum is the kth largest. Keeps only k elements in memory. Used in Kth Largest Element in a Stream.

### Kth Smallest (Max-Heap of Size K)
Same idea but with a max-heap of size k. Push negated values. When size exceeds k, pop the max (which is the smallest among the candidates you're keeping). The top of the heap is the kth smallest.

### Top K Elements
Build a heap of all elements in O(n), then pop k times — O(k log n). Or use a size-k heap as you stream elements — O(n log k). Used in K Closest Points to Origin.

### Greedy with Heap (Task Scheduler)
Greedily pick the most frequent remaining task each cooldown cycle. A max-heap of `(count, task)` lets you always grab the highest-frequency task in O(log n). When a task must wait, hold it in a "cooldown queue" and re-add it to the heap when it's ready.

### Merge K Sorted Streams
Push the first element of each stream into a min-heap along with a pointer to its stream. Pop the minimum, advance that stream's pointer, and push the next element from that stream. Each pop gives the globally smallest remaining element. O(n log k). Used in Design Twitter (k most recent tweets from followed users).
