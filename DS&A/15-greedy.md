# Greedy Algorithms

## What is a Greedy Algorithm?
A greedy algorithm makes the locally optimal choice at each step with the hope of finding a global optimum. It never reconsiders choices, making decisions based on current information without looking at future consequences.

## Core Concepts

### Greedy vs Dynamic Programming

```
Problem: Coin change for amount 11, coins [1, 5, 10]

Greedy approach:
    11
    ↓ take largest (10)
    1
    ↓ take largest (1)
    0

    Result: 2 coins (10 + 1) ✓

Problem: Coin change for amount 6, coins [1, 3, 4]

Greedy approach:
    6
    ↓ take largest (4)
    2
    ↓ take largest (1)
    1
    ↓ take largest (1)
    0

    Result: 3 coins (4 + 1 + 1) ✗

DP approach:
    6
    ├─ 3 + 3 = 2 coins ✓ (optimal)
    └─ 4 + 1 + 1 = 3 coins

Greedy doesn't always work!
Works when problem has greedy-choice property
```

### Greedy Choice Property

```
Definition: Locally optimal choice leads to globally optimal solution

Examples that WORK:
✓ Activity selection (choose earliest ending)
✓ Huffman coding (merge smallest frequencies)
✓ Minimum spanning tree (smallest edge)
✓ Fractional knapsack (highest value/weight)

Examples that DON'T WORK:
✗ 0/1 knapsack (need DP)
✗ Longest path in graph
✗ Some coin change problems
```

## Classic Greedy Problems

### 1. Jump Game

```
Problem: Can reach last index?
nums = [2,3,1,1,4]

Greedy: Track maximum reachable position

Index:    0  1  2  3  4
nums:    [2, 3, 1, 1, 4]
         ↓
max_reach: 0

Step 1: At index 0
    max_reach = max(0, 0 + nums[0]) = 2

    0  1  2  3  4
   [2, 3, 1, 1, 4]
    ═══════
    reachable

Step 2: At index 1
    max_reach = max(2, 1 + nums[1]) = 4

    0  1  2  3  4
   [2, 3, 1, 1, 4]
    ═══════════════
    can reach end!

Answer: True ✓

Visual:
    0  1  2  3  4
   [2, 3, 1, 1, 4]
    ↓  ↓
    can jump to 1,2
       from 1 can jump to 2,3,4
       reached end!

Failure case:
nums = [3,2,1,0,4]

    0  1  2  3  4
   [3, 2, 1, 0, 4]
    ═══════════
    stuck at 3 (can't jump over 0)

Answer: False ✗

Time: O(n)
Space: O(1)
```

### 2. Jump Game II

```
Problem: Minimum jumps to reach end
nums = [2,3,1,1,4]

Greedy: BFS-like, jump to farthest in current range

Index:      0  1  2  3  4
nums:      [2, 3, 1, 1, 4]
jumps:      0  1  1  2  2

Step 1: Start at 0
    current_end = 0
    farthest = 0
    jumps = 0

    From 0, can reach: 1, 2
    farthest = max(0 + 2) = 2

Step 2: Reached end of jump 0 (index 0)
    jumps = 1
    current_end = 2

    Level 1:  [1, 2]
            nums: [3, 1]

    From 1: reach 2,3,4 → farthest = 4
    From 2: reach 3 → already covered

Step 3: Reached end (4) ✓
    jumps = 2

Visual levels:
Level 0: [0]
Level 1: [1, 2]
Level 2: [3, 4]

Minimum jumps: 2
Path: 0 → 1 → 4

Time: O(n)
Space: O(1)
```

### 3. Gas Station

