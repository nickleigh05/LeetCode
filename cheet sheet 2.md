# 🐍 Python LeetCode Cheat Sheet — Vol. 2

> Covers advanced patterns not in Vol. 1: backtracking, tries, intervals, greedy, advanced DP, advanced graphs, segment trees, and more.

---

## Table of Contents

| # | Section |
|---|---------|
| 01 | [Backtracking](#01-backtracking) |
| 02 | [Tries](#02-tries) |
| 03 | [Intervals](#03-intervals) |
| 04 | [Greedy](#04-greedy) |
| 05 | [Monotonic Queue](#05-monotonic-queue) |
| 06 | [Advanced Trees](#06-advanced-trees) |
| 07 | [Advanced Graphs](#07-advanced-graphs) |
| 08 | [Advanced DP](#08-advanced-dp) |
| 09 | [Segment Tree & BIT](#09-segment-tree--bit) |
| 10 | [Math & Number Theory](#10-math--number-theory) |
| 11 | [Recursion & Divide and Conquer](#11-recursion--divide-and-conquer) |
| 12 | [Pattern Recognition Guide](#12-pattern-recognition-guide) |

---

## 01 Backtracking

> Template: choose → recurse → unchoose. Prune early to cut branches.

```python
# --- Generic Backtracking Template ---
def backtrack(start, path):
    if is_solution(path):
        res.append(path[:])   # snapshot — never append path directly
        return
    for choice in choices(start):
        if not is_valid(choice):
            continue
        path.append(choice)       # choose
        backtrack(next, path)     # recurse
        path.pop()                # unchoose

# --- Subsets (no duplicates in input) ---
def subsets(nums):
    res = []
    def bt(start, path):
        res.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            bt(i + 1, path)
            path.pop()
    bt(0, [])
    return res

# --- Subsets II (duplicates in input) ---
def subsets_with_dup(nums):
    res = []
    nums.sort()
    def bt(start, path):
        res.append(path[:])
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i-1]:
                continue           # skip duplicate branches
            path.append(nums[i])
            bt(i + 1, path)
            path.pop()
    bt(0, [])
    return res

# --- Permutations (no duplicates) ---
def permutations(nums):
    res = []
    def bt(path, used):
        if len(path) == len(nums):
            res.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            used[i] = True
            path.append(nums[i])
            bt(path, used)
            path.pop()
            used[i] = False
    bt([], [False] * len(nums))
    return res

# --- Permutations II (duplicates in input) ---
def permutations_with_dup(nums):
    res = []
    nums.sort()
    def bt(path, used):
        if len(path) == len(nums):
            res.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            if i > 0 and nums[i] == nums[i-1] and not used[i-1]:
                continue           # skip same-level duplicates
            used[i] = True
            path.append(nums[i])
            bt(path, used)
            path.pop()
            used[i] = False
    bt([], [False] * len(nums))
    return res

# --- Combination Sum (reuse allowed) ---
def combination_sum(candidates, target):
    res = []
    candidates.sort()
    def bt(start, path, remaining):
        if remaining == 0:
            res.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break              # pruning: sorted, no point continuing
            path.append(candidates[i])
            bt(i, path, remaining - candidates[i])   # i not i+1 = reuse
            path.pop()
    bt(0, [], target)
    return res

# --- N-Queens ---
def solve_n_queens(n):
    res = []
    cols = set()
    diag1 = set()   # row - col
    diag2 = set()   # row + col

    def bt(row, board):
        if row == n:
            res.append(["".join(r) for r in board])
            return
        for col in range(n):
            if col in cols or (row-col) in diag1 or (row+col) in diag2:
                continue
            cols.add(col); diag1.add(row-col); diag2.add(row+col)
            board[row][col] = 'Q'
            bt(row + 1, board)
            board[row][col] = '.'
            cols.remove(col); diag1.remove(row-col); diag2.remove(row+col)

    bt(0, [['.']*n for _ in range(n)])
    return res

# --- Word Search (grid backtracking) ---
def exist(board, word):
    rows, cols = len(board), len(board[0])
    visited = set()

    def bt(r, c, idx):
        if idx == len(word):
            return True
        if not (0 <= r < rows and 0 <= c < cols):
            return False
        if board[r][c] != word[idx] or (r, c) in visited:
            return False
        visited.add((r, c))
        found = any(bt(r+dr, c+dc, idx+1) for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)])
        visited.remove((r, c))
        return found

    return any(bt(r, c, 0) for r in range(rows) for c in range(cols))
```

> **Tip:** Always append `path[:]` (a copy), never `path` itself. Appending the reference means all stored results will reflect the final state of `path`.

---

## 02 Tries

```python
# --- Trie Node ---
class TrieNode:
    def __init__(self):
        self.children = {}       # char → TrieNode
        self.is_end = False

# --- Trie ---
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

# --- Array-based children (faster for a-z only) ---
class TrieNodeArr:
    def __init__(self):
        self.children = [None] * 26
        self.is_end = False

    def get(self, ch):
        return self.children[ord(ch) - ord('a')]

    def put(self, ch, node):
        self.children[ord(ch) - ord('a')] = node

# --- Word Search II (Trie + backtracking) ---
def find_words(board, words):
    root = TrieNode()
    for w in words:
        node = root
        for ch in w:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True        # store word at end node

    res = set()
    rows, cols = len(board), len(board[0])

    def dfs(r, c, node, path):
        ch = board[r][c]
        if ch not in node.children:
            return
        nxt = node.children[ch]
        path += ch
        if nxt.is_end:
            res.add(path)
        board[r][c] = '#'         # mark visited
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != '#':
                dfs(nr, nc, nxt, path)
        board[r][c] = ch          # restore

    for r in range(rows):
        for c in range(cols):
            dfs(r, c, root, "")
    return list(res)
```

---

## 03 Intervals

```python
# --- Merge Overlapping Intervals ---
def merge(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged

# --- Insert Interval ---
def insert(intervals, new):
    res = []
    i = 0
    n = len(intervals)
    # add all intervals that end before new starts
    while i < n and intervals[i][1] < new[0]:
        res.append(intervals[i]); i += 1
    # merge overlapping
    while i < n and intervals[i][0] <= new[1]:
        new[0] = min(new[0], intervals[i][0])
        new[1] = max(new[1], intervals[i][1])
        i += 1
    res.append(new)
    res.extend(intervals[i:])
    return res

# --- Non-overlapping Intervals (min removals) ---
def erase_overlap(intervals):
    intervals.sort(key=lambda x: x[1])   # sort by end
    count = 0
    prev_end = float('-inf')
    for start, end in intervals:
        if start >= prev_end:
            prev_end = end
        else:
            count += 1            # overlap — remove this one
    return count

# --- Meeting Rooms II (min rooms needed) ---
import heapq
def min_meeting_rooms(intervals):
    intervals.sort(key=lambda x: x[0])
    heap = []                     # stores end times
    for start, end in intervals:
        if heap and heap[0] <= start:
            heapq.heapreplace(heap, end)
        else:
            heapq.heappush(heap, end)
    return len(heap)

# --- Sweep Line (count max overlaps) ---
def max_overlap(intervals):
    events = []
    for s, e in intervals:
        events.append((s, 1))
        events.append((e, -1))
    events.sort()
    cur = res = 0
    for _, delta in events:
        cur += delta
        res = max(res, cur)
    return res
```

---

## 04 Greedy

> Greedy works when a locally optimal choice leads to a globally optimal solution. Usually requires sorting first.

```python
# --- Jump Game (can reach end?) ---
def can_jump(nums):
    reach = 0
    for i, n in enumerate(nums):
        if i > reach:
            return False
        reach = max(reach, i + n)
    return True

# --- Jump Game II (min jumps) ---
def jump(nums):
    jumps = cur_end = cur_far = 0
    for i in range(len(nums) - 1):
        cur_far = max(cur_far, i + nums[i])
        if i == cur_end:
            jumps += 1
            cur_end = cur_far
    return jumps

# --- Gas Station ---
def can_complete_circuit(gas, cost):
    if sum(gas) < sum(cost):
        return -1
    tank = start = 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:
            start = i + 1
            tank = 0
    return start

# --- Task Scheduler ---
from collections import Counter
import heapq
def least_interval(tasks, n):
    freq = Counter(tasks)
    heap = [-f for f in freq.values()]
    heapq.heapify(heap)
    time = 0
    q = deque()                   # (count, available_at)
    while heap or q:
        time += 1
        if heap:
            cnt = heapq.heappop(heap) + 1
            if cnt:
                q.append((cnt, time + n))
        if q and q[0][1] == time:
            heapq.heappush(heap, q.popleft()[0])
    return time

# --- Partition Labels ---
def partition_labels(s):
    last = {ch: i for i, ch in enumerate(s)}
    res = []
    start = end = 0
    for i, ch in enumerate(s):
        end = max(end, last[ch])
        if i == end:
            res.append(end - start + 1)
            start = end + 1
    return res

# --- Activity Selection (max non-overlapping) ---
def activity_selection(intervals):
    intervals.sort(key=lambda x: x[1])   # sort by end time
    count = 1
    prev_end = intervals[0][1]
    for start, end in intervals[1:]:
        if start >= prev_end:
            count += 1
            prev_end = end
    return count
```

---

## 05 Monotonic Queue

> Used for sliding window maximum/minimum in O(n). The deque stores indices and maintains a monotonic order of values.

```python
from collections import deque

# --- Sliding Window Maximum ---
def max_sliding_window(nums, k):
    dq = deque()    # stores indices; front = max
    res = []
    for i, n in enumerate(nums):
        # remove indices outside window
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        # maintain decreasing order (pop smaller from back)
        while dq and nums[dq[-1]] < n:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            res.append(nums[dq[0]])
    return res

# --- Sliding Window Minimum (flip comparison) ---
def min_sliding_window(nums, k):
    dq = deque()    # front = min
    res = []
    for i, n in enumerate(nums):
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        while dq and nums[dq[-1]] > n:   # pop larger from back
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            res.append(nums[dq[0]])
    return res

# --- Largest Rectangle in Histogram (monotonic stack) ---
def largest_rectangle(heights):
    stack = []    # stores indices; maintains increasing heights
    res = 0
    heights.append(0)   # sentinel to flush remaining stack
    for i, h in enumerate(heights):
        start = i
        while stack and heights[stack[-1]] > h:
            idx = stack.pop()
            width = i - (stack[-1] + 1 if stack else 0)
            res = max(res, heights[idx] * width)
            start = idx
        stack.append(start)
    return res
```

---

## 06 Advanced Trees

```python
# --- N-ary Tree ---
class Node:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children or []

def n_ary_level_order(root):
    if not root: return []
    res, q = [], deque([root])
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            q.extend(node.children)
        res.append(level)
    return res

# --- Serialize / Deserialize Binary Tree ---
def serialize(root):
    res = []
    def dfs(node):
        if not node:
            res.append('N'); return
        res.append(str(node.val))
        dfs(node.left); dfs(node.right)
    dfs(root)
    return ','.join(res)

def deserialize(data):
    vals = iter(data.split(','))
    def dfs():
        v = next(vals)
        if v == 'N': return None
        node = TreeNode(int(v))
        node.left = dfs(); node.right = dfs()
        return node
    return dfs()

# --- Morris Traversal (inorder, O(1) space) ---
def morris_inorder(root):
    res = []
    cur = root
    while cur:
        if not cur.left:
            res.append(cur.val)
            cur = cur.right
        else:
            prev = cur.left
            while prev.right and prev.right != cur:
                prev = prev.right
            if not prev.right:
                prev.right = cur    # thread
                cur = cur.left
            else:
                prev.right = None   # unthread
                res.append(cur.val)
                cur = cur.right
    return res

# --- Diameter of Binary Tree ---
def diameter(root):
    res = [0]
    def depth(node):
        if not node: return 0
        l, r = depth(node.left), depth(node.right)
        res[0] = max(res[0], l + r)
        return 1 + max(l, r)
    depth(root)
    return res[0]

# --- Path Sum (root to leaf) ---
def has_path_sum(root, target):
    if not root: return False
    if not root.left and not root.right:
        return root.val == target
    return has_path_sum(root.left, target - root.val) or \
           has_path_sum(root.right, target - root.val)
```

---

## 07 Advanced Graphs

```python
# --- Bellman-Ford (handles negative weights) ---
def bellman_ford(n, edges, src):
    dist = [float('inf')] * n
    dist[src] = 0
    for _ in range(n - 1):          # relax n-1 times
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    # check for negative cycle
    for u, v, w in edges:
        if dist[u] + w < dist[v]:
            return None             # negative cycle exists
    return dist

# --- Floyd-Warshall (all-pairs shortest path) ---
def floyd_warshall(n, edges):
    dist = [[float('inf')] * n for _ in range(n)]
    for i in range(n): dist[i][i] = 0
    for u, v, w in edges:
        dist[u][v] = w
    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    return dist

# --- Prim's MST ---
def prims(n, graph):
    visited = set([0])
    heap = [(w, 0, v) for v, w in graph[0]]
    heapq.heapify(heap)
    total = 0
    while heap and len(visited) < n:
        w, u, v = heapq.heappop(heap)
        if v in visited: continue
        visited.add(v)
        total += w
        for nb, weight in graph[v]:
            if nb not in visited:
                heapq.heappush(heap, (weight, v, nb))
    return total

# --- Kruskal's MST ---
def kruskals(n, edges):
    edges.sort(key=lambda x: x[2])     # sort by weight
    parent = list(range(n))
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    total = 0
    for u, v, w in edges:
        pu, pv = find(u), find(v)
        if pu == pv: continue           # skip cycle
        parent[pu] = pv
        total += w
    return total

# --- Bipartite Check (2-coloring via BFS) ---
def is_bipartite(graph):
    color = {}
    for start in range(len(graph)):
        if start in color: continue
        q = deque([start])
        color[start] = 0
        while q:
            node = q.popleft()
            for nb in graph[node]:
                if nb not in color:
                    color[nb] = 1 - color[node]
                    q.append(nb)
                elif color[nb] == color[node]:
                    return False
    return True

# --- Strongly Connected Components (Kosaraju's) ---
def scc(n, graph):
    visited = set()
    order = []
    def dfs1(u):
        visited.add(u)
        for v in graph[u]: 
            if v not in visited: dfs1(v)
        order.append(u)

    rev = defaultdict(list)
    for u in graph:
        for v in graph[u]: rev[v].append(u)

    for i in range(n):
        if i not in visited: dfs1(i)

    visited.clear()
    components = []
    def dfs2(u, comp):
        visited.add(u)
        comp.append(u)
        for v in rev[u]:
            if v not in visited: dfs2(v, comp)

    while order:
        u = order.pop()
        if u not in visited:
            comp = []
            dfs2(u, comp)
            components.append(comp)
    return components
```

---

## 08 Advanced DP

```python
from functools import lru_cache

# --- Longest Increasing Subsequence O(n log n) ---
import bisect
def lis(nums):
    tails = []
    for n in nums:
        idx = bisect.bisect_left(tails, n)
        if idx == len(tails):
            tails.append(n)
        else:
            tails[idx] = n
    return len(tails)

# --- Edit Distance ---
def edit_distance(s, t):
    m, n = len(s), len(t)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1): dp[i][0] = i
    for j in range(n + 1): dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s[i-1] == t[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    return dp[m][n]

# --- Palindrome DP (longest palindromic substring) ---
def longest_palindrome(s):
    n = len(s)
    res = s[0]
    def expand(l, r):
        nonlocal res
        while l >= 0 and r < n and s[l] == s[r]:
            if r - l + 1 > len(res):
                res = s[l:r+1]
            l -= 1; r += 1
    for i in range(n):
        expand(i, i)      # odd length
        expand(i, i + 1)  # even length
    return res

# --- Palindromic Substrings (count all) ---
def count_substrings(s):
    count = 0
    def expand(l, r):
        nonlocal count
        while l >= 0 and r < len(s) and s[l] == s[r]:
            count += 1; l -= 1; r += 1
    for i in range(len(s)):
        expand(i, i); expand(i, i + 1)
    return count

# --- Bitmask DP (e.g. TSP / assign tasks) ---
# dp[mask][i] = min cost to have visited set 'mask', ending at node i
n = 4
dp = [[float('inf')] * n for _ in range(1 << n)]
dp[1][0] = 0   # start at node 0
for mask in range(1 << n):
    for u in range(n):
        if not (mask >> u & 1) or dp[mask][u] == float('inf'):
            continue
        for v in range(n):
            if mask >> v & 1:
                continue
            nmask = mask | (1 << v)
            dp[nmask][v] = min(dp[nmask][v], dp[mask][u] + cost[u][v])

# --- Interval DP (e.g. burst balloons) ---
def max_coins(nums):
    nums = [1] + nums + [1]
    n = len(nums)
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n):
        for l in range(0, n - length):
            r = l + length
            for k in range(l + 1, r):
                dp[l][r] = max(dp[l][r],
                    nums[l] * nums[k] * nums[r] + dp[l][k] + dp[k][r])
    return dp[0][n-1]

# --- DP on Trees (max path sum) ---
def max_path_sum(root):
    res = [root.val]
    def dfs(node):
        if not node: return 0
        l = max(dfs(node.left), 0)
        r = max(dfs(node.right), 0)
        res[0] = max(res[0], node.val + l + r)
        return node.val + max(l, r)
    dfs(root)
    return res[0]

# --- Stock Problems ---
# At most k transactions
def max_profit_k(k, prices):
    n = len(prices)
    if k >= n // 2:
        return sum(max(prices[i+1]-prices[i], 0) for i in range(n-1))
    dp = [[0]*n for _ in range(k+1)]
    for t in range(1, k+1):
        max_so_far = -prices[0]
        for d in range(1, n):
            dp[t][d] = max(dp[t][d-1], prices[d] + max_so_far)
            max_so_far = max(max_so_far, dp[t-1][d] - prices[d])
    return dp[k][n-1]
```

---

## 09 Segment Tree & BIT

```python
# --- Binary Indexed Tree / Fenwick Tree ---
# Point update, prefix sum query — O(log n)
class BIT:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)

    def update(self, i, delta):       # i is 1-indexed
        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)             # add lowest set bit

    def query(self, i):               # prefix sum [1..i]
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)             # remove lowest set bit
        return s

    def range_query(self, l, r):      # sum [l..r], 1-indexed
        return self.query(r) - self.query(l - 1)

# --- Segment Tree (range sum, point update) ---
class SegTree:
    def __init__(self, nums):
        self.n = len(nums)
        self.tree = [0] * (2 * self.n)
        # build
        for i, v in enumerate(nums):
            self.tree[self.n + i] = v
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.tree[2*i] + self.tree[2*i+1]

    def update(self, i, val):         # 0-indexed
        i += self.n
        self.tree[i] = val
        while i > 1:
            i //= 2
            self.tree[i] = self.tree[2*i] + self.tree[2*i+1]

    def query(self, l, r):            # sum [l, r), 0-indexed
        res = 0
        l += self.n; r += self.n
        while l < r:
            if l & 1:
                res += self.tree[l]; l += 1
            if r & 1:
                r -= 1; res += self.tree[r]
            l >>= 1; r >>= 1
        return res

# --- Segment Tree with Lazy Propagation (range update) ---
class LazySegTree:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (4 * n)
        self.lazy = [0] * (4 * n)

    def push_down(self, node, l, r):
        if self.lazy[node]:
            mid = (l + r) // 2
            self.tree[2*node]   += self.lazy[node] * (mid - l + 1)
            self.tree[2*node+1] += self.lazy[node] * (r - mid)
            self.lazy[2*node]   += self.lazy[node]
            self.lazy[2*node+1] += self.lazy[node]
            self.lazy[node] = 0

    def update(self, node, l, r, ql, qr, val):
        if ql <= l and r <= qr:
            self.tree[node] += val * (r - l + 1)
            self.lazy[node] += val
            return
        self.push_down(node, l, r)
        mid = (l + r) // 2
        if ql <= mid: self.update(2*node, l, mid, ql, qr, val)
        if qr > mid:  self.update(2*node+1, mid+1, r, ql, qr, val)
        self.tree[node] = self.tree[2*node] + self.tree[2*node+1]

    def query(self, node, l, r, ql, qr):
        if ql <= l and r <= qr:
            return self.tree[node]
        self.push_down(node, l, r)
        mid = (l + r) // 2
        res = 0
        if ql <= mid: res += self.query(2*node, l, mid, ql, qr)
        if qr > mid:  res += self.query(2*node+1, mid+1, r, ql, qr)
        return res
```

---

## 10 Math & Number Theory

```python
import math
from functools import reduce

# --- Modular Arithmetic ---
MOD = 10**9 + 7
(a + b) % MOD
(a * b) % MOD
pow(a, b, MOD)              # fast modular exponentiation O(log b)

# --- Modular Inverse (Fermat's little theorem, MOD must be prime) ---
inv = pow(a, MOD - 2, MOD)

# --- Combinatorics (nCr mod p) ---
def precompute(n, MOD):
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i-1] * i % MOD
    inv_fact = [1] * (n + 1)
    inv_fact[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n - 1, -1, -1):
        inv_fact[i] = inv_fact[i+1] * (i+1) % MOD
    return fact, inv_fact

def nCr(n, r, fact, inv_fact, MOD):
    if r < 0 or r > n: return 0
    return fact[n] * inv_fact[r] % MOD * inv_fact[n-r] % MOD

# --- GCD / LCM ---
math.gcd(a, b)
math.lcm(a, b)                          # Python 3.9+
reduce(math.gcd, arr)                   # GCD of array
reduce(math.lcm, arr)                   # LCM of array

# --- Integer Square Root / Perfect Square ---
math.isqrt(n)                           # floor sqrt, exact
int(n**0.5)                             # float — avoid for exact checks
n == math.isqrt(n) ** 2                 # is perfect square?

# --- Prime Check ---
def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0: return False
        i += 6
    return True

# --- Prime Factorization ---
def prime_factors(n):
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1: factors.append(n)
    return factors

# --- Sieve of Eratosthenes ---
def sieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(n + 1) if is_prime[i]]

# --- Base Conversion ---
bin(n), oct(n), hex(n)                  # to string
int('1010', 2)                          # binary string → int
int('ff', 16)                           # hex string → int

# --- Random ---
import random
random.randint(a, b)                    # inclusive [a, b]
random.choice(arr)
random.shuffle(arr)                     # in-place
```

---

## 11 Recursion & Divide and Conquer

```python
# --- Merge Sort ---
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left  = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(l, r):
    res = []
    i = j = 0
    while i < len(l) and j < len(r):
        if l[i] <= r[j]: res.append(l[i]); i += 1
        else:             res.append(r[j]); j += 1
    res.extend(l[i:]); res.extend(r[j:])
    return res

# --- Count Inversions (merge sort variant) ---
def count_inversions(arr):
    if len(arr) <= 1:
        return arr, 0
    mid = len(arr) // 2
    left,  lc = count_inversions(arr[:mid])
    right, rc = count_inversions(arr[mid:])
    merged = []
    count = lc + rc
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
            count += len(left) - i    # all remaining left elements > right[j]
    merged.extend(left[i:]); merged.extend(right[j:])
    return merged, count

# --- Quick Select (kth smallest, avg O(n)) ---
import random
def quick_select(arr, k):
    pivot = random.choice(arr)
    lo = [x for x in arr if x < pivot]
    eq = [x for x in arr if x == pivot]
    hi = [x for x in arr if x > pivot]
    if k <= len(lo):
        return quick_select(lo, k)
    elif k <= len(lo) + len(eq):
        return pivot
    else:
        return quick_select(hi, k - len(lo) - len(eq))

# --- Binary Search on Result (D&C flavor) ---
# e.g. find peak element
def find_peak(nums):
    l, r = 0, len(nums) - 1
    while l < r:
        m = (l + r) // 2
        if nums[m] > nums[m + 1]:
            r = m
        else:
            l = m + 1
    return l

# --- Recursion Limit ---
import sys
sys.setrecursionlimit(10**6)    # increase if getting RecursionError
```

---

## 12 Pattern Recognition Guide

> Use this to decide which pattern to reach for given a problem's characteristics.

| Signal in the problem | Pattern to try |
|-----------------------|----------------|
| Sorted array, find target / boundary | Binary Search |
| Subarray sum / length with constraint | Sliding Window |
| Pair / triplet in sorted array | Two Pointers |
| All subsets / permutations / combinations | Backtracking |
| Shortest path, unweighted graph | BFS |
| Explore all paths, connected components | DFS |
| Shortest path, weighted graph (no neg) | Dijkstra |
| Shortest path, negative weights | Bellman-Ford |
| All-pairs shortest path | Floyd-Warshall |
| Cycle detection in linked list / graph | Fast & Slow Pointers |
| Merge connected components | Union-Find |
| Course prereqs / dependency ordering | Topological Sort |
| Prefix / word matching | Trie |
| Overlapping subproblems, optimal substructure | Dynamic Programming |
| Greedy local choice leads to global optimum | Greedy + Sort |
| Range sum / point update queries | BIT / Segment Tree |
| Range update + range query | Lazy Segment Tree |
| Next greater / smaller element | Monotonic Stack |
| Sliding window max / min | Monotonic Queue |
| Intervals: merge / overlap / scheduling | Sort by start or end |
| Find duplicate / missing number | XOR or index marking |
| Top-k elements | Heap |
| Palindrome centered expansion | Two Pointers from center |
| Count ways / min cost over subsets | Bitmask DP |
| Problem on contiguous subarray intervals | Interval DP |

---

### Complexity Cheat Sheet

| Structure / Op | Time |
|----------------|------|
| Hash map get/set | O(1) avg |
| Heap push/pop | O(log n) |
| Binary search | O(log n) |
| Sorting | O(n log n) |
| BFS / DFS | O(V + E) |
| Dijkstra (heap) | O((V+E) log V) |
| Union-Find | O(α(n)) ≈ O(1) |
| Segment Tree query/update | O(log n) |
| BIT query/update | O(log n) |
| LIS (patience sort) | O(n log n) |
| Backtracking subsets | O(2^n) |
| Backtracking permutations | O(n!) |

---

*Part of a two-file Python LeetCode reference. See Vol. 1 for lists, strings, dicts, two pointers, sliding window, binary search, stack, heap, linked list, trees, graphs (basics), DP (basics), sorting, and bit tricks.*