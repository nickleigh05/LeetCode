# 2-D Dynamic Programming

## What is 2-D DP?
2-D Dynamic Programming extends 1-D DP to problems requiring a 2-dimensional state space. The state is typically represented as dp[i][j], where i and j represent different dimensions of the problem (e.g., position in two sequences, grid coordinates).

## Core Concepts

### 2-D State Representation

```
1-D DP: dp[i] represents state at single index i
        Example: dp[5] = Fibonacci number at position 5

2-D DP: dp[i][j] represents state at two indices
        Example: dp[3][4] = longest common substring ending at i=3, j=4

Visual:
       j →
    ┌─────────────┐
  i │ [i][j]      │
  ↓ │             │
    │             │
    └─────────────┘

Common interpretations:
- Grid problems: dp[row][col]
- Two sequences: dp[i][j] for text1[i] and text2[j]
- Game theory: dp[left][right] for subarray bounds
```

### Building 2-D DP Table

```
Process:
1. Define state meaning
2. Find recurrence relation
3. Set base cases
4. Fill table (usually row by row or diagonal)
5. Return answer

Example: Grid paths from (0,0) to (m-1, n-1)

Grid (3×3):
    0   1   2
  ┌───┬───┬───┐
0 │ S │   │   │
  ├───┼───┼───┤
1 │   │   │   │
  ├───┼───┼───┤
2 │   │   │ E │
  └───┴───┴───┘

dp[i][j] = number of paths to reach (i, j)

Recurrence: dp[i][j] = dp[i-1][j] + dp[i][j-1]

Build table:
    0   1   2
  ┌───┬───┬───┐
0 │ 1 │ 1 │ 1 │  ← First row: only one way (right)
  ├───┼───┼───┤
1 │ 1 │ 2 │ 3 │
  ├───┼───┼───┤
2 │ 1 │ 3 │ 6 │
  └───┴───┴───┘
     ↑
     First column: only one way (down)

dp[2][2] = 6 paths
```

## Classic 2-D DP Problems

### 1. Unique Paths

```
Problem: Robot in grid, can only move right or down
Find number of unique paths from (0,0) to (m-1, n-1)

Grid (3×4):
    0   1   2   3
  ┌───┬───┬───┬───┐
0 │ S │   │   │   │
  ├───┼───┼───┼───┤
1 │   │   │   │   │
  ├───┼───┼───┼───┤
2 │   │   │   │ E │
  └───┴───┴───┴───┘

Recurrence: dp[i][j] = dp[i-1][j] + dp[i][j-1]

Base cases:
- dp[0][j] = 1 (first row)
- dp[i][0] = 1 (first column)

Build table:
    0   1   2   3
  ┌───┬───┬───┬───┐
0 │ 1 │ 1 │ 1 │ 1 │
  ├───┼───┼───┼───┤
1 │ 1 │ 2 │ 3 │ 4 │
  ├───┼───┼───┼───┤
2 │ 1 │ 3 │ 6 │10 │
  └───┴───┴───┴───┘

Step-by-step:
dp[1][1] = dp[0][1] + dp[1][0] = 1 + 1 = 2
           ↑         ↑
           from up   from left

dp[1][2] = dp[0][2] + dp[1][1] = 1 + 2 = 3
dp[2][2] = dp[1][2] + dp[2][1] = 3 + 3 = 6
dp[2][3] = dp[1][3] + dp[2][2] = 4 + 6 = 10

Answer: 10 paths

Visual paths:
R=Right, D=Down

Some paths:
1. RRRDD
2. RRDRD
3. RRDDR
4. RDRRD
...
10 total

Time: O(m × n)
Space: O(m × n) or O(n) with optimization
```

### 2. Unique Paths II (With Obstacles)