```
Problem: Starting gas station to complete circuit
gas   = [1,2,3,4,5]
cost  = [3,4,5,1,2]

Greedy insight: If total gas ≥ total cost, solution exists

Station:  0  1  2  3  4
gas:     [1, 2, 3, 4, 5]  Total: 15
cost:    [3, 4, 5, 1, 2]  Total: 15
net:    [-2,-2,-2, 3, 3]

Try starting at each station:

Start at 0:
    0→1: 1-3 = -2 (fail)

Start at 1:
    1→2: 2-4 = -2 (fail)

Start at 2:
    2→3: 3-5 = -2 (fail)

Start at 3:
    3→4: 4-1 = 3 ✓
    4→0: 3+5-2 = 6 ✓
    0→1: 6+1-3 = 4 ✓
    1→2: 4+2-4 = 2 ✓
    2→3: 2+3-5 = 0 ✓

Answer: Start at station 3

Visual:
      ┌─────────────────┐
      ↓                 │
    3 → 4 → 0 → 1 → 2 →┘
    ✓   ✓   ✓   ✓   ✓

Greedy algorithm:
    If total gas ≥ total cost:
        Start from first station where cumulative net ≥ 0

Time: O(n)
Space: O(1)
```

### 4. Partition Labels

```
Problem: Partition string so each letter appears in at most one part
s = "ababcbacadefegdehijhklij"

Greedy: Track last occurrence of each character

Last occurrence:
a: 8, b: 5, c: 7, d: 14, e: 15, f: 11,
g: 13, h: 19, i: 22, j: 23, k: 20, l: 21

Index: 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23
       a b a b c b a c a d e  f  e  g  d  e  h  i  j  h  k  l  i  j

Partition 1: Start at 0
    Current: 'a', last at 8

    Extend to include 'b' (last at 5)
    Extend to include 'c' (last at 7)
    All chars [0-8] have last occurrence ≤ 8

    Partition: "ababcbaca" (length 9)

Partition 2: Start at 9
    Current: 'd', last at 14

    Extend to include 'e' (last at 15)
    Extend to include 'f' (last at 11)
    Extend to include 'g' (last at 13)

    Partition: "defegde" (length 6)

Partition 3: Start at 16
    Current: 'h', last at 19

    Extend to include 'i' (last at 22)
    Extend to include 'j' (last at 23)

    Partition: "hijhklij" (length 8)

Result: [9, 6, 8]

Visual:
"ababcbaca | defegde | hijhklij"
 ═════════   ═══════   ════════
    9          6          8

Time: O(n)
Space: O(1) - fixed alphabet size
```

### 5. Best Time to Buy and Sell Stock

```
Multiple variations:

VARIATION 1: One transaction
prices = [7,1,5,3,6,4]

Greedy: Track minimum price seen so far

Day:    0  1  2  3  4  5
Price: [7, 1, 5, 3, 6, 4]
Min:    7  1  1  1  1  1
Profit: 0  0  4  2  5  3

Step by step:
Day 0: min=7, profit=0
Day 1: min=1, profit=0
Day 2: min=1, profit=5-1=4
Day 3: min=1, profit=3-1=2
Day 4: min=1, profit=6-1=5 ← max
Day 5: min=1, profit=4-1=3

Max profit: 5 (buy day 1, sell day 4)

Visual:
    7
    │ ╲
    │  ╲ 5   6
    │   1 ╲ ╱ ╲ 4
    │      3
    └────────────
    Buy  Sell

VARIATION 2: Unlimited transactions
prices = [7,1,5,3,6,4]

Greedy: Buy every valley, sell every peak

    7
    │ ╲
    │  ╲ 5   6
    │   1 ╲ ╱ ╲ 4
    │      3
    └────────────

Transactions:
Buy 1, sell 5: +4
Buy 3, sell 6: +3
Total: 7

Algorithm: Add every positive difference
profit = (5-1) + (6-3) = 4 + 3 = 7

VARIATION 3: At most 2 transactions
prices = [3,3,5,0,0,3,1,4]

Use DP or greedy with two passes

Time: O(n)
Space: O(1)
```

### 6. Meeting Rooms II

