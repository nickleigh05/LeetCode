# 09. Heaps & Priority Queues
*The always-available extreme element — for top-K and streaming.*

[← Prev](08-tries.md) · [🗺 Roadmap](../../roadmap.md) · [Next →](10-backtracking.md)

---

A **heap** gives you the smallest (or largest) element in O(1) and reinserts in O(log n) — perfect when you repeatedly need the current extreme but don't need everything sorted. It's the engine behind **top-K** problems and streaming medians (the **two-heaps** trick).

## Concept

### Heap and Priority Queue

```
  Min-Heap (smallest at top):    Max-Heap (largest at top):
           1                               9
          / \                             / \
         3   2                           7   8
        / \ / \                         / \ / \
       5  4 6  7                       2  4 1  3

  Array representation (0-indexed):
  heap = [1, 3, 2, 5, 4, 6, 7]
          0  1  2  3  4  5  6

  For node at index i:
    parent     = (i - 1) // 2
    left child = 2*i + 1
    right child= 2*i + 2

  Push: append to end, bubble up   → O(log n)
  Pop:  remove root, sink last     → O(log n)
  Peek: root is always min/max     → O(1)
```

**What it is:** A complete binary tree stored as an array where every parent is smaller (min-heap) or larger (max-heap) than its children. The root is always the global minimum/maximum.

**Key Properties:**
- Python's `heapq` is a **min-heap** only
- For a max-heap: negate all values (`-val`) when pushing, negate when popping
- Push/pop are O(log n); peek is O(1)
- Does NOT support O(log n) arbitrary removal or search — it only guarantees fast access to the min/max

**Complexity:**

| Operation | Time |
|-----------|------|
| Push | O(log n) |
| Pop min/max | O(log n) |
| Peek min/max | O(1) |
| Build heap from list | O(n) |
| Search arbitrary | O(n) |
| Space | O(n) |

**Use when:**
- You repeatedly need the smallest (or largest) element
- Kth largest / Top K frequent elements
- Scheduling: always process the highest-priority task
- Streaming median (use two heaps)
- Dijkstra's algorithm (needs cheapest unvisited node)

**Python:**
```python
import heapq

# Min-heap
heap = []
heapq.heappush(heap, 3)
heapq.heappush(heap, 1)
heapq.heappush(heap, 2)
heapq.heappop(heap)     # → 1 (smallest)
heap[0]                  # peek min without removing

# Build heap from list — O(n)
nums = [3, 1, 4, 1, 5]
heapq.heapify(nums)

# Max-heap: negate values
heapq.heappush(heap, -val)
max_val = -heapq.heappop(heap)

# Heap of tuples (sorted by first element)
heapq.heappush(heap, (priority, item))

# Kth largest
import heapq
def kth_largest(nums, k):
    return heapq.nlargest(k, nums)[-1]
```

## The Pattern

### Top K Elements

```
  Find 3 largest in [3,1,4,1,5,9,2,6,5]:

  Approach 1: Min-heap of size k=3
  Process each element, maintain heap of 3 largest:
  heap=[]
  3 → heap=[3]
  1 → heap=[1,3]
  4 → heap=[1,3,4]  size=k
  1 → 1 ≤ heap[0]=1, skip
  5 → 5 > heap[0]=1, pop 1, push 5 → heap=[3,4,5]
  9 → 9 > heap[0]=3, pop 3, push 9 → heap=[4,5,9]
  2 → 2 ≤ heap[0]=4, skip
  6 → 6 > heap[0]=4, pop 4, push 6 → heap=[5,6,9]
  5 → 5 = heap[0]=5, pop 5, push 5 → heap=[5,6,9]
  Result: [5, 6, 9] ← top 3

  Approach 2: QuickSelect (find kth largest, then return k elements)
  Approach 3: Sort + slice (O(n log n) — only good when already sorting)
```

**What it is:** Maintain a min-heap of size k. Iterate through all elements — if the current element is larger than the heap's minimum, replace it. After processing all elements, the heap contains the top k largest.

**Use this when:**
- [ ] Kth largest element in array/stream
- [ ] Top K frequent elements
- [ ] K closest points to origin
- [ ] K pairs with smallest sums
- [ ] Streaming data where you can't sort the whole input

**Why min-heap for top-k LARGEST?** The heap's root is the smallest of your k candidates — any new element larger than it can replace it.