```
Grid with obstacles:
    0   1   2   3
  ┌───┬───┬───┬───┐
0 │ S │   │   │   │
  ├───┼───┼───┼───┤
1 │   │ X │   │   │  ← X = obstacle
  ├───┼───┼───┼───┤
2 │   │   │   │ E │
  └───┴───┴───┴───┘

Modification:
if grid[i][j] == obstacle:
    dp[i][j] = 0
else:
    dp[i][j] = dp[i-1][j] + dp[i][j-1]

Build table:
    0   1   2   3
  ┌───┬───┬───┬───┐
0 │ 1 │ 1 │ 1 │ 1 │
  ├───┼───┼───┼───┤
1 │ 1 │ 0 │ 1 │ 2 │  ← dp[1][1] = 0 (obstacle)
  ├───┼───┼───┼───┤
2 │ 1 │ 1 │ 2 │ 4 │
  └───┴───┴───┴───┘

Impact of obstacle:
Without obstacle: dp[1][1] = 2
With obstacle: dp[1][1] = 0

This affects all cells to the right and below:
dp[1][2] = dp[0][2] + dp[1][1] = 1 + 0 = 1
dp[2][2] = dp[1][2] + dp[2][1] = 1 + 1 = 2

Answer: 4 paths (vs 10 without obstacle)

Time: O(m × n)
Space: O(m × n)
```

### 3. Longest Common Subsequence (LCS)

```
Problem: Find length of longest common subsequence
text1 = "abcde"
text2 = "ace"

Subsequence: not necessarily contiguous

Recurrence:
if text1[i] == text2[j]:
    dp[i][j] = dp[i-1][j-1] + 1
else:
    dp[i][j] = max(dp[i-1][j], dp[i][j-1])

Build table:
       ""  a  c  e
    ┌───┬───┬───┬───┐
""  │ 0 │ 0 │ 0 │ 0 │
    ├───┼───┼───┼───┤
a   │ 0 │ 1 │ 1 │ 1 │
    ├───┼───┼───┼───┤
b   │ 0 │ 1 │ 1 │ 1 │
    ├───┼───┼───┼───┤
c   │ 0 │ 1 │ 2 │ 2 │
    ├───┼───┼───┼───┤
d   │ 0 │ 1 │ 2 │ 2 │
    ├───┼───┼───┼───┤
e   │ 0 │ 1 │ 2 │ 3 │
    └───┴───┴───┴───┘

Step-by-step:
dp[1][1]: 'a' == 'a' → dp[0][0] + 1 = 1
dp[1][2]: 'a' != 'c' → max(dp[0][2], dp[1][1]) = 1
dp[2][1]: 'b' != 'a' → max(dp[1][1], dp[2][0]) = 1
dp[3][2]: 'c' == 'c' → dp[2][1] + 1 = 2
dp[5][3]: 'e' == 'e' → dp[4][2] + 1 = 3

Answer: 3 (subsequence "ace")

Trace back solution:
Start at dp[5][3] = 3

    text1[5] == text2[3] ('e' == 'e')
    → Include 'e', go to dp[4][2]

    text1[4] != text2[2] ('d' != 'e')
    → max(dp[3][2], dp[4][1]) = dp[3][2]
    → Go to dp[3][2]

    text1[3] == text2[2] ('c' == 'c')
    → Include 'c', go to dp[2][1]

    text1[2] != text2[1] ('b' != 'a')
    → max(dp[1][1], dp[2][0]) = dp[1][1]
    → Go to dp[1][1]

    text1[1] == text2[1] ('a' == 'a')
    → Include 'a', go to dp[0][0]

LCS: "ace" ✓

Time: O(m × n)
Space: O(m × n)
```

### 4. Edit Distance

```
Problem: Minimum operations to convert word1 to word2
Operations: insert, delete, replace

word1 = "horse"
word2 = "ros"

Recurrence:
if word1[i] == word2[j]:
    dp[i][j] = dp[i-1][j-1]  (no operation)
else:
    dp[i][j] = 1 + min(
        dp[i-1][j],    # delete
        dp[i][j-1],    # insert
        dp[i-1][j-1]   # replace
    )

Build table:
        ""  r  o  s
    ┌───┬───┬───┬───┐
""  │ 0 │ 1 │ 2 │ 3 │  ← Insert r, o, s
    ├───┼───┼───┼───┤
h   │ 1 │ 1 │ 2 │ 3 │
    ├───┼───┼───┼───┤
o   │ 2 │ 2 │ 1 │ 2 │
    ├───┼───┼───┼───┤
r   │ 3 │ 2 │ 2 │ 2 │
    ├───┼───┼───┼───┤
s   │ 4 │ 3 │ 3 │ 2 │
    ├───┼───┼───┼───┤
e   │ 5 │ 4 │ 4 │ 3 │
    └───┴───┴───┴───┘
    ↑
    Delete h, o, r, s, e

Step-by-step key cells:
dp[2][2]: 'o' == 'o'
    → dp[1][1] = 1 (no operation)

dp[3][1]: 'r' == 'r'
    → dp[2][0] = 2

dp[5][3]: 'e' != 's'
    → 1 + min(dp[4][3], dp[5][2], dp[4][2])
    → 1 + min(2, 4, 3) = 3

Answer: 3 operations

One solution:
1. Replace 'h' with 'r': horse → rorse
2. Delete 'r': rorse → rose
3. Delete 'e': rose → ros

Visual transformation:
horse
  ↓ replace h→r
rorse
  ↓ delete r
rose
  ↓ delete e
ros ✓

Time: O(m × n)
Space: O(m × n)
```

