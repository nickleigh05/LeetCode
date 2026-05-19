# Data Structures Reference

A complete reference for every major data structure you will encounter in LeetCode and technical interviews. Each section includes a visual, complexity tables, when to reach for it, and links to the algorithms and patterns that use it.

---

## Table of Contents

| # | Data Structure | Jump To |
|---|----------------|---------|
| 1 | Array | [→ Array](#array) |
| 2 | String | [→ String](#string) |
| 3 | Hash Map and Hash Set | [→ Hash Map and Hash Set](#hash-map-and-hash-set) |
| 4 | Stack | [→ Stack](#stack) |
| 5 | Queue and Deque | [→ Queue and Deque](#queue-and-deque) |
| 6 | Linked List | [→ Linked List](#linked-list) |
| 7 | Binary Tree | [→ Binary Tree](#binary-tree) |
| 8 | Binary Search Tree | [→ Binary Search Tree](#binary-search-tree) |
| 9 | Heap and Priority Queue | [→ Heap and Priority Queue](#heap-and-priority-queue) |
| 10 | Trie | [→ Trie](#trie) |
| 11 | Graph | [→ Graph](#graph) |
| 12 | Disjoint Set Union | [→ Disjoint Set Union](#disjoint-set-union) |
| 13 | Monotonic Stack | [→ Monotonic Stack](#monotonic-stack) |

**Other files:** [algorithms.md](algorithms.md) · [patterns.md](patterns.md)

---

## Array

```
Index:  0    1    2    3    4    5
      ┌────┬────┬────┬────┬────┬────┐
Value:│ 3  │ 1  │ 4  │ 1  │ 5  │ 9  │
      └────┴────┴────┴────┴────┴────┘
         ↑                        ↑
       O(1) access             O(1) append
```

**What it is:** A contiguous sequence of elements stored in memory, accessible in O(1) time by index. Python's `list` is a dynamic array that resizes automatically.

**Key Properties:**
- Random access via index in O(1)
- Insertion/deletion in the middle shifts elements → O(n)
- Appending to the end is O(1) amortized (occasionally resizes)
- Elements are ordered — position matters

**Complexity:**

| Operation | Average | Notes |
|-----------|---------|-------|
| Access by index | O(1) | Direct memory offset |
| Search (unsorted) | O(n) | Must scan linearly |
| Search (sorted) | O(log n) | With Binary Search |
| Insert at end | O(1) amortized | Occasional resize |
| Insert at middle | O(n) | Shift elements right |
| Delete at end | O(1) | |
| Delete at middle | O(n) | Shift elements left |
| Space | O(n) | |

**Use when:**
- You need O(1) index-based access
- You are appending/reading from the end frequently
- Order of elements matters
- You need to apply binary search (must be sorted)

**Python:**
```python
arr = [1, 2, 3, 4, 5]
arr.append(6)          # O(1) amortized
arr.insert(2, 99)      # O(n) - insert at index 2
arr.pop()              # O(1) - remove last
arr.pop(2)             # O(n) - remove at index
arr[2]                 # O(1) - access by index
arr[1:4]               # O(k) - slice, k = length of slice
```

**Patterns that use Arrays:**
[Two Pointers](patterns.md#two-pointers) · [Sliding Window](patterns.md#sliding-window) · [Prefix Sum](patterns.md#prefix-sum) · [Binary Search on Answer](patterns.md#binary-search-on-answer) · [Monotonic Stack](patterns.md#monotonic-stack) · [Dynamic Programming](patterns.md#dynamic-programming)

**Algorithms that operate on Arrays:**
[Binary Search](algorithms.md#binary-search) · [Merge Sort](algorithms.md#merge-sort) · [Quick Sort](algorithms.md#quick-sort)

---

## String

```
  s = "h  e  l  l  o"
       0  1  2  3  4    ← indices
       ↑              ↑
     s[0]='h'       s[4]='o'
     s[-1]='o'  (negative indexing wraps around)

  Slicing:
  s[1:4]  →  "ell"   (start inclusive, end exclusive)
  s[::-1] →  "olleh" (reverse)
```

**What it is:** An immutable sequence of characters. In Python, strings cannot be modified in place — any "change" creates a new string.

**Key Properties:**
- Immutable: `s[0] = 'x'` raises `TypeError`
- Concatenation with `+` is O(n+m) — avoid in loops; use `''.join(list)` instead
- String comparison is O(n) (character by character)
- `ord(c)` converts char to integer; `chr(n)` converts back

**Complexity:**

| Operation | Time | Notes |
|-----------|------|-------|
| Access `s[i]` | O(1) | |
| Slice `s[i:j]` | O(j-i) | Creates new string |
| Concat `s + t` | O(n+m) | Avoid in loops |
| `''.join(lst)` | O(n) | Preferred for building strings |
| `in` / `find` | O(n·m) | Naive substring search |
| Split / Strip | O(n) | |

**Use when:**
- Working with character frequency (anagrams, permutations)
- Palindrome checks
- Substring matching or extraction
- Encoding/decoding problems

**Python:**
```python
s = "hello world"
s.lower()              # "hello world"
s.upper()              # "HELLO WORLD"
s.split(" ")           # ["hello", "world"]
s.replace("l", "r")   # "herro worrd"
s[::-1]                # "dlrow olleh"  (reverse)
"".join(["a","b","c"]) # "abc"
ord("a")               # 97
chr(97)                # "a"

from collections import Counter
Counter("banana")      # {'a': 3, 'n': 2, 'b': 1}
```

**Patterns that use Strings:**
[Sliding Window](patterns.md#sliding-window) · [Two Pointers](patterns.md#two-pointers) · [Dynamic Programming](patterns.md#dynamic-programming) · [Trie Search](patterns.md#trie-search)

**Algorithms that operate on Strings:**
[Binary Search](algorithms.md#binary-search) (on sorted char arrays) · [Backtracking](algorithms.md#backtracking) (word search, permutations)

---

## Hash Map and Hash Set

```
  Hash Map (dict):                Hash Set (set):
  ┌─────────────────────────┐    ┌───────────────┐
  │ Key      │ Value         │    │   Elements     │
  ├──────────┼───────────────┤    ├───────────────┤
  │ "apple"  │  5            │    │   "apple"      │
  │ "banana" │  3            │    │   "banana"     │
  │ "cherry" │  1            │    │   "cherry"     │
  └─────────────────────────┘    └───────────────┘
       O(1) avg lookup                O(1) avg lookup
                                      (no duplicates)

  Hashing:
  key ──→ hash(key) ──→ bucket index ──→ value
```

**What it is:** A data structure that maps keys to values (HashMap) or just stores unique keys (HashSet) using a hash function for O(1) average-case access.

**Key Properties:**
- Average O(1) for insert, delete, lookup
- Worst case O(n) due to hash collisions (rare with good hash functions)
- Unordered (Python 3.7+ dicts preserve insertion order, but don't rely on sorted order)
- Keys must be hashable (immutable types: int, str, tuple)

**Complexity:**

| Operation | Average | Worst |
|-----------|---------|-------|
| Insert | O(1) | O(n) |
| Delete | O(1) | O(n) |
| Lookup | O(1) | O(n) |
| Iterate | O(n) | O(n) |
| Space | O(n) | O(n) |

**Use when:**
- You need O(1) lookup by a key (not by position)
- Counting frequencies of elements
- Caching/memoizing previously computed results
- Checking membership quickly (`x in s` is O(1) for sets, O(n) for lists)
- Finding complements (Two Sum pattern: store `target - num`)

**Python:**
```python
# HashMap (dict)
freq = {}
freq["a"] = freq.get("a", 0) + 1

from collections import defaultdict
freq = defaultdict(int)
freq["a"] += 1

from collections import Counter
freq = Counter("banana")  # auto-counts

# HashSet (set)
seen = set()
seen.add(5)
seen.discard(5)    # remove if present (no error if missing)
5 in seen          # O(1) lookup

# Common patterns
# Two Sum: store complement
nums = [2, 7, 11, 15]
target = 9
lookup = {}
for i, n in enumerate(nums):
    if target - n in lookup:
        print(lookup[target - n], i)
    lookup[n] = i
```

**Patterns that use Hash Maps/Sets:**
[Two Pointers](patterns.md#two-pointers) · [Sliding Window](patterns.md#sliding-window) · [Prefix Sum](patterns.md#prefix-sum) · [Top K Elements](patterns.md#top-k-elements) · [Union Find](patterns.md#union-find)

**Algorithms that use Hash Maps/Sets:**
[Dynamic Programming](algorithms.md#dynamic-programming) (memoization) · [Topological Sort](algorithms.md#topological-sort) (in-degree table)

---

## Stack

```
  Push 3 → Push 1 → Push 4 → Pop

  After pushing 3, 1, 4:       After pop:
        ┌───┐                        ┌───┐
  top → │ 4 │                  top → │ 1 │
        ├───┤                        ├───┤
        │ 1 │                        │ 1 │  ← wait no:
        ├───┤                        ├───┤
        │ 3 │                        │ 3 │
        └───┘                        └───┘
       LIFO: Last In, First Out
```

**What it is:** A Last-In-First-Out (LIFO) collection. The last element pushed is the first one popped. Implemented with a Python list using `append`/`pop`.

**Key Properties:**
- O(1) push and pop (from the top)
- O(n) search (must scan)
- No random access
- The call stack in recursion is itself a stack — recursive DFS uses the implicit call stack

**Complexity:**

| Operation | Time |
|-----------|------|
| Push (append) | O(1) |
| Pop | O(1) |
| Peek (top) | O(1) |
| Search | O(n) |
| Space | O(n) |

**Use when:**
- Matching/balancing: parentheses, brackets, tags
- Tracking state as you go deeper (DFS iteratively)
- "Undo" operations — most recent action is most relevant
- Evaluating expressions (postfix notation)
- Keeping a history of previous states

**Python:**
```python
stack = []
stack.append(1)   # push
stack.append(2)
stack.append(3)
stack.pop()       # 3 — O(1)
stack[-1]         # peek top without removing → 2
if stack:         # check not empty
    ...
```

**Patterns that use Stacks:**
[Monotonic Stack](patterns.md#monotonic-stack) · [DFS and Backtracking](patterns.md#dfs-and-backtracking)

**Algorithms that use Stacks:**
[Depth-First Search](algorithms.md#depth-first-search) (iterative) · [Topological Sort](algorithms.md#topological-sort) (DFS version) · [Backtracking](algorithms.md#backtracking)

---

## Queue and Deque

```
  Queue (FIFO):
  Enqueue →  [ 1 | 2 | 3 | 4 ]  → Dequeue
             front             back
             (popleft)         (append)

  Deque (Double-Ended Queue):
  appendleft ←  [ 1 | 2 | 3 | 4 ]  → append
  popleft    →                      ← pop
               O(1) on both ends!
```

**What it is:** A Queue is a First-In-First-Out (FIFO) structure. A Deque (double-ended queue) allows O(1) insertions and deletions from both ends. Always use `collections.deque`, not a plain list (list's `pop(0)` is O(n)).

**Key Properties:**
- Queue: enqueue at back, dequeue from front — both O(1)
- Deque: O(1) at both ends
- BFS requires a queue (not a stack) to guarantee shortest-path exploration
- A deque with a size limit is the sliding window max trick

**Complexity:**

| Operation | Queue | Deque |
|-----------|-------|-------|
| Enqueue / append | O(1) | O(1) |
| Dequeue / popleft | O(1) | O(1) |
| Append left | — | O(1) |
| Pop right | — | O(1) |
| Peek | O(1) | O(1) |
| Space | O(n) | O(n) |

**Use when:**
- BFS traversal (tree level-order, shortest path in grid)
- Processing items in the order they arrived
- Sliding window maximum/minimum (deque stores indices in monotonic order)
- Multi-source BFS (start with multiple nodes in the queue)

**Python:**
```python
from collections import deque

q = deque()
q.append(1)        # enqueue right
q.append(2)
q.popleft()        # dequeue left → 1  (O(1)!)
q.appendleft(0)    # O(1)
q.pop()            # O(1) from right
q[0]               # peek front
q[-1]              # peek back

# BFS template
q = deque([start])
visited = {start}
while q:
    node = q.popleft()
    for neighbor in graph[node]:
        if neighbor not in visited:
            visited.add(neighbor)
            q.append(neighbor)
```

**Patterns that use Queues/Deques:**
[BFS on Grid and Tree](patterns.md#bfs-on-grid-and-tree) · [Sliding Window](patterns.md#sliding-window) · [Topological Sort](patterns.md#topological-sort)

**Algorithms that use Queues/Deques:**
[Breadth-First Search](algorithms.md#breadth-first-search) · [Topological Sort](algorithms.md#topological-sort) (Kahn's algorithm)

---

## Linked List

```
  Singly Linked List:
  head
   ↓
  [1] → [3] → [5] → [7] → None
   ↑              ↑
  O(1) insert   O(n) to reach
  at head        any node

  Doubly Linked List:
  None ← [1] ↔ [3] ↔ [5] ↔ [7] → None
          ↑                    ↑
         head                 tail
       O(1) at both ends (with tail pointer)

  Node structure:
  ┌──────┬──────┐
  │ val  │ next │
  └──────┴──────┘
```

**What it is:** A sequence of nodes where each node holds a value and a pointer to the next node (singly) or both next and previous nodes (doubly). There is no index-based access.

**Key Properties:**
- No random access — must traverse from head → O(n)
- O(1) insert/delete at a known node (just rewire pointers)
- Finding a node first takes O(n)
- Cycle detection is a classic linked list problem

**Complexity:**

| Operation | Singly | Doubly |
|-----------|--------|--------|
| Access node | O(n) | O(n) |
| Insert at head | O(1) | O(1) |
| Insert at tail | O(n) without tail ptr | O(1) with tail ptr |
| Insert at known position | O(1) | O(1) |
| Delete at head | O(1) | O(1) |
| Delete at known node | O(1)* | O(1) |
| Search | O(n) | O(n) |
| Space | O(n) | O(n) |

*For singly, you need the previous node too.

**Use when:**
- You need O(1) insertions/deletions at the head or at a known position
- You don't need random access
- Implementing stacks/queues from scratch
- Problems explicitly about linked lists (reverse, cycle, merge)

**Python:**
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# Build: 1 -> 2 -> 3
head = ListNode(1, ListNode(2, ListNode(3)))

# Traverse
cur = head
while cur:
    print(cur.val)
    cur = cur.next

# Dummy head trick (simplifies edge cases)
dummy = ListNode(0)
dummy.next = head
```

**Patterns that use Linked Lists:**
[Fast and Slow Pointers](patterns.md#fast-and-slow-pointers) · [Two Pointers](patterns.md#two-pointers)

**Algorithms that use Linked Lists:**
[Merge Sort](algorithms.md#merge-sort) (merge step works naturally on linked lists)

---

## Binary Tree

```
  Binary Tree:               Terminology:
       1                     ┌─────────────────────────┐
      / \                    │ root    = node with no   │
     2   3                   │          parent (1)       │
    / \   \                  │ leaf    = node with no   │
   4   5   6                 │          children (4,5,6) │
                             │ height  = longest path   │
  Node structure:            │          from root→leaf  │
  ┌──────┬──────┬──────┐     │ depth   = distance from  │
  │ val  │ left │ right│     │          root to node    │
  └──────┴──────┴──────┘     └─────────────────────────┘

  Traversals (on tree above):
  Inorder   (L→root→R): 4, 2, 5, 1, 3, 6
  Preorder  (root→L→R): 1, 2, 4, 5, 3, 6
  Postorder (L→R→root): 4, 5, 2, 6, 3, 1
  Level-order (BFS):    1, 2, 3, 4, 5, 6
```

**What it is:** A hierarchical structure where each node has at most two children: `left` and `right`. There are no ordering guarantees (unlike BST).

**Key Properties:**
- Height of a balanced tree: O(log n)
- Height of a skewed tree (worst case): O(n)
- Inorder traversal of a BST yields sorted order
- Most tree problems are solved with DFS (recursion) or BFS (queue)

**Complexity (balanced):**

| Operation | Time |
|-----------|------|
| Access | O(log n) |
| Search | O(log n) |
| Insert | O(log n) |
| Delete | O(log n) |
| Traversal (all nodes) | O(n) |
| Space (balanced) | O(log n) stack space |

**Use when:**
- The problem has hierarchical or parent-child relationships
- You need to explore all paths (DFS) or process level by level (BFS)
- Representing expression trees, file systems, decision trees

**Python:**
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# DFS - Inorder (recursive)
def inorder(root):
    if not root:
        return []
    return inorder(root.left) + [root.val] + inorder(root.right)

# BFS - Level order
from collections import deque
def level_order(root):
    if not root:
        return []
    q, result = deque([root]), []
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left:  q.append(node.left)
            if node.right: q.append(node.right)
        result.append(level)
    return result
```

**Patterns that use Binary Trees:**
[BFS on Grid and Tree](patterns.md#bfs-on-grid-and-tree) · [DFS and Backtracking](patterns.md#dfs-and-backtracking) · [Dynamic Programming](patterns.md#dynamic-programming) (tree DP)

**Algorithms that use Binary Trees:**
[Breadth-First Search](algorithms.md#breadth-first-search) · [Depth-First Search](algorithms.md#depth-first-search)

---

## Binary Search Tree

```
  Valid BST:                 BST Property:
       8                     For every node N:
      / \                    ┌─────────────────────────────────┐
     3   10                  │ All nodes in LEFT subtree  < N  │
    / \    \                 │ All nodes in RIGHT subtree > N  │
   1   6    14               │ No duplicates (by convention)   │
      / \   /                └─────────────────────────────────┘
     4   7 13
                             Inorder: 1, 3, 4, 6, 7, 8, 10, 13, 14
                             Always sorted!
```

**What it is:** A Binary Tree with the invariant that every left subtree contains only values less than the node, and every right subtree contains only values greater. Inorder traversal always yields sorted order.

**Key Properties:**
- Inorder traversal = sorted sequence (extremely useful)
- O(log n) operations when balanced (AVL, Red-Black tree); O(n) when skewed
- Python does not have a built-in balanced BST — use `sortedcontainers.SortedList` if needed

**Complexity (balanced):**

| Operation | Time |
|-----------|------|
| Search | O(log n) |
| Insert | O(log n) |
| Delete | O(log n) |
| Min / Max | O(log n) |
| Inorder traversal | O(n) |

**Use when:**
- You need sorted data with fast insert/search/delete
- Finding kth smallest/largest element
- Validating BST structure
- Range queries (find all values between lo and hi)

**Python:**
```python
# Search in BST
def search(root, target):
    if not root:
        return None
    if target == root.val:
        return root
    elif target < root.val:
        return search(root.left, target)
    else:
        return search(root.right, target)

# Inorder → sorted list
def inorder(root, result=[]):
    if root:
        inorder(root.left, result)
        result.append(root.val)
        inorder(root.right, result)
```

**Patterns that use BSTs:**
[DFS and Backtracking](patterns.md#dfs-and-backtracking) · [Binary Search on Answer](patterns.md#binary-search-on-answer)

**Algorithms that use BSTs:**
[Depth-First Search](algorithms.md#depth-first-search)

---

## Heap and Priority Queue

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

**Patterns that use Heaps:**
[Top K Elements](patterns.md#top-k-elements) · [Two Heaps](patterns.md#two-heaps) · [BFS on Grid and Tree](patterns.md#bfs-on-grid-and-tree) (Dijkstra variant)

**Algorithms that use Heaps:**
[Dijkstras Algorithm](algorithms.md#dijkstras-algorithm) · [Merge Sort](algorithms.md#merge-sort) (merge K sorted lists variant)

---

## Trie

```
  Words inserted: "cat", "car", "card", "care", "bat"

         root
        /    \
       c      b
       |      |
       a      a
      / \     |
     t*  r    t*
         |
         *    ← "car"
        / \
       d*  e*  ← "card", "care"

  * = end of word marker (is_end = True)

  Each node:
  ┌──────────────────────────────┐
  │ children: dict[char → Node]  │
  │ is_end:   bool               │
  └──────────────────────────────┘
```

**What it is:** A tree where each path from root to a marked node spells out a word. Each node represents a character, and children represent the next possible characters.

**Key Properties:**
- Insert and search are O(L) where L = length of the word — independent of how many words are stored
- Excellent for prefix queries ("all words starting with 'ca'")
- Space is O(ALPHABET_SIZE × L × N) — can be large for big alphabets

**Complexity:**

| Operation | Time |
|-----------|------|
| Insert word | O(L) |
| Search word | O(L) |
| Prefix search | O(L) |
| Space | O(L × N × A) |

L = word length, N = number of words, A = alphabet size

**Use when:**
- Autocomplete / prefix matching
- Word search on a board (combine with DFS)
- Checking if any word in a list is a prefix of another
- Implementing a spell checker

**Python:**
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end

    def starts_with(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True
```

**Patterns that use Tries:**
[Trie Search](patterns.md#trie-search) · [DFS and Backtracking](patterns.md#dfs-and-backtracking) (word search on grid)

**Algorithms that use Tries:**
[Depth-First Search](algorithms.md#depth-first-search) (searching paths in the trie)

---

## Graph

```
  Undirected Graph:           Directed Graph (DAG):
    1 ── 2                      1 ──→ 2
    │  ╲ │                      │     │
    │   ╲│                      ↓     ↓
    3    4                      3 ──→ 4

  Adjacency List (most common for sparse graphs):
  graph = {
      1: [2, 3, 4],
      2: [1, 4],
      3: [1],
      4: [1, 2]
  }

  Adjacency Matrix (for dense graphs / O(1) edge lookup):
       1  2  3  4
  1  [ 0, 1, 1, 1 ]
  2  [ 1, 0, 0, 1 ]
  3  [ 1, 0, 0, 0 ]
  4  [ 1, 1, 0, 0 ]

  Grid as graph (4-directional neighbors):
  directions = [(0,1),(0,-1),(1,0),(-1,0)]
```

**What it is:** A set of vertices (nodes) connected by edges. Can be directed or undirected, weighted or unweighted, cyclic or acyclic.

**Key Properties:**
- Adjacency list: O(V + E) space — standard for most LeetCode problems
- Adjacency matrix: O(V²) space — use only when edges are dense or O(1) edge lookup needed
- A grid is an implicit graph where each cell connects to its neighbors
- V = number of vertices, E = number of edges

**Complexity (Adjacency List):**

| Operation | Time |
|-----------|------|
| Add vertex | O(1) |
| Add edge | O(1) |
| Check edge (u, v) | O(degree of u) |
| Get neighbors | O(degree) |
| BFS / DFS traversal | O(V + E) |
| Space | O(V + E) |

**Use when:**
- Problems about connections, paths, or reachability
- Islands, clones, dependencies (course schedule), routes
- The problem involves nodes and relationships between them
- Grid traversal (number of islands, shortest path in maze)

**Python:**
```python
from collections import defaultdict, deque

# Build adjacency list
graph = defaultdict(list)
graph[1].append(2)
graph[2].append(1)   # undirected: add both directions

# Build from edge list
edges = [(1,2), (2,3), (3,4)]
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)  # omit for directed

# Grid traversal
def neighbors(r, c, rows, cols):
    for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
        nr, nc = r+dr, c+dc
        if 0 <= nr < rows and 0 <= nc < cols:
            yield nr, nc
```

**Patterns that use Graphs:**
[BFS on Grid and Tree](patterns.md#bfs-on-grid-and-tree) · [DFS and Backtracking](patterns.md#dfs-and-backtracking) · [Union Find](patterns.md#union-find) · [Topological Sort](patterns.md#topological-sort)

**Algorithms that use Graphs:**
[Breadth-First Search](algorithms.md#breadth-first-search) · [Depth-First Search](algorithms.md#depth-first-search) · [Dijkstras Algorithm](algorithms.md#dijkstras-algorithm) · [Topological Sort](algorithms.md#topological-sort)

---

## Disjoint Set Union

```
  Initial: 5 separate components
  {0} {1} {2} {3} {4}
   0   1   2   3   4   ← parent[i] = i (each is own root)

  union(0, 1):       union(1, 2):       union(3, 4):
  {0,1} {2} {3} {4}  {0,1,2} {3} {4}  {0,1,2} {3,4}

  Tree after union(0,1) and union(1,2):
       0                       With path compression:
      /                        find(2) → 2→1→0, then set parent[2]=0
     1
     |
     2

  find(x): return root of x's component (with path compression)
  union(x, y): merge the two components (by rank)
```

**What it is:** A data structure that tracks which elements are in the same connected component. Supports two operations: `find` (which component?) and `union` (merge two components). With path compression and union by rank, both are nearly O(1).

**Key Properties:**
- `find(x)` returns the representative (root) of x's component
- `union(x, y)` connects x's and y's components
- Path compression: on `find`, directly connect nodes to root → amortized O(α(n)) ≈ O(1)
- Union by rank: always attach smaller tree under larger → keeps trees flat

**Complexity:**

| Operation | Time |
|-----------|------|
| find | O(α(n)) ≈ O(1) |
| union | O(α(n)) ≈ O(1) |
| Build for n elements | O(n) |
| Space | O(n) |

α(n) = inverse Ackermann function, effectively constant for all practical n.

**Use when:**
- Counting connected components
- Detecting a cycle in an undirected graph
- Kruskal's Minimum Spanning Tree
- Dynamic connectivity: checking if two nodes are in the same group

**Python:**
```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False   # already connected
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px          # union by rank
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        self.components -= 1
        return True

    def connected(self, x, y):
        return self.find(x) == self.find(y)
```

**Patterns that use Disjoint Set Union:**
[Union Find](patterns.md#union-find)

**Algorithms that relate to DSU:**
[Depth-First Search](algorithms.md#depth-first-search) (alternative for connectivity) · [Breadth-First Search](algorithms.md#breadth-first-search) (alternative for connectivity)

---

## Monotonic Stack

```
  Array:  [2, 1, 5, 6, 2, 3]
  Goal: find "next greater element" for each index

  Process left to right, maintain a DECREASING stack:

  i=0, val=2:  stack=[]         push 2  → stack=[2]
  i=1, val=1:  1 < 2, push     → stack=[2,1]
  i=2, val=5:  5 > 1, pop 1 (next greater of 1 = 5)
               5 > 2, pop 2 (next greater of 2 = 5)
               push 5          → stack=[5]
  i=3, val=6:  6 > 5, pop 5 (next greater of 5 = 6)
               push 6          → stack=[6]
  i=4, val=2:  2 < 6, push     → stack=[6,2]
  i=5, val=3:  3 > 2, pop 2 (next greater of 2 = 3)
               3 < 6, push     → stack=[6,3]

  Result: [5, 5, 6, -1, 3, -1]
            ↑                ↑
           next greater   no next greater → -1
```

**What it is:** A stack that maintains a monotonically increasing or decreasing order. When a new element violates the order, you pop elements (and that's usually when you record the answer).

**Key Properties:**
- Each element is pushed and popped at most once → O(n) total
- Decreasing stack: useful for "next greater element"
- Increasing stack: useful for "next smaller element"
- Store indices, not values — you'll often need the position too

**Complexity:**

| Operation | Time |
|-----------|------|
| Process entire array | O(n) total |
| Space | O(n) |

**Use when:**
- Next Greater Element / Next Smaller Element
- Largest Rectangle in Histogram
- Daily Temperatures
- Trapping Rain Water
- Maximum width ramp

**Python:**
```python
# Next Greater Element template
def next_greater(nums):
    n = len(nums)
    result = [-1] * n
    stack = []  # stores indices, maintains decreasing values

    for i in range(n):
        while stack and nums[i] > nums[stack[-1]]:
            idx = stack.pop()
            result[idx] = nums[i]   # nums[i] is next greater for idx
        stack.append(i)

    return result

# Increasing monotonic stack (next smaller element)
def next_smaller(nums):
    result = [-1] * len(nums)
    stack = []
    for i, val in enumerate(nums):
        while stack and val < nums[stack[-1]]:
            result[stack.pop()] = val
        stack.append(i)
    return result
```

**Patterns that use Monotonic Stack:**
[Monotonic Stack](patterns.md#monotonic-stack) · [Sliding Window](patterns.md#sliding-window) (deque variant for max/min)

**Algorithms that use Monotonic Stack:**
[Depth-First Search](algorithms.md#depth-first-search) (conceptually similar stack-based traversal)

---

*Back to [Table of Contents](#table-of-contents) · See also: [algorithms.md](algorithms.md) · [patterns.md](patterns.md)*
