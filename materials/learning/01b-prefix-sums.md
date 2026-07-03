# 01b. Prefix Sums & Difference Arrays

*Precompute once, answer range queries in O(1). The hidden engine behind subarray problems.*

[← Prev](01-arrays-hashing.md) · [🗺 Roadmap](../../roadmap.md) · [Next →](02-two-pointers.md)

---

> **Builds on:** arrays from [Lesson 01](01-arrays-hashing.md) and hash maps for the subarray-sum pattern. This technique is used inside sliding window (03), 2-D DP (15), and several hard array problems — learn it now and it'll feel familiar later.

A prefix sum turns "what's the sum of elements from index 3 to 7?" from an O(n) scan into an O(1) subtraction. A difference array turns "add 5 to every element from index 2 to 9" from an O(n) update into two O(1) writes. Both trade a single O(n) setup cost for constant-time operations that would otherwise force you into nested loops.

## Concept

### 1-D Prefix Sum

```
  Array:   [1,  2,  3,  4,  5]
  Index:    0   1   2   3   4

  Prefix:  [0,  1,  3,  6, 10, 15]
  Index:    0   1   2   3   4   5
            ↑
            sentinel zero — makes the formula work when l=0

  prefix[i] = arr[0] + arr[1] + ... + arr[i-1]
            = prefix[i-1] + arr[i-1]

  Range sum [l, r] (inclusive, 0-indexed):
  sum(l, r) = prefix[r+1] - prefix[l]

  Example:  sum(1, 3) = prefix[4] - prefix[1]
                      = 10 - 1 = 9
  Check:    arr[1]+arr[2]+arr[3] = 2+3+4 = 9 ✓
```

**What it is:** Precompute `prefix[i]` = sum of the first `i` elements. Any range sum then becomes a single subtraction.

**Why it works:** `prefix[r+1]` contains everything from index 0 to r. `prefix[l]` contains everything from 0 to l-1. Subtracting cancels the left portion, leaving exactly [l, r].

```python
def build_prefix(arr):
    prefix = [0] * (len(arr) + 1)
    for i, val in enumerate(arr):
        prefix[i + 1] = prefix[i] + val
    return prefix

def range_sum(prefix, l, r):    # O(1)
    return prefix[r + 1] - prefix[l]
```

**Complexity:** O(n) build once, O(1) per query. Space: O(n).

### Prefix Sum + Hash Map — Subarray Sum Equals K

This is the most common interview use of prefix sums and trips up nearly every beginner.

```
  nums = [1, 2, 3], k = 3

  We want: how many subarrays sum to k?

  Key insight: if prefix[j] - prefix[i] = k,
               then subarray [i, j-1] sums to k.
               Rearranged: prefix[i] = prefix[j] - k.
               So at each j, ask: "have I seen (prefix[j] - k) before?"

  Walk through:
  seen = {0: 1}   ← sentinel: the empty prefix (before index 0) has sum 0

  j=0: prefix=1, need=1-3=-2, seen[-2]=0,  seen={0:1, 1:1}
  j=1: prefix=3, need=3-3=0,  seen[0]=1 ✓ count=1, seen={0:1,1:1,3:1}
  j=2: prefix=6, need=6-3=3,  seen[3]=1 ✓ count=2, seen={...,6:1}

  Answer: 2  (subarrays [1,2] and [3])
```

```python
from collections import defaultdict

def subarray_sum(nums, k):
    count = 0
    prefix = 0
    seen = defaultdict(int)
    seen[0] = 1               # empty prefix
    for num in nums:
        prefix += num
        count += seen[prefix - k]   # how many times we've seen the needed prefix
        seen[prefix] += 1
    return count
```

**Why the `{0: 1}` seed matters:** without it, a subarray that starts at index 0 and sums to k would never be counted, because `prefix[j] - k = 0` and `seen[0]` would be 0.

### 2-D Prefix Sum (used in Lesson 15)

For a matrix, precompute a 2-D prefix table so any rectangle sum is O(1):

```
  Matrix:                Prefix:
  1  2  3                0  0  0  0
  4  5  6     →          0  1  3  6
  7  8  9                0  5 12 21
                         0 12 27 45

  prefix[r][c] = sum of rectangle from (0,0) to (r-1, c-1)

  Rectangle sum [r1,c1] to [r2,c2]:
  = prefix[r2+1][c2+1]
  - prefix[r1][c2+1]
  - prefix[r2+1][c1]
  + prefix[r1][c1]       ← add back the doubly-subtracted corner
```

```python
def build_2d_prefix(matrix):
    R, C = len(matrix), len(matrix[0])
    p = [[0] * (C + 1) for _ in range(R + 1)]
    for r in range(R):
        for c in range(C):
            p[r+1][c+1] = matrix[r][c] + p[r][c+1] + p[r+1][c] - p[r][c]
    return p

def rect_sum(p, r1, c1, r2, c2):
    return p[r2+1][c2+1] - p[r1][c2+1] - p[r2+1][c1] + p[r1][c1]
```

### Difference Array — Efficient Range Updates

When you need to add a value to every element in a range [l, r] (potentially many such updates), a difference array does each update in O(1) and reconstructs the result in O(n).