### 5. Minimum Path Sum

```
Problem: Find path with minimum sum from top-left to bottom-right
Can only move right or down

Grid:
    0   1   2
  ┌───┬───┬───┐
0 │ 1 │ 3 │ 1 │
  ├───┼───┼───┤
1 │ 1 │ 5 │ 1 │
  ├───┼───┼───┤
2 │ 4 │ 2 │ 1 │
  └───┴───┴───┘

Recurrence: dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])

Build DP table:
    0   1   2
  ┌───┬───┬───┐
0 │ 1 │ 4 │ 5 │  ← Cumulative sum going right
  ├───┼───┼───┤
1 │ 2 │ 7 │ 6 │
  ├───┼───┼───┤
2 │ 6 │ 8 │ 7 │
  └───┴───┴───┘
  ↑
  Cumulative sum going down

Step-by-step:
dp[0][0] = 1 (start)
dp[0][1] = 1 + 3 = 4 (can only come from left)
dp[1][0] = 1 + 1 = 2 (can only come from top)

dp[1][1] = grid[1][1] + min(dp[0][1], dp[1][0])
         = 5 + min(4, 2)
         = 5 + 2 = 7

dp[1][2] = grid[1][2] + min(dp[0][2], dp[1][1])
         = 1 + min(5, 7)
         = 1 + 5 = 6

dp[2][2] = grid[2][2] + min(dp[1][2], dp[2][1])
         = 1 + min(6, 8)
         = 1 + 6 = 7

Answer: 7

Path with minimum sum:
1 → 3 → 1
        ↓
        1
        ↓
        1

Path: (0,0)→(0,1)→(0,2)→(1,2)→(2,2)
Sum: 1 + 3 + 1 + 1 + 1 = 7 ✓

Time: O(m × n)
Space: O(m × n) or O(n) with optimization
```

### 6. Longest Palindromic Substring

