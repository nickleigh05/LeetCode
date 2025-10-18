# Heaps & Priority Queues

## What is a Heap?
A heap is a complete binary tree that satisfies the heap property. It's commonly used to implement priority queues, where elements are processed based on priority rather than insertion order.

## Heap Property

### Max Heap
Parent ≥ Children (largest element at root)
```
         50  ← Maximum element at root
        /  \
      30    40
     / \    /
   10  20  35

Property: Every parent ≥ its children
50 ≥ 30, 50 ≥ 40
30 ≥ 10, 30 ≥ 20
40 ≥ 35
```

### Min Heap
Parent ≤ Children (smallest element at root)
```
         10  ← Minimum element at root
        /  \
      20    15
     / \    /
   30  25  40

Property: Every parent ≤ its children
10 ≤ 20, 10 ≤ 15
20 ≤ 30, 20 ≤ 25
15 ≤ 40
```

## Array Representation

Heaps are efficiently stored in arrays using level-order traversal:

```
Min Heap Tree:
         10
        /  \
      20    15
     / \    /
   30  25  40

Array: [10, 20, 15, 30, 25, 40]
Index:  0   1   2   3   4   5

Parent-Child Relationships:
For node at index i:
- Left child:  2*i + 1
- Right child: 2*i + 2
- Parent:      (i - 1) // 2

Visual mapping:
Index:  0    1    2    3    4    5
      ┌────┬────┬────┬────┬────┬────┐
      │ 10 │ 20 │ 15 │ 30 │ 25 │ 40 │
      └────┴────┴────┴────┴────┴────┘
        ↑    ↑↑   ↑↑   ↑    ↑    ↑
        │   ││  ││   │    │    │
       root  children  children  child
             of 0      of 1      of 2

Example calculations:
- Index 1 (20): left = 2*1+1 = 3 (30), right = 2*1+2 = 4 (25)
- Index 3 (30): parent = (3-1)//2 = 1 (20)
```

## Heap Operations

### 1. Heapify Up (Bubble Up)

Used after insertion to maintain heap property:

```
Min Heap - Insert 5:

Step 1: Add 5 at end
         10
        /  \
      20    15
     / \    / \
   30  25  40  5   ← Insert at end

Array: [10, 20, 15, 30, 25, 40, 5]
Index:  0   1   2   3   4   5   6

Step 2: Compare with parent (15)
         10
        /  \
      20    15  ← parent(6) = (6-1)//2 = 2
     / \    / \
   30  25  40  5  ← 5 < 15, swap!

Step 3: Swap 5 and 15
         10
        /  \
      20    5   ← Swapped
     / \    / \
   30  25  40  15

Array: [10, 20, 5, 30, 25, 40, 15]

Step 4: Compare with parent (10)
         10  ← parent(2) = (2-1)//2 = 0
        /  \
      20    5  ← 5 < 10, swap!
     / \    / \
   30  25  40  15

Step 5: Swap 5 and 10
         5   ← New root (smallest)
        /  \
      20    10
     / \    / \
   30  25  40  15

Final Array: [5, 20, 10, 30, 25, 40, 15]

Time: O(log n) - height of tree
```

### 2. Heapify Down (Bubble Down)

Used after deletion to maintain heap property:

```
Min Heap - Remove root (5):

Initial:
         5
        /  \
      20    10
     / \    / \
   30  25  40  15

Array: [5, 20, 10, 30, 25, 40, 15]

Step 1: Replace root with last element
         15  ← Move last to root
        /  \
      20    10
     / \    /
   30  25  40

Array: [15, 20, 10, 30, 25, 40]

Step 2: Compare with children
         15  ← Compare with 20 and 10
        /  \
      20    10  ← Smaller child = 10

15 > 10, swap with smaller child

Step 3: Swap 15 and 10
         10  ← Swapped
        /  \
      20    15
     / \    /
   30  25  40

Step 4: Compare 15 with children
         10
        /  \
      20    15  ← Compare with 40
     / \    /
   30  25  40  ← Only one child

15 < 40, heap property satisfied ✓

Final Array: [10, 20, 15, 30, 25, 40]

Time: O(log n) - height of tree
```

### 3. Build Heap

Convert array to heap efficiently:

