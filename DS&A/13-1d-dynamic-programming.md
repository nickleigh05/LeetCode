# 1-D Dynamic Programming

## What is Dynamic Programming?
Dynamic Programming (DP) is an optimization technique that solves complex problems by breaking them down into simpler subproblems. It stores solutions to subproblems to avoid redundant computation.

## Core Concepts

### Two Key Properties

```
1. Optimal Substructure:
   Solution to problem can be constructed from solutions to subproblems

   Example: Fibonacci
   F(5) = F(4) + F(3)
        = [F(3) + F(2)] + [F(2) + F(1)]

2. Overlapping Subproblems:
   Same subproblems are solved multiple times

   Example: Fibonacci recursion tree
            F(5)
           /    \
         F(4)   F(3)
        /  \    /  \
      F(3) F(2) F(2) F(1)
      /  \
    F(2) F(1)

   F(3) computed 2 times
   F(2) computed 3 times
```

### DP vs Recursion vs Greedy

```
Problem: Minimum coins for amount 11
Coins: [1, 5, 10]

Recursion (brute force):
   Try all combinations
   Time: O(amount^n)

DP (memoization):
   Store computed results
   Time: O(amount * n)

Greedy (doesn't always work):
   Take largest coin first
   11 → 10 + 1 ✓ (works here)

   But for coins [1, 3, 4] and amount 6:
   Greedy: 4 + 1 + 1 = 3 coins
   Optimal: 3 + 3 = 2 coins ✗

DP is correct when greedy fails!
```

## DP Approaches

### 1. Top-Down (Memoization)

```
Start from problem, recurse down, cache results

Fibonacci:
def fib(n, memo={}):
    if n in memo:
        return memo[n]

    if n <= 1:
        return n

    memo[n] = fib(n-1, memo) + fib(n-2, memo)
    return memo[n]

Execution for fib(5):

Call fib(5)
├─ Call fib(4)
│  ├─ Call fib(3)
│  │  ├─ Call fib(2)
│  │  │  ├─ Call fib(1) → 1
│  │  │  └─ Call fib(0) → 0
│  │  │  └─ memo[2] = 1
│  │  ├─ Call fib(1) → 1
│  │  └─ memo[3] = 2
│  ├─ Call fib(2) → memo[2] = 1 (cached!)
│  └─ memo[4] = 3
├─ Call fib(3) → memo[3] = 2 (cached!)
└─ memo[5] = 5

Memo after: {2:1, 3:2, 4:3, 5:5}
```

### 2. Bottom-Up (Tabulation)

```
Start from base cases, build up to solution

Fibonacci:
def fib(n):
    if n <= 1:
        return n

    dp = [0] * (n + 1)
    dp[1] = 1

    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]

    return dp[n]

Execution for fib(5):

Initialize: dp = [0, 1, 0, 0, 0, 0]
                  0  1  2  3  4  5

i=2: dp[2] = dp[1] + dp[0] = 1 + 0 = 1
     dp = [0, 1, 1, 0, 0, 0]

i=3: dp[3] = dp[2] + dp[1] = 1 + 1 = 2
     dp = [0, 1, 1, 2, 0, 0]

i=4: dp[4] = dp[3] + dp[2] = 2 + 1 = 3
     dp = [0, 1, 1, 2, 3, 0]

i=5: dp[5] = dp[4] + dp[3] = 3 + 2 = 5
     dp = [0, 1, 1, 2, 3, 5]

Result: dp[5] = 5
```

### Space Optimization

```
Often we only need last few states

Fibonacci (O(n) → O(1) space):

def fib(n):
    if n <= 1:
        return n

    prev2, prev1 = 0, 1

    for i in range(2, n + 1):
        curr = prev1 + prev2
        prev2 = prev1
        prev1 = curr

    return prev1

State transitions:
i=2: prev2=0, prev1=1 → curr=1 → prev2=1, prev1=1
i=3: prev2=1, prev1=1 → curr=2 → prev2=1, prev1=2
i=4: prev2=1, prev1=2 → curr=3 → prev2=2, prev1=3
i=5: prev2=2, prev1=3 → curr=5 → prev2=3, prev1=5

Only need 2 variables instead of array!
```

## Classic 1-D DP Problems

### 1. Climbing Stairs

