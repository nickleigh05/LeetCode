# Heap / Priority Queue

## How to use this README

Problems are split into three tiers: Blind 75 is the core set every interviewer expects you to know cold. NeetCode 150 adds problems that sharpen the same patterns with more constraints or design requirements. NeetCode 250 pushes into harder heap simulations and greedy combinations. Work through tiers in order — the Core Patterns and Syntax Reference sections below map directly to the problems in each table, so when you hit a new problem, find the matching pattern first, then check the syntax.

---

## Problems

### Blind 75
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved |
|-----------|------------|--------------|---------------|--------|
| 295 | Hard | Find Median from Data Stream | [Link](https://leetcode.com/problems/find-median-from-data-stream/) | ☐ |

### NeetCode 150
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved |
|-----------|------------|--------------|---------------|--------|
| 703 | Easy | Kth Largest Element in a Stream | [Link](https://leetcode.com/problems/kth-largest-element-in-a-stream/) | ☐ |
| 1046 | Easy | Last Stone Weight | [Link](https://leetcode.com/problems/last-stone-weight/) | ☐ |
| 973 | Medium | K Closest Points to Origin | [Link](https://leetcode.com/problems/k-closest-points-to-origin/) | ☐ |
| 215 | Medium | Kth Largest Element in an Array | [Link](https://leetcode.com/problems/kth-largest-element-in-an-array/) | ☐ |
| 621 | Medium | Task Scheduler | [Link](https://leetcode.com/problems/task-scheduler/) | ☐ |
| 355 | Medium | Design Twitter | [Link](https://leetcode.com/problems/design-twitter/) | ☐ |

### NeetCode 250
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved | Pattern |
|-----------|------------|--------------|---------------|--------|---------|
| 1834 | Medium | Single-Threaded CPU | [Link](https://leetcode.com/problems/single-threaded-cpu/) | ☐ | Heap simulation |
| 767 | Medium | Reorganize String | [Link](https://leetcode.com/problems/reorganize-string/) | ☐ | Greedy + max-heap |
| 1405 | Medium | Longest Happy String | [Link](https://leetcode.com/problems/longest-happy-string/) | ☐ | Greedy + max-heap |
| 1094 | Medium | Car Pooling | [Link](https://leetcode.com/problems/car-pooling/) | ☐ | Sweep line + heap |
| 502 | Hard | IPO | [Link](https://leetcode.com/problems/ipo/) | ☐ | Two-heap greedy |

---

## Complexity Reference

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| heappush | O(log n) | O(1) | Sifts up to restore heap property |
| heappop | O(log n) | O(1) | Sifts down to restore heap property |
| heapify (build from list) | O(n) | O(1) | Better than pushing n times (O(n log n)) |
| Peek minimum (h[0]) | O(1) | O(1) | Root is always the minimum |
| heapreplace (pop + push) | O(log n) | O(1) | Faster than separate pop then push |
| Top-K largest (min-heap of size k) | O(n log k) | O(k) | Maintain heap of fixed size k |
| K-way merge | O(n log k) | O(k) | n total elements across k sorted lists |
| Two-heap median insert | O(log n) | O(n) | One push + one rebalance push |
| Two-heap median query | O(1) | O(n) | Read one or two heap tops |

---

## Data Structures

### Binary Heap

A binary heap is a complete binary tree stored in a flat array. "Complete" means every level is fully filled except possibly the last, which is filled left to right. This shape guarantee is what lets the tree live in an array without storing pointers. For any node at index `i`, its parent is at `(i-1)//2` and its children are at `2*i+1` and `2*i+2`. A **min-heap** enforces that every parent is less than or equal to both its children, so the minimum is always at index 0.

```
Min-heap tree view:        Array representation:
         1                 index: 0  1  2  3  4  5
       /   \               value: 1  3  2  6  5  4
      3     2
     / \   /
    6   5 4

Parent of index 3 → (3-1)//2 = 1  (value 3) ✓
Children of index 1 → 2*1+1=3 (value 6), 2*1+2=4 (value 5) ✓
```

**When it matters:** Use a heap when you repeatedly need the minimum (or maximum) element and the collection is changing. A sorted array gives O(1) min but O(n) insert; a heap gives O(log n) for both.

### Priority Queue

A priority queue is an abstract data type: you push elements with a priority and always pop the highest-priority element first. Python's `heapq` implements a min-priority queue — the element with the lowest value (highest priority by default) comes out first. To simulate a max-priority queue, negate values before pushing.

**When it matters:** Any problem that says "always process the smallest/largest available item next" — task scheduling, Dijkstra's algorithm, median maintenance.

### Python's heapq Module

Python's `heapq` is 0-indexed and operates on a plain list in-place. `h[0]` is always the minimum. There is no separate heap object — the list IS the heap after `heapify` or after being built via `heappush`. The module does not support a max-heap natively; negate values to work around this.

```
After heapq.heapify([5, 3, 8, 1, 2]):

h = [1, 2, 8, 3, 5]
     ↑
   h[0] = 1 (minimum, always at root)
```

**When it matters:** Use `heapq` directly when you need fine-grained control (fixed-size heaps, custom comparators via tuples). Use `heapq.nlargest` / `heapq.nsmallest` for one-shot queries on a static collection.

---

## Core Patterns

### Min-Heap for Top-K Largest

**When to use:** You need the k largest elements from a stream or large array.
**Complexity:** O(n log k) time, O(k) space
**Problems:** Kth Largest Element in a Stream (#703), Kth Largest Element in an Array (#215), K Closest Points to Origin (#973)
**Common mistake:** Using a max-heap and pushing everything — that's O(n log n). The trick is a MIN-heap of size k: the smallest thing in the heap is the k-th largest overall, and you pop it whenever the heap grows past k.

```python
import heapq

def top_k_largest(nums, k):
    h = []
    for num in nums:
        heapq.heappush(h, num)
        if len(h) > k:
            heapq.heappop(h)   # evict the smallest — it's not top-k
    return list(h)             # everything remaining is top-k
```

### Max-Heap Simulation (Negate Values)

**When to use:** You need the largest element first, but Python only has a min-heap.
**Complexity:** O(log n) per push/pop, same as min-heap
**Problems:** Last Stone Weight (#1046), Reorganize String (#767), Longest Happy String (#1405), IPO (#502)
**Common mistake:** Forgetting to negate on the way out — `heappop` returns the negated value, so you must negate it again to get the original.

```python
import heapq

h = []
heapq.heappush(h, -val)        # push negated
max_val = -heapq.heappop(h)    # pop and negate to recover original

# Heapify a list as a max-heap:
nums = [3, 1, 4, 1, 5]
h = [-x for x in nums]
heapq.heapify(h)
largest = -heapq.heappop(h)    # 5
```

### K-Way Merge

**When to use:** You have k sorted lists and need to merge them or find the k-th smallest across all of them.
**Complexity:** O(n log k) where n is total elements across all lists
**Problems:** Find Median from Data Stream (#295) uses a related idea; general merge pattern appears in Design Twitter (#355)
**Common mistake:** Not storing the list index and element index alongside the value in the heap tuple — you need them to fetch the next element from the same list.

```python
import heapq

def k_way_merge(lists):
    h = []
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(h, (lst[0], i, 0))   # (value, list_idx, elem_idx)
    result = []
    while h:
        val, li, ei = heapq.heappop(h)
        result.append(val)
        if ei + 1 < len(lists[li]):
            heapq.heappush(h, (lists[li][ei + 1], li, ei + 1))
    return result
```

### Two-Heap Median

**When to use:** You need to find the median of a dynamic stream of numbers efficiently.
**Complexity:** O(log n) insert, O(1) query
**Problems:** Find Median from Data Stream (#295), IPO (#502)
**Common mistake:** Forgetting to rebalance after each insert. The invariant is that the max-heap (lower half) and min-heap (upper half) must differ in size by at most 1.

```python
import heapq

lo = []   # max-heap (lower half) — store negated
hi = []   # min-heap (upper half)

def add_num(num):
    heapq.heappush(lo, -num)           # always push to lower half first
    if lo and hi and (-lo[0] > hi[0]): # fix cross-over
        heapq.heappush(hi, -heapq.heappop(lo))
    if len(lo) > len(hi) + 1:         # rebalance sizes
        heapq.heappush(hi, -heapq.heappop(lo))
    elif len(hi) > len(lo):
        heapq.heappush(lo, -heapq.heappop(hi))

def find_median():
    if len(lo) > len(hi):
        return -lo[0]
    return (-lo[0] + hi[0]) / 2
```

---

## Syntax Reference

### heapq basics

```python
import heapq

h = []
heapq.heappush(h, val)      # push — O(log n)
heapq.heappop(h)            # pop smallest — O(log n)
h[0]                        # peek at smallest without removing — O(1)
heapq.heapify(lst)          # convert list to heap in-place — O(n)
heapq.heapreplace(h, val)   # pop smallest then push val — O(log n), faster than two calls
```

### Max-heap via negation

```python
heapq.heappush(h, -val)         # push negated value
max_val = -heapq.heappop(h)     # recover original by negating again
```

### Heap of tuples (custom sort key)

Python compares tuples lexicographically, so put the sort key first. This lets you store extra data alongside the priority without a custom comparator.

```python
# (priority, value) — heap orders by priority first
heapq.heappush(h, (dist, node))
dist, node = heapq.heappop(h)

# (priority, tiebreaker, value) — avoids comparison errors on non-comparable values
import itertools
counter = itertools.count()
heapq.heappush(h, (priority, next(counter), task))
```

### One-shot top-k queries

```python
heapq.nlargest(k, iterable)                        # k largest — O(n log k)
heapq.nsmallest(k, iterable)                       # k smallest — O(n log k)
heapq.nlargest(k, items, key=lambda x: x[1])       # with custom key
```

### Fixed-size heap (sliding window top-k)

```python
# Maintain exactly k elements — the heap top is the k-th largest seen so far
h = []
for val in stream:
    heapq.heappush(h, val)
    if len(h) > k:
        heapq.heappop(h)
kth_largest = h[0]   # smallest in the heap = k-th largest overall
```
