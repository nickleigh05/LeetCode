# Backtracking

## How to use this README

Problems are split into three tiers: Blind 75 is the core set every interviewer expects you to know cold. NeetCode 150 extends the pattern library to cover permutations, deduplication, and constraint-based generation. NeetCode 250 adds harder variants — duplicate permutations, partition problems, and backtracking with memoization. Work through tiers in order — the Core Patterns and Syntax Reference sections below map directly to the problems in each table, so when you hit a new problem, identify which pattern family it belongs to (subsets, combinations, permutations, or constrained generation) before writing any code.

---

## Problems

### Blind 75
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved |
|-----------|------------|--------------|---------------|--------|
| 39 | Medium | Combination Sum | [Link](https://leetcode.com/problems/combination-sum/) | ☐ |
| 79 | Medium | Word Search | [Link](https://leetcode.com/problems/word-search/) | ☐ |

### NeetCode 150
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved |
|-----------|------------|--------------|---------------|--------|
| 78 | Medium | Subsets | [Link](https://leetcode.com/problems/subsets/) | ☐ |
| 46 | Medium | Permutations | [Link](https://leetcode.com/problems/permutations/) | ☐ |
| 90 | Medium | Subsets II | [Link](https://leetcode.com/problems/subsets-ii/) | ☐ |
| 40 | Medium | Combination Sum II | [Link](https://leetcode.com/problems/combination-sum-ii/) | ☐ |
| 131 | Medium | Palindrome Partitioning | [Link](https://leetcode.com/problems/palindrome-partitioning/) | ☐ |
| 17 | Medium | Letter Combinations of a Phone Number | [Link](https://leetcode.com/problems/letter-combinations-of-a-phone-number/) | ☐ |
| 51 | Hard | N-Queens | [Link](https://leetcode.com/problems/n-queens/) | ☐ |

### NeetCode 250
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved | Pattern |
|-----------|------------|--------------|---------------|--------|---------|
| 1863 | Easy | Sum of All Subset XOR Totals | [Link](https://leetcode.com/problems/sum-of-all-subset-xor-totals/) | ☐ | Enumerate all subsets |
| 77 | Medium | Combinations | [Link](https://leetcode.com/problems/combinations/) | ☐ | Choose k from n |
| 47 | Medium | Permutations II | [Link](https://leetcode.com/problems/permutations-ii/) | ☐ | Permutations with duplicates |
| 22 | Medium | Generate Parentheses | [Link](https://leetcode.com/problems/generate-parentheses/) | ☐ | Constrained generation |
| 473 | Medium | Matchsticks to Square | [Link](https://leetcode.com/problems/matchsticks-to-square/) | ☐ | Partition backtracking |
| 698 | Medium | Partition to K Equal Sum Subsets | [Link](https://leetcode.com/problems/partition-to-k-equal-sum-subsets/) | ☐ | Partition backtracking |
| 52 | Hard | N-Queens II | [Link](https://leetcode.com/problems/n-queens-ii/) | ☐ | Count solutions |
| 140 | Hard | Word Break II | [Link](https://leetcode.com/problems/word-break-ii/) | ☐ | Backtracking + memo |

---

## Complexity Reference

| Pattern | Time | Space | Notes |
|---------|------|-------|-------|
| Subsets (power set) | O(2^n) | O(n) | 2^n subsets, each up to length n |
| Combinations (choose k from n) | O(C(n,k) * k) | O(k) | C(n,k) results, each of length k |
| Permutations | O(n! * n) | O(n) | n! results, each of length n |
| Combination Sum (unlimited reuse) | O(n^(t/m)) | O(t/m) | t=target, m=min element |
| Word Search (grid) | O(m*n * 4^L) | O(L) | L=word length, 4 directions |
| N-Queens | O(n!) | O(n) | Pruning cuts this in practice |
| Generate Parentheses | O(C(2n,n)/n+1) | O(n) | Catalan number of valid sequences |

---

## Data Structures

### Recursion Stack

The call stack itself is the backtracking mechanism. Every recursive call pushes a frame containing the current state (the path built so far, the current index, any counters). When the call returns, Python automatically unwinds to the previous frame — that's the "undo" step. You don't need an explicit undo data structure; the stack handles it for you.

```
bt(start=0, path=[])
  └─ append 1 → bt(start=1, path=[1])
       └─ append 2 → bt(start=2, path=[1,2])   ← base case hit, record [1,2]
       └─ return: path=[1] again (undo happened automatically)
       └─ append 3 → bt(start=3, path=[1,3])   ← base case hit, record [1,3]
  └─ return: path=[] again
  └─ append 2 → bt(start=2, path=[2]) ...
```

**When it matters:** Any time you're building candidates incrementally and need to explore all branches — the stack depth equals the maximum path length, which is O(n) in most problems.

### Path List (Mutable State with Undo)

The path list accumulates the current candidate as you recurse. The critical discipline: `append` before the recursive call, `pop` after it returns. This restores the path to its pre-call state so the next branch starts clean.

```
path = []
path.append(x)   # going deeper — x is now part of the candidate
bt(...)          # explore everything reachable from here
path.pop()       # coming back — remove x, try the next option
```

**When it matters:** Every backtracking problem. The common bug is appending to `res` a reference to `path` rather than a copy — `res.append(path)` appends the same list object, which will be mutated later. Always use `res.append(path[:])`.

---

## Core Patterns

### Subsets (Power Set)

**When to use:** Generate all possible subsets of a collection. No size constraint on output.
**Complexity:** O(2^n) time, O(n) recursion depth
**Problems:** Subsets (#78), Sum of All Subset XOR Totals (#1863)
**Common mistake:** Appending the path reference instead of a copy. Also: for the "include/exclude" style, you don't need a start index — the index advances naturally.

```python
def subsets(nums):
    res = []
    def bt(i, path):
        if i == len(nums):
            res.append(path[:])
            return
        path.append(nums[i])
        bt(i + 1, path)        # include nums[i]
        path.pop()
        bt(i + 1, path)        # exclude nums[i]
    bt(0, [])
    return res
```

### Combinations (Choose K)

**When to use:** Generate all size-k subsets. Elements are not reused; order doesn't matter.
**Complexity:** O(C(n,k) * k) time
**Problems:** Combinations (#77), Combination Sum (#39), Combination Sum II (#40)
**Common mistake:** Not passing a `start` index — without it, earlier elements get revisited and you produce duplicates. For unlimited reuse (Combination Sum), pass `i` instead of `i+1` to allow reusing the current element.

```python
def combine(n, k):
    res = []
    def bt(start, path):
        if len(path) == k:
            res.append(path[:])
            return
        for i in range(start, n + 1):
            path.append(i)
            bt(i + 1, path)    # i+1 prevents reuse; use i for unlimited reuse
            path.pop()
    bt(1, [])
    return res
```

### Permutations

**When to use:** Generate all orderings of a collection. Every element must appear exactly once.
**Complexity:** O(n! * n) time
**Problems:** Permutations (#46), Permutations II (#47)
**Common mistake:** Using a `start` index like combinations — that only generates elements in forward order and misses permutations. You need a `used` boolean array so any unused element can be the next pick.

```python
def permutations(nums):
    res = []
    used = [False] * len(nums)
    def bt(path):
        if len(path) == len(nums):
            res.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            used[i] = True
            path.append(nums[i])
            bt(path)
            path.pop()
            used[i] = False
    bt([])
    return res
```

### Deduplication (Subsets II / Permutations II)

**When to use:** Input has duplicates and you need unique results only.
**Complexity:** Same as base pattern — O(2^n) or O(n!)
**Problems:** Subsets II (#90), Combination Sum II (#40), Permutations II (#47)
**Common mistake:** Forgetting to sort first. The skip condition `nums[i] == nums[i-1]` only works when duplicates are adjacent. Also: the check is `i > start` for combinations (not `i > 0`) — you only skip duplicates at the same recursion level.

```python
def subsets_with_dup(nums):
    nums.sort()                  # MUST sort so duplicates are adjacent
    res = []
    def bt(start, path):
        res.append(path[:])
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:
                continue         # skip duplicate at same recursion level
            path.append(nums[i])
            bt(i + 1, path)
            path.pop()
    bt(0, [])
    return res
```

### Constraint-Based Generation (N-Queens / Generate Parentheses)

**When to use:** You're building a sequence where each step must satisfy a structural rule — not just picking from a list.
**Complexity:** Depends on constraint tightness; often much less than the naive bound
**Problems:** N-Queens (#51), N-Queens II (#52), Generate Parentheses (#22)
**Common mistake:** Checking validity after building the full candidate instead of pruning early. The power of constraint-based backtracking is that invalid branches are cut before they grow.

```python
def generate_parentheses(n):
    res = []
    def bt(open_count, close_count, path):
        if len(path) == 2 * n:
            res.append("".join(path))
            return
        if open_count < n:
            path.append("(")
            bt(open_count + 1, close_count, path)
            path.pop()
        if close_count < open_count:   # can only close if there's an unmatched open
            path.append(")")
            bt(open_count, close_count + 1, path)
            path.pop()
    bt(0, 0, [])
    return res
```

---

## Syntax Reference

### Backtrack template

The minimal skeleton every backtracking solution follows. Fill in the base case, the loop range, and the pruning condition.

```python
def backtrack(start, path):
    if <base case>:
        res.append(path[:])   # always copy, never append path directly
        return
    for i in range(start, n):
        if <prune condition>:
            continue
        path.append(nums[i])
        backtrack(i + 1, path)   # or i for unlimited reuse
        path.pop()               # undo — this is the "backtrack" step
```

### Copy before appending to results

```python
res.append(path[:])        # correct — creates a shallow copy of the list
res.append(list(path))     # also correct
res.append(path.copy())    # also correct
res.append(path)           # WRONG — appends the same list object; future mutations corrupt it
```

### Sort + skip duplicates

```python
nums.sort()                              # must sort first so duplicates are adjacent
for i in range(start, len(nums)):
    if i > start and nums[i] == nums[i - 1]:
        continue                         # skip duplicate at this level of the tree
```

### Used array for permutations

```python
used = [False] * len(nums)

# inside the loop:
if used[i]: continue
used[i] = True
path.append(nums[i])
bt(path)
path.pop()
used[i] = False
```

### Visited set for grid problems (Word Search)

```python
visited = set()

def dfs(r, c, idx):
    if idx == len(word): return True
    if r < 0 or r >= rows or c < 0 or c >= cols: return False
    if (r, c) in visited or board[r][c] != word[idx]: return False
    visited.add((r, c))
    found = any(dfs(r+dr, c+dc, idx+1) for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)])
    visited.remove((r, c))   # backtrack — remove from visited on the way out
    return found
```