```
Problem: Find longest palindromic substring
s = "babad"

dp[i][j] = True if s[i:j+1] is palindrome

Recurrence:
dp[i][j] = (s[i] == s[j]) and (j-i <= 2 or dp[i+1][j-1])

Build table (diagonal approach):
       b  a  b  a  d
    ┌──┬──┬──┬──┬──┐
b   │ T│  │  │  │  │
    ├──┼──┼──┼──┼──┤
a   │  │ T│  │  │  │
    ├──┼──┼──┼──┼──┤
b   │  │  │ T│  │  │
    ├──┼──┼──┼──┼──┤
a   │  │  │  │ T│  │
    ├──┼──┼──┼──┼──┤
d   │  │  │  │  │ T│
    └──┴──┴──┴──┴──┘

Length 1: All True (single characters)
       b  a  b  a  d
    ┌──┬──┬──┬──┬──┐
b   │ T│  │  │  │  │
    ├──┼──┼──┼──┼──┤
a   │  │ T│  │  │  │
    ├──┼──┼──┼──┼──┤
b   │  │  │ T│  │  │
    ├──┼──┼──┼──┼──┤
a   │  │  │  │ T│  │
    ├──┼──┼──┼──┼──┤
d   │  │  │  │  │ T│
    └──┴──┴──┴──┴──┘

Length 2:
       b  a  b  a  d
    ┌──┬──┬──┬──┬──┐
b   │ T│ F│  │  │  │  ba: b != a
    ├──┼──┼──┼──┼──┤
a   │  │ T│ F│  │  │  ab: a != b
    ├──┼──┼──┼──┼──┤
b   │  │  │ T│ F│  │  ba: b != a
    ├──┼──┼──┼──┼──┤
a   │  │  │  │ T│ F│  ad: a != d
    ├──┼──┼──┼──┼──┤
d   │  │  │  │  │ T│
    └──┴──┴──┴──┴──┘

Length 3:
       b  a  b  a  d
    ┌──┬──┬──┬──┬──┐
b   │ T│ F│ T│  │  │  bab: b==b, dp[1][1]=T ✓
    ├──┼──┼──┼──┼──┤
a   │  │ T│ F│ T│  │  aba: a==a, dp[1][2]=F ✓
    ├──┼──┼──┼──┼──┤
b   │  │  │ T│ F│ F│
    ├──┼──┼──┼──┼──┤
a   │  │  │  │ T│ F│
    ├──┼──┼──┼──┼──┤
d   │  │  │  │  │ T│
    └──┴──┴──┴──┴──┘

Length 4, 5: Continue...

Final:
       b  a  b  a  d
    ┌──┬──┬──┬──┬──┐
b   │ T│ F│ T│ F│ F│
    ├──┼──┼──┼──┼──┤
a   │  │ T│ F│ T│ F│
    ├──┼──┼──┼──┼──┤
b   │  │  │ T│ F│ F│
    ├──┼──┼──┼──┼──┤
a   │  │  │  │ T│ F│
    ├──┼──┼──┼──┼──┤
d   │  │  │  │  │ T│
    └──┴──┴──┴──┴──┘

Longest: "bab" or "aba" (length 3)

Time: O(n²)
Space: O(n²)
```

### 7. Interleaving String

```
Problem: Is s3 formed by interleaving s1 and s2?
s1 = "aabcc"
s2 = "dbbca"
s3 = "aadbbcbcac"

dp[i][j] = True if s3[0:i+j] is interleaving of s1[0:i] and s2[0:j]

Recurrence:
dp[i][j] = (dp[i-1][j] and s1[i-1] == s3[i+j-1]) or
           (dp[i][j-1] and s2[j-1] == s3[i+j-1])

Build table:
s1 = "aabcc"
s2 = "dbbca"
s3 = "aadbbcbcac"

       ""  d  b  b  c  a
    ┌───┬──┬──┬──┬──┬──┐
""  │ T │ F│ F│ F│ F│ F│
    ├───┼──┼──┼──┼──┼──┤
a   │ T │ F│ F│ F│ F│ F│
    ├───┼──┼──┼──┼──┼──┤
a   │ T │ T│ T│ T│ T│ F│
    ├───┼──┼──┼──┼──┼──┤
b   │ F │ T│ T│ F│ T│ F│
    ├───┼──┼──┼──┼──┼──┤
c   │ F │ F│ T│ T│ T│ T│
    ├───┼──┼──┼──┼──┼──┤
c   │ F │ F│ F│ T│ F│ T│
    └───┴──┴──┴──┴──┴──┘

Example calculation:
dp[2][2]: s1[0:2]="aa", s2[0:2]="db", s3[0:4]="aadb"
    From dp[1][2]: s1[1]='a' == s3[3]='b' ✗
    From dp[2][1]: s2[1]='b' == s3[3]='b' ✓
    dp[2][2] = True

dp[5][5]: s1[0:5]="aabcc", s2[0:5]="dbbca", s3[0:10]="aadbbcbcac"
    Result: True ✓

Visual interleaving:
s1: a a b c c
s2:   d b b c a

s3: a a d b b c b c a c
    ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑
    1 1 2 2 2 1 2 1 2 1

Time: O(m × n)
Space: O(m × n)
```

### 8. Regular Expression Matching

