# 2-D Dynamic Programming

## 14. 2-D Dynamic Programming (11 problems)

| Problem # | Difficulty | Problem Name | LeetCode Link |
|-----------|------------|--------------|---------------|
| 62 | Medium | Unique Paths | [Link](https://leetcode.com/problems/unique-paths/) |
| 1143 | Medium | Longest Common Subsequence | [Link](https://leetcode.com/problems/longest-common-subsequence/) |
| 309 | Medium | Best Time to Buy and Sell Stock with Cooldown | [Link](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/) |
| 518 | Medium | Coin Change II | [Link](https://leetcode.com/problems/coin-change-ii/) |
| 494 | Medium | Target Sum | [Link](https://leetcode.com/problems/target-sum/) |
| 97 | Medium | Interleaving String | [Link](https://leetcode.com/problems/interleaving-string/) |
| 329 | Hard | Longest Increasing Path in a Matrix | [Link](https://leetcode.com/problems/longest-increasing-path-in-a-matrix/) |
| 115 | Hard | Distinct Subsequences | [Link](https://leetcode.com/problems/distinct-subsequences/) |
| 72 | Hard | Edit Distance | [Link](https://leetcode.com/problems/edit-distance/) |
| 312 | Hard | Burst Balloons | [Link](https://leetcode.com/problems/burst-balloons/) |
| 10 | Hard | Regular Expression Matching | [Link](https://leetcode.com/problems/regular-expression-matching/) |

---

## Data Structures

### 2D DP Table
A grid `dp[i][j]` where each cell stores the answer to a subproblem defined by two dimensions — usually the first `i` elements of one input and the first `j` elements of another. Fill row by row. Often the table can be compressed to one or two rows since each row only depends on the previous one.

---

## Core Patterns

### String DP (LCS, Edit Distance, Distinct Subsequences)
`dp[i][j]` represents the answer for `s1[:i]` and `s2[:j]`. The recurrence depends on whether `s1[i-1] == s2[j-1]`. When characters match, you often get `dp[i-1][j-1] + 1`. When they don't match, you take the best of inserting, deleting, or replacing. Used in LCS, Edit Distance, Distinct Subsequences.

### Grid DP (Unique Paths)
`dp[i][j]` = number of ways to reach cell `(i, j)`. Transitions come from above (`dp[i-1][j]`) and from the left (`dp[i][j-1]`). Base case: first row and first column all equal 1.

### Knapsack Variants (Coin Change II, Target Sum)
Two dimensions: items considered so far (row) and remaining target/capacity (column). Coin Change II counts combinations — iterate coins as rows and amounts as columns. Target Sum can be reframed as a subset-sum knapsack.

### State Machine DP (Stock with Cooldown)
Multiple states: "holding", "sold", "cooldown". `dp[i][state]` = max profit on day `i` in that state. Transitions are: buy (held → holding), sell (holding → sold), cooldown (sold → cooldown → held).

### Interval DP (Burst Balloons)
`dp[i][j]` = max coins from bursting all balloons between `i` and `j`. Try each balloon `k` as the **last** to be burst in that range — it's adjacent to the boundary balloons `i-1` and `j+1` at that moment. Build solutions from small intervals to large. Used in Burst Balloons.

### Memoized DFS on Matrix (Longest Increasing Path)
DFS from each cell, only moving to neighbors with strictly greater values. Cache results — `memo[i][j]` is the longest increasing path starting at `(i, j)`. No need for a visited set because the strictly increasing constraint prevents cycles.