```
Problem: n stairs, can climb 1 or 2 steps
How many ways to reach top?

n=5:

Stairs: [1] [2] [3] [4] [5]

Recurrence: dp[i] = dp[i-1] + dp[i-2]
- From step i-1: take 1 step
- From step i-2: take 2 steps

Base cases:
- dp[1] = 1 (one way)
- dp[2] = 2 (1+1 or 2)

Build table:
i=1: dp[1] = 1
i=2: dp[2] = 2
i=3: dp[3] = dp[2] + dp[1] = 2 + 1 = 3
i=4: dp[4] = dp[3] + dp[2] = 3 + 2 = 5
i=5: dp[5] = dp[4] + dp[3] = 5 + 3 = 8

dp = [0, 1, 2, 3, 5, 8]
      0  1  2  3  4  5

Visual paths for n=3:
[1] → [2] → [3]   (1+1+1)
[1] → [3]         (1+2)
[2] → [3]         (2+1)

Total: 3 ways ✓

Time: O(n)
Space: O(1) with optimization
```

### 2. House Robber

```
Problem: Houses in row with money
Cannot rob adjacent houses
Maximize money robbed

houses = [2, 7, 9, 3, 1]

Decision at each house:
- Rob it: get money + skip next
- Skip it: continue to next

Recurrence: dp[i] = max(dp[i-1], dp[i-2] + houses[i])
- dp[i-1]: skip house i
- dp[i-2] + houses[i]: rob house i

Build table:
         [2, 7, 9, 3, 1]
index:    0  1  2  3  4

i=0: dp[0] = 2
     Rob house 0

i=1: dp[1] = max(2, 0+7) = 7
     Skip house 0, rob house 1

     Houses: [2, 7*, 9, 3, 1]

i=2: dp[2] = max(7, 2+9) = 11
     Rob houses 0 and 2

     Houses: [2*, 7, 9*, 3, 1]

i=3: dp[3] = max(11, 7+3) = 11
     Keep houses 0 and 2

     Houses: [2*, 7, 9*, 3, 1]

i=4: dp[4] = max(11, 11+1) = 12
     Rob houses 0, 2, and 4

     Houses: [2*, 7, 9*, 3, 1*]

dp = [2, 7, 11, 11, 12]
      0  1   2   3   4

Max money: 12 (houses 0, 2, 4)

Time: O(n)
Space: O(1) with optimization
```

### 3. Coin Change

```
Problem: Minimum coins to make amount
coins = [1, 2, 5], amount = 11

Recurrence: dp[i] = min(dp[i], dp[i-coin] + 1)
For each coin, try using it

Build table:
Amount:  0  1  2  3  4  5  6  7  8  9  10  11
dp:     [0, ∞, ∞, ∞, ∞, ∞, ∞, ∞, ∞, ∞, ∞, ∞]

Base: dp[0] = 0 (0 coins for amount 0)

For coin = 1:
Amount:  0  1  2  3  4  5  6  7  8  9  10  11
dp:     [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

For coin = 2:
i=2: dp[2] = min(2, dp[0]+1) = 1
i=3: dp[3] = min(3, dp[1]+1) = 2
i=4: dp[4] = min(4, dp[2]+1) = 2
...

Amount:  0  1  2  3  4  5  6  7  8  9  10  11
dp:     [0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5,  6]

For coin = 5:
i=5: dp[5] = min(3, dp[0]+1) = 1
i=6: dp[6] = min(3, dp[1]+1) = 2
i=7: dp[7] = min(4, dp[2]+1) = 2
...

Amount:  0  1  2  3  4  5  6  7  8  9  10  11
dp:     [0, 1, 1, 2, 2, 1, 2, 2, 3, 3, 2,  3]

Answer: dp[11] = 3 coins (5 + 5 + 1)

Visual:
11
├─ Use coin 1: 1 + dp[10] = 1 + 2 = 3 ✓
├─ Use coin 2: 1 + dp[9] = 1 + 3 = 4
└─ Use coin 5: 1 + dp[6] = 1 + 2 = 3 ✓

Time: O(amount * coins)
Space: O(amount)
```

### 4. Longest Increasing Subsequence (LIS)