```
Array: [50, 30, 20, 15, 10, 8, 16]

Method: Heapify from last non-leaf node to root
Last non-leaf = (n//2 - 1) = (7//2 - 1) = 2

Initial tree (not a heap):
         50
        /  \
      30    20
     / \    / \
   15  10  8  16

Step 1: Heapify index 2 (20)
Compare 20 with children (8, 16)
Smallest = 8, swap

         50
        /  \
      30    8   ← Swapped
     / \    / \
   15  10  20  16

Step 2: Heapify index 1 (30)
Compare 30 with children (15, 10)
Smallest = 10, swap

         50
        /  \
      10    8   ← Swapped
     / \    / \
   15  30  20  16

Step 3: Heapify index 0 (50)
Compare 50 with children (10, 8)
Smallest = 8, swap

         8      ← Swapped
        /  \
      10    50
     / \    / \
   15  30  20  16

Continue heapify down for 50:
Compare 50 with children (20, 16)
Smallest = 16, swap

         8
        /  \
      10    16   ← Swapped
     / \    / \
   15  30  20  50

Final Min Heap:
         8
        /  \
      10    16
     / \    / \
   15  30  20  50

Array: [8, 10, 16, 15, 30, 20, 50]

Time: O(n) - better than n insertions O(n log n)
Space: O(1) - in-place
```

## Priority Queue

Priority Queue is an abstract data type, usually implemented with a heap:

```
Operations:
- push(element, priority): Add element
- pop(): Remove highest priority
- peek(): View highest priority
- size(): Get count

Example: Task Scheduler (Min Heap by priority)

Tasks: [
  (Task A, priority 3),
  (Task B, priority 1),
  (Task C, priority 2)
]

Min Heap (by priority):
         1(B)  ← Highest priority
        /  \
      3(A)  2(C)

Operations:
1. peek() → Task B (priority 1)
2. pop()  → Remove B
   Heap:
         2(C)
        /
      3(A)

3. push(Task D, priority 0)
   Heap:
         0(D)  ← New highest
        /  \
      3(A)  2(C)

Process order: B, D, C, A
```

## Common Use Cases

### 1. K Largest/Smallest Elements

```
Find K largest in [3, 1, 5, 12, 2, 11], K = 3

Use Min Heap of size K:

Step 1: Add first 3 elements
Heap: [1, 3, 5]
         1
        / \
       3   5

Step 2: Add 12
12 > 1 (root), replace 1 with 12
         3
        / \
       5  12
After heapify: [3, 5, 12]

Step 3: Add 2
2 < 3 (root), ignore

Step 4: Add 11
11 > 3 (root), replace 3 with 11
         5
        / \
      11  12
After heapify: [5, 11, 12]

Result: [5, 11, 12]

Time: O(n log k)
Space: O(k)
```

### 2. Merge K Sorted Lists

```
Lists:
L1: 1 → 4 → 7
L2: 2 → 5 → 8
L3: 3 → 6 → 9

Min Heap approach:

Step 1: Add first element of each list
Heap: [(1, L1), (2, L2), (3, L3)]
         1
        / \
       2   3

Step 2: Pop minimum (1), add to result
Result: [1]
Add next from L1 (4)
Heap: [(2, L2), (3, L3), (4, L1)]
         2
        / \
       3   4

Step 3: Pop minimum (2), add to result
Result: [1, 2]
Add next from L2 (5)
Heap: [(3, L3), (4, L1), (5, L2)]
         3
        / \
       4   5

Continue...
Result: [1, 2, 3, 4, 5, 6, 7, 8, 9]

Time: O(n log k) where k = number of lists
Space: O(k) for heap
```

### 3. Running Median

```
Stream: [5, 15, 1, 3]

Use two heaps:
- Max Heap (left half): stores smaller values
- Min Heap (right half): stores larger values

Median is at top of heaps

Step 1: Add 5
MaxHeap: [5]
MinHeap: []
Median: 5

Visual:
MaxHeap │ MinHeap
   5    │   -

Step 2: Add 15
MaxHeap: [5]
MinHeap: [15]
Median: (5 + 15) / 2 = 10

Visual:
MaxHeap │ MinHeap
   5    │   15

Step 3: Add 1
1 < 5, add to MaxHeap
MaxHeap: [5, 1]
MinHeap: [15]
Rebalance: Move 5 to MinHeap
MaxHeap: [1]
MinHeap: [5, 15]
Median: 5

Visual:
MaxHeap │ MinHeap
   1    │   5
        │  / \
        │ 15  -

Step 4: Add 3
3 > 1, but MinHeap needs balancing
Add to MaxHeap: [3, 1]
MaxHeap: [3, 1]
MinHeap: [5, 15]
Median: (3 + 5) / 2 = 4

Final:
MaxHeap │ MinHeap
   3    │   5
  /     │  /
 1      │ 15

Property maintained:
- MaxHeap size ≈ MinHeap size
- All MaxHeap elements ≤ all MinHeap elements
- Median = top(s) of heap(s)

Time: O(log n) per insertion
Space: O(n)
```

### 4. Dijkstra's Algorithm