```
  Goal: add 3 to indices 1–3, then add -1 to indices 2–4.
  arr = [0, 0, 0, 0, 0]   (5 elements)

  Difference array trick:
  diff[l] += val
  diff[r+1] -= val

  Update 1 (add 3 to [1,3]):  diff = [0, +3,  0,  0, -3,  0]
  Update 2 (add -1 to [2,4]): diff = [0, +3, -1,  0, -3, +1]

  Reconstruct with prefix sum:
  result[0] = diff[0] = 0
  result[1] = 0 + 3   = 3
  result[2] = 3 + (-1)= 2
  result[3] = 2 + 0   = 2
  result[4] = 2 + (-3)= -1
```

```python
def range_update(n, updates):
    """updates: list of (l, r, val) — add val to arr[l..r]"""
    diff = [0] * (n + 1)
    for l, r, val in updates:
        diff[l] += val
        diff[r + 1] -= val
    # reconstruct
    result, running = [], 0
    for i in range(n):
        running += diff[i]
        result.append(running)
    return result
```

**Use when:** many range-update queries, then one read of all values. If you need to read individual elements between updates, reach for a segment tree (Lesson 20) instead.

## The Pattern — Recognition Guide

| Signal | Tool |
|--------|------|
| "Sum of subarray from l to r" (multiple queries) | Prefix sum |
| "Number of subarrays with sum equal to k" | Prefix sum + hash map |
| "Product of array except self" | Prefix product + suffix product |
| "Pivot index / balance point" | Prefix sum == suffix sum |
| "Add v to every element in range [l, r], repeat" | Difference array |
| "Range query + point updates" | Segment tree (Lesson 20) |

## Worked Trace — Product of Array Except Self

A classic that combines left prefix products with right suffix products (no division allowed):

```
  nums = [1, 2, 3, 4]

  Left prefix products (each element = product of everything to its left):
  left = [1, 1, 2, 6]

  Right suffix products (each element = product of everything to its right):
  right = [24, 12, 4, 1]

  result[i] = left[i] * right[i]:
  result = [1*24, 1*12, 2*4, 6*1] = [24, 12, 8, 6]
```

```python
def product_except_self(nums):
    n = len(nums)
    result = [1] * n
    prefix = 1
    for i in range(n):              # build left products in-place
        result[i] = prefix
        prefix *= nums[i]
    suffix = 1
    for i in range(n - 1, -1, -1): # multiply in right products
        result[i] *= suffix
        suffix *= nums[i]
    return result
```

## Exercises

<details>
<summary><strong>Exercise 1 — range sum query</strong></summary>

Given `arr = [3, 1, 4, 1, 5, 9, 2, 6]`, compute the sum of elements from index 2 to 5 (inclusive) using a prefix sum.

```
prefix = [0, 3, 4, 8, 9, 14, 23, 25, 31]
sum(2, 5) = prefix[6] - prefix[2] = 23 - 4 = 19
Check: 4+1+5+9 = 19 ✓
```
</details>

<details>
<summary><strong>Exercise 2 — subarray sum equals k, trace</strong></summary>

`nums = [3, 4, 7, 2, -3, 1, 4, 2]`, `k = 7`. How many subarrays sum to 7?

Walk through the prefix-sum + hash-map algorithm. Subarrays: `[3,4]`, `[7]`, `[7,2,-3,1]`, `[1,4,2]` → **4**.
</details>

<details>
<summary><strong>Exercise 3 — pivot index</strong></summary>

Find an index where the sum of elements to its left equals the sum to its right.

```python
def pivot_index(nums):
    total = sum(nums)
    left = 0
    for i, n in enumerate(nums):
        # right sum = total - left - nums[i]
        if left == total - left - n:
            return i
        left += n
    return -1
```

This is O(n) time, O(1) extra space — no prefix array needed, just a running sum.
</details>

## The Template

There's no dedicated code template file for prefix sums (the pattern is compact enough to inline). The standard shapes are the three code blocks above: 1-D build + range query, subarray-sum-k, and product-except-self. Write each one from memory before drilling problems.

## Practice

Work these from the curated list in order:

| # | Difficulty | Problem |
|---|------------|---------|
| 303 | Easy | [Range Sum Query — Immutable](https://leetcode.com/problems/range-sum-query-immutable/) |
| 238 | Medium | [Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) |
| 724 | Easy | [Find Pivot Index](https://leetcode.com/problems/find-pivot-index/) |
| 560 | Medium | [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) |
| 525 | Medium | [Contiguous Array](https://leetcode.com/problems/contiguous-array/) |
| 1480 | Easy | [Running Sum of 1D Array](https://leetcode.com/problems/running-sum-of-1d-array/) |

When you can write the subarray-sum-k solution cold (including the `{0:1}` seed and the reason for it), move on.

## Check Yourself

- [ ] I can build a prefix sum array and answer any range query in O(1).
- [ ] I can write the subarray-sum-k solution from scratch, including the `{0: 1}` seed and the reason it's required.
- [ ] I understand the 2-D prefix sum formula (the inclusion-exclusion with four corners).
- [ ] I know what a difference array is and when to use it instead of a prefix sum.
- [ ] I can solve Product of Array Except Self using prefix + suffix products.

---

**Up next:** [Two Pointers](02-two-pointers.md) — once an array is sorted, two cursors closing in can find pairs and triplets without a hash map.

[← Prev](01-arrays-hashing.md) · [🗺 Roadmap](../../roadmap.md) · [Next →](02-two-pointers.md)