```
Problem: Length of longest increasing subsequence
nums = [10, 9, 2, 5, 3, 7, 101, 18]

Subsequence: not necessarily contiguous
Increasing: strictly increasing

Recurrence: dp[i] = max(dp[j] + 1) for all j < i where nums[j] < nums[i]

Build table:
nums: [10, 9, 2, 5, 3, 7, 101, 18]
dp:   [ 1, 1, 1, 1, 1, 1,  1,  1]

i=0: dp[0] = 1 (base case)
     Subsequence: [10]

i=1: nums[1]=9
     No j where nums[j] < 9
     dp[1] = 1
     Subsequence: [9]

i=2: nums[2]=2
     No j where nums[j] < 2
     dp[2] = 1
     Subsequence: [2]

i=3: nums[3]=5
     j=2: nums[2]=2 < 5
     dp[3] = dp[2] + 1 = 2
     Subsequence: [2, 5]

nums: [10, 9, 2, 5, 3, 7, 101, 18]
dp:   [ 1, 1, 1, 2, 1, 1,  1,  1]

i=4: nums[4]=3
     j=2: nums[2]=2 < 3
     dp[4] = dp[2] + 1 = 2
     Subsequence: [2, 3]

i=5: nums[5]=7
     j=2: nums[2]=2 < 7, dp[2]+1 = 2
     j=3: nums[3]=5 < 7, dp[3]+1 = 3
     j=4: nums[4]=3 < 7, dp[4]+1 = 3
     dp[5] = max(2, 3, 3) = 3
     Subsequence: [2, 5, 7] or [2, 3, 7]

nums: [10, 9, 2, 5, 3, 7, 101, 18]
dp:   [ 1, 1, 1, 2, 2, 3,  1,  1]

i=6: nums[6]=101
     Best: dp[5] + 1 = 4
     Subsequence: [2, 5, 7, 101]

i=7: nums[7]=18
     Best: dp[5] + 1 = 4
     Subsequence: [2, 5, 7, 18]

Final:
nums: [10, 9, 2, 5, 3, 7, 101, 18]
dp:   [ 1, 1, 1, 2, 2, 3,  4,  4]

LIS length: max(dp) = 4

One valid LIS: [2, 5, 7, 101]

Time: O(n²)
Space: O(n)

Binary search optimization: O(n log n)
```

### 5. Maximum Subarray (Kadane's Algorithm)

```
Problem: Find subarray with maximum sum
nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

Recurrence: dp[i] = max(nums[i], dp[i-1] + nums[i])
At each position: start new or extend previous

Build table:
nums: [-2, 1, -3, 4, -1, 2, 1, -5, 4]
dp:   [-2, 1, -2, 4,  3, 5, 6,  1, 5]

i=0: dp[0] = -2
     Subarray: [-2]

i=1: dp[1] = max(1, -2+1) = 1
     Start new: [1]

i=2: dp[2] = max(-3, 1+(-3)) = -2
     Extend: [1, -3]

i=3: dp[3] = max(4, -2+4) = 4
     Start new: [4]

i=4: dp[4] = max(-1, 4+(-1)) = 3
     Extend: [4, -1]

i=5: dp[5] = max(2, 3+2) = 5
     Extend: [4, -1, 2]

i=6: dp[6] = max(1, 5+1) = 6
     Extend: [4, -1, 2, 1]

i=7: dp[7] = max(-5, 6+(-5)) = 1
     Extend: [4, -1, 2, 1, -5]

i=8: dp[8] = max(4, 1+4) = 5
     Extend: [4, -1, 2, 1, -5, 4]

Visual:
nums: [-2, 1, -3, 4, -1, 2, 1, -5, 4]
       ↓   ↓   ↓  ===START===
      -2   1  -2   4   3  5  6   1  5

Max sum: 6 (subarray [4, -1, 2, 1])

Time: O(n)
Space: O(1) with optimization
```

### 6. Decode Ways

```
Problem: Decode string of digits
'A' = 1, 'B' = 2, ..., 'Z' = 26

s = "226"

Possible decodings:
- "2" "2" "6" → "BBF"
- "22" "6" → "VF"
- "2" "26" → "BZ"

Total: 3 ways

Recurrence:
dp[i] = number of ways to decode s[0:i]

if s[i-1] valid (1-9):
    dp[i] += dp[i-1]

if s[i-2:i] valid (10-26):
    dp[i] += dp[i-2]

Build table for "226":
s = "226"
     0 1 2

dp = [1, 0, 0, 0]  (dp[0] = 1, base case)
      ^
      empty string

i=1: s[0] = '2' (valid)
     dp[1] = dp[0] = 1
     Decodings: ["2"]

i=2: s[1] = '2' (valid)
     One digit: dp[2] += dp[1] = 1
     Two digits: "22" (valid)
     dp[2] += dp[0] = 1 + 1 = 2
     Decodings: ["2","2"] and ["22"]

i=3: s[2] = '6' (valid)
     One digit: dp[3] += dp[2] = 2
     Two digits: "26" (valid)
     dp[3] += dp[1] = 2 + 1 = 3
     Decodings: ["2","2","6"], ["22","6"], ["2","26"]

dp = [1, 1, 2, 3]
      0  1  2  3

Answer: 3

Edge cases:
- '0' cannot be decoded alone
- Leading zeros invalid
- "06" invalid (leading zero)
- "60" invalid ('0' alone)

Time: O(n)
Space: O(1) with optimization
```

