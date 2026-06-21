# Patterns Reference

The 16 core problem-solving patterns that appear across nearly every LeetCode category. Recognizing the pattern is half the battle — this file tells you what the pattern looks like, when to use it, and exactly how to code it. Every pattern links back to the data structures and algorithms it relies on.

---

## Table of Contents

| # | Pattern | Jump To |
|---|---------|---------|
| 1 | Two Pointers | [→ Two Pointers](#two-pointers) |
| 2 | Sliding Window | [→ Sliding Window](#sliding-window) |
| 3 | Fast and Slow Pointers | [→ Fast and Slow Pointers](#fast-and-slow-pointers) |
| 4 | Merge Intervals | [→ Merge Intervals](#merge-intervals) |
| 5 | Binary Search on Answer | [→ Binary Search on Answer](#binary-search-on-answer) |
| 6 | Prefix Sum | [→ Prefix Sum](#prefix-sum) |
| 7 | Monotonic Stack | [→ Monotonic Stack](#monotonic-stack) |
| 8 | BFS on Grid and Tree | [→ BFS on Grid and Tree](#bfs-on-grid-and-tree) |
| 9 | DFS and Backtracking | [→ DFS and Backtracking](#dfs-and-backtracking) |
| 10 | Top K Elements | [→ Top K Elements](#top-k-elements) |
| 11 | Two Heaps | [→ Two Heaps](#two-heaps) |
| 12 | Union Find | [→ Union Find](#union-find) |
| 13 | Topological Sort | [→ Topological Sort](#topological-sort) |
| 14 | Trie Search | [→ Trie Search](#trie-search) |
| 15 | Dynamic Programming | [→ Dynamic Programming](#dynamic-programming) |
| 16 | Bit Manipulation and XOR | [→ Bit Manipulation and XOR](#bit-manipulation-and-xor) |

**Other files:** [datastructures.md](../ds&a/datastructures.md) · [algorithms.md](../ds&a/algorithms.md) · [templates/](templates/) · [lists/](../../lists/)

---

## Two Pointers

```
  Sorted array — find pair that sums to target:
  arr = [1, 2, 3, 4, 6],  target = 6

  lo=0  hi=4
  ┌───┬───┬───┬───┬───┐
  │ 1 │ 2 │ 3 │ 4 │ 6 │
  └───┴───┴───┴───┴───┘
   ↑                 ↑
   lo               hi

  sum=1+6=7 > 6 → hi--
  sum=1+4=5 < 6 → lo++
  sum=2+4=6 == 6 ✓  → found!

  Variation — same direction (remove duplicates):
  arr = [1, 1, 2, 3, 3, 4]
  slow=0  fast=1
  ┌───┬───┬───┬───┬───┬───┐
  │ 1 │ 1 │ 2 │ 3 │ 3 │ 4 │
  └───┴───┴───┴───┴───┴───┘
   ↑   ↑
  slow fast
  arr[fast] == arr[slow]? yes → fast++ only
  arr[fast] != arr[slow]? → slow++, copy fast to slow
```

**What it is:** Two index variables (usually `left` and `right`, or `slow` and `fast`) that traverse the array, either toward each other or in the same direction, to avoid the O(n²) brute-force nested loop.

**Use this when:**
- [ ] Array or string is sorted (or can be sorted)
- [ ] You are searching for pairs or triplets with a sum constraint
- [ ] Removing duplicates in-place
- [ ] Palindrome checking
- [ ] Container with most water / trapping rain water

**Step-by-step template:**
1. Sort if needed
2. Place `left = 0`, `right = len - 1`
3. While `left < right`: evaluate the pair, move the pointer that brings you closer to the goal

**Python:**
```python
# Opposite-direction: pair sum in sorted array
def two_sum_sorted(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        s = nums[lo] + nums[hi]
        if s == target:
            return [lo, hi]
        elif s < target:
            lo += 1
        else:
            hi -= 1
    return []

# Same-direction: remove duplicates in-place
def remove_duplicates(nums):
    slow = 0
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
    return slow + 1

# 3Sum (extend two pointers)
def three_sum(nums):
    nums.sort()
    result = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i-1]:
            continue      # skip duplicates for i
        lo, hi = i+1, len(nums)-1
        while lo < hi:
            s = nums[i] + nums[lo] + nums[hi]
            if s == 0:
                result.append([nums[i], nums[lo], nums[hi]])
                while lo < hi and nums[lo] == nums[lo+1]: lo += 1
                while lo < hi and nums[hi] == nums[hi-1]: hi -= 1
                lo += 1; hi -= 1
            elif s < 0: lo += 1
            else: hi -= 1
    return result
```

**Complexity:** O(n) time after sorting, O(n log n) total (sort dominates). O(1) extra space.

**Blind 75 examples:** Valid Palindrome · 3Sum · Container With Most Water

**Data structures used:**
[Array](../ds&a/datastructures.md#array) · [Linked List](../ds&a/datastructures.md#linked-list) · [String](../ds&a/datastructures.md#string)

**Algorithms used:**
[Merge Sort](../ds&a/algorithms.md#merge-sort) (often sort first) · [Binary Search](../ds&a/algorithms.md#binary-search) (combined in advanced variants)

---

## Sliding Window

```
  Find longest substring without repeating chars: "abcabcbb"

  Fixed window of size 3? → use fixed template
  Variable window:

  "a b c a b c b b"
   0 1 2 3 4 5 6 7

  left=0, right=0, window={}
  Add 'a': {a:1}         window="a"    len=1
  Add 'b': {a:1,b:1}     window="ab"   len=2
  Add 'c': {a:1,b:1,c:1} window="abc"  len=3
  Add 'a': a already in window!
    → shrink: remove arr[left]='a', left=1
    → now window="bc", add 'a': {b:1,c:1,a:1}  len=3
  Add 'b': b in window!
    → shrink: remove 'b', left=2
    → window="ca", add 'b': {c:1,a:1,b:1}  len=3
  ...
  Max = 3 ("abc")

  Fixed window (size k):
  [1,3,-1,-3,5,3,6,7]  k=3
  ┌───────┐
  │1  3 -1│-3  5  3  6  7   → max = 3
     ┌───────┐
      1│ 3 -1 -3│ 5  3  6  7  → max = 3
```

**What it is:** Maintain a "window" (contiguous subarray or substring) that expands or contracts to satisfy a condition. Avoids O(n²) by never re-scanning elements — each element enters and exits the window at most once.

**Two flavors:**
- **Fixed size k**: window is always exactly k elements; slide by one each step
- **Variable size**: expand right pointer, shrink left when constraint violated

**Use this when:**
- [ ] "Longest/shortest subarray/substring with constraint X"
- [ ] "Maximum sum subarray of size k"
- [ ] "Minimum window containing all characters"
- [ ] Contiguous elements, no gaps
- [ ] Constraint is about the window contents (sum, count, unique chars)

**Python:**
```python
# Fixed-size window: max sum subarray of length k
def max_sum_k(nums, k):
    window_sum = sum(nums[:k])
    best = window_sum
    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i - k]   # slide: add right, remove left
        best = max(best, window_sum)
    return best

# Variable-size window: longest substring with at most k distinct chars
def longest_k_distinct(s, k):
    freq = {}
    left = best = 0
    for right, ch in enumerate(s):
        freq[ch] = freq.get(ch, 0) + 1
        while len(freq) > k:              # violated → shrink
            left_ch = s[left]
            freq[left_ch] -= 1
            if freq[left_ch] == 0:
                del freq[left_ch]
            left += 1
        best = max(best, right - left + 1)
    return best

# Minimum window substring (hard variant)
from collections import Counter
def min_window(s, t):
    need = Counter(t)
    missing = len(t)
    left = best_left = best_right = 0
    for right, ch in enumerate(s, 1):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1
        if missing == 0:                  # valid window found
            while need[s[left]] < 0:     # shrink from left
                need[s[left]] += 1
                left += 1
            if not best_right or right - left < best_right - best_left:
                best_left, best_right = left, right
            need[s[left]] += 1
            missing += 1
            left += 1
    return s[best_left:best_right]
```

**Complexity:** O(n) — each element is added and removed from the window at most once.

**Blind 75 examples:** Best Time to Buy and Sell Stock · Longest Substring Without Repeating Characters · Minimum Window Substring · Longest Repeating Character Replacement

**Data structures used:**
[Array](../ds&a/datastructures.md#array) · [String](../ds&a/datastructures.md#string) · [Hash Map and Hash Set](../ds&a/datastructures.md#hash-map-and-hash-set) · [Queue and Deque](../ds&a/datastructures.md#queue-and-deque) (for sliding window max)

**Algorithms used:**
[Depth-First Search](../ds&a/algorithms.md#depth-first-search) (not here) · [Bit Manipulation](../ds&a/algorithms.md#bit-manipulation) (some variants)

---

## Fast and Slow Pointers

```
  Linked list cycle detection (Floyd's algorithm):

  List: 1 → 2 → 3 → 4 → 5 → 3 (cycle back to node 3)
                        ↑_______↑

  slow moves 1 step, fast moves 2 steps:
  Start: slow=1, fast=1
  Step1: slow=2, fast=3
  Step2: slow=3, fast=5
  Step3: slow=4, fast=4   ← MEET! cycle detected

  Find middle of linked list:
  List: 1 → 2 → 3 → 4 → 5 → None

  slow=1, fast=1
  Step1: slow=2, fast=3
  Step2: slow=3, fast=5
  fast.next = None → STOP → slow=3 is the MIDDLE

  For even length: 1 → 2 → 3 → 4 → None
  Step1: slow=2, fast=3
  Step2: slow=3, fast=None → STOP → slow=3 (second middle)
```

**What it is:** Two pointers moving at different speeds through a linked list (or array). The key insight: if there is a cycle, the fast pointer must eventually lap the slow pointer and they will meet.

**Use this when:**
- [ ] Detect a cycle in a linked list
- [ ] Find the start of a cycle
- [ ] Find the middle node of a linked list
- [ ] Check if a linked list is a palindrome (find middle, reverse second half)
- [ ] Happy number (detect cycle in sequence of digit-square-sums)

**Python:**
```python
# Cycle detection
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False

# Find start of cycle (after detecting meeting point)
def cycle_start(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            break
    else:
        return None   # no cycle
    # reset slow to head; both move 1 step at a time
    slow = head
    while slow is not fast:
        slow = slow.next
        fast = fast.next
    return slow   # start of cycle

# Find middle node
def find_middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow   # middle (or second middle for even length)

# Happy number (cycle detection on numbers)
def is_happy(n):
    def digit_square_sum(n):
        return sum(int(d)**2 for d in str(n))
    slow = fast = n
    while True:
        slow = digit_square_sum(slow)
        fast = digit_square_sum(digit_square_sum(fast))
        if slow == fast:
            return slow == 1
```

**Complexity:** O(n) time, O(1) space (no extra data structures).

**Blind 75 examples:** Linked List Cycle · (Reorder List uses find middle)

**Data structures used:**
[Linked List](../ds&a/datastructures.md#linked-list)

**Algorithms used:**
[Depth-First Search](../ds&a/algorithms.md#depth-first-search) (conceptually similar exploration)

---

## Merge Intervals

```
  Input: [[1,3],[2,6],[8,10],[15,18]]
  Sort by start time:

  Timeline:
  [1──────3]
       [2──────6]
                    [8───10]
                                  [15────18]

  Merge overlapping:
  current=[1,3], next=[2,6]: 2 ≤ 3 → overlap → merge to [1,6]
  current=[1,6], next=[8,10]: 8 > 6 → no overlap → save [1,6]
  current=[8,10], next=[15,18]: 15 > 10 → no overlap → save [8,10]
  Final: [[1,6],[8,10],[15,18]]

  Insert interval:
  existing=[[1,3],[6,9]], new=[2,5]
  → merge [1,3] and [2,5] → [1,5]
  → merge [1,5] and [6,9]? 6 > 5 → no
  Result: [[1,5],[6,9]]
```

**What it is:** Sort intervals by start time, then scan linearly, merging any interval that overlaps with the last merged interval.

**Use this when:**
- [ ] Merge overlapping intervals
- [ ] Insert a new interval into a sorted list
- [ ] Find minimum number of meeting rooms needed
- [ ] Find gaps between intervals
- [ ] Employee free time

**Python:**
```python
# Merge intervals
def merge(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = []
    for start, end in intervals:
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged

# Insert interval
def insert(intervals, new_interval):
    result = []
    i = 0
    n = len(intervals)
    # Add all intervals that end before new_interval starts
    while i < n and intervals[i][1] < new_interval[0]:
        result.append(intervals[i]); i += 1
    # Merge all overlapping intervals
    while i < n and intervals[i][0] <= new_interval[1]:
        new_interval[0] = min(new_interval[0], intervals[i][0])
        new_interval[1] = max(new_interval[1], intervals[i][1])
        i += 1
    result.append(new_interval)
    # Add remaining
    result.extend(intervals[i:])
    return result

# Meeting rooms II — minimum rooms needed
import heapq
def min_meeting_rooms(intervals):
    intervals.sort(key=lambda x: x[0])
    heap = []   # min-heap of end times
    for start, end in intervals:
        if heap and heap[0] <= start:
            heapq.heapreplace(heap, end)   # reuse a room
        else:
            heapq.heappush(heap, end)      # new room needed
    return len(heap)
```

**Complexity:** O(n log n) for sort, O(n) for merge scan.

**Blind 75 examples:** Merge Intervals · Insert Interval · Non-overlapping Intervals · Meeting Rooms · Meeting Rooms II

**Data structures used:**
[Array](../ds&a/datastructures.md#array) · [Heap and Priority Queue](../ds&a/datastructures.md#heap-and-priority-queue) (meeting rooms II)

**Algorithms used:**
[Merge Sort](../ds&a/algorithms.md#merge-sort) (sort step) · [Greedy](../ds&a/algorithms.md#greedy) (greedy merge)

---

## Binary Search on Answer

```
  Problem: "Minimum capacity to ship packages in D days"
  weights = [1,2,3,4,5,6,7,8,9,10], D = 5

  Instead of searching an array — search the ANSWER SPACE:
  min capacity = max(weights) = 10   (must carry heaviest)
  max capacity = sum(weights) = 55   (carry all in 1 day)

  Binary search on capacity:
  lo=10, hi=55, mid=32
  Can we ship in ≤ 5 days with capacity 32? YES → hi=32
  lo=10, hi=32, mid=21
  Can we ship in ≤ 5 days with capacity 21? YES → hi=21
  lo=10, hi=21, mid=15
  Can we ship in ≤ 5 days with capacity 15? YES → hi=15
  lo=10, hi=15, mid=12
  Can we ship in ≤ 5 days with capacity 12? NO  → lo=13
  lo=13, hi=15, mid=14
  Can we ship in ≤ 5 days with capacity 14? YES → hi=14
  lo=13, hi=14, mid=13
  Can we ship in ≤ 5 days with capacity 13? NO  → lo=14
  lo=14 == hi=14 → answer: 15

  Key: the feasibility check must be monotone:
  if capacity X works → any X' > X also works (monotone!)
  → binary search is valid!
```

**What it is:** When you cannot binary search the input directly but the answer lies in a range, binary search the answer range. Write a feasibility function `can_do(mid)` and find the boundary where it flips from False to True (or True to False).

**Use this when:**
- [ ] "Minimum/maximum value such that condition holds"
- [ ] "Can we achieve X within K operations?"
- [ ] Answer is a number in a computable range
- [ ] Feasibility function is monotone (if X works, all larger/smaller also work)

**Step-by-step:**
1. Define `lo` = minimum possible answer, `hi` = maximum possible answer
2. Write `feasible(mid)` → True/False
3. Binary search: move `lo` or `hi` based on `feasible(mid)`
4. The loop exits when `lo == hi` = the answer

**Python:**
```python
# Template: find minimum X where feasible(X) is True
def solve():
    lo, hi = MIN_ANSWER, MAX_ANSWER
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid       # mid might be the answer, don't exclude it
        else:
            lo = mid + 1   # mid definitely not the answer
    return lo              # lo == hi == answer

# Ship packages in D days
def ship_capacity(weights, days):
    def feasible(cap):
        days_needed, cur = 1, 0
        for w in weights:
            if cur + w > cap:
                days_needed += 1
                cur = 0
            cur += w
        return days_needed <= days

    lo, hi = max(weights), sum(weights)
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo

# Koko eating bananas
def min_eating_speed(piles, h):
    def feasible(speed):
        return sum(-(-p // speed) for p in piles) <= h   # ceiling division
    lo, hi = 1, max(piles)
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid): hi = mid
        else: lo = mid + 1
    return lo
```

**Complexity:** O(n log(range)) where range = hi - lo.

**Blind 75 examples:** Find Minimum in Rotated Sorted Array · Search in Rotated Sorted Array

**Data structures used:**
[Array](../ds&a/datastructures.md#array)

**Algorithms used:**
[Binary Search](../ds&a/algorithms.md#binary-search)

---

## Prefix Sum

```
  Array: [1, 2, 3, 4, 5]
  Prefix: [0, 1, 3, 6, 10, 15]
           ↑  ↑  ↑  ↑   ↑   ↑
           0  1  2  3   4   5  ← index in prefix array

  Range sum query [l, r] (0-indexed, inclusive):
  sum(2..4) = prefix[5] - prefix[2] = 15 - 3 = 12 ✓
  (3 + 4 + 5 = 12)

  General formula:
  prefix[i] = arr[0] + arr[1] + ... + arr[i-1]
  sum(l, r) = prefix[r+1] - prefix[l]    ← O(1)!

  Subarray sum equals k (use HashMap):
  arr = [1, 2, 3], k = 3
  prefix sums seen: {0: 1}
  i=0: prefix=1,  need=1-3=-2,  count += seen[-2] = 0
  i=1: prefix=3,  need=3-3=0,   count += seen[0] = 1   ← [1,2]
  i=2: prefix=6,  need=6-3=3,   count += seen[3] = 1   ← [3]
  Total = 2
```

**What it is:** Precompute cumulative sums so that any range sum query answers in O(1) instead of O(n). When combined with a hash map, it finds subarrays with a target sum in O(n).

**Use this when:**
- [ ] "Sum of subarray from index l to r" (multiple queries)
- [ ] "Number of subarrays with sum equal to k"
- [ ] "Product of array except self" (prefix + suffix products)
- [ ] 2D matrix range queries (2D prefix sum)
- [ ] Balance point / pivot index problems

**Python:**
```python
# Build prefix sum
def build_prefix(arr):
    prefix = [0] * (len(arr) + 1)
    for i, val in enumerate(arr):
        prefix[i+1] = prefix[i] + val
    return prefix

# Range sum query — O(1)
def range_sum(prefix, l, r):
    return prefix[r+1] - prefix[l]

# Subarray sum equals k — O(n)
from collections import defaultdict
def subarray_sum(nums, k):
    count = 0
    prefix = 0
    seen = defaultdict(int)
    seen[0] = 1
    for num in nums:
        prefix += num
        count += seen[prefix - k]   # how many times (prefix - k) appeared before
        seen[prefix] += 1
    return count

# Product of array except self (prefix × suffix)
def product_except_self(nums):
    n = len(nums)
    result = [1] * n
    prefix = 1
    for i in range(n):
        result[i] = prefix
        prefix *= nums[i]
    suffix = 1
    for i in range(n-1, -1, -1):
        result[i] *= suffix
        suffix *= nums[i]
    return result
```

**Complexity:** O(n) build, O(1) query. Subarray sum k: O(n) time, O(n) space.

**Blind 75 examples:** Product of Array Except Self · (Subarray Sum Equals K is a common extension)

**Data structures used:**
[Array](../ds&a/datastructures.md#array) · [Hash Map and Hash Set](../ds&a/datastructures.md#hash-map-and-hash-set)

**Algorithms used:**
[Dynamic Programming](../ds&a/algorithms.md#dynamic-programming) (conceptually related — precompute and reuse)

---

## Monotonic Stack

```
  Daily Temperatures — find days until warmer:
  temps = [73, 74, 75, 71, 69, 72, 76, 73]

  Maintain a DECREASING stack of indices:

  i=0 (73):  stack=[]         → push 0      stack=[0]
  i=1 (74):  74>73 → pop 0,  result[0]=1-0=1  → push 1  stack=[1]
  i=2 (75):  75>74 → pop 1,  result[1]=2-1=1  → push 2  stack=[2]
  i=3 (71):  71<75 → push 3                   stack=[2,3]
  i=4 (69):  69<71 → push 4                   stack=[2,3,4]
  i=5 (72):  72>69 → pop 4,  result[4]=5-4=1
             72>71 → pop 3,  result[3]=5-3=2
             72<75 → push 5                   stack=[2,5]
  i=6 (76):  76>72 → pop 5,  result[5]=6-5=1
             76>75 → pop 2,  result[2]=6-2=4
             push 6                           stack=[6]
  i=7 (73):  73<76 → push 7                   stack=[6,7]
  End: remaining stack → result[6]=result[7]=0

  Result: [1, 1, 4, 2, 1, 1, 0, 0]
```

**What it is:** A stack that is kept in monotonically increasing or decreasing order. When a new element breaks the order, we pop elements and record the answer for each popped element (the new element is the "answer" for those elements).

**Use this when:**
- [ ] "Next Greater Element" / "Next Smaller Element"
- [ ] "Previous Greater/Smaller Element"
- [ ] Largest Rectangle in Histogram
- [ ] Trapping Rain Water
- [ ] Daily Temperatures
- [ ] Maximum width ramp / Stock span problem

**Decreasing vs Increasing:**
- **Decreasing stack** → finds next GREATER element (new larger element pops)
- **Increasing stack** → finds next SMALLER element (new smaller element pops)

**Python:**
```python
# Next Greater Element — decreasing stack
def next_greater(nums):
    result = [-1] * len(nums)
    stack = []   # stores indices
    for i, val in enumerate(nums):
        while stack and val > nums[stack[-1]]:
            result[stack.pop()] = val
        stack.append(i)
    return result

# Daily Temperatures
def daily_temperatures(temps):
    result = [0] * len(temps)
    stack = []
    for i, t in enumerate(temps):
        while stack and t > temps[stack[-1]]:
            j = stack.pop()
            result[j] = i - j
        stack.append(i)
    return result

# Largest Rectangle in Histogram
def largest_rectangle(heights):
    stack = []   # increasing stack of indices
    max_area = 0
    heights.append(0)   # sentinel to flush stack
    for i, h in enumerate(heights):
        while stack and h < heights[stack[-1]]:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)
    return max_area

# Trapping Rain Water
def trap(height):
    stack = []
    water = 0
    for i, h in enumerate(height):
        while stack and h > height[stack[-1]]:
            bottom = stack.pop()
            if not stack: break
            width = i - stack[-1] - 1
            bounded_height = min(h, height[stack[-1]]) - height[bottom]
            water += width * bounded_height
        stack.append(i)
    return water
```

**Complexity:** O(n) — each element is pushed and popped at most once.

**Blind 75 examples:** (Directly used in Largest Rectangle in Histogram, Daily Temperatures)

**Data structures used:**
[Stack](../ds&a/datastructures.md#stack) · [Array](../ds&a/datastructures.md#array) · [Monotonic Stack](../ds&a/datastructures.md#monotonic-stack)

**Algorithms used:**
[Depth-First Search](../ds&a/algorithms.md#depth-first-search) (conceptual similarity — explore and backtrack)

---

## BFS on Grid and Tree

```
  Shortest path in grid (0=open, 1=wall):
  ┌───┬───┬───┬───┐
  │ S │ 0 │ 1 │ 0 │   S = start (0,0)
  ├───┼───┼───┼───┤   E = end   (3,3)
  │ 0 │ 0 │ 1 │ 0 │
  ├───┼───┼───┼───┤
  │ 1 │ 0 │ 0 │ 0 │
  ├───┼───┼───┼───┤
  │ 0 │ 0 │ 0 │ E │
  └───┴───┴───┴───┘

  BFS expands level by level (each level = 1 more step):
  Level 0: {(0,0)}
  Level 1: {(0,1),(1,0)}
  Level 2: {(1,1),(2,1)}    ← (0,2) blocked by wall
  Level 3: {(2,2),(3,1)}
  Level 4: {(2,3),(3,2)}
  Level 5: {(3,3)} ✓  shortest path = 5 steps

  Tree level-order (BFS):
       1
      / \
     2   3       Level 0: [1]
    / \   \      Level 1: [2, 3]
   4   5   6     Level 2: [4, 5, 6]
```

**What it is:** BFS guarantees the shortest path in unweighted graphs and grids, and processes tree nodes level by level. Use when you need the minimum distance/steps or want to process nodes by distance from the source.

**Use this when:**
- [ ] Shortest path in an unweighted grid or graph
- [ ] "Minimum steps/moves to reach X"
- [ ] Level-order traversal of a binary tree
- [ ] Multi-source BFS (start from all sources at once)
- [ ] "Rotting oranges" style — spread from multiple origins
- [ ] 0-1 BFS (use deque: 0-weight edges go to front, 1-weight go to back)

**Python:**
```python
from collections import deque

# Grid BFS — shortest path
def shortest_path(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    q = deque([(start[0], start[1], 0)])
    visited = {start}
    dirs = [(0,1),(0,-1),(1,0),(-1,0)]

    while q:
        r, c, steps = q.popleft()
        if (r, c) == end:
            return steps
        for dr, dc in dirs:
            nr, nc = r+dr, c+dc
            if 0<=nr<rows and 0<=nc<cols and (nr,nc) not in visited and grid[nr][nc]==0:
                visited.add((nr, nc))
                q.append((nr, nc, steps+1))
    return -1

# Multi-source BFS (rotting oranges)
def oranges_rotting(grid):
    rows, cols = len(grid), len(grid[0])
    q = deque()
    fresh = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2: q.append((r, c, 0))
            elif grid[r][c] == 1: fresh += 1
    minutes = 0
    while q:
        r, c, t = q.popleft()
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nr, nc = r+dr, c+dc
            if 0<=nr<rows and 0<=nc<cols and grid[nr][nc]==1:
                grid[nr][nc] = 2
                fresh -= 1
                minutes = t + 1
                q.append((nr, nc, t+1))
    return minutes if fresh == 0 else -1

# Tree level-order
def level_order(root):
    if not root: return []
    q, result = deque([root]), []
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left: q.append(node.left)
            if node.right: q.append(node.right)
        result.append(level)
    return result
```

**Complexity:** O(V + E) for graphs, O(r·c) for grids, O(n) for trees.

**Blind 75 examples:** Binary Tree Level Order Traversal · Number of Islands (BFS variant) · Course Schedule (BFS topo sort)

**Data structures used:**
[Queue and Deque](../ds&a/datastructures.md#queue-and-deque) · [Graph](../ds&a/datastructures.md#graph) · [Binary Tree](../ds&a/datastructures.md#binary-tree)

**Algorithms used:**
[Breadth-First Search](../ds&a/algorithms.md#breadth-first-search) · [Topological Sort](../ds&a/algorithms.md#topological-sort) (Kahn's is BFS)

---

## DFS and Backtracking

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

**Data structures used:**
[Stack](../ds&a/datastructures.md#stack) · [Graph](../ds&a/datastructures.md#graph) · [Array](../ds&a/datastructures.md#array) · [Hash Map and Hash Set](../ds&a/datastructures.md#hash-map-and-hash-set)

**Algorithms used:**
[Depth-First Search](../ds&a/algorithms.md#depth-first-search) · [Backtracking](../ds&a/algorithms.md#backtracking)

---

## Top K Elements

```
  Find 3 largest in [3,1,4,1,5,9,2,6,5]:

  Approach 1: Min-heap of size k=3
  Process each element, maintain heap of 3 largest:
  heap=[]
  3 → heap=[3]
  1 → heap=[1,3]
  4 → heap=[1,3,4]  size=k
  1 → 1 ≤ heap[0]=1, skip
  5 → 5 > heap[0]=1, pop 1, push 5 → heap=[3,4,5]
  9 → 9 > heap[0]=3, pop 3, push 9 → heap=[4,5,9]
  2 → 2 ≤ heap[0]=4, skip
  6 → 6 > heap[0]=4, pop 4, push 6 → heap=[5,6,9]
  5 → 5 = heap[0]=5, pop 5, push 5 → heap=[5,6,9]
  Result: [5, 6, 9] ← top 3

  Approach 2: QuickSelect (find kth largest, then return k elements)
  Approach 3: Sort + slice (O(n log n) — only good when already sorting)
```

**What it is:** Maintain a min-heap of size k. Iterate through all elements — if the current element is larger than the heap's minimum, replace it. After processing all elements, the heap contains the top k largest.

**Use this when:**
- [ ] Kth largest element in array/stream
- [ ] Top K frequent elements
- [ ] K closest points to origin
- [ ] K pairs with smallest sums
- [ ] Streaming data where you can't sort the whole input

**Why min-heap for top-k LARGEST?** The heap's root is the smallest of your k candidates — any new element larger than it can replace it.

**Python:**
```python
import heapq
from collections import Counter

# Kth largest element
def kth_largest(nums, k):
    heap = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]   # smallest of the top-k = kth largest

# Or simply:
def kth_largest_v2(nums, k):
    return heapq.nlargest(k, nums)[-1]

# Top K frequent elements
def top_k_frequent(nums, k):
    freq = Counter(nums)
    # min-heap of (count, element), keep top k
    return heapq.nlargest(k, freq.keys(), key=freq.get)

# K closest points to origin
def k_closest(points, k):
    # max-heap: negate distance to simulate max-heap with heapq (min-heap)
    heap = []
    for x, y in points:
        dist = x*x + y*y
        heapq.heappush(heap, (-dist, x, y))
        if len(heap) > k:
            heapq.heappop(heap)
    return [[x, y] for _, x, y in heap]

# Streaming — process one at a time
class KthLargestStream:
    def __init__(self, k, nums):
        self.k = k
        self.heap = []
        for n in nums:
            self.add(n)

    def add(self, val):
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)
        return self.heap[0]
```

**Complexity:** O(n log k) — better than O(n log n) sort when k << n.

**Blind 75 examples:** Top K Frequent Elements · (Kth Largest in Stream is a classic extension)

**Data structures used:**
[Heap and Priority Queue](../ds&a/datastructures.md#heap-and-priority-queue) · [Hash Map and Hash Set](../ds&a/datastructures.md#hash-map-and-hash-set)

**Algorithms used:**
[Quick Sort](../ds&a/algorithms.md#quick-sort) (QuickSelect alternative) · [Greedy](../ds&a/algorithms.md#greedy)

---

## Two Heaps

```
  Find Median from Data Stream:

  Idea: split numbers into two halves.
  Left half (max-heap): stores smaller half  → root = lower median
  Right half (min-heap): stores larger half  → root = upper median

  Insert 1, 2, 3, 4, 5 one by one:

  After 1:  max_heap=[-1]    min_heap=[]      median=1
  After 2:  max_heap=[-1]    min_heap=[2]     median=(1+2)/2=1.5
  After 3:  max_heap=[-2,-1] min_heap=[3]     median=2
                              ↑ rebalanced
  After 4:  max_heap=[-2,-1] min_heap=[3,4]   median=(2+3)/2=2.5
  After 5:  max_heap=[-3,-2,-1] min_heap=[4,5] median=3
                              ↑ rebalanced

  Invariant:
  • Both heaps differ in size by at most 1
  • All elements in max_heap ≤ all elements in min_heap
  • If equal size: median = (max_heap[0] + min_heap[0]) / 2
  • If max_heap has one more: median = -max_heap[0]
```

**What it is:** Use a max-heap to represent the lower half of numbers and a min-heap for the upper half. This lets you find the median in O(1) and insert in O(log n).

**Use this when:**
- [ ] Streaming median (Find Median from Data Stream)
- [ ] Sliding window median
- [ ] "Balance" problems where you need the middle value of a dynamic dataset

**Python:**
```python
import heapq

class MedianFinder:
    def __init__(self):
        self.lo = []   # max-heap (negate values) — lower half
        self.hi = []   # min-heap                 — upper half

    def add_num(self, num):
        # Always push to lo first
        heapq.heappush(self.lo, -num)

        # Maintain order: lo's max ≤ hi's min
        if self.lo and self.hi and (-self.lo[0]) > self.hi[0]:
            heapq.heappush(self.hi, -heapq.heappop(self.lo))

        # Rebalance sizes: lo can have at most 1 more than hi
        if len(self.lo) > len(self.hi) + 1:
            heapq.heappush(self.hi, -heapq.heappop(self.lo))
        if len(self.hi) > len(self.lo):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def find_median(self):
        if len(self.lo) > len(self.hi):
            return -self.lo[0]
        return (-self.lo[0] + self.hi[0]) / 2.0
```

**Complexity:** O(log n) insert, O(1) median.

**Blind 75 examples:** Find Median from Data Stream

**Data structures used:**
[Heap and Priority Queue](../ds&a/datastructures.md#heap-and-priority-queue) (two of them)

**Algorithms used:**
[Greedy](../ds&a/algorithms.md#greedy) (balancing decision) · [Merge Sort](../ds&a/algorithms.md#merge-sort) (conceptual — dividing into two sorted halves)

---

## Union Find

```
  6 nodes, edges: (0,1),(1,2),(3,4),(4,5)

  Initial:  parent=[0,1,2,3,4,5]
  union(0,1): root(0)=0, root(1)=1 → parent[1]=0
              parent=[0,0,2,3,4,5]
  union(1,2): root(1)=0, root(2)=2 → parent[2]=0
              parent=[0,0,0,3,4,5]
  union(3,4): parent[4]=3
              parent=[0,0,0,3,3,5]
  union(4,5): root(4)=3, root(5)=5 → parent[5]=3
              parent=[0,0,0,3,3,3]

  Components: {0,1,2} and {3,4,5}  → count=2

  Cycle detection (undirected graph):
  For each edge (u,v): if find(u)==find(v) → CYCLE!
  Otherwise: union(u,v)
```

**What it is:** Tracks connected components. Two operations: `find(x)` returns the root of x's group, `union(x,y)` merges two groups. Path compression + union by rank makes both nearly O(1).

**Use this when:**
- [ ] Count connected components (and you process edges one at a time)
- [ ] Detect cycle in an undirected graph
- [ ] Kruskal's Minimum Spanning Tree
- [ ] Dynamic connectivity queries ("are A and B connected?")
- [ ] Redundant connection / extra edge in graph

**Python:**
```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])   # path compression
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py: return False   # already connected
        if self.rank[px] < self.rank[py]: px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]: self.rank[px] += 1
        self.components -= 1
        return True

# Number of connected components
def count_components(n, edges):
    uf = UnionFind(n)
    for u, v in edges:
        uf.union(u, v)
    return uf.components

# Detect cycle in undirected graph
def has_cycle(n, edges):
    uf = UnionFind(n)
    for u, v in edges:
        if not uf.union(u, v):   # already connected → adding this edge = cycle
            return True
    return False
```

**Complexity:** Nearly O(1) per operation with path compression + union by rank.

**Blind 75 examples:** Graph Valid Tree · Number of Connected Components · (Redundant Connection)

**Data structures used:**
[Disjoint Set Union](../ds&a/datastructures.md#disjoint-set-union) · [Array](../ds&a/datastructures.md#array)

**Algorithms used:**
[Depth-First Search](../ds&a/algorithms.md#depth-first-search) (alternative for same problems) · [Breadth-First Search](../ds&a/algorithms.md#breadth-first-search) (alternative)

---

## Topological Sort

```
  Prerequisites: 0→2, 1→2, 1→3, 2→4, 3→4
  (read: must complete 0 before 2, etc.)

  Build in-degree map:
  in_degree = {0:0, 1:0, 2:2, 3:1, 4:2}

  Queue all nodes with in_degree=0: [0,1]

  Process 0: decrement neighbor 2 → in_degree[2]=1
  Process 1: decrement 2 → in_degree[2]=0 ✓ add to queue
             decrement 3 → in_degree[3]=0 ✓ add to queue
  Queue: [2,3]
  Process 2: decrement 4 → in_degree[4]=1
  Process 3: decrement 4 → in_degree[4]=0 ✓ add to queue
  Queue: [4]
  Process 4: done.
  Order: [0,1,2,3,4]

  If any node was never processed → CYCLE (impossible ordering)
```

**What it is:** Produces a valid ordering of tasks with dependencies. Uses Kahn's algorithm (BFS on in-degrees) or DFS with a post-order stack. Also detects cycles in directed graphs.

**Use this when:**
- [ ] Course prerequisites / task scheduling
- [ ] Build order with dependencies
- [ ] "Is it possible to complete all tasks?" (cycle detection in directed graph)
- [ ] Ordering of compilation units
- [ ] Alien dictionary (derive character order)

**Python:**
```python
from collections import defaultdict, deque

# Kahn's BFS — detect cycle + return order
def topo_sort(num_nodes, prerequisites):
    graph = defaultdict(list)
    in_degree = [0] * num_nodes

    for a, b in prerequisites:  # b must come before a
        graph[b].append(a)
        in_degree[a] += 1

    queue = deque(i for i in range(num_nodes) if in_degree[i] == 0)
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # If len(order) < num_nodes → cycle exists → no valid ordering
    return order if len(order) == num_nodes else []

# Course Schedule (can we finish all courses?)
def can_finish(num_courses, prerequisites):
    return len(topo_sort(num_courses, prerequisites)) == num_courses

# Course Schedule II (return one valid ordering)
def find_order(num_courses, prerequisites):
    return topo_sort(num_courses, prerequisites)
```

**Complexity:** O(V + E) time and space.

**Blind 75 examples:** Course Schedule · Course Schedule II · Alien Dictionary

**Data structures used:**
[Graph](../ds&a/datastructures.md#graph) · [Queue and Deque](../ds&a/datastructures.md#queue-and-deque) · [Hash Map and Hash Set](../ds&a/datastructures.md#hash-map-and-hash-set)

**Algorithms used:**
[Breadth-First Search](../ds&a/algorithms.md#breadth-first-search) (Kahn's) · [Depth-First Search](../ds&a/algorithms.md#depth-first-search) (DFS-based topo) · [Topological Sort](../ds&a/algorithms.md#topological-sort)

---

## Trie Search

```
  Inserted words: "apple", "app", "apply", "apt"

              root
               |
               a
               |
               p
              / \
             p   t*   ← "apt"
            / \
           *   l
           ↑   |
          "app" y*  ← "apply"
               |
               e*  ← "apple"

  Search "apply": a→p→p→l→y → is_end=True ✓
  Search "ap":    a→p → is_end=False → word not in trie
  Prefix "ap":    a→p → node exists → prefix found ✓
  Search "apl":   a→p → no child 'l' → False
```

**What it is:** Build a Trie from a set of words, then traverse it character by character for search, prefix matching, or DFS over all words. Enables O(L) search independent of how many words exist.

**Use this when:**
- [ ] Implement autocomplete / search suggestions
- [ ] Check if any word from a dictionary is a prefix of another
- [ ] Word Search II (find all words from dictionary on a board)
- [ ] Replace words with prefixes (shortest prefix match)
- [ ] Design a search system with prefix filtering

**Python:**
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_end = True

    def search(self, word):
        node = self._get_node(word)
        return node is not None and node.is_end

    def starts_with(self, prefix):
        return self._get_node(prefix) is not None

    def _get_node(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

# Word Search II — find all words from list on board
def find_words(board, words):
    trie = Trie()
    for w in words:
        trie.insert(w)

    rows, cols = len(board), len(board[0])
    result = set()

    def dfs(node, r, c, path):
        ch = board[r][c]
        if ch not in node.children:
            return
        next_node = node.children[ch]
        path.append(ch)
        if next_node.is_end:
            result.add(''.join(path))
        board[r][c] = '#'   # mark visited
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nr, nc = r+dr, c+dc
            if 0<=nr<rows and 0<=nc<cols and board[nr][nc] != '#':
                dfs(next_node, nr, nc, path)
        board[r][c] = ch    # restore
        path.pop()

    for r in range(rows):
        for c in range(cols):
            dfs(trie.root, r, c, [])
    return list(result)
```

**Complexity:** Insert/search: O(L). Word Search II: O(rows × cols × 4^L) with pruning.

**Blind 75 examples:** Implement Trie · Design Add and Search Words · Word Search II

**Data structures used:**
[Trie](../ds&a/datastructures.md#trie) · [Hash Map and Hash Set](../ds&a/datastructures.md#hash-map-and-hash-set) (children dict)

**Algorithms used:**
[Depth-First Search](../ds&a/algorithms.md#depth-first-search) (DFS through trie + grid) · [Backtracking](../ds&a/algorithms.md#backtracking)

---

## Dynamic Programming

```
  Recognize by asking:
  1. Can the problem be broken into smaller subproblems?
  2. Do subproblems repeat (overlapping)?
  3. Is there an optimal substructure?
  If YES to all three → likely DP.

  House Robber — 1D DP:
  nums = [2, 7, 9, 3, 1]
  dp[i] = max money robbing houses 0..i

  dp[0] = 2
  dp[1] = max(2, 7) = 7
  dp[2] = max(dp[1], dp[0]+9) = max(7,11) = 11
  dp[3] = max(dp[2], dp[1]+3) = max(11,10) = 11
  dp[4] = max(dp[3], dp[2]+1) = max(11,12) = 12

  Coin Change — unbounded knapsack:
  coins=[1,2,5], amount=11
  dp = [0,∞,∞,∞,∞,∞,∞,∞,∞,∞,∞,∞]
  After coin=1: dp=[0,1,2,3,4,5,6,7,8,9,10,11]
  After coin=2: dp=[0,1,1,2,2,3,3,4,4,5,5,6]
  After coin=5: dp=[0,1,1,2,2,1,2,2,3,3,2,3]
  Answer: dp[11] = 3  (5+5+1)
```

**What it is:** Store the results of overlapping subproblems so each is computed only once. Either top-down (memoize recursive calls) or bottom-up (fill a table iteratively).

**DP families — recognition guide:**

| Family | Recurrence | Examples |
|--------|-----------|---------|
| Linear 1D | `dp[i] = f(dp[i-1], dp[i-2])` | Climbing Stairs, House Robber, Fib |
| Kadane's | `dp[i] = max(dp[i-1]+a[i], a[i])` | Max Subarray |
| Knapsack (0/1) | `dp[i][w] = max(skip, take)` | 0/1 Knapsack, Partition Equal Subset |
| Unbounded | `dp[i] = min(dp[i-c]+1)` for each coin | Coin Change |
| LCS/Edit | `dp[i][j] = f(dp[i-1][j-1], ...)` | LCS, Edit Distance, Unique Paths |
| LIS | `dp[i] = max(dp[j]+1)` for j<i | Longest Increasing Subsequence |
| Palindrome | `dp[i][j] = dp[i+1][j-1] and s[i]==s[j]` | Palindromic Substrings |

**Python:**
```python
# 1D DP — Climbing Stairs
def climb_stairs(n):
    if n <= 2: return n
    a, b = 1, 2
    for _ in range(3, n+1):
        a, b = b, a + b
    return b

# House Robber
def rob(nums):
    prev2, prev1 = 0, 0
    for num in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + num)
    return prev1

# LCS — 2D DP
def lcs(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]

# LIS — O(n²)
def lis(nums):
    dp = [1] * len(nums)
    for i in range(1, len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)

# Memoization with @cache (Python 3.9+)
from functools import cache
def word_break(s, word_dict):
    word_set = set(word_dict)
    @cache
    def dp(i):
        if i == len(s): return True
        return any(s[i:j] in word_set and dp(j) for j in range(i+1, len(s)+1))
    return dp(0)
```

**Complexity:** Varies — typically O(n), O(n²), or O(n·m) time; often reducible with space optimization.

**Blind 75 examples:** Climbing Stairs · House Robber · Coin Change · LCS · Longest Increasing Subsequence · Word Break · Decode Ways · Unique Paths

**Data structures used:**
[Array](../ds&a/datastructures.md#array) · [Hash Map and Hash Set](../ds&a/datastructures.md#hash-map-and-hash-set) (memoization cache)

**Algorithms used:**
[Dynamic Programming](../ds&a/algorithms.md#dynamic-programming) · [Backtracking](../ds&a/algorithms.md#backtracking) (DP vs backtracking tradeoff)

---

## Bit Manipulation and XOR

```
  Binary number cheat sheet:
  Dec  Bin
   0 = 0000
   1 = 0001
   2 = 0010
   4 = 0100
   8 = 1000
  15 = 1111

  XOR magic:
  a ^ a = 0000  (cancels itself)
  a ^ 0 = a     (identity)
  [1,1,2,2,3] XOR all: 1^1^2^2^3 = 0^0^3 = 3   ← finds single number!

  Missing number in [0..n]:
  [0,1,3]:  XOR indices 0,1,2,3 = 0^1^2^3 = 0
            XOR nums  0,1,3     = 0^1^3 = 2
            0 ^ 2 = 2  ← missing!

  Power of 2 check:
  8  = 1000
  7  = 0111
  8 & 7 = 0000 ← power of 2!

  n & (n-1) clears the lowest set bit:
  12 = 1100
  11 = 1011
  12 & 11 = 1000  ← cleared bit 2

  Counting set bits — Kernighan's:
  n=12=1100:
  12 & 11 = 1000 (count=1)
   8 &  7 = 0000 (count=2) → 2 set bits
```

**What it is:** Direct manipulation of binary representations of integers to achieve results that would otherwise require extra space or more time.

**Use this when:**
- [ ] Find the single number (others appear twice)
- [ ] Find the missing number in [0..n]
- [ ] Check if n is a power of 2
- [ ] Count number of set bits
- [ ] Reverse bits of a 32-bit integer
- [ ] Sum of two integers without using `+`
- [ ] Enumerate all subsets (bitmask DP)

**Core tricks reference:**

| Trick | Expression | What it does |
|-------|-----------|-------------|
| Check bit k | `(n >> k) & 1` | 1 if bit k is set |
| Set bit k | `n \| (1 << k)` | Force bit k to 1 |
| Clear bit k | `n & ~(1 << k)` | Force bit k to 0 |
| Toggle bit k | `n ^ (1 << k)` | Flip bit k |
| Power of 2? | `n & (n-1) == 0` | True if exactly 1 bit set |
| Clear lowest bit | `n & (n-1)` | Remove lowest set bit |
| Get lowest bit | `n & (-n)` | Isolate lowest set bit |

**Python:**
```python
# Single number — XOR all elements
from functools import reduce
import operator
def single_number(nums):
    return reduce(operator.xor, nums)

# Missing number
def missing_number(nums):
    return len(nums) ^ reduce(operator.xor, enumerate(nums), 0)
    # or cleaner:
    n = len(nums)
    return n*(n+1)//2 - sum(nums)  # math alternative

# Count set bits (Hamming weight)
def hamming_weight(n):
    count = 0
    while n:
        n &= n - 1    # clear lowest set bit
        count += 1
    return count

# Reverse bits of 32-bit integer
def reverse_bits(n):
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result

# Sum without + (bit carry simulation)
def get_sum(a, b):
    mask = 0xFFFFFFFF
    while b & mask:
        carry = (a & b) << 1
        a = a ^ b
        b = carry
    return a if b == 0 else a & mask

# Subset enumeration with bitmask
def all_subsets(nums):
    n = len(nums)
    result = []
    for mask in range(1 << n):
        subset = [nums[i] for i in range(n) if mask & (1 << i)]
        result.append(subset)
    return result
```

**Complexity:** All individual operations are O(1). Problems over arrays are typically O(n) time, O(1) space.

**Blind 75 examples:** Number of 1 Bits · Counting Bits · Reverse Bits · Missing Number · Sum of Two Integers

**Data structures used:**
[Array](../ds&a/datastructures.md#array) (of integers)

**Algorithms used:**
[Bit Manipulation](../ds&a/algorithms.md#bit-manipulation) · [Dynamic Programming](../ds&a/algorithms.md#dynamic-programming) (Counting Bits: `dp[i] = dp[i >> 1] + (i & 1)`)

---

*Back to [Table of Contents](#table-of-contents) · See also: [datastructures.md](../ds&a/datastructures.md) · [algorithms.md](../ds&a/algorithms.md)*