```
Graph:
    A --1-- B
    |       |
    4       2
    |       |
    C --1-- D

Find shortest path from A to all nodes:

Min Heap: (distance, node)

Step 1: Start with A
Heap: [(0, A)]
Distances: {A: 0}

Step 2: Pop (0, A), explore neighbors
B: 0 + 1 = 1
C: 0 + 4 = 4
Heap: [(1, B), (4, C)]
Distances: {A: 0, B: 1, C: 4}

Step 3: Pop (1, B), explore neighbors
D: 1 + 2 = 3
Heap: [(3, D), (4, C)]
Distances: {A: 0, B: 1, C: 4, D: 3}

Step 4: Pop (3, D), explore neighbors
C: 3 + 1 = 4 (not better than 4)
Heap: [(4, C)]

Step 5: Pop (4, C), done

Final Distances: {A: 0, B: 1, C: 4, D: 3}
Shortest paths from A

Time: O((V + E) log V)
Space: O(V)
```

## Heap vs Other Structures

```
Operation comparison:

                    Heap    Sorted Array  BST
Insert:            O(log n)    O(n)      O(log n)
Delete Max/Min:    O(log n)    O(1)      O(log n)
Get Max/Min:       O(1)        O(1)      O(log n)
Search:            O(n)        O(log n)  O(log n)
Build:             O(n)        O(n log n) O(n log n)

Heap advantages:
✓ Fast insertion
✓ Fast min/max access
✓ Efficient build (O(n))
✓ Good for priority queue

Heap disadvantages:
✗ Slow search
✗ Not sorted (only partial order)
✗ No range queries
```

## Advanced Heap Variants

### 1. Fibonacci Heap

```
Lazy merging for better amortized complexity:

Operations:
- Insert: O(1) amortized
- Decrease Key: O(1) amortized
- Delete Min: O(log n) amortized

Structure: Forest of trees

Used in:
- Dijkstra's algorithm optimization
- Prim's MST algorithm
```

### 2. Binomial Heap

```
Collection of binomial trees:

Binomial Tree B₀: •

Binomial Tree B₁: •
                  |
                  •

Binomial Tree B₂:   •
                   /|\
                  • • •
                  |
                  •

Properties:
- Merge: O(log n)
- Insert: O(log n) worst, O(1) amortized
- Used when frequent merging needed
```

### 3. D-ary Heap

```
Each node has d children (not just 2):

Binary Heap (d=2):
         1
        / \
       2   3
      / \
     4   5

4-ary Heap (d=4):
         1
      /  | |  \
     2   3 4   5
    /|\
   6 7 8

Trade-offs:
- Shallower tree: Better cache performance
- More children: Slower heapify down
- Optimal d depends on use case

Best for:
- Decrease-key heavy workloads
- Cache-sensitive applications
```

## Time and Space Complexity

### Time Complexity Summary
| Operation | Min/Max Heap | Binary Heap |
|-----------|-------------|-------------|
| Insert | O(log n) | O(log n) |
| Delete Min/Max | O(log n) | O(log n) |
| Peek Min/Max | O(1) | O(1) |
| Heapify | O(log n) | O(log n) |
| Build Heap | O(n) | O(n) |
| Heap Sort | O(n log n) | O(n log n) |

### Space Complexity
- Array-based: O(n)
- No extra space for pointers
- Recursion stack: O(log n) for heapify

## Python Implementation