**Python:**
```python
import heapq
from collections import Counter

# Kth largest element
def kth_largest(nums, k):
    heap = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]   # smallest of the top-k = kth largest

# Or simply:
def kth_largest_v2(nums, k):
    return heapq.nlargest(k, nums)[-1]

# Top K frequent elements
def top_k_frequent(nums, k):
    freq = Counter(nums)
    # min-heap of (count, element), keep top k
    return heapq.nlargest(k, freq.keys(), key=freq.get)

# K closest points to origin
def k_closest(points, k):
    # max-heap: negate distance to simulate max-heap with heapq (min-heap)
    heap = []
    for x, y in points:
        dist = x*x + y*y
        heapq.heappush(heap, (-dist, x, y))
        if len(heap) > k:
            heapq.heappop(heap)
    return [[x, y] for _, x, y in heap]

# Streaming — process one at a time
class KthLargestStream:
    def __init__(self, k, nums):
        self.k = k
        self.heap = []
        for n in nums:
            self.add(n)

    def add(self, val):
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)
        return self.heap[0]
```

**Complexity:** O(n log k) — better than O(n log n) sort when k << n.

**Blind 75 examples:** Top K Frequent Elements · (Kth Largest in Stream is a classic extension)

### Two Heaps

```
  Find Median from Data Stream:

  Idea: split numbers into two halves.
  Left half (max-heap): stores smaller half  → root = lower median
  Right half (min-heap): stores larger half  → root = upper median

  Insert 1, 2, 3, 4, 5 one by one:

  After 1:  max_heap=[-1]    min_heap=[]      median=1
  After 2:  max_heap=[-1]    min_heap=[2]     median=(1+2)/2=1.5
  After 3:  max_heap=[-2,-1] min_heap=[3]     median=2
                              ↑ rebalanced
  After 4:  max_heap=[-2,-1] min_heap=[3,4]   median=(2+3)/2=2.5
  After 5:  max_heap=[-3,-2,-1] min_heap=[4,5] median=3
                              ↑ rebalanced

  Invariant:
  • Both heaps differ in size by at most 1
  • All elements in max_heap ≤ all elements in min_heap
  • If equal size: median = (max_heap[0] + min_heap[0]) / 2
  • If max_heap has one more: median = -max_heap[0]
```

**What it is:** Use a max-heap to represent the lower half of numbers and a min-heap for the upper half. This lets you find the median in O(1) and insert in O(log n).

**Use this when:**
- [ ] Streaming median (Find Median from Data Stream)
- [ ] Sliding window median
- [ ] "Balance" problems where you need the middle value of a dynamic dataset

**Python:**
```python
import heapq

class MedianFinder:
    def __init__(self):
        self.lo = []   # max-heap (negate values) — lower half
        self.hi = []   # min-heap                 — upper half

    def add_num(self, num):
        # Always push to lo first
        heapq.heappush(self.lo, -num)

        # Maintain order: lo's max ≤ hi's min
        if self.lo and self.hi and (-self.lo[0]) > self.hi[0]:
            heapq.heappush(self.hi, -heapq.heappop(self.lo))

        # Rebalance sizes: lo can have at most 1 more than hi
        if len(self.lo) > len(self.hi) + 1:
            heapq.heappush(self.hi, -heapq.heappop(self.lo))
        if len(self.hi) > len(self.lo):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def find_median(self):
        if len(self.lo) > len(self.hi):
            return -self.lo[0]
        return (-self.lo[0] + self.hi[0]) / 2.0
```

**Complexity:** O(log n) insert, O(1) median.

**Blind 75 examples:** Find Median from Data Stream

## The Template

The reusable code skeleton for this pattern lives in [`appendix/templates/heap-priority-queue/`](../appendix/templates/heap-priority-queue/). Read the README (when to reach for it, variations, common bugs), then type out [`template.py`](../appendix/templates/heap-priority-queue/template.py) from memory before you drill problems.

## Practice

Work the matching set in the curated list: [**Heaps & Priority Queues problems →**](../../lists/recommended.md#8-heap--priority-queue-14-problems). Easy → hard, top to bottom. When the pattern feels automatic, move on — don't grind it forever.

## Check Yourself

- [ ] I can explain when a heap beats sorting (streaming / top-K without seeing all data at once).
- [ ] I can write the top-K pattern with `heapq` from memory, and simulate a max-heap with negation.
- [ ] I know the two-heap trick for a running median.
- [ ] I solved a 🔴 Hard heap problem (e.g. Find Median from Data Stream).

---

**Up next:** [Backtracking](10-backtracking.md) — choose → explore → un-choose, over the tree of partial solutions.

[← Prev](08-tries.md) · [🗺 Roadmap](../../roadmap.md) · [Next →](10-backtracking.md)