```
Problem: Minimum meeting rooms needed
intervals = [[0,30],[5,10],[15,20]]

Greedy: Use min heap for end times

Sort by start time:
[0,30], [5,10], [15,20]

Visual timeline:
    0    5    10   15   20   25   30
    |────────────────────────────|  Room 1
         |────|                      Room 2
              |────|                 Room 2

Step 1: Add [0,30]
    rooms = [30]
    count = 1

Step 2: Add [5,10]
    5 < 30 (conflicts with [0,30])
    Need new room
    rooms = [10, 30]
    count = 2

Step 3: Add [15,20]
    15 > 10 (room freed)
    Reuse room
    rooms = [20, 30]
    count = 2 (max)

Answer: 2 rooms

Using heap:
    heap = []

    [0,30]: push 30 → heap = [30]
    [5,10]: 5 < 30, push 10 → heap = [10, 30]
    [15,20]: 15 > 10, pop 10, push 20 → heap = [20, 30]

    max heap size = 2

Time: O(n log n)
Space: O(n)
```

### 7. Hand of Straights

```
Problem: Can rearrange hand into groups of W consecutive cards?
hand = [1,2,3,6,2,3,4,7,8], W = 3

Greedy: Always start with smallest card

Sort: [1,2,2,3,3,4,6,7,8]
Count: {1:1, 2:2, 3:2, 4:1, 6:1, 7:1, 8:1}

Group 1: Start with 1
    Take: 1, 2, 3
    Remaining: {2:1, 3:1, 4:1, 6:1, 7:1, 8:1}

    [1, 2, 3] ✓

Group 2: Start with 2
    Take: 2, 3, 4
    Remaining: {6:1, 7:1, 8:1}

    [2, 3, 4] ✓

Group 3: Start with 6
    Take: 6, 7, 8
    Remaining: {}

    [6, 7, 8] ✓

Answer: True

Visual groups:
[1, 2, 3]
[2, 3, 4]
[6, 7, 8]

Failure case:
hand = [1,2,3,4,5], W = 4
Can't form [1,2,3,4] AND have [5] left

Time: O(n log n)
Space: O(n)
```

## Greedy Patterns

### Pattern 1: Interval Problems
```
Sort by end time:
- Activity selection
- Non-overlapping intervals

Sort by start time:
- Meeting rooms
- Merge intervals
```

### Pattern 2: Two Pointers
```
Left/right pointers moving greedily:
- Container with most water
- Trapping rain water
```

### Pattern 3: Priority Queue
```
Always process min/max first:
- Meeting rooms II
- Task scheduler
- IPO
```

### Pattern 4: Sort and Scan
```
Sort then make greedy choice:
- Assign cookies
- Queue reconstruction
```

## Time and Space Complexity

```
Problem                  Time        Space
Jump Game                O(n)        O(1)
Jump Game II             O(n)        O(1)
Gas Station              O(n)        O(1)
Partition Labels         O(n)        O(1)
Stock (one transaction)  O(n)        O(1)
Stock (unlimited)        O(n)        O(1)
Meeting Rooms II         O(n log n)  O(n)
Hand of Straights        O(n log n)  O(n)
```

## Python Implementation

