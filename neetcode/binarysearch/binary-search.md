# Binary Search

## How to use this README

Problems are split into three tiers: Blind 75 is the core set every interviewer expects you to know cold. NeetCode 150 adds problems that push binary search into 2D matrices, abstract feasibility checks, and design problems. NeetCode 250 introduces "binary search on the answer" — searching a value space rather than an index space — and bitonic/rotated variants with duplicates. Work through tiers in order — the Core Patterns and Syntax Reference sections below map directly to the problems in each table, so when you hit a new problem, determine whether you're searching an index space or an answer space, then find the matching pattern.

---

## Problems

### Blind 75
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved |
|-----------|------------|--------------|---------------|--------|
| 153 | Medium | Find Minimum in Rotated Sorted Array | [Link](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/) | ☐ |
| 33 | Medium | Search in Rotated Sorted Array | [Link](https://leetcode.com/problems/search-in-rotated-sorted-array/) | ☐ |

### NeetCode 150
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved |
|-----------|------------|--------------|---------------|--------|
| 704 | Easy | Binary Search | [Link](https://leetcode.com/problems/binary-search/) | ☑ |
| 74 | Medium | Search a 2D Matrix | [Link](https://leetcode.com/problems/search-a-2d-matrix/) | ☐ |
| 875 | Medium | Koko Eating Bananas | [Link](https://leetcode.com/problems/koko-eating-bananas/) | ☐ |
| 981 | Medium | Time Based Key-Value Store | [Link](https://leetcode.com/problems/time-based-key-value-store/) | ☐ |
| 4 | Hard | Median of Two Sorted Arrays | [Link](https://leetcode.com/problems/median-of-two-sorted-arrays/) | ☐ |

### NeetCode 250
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved | Pattern |
|-----------|------------|--------------|---------------|--------|---------|
| 35 | Easy | Search Insert Position | [Link](https://leetcode.com/problems/search-insert-position/) | ☐ | Standard lower bound |
| 374 | Easy | Guess Number Higher or Lower | [Link](https://leetcode.com/problems/guess-number-higher-or-lower/) | ☐ | Black-box binary search |
| 69 | Easy | Sqrt(x) | [Link](https://leetcode.com/problems/sqrtx/) | ☐ | Binary search on answer |
| 1011 | Medium | Capacity to Ship Packages Within D Days | [Link](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/) | ☐ | Binary search on answer |
| 81 | Medium | Search in Rotated Sorted Array II | [Link](https://leetcode.com/problems/search-in-rotated-sorted-array-ii/) | ☐ | Rotated + duplicates |
| 410 | Hard | Split Array Largest Sum | [Link](https://leetcode.com/problems/split-array-largest-sum/) | ☐ | Binary search on answer |
| 1095 | Hard | Find in Mountain Array | [Link](https://leetcode.com/problems/find-in-mountain-array/) | ☐ | Bitonic binary search |

---

## Complexity Reference

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| Classic binary search (sorted array) | O(log n) | O(1) | Halves search space each step |
| Lower / upper bound | O(log n) | O(1) | bisect_left / bisect_right |
| Binary search on answer | O(log(hi-lo) · f(n)) | O(1) | f(n) = cost of feasibility check |
| Search in rotated array | O(log n) | O(1) | One extra comparison per step |
| Search in 2D matrix (row-major) | O(log(m·n)) | O(1) | Flatten index: row=mid//n, col=mid%n |
| Median of two sorted arrays | O(log(min(m,n))) | O(1) | Partition on shorter array |
| bisect_left / bisect_right | O(log n) | O(1) | From Python stdlib |
| bisect.insort | O(n) | O(1) | O(log n) to find, O(n) to shift |

---

## Data Structures

### Sorted Array (Index Space)

Binary search works on any sorted sequence because you can make a guaranteed elimination at each step: if `arr[mid] < target`, everything at mid and to its left cannot be the target, so you discard the entire left half. Each elimination halves the remaining space, giving O(log n) total steps.

```
Target = 7, Array = [1, 3, 5, 7, 9, 11, 13]

Step 1: left=0, right=6, mid=3  → arr[3]=7 == target → found

Step 1 (miss): left=0, right=6, mid=3 → arr[3]=5 < 7 → left=4
Step 2:        left=4, right=6, mid=5 → arr[5]=11 > 7 → right=4
Step 3:        left=4, right=4, mid=4 → arr[4]=9 > 7 → right=3
               left > right → not found
```

**When it matters:** Any lookup in a sorted structure. Also applies to implicit sorted spaces — monotone functions where you're searching for the threshold, not an array element.

### Answer Space (Value Space)

For "binary search on the answer" problems, there is no explicit array of candidates. Instead, you define a range `[lo, hi]` of possible answers and a boolean function `feasible(mid)` that is monotone: if mid is feasible, so is everything on one side. Binary search the value space the same way you would an index space.

```
"What is the minimum capacity to ship in D days?"

Possible capacities: [max(weights)  ...  sum(weights)]
                         ↑                    ↑
                      lo (must fit          hi (ship all
                       at least one)         in one day)

feasible(mid) = can we ship everything in ≤ D days at capacity mid?
→ If True,  try smaller: right = mid
→ If False, need more:   left = mid + 1
```

**When it matters:** Koko Eating Bananas (#875), Capacity to Ship (#1011), Split Array Largest Sum (#410), Sqrt(x) (#69). Recognizable by phrasing like "minimum X such that Y" or "maximum X such that Y".

---

## Core Patterns

### Classic Search (Sorted Array)
**When to use:** Find a specific value in a sorted array. Return its index or -1.
**Complexity:** O(log n) time, O(1) space
**Problems:** Binary Search (#704), Search Insert Position (#35), Guess Number (#374)
**Common mistake:** Using `mid = (left + right) // 2` — not an issue in Python (arbitrary precision ints), but the safe form `left + (right - left) // 2` is a habit worth keeping.

```python
left, right = 0, len(nums) - 1
while left <= right:              # <= because a single-element window is valid
    mid = left + (right - left) // 2
    if nums[mid] == target:
        return mid
    elif nums[mid] < target:
        left = mid + 1
    else:
        right = mid - 1
return -1
```

### Lower Bound (First True)
**When to use:** Find the first index where a condition becomes true. The condition is false for indices below the answer and true for indices at/above it. Converges to `left == right`.
**Complexity:** O(log n) time, O(1) space
**Problems:** Search Insert Position (#35), Time Based Key-Value Store (#981), Koko Eating Bananas (#875)
**Common mistake:** Setting `right = n - 1` instead of `right = n` — if the answer is "insert at the end", the result is n, which is out of bounds for right = n-1.

```python
left, right = 0, len(nums)   # right = n, not n-1, to allow answer = n
while left < right:           # strict < — loop ends when left == right
    mid = left + (right - left) // 2
    if condition(mid):
        right = mid           # mid could be the answer, don't exclude it
    else:
        left = mid + 1        # mid is definitely not the answer
return left                   # left == right == first index where condition is True
```

### Binary Search on the Answer
**When to use:** The problem asks for the minimum (or maximum) value satisfying some constraint. Define `lo` and `hi` as the bounds of the answer space and write a `feasible(mid)` checker.
**Complexity:** O(log(hi - lo) · cost_of_feasible) time, O(1) space
**Problems:** Koko Eating Bananas (#875), Capacity to Ship (#1011), Sqrt(x) (#69), Split Array Largest Sum (#410)
**Common mistake:** Getting the feasibility direction wrong — if `feasible(mid)` means "mid is good enough", you want the minimum feasible value, so set `right = mid` (not `right = mid - 1`) to avoid skipping the answer.

```python
lo, hi = min_possible_answer, max_possible_answer
while lo < hi:
    mid = lo + (hi - lo) // 2
    if feasible(mid):
        hi = mid         # mid works, but something smaller might too
    else:
        lo = mid + 1     # mid doesn't work, need at least mid+1
return lo                # minimum value that is feasible
```

### Rotated Sorted Array
**When to use:** A sorted array has been rotated at an unknown pivot. Determine which half is still contiguous and sorted, then check if the target falls in that half.
**Complexity:** O(log n) time, O(1) space
**Problems:** Search in Rotated Sorted Array (#33), Find Minimum in Rotated Sorted Array (#153), Search in Rotated Sorted Array II (#81)
**Common mistake:** Not handling duplicates (for #81) — when `nums[left] == nums[mid]`, you can't determine which half is sorted, so you must shrink with `left += 1` instead of halving.

```python
left, right = 0, len(nums) - 1
while left <= right:
    mid = left + (right - left) // 2
    if nums[mid] == target:
        return mid
    # left half is sorted
    if nums[left] <= nums[mid]:
        if nums[left] <= target < nums[mid]:
            right = mid - 1
        else:
            left = mid + 1
    # right half is sorted
    else:
        if nums[mid] < target <= nums[right]:
            left = mid + 1
        else:
            right = mid - 1
return -1
```

---

## Syntax Reference

### Standard binary search template

```python
left, right = 0, len(nums) - 1    # inclusive bounds for classic search
while left <= right:               # change to < for lower-bound pattern
    mid = left + (right - left) // 2
    if nums[mid] == target: ...
    elif nums[mid] < target: left = mid + 1
    else: right = mid - 1
```

### bisect module (stdlib)

Use `bisect` when you need lower/upper bound without writing the loop yourself.

```python
import bisect

bisect.bisect_left(arr, x)    # index of first element >= x (lower bound)
bisect.bisect_right(arr, x)   # index of first element > x  (upper bound)
                               # equivalently: index to insert x to keep arr sorted, after existing x's

# Example:
arr = [1, 3, 3, 5, 7]
bisect.bisect_left(arr, 3)    # → 1  (first 3 is at index 1)
bisect.bisect_right(arr, 3)   # → 3  (insert after both 3s)

# Check if x exists:
i = bisect.bisect_left(arr, x)
if i < len(arr) and arr[i] == x:
    ...  # x is present

bisect.insort(arr, x)         # inserts x in sorted order — O(n) due to list shift
```

### 2D matrix flattened to 1D

For a matrix with `m` rows and `n` columns treated as a single sorted array of length `m*n`:

```python
left, right = 0, m * n - 1
while left <= right:
    mid = left + (right - left) // 2
    row, col = mid // n, mid % n        # convert flat index to (row, col)
    val = matrix[row][col]
    if val == target: return True
    elif val < target: left = mid + 1
    else: right = mid - 1
```

### Feasibility check for "binary search on answer"

```python
# Koko Eating Bananas — feasible(k) = can eat all piles in h hours at speed k?
def feasible(k):
    return sum(math.ceil(p / k) for p in piles) <= h

# Capacity to Ship — feasible(cap) = can ship all weights in d days at capacity cap?
def feasible(cap):
    days, load = 1, 0
    for w in weights:
        if load + w > cap:
            days += 1; load = 0
        load += w
    return days <= d
```

### Handling duplicates in rotated array (#81)

```python
# When nums[left] == nums[mid], you can't tell which half is sorted.
# Shrink left by 1 — this is the only case where O(log n) degrades to O(n).
if nums[left] == nums[mid]:
    left += 1
    continue
```

### math.ceil without importing math

```python
import math
math.ceil(a / b)     # standard

# Integer-only equivalent (no float):
(a + b - 1) // b    # ceiling division for positive integers
```
