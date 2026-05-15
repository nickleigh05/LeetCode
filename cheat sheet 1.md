# 🐍 Python LeetCode Cheat Sheet

> Quick reference for patterns, syntax, and data structures used in competitive problem solving.

---

## Table of Contents

| # | Section |
|---|---------|
| 01 | [Lists & Arrays](#01-lists--arrays) |
| 02 | [Strings](#02-strings) |
| 03 | [Dicts & Sets](#03-dicts--sets) |
| 04 | [Two Pointers](#04-two-pointers) |
| 05 | [Sliding Window](#05-sliding-window) |
| 06 | [Binary Search](#06-binary-search) |
| 07 | [Stack & Queue](#07-stack--queue) |
| 08 | [Heap / Priority Queue](#08-heap--priority-queue) |
| 09 | [Linked List](#09-linked-list) |
| 10 | [Trees](#10-trees) |
| 11 | [Graphs](#11-graphs) |
| 12 | [Dynamic Programming](#12-dynamic-programming) |
| 13 | [Sorting & Math](#13-sorting--math) |
| 14 | [Bit Tricks](#14-bit-tricks) |

---

## 01 Lists & Arrays

```python
# --- Create / Init ---
arr = []
arr = [0] * n                          # 1D, all zeros
arr = [[0] * n for _ in range(m)]      # 2D, all zeros
arr = list(range(n))                   # [0, 1, ..., n-1]

# --- Slicing ---
arr[i:j]        # [i, j)
arr[i:j:step]   # with step
arr[::-1]       # reversed copy
arr[-1]         # last element
arr[-k:]        # last k elements

# --- Mutation ---
arr.append(x)      # O(1) — add to end
arr.pop()          # O(1) — remove from end
arr.pop(i)         # O(n) — remove at index
arr.insert(i, x)   # O(n) — insert at index
arr.remove(x)      # O(n) — removes first match
arr.extend(other)  # O(k) — append another list

# --- Sort & Search ---
arr.sort()                        # in-place, O(n log n)
arr.sort(reverse=True)
arr.sort(key=lambda x: x[1])     # sort by second element
sorted(arr)                       # returns new list
arr.index(x)                      # first index of x, O(n)
x in arr                          # O(n) membership

# --- Comprehensions ---
squares  = [x**2 for x in arr]
filtered = [x for x in arr if x > 0]
flat     = [x for row in grid for x in row]   # flatten 2D

# --- Useful Builtins ---
len(arr), sum(arr), min(arr), max(arr)
enumerate(arr)          # yields (index, value)
zip(a, b)               # paired iteration
any(arr), all(arr)
```

> **Tip:** `arr.pop(i)` and `arr.insert(i, x)` are O(n) due to shifting. Prefer deque for frequent front operations.

---

## 02 Strings

```python
# --- Common Methods ---
s.lower(), s.upper()
s.strip()                  # remove leading/trailing whitespace
s.split(" ")               # split by delimiter → list
" ".join(words)            # list → string
s.replace(old, new)
s.startswith(prefix)
s.endswith(suffix)

# --- Search & Count ---
s.find(sub)         # returns -1 if not found
s.index(sub)        # raises ValueError if not found
s.count(sub)        # count non-overlapping occurrences
sub in s            # O(n) membership

# --- Char Tricks ---
ord('a')              # → 97
chr(97)               # → 'a'
ord(c) - ord('a')     # → 0-25 index for lowercase letters

s.isalpha()           # only letters
s.isdigit()           # only digits
s.isalnum()           # letters or digits

# --- Mutable String Pattern ---
chars = list(s)       # convert to list for mutation
chars[i] = 'x'
s = "".join(chars)    # back to string
```

> **Tip:** String concatenation in a loop is O(n²). Use `list` + `"".join()` instead.

---

## 03 Dicts & Sets

```python
from collections import defaultdict, Counter, OrderedDict

# --- Dict Basics ---
d = {}
d[key] = val
d.get(key, default)       # safe get with fallback
d.keys(), d.values(), d.items()
key in d                  # O(1) lookup
del d[key]
d.pop(key, None)          # remove and return, no error if missing

# --- defaultdict ---
dd = defaultdict(int)     # missing keys default to 0
dd = defaultdict(list)    # missing keys default to []
dd = defaultdict(set)

# --- Counter ---
cnt = Counter(arr)              # frequency map
cnt = Counter(s)                # works on strings too
cnt.most_common(k)              # top-k (val, freq) pairs
cnt['x'] += 1                   # safe increment

# --- Set Ops ---
s = set()
s = {1, 2, 3}
s.add(x)
s.discard(x)        # no error if missing
s.remove(x)         # raises KeyError if missing

a & b               # intersection
a | b               # union
a - b               # difference
a ^ b               # symmetric difference
a.issubset(b)
a.issuperset(b)

# --- Dedup while preserving order ---
seen = set()
unique = [x for x in arr if not (x in seen or seen.add(x))]
```

---

## 04 Two Pointers

```python
# --- Opposite Ends (e.g. Two Sum on sorted array) ---
l, r = 0, len(arr) - 1
while l < r:
    s = arr[l] + arr[r]
    if s == target:
        return [l, r]
    elif s < target:
        l += 1
    else:
        r -= 1

# --- Same Direction / Slow+Fast (e.g. remove duplicates) ---
slow = 0
for fast in range(len(arr)):
    if arr[fast] != val:
        arr[slow] = arr[fast]
        slow += 1
return slow

# --- Three Pointers (e.g. 3Sum) ---
arr.sort()
for i in range(len(arr) - 2):
    if i > 0 and arr[i] == arr[i-1]:
        continue                    # skip duplicates
    l, r = i + 1, len(arr) - 1
    while l < r:
        s = arr[i] + arr[l] + arr[r]
        if s == 0:
            res.append([arr[i], arr[l], arr[r]])
            while l < r and arr[l] == arr[l+1]: l += 1
            while l < r and arr[r] == arr[r-1]: r -= 1
            l += 1; r -= 1
        elif s < 0: l += 1
        else: r -= 1
```

---

## 05 Sliding Window

```python
# --- Fixed Size Window ---
window = sum(arr[:k])
res = window
for i in range(k, len(arr)):
    window += arr[i] - arr[i - k]
    res = max(res, window)

# --- Variable Size Window ---
l = 0
cur = 0
res = 0
for r in range(len(arr)):
    cur += arr[r]                   # expand window
    while cur > limit:              # shrink until valid
        cur -= arr[l]
        l += 1
    res = max(res, r - l + 1)      # r - l + 1 = window length

# --- Window with Frequency Map (e.g. longest unique substring) ---
from collections import defaultdict
freq = defaultdict(int)
l = 0
res = 0
for r in range(len(s)):
    freq[s[r]] += 1
    while freq[s[r]] > 1:          # shrink while invalid
        freq[s[l]] -= 1
        l += 1
    res = max(res, r - l + 1)
```

---

## 06 Binary Search

```python
# --- Standard Template ---
l, r = 0, len(arr) - 1
while l <= r:
    m = (l + r) // 2
    if arr[m] == target:
        return m
    elif arr[m] < target:
        l = m + 1
    else:
        r = m - 1
return -1

# --- Find Leftmost / Rightmost ---
# leftmost index where arr[i] >= target
l, r = 0, len(arr)
while l < r:
    m = (l + r) // 2
    if arr[m] < target:
        l = m + 1
    else:
        r = m
return l   # l == r is insertion point

# --- bisect module ---
import bisect
bisect.bisect_left(arr, x)    # leftmost index for x
bisect.bisect_right(arr, x)   # rightmost index + 1
bisect.insort(arr, x)         # insert maintaining sort order

# --- Search on Answer Space ---
def feasible(mid): ...

l, r = lo, hi
while l < r:
    m = (l + r) // 2
    if feasible(m):
        r = m
    else:
        l = m + 1
# l is the minimum value satisfying feasible()
```

> **Tip:** Use `l < r` (not `<=`) when you're converging on a boundary, not a value.

---

## 07 Stack & Queue

```python
from collections import deque

# --- Stack (use list) ---
stack = []
stack.append(x)    # push O(1)
stack.pop()        # pop  O(1)
stack[-1]          # peek
if not stack: ...

# --- Queue (use deque) ---
q = deque()
q.append(x)        # enqueue right  O(1)
q.appendleft(x)    # enqueue left   O(1)
q.popleft()        # dequeue left   O(1)
q.pop()            # dequeue right  O(1)
q[0]               # peek left

# --- Monotonic Stack (next greater element) ---
stack = []   # stores indices; maintains decreasing values
res = [-1] * len(arr)
for i in range(len(arr)):
    while stack and arr[stack[-1]] < arr[i]:
        j = stack.pop()
        res[j] = arr[i]     # arr[i] is next greater for arr[j]
    stack.append(i)

# --- Min Stack ---
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []
    def push(self, val):
        self.stack.append(val)
        self.min_stack.append(min(val, self.min_stack[-1] if self.min_stack else val))
    def pop(self):
        self.stack.pop(); self.min_stack.pop()
    def getMin(self):
        return self.min_stack[-1]
```

---

## 08 Heap / Priority Queue

```python
import heapq

# --- Min-Heap (default) ---
h = []
heapq.heappush(h, val)
heapq.heappop(h)          # removes and returns min
h[0]                       # peek min (no removal)
heapq.heapify(arr)         # convert list in-place O(n)

# --- Max-Heap (negate values) ---
heapq.heappush(h, -val)
max_val = -heapq.heappop(h)

# --- Heap of Tuples (tie-breaking / multi-key) ---
heapq.heappush(h, (dist, node))
heapq.heappush(h, (priority, idx, val))

# --- K Largest / Smallest ---
heapq.nlargest(k, arr)          # O(n log k)
heapq.nsmallest(k, arr)

# --- Fixed-size max-heap trick (k smallest) ---
h = []
for x in arr:
    heapq.heappush(h, -x)
    if len(h) > k:
        heapq.heappop(h)        # drop the largest
return [-x for x in h]          # k smallest remain
```

---

## 09 Linked List

```python
# --- Node Definition ---
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# --- Dummy Head (simplifies edge cases) ---
dummy = ListNode(0)
dummy.next = head
cur = dummy
# ... manipulate list ...
return dummy.next

# --- Reverse a Linked List ---
prev = None
cur = head
while cur:
    nxt = cur.next
    cur.next = prev
    prev = cur
    cur = nxt
return prev

# --- Fast / Slow Pointers ---
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
# slow is now at the middle

# --- Detect Cycle ---
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
    if slow == fast:
        return True
return False

# --- Find Cycle Start ---
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
    if slow == fast:
        slow = head
        while slow != fast:
            slow = slow.next
            fast = fast.next
        return slow     # cycle start node
return None
```

---

## 10 Trees

```python
from collections import deque

# --- Node Definition ---
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# --- DFS Recursive ---
def dfs(node):
    if not node:
        return
    # preorder:  process here
    dfs(node.left)
    # inorder:   process here
    dfs(node.right)
    # postorder: process here

# --- DFS Iterative (inorder) ---
stack, res = [], []
cur = root
while cur or stack:
    while cur:
        stack.append(cur)
        cur = cur.left
    cur = stack.pop()
    res.append(cur.val)
    cur = cur.right

# --- BFS Level Order ---
q = deque([root])
while q:
    for _ in range(len(q)):        # iterate level by level
        node = q.popleft()
        if node.left:  q.append(node.left)
        if node.right: q.append(node.right)

# --- Height / Depth ---
def height(node):
    if not node:
        return 0
    return 1 + max(height(node.left), height(node.right))

# --- Lowest Common Ancestor ---
def lca(root, p, q):
    if not root or root == p or root == q:
        return root
    left  = lca(root.left, p, q)
    right = lca(root.right, p, q)
    return root if left and right else left or right

# --- Validate BST ---
def is_valid(node, lo=float('-inf'), hi=float('inf')):
    if not node:
        return True
    if not (lo < node.val < hi):
        return False
    return is_valid(node.left, lo, node.val) and \
           is_valid(node.right, node.val, hi)
```

---

## 11 Graphs

```python
from collections import defaultdict, deque
import heapq

# --- Build Adjacency List ---
graph = defaultdict(list)
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)     # omit for directed

# --- DFS Iterative ---
visited = set()
stack = [start]
while stack:
    node = stack.pop()
    if node in visited:
        continue
    visited.add(node)
    for nb in graph[node]:
        stack.append(nb)

# --- DFS Recursive ---
def dfs(node, visited):
    visited.add(node)
    for nb in graph[node]:
        if nb not in visited:
            dfs(nb, visited)

# --- BFS Shortest Path (unweighted) ---
q = deque([(start, 0)])
visited = {start}
while q:
    node, dist = q.popleft()
    if node == end:
        return dist
    for nb in graph[node]:
        if nb not in visited:
            visited.add(nb)
            q.append((nb, dist + 1))

# --- Dijkstra (weighted shortest path) ---
dist = {node: float('inf') for node in graph}
dist[src] = 0
pq = [(0, src)]
while pq:
    d, u = heapq.heappop(pq)
    if d > dist[u]:
        continue
    for v, w in graph[u]:
        if dist[u] + w < dist[v]:
            dist[v] = dist[u] + w
            heapq.heappush(pq, (dist[v], v))

# --- Union-Find (with path compression + rank) ---
parent = list(range(n))
rank   = [0] * n

def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])   # path compression
    return parent[x]

def union(a, b):
    a, b = find(a), find(b)
    if a == b:
        return False
    if rank[a] < rank[b]:
        a, b = b, a
    parent[b] = a
    if rank[a] == rank[b]:
        rank[a] += 1
    return True

# --- Topological Sort (Kahn's BFS) ---
indeg = [0] * n
for u, v in edges:
    indeg[v] += 1
q = deque([i for i in range(n) if indeg[i] == 0])
order = []
while q:
    u = q.popleft()
    order.append(u)
    for v in graph[u]:
        indeg[v] -= 1
        if indeg[v] == 0:
            q.append(v)
# if len(order) != n → cycle exists

# --- Grid BFS (4-directional) ---
directions = [(0,1),(0,-1),(1,0),(-1,0)]
visited = set()
q = deque([(r, c)])
visited.add((r, c))
while q:
    row, col = q.popleft()
    for dr, dc in directions:
        nr, nc = row + dr, col + dc
        if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
            visited.add((nr, nc))
            q.append((nr, nc))
```

---

## 12 Dynamic Programming

```python
from functools import lru_cache

# --- 1D DP ---
dp = [0] * (n + 1)
dp[0] = base_case
for i in range(1, n + 1):
    dp[i] = f(dp[i-1], ...)

# --- 2D DP ---
dp = [[0] * (n + 1) for _ in range(m + 1)]
for i in range(1, m + 1):
    for j in range(1, n + 1):
        dp[i][j] = f(dp[i-1][j], dp[i][j-1], ...)

# --- Memoization (top-down) ---
@lru_cache(maxsize=None)
def dp(i, j):
    if i == 0:
        return base
    return max(dp(i-1, j), dp(i, j-1), ...)

# clear cache if needed: dp.cache_clear()

# --- 0/1 Knapsack ---
dp = [0] * (cap + 1)
for w, v in items:
    for j in range(cap, w - 1, -1):   # iterate backwards!
        dp[j] = max(dp[j], dp[j - w] + v)

# --- Unbounded Knapsack ---
dp = [0] * (cap + 1)
for w, v in items:
    for j in range(w, cap + 1):       # iterate forwards
        dp[j] = max(dp[j], dp[j - w] + v)

# --- Longest Common Subsequence ---
dp = [[0] * (n + 1) for _ in range(m + 1)]
for i in range(1, m + 1):
    for j in range(1, n + 1):
        if s[i-1] == t[j-1]:
            dp[i][j] = dp[i-1][j-1] + 1
        else:
            dp[i][j] = max(dp[i-1][j], dp[i][j-1])

# --- Coin Change (min coins) ---
dp = [float('inf')] * (amount + 1)
dp[0] = 0
for coin in coins:
    for j in range(coin, amount + 1):
        dp[j] = min(dp[j], dp[j - coin] + 1)
```

> **Tip:** If a recursive solution is clear, add `@lru_cache` first. Only convert to bottom-up if you hit recursion depth limits or need space optimization.

---

## 13 Sorting & Math

```python
import math

# --- Sort Tricks ---
arr.sort(key=lambda x: (x[0], -x[1]))         # multi-key sort
sorted(d.items(), key=lambda x: x[1])          # sort dict by value
sorted(arr, key=abs)                            # sort by absolute value

# --- Math Operators ---
x // y              # floor division
x % y               # modulo
x ** y              # power
abs(x)
divmod(x, y)        # returns (quotient, remainder)
float('inf'), float('-inf')

# --- math module ---
math.gcd(a, b)
math.lcm(a, b)           # Python 3.9+
math.ceil(x)
math.floor(x)
math.sqrt(x)
math.log(x, base)
math.isqrt(x)            # integer square root

# --- Prefix Sum ---
prefix = [0] * (len(arr) + 1)
for i, v in enumerate(arr):
    prefix[i + 1] = prefix[i] + v
# sum of arr[l..r] = prefix[r+1] - prefix[l]

# --- Prefix Product ---
left  = [1] * n
right = [1] * n
for i in range(1, n):
    left[i] = left[i-1] * arr[i-1]
for i in range(n - 2, -1, -1):
    right[i] = right[i+1] * arr[i+1]
# product except self at i = left[i] * right[i]

# --- GCD / LCM ---
from math import gcd
lcm = lambda a, b: a * b // gcd(a, b)

# --- Prime Sieve ---
def sieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(n + 1) if is_prime[i]]
```

---

## 14 Bit Tricks

```python
# --- Operators ---
a & b        # AND
a | b        # OR
a ^ b        # XOR
~a           # NOT (bitwise complement)
a << k       # left shift  = a * 2^k
a >> k       # right shift = a // 2^k

# --- Common Patterns ---
n & 1                   # is odd?
n & (n - 1) == 0        # is power of 2?
n & (-n)                # isolate lowest set bit
n & ~(n - 1)            # same as above
n ^ n == 0              # XOR with self = 0
a ^ b ^ b == a          # XOR cancels pairs (find missing number)

# --- Check / Set / Clear / Toggle bit k ---
(n >> k) & 1            # check bit k
n | (1 << k)            # set bit k
n & ~(1 << k)           # clear bit k
n ^ (1 << k)            # toggle bit k

# --- Count / Inspect ---
bin(n)                  # '0b1010'
bin(n).count('1')       # popcount (number of set bits)
n.bit_length()          # floor(log2(n)) + 1

# --- XOR tricks ---
# Find the one number that appears once (all others appear twice):
result = 0
for x in arr:
    result ^= x

# Find two unique numbers among pairs:
xor = 0
for x in arr: xor ^= x             # xor = a ^ b
bit = xor & (-xor)                  # rightmost differing bit
a = b = 0
for x in arr:
    if x & bit: a ^= x
    else: b ^= x
```

---

*Generated for use in a LeetCode solutions repo. Each section maps to a common problem-solving pattern.*