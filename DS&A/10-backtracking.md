# Backtracking

## What is Backtracking?
Backtracking is an algorithmic technique for solving problems recursively by trying to build a solution incrementally, one piece at a time, and removing solutions that fail to satisfy the constraints (backtracking) to try another path.

## Core Concept

### The Backtracking Template
```
Backtracking follows this pattern:

1. Make a choice
2. Explore consequences (recurse)
3. Undo the choice (backtrack)
4. Try next choice

Visual representation:
                Start
                  |
        ┌─────────┼─────────┐
     Choice1   Choice2   Choice3
        |         |         |
      ┌─┴─┐     ┌─┴─┐     ┌─┴─┐
     C1  C2    C1  C2    C1  C2

If C1 fails → backtrack → try C2
If Choice1 fails → backtrack → try Choice2
```

### Decision Tree
```
All possible paths explored:

                    []
                    |
        ┌───────────┼───────────┐
       [1]         [2]         [3]
        |           |           |
    ┌───┼───┐   ┌───┼───┐   ┌───┼───┐
  [1,2][1,3] [2,1][2,3] [3,1][3,2]
    |    |     |    |     |    |
  Valid Valid Valid Valid Valid Valid

Backtracking explores all paths efficiently
Prunes invalid paths early
```

## Classic Template Pattern

```
def backtrack(state, choices):
    # Base case: solution found
    if is_valid_solution(state):
        output.append(state.copy())
        return

    # Iterate through choices
    for choice in choices:
        # 1. Make choice
        state.add(choice)

        # 2. Recurse with updated state
        backtrack(state, get_next_choices(choice))

        # 3. Undo choice (backtrack)
        state.remove(choice)

Visual execution:
State: []
├─ Add 1 → [1]
│  ├─ Add 2 → [1,2] ✓ (solution)
│  │  └─ Backtrack → [1]
│  └─ Add 3 → [1,3] ✓ (solution)
│     └─ Backtrack → [1]
│  └─ Backtrack → []
└─ Add 2 → [2]
   └─ Continue...
```

## Common Backtracking Problems

### 1. Subsets (Powerset)

```
Find all subsets of [1, 2, 3]:

Decision tree:
                        []
                    /        \
                include 1    exclude 1
                  /              \
                [1]              []
              /     \          /     \
          incl 2  excl 2   incl 2  excl 2
           /  \      |       |       |
        [1,2] [1]   [1]     [2]     []
         / \   / \   / \    / \     / \
      [1,2,3][1,2][1,3][1][2,3][2][3][]

All subsets (2^n = 8):
[], [1], [2], [3], [1,2], [1,3], [2,3], [1,2,3]

Execution trace:
Start: []
├─ Include 1: [1]
│  ├─ Include 2: [1,2]
│  │  ├─ Include 3: [1,2,3] ✓
│  │  └─ Exclude 3: [1,2] ✓
│  └─ Exclude 2: [1]
│     ├─ Include 3: [1,3] ✓
│     └─ Exclude 3: [1] ✓
└─ Exclude 1: []
   ├─ Include 2: [2]
   │  ├─ Include 3: [2,3] ✓
   │  └─ Exclude 3: [2] ✓
   └─ Exclude 2: []
      ├─ Include 3: [3] ✓
      └─ Exclude 3: [] ✓

Time: O(2^n)
Space: O(n) recursion depth
```

### 2. Permutations

```
Find all permutations of [1, 2, 3]:

Decision tree:
                    []
            /       |       \
          [1]      [2]      [3]
         /  \     /  \     /  \
      [1,2][1,3][2,1][2,3][3,1][3,2]
       |    |    |    |    |    |
    [1,2,3][1,3,2][2,1,3][2,3,1][3,1,2][3,2,1]

All permutations (n! = 6):
[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]

Step-by-step execution for [1,2,3]:

State: []
├─ Choose 1 → [1]
│  ├─ Choose 2 → [1,2]
│  │  ├─ Choose 3 → [1,2,3] ✓ SOLUTION
│  │  └─ Backtrack → [1,2]
│  └─ Backtrack → [1]
│  ├─ Choose 3 → [1,3]
│  │  ├─ Choose 2 → [1,3,2] ✓ SOLUTION
│  │  └─ Backtrack → [1,3]
│  └─ Backtrack → [1]
└─ Backtrack → []
├─ Choose 2 → [2]
│  ├─ Choose 1 → [2,1]
│  │  └─ Choose 3 → [2,1,3] ✓ SOLUTION
│  └─ ...

Key difference from subsets:
- Each element used exactly once
- Order matters
- Track used elements

Time: O(n! * n)
Space: O(n)
```