```python
# Jump Game
def can_jump(nums):
    """
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
    Time: O(n), Space: O(1)
    """
    if len(nums) <= 1:
        return 0

    jumps = current_end = farthest = 0

    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])

        if i == current_end:
            jumps += 1
            current_end = farthest

            if current_end >= len(nums) - 1:
                break

    return jumps


# Gas Station
def can_complete_circuit(gas, cost):
    """
    Time: O(n), Space: O(1)
    """
    if sum(gas) < sum(cost):
        return -1

    total = start = 0

    for i in range(len(gas)):
        total += gas[i] - cost[i]

        if total < 0:
            total = 0
            start = i + 1

    return start


# Partition Labels
def partition_labels(s):
    """
    Time: O(n), Space: O(1)
    """
    last = {c: i for i, c in enumerate(s)}
    result = []
    start = end = 0

    for i, c in enumerate(s):
        end = max(end, last[c])

        if i == end:
            result.append(end - start + 1)
            start = i + 1

    return result


# Best Time to Buy and Sell Stock
def max_profit(prices):
    """
    One transaction.
    Time: O(n), Space: O(1)
    """
    min_price = float('inf')
    max_profit = 0

    for price in prices:
        min_price = min(min_price, price)
        max_profit = max(max_profit, price - min_price)

    return max_profit


# Best Time to Buy and Sell Stock II
def max_profit_ii(prices):
    """
    Unlimited transactions.
    Time: O(n), Space: O(1)
    """
    profit = 0

    for i in range(1, len(prices)):
        if prices[i] > prices[i-1]:
            profit += prices[i] - prices[i-1]

    return profit


# Meeting Rooms II
import heapq

def min_meeting_rooms(intervals):
    """
    Time: O(n log n), Space: O(n)
    """
    if not intervals:
        return 0

    intervals.sort(key=lambda x: x[0])
    heap = []

    for interval in intervals:
        if heap and heap[0] <= interval[0]:
            heapq.heappop(heap)
        heapq.heappush(heap, interval[1])

    return len(heap)


# Hand of Straights
from collections import Counter

def is_n_straight_hand(hand, W):
    """
    Time: O(n log n), Space: O(n)
    """
    if len(hand) % W != 0:
        return False

    count = Counter(hand)

    for card in sorted(count):
        if count[card] > 0:
            need = count[card]

            for i in range(W):
                if count[card + i] < need:
                    return False
                count[card + i] -= need

    return True


# Non-overlapping Intervals
def erase_overlap_intervals(intervals):
    """
    Time: O(n log n), Space: O(1)
    """
    if not intervals:
        return 0

    intervals.sort(key=lambda x: x[1])
    end = intervals[0][1]
    count = 0

    for i in range(1, len(intervals)):
        if intervals[i][0] < end:
            count += 1
        else:
            end = intervals[i][1]

    return count


# Task Scheduler
def least_interval(tasks, n):
    """
    Time: O(n), Space: O(1)
    """
    count = Counter(tasks)
    max_freq = max(count.values())
    max_count = sum(1 for v in count.values() if v == max_freq)

    return max(len(tasks), (max_freq - 1) * (n + 1) + max_count)


# Container With Most Water
def max_area(height):
    """
    Time: O(n), Space: O(1)
    """
    left, right = 0, len(height) - 1
    max_water = 0

    while left < right:
        width = right - left
        max_water = max(max_water, min(height[left], height[right]) * width)

        if height[left] < height[right]:
            left += 1
        else:
            right -= 1

    return max_water


# Assign Cookies
def find_content_children(g, s):
    """
    Time: O(n log n), Space: O(1)
    """
    g.sort()
    s.sort()

    child = cookie = 0

    while child < len(g) and cookie < len(s):
        if s[cookie] >= g[child]:
            child += 1
        cookie += 1

    return child
```

## Key Takeaways

1. **When to Use Greedy**:
   - Problem has greedy-choice property
   - Local optimum leads to global optimum
   - Can prove correctness

2. **Greedy vs DP**:
   - Greedy: Makes choice, never reconsiders
   - DP: Considers all choices
   - Greedy is O(n) vs DP O(n²)

3. **Common Strategies**:
   - Sort first
   - Priority queue
   - Two pointers
   - Track min/max

4. **Verification**:
   - Always verify greedy works
   - Consider counterexamples
   - Prove or test thoroughly

5. **Patterns**:
   - Intervals: sort by end
   - Arrays: track extremes
   - Scheduling: earliest deadline
   - Grouping: frequency-based

6. **Complexity**:
   - Often O(n log n) due to sorting
   - Can be O(n) with preprocessing
   - Usually O(1) or O(n) space
