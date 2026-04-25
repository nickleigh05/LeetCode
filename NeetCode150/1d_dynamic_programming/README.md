# 1-D Dynamic Programming

## 13. 1-D Dynamic Programming (12 problems)

| Problem # | Difficulty | Problem Name | LeetCode Link |
|-----------|------------|--------------|---------------|
| 70 | Easy | Climbing Stairs | [Link](https://leetcode.com/problems/climbing-stairs/) |
| 746 | Easy | Min Cost Climbing Stairs | [Link](https://leetcode.com/problems/min-cost-climbing-stairs/) |
| 198 | Medium | House Robber | [Link](https://leetcode.com/problems/house-robber/) |
| 213 | Medium | House Robber II | [Link](https://leetcode.com/problems/house-robber-ii/) |
| 5 | Medium | Longest Palindromic Substring | [Link](https://leetcode.com/problems/longest-palindromic-substring/) |
| 647 | Medium | Palindromic Substrings | [Link](https://leetcode.com/problems/palindromic-substrings/) |
| 91 | Medium | Decode Ways | [Link](https://leetcode.com/problems/decode-ways/) |
| 322 | Medium | Coin Change | [Link](https://leetcode.com/problems/coin-change/) |
| 152 | Medium | Maximum Product Subarray | [Link](https://leetcode.com/problems/maximum-product-subarray/) |
| 139 | Medium | Word Break | [Link](https://leetcode.com/problems/word-break/) |
| 300 | Medium | Longest Increasing Subsequence | [Link](https://leetcode.com/problems/longest-increasing-subsequence/) |
| 416 | Medium | Partition Equal Subset Sum | [Link](https://leetcode.com/problems/partition-equal-subset-sum/) |

---

## Data Structures

### DP Array
A 1D array `dp` where `dp[i]` stores the answer for a subproblem of size `i`. You fill it left to right, building each answer from previously computed values. Often the full array can be compressed to just a few variables when you only need the last 1–2 values.

### Memoization (Top-Down)
A hash map (or array) that caches the result of recursive calls. The first time you compute `f(i)`, store it. On subsequent calls with the same `i`, return the cached result. Prevents exponential recomputation.

---

## Core Patterns

### Fibonacci-Style (Decision at Each Step)
`dp[i]` depends on a small, fixed number of previous states. Classic form: `dp[i] = dp[i-1] + dp[i-2]`. Used in Climbing Stairs, Min Cost Climbing Stairs.

### House Robber Pattern
Can't take two adjacent elements. `dp[i] = max(dp[i-1], dp[i-2] + nums[i])`. Compress to two variables. For a circular array (House Robber II), run the DP twice — once on `nums[0..n-2]` and once on `nums[1..n-1]`.

### Unbounded Knapsack (Coin Change)
Each item can be used unlimited times. `dp[i] = min(dp[i - coin] + 1)` for all coins ≤ i. Initialize `dp[0] = 0` and everything else to infinity.

### 0/1 Knapsack (Partition Equal Subset Sum)
Each item can only be used once. Iterate through items, update the DP array **backwards** (right to left) to avoid using the same item twice. `dp[j] = dp[j] or dp[j - nums[i]]`.

### Longest Increasing Subsequence (LIS)
`dp[i]` = length of the longest increasing subsequence ending at index `i`. For each `i`, look back at all `j < i` where `nums[j] < nums[i]` and take `dp[j] + 1`. O(n²). Can be optimized to O(n log n) with binary search on a maintained "patience sorting" array.

### Expand Around Center (Palindromes)
For each character (and each gap between characters), expand outward as long as both sides match. O(n²) but very clean. Used in Longest Palindromic Substring, Palindromic Substrings.

### Kadane's Algorithm (Maximum Subarray / Product)
Track the best result ending at the current position. For sum: `curr = max(nums[i], curr + nums[i])`. For product: track both max and min ending here (since a negative times a negative becomes positive).