### 7. Word Break

```
Problem: Can string be segmented into dictionary words?
s = "leetcode"
dict = ["leet", "code"]

DP approach:
dp[i] = True if s[0:i] can be segmented

Build table:
s = "leetcode"
     01234567

dp = [T, F, F, F, F, F, F, F, F]
      ^
      empty string

i=1: "l" not in dict → dp[1] = False
i=2: "le" not in dict → dp[2] = False
i=3: "lee" not in dict → dp[3] = False
i=4: "leet" in dict and dp[0]=True
     dp[4] = True

dp = [T, F, F, F, T, F, F, F, F]
      0  1  2  3  4  5  6  7  8

i=5: Check all splits:
     "leetc" not in dict
     "c" not in dict (from dp[4])
     dp[5] = False

i=6: Similar checks → dp[6] = False
i=7: Similar checks → dp[7] = False

i=8: Check all splits:
     "code" in dict and dp[4]=True
     dp[8] = True

dp = [T, F, F, F, T, F, F, F, T]
      0  1  2  3  4  5  6  7  8

Answer: dp[8] = True

Segmentation: "leet" + "code"

Visual:
    "leetcode"
     ====    ====
     leet    code

Time: O(n² * m) where m = avg word length
Space: O(n)
```

## DP Pattern Recognition

```
1. Counting problems:
   - "How many ways..."
   - Example: Climbing stairs, decode ways

2. Optimization problems:
   - "Maximize/Minimize..."
   - Example: House robber, coin change

3. Decision problems:
   - "Can we..."
   - Example: Word break, partition

4. Sequence problems:
   - Subsequence, subarray
   - Example: LIS, maximum subarray

5. String problems:
   - Matching, editing
   - Example: Edit distance (2D DP)
```

## Time and Space Complexity

```
Problem                   Time      Space    Optimized Space
Fibonacci                 O(n)      O(n)     O(1)
Climbing Stairs           O(n)      O(n)     O(1)
House Robber              O(n)      O(n)     O(1)
Coin Change               O(n*m)    O(n)     O(n)
LIS                       O(n²)     O(n)     O(n log n) with BS
Maximum Subarray          O(n)      O(n)     O(1)
Decode Ways               O(n)      O(n)     O(1)
Word Break                O(n²*m)   O(n)     O(n)

n = input size
m = number of coins/words
```

## Python Implementation

