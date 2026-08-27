# 10. Backtracking
*Choose → explore → un-choose, over the tree of partial solutions.*

[← Prev](09-heap-priority-queue.md) · [🗺 Roadmap](../../roadmap.md) · [Next →](11-graphs.md)

---

> **Builds on:** [recursion (04b)](04b-recursion.md) and DFS from [Lesson 07 — Trees](07-trees.md). Backtracking is DFS over a tree of *choices* instead of a tree of nodes.

Backtracking is exhaustive search done cleanly: at each step make a choice, recurse, then **undo the choice** before trying the next. Subsets, permutations, combinations, word search, N-Queens — they're all the same skeleton over a decision tree. Get the choose/un-choose rhythm right and pruning becomes natural.

## The Pattern

### DFS and Backtracking

```
  Number of Islands — DFS flood fill:
  grid:          After DFS from (0,0):
  1 1 0 0 0      X X 0 0 0   (X = visited land)
  1 1 0 0 0      X X 0 0 0
  0 0 1 0 0  →   0 0 1 0 0   ← separate island
  0 0 0 1 1      0 0 0 1 1   ← separate island
  Count = 3

  Subsets backtracking — [1,2,3]:
  choose/skip at each index:
  dfs(0,[]):
  ├─ skip: dfs(1,[])
  │   ├─ skip: dfs(2,[])
  │   │   ├─ skip: → []
  │   │   └─ take 3: → [3]
  │   └─ take 2: dfs(2,[2])
  │       ├─ skip: → [2]
  │       └─ take 3: → [2,3]
  └─ take 1: ... (same structure)
```

**What it is:** DFS explores all reachable nodes from a starting point. Backtracking is DFS on a decision tree — you make a choice, recurse, then undo the choice to try the next option.

**Use this when:**
- [ ] Count connected components (islands, provinces)
- [ ] Detect cycles
- [ ] Find all paths from source to destination
- [ ] Generate all permutations / combinations / subsets
- [ ] Maze solving, word search on grid
- [ ] Solve puzzles: N-Queens, Sudoku

**Python:**
```python
# DFS — Count connected components (Number of Islands)
def num_islands(grid):
    rows, cols = len(grid), len(grid[0])
    count = 0

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1':
            return
        grid[r][c] = '0'   # mark visited
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            dfs(r+dr, c+dc)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                dfs(r, c)
                count += 1
    return count

# Backtracking — Word Search on Grid
def word_search(board, word):
    rows, cols = len(board), len(board[0])

    def dfs(r, c, idx):
        if idx == len(word): return True
        if r<0 or r>=rows or c<0 or c>=cols or board[r][c] != word[idx]:
            return False
        tmp, board[r][c] = board[r][c], '#'   # mark visited
        found = any(dfs(r+dr, c+dc, idx+1) for dr,dc in [(0,1),(0,-1),(1,0),(-1,0)])
        board[r][c] = tmp                      # restore (backtrack)
        return found

    return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))

# Backtracking — All combinations
def combine(n, k):
    result = []
    def bt(start, current):
        if len(current) == k:
            result.append(current[:]); return
        for i in range(start, n+1):
            current.append(i)
            bt(i+1, current)
            current.pop()
    bt(1, [])
    return result
```

**Complexity:** DFS on graph/grid: O(V+E) or O(r·c). Backtracking: exponential (O(2^n) for subsets, O(n!) for permutations) — pruning reduces actual runtime.

**Blind 75 examples:** Number of Islands · Clone Graph · Word Search · Combination Sum · Pacific Atlantic Water Flow

## Algorithm Deep-Dive

### Backtracking

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
Stack (call stack) · Array · Hash Map and Hash Set (for visited/used tracking)

## The Template

The reusable code skeleton for this pattern lives in [`appendix/templates/backtracking/`](../appendix/templates/backtracking/). Read the README (when to reach for it, variations, common bugs), then type out [`template.py`](../appendix/templates/backtracking/template.py) from memory before you drill problems.

## Practice

Work the guided set with hints & solutions: [**Backtracking — Practice →**](../rmap-practice/10-backtracking.md). Easy → hard, top to bottom; when the pattern feels automatic, move on — don’t grind it forever. Want more volume? See the [recommended list](../../lists/recommended.md#9-backtracking-16-problems).

## Check Yourself

- [ ] I can write the choose → explore → un-choose template from memory.
- [ ] I can explain how pruning cuts the search tree and where to place the prune check.
- [ ] I can handle the duplicate-skipping and used-set variants (subsets II, permutations).
- [ ] I solved a 🔴 Hard backtracking problem (e.g. N-Queens or Sudoku Solver).

---

**Up next:** [Graphs (BFS & DFS)](11-graphs.md) — bFS for shortest unweighted paths, DFS for connectivity.

[← Prev](09-heap-priority-queue.md) · [🗺 Roadmap](../../roadmap.md) · [Next →](11-graphs.md)

