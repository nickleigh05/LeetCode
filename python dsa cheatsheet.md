# Python DSA Cheat Sheet (LeetCode)

## Lists (Arrays / Stacks)

```python
a = [1, 2, 3]

# Access / slice
a[0], a[-1]        # first, last
a[1:3]             # [2, 3]
a[::-1]            # reversed

# Mutate
a.append(4)        # add to end
a.pop()            # remove from end  O(1)
a.pop(0)           # remove from front O(n) — use deque instead
a.insert(1, 99)    # insert at index
a.remove(2)        # remove first occurrence of value

# Useful
len(a)
a.sort()                          # in-place
sorted(a)                         # returns new
a.sort(key=lambda x: -x)          # custom sort
min(a), max(a), sum(a)
a.count(2)
a.index(2)                        # first index of value
x in a                            # membership  O(n)

# Initialize
a = [0] * 5                       # [0, 0, 0, 0, 0]
a = [[0]*3 for _ in range(3)]     # 2D grid — don't use [[0]*3]*3
```

---

## Deque (Queue / Double-ended)

```python
from collections import deque

q = deque([1, 2, 3])
q.append(4)       # add right
q.appendleft(0)   # add left
q.pop()           # remove right  O(1)
q.popleft()       # remove left   O(1)  ← use this over list.pop(0)
len(q)
q[0], q[-1]       # peek both ends
```

---

## HashMap (dict)

```python
d = {}
d = {"a": 1}

d["a"] = 2          # set
d.get("b", 0)       # get with default
"a" in d            # key exists
del d["a"]          # delete key

d.keys(), d.values(), d.items()

for k, v in d.items():
    pass

# Very common pattern
d[key] = d.get(key, 0) + 1   # frequency count
```

---

## defaultdict & Counter

```python
from collections import defaultdict, Counter

# defaultdict — no KeyError on missing keys
d = defaultdict(int)     # default 0
d = defaultdict(list)    # default []
d["x"] += 1
d["y"].append(5)

# Counter — frequency map shortcut
c = Counter([1, 1, 2, 3])  # Counter({1: 2, 2: 1, 3: 1})
c["z"]                      # 0, no KeyError
c.most_common(2)            # top 2 frequent
```

---

## HashSet

```python
s = set()
s = {1, 2, 3}

s.add(4)
s.remove(4)      # raises if missing
s.discard(4)     # safe remove
x in s           # O(1) lookup

# Set ops
a | b   # union
a & b   # intersection
a - b   # difference
a ^ b   # symmetric difference
```

---

## Heap (Priority Queue)

```python
import heapq

# Min-heap by default
h = []
heapq.heappush(h, 3)
heapq.heappush(h, 1)
heapq.heappop(h)     # returns 1 (smallest)
h[0]                 # peek min without popping

# Build heap from list
heapq.heapify(h)

# Max-heap trick — negate values
heapq.heappush(h, -val)
-heapq.heappop(h)

# Heap of tuples — sorts by first element
heapq.heappush(h, (priority, value))
```

---

## String

```python
s = "hello"

s[0], s[-1], s[1:4]
len(s)
s.upper(), s.lower()
s.strip()           # remove whitespace
s.split(" ")        # → list
" ".join(["a","b"]) # → "a b"
s.replace("l","r")
s.startswith("he"), s.endswith("lo")
s.isdigit(), s.isalpha(), s.isalnum()
ord("a")  # → 97
chr(97)   # → "a"

# Strings are immutable — build with list then join
parts = []
parts.append("x")
"".join(parts)
```

---

## Tuple

```python
t = (1, 2)
t[0]          # access
a, b = t      # unpack

# Common use: hashable key in dict/set
seen = set()
seen.add((row, col))   # coordinate pairs
```

---

## Patterns

### Two Pointers

```python
l, r = 0, len(a) - 1
while l < r:
    # do something
    l += 1
    r -= 1
```

### Sliding Window

```python
l = 0
for r in range(len(a)):
    # expand window
    while condition:
        # shrink window
        l += 1
```

### Fast / Slow Pointers (Linked List)

```python
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
```

### Binary Search

```python
l, r = 0, len(a) - 1
while l <= r:
    mid = (l + r) // 2
    if a[mid] == target:
        return mid
    elif a[mid] < target:
        l = mid + 1
    else:
        r = mid - 1
```

### DFS (recursive)

```python
def dfs(node):
    if not node:
        return
    dfs(node.left)
    dfs(node.right)
```

### BFS

```python
from collections import deque
q = deque([start])
visited = set([start])
while q:
    node = q.popleft()
    for neighbor in graph[node]:
        if neighbor not in visited:
            visited.add(neighbor)
            q.append(neighbor)
```

---

## Miscellaneous

```python
# Enumerate
for i, val in enumerate(a):
    pass

# Zip
for x, y in zip(a, b):
    pass

# List comprehension
[x*2 for x in a if x > 0]

# Infinity
float("inf"), float("-inf")

# Integer division / modulo
7 // 2   # 3
7 % 2    # 1

# Multiple assignment
a, b = b, a      # swap
a = b = 0        # both zero

# Ternary
x = val if condition else other
```