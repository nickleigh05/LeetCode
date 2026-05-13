# 2-D Dynamic Programming

## How to use this README

Problems are split into three tiers: Blind 75 is the core set every interviewer expects you to know cold. NeetCode 150 adds problems that sharpen the same patterns with more constraints — stock state machines, interval DP, and full string-matching recurrences. NeetCode 250 extends those patterns into game theory and grid obstacles. Work through tiers in order — the Core Patterns and Syntax Reference sections below map directly to the problems in each table, so when you hit a new problem, identify whether it is grid DP, string DP, interval DP, or a state machine first, then find the matching pattern.

---

## Problems

### Blind 75
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved |
|-----------|------------|--------------|---------------|--------|
| 62 | Medium | Unique Paths | [Link](https://leetcode.com/problems/unique-paths/) | ☐ |
| 1143 | Medium | Longest Common Subsequence | [Link](https://leetcode.com/problems/longest-common-subsequence/) | ☐ |

### NeetCode 150
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved |
|-----------|------------|--------------|---------------|--------|
| 309 | Medium | Best Time to Buy and Sell Stock with Cooldown | [Link](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/) | ☐ |
| 518 | Medium | Coin Change II | [Link](https://leetcode.com/problems/coin-change-ii/) | ☐ |
| 494 | Medium | Target Sum | [Link](https://leetcode.com/problems/target-sum/) | ☐ |
| 97 | Medium | Interleaving String | [Link](https://leetcode.com/problems/interleaving-string/) | ☐ |
| 329 | Hard | Longest Increasing Path in a Matrix | [Link](https://leetcode.com/problems/longest-increasing-path-in-a-matrix/) | ☐ |
| 115 | Hard | Distinct Subsequences | [Link](https://leetcode.com/problems/distinct-subsequences/) | ☐ |
| 72 | Medium | Edit Distance | [Link](https://leetcode.com/problems/edit-distance/) | ☐ |
| 312 | Hard | Burst Balloons | [Link](https://leetcode.com/problems/burst-balloons/) | ☐ |
| 10 | Hard | Regular Expression Matching | [Link](https://leetcode.com/problems/regular-expression-matching/) | ☐ |

### NeetCode 250
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved | Pattern |
|-----------|------------|--------------|---------------|--------|---------|
| 63 | Medium | Unique Paths II | [Link](https://leetcode.com/problems/unique-paths-ii/) | ☐ | Grid DP with obstacles |
| 64 | Medium | Minimum Path Sum | [Link](https://leetcode.com/problems/minimum-path-sum/) | ☐ | Grid DP min cost |
| 1049 | Medium | Last Stone Weight II | [Link](https://leetcode.com/problems/last-stone-weight-ii/) | ☐ | Knapsack variant |
| 877 | Medium | Stone Game | [Link](https://leetcode.com/problems/stone-game/) | ☐ | Game theory 2D DP |
| 1140 | Medium | Stone Game II | [Link](https://leetcode.com/problems/stone-game-ii/) | ☐ | Game theory 2D DP |

---

## Complexity Reference

| Pattern / Operation | Time | Space | Notes |
|---------------------|------|-------|-------|
| Grid DP (m×n grid) | O(m·n) | O(m·n) | Can often compress to O(n) per row |
| Grid DP (space-optimized) | O(m·n) | O(n) | Keep only previous row |
| LCS / Edit Distance | O(m·n) | O(m·n) | m, n = lengths of two strings |
| LCS / Edit Distance (optimized) | O(m·n) | O(n) | One rolling row |
| Interval DP (Burst Balloons) | O(n³) | O(n²) | All pairs i,j × all split points k |
| State machine DP (stocks) | O(n) | O(1) | Fixed number of states per day |
| Coin Change II (count ways) | O(n·amount) | O(amount) | Unbounded knapsack counting |
| Target Sum (count with +/-) | O(n·total) | O(total) | Convert to subset-sum count |
| Distinct Subsequences | O(m·n) | O(m·n) | Standard string DP |
| Regex Matching | O(m·n) | O(m·n) | Hardest: handle * lookahead |

---

## Data Structures

### The 2-D dp Table

The core structure for 2-D DP. `dp[i][j]` stores the answer to the subproblem defined by two parameters — usually two string indices, or row and column in a grid. You fill the table in a specific direction, and each cell depends only on cells already computed.

```
LCS of "abcde" and "ace" — dp[i][j] = LCS length for s1[:i] vs s2[:j]

        ""   a    c    e
    ""  [ 0 | 0 | 0 | 0 ]
    a   [ 0 | 1 | 1 | 1 ]
    b   [ 0 | 1 | 1 | 1 ]
    c   [ 0 | 1 | 2 | 2 ]
    d   [ 0 | 1 | 2 | 2 ]
    e   [ 0 | 1 | 2 | 3 ]  ← answer
              ↑
         fill left→right, top→bottom

If s1[i-1] == s2[j-1]:  dp[i][j] = dp[i-1][j-1] + 1   ← diagonal
Else:                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
```

**When it matters:** Any problem where you're comparing two sequences, navigating a grid, or splitting a range into sub-ranges.

### Grid DP Table (Unique Paths style)

For grid navigation problems, `dp[i][j]` = answer for reaching or leaving cell (i, j). Base cases are the first row and first column. The fill direction is always top-left to bottom-right when moves are only right and down.

```
Unique Paths — dp[i][j] = number of paths to reach (i, j)

     col→  0    1    2    3
row↓   0 [ 1  | 1  | 1  | 1  ]   ← first row: only 1 way (go right)
       1 [ 1  | 2  | 3  | 4  ]
       2 [ 1  | 3  | 6  | 10 ]   ← answer

dp[i][j] = dp[i-1][j] + dp[i][j-1]
           (from above) (from left)

Fill direction:  →→→
                 →→→
                 →→→  (top-left to bottom-right)
```

**When it matters:** Grid traversal problems. If there are obstacles, set `dp[i][j] = 0` when `grid[i][j] == 1`.

### Interval DP Table (Burst Balloons)

For interval DP, `dp[i][j]` = best answer for the subarray from i to j (inclusive). Fill by increasing interval length so shorter subproblems are always solved before longer ones.

```
Burst Balloons — dp[i][j] = max coins for bursting all balloons in i..j

         j→  0    1    2    3
i↓  0      [  0 |  ? |  ? |  ? ]
    1      [  - |  0 |  ? |  ? ]
    2      [  - |  - |  0 |  ? ]
    3      [  - |  - |  - |  0 ]

Fill by length:  length=1, then length=2, ...
For each (i,j): try every split point k as the LAST balloon to burst
  dp[i][j] = max(dp[i][k-1] + nums[i-1]*nums[k]*nums[j+1] + dp[k+1][j])

Fill direction:  diagonals, short→long
```

**When it matters:** Problems where you split a range at a "last" choice point (Burst Balloons, Stone Game). Think "what is the last thing I do in range [i..j]?"

---

## Core Patterns

### Grid DP
**When to use:** Navigate a 2-D grid from top-left to bottom-right, counting paths or minimizing/maximizing cost.
**Complexity:** O(m·n) time, O(n) space with row compression
**Problems:** Unique Paths (#62), Unique Paths II (#63), Minimum Path Sum (#64)
**Common mistake:** Forgetting to handle the first row and first column as base cases before the main nested loop.

```python
m, n = len(grid), len(grid[0])
dp = [[0] * n for _ in range(m)]
dp[0][0] = 1
for i in range(m):
    for j in range(n):
        if i > 0: dp[i][j] += dp[i-1][j]
        if j > 0: dp[i][j] += dp[i][j-1]
return dp[m-1][n-1]
```

### String Comparison DP (LCS, Edit Distance)
**When to use:** Compare two strings character by character. `dp[i][j]` = answer for `s1[:i]` vs `s2[:j]`.
**Complexity:** O(m·n) time, O(m·n) space (O(n) with row compression)
**Problems:** Longest Common Subsequence (#1143), Edit Distance (#72), Distinct Subsequences (#115), Interleaving String (#97)
**Common mistake:** Off-by-one — `dp[i][j]` represents the first i characters of s1 and first j of s2, so `s1[i-1]` and `s2[j-1]` are the characters at those positions.

```python
m, n = len(s1), len(s2)
dp = [[0] * (n + 1) for _ in range(m + 1)]
for i in range(1, m + 1):
    for j in range(1, n + 1):
        if s1[i-1] == s2[j-1]:
            dp[i][j] = dp[i-1][j-1] + 1        # characters match — use diagonal
        else:
            dp[i][j] = max(dp[i-1][j], dp[i][j-1])  # take best of drop-one
return dp[m][n]
```

### Interval DP (Burst Balloons)
**When to use:** The optimal answer for range [i..j] depends on choosing a "last" element k inside that range and combining the answers for [i..k-1] and [k+1..j].
**Complexity:** O(n³) time, O(n²) space
**Problems:** Burst Balloons (#312)
**Common mistake:** Thinking about the first balloon to burst, not the last. The "last burst" framing works because at that point the left and right neighbors are fixed (they are the boundaries, not other balloons).

```python
nums = [1] + nums + [1]        # pad with 1s at edges
n = len(nums)
dp = [[0] * n for _ in range(n)]
for length in range(2, n):     # interval length
    for left in range(0, n - length):
        right = left + length
        for k in range(left + 1, right):  # k = last balloon to burst
            dp[left][right] = max(
                dp[left][right],
                dp[left][k] + nums[left]*nums[k]*nums[right] + dp[k][right]
            )
return dp[0][n-1]
```

### State Machine DP (Stock Problems)
**When to use:** You have a fixed set of discrete states (holding, not holding, on cooldown) and transition between them day by day.
**Complexity:** O(n) time, O(1) space
**Problems:** Best Time to Buy/Sell Stock with Cooldown (#309)
**Common mistake:** Updating all state variables at the same time with the old values — compute new values into temps first, then assign.

```python
# States: holding, not holding (can buy), cooldown
hold = -float('inf')
free = 0
cool = 0
for price in prices:
    hold, free, cool = (
        max(hold, free - price),   # keep holding, or buy from free state
        max(free, cool),           # stay free, or exit cooldown
        hold + price               # sell what we're holding → go to cooldown
    )
return max(free, cool)
```

---

## Syntax Reference

### Building a 2-D dp Table

```python
m, n = len(s1), len(s2)
dp = [[0] * (n + 1) for _ in range(m + 1)]
# Note: do NOT use [[0] * (n+1)] * (m+1) — that creates m references to the SAME row

# Access:
dp[i][j]         # row i, column j
dp[i-1][j-1]     # diagonal (used in LCS when chars match)
dp[i-1][j]       # cell above (delete from s1)
dp[i][j-1]       # cell to left (delete from s2)
```

### Space Optimization (keep only previous row)

```python
prev = [0] * (n + 1)
for i in range(1, m + 1):
    curr = [0] * (n + 1)
    for j in range(1, n + 1):
        if s1[i-1] == s2[j-1]:
            curr[j] = prev[j-1] + 1
        else:
            curr[j] = max(prev[j], curr[j-1])
    prev = curr
return prev[n]
```

### Edit Distance Recurrence

```python
# dp[i][j] = min edits to turn s1[:i] into s2[:j]
if s1[i-1] == s2[j-1]:
    dp[i][j] = dp[i-1][j-1]          # no edit needed
else:
    dp[i][j] = 1 + min(
        dp[i-1][j],    # delete from s1
        dp[i][j-1],    # insert into s1 (= delete from s2)
        dp[i-1][j-1]   # replace
    )
```

### Interval DP Loop Order

```python
# ALWAYS iterate by length first, then left endpoint
for length in range(2, n):
    for left in range(0, n - length):
        right = left + length
        for k in range(left + 1, right):   # split point
            dp[left][right] = max(dp[left][right], ...)
```

> The key invariant: when computing `dp[left][right]`, all sub-intervals `dp[left][k]` and `dp[k][right]` have already been filled because they are shorter.

### Coin Change II (Count Ways — Unbounded Knapsack)

```python
dp = [0] * (amount + 1)
dp[0] = 1
for coin in coins:
    for j in range(coin, amount + 1):   # forward — coin is reusable
        dp[j] += dp[j - coin]
return dp[amount]
```

> Forward inner loop = unbounded (can reuse coins). Reverse inner loop = 0/1 (each coin once).

### Target Sum → Subset Sum Conversion

```python
# Instead of exploring +/- for each num, convert to:
# find subsets with sum = (total + target) // 2
total = sum(nums)
if (total + target) % 2 != 0:
    return 0
goal = (total + target) // 2
dp = [0] * (goal + 1)
dp[0] = 1
for num in nums:
    for j in range(goal, num - 1, -1):   # reverse — each num used once
        dp[j] += dp[j - num]
return dp[goal]
```