### 3. Combinations

```
Find all combinations of size k=2 from [1,2,3,4]:

Decision tree (with pruning):
                    []
        /     |      |      \
      [1]   [2]    [3]    [4]
     / | \   |  \    |
  [1,2][1,3][1,4][2,3][2,4][3,4]
   ✓    ✓    ✓    ✓    ✓    ✓

Valid combinations:
[1,2], [1,3], [1,4], [2,3], [2,4], [3,4]

Execution trace:
Start: [], start_index = 0
├─ Add 1 → [1], start = 1
│  ├─ Add 2 → [1,2] ✓ (k=2)
│  │  └─ Backtrack → [1]
│  ├─ Add 3 → [1,3] ✓ (k=2)
│  │  └─ Backtrack → [1]
│  └─ Add 4 → [1,4] ✓ (k=2)
│     └─ Backtrack → [1]
│  └─ Backtrack → []
├─ Add 2 → [2], start = 2
│  ├─ Add 3 → [2,3] ✓ (k=2)
│  │  └─ Backtrack → [2]
│  └─ Add 4 → [2,4] ✓ (k=2)
│     └─ Backtrack → [2]
│  └─ Backtrack → []
└─ Add 3 → [3], start = 3
   └─ Add 4 → [3,4] ✓ (k=2)
      └─ Backtrack → [3]
   └─ Backtrack → []

Key: start_index prevents duplicates
[1,2] generated, but not [2,1]

Time: O(C(n,k)) = O(n!/(k!(n-k)!))
Space: O(k)
```

### 4. N-Queens

```
Place N queens on N×N board (no attacks):

N = 4:
Board positions:
  0 1 2 3
0 . . . .
1 . . . .
2 . . . .
3 . . . .

Solution 1:
  0 1 2 3
0 . Q . .  ← Queen at (0,1)
1 . . . Q  ← Queen at (1,3)
2 Q . . .  ← Queen at (2,0)
3 . . Q .  ← Queen at (3,2)

Decision tree (simplified):
                    Row 0
        /      |       |      \
      Col0   Col1    Col2   Col3
       |       |       |       |
     Invalid  Valid  Invalid Invalid
              |
            Row 1
      /    |    |    \
    Col0 Col1 Col2 Col3
     |    X    X    |
   Invalid     Valid
                 |
               Row 2
         /    |    |    \
       Col0 Col1 Col2 Col3
        |    X    X    X
      Valid
        |
      Row 3
    /  |   |   \
  Col0 Col1 Col2 Col3
   X    X   Valid  X
            |
         SOLUTION!

Attack validation:
Queen at (r1, c1) attacks (r2, c2) if:
- Same row: r1 == r2
- Same col: c1 == c2
- Same diagonal: |r1-r2| == |c1-c2|

Visual attack pattern:
     Q . . .
     . . . .
     . . . .
     . . . .

Q attacks:
- Entire row 0
- Entire col 0
- Diagonals:
     Q . . .
     * * . .
     . * * .
     . . * *

Backtracking:
1. Try queen in row 0
2. Try all safe positions
3. If stuck, backtrack
4. Try next position

Time: O(N!)
Space: O(N)
```

### 5. Sudoku Solver

```
Fill 9×9 grid with constraints:
- Each row: 1-9 once
- Each col: 1-9 once
- Each 3×3 box: 1-9 once

Example (simplified 4×4):
Input:
  1 . . 4
  . 3 . .
  . . 4 .
  4 . . 2

Decision tree:
        Try (0,1)
    /   |   |   \
   1    2   3   4
   X    ✓   X   X
        |
      Try (0,2)
    /   |   |   \
   1    2   3   4
   ✓    X   X   X
        |
      Try (1,0)
        ...

Backtracking:
Position (0,1):
├─ Try 1: Invalid (row has 1) ✗
├─ Try 2: Valid ✓
│  └─ Continue to (0,2)
│     ├─ Try 1: Valid ✓
│     │  └─ Continue...
│     │     └─ Dead end at (3,2)
│     │        └─ Backtrack to (0,2)
│     ├─ Try 2: Invalid ✗
│     ├─ Try 3: Valid ✓
│     │  └─ Continue and find solution!

Solution:
  1 2 3 4
  2 3 1 4
  3 1 4 2
  4 4 2 1

Time: O(9^(n*n)) worst case
Space: O(n*n)
```

