# Greedy

## How to use this README

Problems are split into three tiers: Blind 75 is the core set every interviewer expects you to know cold. NeetCode 150 adds problems that sharpen the same patterns with more constraints — scheduling, gas stations, and greedy interval problems. NeetCode 250 pushes into circular subarrays, queue simulations, and two-pass strategies. Work through tiers in order — the Core Patterns and Syntax Reference sections below map directly to the problems in each table. For each new problem, ask yourself: does making the locally optimal choice here prevent me from reaching any globally better outcome? If the answer is no, greedy works.

---

## Problems

### Blind 75
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved |
|-----------|------------|--------------|---------------|--------|
| 53 | Medium | Maximum Subarray | [Link](https://leetcode.com/problems/maximum-subarray/) | ☐ |
| 55 | Medium | Jump Game | [Link](https://leetcode.com/problems/jump-game/) | ☐ |

### NeetCode 150
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved |
|-----------|------------|--------------|---------------|--------|
| 45 | Medium | Jump Game II | [Link](https://leetcode.com/problems/jump-game-ii/) | ☐ |
| 134 | Medium | Gas Station | [Link](https://leetcode.com/problems/gas-station/) | ☐ |
| 846 | Medium | Hand of Straights | [Link](https://leetcode.com/problems/hand-of-straights/) | ☐ |
| 1899 | Medium | Merge Triplets to Form Target Triplet | [Link](https://leetcode.com/problems/merge-triplets-to-form-target-triplet/) | ☐ |
| 763 | Medium | Partition Labels | [Link](https://leetcode.com/problems/partition-labels/) | ☐ |
| 678 | Medium | Valid Parenthesis String | [Link](https://leetcode.com/problems/valid-parenthesis-string/) | ☐ |

### NeetCode 250
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved | Pattern |
|-----------|------------|--------------|---------------|--------|---------|
| 860 | Easy | Lemonade Change | [Link](https://leetcode.com/problems/lemonade-change/) | ☐ | Greedy coin change |
| 918 | Medium | Maximum Sum Circular Subarray | [Link](https://leetcode.com/problems/maximum-sum-circular-subarray/) | ☐ | Kadane variant |
| 978 | Medium | Longest Turbulent Subarray | [Link](https://leetcode.com/problems/longest-turbulent-subarray/) | ☐ | Local scan greedy |
| 1871 | Medium | Jump Game VII | [Link](https://leetcode.com/problems/jump-game-vii/) | ☐ | Sliding window greedy |
| 649 | Medium | Dota2 Senate | [Link](https://leetcode.com/problems/dota2-senate/) | ☐ | Queue simulation |
| 135 | Hard | Candy | [Link](https://leetcode.com/problems/candy/) | ☐ | Two-pass greedy |

---

## Complexity Reference

| Pattern / Operation | Time | Space | Notes |
|---------------------|------|-------|-------|
| Kadane's (max subarray) | O(n) | O(1) | Reset when current sum goes negative |
| Jump Game (furthest reach) | O(n) | O(1) | Track max reachable index |
| Jump Game II (min jumps) | O(n) | O(1) | BFS-level greedy |
| Gas Station (running total) | O(n) | O(1) | Single pass with reset |
| Partition Labels | O(n) | O(26) | Last-occurrence map + greedy |
| Hand of Straights | O(n log n) | O(n) | Sort + ordered map |
| Candy (two-pass) | O(n) | O(n) | Left pass + right pass |
| Max Sum Circular Subarray | O(n) | O(1) | Kadane + total - min subarray |
| Valid Parenthesis String | O(n) | O(1) | Track [lo, hi] range of open counts |

---

## Data Structures

### Running Accumulator

The simplest greedy structure — just one or two scalar variables tracking the current best and overall best. Most O(n) greedy algorithms reduce to maintaining a running sum/count/reach and knowing when to reset it.

```
Kadane's Algorithm — track current_sum and max_sum

nums:        [-2, 1, -3, 4, -1, 2, 1, -5, 4]
curr_sum:    [-2, 1, -2, 4,  3, 5, 6,  1, 5]
max_sum:     [-2, 1,  1, 4,  4, 5, 6,  6, 6]  ← answer = 6
                  ↑
             reset here: curr_sum < 0, start fresh from next element
```

**When it matters:** Subarray problems where you want the best contiguous window without knowing its boundaries in advance. The reset is the greedy choice: if carrying a negative prefix only hurts you, discard it.

### Ordered Map / Sorted Structure

Some greedy problems (Hand of Straights) need both fast min/max access and fast key lookup. A `SortedDict` (from `sortedcontainers`) or a `Counter` iterated in sorted order fills this role.

```
Hand of Straights — always start the next group from the smallest available card

Cards: [1, 2, 3, 6, 2, 3, 4, 7, 8]  groupSize=3
count: {1:1, 2:2, 3:2, 4:1, 6:1, 7:1, 8:1}

Step 1: smallest=1 → form [1,2,3] → remove 1 from each → {2:1,3:1,4:1,6:1,7:1,8:1}
Step 2: smallest=2 → form [2,3,4] → remove 1 from each → {6:1,7:1,8:1}
Step 3: smallest=6 → form [6,7,8] → done ✓
```

**When it matters:** When the greedy choice is always "process the smallest/largest available element" — use `heapq` or a sorted iteration of a `Counter`.

---

## Core Patterns

### Local Optimal → Global Optimal
**When to use:** At each step, the best immediate choice is also the best long-term choice. Verify this before applying greedy — DP is the fallback when local choices interact.
**Complexity:** Problem-dependent, usually O(n) or O(n log n)
**Problems:** Jump Game (#55), Gas Station (#134), Partition Labels (#763), Lemonade Change (#860)
**Common mistake:** Applying greedy to a problem without the greedy-choice property — always ask "does taking the locally best option now ever prevent a globally better outcome?"

```python
# Jump Game: greedily track the furthest reachable index
max_reach = 0
for i, jump in enumerate(nums):
    if i > max_reach:
        return False          # current index is unreachable
    max_reach = max(max_reach, i + jump)
return True
```

### Kadane's Algorithm
**When to use:** Maximum sum (or product) of a contiguous subarray.
**Complexity:** O(n) time, O(1) space
**Problems:** Maximum Subarray (#53), Maximum Sum Circular Subarray (#918)
**Common mistake:** Initializing current_sum to 0 when the entire array might be negative — initialize both to `nums[0]` and start the loop at index 1.

```python
current_sum = max_sum = nums[0]
for num in nums[1:]:
    current_sum = max(num, current_sum + num)  # restart or extend
    max_sum = max(max_sum, current_sum)
return max_sum
```

### Jump Game (Furthest Reach)
**When to use:** Determine reachability or minimum jumps in an array where each element tells you how far you can jump.
**Complexity:** O(n) time, O(1) space
**Problems:** Jump Game (#55), Jump Game II (#45), Jump Game VII (#1871)
**Common mistake:** For Jump Game II, confusing "current level end" with "next level end" — think of it as BFS levels, not individual steps.

```python
# Jump Game II — minimum jumps to reach end
jumps = current_end = farthest = 0
for i in range(len(nums) - 1):
    farthest = max(farthest, i + nums[i])
    if i == current_end:          # reached end of current BFS level
        jumps += 1
        current_end = farthest    # expand to next level
return jumps
```

### Two-Pass Sweep
**When to use:** The optimal value at position i depends on both its left neighbors and its right neighbors. A single pass can't capture both.
**Complexity:** O(n) time, O(n) space
**Problems:** Candy (#135)
**Common mistake:** Not resetting or re-examining after the second pass — the final answer combines both passes (element-wise max).

```python
n = len(ratings)
candies = [1] * n
for i in range(1, n):               # left pass: right neighbor gets more if higher
    if ratings[i] > ratings[i-1]:
        candies[i] = candies[i-1] + 1
for i in range(n - 2, -1, -1):     # right pass: left neighbor gets more if higher
    if ratings[i] > ratings[i+1]:
        candies[i] = max(candies[i], candies[i+1] + 1)
return sum(candies)
```

### Running Total with Reset
**When to use:** You need to find a valid starting point in a circular or linear array where a cumulative total never drops below zero.
**Complexity:** O(n) time, O(1) space
**Problems:** Gas Station (#134)
**Common mistake:** Thinking you need O(n²) to try every starting point — a single pass suffices because if the total sum >= 0 then a solution exists, and the valid start is always after the last deficit.

```python
total = tank = start = 0
for i, (gas, cost) in enumerate(zip(gas, cost)):
    tank += gas - cost
    total += gas - cost
    if tank < 0:           # can't reach i+1 from start
        start = i + 1      # try starting from i+1
        tank = 0
return start if total >= 0 else -1
```

---

## Syntax Reference

### Kadane's Variants

```python
# Standard max subarray
current = best = nums[0]
for n in nums[1:]:
    current = max(n, current + n)
    best = max(best, current)

# Circular max subarray (#918):
# Answer is either max normal subarray, or total - min normal subarray
max_sub = min_sub = nums[0]
cur_max = cur_min = nums[0]
total = nums[0]
for n in nums[1:]:
    cur_max = max(n, cur_max + n)
    cur_min = min(n, cur_min + n)
    max_sub = max(max_sub, cur_max)
    min_sub = min(min_sub, cur_min)
    total += n
return max(max_sub, total - min_sub) if max_sub > 0 else max_sub
```

### Partition Labels Pattern

```python
last = {c: i for i, c in enumerate(s)}   # last occurrence of each character
result = []
start = end = 0
for i, c in enumerate(s):
    end = max(end, last[c])               # extend partition to cover c's last occurrence
    if i == end:                          # reached the end of this partition
        result.append(end - start + 1)
        start = i + 1
return result
```

### Valid Parenthesis String (Track Range of Valid Open Counts)

```python
lo = hi = 0     # lo = min possible open parens, hi = max possible open parens
for c in s:
    if c == '(':
        lo += 1; hi += 1
    elif c == ')':
        lo -= 1; hi -= 1
    else:        # '*' can be '(', ')', or ''
        lo -= 1; hi += 1
    if hi < 0:   # impossible — too many ')'
        return False
    lo = max(lo, 0)   # lo can't go below 0
return lo == 0        # can we have exactly 0 open parens at the end?
```

### Sorted Counter (Hand of Straights)

```python
from collections import Counter
count = Counter(hand)
for card in sorted(count):
    if count[card] > 0:
        n = count[card]
        for i in range(groupSize):
            if count[card + i] < n:
                return False
            count[card + i] -= n
return True
```

### heapq for Greedy Scheduling

```python
import heapq
# Push smallest-first: use a min-heap directly
heap = []
heapq.heappush(heap, value)
smallest = heapq.heappop(heap)

# Max-heap trick: negate values
heapq.heappush(heap, -value)
largest = -heapq.heappop(heap)
```