```python
import heapq  # Python's built-in heap (min heap)

class MinHeap:
    def __init__(self):
        self.heap = []

    def push(self, val):
        """
        Insert element.
        Time: O(log n), Space: O(1)
        """
        heapq.heappush(self.heap, val)

    def pop(self):
        """
        Remove and return minimum.
        Time: O(log n), Space: O(1)
        """
        if not self.heap:
            return None
        return heapq.heappop(self.heap)

    def peek(self):
        """
        View minimum without removing.
        Time: O(1), Space: O(1)
        """
        return self.heap[0] if self.heap else None

    def size(self):
        """Get heap size."""
        return len(self.heap)


class MaxHeap:
    """Max heap using min heap (negate values)"""
    def __init__(self):
        self.heap = []

    def push(self, val):
        heapq.heappush(self.heap, -val)  # Negate for max

    def pop(self):
        if not self.heap:
            return None
        return -heapq.heappop(self.heap)  # Negate back

    def peek(self):
        return -self.heap[0] if self.heap else None


# Manual heap implementation
class Heap:
    def __init__(self, max_heap=False):
        self.heap = []
        self.max_heap = max_heap

    def _compare(self, a, b):
        """Compare based on heap type."""
        if self.max_heap:
            return a > b
        return a < b

    def _parent(self, i):
        return (i - 1) // 2

    def _left_child(self, i):
        return 2 * i + 1

    def _right_child(self, i):
        return 2 * i + 2

    def _heapify_up(self, i):
        """Bubble up element at index i."""
        parent = self._parent(i)
        if i > 0 and self._compare(self.heap[i], self.heap[parent]):
            self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
            self._heapify_up(parent)

    def _heapify_down(self, i):
        """Bubble down element at index i."""
        smallest = i
        left = self._left_child(i)
        right = self._right_child(i)

        if left < len(self.heap) and self._compare(self.heap[left], self.heap[smallest]):
            smallest = left

        if right < len(self.heap) and self._compare(self.heap[right], self.heap[smallest]):
            smallest = right

        if smallest != i:
            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            self._heapify_down(smallest)

    def insert(self, val):
        """Insert element."""
        self.heap.append(val)
        self._heapify_up(len(self.heap) - 1)

    def extract(self):
        """Remove and return root."""
        if not self.heap:
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return root

    def build_heap(self, arr):
        """Build heap from array in O(n)."""
        self.heap = arr[:]
        # Start from last non-leaf node
        for i in range(len(self.heap) // 2 - 1, -1, -1):
            self._heapify_down(i)


# Priority Queue implementation
class PriorityQueue:
    def __init__(self):
        self.heap = []

    def push(self, item, priority):
        """
        Add item with priority.
        Lower priority number = higher priority
        """
        heapq.heappush(self.heap, (priority, item))

    def pop(self):
        """Remove highest priority item."""
        if not self.heap:
            return None
        priority, item = heapq.heappop(self.heap)
        return item

    def peek(self):
        """View highest priority without removing."""
        if not self.heap:
            return None
        return self.heap[0][1]


# Common heap problems

def kth_largest(nums, k):
    """
    Find kth largest element.
    Time: O(n log k), Space: O(k)
    """
    heap = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]


def merge_k_sorted_lists(lists):
    """
    Merge k sorted lists.
    Time: O(n log k), Space: O(k)
    """
    heap = []
    result = []

    # Add first element of each list
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))

    while heap:
        val, list_idx, elem_idx = heapq.heappop(heap)
        result.append(val)

        # Add next element from same list
        if elem_idx + 1 < len(lists[list_idx]):
            next_val = lists[list_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))

    return result


class MedianFinder:
    """
    Find median from data stream.
    Time: O(log n) insert, O(1) find
    Space: O(n)
    """
    def __init__(self):
        self.small = []  # Max heap (left half)
        self.large = []  # Min heap (right half)

    def addNum(self, num):
        # Add to max heap (negate for max)
        heapq.heappush(self.small, -num)

        # Balance: move largest from small to large
        if self.small and self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)

        # Maintain size property
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)

        if len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

    def findMedian(self):
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2.0


def top_k_frequent(nums, k):
    """
    Find k most frequent elements.
    Time: O(n log k), Space: O(n)
    """
    from collections import Counter

    count = Counter(nums)
    # Min heap of size k
    heap = []

    for num, freq in count.items():
        heapq.heappush(heap, (freq, num))
        if len(heap) > k:
            heapq.heappop(heap)

    return [num for freq, num in heap]


def meeting_rooms_ii(intervals):
    """
    Minimum meeting rooms needed.
    Time: O(n log n), Space: O(n)
    """
    if not intervals:
        return 0

    intervals.sort(key=lambda x: x[0])
    heap = []  # End times

    for start, end in intervals:
        # Remove finished meetings
        if heap and heap[0] <= start:
            heapq.heappop(heap)
        heapq.heappush(heap, end)

    return len(heap)


# Heap sort
def heap_sort(arr):
    """
    Sort using heap.
    Time: O(n log n), Space: O(1) in-place
    """
    n = len(arr)

    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify_down(arr, n, i)

    # Extract elements
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify_down(arr, i, 0)

    return arr

def heapify_down(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify_down(arr, n, largest)
```

## Key Takeaways

1. **Structure**: Complete binary tree with heap property
2. **Types**:
   - Min Heap: Parent ≤ Children
   - Max Heap: Parent ≥ Children

3. **Array Representation**:
   - Parent: (i-1)//2
   - Left child: 2i+1
   - Right child: 2i+2

4. **Core Operations**: O(log n)
   - Insert (heapify up)
   - Delete (heapify down)
   - Build heap: O(n)

5. **Use Cases**:
   - Priority queues
   - K largest/smallest
   - Merge sorted lists
   - Median finding
   - Dijkstra's algorithm
   - Task scheduling

6. **Python heapq Module**:
   - Min heap by default
   - Max heap: negate values
   - Priority queue: use tuples

7. **Common Patterns**:
   - K elements: heap of size K
   - Streaming data: dual heap (median)
   - Merge: heap of iterators
   - Scheduling: min heap by time

8. **When to Use**:
   - Need min/max quickly
   - Priority-based processing
   - K-way merging
   - Streaming median/percentiles

9. **When NOT to Use**:
   - Need sorted order (use sorting)
   - Random access (use array)
   - Range queries (use segment tree)
   - All elements matter equally (use queue)