### 6. Word Search

```
Board:
  A B C E
  S F C S
  A D E E

Find "ABCCED":

Search tree from 'A' at (0,0):
         A(0,0)
        /  |  \  \
       B  S  ...
      (0,1)
       |
       C(0,2)
      / \
     C  F
   (0,3) X
     |
     E(1,3)
     |
     D(2,3)
     X (not 'E')

Backtrack to C(0,2):
       C(0,2)
      / \
     C  S  E
   done X  (1,2)
           |
           D(2,2)
           ✓ FOUND!

Visual execution:
Step 1: Start at A(0,0)
  A B C E     Visited: {(0,0)}
  S F C S     Path: "A"
  A D E E

Step 2: Move to B(0,1)
  A B C E     Visited: {(0,0), (0,1)}
  S F C S     Path: "AB"
  A D E E

Step 3: Move to C(0,2)
  A B C E     Visited: {(0,0), (0,1), (0,2)}
  S F C S     Path: "ABC"
  A D E E

Step 4: Move to C(1,2)
  A B C E     Visited: {(0,0), (0,1), (0,2), (1,2)}
  S F C S     Path: "ABCC"
  A D E E

Step 5: Move to E(1,3)
  A B C E     Visited: {(0,0), (0,1), (0,2), (1,2), (1,3)}
  S F C S     Path: "ABCCE"
  A D E E

Step 6: Move to D(2,3)
  A B C E     Visited: {(0,0), (0,1), (0,2), (1,2), (1,3), (2,3)}
  S F C S     Path: "ABCCED" ✓ FOUND!
  A D E E

Key points:
- Mark visited cells
- Explore 4 directions
- Backtrack: unmark cell
- Prune: stop if char doesn't match

Time: O(m*n*4^L) where L = word length
Space: O(L) for recursion
```

## Optimization Techniques

### 1. Pruning

```
Early termination when path is invalid:

Bad (no pruning):
    Explore all 2^n paths
    Check validity at end
    Many wasted explorations

Good (with pruning):
                []
            /   |   \
          [1]  [2]  [3]
         /  X   |
      [1,1]  (invalid, sum > target)

Stop exploring when:
- Constraint violated
- No valid solution possible
- Better solution found

Example: Combination sum
Target = 7, nums = [2,3,6,7]

Without pruning:
    Try [2,2,2,2] → sum=8 > 7 ✗

With pruning:
    [2,2,2] → sum=6
    └─ Try 2 → sum=8 > 7, STOP! Don't explore deeper

Savings: Entire subtrees eliminated
```

### 2. Memoization

```
Cache results to avoid recomputation:

Problem: Word Break
s = "catsanddog"
dict = ["cat", "cats", "and", "sand", "dog"]

Without memo:
    "catsanddog"
   /           \
"atsanddog"  "sanddog"  (both from "cat"/"cats")
              /      \
         "anddog"  "dog"
         /      \
      "dog"   "og"

"dog" checked multiple times!

With memo:
memo = {
    "dog": True,
    "anddog": True,
    "sanddog": True,
    ...
}

When we see "dog" again, return cached result

Time: O(n^2) with memo vs O(2^n) without
```

### 3. Constraint Propagation

```
Use constraints to limit choices:

N-Queens: Track attacked positions

Bad approach:
    Try every position
    Check all attack patterns

Good approach:
    cols = set()      # attacked columns
    diag1 = set()     # attacked diagonal /
    diag2 = set()     # attacked diagonal \

    When placing queen at (r, c):
    - Add c to cols
    - Add r-c to diag1
    - Add r+c to diag2

    Only try positions not in these sets!

Visual:
Place Q at (0, 1):
    . Q . .

cols = {1}
diag1 = {-1}  (0-1)
diag2 = {1}   (0+1)

Row 1 invalid positions:
    X X . X

Only position (1,2) valid!
Much faster than checking all 4 positions

Reduction: 4 choices → 1 choice
```

## Backtracking Patterns

### Pattern 1: Build Solution Incrementally
```
Examples: Permutations, Combinations

Template:
def backtrack(current, remaining):
    if len(current) == target_size:
        result.append(current[:])
        return

    for choice in remaining:
        current.append(choice)
        backtrack(current, new_remaining)
        current.pop()
```

