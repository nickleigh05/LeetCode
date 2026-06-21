# Algorithms Reference

A complete reference for every major algorithm used in LeetCode and technical interviews. Each section includes a visual trace, complexity analysis, recognition signals, a Python template, and links to the data structures and patterns it connects to.

---

## Table of Contents

| # | Algorithm | Jump To |
|---|-----------|---------|
| 1 | Binary Search | [→ Binary Search](#binary-search) |
| 2 | Merge Sort | [→ Merge Sort](#merge-sort) |
| 3 | Quick Sort | [→ Quick Sort](#quick-sort) |
| 4 | Breadth-First Search | [→ Breadth-First Search](#breadth-first-search) |
| 5 | Depth-First Search | [→ Depth-First Search](#depth-first-search) |
| 6 | Dijkstra's Algorithm | [→ Dijkstra's Algorithm](#dijkstras-algorithm) |
| 7 | Topological Sort | [→ Topological Sort](#topological-sort) |
| 8 | Dynamic Programming | [→ Dynamic Programming](#dynamic-programming) |
| 9 | Backtracking | [→ Backtracking](#backtracking) |
| 10 | Greedy | [→ Greedy](#greedy) |
| 11 | Bit Manipulation | [→ Bit Manipulation](#bit-manipulation) |

**Other files:** [datastructures.md](datastructures.md) · [patterns.md](../skeletons/patterns.md) · [templates/](../skeletons/templates/) · [lists/](../../lists/)

---

## Binary Search

```
  Sorted array: [1, 3, 5, 7, 9, 11, 13, 15]
  Target: 7

  Step 1:  lo=0, hi=7, mid=3 → arr[3]=7 == target ✓

  Step 2 (if target=11):
           lo=0  hi=7  mid=3  arr[3]=7  < 11 → lo=4
           lo=4  hi=7  mid=5  arr[5]=11 == 11 ✓

  Step 3 (if target=6, not present):
           lo=0  hi=7  mid=3  arr[3]=7  > 6 → hi=2
           lo=0  hi=2  mid=1  arr[1]=3  < 6 → lo=2
           lo=2  hi=2  mid=2  arr[2]=5  < 6 → lo=3
           lo=3  hi=2  → lo > hi, STOP → not found

  Search space halves each step → O(log n)
```

**What it does:** Finds a target in a sorted array by repeatedly halving the search space. Requires the array to be sorted (or the search space to be monotone).

**Recognition signals:**
- Array is sorted, or can be sorted
- "Find if X exists", "find leftmost/rightmost position"
- "Minimum/maximum value such that condition holds" → Binary Search on Answer
- O(log n) requirement
- Rotated sorted array

**Variants:**

| Variant | lo/hi adjustment |
|---------|-----------------|
| Standard (find exact) | `lo = mid+1` or `hi = mid-1` |
| Leftmost occurrence | `hi = mid` when `arr[mid] >= target` |
| Rightmost occurrence | `lo = mid` when `arr[mid] <= target` |
| Rotated array | check which half is sorted, adjust accordingly |

**Python:**
```python
# Standard binary search
def binary_search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2   # avoids overflow (matters in other langs)
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

# Find leftmost position (first occurrence)
def leftmost(nums, target):
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid          # don't exclude mid!
    return lo  # lo == hi == insertion point

# Python built-in
import bisect
bisect.bisect_left(nums, target)   # leftmost insertion point
bisect.bisect_right(nums, target)  # rightmost insertion point
```

**Complexity:**

| | Time | Space |
|-|------|-------|
| Standard | O(log n) | O(1) |

**Data structures it uses:**
[Array](datastructures.md#array) · [Binary Search Tree](datastructures.md#binary-search-tree)

**Patterns it enables:**
[Binary Search on Answer](../skeletons/patterns.md#binary-search-on-answer)

---

## Merge Sort

```
  Array: [5, 2, 8, 1, 9, 3]

  Divide:
  [5,2,8,1,9,3]
  [5,2,8]  [1,9,3]
  [5,2] [8]  [1,9] [3]
  [5][2]      [1][9]

  Conquer (merge sorted halves):
  [2,5] [8]  [1,9] [3]
  [2,5,8]  [1,3,9]
  [1,2,3,5,8,9]  ✓

  Merge step (two sorted arrays → one sorted):
  L=[2,5,8]  R=[1,3,9]
  Compare heads:  1<2 → take 1
  L=[2,5,8]  R=[3,9]
  Compare heads:  2<3 → take 2
  ...and so on
```

**What it does:** Recursively divides the array in half, sorts each half, then merges the sorted halves. Guaranteed O(n log n) in all cases and is stable (equal elements maintain relative order).

**Recognition signals:**
- Need stable sort
- Counting inversions
- Sorting linked lists (merge step is natural for linked lists)
- Merge K sorted lists / arrays
- External sorting (data too large for memory)

**Python:**
```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left  = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# Count inversions (during merge, count how many swaps needed)
inversions = 0
def merge_count(arr):
    global inversions
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left  = merge_count(arr[:mid])
    right = merge_count(arr[mid:])
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
            inversions += len(left) - i   # all remaining left elements > right[j]
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged
```

**Complexity:**

| Case | Time | Space |
|------|------|-------|
| Best | O(n log n) | O(n) |
| Average | O(n log n) | O(n) |
| Worst | O(n log n) | O(n) |

**Data structures it uses:**
[Array](datastructures.md#array) · [Linked List](datastructures.md#linked-list) (natural merge step)

**Patterns it enables:**
[Merge Intervals](../skeletons/patterns.md#merge-intervals) (sort + process) · [Top K Elements](../skeletons/patterns.md#top-k-elements) (merge K sorted)

---

## Quick Sort

```
  Array: [3, 6, 8, 10, 1, 2, 1]
  Pivot = last element = 1

  Partition around pivot 1:
  i = -1 (boundary of elements ≤ pivot)
  j scans left to right:
    j=0: 3 > 1, skip
    j=1: 6 > 1, skip
    j=2: 8 > 1, skip
    j=3: 10 > 1, skip
    j=4: 1 ≤ 1, i=0, swap arr[0] and arr[4] → [1,6,8,10,3,2,1]
    j=5: 2 > 1, skip
  Swap pivot (arr[6]) with arr[i+1=1]:    → [1,1,8,10,3,2,6]
                                                 ↑
                                           pivot in final position

  Recurse on [1] and [8,10,3,2,6]

  QuickSelect (find kth smallest without full sort):
  Only recurse on the side containing index k → O(n) average
```

**What it does:** Picks a pivot, partitions the array so all elements less than the pivot come before it and all greater after, then recurses on both halves. In-place and cache-friendly. QuickSelect finds the kth element in O(n) average.

**Recognition signals:**
- In-place sort needed (O(1) extra space excluding recursion)
- Kth largest/smallest element (QuickSelect variant)
- When average-case O(n log n) is acceptable but worst-case O(n²) must be avoided by random pivot

**Python:**
```python
import random

def quick_sort(arr, lo, hi):
    if lo < hi:
        p = partition(arr, lo, hi)
        quick_sort(arr, lo, p - 1)
        quick_sort(arr, p + 1, hi)

def partition(arr, lo, hi):
    pivot_idx = random.randint(lo, hi)
    arr[pivot_idx], arr[hi] = arr[hi], arr[pivot_idx]  # move pivot to end
    pivot = arr[hi]
    i = lo - 1
    for j in range(lo, hi):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i+1], arr[hi] = arr[hi], arr[i+1]
    return i + 1

# QuickSelect: kth smallest (0-indexed k)
def quick_select(arr, lo, hi, k):
    if lo == hi:
        return arr[lo]
    p = partition(arr, lo, hi)
    if p == k:
        return arr[p]
    elif k < p:
        return quick_select(arr, lo, p - 1, k)
    else:
        return quick_select(arr, p + 1, hi, k)
```

**Complexity:**

| Case | Time | Space |
|------|------|-------|
| Best / Average | O(n log n) | O(log n) stack |
| Worst (sorted + bad pivot) | O(n²) | O(n) stack |
| QuickSelect avg | O(n) | O(log n) |

**Data structures it uses:**
[Array](datastructures.md#array)

**Patterns it enables:**
[Top K Elements](../skeletons/patterns.md#top-k-elements) (QuickSelect alternative)

---

## Breadth-First Search

```
  Graph/Tree:          BFS order (starting from A):
      A                Level 0: A
     / \               Level 1: B, C
    B   C              Level 2: D, E, F
   / \   \
  D   E   F

  Queue evolution:
  Start:  [A]
  Pop A:  process A, enqueue B, C  → [B, C]
  Pop B:  process B, enqueue D, E  → [C, D, E]
  Pop C:  process C, enqueue F     → [D, E, F]
  Pop D:  process D (leaf)         → [E, F]
  Pop E:  process E (leaf)         → [F]
  Pop F:  process F (leaf)         → []

  BFS guarantees: first time you reach a node = shortest path
  (in unweighted graphs)
```

**What it does:** Explores all neighbors of the current node before moving deeper. Uses a queue (FIFO). Guarantees the shortest path in an unweighted graph.

**Recognition signals:**
- Shortest path in an unweighted graph or grid
- Level-order tree traversal
- "Minimum steps to reach X"
- Multi-source BFS (start with multiple nodes simultaneously)
- Check if a graph is bipartite

**Python:**
```python
from collections import deque

# Graph BFS (shortest path / connected components)
def bfs(graph, start):
    visited = {start}
    q = deque([start])
    distance = {start: 0}

    while q:
        node = q.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                distance[neighbor] = distance[node] + 1
                q.append(neighbor)
    return distance

# Grid BFS (shortest path in 2D grid)
def bfs_grid(grid, start_r, start_c):
    rows, cols = len(grid), len(grid[0])
    q = deque([(start_r, start_c, 0)])  # (row, col, steps)
    visited = {(start_r, start_c)}
    dirs = [(0,1),(0,-1),(1,0),(-1,0)]

    while q:
        r, c, steps = q.popleft()
        for dr, dc in dirs:
            nr, nc = r+dr, c+dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr,nc) not in visited:
                if grid[nr][nc] == 0:  # passable
                    visited.add((nr, nc))
                    q.append((nr, nc, steps + 1))

# Multi-source BFS (e.g., rotting oranges: all rotten start at once)
q = deque()
for r in range(rows):
    for c in range(cols):
        if grid[r][c] == ROTTEN:
            q.append((r, c, 0))
```

**Complexity:**

| | Time | Space |
|-|------|-------|
| Graph | O(V + E) | O(V) |
| Grid (r×c) | O(r·c) | O(r·c) |

**Data structures it uses:**
[Queue and Deque](datastructures.md#queue-and-deque) · [Graph](datastructures.md#graph) · [Binary Tree](datastructures.md#binary-tree)

**Patterns it enables:**
[BFS on Grid and Tree](../skeletons/patterns.md#bfs-on-grid-and-tree) · [Topological Sort](../skeletons/patterns.md#topological-sort) (Kahn's)

---

## Depth-First Search

```
  Graph:    DFS from A (pre-order):
    A         Visit A → push B, C
   / \        Visit B → push D, E
  B   C       Visit D (leaf, backtrack)
 / \   \      Visit E (leaf, backtrack)
D   E   F     Visit C → push F
              Visit F (leaf, backtrack)
  DFS order: A, B, D, E, C, F

  Call stack visualization:
  dfs(A)
   └─ dfs(B)
       ├─ dfs(D)   ← returns
       └─ dfs(E)   ← returns
   └─ dfs(C)
       └─ dfs(F)   ← returns

  Cycle detection (directed graph):
  WHITE = unvisited, GRAY = in current path, BLACK = done
  If you reach a GRAY node → cycle!
```

**What it does:** Explores as far as possible along each branch before backtracking. Can be implemented recursively (using the call stack) or iteratively (with an explicit stack). Foundational for almost all tree problems.

**Recognition signals:**
- Exploring all paths (permutations, combinations, subsets)
- Connected components in a graph
- Cycle detection
- Topological sort (DFS-based)
- Tree traversals (inorder, preorder, postorder)
- Path sum / max path problems on trees

**Python:**
```python
# Recursive DFS (graph)
def dfs(node, graph, visited):
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(neighbor, graph, visited)

# Iterative DFS (graph) — use when recursion depth is large
def dfs_iter(start, graph):
    visited = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                stack.append(neighbor)

# Tree DFS (recursive) — inorder
def inorder(root):
    if not root: return
    inorder(root.left)
    process(root.val)      # swap order for pre/postorder
    inorder(root.right)

# Grid DFS (flood fill / number of islands)
def dfs_grid(grid, r, c, visited):
    if r < 0 or r >= len(grid) or c < 0 or c >= len(grid[0]):
        return
    if (r, c) in visited or grid[r][c] == 0:
        return
    visited.add((r, c))
    for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
        dfs_grid(grid, r+dr, c+dc, visited)
```

**Complexity:**

| | Time | Space |
|-|------|-------|
| Graph | O(V + E) | O(V) call stack |
| Grid | O(r·c) | O(r·c) |
| Tree | O(n) | O(h) where h = height |

**Data structures it uses:**
[Stack](datastructures.md#stack) · [Graph](datastructures.md#graph) · [Binary Tree](datastructures.md#binary-tree) · [Trie](datastructures.md#trie)

**Patterns it enables:**
[DFS and Backtracking](../skeletons/patterns.md#dfs-and-backtracking) · [Trie Search](../skeletons/patterns.md#trie-search) · [Topological Sort](../skeletons/patterns.md#topological-sort)

---

## Dijkstras Algorithm

```
  Weighted graph (all non-negative weights):
       A
     2/ \5
     B   C
    1\   /3
       D

  Start at A. Min-heap: [(cost, node)]
  Init:  heap=[(0,A)],  dist={A:0, B:∞, C:∞, D:∞}

  Pop (0,A):  update neighbors:
    B: 0+2=2 < ∞ → dist[B]=2, push (2,B)
    C: 0+5=5 < ∞ → dist[C]=5, push (5,C)
  heap=[(2,B),(5,C)]

  Pop (2,B):  update neighbors:
    D: 2+1=3 < ∞ → dist[D]=3, push (3,D)
  heap=[(3,D),(5,C)]

  Pop (3,D):  update neighbors:
    C: 3+3=6 > 5 → no update
  heap=[(5,C)]

  Pop (5,C):  done
  Final: dist={A:0, B:2, C:5, D:3}
```

**What it does:** Finds the shortest path from a source to all other nodes in a weighted graph with non-negative edge weights. Uses a min-heap to always process the cheapest unvisited node next.

**Recognition signals:**
- Shortest path in a weighted graph
- Minimum cost to reach a destination
- Graph has non-negative edge weights
- "Network delay time", "cheapest flights", "path with minimum effort"

**Limitation:** Does NOT work with negative edge weights (use Bellman-Ford instead).

**Python:**
```python
import heapq
from collections import defaultdict

def dijkstra(graph, start):
    # graph[u] = [(weight, v), ...]
    dist = defaultdict(lambda: float('inf'))
    dist[start] = 0
    heap = [(0, start)]   # (cost, node)

    while heap:
        cost, node = heapq.heappop(heap)
        if cost > dist[node]:
            continue       # stale entry, skip
        for weight, neighbor in graph[node]:
            new_cost = cost + weight
            if new_cost < dist[neighbor]:
                dist[neighbor] = new_cost
                heapq.heappush(heap, (new_cost, neighbor))

    return dist

# Grid variant: min cost path
def dijkstra_grid(grid):
    rows, cols = len(grid), len(grid[0])
    dist = [[float('inf')] * cols for _ in range(rows)]
    dist[0][0] = grid[0][0]
    heap = [(grid[0][0], 0, 0)]

    while heap:
        cost, r, c = heapq.heappop(heap)
        if cost > dist[r][c]: continue
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < rows and 0 <= nc < cols:
                nc_cost = cost + grid[nr][nc]
                if nc_cost < dist[nr][nc]:
                    dist[nr][nc] = nc_cost
                    heapq.heappush(heap, (nc_cost, nr, nc))
    return dist[rows-1][cols-1]
```

**Complexity:**

| | Time | Space |
|-|------|-------|
| With binary heap | O((V + E) log V) | O(V) |

**Data structures it uses:**
[Heap and Priority Queue](datastructures.md#heap-and-priority-queue) · [Graph](datastructures.md#graph) · [Hash Map and Hash Set](datastructures.md#hash-map-and-hash-set)

**Patterns it enables:**
[BFS on Grid and Tree](../skeletons/patterns.md#bfs-on-grid-and-tree) (weighted variant) · [Top K Elements](../skeletons/patterns.md#top-k-elements) (heap usage)

---

## Topological Sort

```
  DAG (Directed Acyclic Graph):
  Courses: 0→2, 1→2, 1→3, 2→4, 3→4

  0 ──→ 2 ──→ 4
  1 ──→ 3 ──↗

  In-degrees: {0:0, 1:0, 2:2, 3:1, 4:2}

  Kahn's BFS method:
  Queue starts with all in-degree=0: [0, 1]
  Pop 0: process, decrement neighbors → 2's in-degree: 2→1
  Pop 1: process, decrement 2→0, 3→0 → queue: [2, 3]
  Pop 2: process, decrement 4→1
  Pop 3: process, decrement 4→0 → queue: [4]
  Pop 4: process

  Order: [0, 1, 2, 3, 4]  ← one valid topological ordering
  If queue empties before all nodes processed → CYCLE exists!
```

**What it does:** Produces a linear ordering of vertices in a Directed Acyclic Graph (DAG) such that for every directed edge u→v, u appears before v. Two methods: Kahn's (BFS) and DFS-based.

**Recognition signals:**
- Task scheduling with prerequisites
- Course schedule (must take A before B)
- Build order (dependencies)
- Detecting cycles in directed graphs
- Any "ordering" problem with directed constraints

**Python:**
```python
from collections import defaultdict, deque

# Kahn's Algorithm (BFS) — detects cycle if output length < n
def topo_sort_bfs(n, prerequisites):
    graph = defaultdict(list)
    in_degree = [0] * n

    for a, b in prerequisites:  # b → a (must take b before a)
        graph[b].append(a)
        in_degree[a] += 1

    queue = deque([i for i in range(n) if in_degree[i] == 0])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return order if len(order) == n else []   # [] if cycle

# DFS-based Topological Sort
def topo_sort_dfs(n, graph):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n
    result = []
    has_cycle = [False]

    def dfs(node):
        if has_cycle[0]: return
        color[node] = GRAY
        for neighbor in graph[node]:
            if color[neighbor] == GRAY:
                has_cycle[0] = True; return
            if color[neighbor] == WHITE:
                dfs(neighbor)
        color[node] = BLACK
        result.append(node)   # add to result AFTER processing all neighbors

    for i in range(n):
        if color[i] == WHITE:
            dfs(i)

    return [] if has_cycle[0] else result[::-1]
```

**Complexity:**

| | Time | Space |
|-|------|-------|
| Kahn's BFS | O(V + E) | O(V + E) |
| DFS | O(V + E) | O(V) |

**Data structures it uses:**
[Graph](datastructures.md#graph) · [Queue and Deque](datastructures.md#queue-and-deque) · [Stack](datastructures.md#stack) (DFS version)

**Patterns it enables:**
[Topological Sort](../skeletons/patterns.md#topological-sort)

---

## Dynamic Programming

```
  Fibonacci with memoization (top-down):
  fib(5)
  ├─ fib(4)
  │   ├─ fib(3)
  │   │   ├─ fib(2) = 1  ← cached
  │   │   └─ fib(1) = 1
  │   └─ fib(2) = 1  ← use cache, don't recompute!
  └─ fib(3) = 2  ← use cache!

  Fibonacci with tabulation (bottom-up):
  dp[0]=0, dp[1]=1
  dp[2] = dp[1]+dp[0] = 1
  dp[3] = dp[2]+dp[1] = 2
  dp[4] = dp[3]+dp[2] = 3
  dp[5] = dp[4]+dp[3] = 5

  2D DP — Longest Common Subsequence ("abcde", "ace"):
       "" a  c  e
  ""  [ 0, 0, 0, 0 ]
  a   [ 0, 1, 1, 1 ]
  b   [ 0, 1, 1, 1 ]
  c   [ 0, 1, 2, 2 ]
  d   [ 0, 1, 2, 2 ]
  e   [ 0, 1, 2, 3 ] ← answer: 3 ("ace")
```

**What it does:** Solves problems by breaking them into overlapping subproblems and storing results to avoid recomputation. Applicable when the problem has **optimal substructure** and **overlapping subproblems**.

**Recognition signals:**
- "How many ways…" → count DP
- "Minimum/maximum cost/steps…" → optimization DP
- "Can we reach / is it possible…" → boolean DP
- Decision at each step: include/exclude, take/skip
- Problem can be defined recursively with a base case

**Two approaches:**

| | Top-Down (Memoization) | Bottom-Up (Tabulation) |
|-|----------------------|----------------------|
| Style | Recursive + cache | Iterative + array |
| Space | O(n) + call stack | O(n) or O(1) optimized |
| Code | More natural | More efficient |
| When | Complex state transitions | When you know the order |

**Common DP families:**
- **1D DP**: Climbing Stairs, House Robber, Coin Change, LIS
- **2D DP**: LCS, Edit Distance, Unique Paths, Knapsack
- **Interval DP**: Burst Balloons, Matrix Chain Multiplication
- **Tree DP**: Max path sum, diameter

**Python:**
```python
# Top-Down Memoization template
from functools import lru_cache

@lru_cache(maxsize=None)
def dp(state):
    # base case
    if state == base:
        return base_value
    # recursive case
    return min/max/sum(dp(next_state) for next_state in transitions(state))

# Bottom-Up Tabulation template (1D)
def solve(n):
    dp = [0] * (n + 1)
    dp[0] = base_case_0
    dp[1] = base_case_1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]   # recurrence relation
    return dp[n]

# Bottom-Up 2D DP template (LCS)
def lcs(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n+1) for _ in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]

# Coin Change (unbounded knapsack style)
def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1
```

**Complexity:** Varies — typically O(n), O(n²), or O(n·m) time and space, often reducible with space optimization.

**Data structures it uses:**
[Array](datastructures.md#array) · [Hash Map and Hash Set](datastructures.md#hash-map-and-hash-set) (memoization)

**Patterns it enables:**
[Dynamic Programming](../skeletons/patterns.md#dynamic-programming)

---

## Backtracking

```
  Generate all subsets of [1, 2, 3]:

  dfs(index=0, current=[])
  ├─ skip 1: dfs(1, [])
  │   ├─ skip 2: dfs(2, [])
  │   │   ├─ skip 3: dfs(3, [])   → add []
  │   │   └─ take 3: dfs(3, [3]) → add [3]
  │   └─ take 2: dfs(2, [2])
  │       ├─ skip 3: dfs(3, [2]) → add [2]
  │       └─ take 3: dfs(3,[2,3])→ add [2,3]
  └─ take 1: dfs(1, [1])
      └─ ... (same pattern)

  Result: [], [3], [2], [2,3], [1], [1,3], [1,2], [1,2,3]

  Pruning: if adding current element already exceeds target sum,
  stop exploring that branch → prune!
```

**What it does:** Systematically explores all possible solutions by building candidates incrementally and abandoning ("backtracking") a candidate as soon as it cannot lead to a valid solution.

**Recognition signals:**
- "Find all combinations/permutations/subsets"
- "Can we construct X?" (word break, partition)
- N-Queens, Sudoku solver
- Decision at each step: choose or skip

**Key insight:** Backtracking = DFS on the decision tree + pruning invalid branches early.

**Python:**
```python
# Template: Subsets / Combinations
def backtrack(start, current, result, nums):
    result.append(current[:])   # save a copy of current state
    for i in range(start, len(nums)):
        current.append(nums[i])          # choose
        backtrack(i + 1, current, result, nums)  # explore
        current.pop()                    # unchoose (backtrack)

# Template: Permutations
def permutations(nums):
    result = []
    def bt(current, remaining):
        if not remaining:
            result.append(current[:])
            return
        for i, num in enumerate(remaining):
            current.append(num)
            bt(current, remaining[:i] + remaining[i+1:])
            current.pop()
    bt([], nums)
    return result

# Template: Combination Sum (elements can repeat)
def combination_sum(candidates, target):
    result = []
    def bt(start, current, remaining):
        if remaining == 0:
            result.append(current[:]); return
        if remaining < 0:
            return           # prune!
        for i in range(start, len(candidates)):
            current.append(candidates[i])
            bt(i, current, remaining - candidates[i])  # i, not i+1 (can reuse)
            current.pop()
    bt(0, [], target)
    return result
```

**Complexity:** Exponential in the worst case — O(2^n) for subsets, O(n!) for permutations. Pruning can dramatically reduce actual runtime.

**Data structures it uses:**
[Stack](datastructures.md#stack) (call stack) · [Array](datastructures.md#array) · [Hash Map and Hash Set](datastructures.md#hash-map-and-hash-set) (for visited/used tracking)

**Patterns it enables:**
[DFS and Backtracking](../skeletons/patterns.md#dfs-and-backtracking)

---

## Greedy

```
  Merge Intervals — Greedy approach:
  Input: [[1,3],[2,6],[8,10],[15,18]]
  Sort by start: [1,3],[2,6],[8,10],[15,18]

  current = [1,3]
  [2,6]:  2 ≤ 3 → overlap → merge → [1,6]
  [8,10]: 8 > 6 → no overlap → save [1,6], current=[8,10]
  [15,18]:15 > 10 → no overlap → save [8,10], current=[15,18]
  Save [15,18]
  Result: [[1,6],[8,10],[15,18]]

  Why greedy works here: sorting by start guarantees we only
  need to check the last merged interval — no need to look back.

  Jump Game — Greedy:
  nums = [2, 3, 1, 1, 4]
  max_reach = 0
  i=0: max_reach = max(0, 0+2) = 2
  i=1: max_reach = max(2, 1+3) = 4
  i=2: max_reach = max(4, 2+1) = 4
  i=3: max_reach = max(4, 3+1) = 4  ← i never exceeds max_reach
  i=4: reached end → True
```

**What it does:** Makes the locally optimal choice at each step with the hope that it leads to a globally optimal solution. Works only when the **greedy choice property** holds — you must prove (or recognize) that local optimality → global optimality.

**Recognition signals:**
- Interval scheduling / merging
- Minimum number of something (jumps, coins — but check if DP not needed)
- "Always pick the smallest/largest/earliest"
- Activity selection problems
- Huffman encoding, Kruskal's MST

**Python:**
```python
# Merge Intervals
def merge(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged

# Jump Game (can we reach end?)
def can_jump(nums):
    max_reach = 0
    for i, jump in enumerate(nums):
        if i > max_reach:
            return False    # can't reach this position
        max_reach = max(max_reach, i + jump)
    return True

# Activity selection (maximize non-overlapping intervals)
def max_activities(intervals):
    intervals.sort(key=lambda x: x[1])  # sort by END time
    count, last_end = 0, float('-inf')
    for start, end in intervals:
        if start >= last_end:
            count += 1
            last_end = end
    return count
```

**Complexity:** Usually O(n log n) due to sorting, then O(n) for the greedy pass.

**Data structures it uses:**
[Array](datastructures.md#array) · [Heap and Priority Queue](datastructures.md#heap-and-priority-queue) (for some greedy problems)

**Patterns it enables:**
[Merge Intervals](../skeletons/patterns.md#merge-intervals) · [Top K Elements](../skeletons/patterns.md#top-k-elements) (partial)

---

## Bit Manipulation

```
  Binary representation:
  13 = 1101₂  →  bit3=1, bit2=1, bit1=0, bit0=1

  Core operations:
  ┌──────────────┬──────────┬─────────────────────────────┐
  │ Operation    │ Syntax   │ Example                      │
  ├──────────────┼──────────┼─────────────────────────────┤
  │ AND          │ a & b    │ 1101 & 1010 = 1000           │
  │ OR           │ a | b    │ 1101 | 1010 = 1111           │
  │ XOR          │ a ^ b    │ 1101 ^ 1010 = 0111           │
  │ NOT          │ ~a       │ ~1101 = ...0010 (2's comp)   │
  │ Left shift   │ a << n   │ 0001 << 2 = 0100 (× 2^n)    │
  │ Right shift  │ a >> n   │ 1100 >> 2 = 0011 (÷ 2^n)    │
  └──────────────┴──────────┴─────────────────────────────┘

  XOR truth table:
  0 ^ 0 = 0   (same → 0)
  0 ^ 1 = 1   (diff → 1)
  1 ^ 0 = 1
  1 ^ 1 = 0   (same → 0)

  Key XOR properties:
  a ^ a = 0        (self-cancels)
  a ^ 0 = a        (identity)
  a ^ b ^ a = b    (used in "find single number")
```

**What it does:** Operates directly on the binary representation of integers. Enables O(1) space solutions and often O(n) time for problems that would otherwise require sets or additional space.

**Recognition signals:**
- "Find the single number" (XOR pairs to cancel)
- "Missing number" (XOR with full range)
- Powers of 2 check: `n & (n-1) == 0`
- Count set bits (popcount)
- Subset generation using bitmask
- "Sum without +" (bit by bit carry simulation)

**Python:**
```python
# Check if bit k is set
(n >> k) & 1

# Set bit k
n | (1 << k)

# Clear bit k
n & ~(1 << k)

# Toggle bit k
n ^ (1 << k)

# Check power of 2 (exactly one bit set)
n > 0 and (n & (n - 1)) == 0

# Count set bits (Hamming weight)
bin(n).count('1')
# OR kernighan's method: O(number of set bits)
count = 0
while n:
    n &= n - 1   # clear lowest set bit
    count += 1

# XOR: find single number (all others appear twice)
from functools import reduce
import operator
single = reduce(operator.xor, nums)

# Missing number (0..n, one missing)
missing = len(nums)
for i, num in enumerate(nums):
    missing ^= i ^ num

# Subset enumeration using bitmask
n = 3
for mask in range(1 << n):   # 0 to 2^n - 1
    subset = [i for i in range(n) if mask & (1 << i)]
```

**Complexity:** All individual bit operations are O(1). Problems using bits over an array are typically O(n) time, O(1) space.

**Data structures it uses:**
[Array](datastructures.md#array) (of integers)

**Patterns it enables:**
[Bit Manipulation and XOR](../skeletons/patterns.md#bit-manipulation-and-xor)

---

*Back to [Table of Contents](#table-of-contents) · See also: [datastructures.md](datastructures.md) · [patterns.md](../skeletons/patterns.md)*
