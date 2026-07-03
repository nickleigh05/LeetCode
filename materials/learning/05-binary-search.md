# 05. Binary Search & Sorting
*Halve any ordered search space — including the answer itself.*

[← Prev](04b-recursion.md) · [🗺 Roadmap](../../roadmap.md) · [Next →](05b-sorting.md)

---

> **Builds on:** sorted arrays from [Lesson 01](01-arrays-hashing.md). Binary search is the payoff for keeping data ordered.

If the data is sorted (or the *answer* is monotonic), you can throw away half the possibilities with every comparison — O(log n) instead of O(n). The hard part is never the idea; it's the boundary conditions. This lesson also covers **merge sort** and **quick sort**, the two sorts worth knowing cold, since binary search assumes sorted input and many problems sort first.

## The Pattern

### Binary Search on Answer

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

## Algorithm Deep-Dive

### Binary Search

```
  Sorted array: [1, 3, 5, 7, 9, 11, 13, 15]
  Target: 7

  Step 1:  lo=0, hi=7, mid=3 → arr[3]=7 == target ✓

  Step 2 (if target=11):
           lo=0  hi=7  mid=3  arr[3]=7  < 11 → lo=4
           lo=4  hi=7  mid=5  arr[5]=11 == 11 ✓

  Step 3 (if target=6, not present):
           lo=0  hi=7  mid=3  arr[3]=7  > 6 → hi=2
           lo=0  hi=2  mid=1  arr[1]=3  < 6 → lo=2
           lo=2  hi=2  mid=2  arr[2]=5  < 6 → lo=3
           lo=3  hi=2  → lo > hi, STOP → not found

  Search space halves each step → O(log n)
```

**What it does:** Finds a target in a sorted array by repeatedly halving the search space. Requires the array to be sorted (or the search space to be monotone).

**Recognition signals:**
- Array is sorted, or can be sorted
- "Find if X exists", "find leftmost/rightmost position"
- "Minimum/maximum value such that condition holds" → Binary Search on Answer
- O(log n) requirement
- Rotated sorted array

**Variants:**

| Variant | lo/hi adjustment |
|---------|-----------------|
| Standard (find exact) | `lo = mid+1` or `hi = mid-1` |
| Leftmost occurrence | `hi = mid` when `arr[mid] >= target` |
| Rightmost occurrence | `lo = mid` when `arr[mid] <= target` |
| Rotated array | check which half is sorted, adjust accordingly |

**Python:**
```python
# Standard binary search
def binary_search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2   # avoids overflow (matters in other langs)
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

# Find leftmost position (first occurrence)
def leftmost(nums, target):
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid          # don't exclude mid!
    return lo  # lo == hi == insertion point

# Python built-in
import bisect
bisect.bisect_left(nums, target)   # leftmost insertion point
bisect.bisect_right(nums, target)  # rightmost insertion point
```

**Complexity:**

| | Time | Space |
|-|------|-------|
| Standard | O(log n) | O(1) |

**Data structures it uses:**
Array · Binary Search Tree

### Merge Sort

```
  Array: [5, 2, 8, 1, 9, 3]

  Divide:
  [5,2,8,1,9,3]
  [5,2,8]  [1,9,3]
  [5,2] [8]  [1,9] [3]
  [5][2]      [1][9]

  Conquer (merge sorted halves):
  [2,5] [8]  [1,9] [3]
  [2,5,8]  [1,3,9]
  [1,2,3,5,8,9]  ✓

  Merge step (two sorted arrays → one sorted):
  L=[2,5,8]  R=[1,3,9]
  Compare heads:  1<2 → take 1
  L=[2,5,8]  R=[3,9]
  Compare heads:  2<3 → take 2
  ...and so on
```

**What it does:** Recursively divides the array in half, sorts each half, then merges the sorted halves. Guaranteed O(n log n) in all cases and is stable (equal elements maintain relative order).

**Recognition signals:**
- Need stable sort
- Counting inversions
- Sorting linked lists (merge step is natural for linked lists)
- Merge K sorted lists / arrays
- External sorting (data too large for memory)