### Pattern 2: Decision at Each Step
```
Examples: Subsets, Partition

Template:
def backtrack(index, current):
    if index == n:
        result.append(current[:])
        return

    # Include current element
    current.append(nums[index])
    backtrack(index + 1, current)
    current.pop()

    # Exclude current element
    backtrack(index + 1, current)
```

### Pattern 3: Fill Grid/Board
```
Examples: Sudoku, N-Queens

Template:
def backtrack(row, col):
    if row == n:
        result.append(copy_board())
        return

    next_row, next_col = get_next_position(row, col)

    for choice in valid_choices(row, col):
        board[row][col] = choice
        if is_valid(row, col):
            backtrack(next_row, next_col)
        board[row][col] = empty
```

### Pattern 4: Path Finding
```
Examples: Word Search, Maze

Template:
def backtrack(row, col, path):
    if is_target(row, col):
        result.append(path[:])
        return

    visited.add((row, col))

    for dr, dc in directions:
        new_r, new_c = row + dr, col + dc
        if is_valid(new_r, new_c):
            path.append((new_r, new_c))
            backtrack(new_r, new_c, path)
            path.pop()

    visited.remove((row, col))
```

## Time and Space Complexity

```
General complexities:

Problem Type         Time            Space
Subsets              O(2^n)          O(n)
Permutations         O(n!)           O(n)
Combinations         O(C(n,k))       O(k)
N-Queens             O(n!)           O(n^2)
Sudoku               O(9^(n*n))      O(n*n)
Word Search          O(m*n*4^L)      O(L)

Where:
n = input size
k = subset size
m, n = grid dimensions
L = word length

Space is typically recursion depth
Time depends on:
- Number of choices at each step
- Depth of recursion tree
- Pruning effectiveness
```

## Python Implementation

