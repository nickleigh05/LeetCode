# 1-D Dynamic Programming

## How to use this README

Problems are split into three tiers: Blind 75 is the core set every interviewer expects you to know cold. NeetCode 150 adds problems that sharpen the same patterns with more constraints. NeetCode 250 introduces new patterns (game theory DP, counting orderings, BFS/DP hybrids) and pushes each technique to its limit. Work through tiers in order — the Core Patterns and Syntax Reference sections below map directly to the problems in each table, so when you hit a new problem, find the matching pattern first, then check the syntax.

---

## Problems

### Blind 75
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved |
|-----------|------------|--------------|---------------|--------|
| 70 | Easy | Climbing Stairs | [Link](https://leetcode.com/problems/climbing-stairs/) | ☐ |
| 198 | Medium | House Robber | [Link](https://leetcode.com/problems/house-robber/) | ☐ |
| 213 | Medium | House Robber II | [Link](https://leetcode.com/problems/house-robber-ii/) | ☐ |
| 5 | Medium | Longest Palindromic Substring | [Link](https://leetcode.com/problems/longest-palindromic-substring/) | ☐ |
| 647 | Medium | Palindromic Substrings | [Link](https://leetcode.com/problems/palindromic-substrings/) | ☐ |
| 91 | Medium | Decode Ways | [Link](https://leetcode.com/problems/decode-ways/) | ☐ |
| 322 | Medium | Coin Change | [Link](https://leetcode.com/problems/coin-change/) | ☐ |
| 152 | Medium | Maximum Product Subarray | [Link](https://leetcode.com/problems/maximum-product-subarray/) | ☐ |
| 139 | Medium | Word Break | [Link](https://leetcode.com/problems/word-break/) | ☐ |
| 300 | Medium | Longest Increasing Subsequence | [Link](https://leetcode.com/problems/longest-increasing-subsequence/) | ☐ |

### NeetCode 150
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved |
|-----------|------------|--------------|---------------|--------|
| 746 | Easy | Min Cost Climbing Stairs | [Link](https://leetcode.com/problems/min-cost-climbing-stairs/) | ☐ |
| 416 | Medium | Partition Equal Subset Sum | [Link](https://leetcode.com/problems/partition-equal-subset-sum/) | ☐ |

### NeetCode 250
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved | Pattern |
|-----------|------------|--------------|---------------|--------|---------|
| 1137 | Easy | N-th Tribonacci Number | [Link](https://leetcode.com/problems/n-th-tribonacci-number/) | ☐ | Fibonacci-style DP |
| 377 | Medium | Combination Sum IV | [Link](https://leetcode.com/problems/combination-sum-iv/) | ☐ | Count of orderings |
| 279 | Medium | Perfect Squares | [Link](https://leetcode.com/problems/perfect-squares/) | ☐ | BFS / DP |
| 343 | Medium | Integer Break | [Link](https://leetcode.com/problems/integer-break/) | ☐ | Math / DP |
| 1406 | Hard | Stone Game III | [Link](https://leetcode.com/problems/stone-game-iii/) | ☐ | Game theory DP |

---

## Complexity Reference

| Pattern / Operation | Time | Space | Notes |
|---------------------|------|-------|-------|
| Bottom-up tabulation | O(n) | O(n) | Fill dp array once left to right |
| Space-optimized DP (two vars) | O(n) | O(1) | Replace dp array with prev/curr vars |
| Knapsack (0/1) | O(n·W) | O(W) | n items, W capacity; inner loop reversed |
| Coin change (unbounded) | O(n·amount) | O(amount) | Each coin reusable; inner loop forward |
| LIS (patience sort) | O(n log n) | O(n) | Binary search on tails array |
| LIS (basic DP) | O(n²) | O(n) | For each i, scan all j < i |
| Palindrome (center expand) | O(n²) | O(1) | 2n-1 centers, expand each |
| Palindrome (DP table) | O(n²) | O(n²) | dp[i][j] = is s[i..j] a palindrome |
| Kadane's / max product scan | O(n) | O(1) | Track running best + running min/max |
| Word break (DP) | O(n²·k) | O(n) | k = avg word length for substring check |

---

## Data Structures

### The dp Array (1-D table)

The core structure for 1-D DP. `dp[i]` stores the answer to the subproblem "what is the best result for input size i (or ending at index i)?" You fill it left to right, and each cell's value depends only on previously filled cells — no recursion needed.

```
Problem: Climbing Stairs — dp[i] = number of ways to reach step i

i:    0    1    2    3    4    5
    +----+----+----+----+----+----+
dp: | 1  | 1  | 2  | 3  | 5  | 8  |
    +----+----+----+----+----+----+
         ↑         ↑
      base case   dp[3] = dp[2] + dp[1]  (take 1 or 2 steps)

Fill direction: left → right
Dependency:    dp[i] depends on dp[i-1] and dp[i-2]
```

**When it matters:** Any problem where the answer for size n can be built from answers for smaller sizes. Recognize these by the phrase "optimal substructure" — the best solution to n contains best solutions to sub-problems.

### Space-Optimized Variables (rolling state)

When `dp[i]` only needs `dp[i-1]` and maybe `dp[i-2]`, you don't need the full array. Replace it with two variables and update them in a rolling fashion. Cuts space from O(n) to O(1).

```
House Robber — replace dp array with two variables:

Full array:    dp = [0, 2, 4, 4, 7, 8, ...]
                          ↑ only these two matter
Rolling vars:  prev2=0, prev1=0  →  curr = max(prev1, prev2 + nums[i])
               then shift: prev2 = prev1, prev1 = curr

State at each step:
  Step 0: prev2=0,  prev1=0,  curr=2  → (prev2=0,  prev1=2)
  Step 1: prev2=2,  prev1=2,  curr=4  → (prev2=2,  prev1=4)
  Step 2: prev2=4,  prev1=4,  curr=4  → (prev2=4,  prev1=4)
  ...
```

**When it matters:** Whenever the dp recurrence only looks back 1 or 2 positions. Always try to space-optimize after getting the O(n) solution working.

### Memoization Cache (top-down DP)

A dict or array that caches the result of each recursive call. First call computes the answer; subsequent calls return the cached value in O(1). Equivalent to bottom-up but written recursively — useful when the subproblem space is sparse or the recurrence is hard to reverse.

```
Word Break — memo[i] = can s[i:] be segmented?

Recursion tree (without memo):          With memo:
canBreak("leetcode")                    compute once, reuse
├── canBreak("etcode")   ← computed     memo = {7: True, 4: True, 0: True}
│   ├── canBreak("code") ← computed
│   │   └── canBreak("") ← True
...
```

**When it matters:** Top-down is easier to write when you're unsure of the fill order. Bottom-up is faster in practice (no recursion overhead). Both are O(n) for the same subproblem set.

---

## Core Patterns

### Bottom-up Tabulation
**When to use:** The subproblems form a linear sequence and each answer depends on a fixed number of previous answers.
**Complexity:** O(n) time, O(n) space (O(1) with space optimization)
**Problems:** Climbing Stairs (#70), House Robber (#198), Min Cost Climbing Stairs (#746), Tribonacci (#1137)
**Common mistake:** Initializing base cases wrong — always think through dp[0] and dp[1] before writing the loop.

```python
dp = [0] * (n + 1)
dp[0] = 1   # base case: 1 way to reach step 0
dp[1] = 1   # base case: 1 way to reach step 1
for i in range(2, n + 1):
    dp[i] = dp[i - 1] + dp[i - 2]
return dp[n]
```

### Space Optimization
**When to use:** `dp[i]` only depends on `dp[i-1]` (and maybe `dp[i-2]`). Replace the array with rolling variables.
**Complexity:** O(n) time, O(1) space
**Problems:** Climbing Stairs (#70), House Robber (#198/#213), Min Cost Climbing Stairs (#746)
**Common mistake:** Updating variables in the wrong order — always compute `curr` before overwriting `prev`.

```python
prev2, prev1 = 0, 0
for num in nums:
    curr = max(prev1, prev2 + num)
    prev2 = prev1
    prev1 = curr
return prev1
```

### Knapsack (Bounded Choice)
**When to use:** At each item, you choose to include or exclude it. Total capacity or sum is bounded.
**Complexity:** O(n·W) time, O(W) space
**Problems:** Partition Equal Subset Sum (#416), Combination Sum IV (#377)
**Common mistake:** For 0/1 knapsack, iterate the inner loop in reverse to prevent using the same item twice. For unbounded (coin change), iterate forward.

```python
dp = [False] * (target + 1)
dp[0] = True
for num in nums:
    for j in range(target, num - 1, -1):  # reverse for 0/1 knapsack
        dp[j] = dp[j] or dp[j - num]
return dp[target]
```

### Linear Scan DP with Running Tracker
**When to use:** The answer at each position depends on a running min or max seen so far — not just the immediately previous element.
**Complexity:** O(n) time, O(1) space
**Problems:** Maximum Product Subarray (#152), Maximum Subarray (#53)
**Common mistake:** For product subarray, a negative number flips min to max — always track both current_min and current_max simultaneously.

```python
max_prod = min_prod = result = nums[0]
for n in nums[1:]:
    candidates = (n, max_prod * n, min_prod * n)
    max_prod = max(candidates)
    min_prod = min(candidates)
    result = max(result, max_prod)
return result
```

### Palindrome Expansion
**When to use:** You need to find or count palindromic substrings. Expand around every possible center.
**Complexity:** O(n²) time, O(1) space
**Problems:** Longest Palindromic Substring (#5), Palindromic Substrings (#647)
**Common mistake:** Forgetting even-length palindromes — there are 2n-1 centers total (n odd centers, n-1 even centers between adjacent characters).

```python
def expand(s, l, r):
    while l >= 0 and r < len(s) and s[l] == s[r]:
        l -= 1
        r += 1
    return r - l - 1  # length of palindrome found

for i in range(len(s)):
    odd_len  = expand(s, i, i)      # odd-length palindromes
    even_len = expand(s, i, i + 1)  # even-length palindromes
```

---

## Syntax Reference

### Building and Initializing a dp Array

```python
dp = [0] * (n + 1)         # n+1 slots so dp[n] is valid
dp = [float('inf')] * (n + 1)  # use inf for "minimum cost" problems
dp = [False] * (target + 1)    # use bool for "can we reach X" problems
dp[0] = 0   # base case — always set before the loop
```

### Iterating with Lookback

```python
# standard left-to-right fill
for i in range(1, n + 1):
    dp[i] = dp[i - 1] + dp[i - 2]   # Fibonacci-style

# inner loop reversed (0/1 knapsack — prevent reusing same item)
for num in nums:
    for j in range(target, num - 1, -1):
        dp[j] = dp[j] or dp[j - num]

# inner loop forward (unbounded knapsack — coin change, can reuse coins)
for coin in coins:
    for j in range(coin, amount + 1):
        dp[j] = min(dp[j], dp[j - coin] + 1)
```

### Memoization with functools.lru_cache

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def dp(i):
    if i <= 1:
        return i
    return dp(i - 1) + dp(i - 2)
```

> `lru_cache` turns any recursive function into a memoized one automatically. `maxsize=None` means unbounded cache. Equivalent to writing a `memo` dict manually but cleaner.

### Coin Change Pattern (Unbounded Knapsack)

```python
dp = [float('inf')] * (amount + 1)
dp[0] = 0
for coin in coins:
    for j in range(coin, amount + 1):
        dp[j] = min(dp[j], dp[j - coin] + 1)
return dp[amount] if dp[amount] != float('inf') else -1
```

### LIS (Longest Increasing Subsequence)

```python
# O(n^2) DP
dp = [1] * len(nums)
for i in range(len(nums)):
    for j in range(i):
        if nums[j] < nums[i]:
            dp[i] = max(dp[i], dp[j] + 1)
return max(dp)

# O(n log n) with binary search (patience sorting)
import bisect
tails = []
for num in nums:
    pos = bisect.bisect_left(tails, num)
    if pos == len(tails):
        tails.append(num)
    else:
        tails[pos] = num
return len(tails)
```

### Handling String Indices in DP

```python
# Decode Ways (#91) — 1-indexed dp on 0-indexed string
dp = [0] * (len(s) + 1)
dp[0] = 1           # empty string: 1 way
dp[1] = 0 if s[0] == '0' else 1
for i in range(2, len(s) + 1):
    one_digit = int(s[i-1])
    two_digit = int(s[i-2:i])
    if one_digit >= 1:
        dp[i] += dp[i - 1]
    if 10 <= two_digit <= 26:
        dp[i] += dp[i - 2]
```