```
Problem: Match string with pattern ('.' = any char, '*' = 0 or more prev char)
s = "aab"
p = "c*a*b"

dp[i][j] = True if s[0:i] matches p[0:j]

Recurrence:
if p[j-1] == '*':
    dp[i][j] = dp[i][j-2]  # 0 occurrences
    or (dp[i-1][j] and (s[i-1] == p[j-2] or p[j-2] == '.'))
else:
    dp[i][j] = dp[i-1][j-1] and (s[i-1] == p[j-1] or p[j-1] == '.')

Build table:
s = "aab"
p = "c*a*b"

       ""  c  *  a  *  b
    ┌───┬──┬──┬──┬──┬──┐
""  │ T │ F│ T│ F│ T│ F│
    ├───┼──┼──┼──┼──┼──┤
a   │ F │ F│ F│ T│ T│ F│
    ├───┼──┼──┼──┼──┼──┤
a   │ F │ F│ F│ F│ T│ F│
    ├───┼──┼──┼──┼──┼──┤
b   │ F │ F│ F│ F│ F│ T│
    └───┴──┴──┴──┴──┴──┘

Key cells:
dp[0][2] = T (c* matches empty, 0 occurrences)
dp[1][3] = T ('a' matches 'a')
dp[1][4] = T (a* matches 'a', 1 occurrence)
dp[2][4] = T (a* matches 'aa', 2 occurrences)
dp[3][5] = T ('b' matches 'b')

Answer: True

Pattern matching:
c*a*b
↓ 0 c's
a*b
↓ 2 a's
aab ✓

Time: O(m × n)
Space: O(m × n)
```

## Space Optimization Techniques

### Rolling Array

```
Many 2-D DP problems only need current and previous row:

Original:
dp = [[0] * n for _ in range(m)]

Optimized:
prev = [0] * n
curr = [0] * n

for i in range(m):
    for j in range(n):
        curr[j] = f(prev[j], curr[j-1], prev[j-1])
    prev, curr = curr, prev

Example: Unique Paths
       0   1   2   3
     ┌───┬───┬───┬───┐
  0  │ 1 │ 1 │ 1 │ 1 │  ← Previous row
     ├───┼───┼───┼───┤
  1  │ 1 │ 2 │ 3 │ 4 │  ← Current row
     └───┴───┴───┴───┘

Only need previous row to compute current!

Space: O(m × n) → O(n)
```

## Time and Space Complexity

```
Problem                        Time      Space    Optimized
Unique Paths                   O(m*n)    O(m*n)   O(n)
Unique Paths II                O(m*n)    O(m*n)   O(n)
LCS                            O(m*n)    O(m*n)   O(min(m,n))
Edit Distance                  O(m*n)    O(m*n)   O(min(m,n))
Minimum Path Sum               O(m*n)    O(m*n)   O(n)
Longest Palindrome Substring   O(n²)     O(n²)    O(1) with expand
Interleaving String            O(m*n)    O(m*n)   O(n)
Regular Expression             O(m*n)    O(m*n)   O(n)
```

## Python Implementation