```python
# Template for backtracking problems
def backtrack_template(nums):
    result = []

    def backtrack(current, remaining):
        # Base case
        if is_solution(current):
            result.append(current[:])  # Important: copy!
            return

        # Recursive case
        for i, choice in enumerate(remaining):
            # Make choice
            current.append(choice)

            # Recurse
            backtrack(current, remaining[i+1:])

            # Undo choice (backtrack)
            current.pop()

    backtrack([], nums)
    return result


# 1. Subsets
def subsets(nums):
    """
    All subsets of nums.
    Time: O(2^n), Space: O(n)
    """
    result = []

    def backtrack(index, current):
        if index == len(nums):
            result.append(current[:])
            return

        # Include nums[index]
        current.append(nums[index])
        backtrack(index + 1, current)
        current.pop()

        # Exclude nums[index]
        backtrack(index + 1, current)

    backtrack(0, [])
    return result


# 2. Permutations
def permutations(nums):
    """
    All permutations of nums.
    Time: O(n!), Space: O(n)
    """
    result = []

    def backtrack(current, remaining):
        if not remaining:
            result.append(current[:])
            return

        for i in range(len(remaining)):
            current.append(remaining[i])
            backtrack(current, remaining[:i] + remaining[i+1:])
            current.pop()

    backtrack([], nums)
    return result


# Alternative permutations with swap
def permutations_swap(nums):
    result = []

    def backtrack(start):
        if start == len(nums):
            result.append(nums[:])
            return

        for i in range(start, len(nums)):
            # Swap
            nums[start], nums[i] = nums[i], nums[start]
            backtrack(start + 1)
            # Swap back
            nums[start], nums[i] = nums[i], nums[start]

    backtrack(0)
    return result


# 3. Combinations
def combinations(n, k):
    """
    All combinations of k numbers from 1..n.
    Time: O(C(n,k)), Space: O(k)
    """
    result = []

    def backtrack(start, current):
        if len(current) == k:
            result.append(current[:])
            return

        # Pruning: need k - len(current) more elements
        # Available: n - start + 1
        # If not enough: stop
        for i in range(start, n + 1):
            if n - i + 1 < k - len(current):
                break

            current.append(i)
            backtrack(i + 1, current)
            current.pop()

    backtrack(1, [])
    return result


# 4. Combination Sum
def combination_sum(candidates, target):
    """
    All combinations that sum to target.
    Can reuse elements.
    Time: O(2^target), Space: O(target)
    """
    result = []

    def backtrack(start, current, total):
        if total == target:
            result.append(current[:])
            return

        if total > target:
            return  # Pruning

        for i in range(start, len(candidates)):
            current.append(candidates[i])
            # Can reuse same element: start = i
            backtrack(i, current, total + candidates[i])
            current.pop()

    backtrack(0, [], 0)
    return result


# 5. N-Queens
def solve_n_queens(n):
    """
    Place n queens on n×n board.
    Time: O(n!), Space: O(n)
    """
    result = []
    board = [['.'] * n for _ in range(n)]

    cols = set()
    diag1 = set()  # r - c
    diag2 = set()  # r + c

    def backtrack(row):
        if row == n:
            result.append([''.join(row) for row in board])
            return

        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue

            # Place queen
            board[row][col] = 'Q'
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)

            backtrack(row + 1)

            # Remove queen
            board[row][col] = '.'
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)

    backtrack(0)
    return result


# 6. Sudoku Solver
def solve_sudoku(board):
    """
    Solve 9×9 sudoku.
    Time: O(9^(n*n)), Space: O(n*n)
    """
    def is_valid(row, col, num):
        # Check row
        if num in board[row]:
            return False

        # Check column
        if num in [board[i][col] for i in range(9)]:
            return False

        # Check 3×3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if board[i][j] == num:
                    return False

        return True

    def backtrack():
        for row in range(9):
            for col in range(9):
                if board[row][col] == '.':
                    for num in '123456789':
                        if is_valid(row, col, num):
                            board[row][col] = num

                            if backtrack():
                                return True

                            board[row][col] = '.'

                    return False  # No valid number

        return True  # All cells filled

    backtrack()


# 7. Word Search
def word_search(board, word):
    """
    Find word in board.
    Time: O(m*n*4^L), Space: O(L)
    """
    rows, cols = len(board), len(board[0])

    def backtrack(row, col, index):
        if index == len(word):
            return True

        if (row < 0 or row >= rows or col < 0 or col >= cols or
            board[row][col] != word[index]):
            return False

        # Mark visited
        temp = board[row][col]
        board[row][col] = '#'

        # Explore neighbors
        found = (backtrack(row + 1, col, index + 1) or
                 backtrack(row - 1, col, index + 1) or
                 backtrack(row, col + 1, index + 1) or
                 backtrack(row, col - 1, index + 1))

        # Restore
        board[row][col] = temp

        return found

    for r in range(rows):
        for c in range(cols):
            if backtrack(r, c, 0):
                return True

    return False


# 8. Palindrome Partitioning
def partition(s):
    """
    All palindrome partitions.
    Time: O(n * 2^n), Space: O(n)
    """
    result = []

    def is_palindrome(sub):
        return sub == sub[::-1]

    def backtrack(start, current):
        if start == len(s):
            result.append(current[:])
            return

        for end in range(start + 1, len(s) + 1):
            substring = s[start:end]
            if is_palindrome(substring):
                current.append(substring)
                backtrack(end, current)
                current.pop()

    backtrack(0, [])
    return result


# 9. Generate Parentheses
def generate_parentheses(n):
    """
    All valid n pairs of parentheses.
    Time: O(4^n / sqrt(n)), Space: O(n)
    """
    result = []

    def backtrack(current, open_count, close_count):
        if len(current) == 2 * n:
            result.append(current)
            return

        if open_count < n:
            backtrack(current + '(', open_count + 1, close_count)

        if close_count < open_count:
            backtrack(current + ')', open_count, close_count + 1)

    backtrack('', 0, 0)
    return result
```

## Key Takeaways

1. **Core Idea**: Try, recurse, backtrack
2. **Template**:
   - Make choice
   - Explore (recurse)
   - Undo choice (backtrack)

3. **When to Use**:
   - Generate all solutions
   - Constraint satisfaction
   - Combinatorial problems
   - Optimization problems

4. **Optimization**:
   - Pruning (early termination)
   - Memoization (cache results)
   - Constraint propagation

5. **Common Patterns**:
   - Subsets: include/exclude
   - Permutations: swap or remaining
   - Combinations: start index
   - Grid: DFS with visited tracking

6. **Time Complexity**:
   - Often exponential
   - Depends on branching factor
   - Pruning can significantly improve

7. **Space Complexity**:
   - Recursion stack depth
   - Usually O(n) or O(h) for height

8. **Implementation Tips**:
   - Always copy when adding to result
   - Mark/unmark for visited
   - Use constraints to prune
   - Base case: check solution validity