```python
# Fibonacci
def fib(n):
    """
    Time: O(n), Space: O(1)
    """
    if n <= 1:
        return n

    prev2, prev1 = 0, 1
    for _ in range(2, n + 1):
        curr = prev1 + prev2
        prev2, prev1 = prev1, curr

    return prev1


# Climbing Stairs
def climb_stairs(n):
    """
    Time: O(n), Space: O(1)
    """
    if n <= 2:
        return n

    prev2, prev1 = 1, 2
    for _ in range(3, n + 1):
        curr = prev1 + prev2
        prev2, prev1 = prev1, curr

    return prev1


# House Robber
def rob(nums):
    """
    Time: O(n), Space: O(1)
    """
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]

    prev2, prev1 = 0, 0

    for num in nums:
        curr = max(prev1, prev2 + num)
        prev2, prev1 = prev1, curr

    return prev1


# Coin Change
def coin_change(coins, amount):
    """
    Minimum coins to make amount.
    Time: O(amount * coins), Space: O(amount)
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1


# Coin Change - Number of ways
def coin_change_ways(coins, amount):
    """
    Number of ways to make amount.
    Time: O(amount * coins), Space: O(amount)
    """
    dp = [0] * (amount + 1)
    dp[0] = 1

    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] += dp[i - coin]

    return dp[amount]


# Longest Increasing Subsequence
def length_of_lis(nums):
    """
    Time: O(n²), Space: O(n)
    """
    if not nums:
        return 0

    dp = [1] * len(nums)

    for i in range(1, len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)


# LIS - Optimized with Binary Search
def length_of_lis_optimized(nums):
    """
    Time: O(n log n), Space: O(n)
    """
    from bisect import bisect_left

    sub = []

    for num in nums:
        pos = bisect_left(sub, num)

        if pos == len(sub):
            sub.append(num)
        else:
            sub[pos] = num

    return len(sub)


# Maximum Subarray
def max_subarray(nums):
    """
    Kadane's algorithm.
    Time: O(n), Space: O(1)
    """
    max_sum = nums[0]
    curr_sum = nums[0]

    for i in range(1, len(nums)):
        curr_sum = max(nums[i], curr_sum + nums[i])
        max_sum = max(max_sum, curr_sum)

    return max_sum


# Decode Ways
def num_decodings(s):
    """
    Time: O(n), Space: O(1)
    """
    if not s or s[0] == '0':
        return 0

    prev2, prev1 = 1, 1

    for i in range(1, len(s)):
        curr = 0

        # One digit
        if s[i] != '0':
            curr += prev1

        # Two digits
        two_digit = int(s[i-1:i+1])
        if 10 <= two_digit <= 26:
            curr += prev2

        prev2, prev1 = prev1, curr

    return prev1


# Word Break
def word_break(s, word_dict):
    """
    Time: O(n² * m), Space: O(n)
    """
    word_set = set(word_dict)
    dp = [False] * (len(s) + 1)
    dp[0] = True

    for i in range(1, len(s) + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break

    return dp[len(s)]


# Delete and Earn
def delete_and_earn(nums):
    """
    Time: O(n + m), Space: O(m)
    m = max(nums)
    """
    if not nums:
        return 0

    # Convert to house robber
    points = [0] * (max(nums) + 1)
    for num in nums:
        points[num] += num

    # House robber on points
    prev2, prev1 = 0, 0
    for point in points:
        curr = max(prev1, prev2 + point)
        prev2, prev1 = prev1, curr

    return prev1


# Min Cost Climbing Stairs
def min_cost_climbing_stairs(cost):
    """
    Time: O(n), Space: O(1)
    """
    prev2, prev1 = 0, 0

    for i in range(2, len(cost) + 1):
        curr = min(prev1 + cost[i-1], prev2 + cost[i-2])
        prev2, prev1 = prev1, curr

    return prev1


# Jump Game
def can_jump(nums):
    """
    Can reach last index?
    Time: O(n), Space: O(1)
    """
    max_reach = 0

    for i in range(len(nums)):
        if i > max_reach:
            return False

        max_reach = max(max_reach, i + nums[i])

        if max_reach >= len(nums) - 1:
            return True

    return True


# Jump Game II
def jump(nums):
    """
    Minimum jumps to reach end.
    Time: O(n), Space: O(1)
    """
    if len(nums) <= 1:
        return 0

    jumps = 0
    current_end = 0
    farthest = 0

    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])

        if i == current_end:
            jumps += 1
            current_end = farthest

            if current_end >= len(nums) - 1:
                break

    return jumps


# Partition Equal Subset Sum
def can_partition(nums):
    """
    Can partition into two equal sum subsets?
    Time: O(n * sum), Space: O(sum)
    """
    total = sum(nums)

    if total % 2 != 0:
        return False

    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True

    for num in nums:
        for i in range(target, num - 1, -1):
            dp[i] = dp[i] or dp[i - num]

    return dp[target]
```

## Key Takeaways

1. **Identify DP**:
   - Optimal substructure
   - Overlapping subproblems
   - Optimization/counting/decision

2. **Approaches**:
   - Top-down: Recursion + memoization
   - Bottom-up: Iterative tabulation
   - Space optimization: Rolling variables

3. **Steps to Solve**:
   - Define state (dp[i] meaning)
   - Find recurrence relation
   - Set base cases
   - Determine computation order
   - Optimize space if possible

4. **Common Patterns**:
   - Fibonacci-like: dp[i] = f(dp[i-1], dp[i-2])
   - Decision: take it or leave it
   - Partition: subset sum, knapsack
   - Sequences: LIS, subarray

5. **Time Complexity**:
   - Usually O(n) or O(n²)
   - Depends on states × transitions

6. **Space Optimization**:
   - Often reducible to O(1)
   - Keep only necessary states
   - Rolling array technique

7. **When to Use DP**:
   - Optimization problems
   - Counting combinations
   - Decision problems
   - Greedy doesn't work