```python
# Unique Paths
def unique_paths(m, n):
    """
    Time: O(m*n), Space: O(n)
    """
    dp = [1] * n

    for i in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j-1]

    return dp[n-1]


# Unique Paths II
def unique_paths_with_obstacles(grid):
    """
    Time: O(m*n), Space: O(n)
    """
    if not grid or grid[0][0] == 1:
        return 0

    m, n = len(grid), len(grid[0])
    dp = [0] * n
    dp[0] = 1

    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:
                dp[j] = 0
            elif j > 0:
                dp[j] += dp[j-1]

    return dp[n-1]


# Longest Common Subsequence
def longest_common_subsequence(text1, text2):
    """
    Time: O(m*n), Space: O(m*n)
    """
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    return dp[m][n]


# Edit Distance
def min_distance(word1, word2):
    """
    Time: O(m*n), Space: O(m*n)
    """
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j],    # delete
                    dp[i][j-1],    # insert
                    dp[i-1][j-1]   # replace
                )

    return dp[m][n]


# Minimum Path Sum
def min_path_sum(grid):
    """
    Time: O(m*n), Space: O(1) in-place
    """
    if not grid:
        return 0

    m, n = len(grid), len(grid[0])

    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:
                continue
            elif i == 0:
                grid[i][j] += grid[i][j-1]
            elif j == 0:
                grid[i][j] += grid[i-1][j]
            else:
                grid[i][j] += min(grid[i-1][j], grid[i][j-1])

    return grid[m-1][n-1]


# Longest Palindromic Substring
def longest_palindrome(s):
    """
    Time: O(n²), Space: O(n²)
    """
    n = len(s)
    if n < 2:
        return s

    dp = [[False] * n for _ in range(n)]
    start, max_len = 0, 1

    # All single characters are palindromes
    for i in range(n):
        dp[i][i] = True

    # Check substrings of length 2+
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1

            if s[i] == s[j]:
                if length == 2 or dp[i+1][j-1]:
                    dp[i][j] = True
                    start = i
                    max_len = length

    return s[start:start + max_len]


# Longest Palindrome - Expand from center (O(1) space)
def longest_palindrome_expand(s):
    """
    Time: O(n²), Space: O(1)
    """
    def expand(left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return right - left - 1

    start, end = 0, 0

    for i in range(len(s)):
        len1 = expand(i, i)      # Odd length
        len2 = expand(i, i + 1)  # Even length
        max_len = max(len1, len2)

        if max_len > end - start:
            start = i - (max_len - 1) // 2
            end = i + max_len // 2

    return s[start:end + 1]


# Interleaving String
def is_interleave(s1, s2, s3):
    """
    Time: O(m*n), Space: O(n)
    """
    m, n, l = len(s1), len(s2), len(s3)

    if m + n != l:
        return False

    dp = [False] * (n + 1)
    dp[0] = True

    for j in range(1, n + 1):
        dp[j] = dp[j-1] and s2[j-1] == s3[j-1]

    for i in range(1, m + 1):
        dp[0] = dp[0] and s1[i-1] == s3[i-1]

        for j in range(1, n + 1):
            dp[j] = (dp[j] and s1[i-1] == s3[i+j-1]) or \
                    (dp[j-1] and s2[j-1] == s3[i+j-1])

    return dp[n]


# Regular Expression Matching
def is_match(s, p):
    """
    Time: O(m*n), Space: O(m*n)
    """
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True

    # Handle patterns like a*, a*b*, etc.
    for j in range(2, n + 1):
        if p[j-1] == '*':
            dp[0][j] = dp[0][j-2]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j-1] == '*':
                # 0 occurrences
                dp[i][j] = dp[i][j-2]
                # 1+ occurrences
                if s[i-1] == p[j-2] or p[j-2] == '.':
                    dp[i][j] = dp[i][j] or dp[i-1][j]
            elif s[i-1] == p[j-1] or p[j-1] == '.':
                dp[i][j] = dp[i-1][j-1]

    return dp[m][n]


# Maximal Square
def maximal_square(matrix):
    """
    Largest square of 1's in binary matrix.
    Time: O(m*n), Space: O(n)
    """
    if not matrix:
        return 0

    m, n = len(matrix), len(matrix[0])
    dp = [0] * (n + 1)
    max_side = 0
    prev = 0

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            temp = dp[j]
            if matrix[i-1][j-1] == '1':
                dp[j] = min(dp[j], dp[j-1], prev) + 1
                max_side = max(max_side, dp[j])
            else:
                dp[j] = 0
            prev = temp

    return max_side * max_side


# Burst Balloons
def max_coins(nums):
    """
    Time: O(n³), Space: O(n²)
    """
    nums = [1] + nums + [1]
    n = len(nums)
    dp = [[0] * n for _ in range(n)]

    for length in range(3, n + 1):
        for left in range(n - length + 1):
            right = left + length - 1

            for i in range(left + 1, right):
                coins = nums[left] * nums[i] * nums[right]
                coins += dp[left][i] + dp[i][right]
                dp[left][right] = max(dp[left][right], coins)

    return dp[0][n-1]
```

## Key Takeaways

1. **Identify 2-D DP**:
   - Two sequences/strings
   - Grid problems
   - Intervals/ranges

2. **State Definition**:
   - dp[i][j] meaning is crucial
   - Often represents up to i in first dimension, j in second

3. **Recurrence**:
   - Usually combines:
     - dp[i-1][j] (from top)
     - dp[i][j-1] (from left)
     - dp[i-1][j-1] (from diagonal)

4. **Base Cases**:
   - First row/column
   - Empty string cases
   - Initialize properly

5. **Fill Order**:
   - Row by row (most common)
   - Diagonal (palindrome problems)
   - Reverse (burst balloons)

6. **Space Optimization**:
   - Often O(n) instead of O(m*n)
   - Rolling array technique
   - In-place modification

7. **Common Patterns**:
   - Grid paths: sum from top and left
   - String matching: match chars or skip
   - Intervals: try all middle points