**Python:**
```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left  = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# Count inversions (during merge, count how many swaps needed)
inversions = 0
def merge_count(arr):
    global inversions
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left  = merge_count(arr[:mid])
    right = merge_count(arr[mid:])
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
            inversions += len(left) - i   # all remaining left elements > right[j]
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged
```

**Complexity:**

| Case | Time | Space |
|------|------|-------|
| Best | O(n log n) | O(n) |
| Average | O(n log n) | O(n) |
| Worst | O(n log n) | O(n) |

**Data structures it uses:**
Array · Linked List (natural merge step)

### Quick Sort

```
  Array: [3, 6, 8, 10, 1, 2, 1]
  Pivot = last element = 1

  Partition around pivot 1:
  i = -1 (boundary of elements ≤ pivot)
  j scans left to right:
    j=0: 3 > 1, skip
    j=1: 6 > 1, skip
    j=2: 8 > 1, skip
    j=3: 10 > 1, skip
    j=4: 1 ≤ 1, i=0, swap arr[0] and arr[4] → [1,6,8,10,3,2,1]
    j=5: 2 > 1, skip
  Swap pivot (arr[6]) with arr[i+1=1]:    → [1,1,8,10,3,2,6]
                                                 ↑
                                           pivot in final position

  Recurse on [1] and [8,10,3,2,6]

  QuickSelect (find kth smallest without full sort):
  Only recurse on the side containing index k → O(n) average
```

**What it does:** Picks a pivot, partitions the array so all elements less than the pivot come before it and all greater after, then recurses on both halves. In-place and cache-friendly. QuickSelect finds the kth element in O(n) average.

**Recognition signals:**
- In-place sort needed (O(1) extra space excluding recursion)
- Kth largest/smallest element (QuickSelect variant)
- When average-case O(n log n) is acceptable but worst-case O(n²) must be avoided by random pivot

**Python:**
```python
import random

def quick_sort(arr, lo, hi):
    if lo < hi:
        p = partition(arr, lo, hi)
        quick_sort(arr, lo, p - 1)
        quick_sort(arr, p + 1, hi)

def partition(arr, lo, hi):
    pivot_idx = random.randint(lo, hi)
    arr[pivot_idx], arr[hi] = arr[hi], arr[pivot_idx]  # move pivot to end
    pivot = arr[hi]
    i = lo - 1
    for j in range(lo, hi):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i+1], arr[hi] = arr[hi], arr[i+1]
    return i + 1

# QuickSelect: kth smallest (0-indexed k)
def quick_select(arr, lo, hi, k):
    if lo == hi:
        return arr[lo]
    p = partition(arr, lo, hi)
    if p == k:
        return arr[p]
    elif k < p:
        return quick_select(arr, lo, p - 1, k)
    else:
        return quick_select(arr, p + 1, hi, k)
```

**Complexity:**

| Case | Time | Space |
|------|------|-------|
| Best / Average | O(n log n) | O(log n) stack |
| Worst (sorted + bad pivot) | O(n²) | O(n) stack |
| QuickSelect avg | O(n) | O(log n) |

**Data structures it uses:**
Array

## The Template

The reusable code skeleton for this pattern lives in [`appendix/templates/binary-search/`](../appendix/templates/binary-search/). Read the README (when to reach for it, variations, common bugs), then type out [`template.py`](../appendix/templates/binary-search/template.py) from memory before you drill problems.

## Practice

Work the matching set in the curated list: [**Binary Search & Sorting problems →**](../../lists/recommended.md#5-binary-search-18-problems). Easy → hard, top to bottom. When the pattern feels automatic, move on — don't grind it forever.

## Check Yourself

- [ ] I can write a binary search with no off-by-one or infinite-loop bugs (I know my loop invariant).
- [ ] I can explain "binary search on the answer" and recognize when the search space isn't the array itself.
- [ ] I can adapt the template to find leftmost/rightmost occurrence.
- [ ] I solved a 🔴 Hard binary-search problem (e.g. Median of Two Sorted Arrays).

---

**Up next:** [Sorting](05b-sorting.md) — how the `sorted()` you lean on actually works, and the n·log n floor.

[← Prev](04b-recursion.md) · [🗺 Roadmap](../../roadmap.md) · [Next →](05b-sorting.md)

