# Two Pointers

## How to use this README

Problems are split into three tiers: Blind 75 is the core set every interviewer expects you to know cold. NeetCode 150 adds problems that sharpen the same patterns with more constraints. NeetCode 250 introduces new patterns (reversal tricks, greedy two pointers, multi-pointer reduction) and more complex scenarios. Work through tiers in order — the Core Patterns and Syntax Reference sections below map directly to the problems in each table, so when you hit a new problem, find the matching pattern first, then check the syntax.

---

## Problems

### Blind 75
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved |
|-----------|------------|--------------|---------------|--------|
| 125 | Easy | Valid Palindrome | [Link](https://leetcode.com/problems/valid-palindrome/) | ☑ |
| 15 | Medium | 3Sum | [Link](https://leetcode.com/problems/3sum/) | ☑ |
| 11 | Medium | Container With Most Water | [Link](https://leetcode.com/problems/container-with-most-water/) | ☑ |

### NeetCode 150
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved |
|-----------|------------|--------------|---------------|--------|
| 167 | Medium | Two Sum II - Input Array Is Sorted | [Link](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) | ☑ |
| 42 | Hard | Trapping Rain Water | [Link](https://leetcode.com/problems/trapping-rain-water/) | ☑ |

### NeetCode 250
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved | Pattern |
|-----------|------------|--------------|---------------|--------|---------|
| 344 | Easy | Reverse String | [Link](https://leetcode.com/problems/reverse-string/) | ☐ | Array (in-place reversal) |
| 680 | Easy | Valid Palindrome II | [Link](https://leetcode.com/problems/valid-palindrome-ii/) | ☐ | Shrink from both ends |
| 1768 | Easy | Merge Strings Alternately | [Link](https://leetcode.com/problems/merge-strings-alternately/) | ☐ | Parallel iteration |
| 88 | Easy | Merge Sorted Array | [Link](https://leetcode.com/problems/merge-sorted-array/) | ☐ | Two pointers from the right |
| 26 | Easy | Remove Duplicates from Sorted Array | [Link](https://leetcode.com/problems/remove-duplicates-from-sorted-array/) | ☐ | Slow/fast pointer |
| 18 | Medium | 4Sum | [Link](https://leetcode.com/problems/4sum/) | ☐ | Multi-pointer reduction |
| 189 | Medium | Rotate Array | [Link](https://leetcode.com/problems/rotate-array/) | ☐ | Reversal trick |
| 881 | Medium | Boats to Save People | [Link](https://leetcode.com/problems/boats-to-save-people/) | ☐ | Greedy two pointers |

---

## Complexity Reference

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| Shrink from both ends (single pass) | O(n) | O(1) | Each pointer moves at most n/2 steps |
| Slow/fast pointer (in-place removal) | O(n) | O(1) | One pass, write pointer trails read pointer |
| Two-pointer after sort (2Sum) | O(n log n) | O(1) | Sort dominates; two-pointer scan is O(n) |
| kSum reduction (k=3) | O(n²) | O(1) | Fix one element, run two-pointer for the rest |
| kSum reduction (k=4) | O(n³) | O(1) | Fix two elements, run two-pointer for the rest |
| Merge from right | O(n + m) | O(1) | Merge into pre-allocated buffer |
| Parallel iteration | O(n + m) | O(1) | Walk both arrays one step at a time |

---

## Data Structures

### Array (sorted)

Two pointers work because a sorted array is monotonic — moving left rightward increases values, moving right leftward decreases them. This monotonicity lets you make a guaranteed decision at each step: if the current pair sums too low, advance left; if too high, advance right. No element is visited more than once, so you get O(n) after sorting.

```
Sorted array, two pointers shrinking inward:

Index:   0    1    2    3    4    5
       +----+----+----+----+----+----+
       |  1 |  2 |  5 |  7 |  9 | 11 |
       +----+----+----+----+----+----+
         ↑                        ↑
        left                    right
         └──── compare, move one ────┘
```

**When it matters:** The array must be sorted (or have a monotonic property) for the elimination logic to be correct. If it's unsorted and you can't sort it, two pointers usually won't work.

### Slow/Fast Pointer

Two pointers at different speeds in the same direction. `slow` marks the last valid write position; `fast` scans ahead looking for elements to keep. The gap between them is the "dead zone" of removed elements. Both pointers start at the same end and move rightward — this is different from the shrink-from-both-ends approach.

```
Remove all 2s in-place:

       slow
        ↓
[1, 2, 2, 3, 4]
        ↑ fast scans, skips 2s, copies keepers to slow

After scan: [1, 3, 4, _, _]  — first `slow` elements are valid
```

**When it matters:** Any in-place removal or deduplication on a sorted array. You never shift elements; you just overwrite.

---

## Core Patterns

### Shrink from Both Ends
**When to use:** You need to find a pair (or check a property) across the whole array, and you can eliminate one end based on the comparison result.
**Complexity:** O(n) time after any needed sort, O(1) space
**Problems:** Valid Palindrome (#125), Container With Most Water (#11), Two Sum II (#167), Boats to Save People (#881), Valid Palindrome II (#680)
**Common mistake:** Using `left < right` not `left <= right` — when they meet, there's no pair left to check.

```python
left, right = 0, len(nums) - 1
while left < right:
    if condition_met(nums[left], nums[right]):
        return result
    elif should_advance_left(nums[left], nums[right]):
        left += 1
    else:
        right -= 1
```

### Slow/Fast Pointer
**When to use:** In-place removal or deduplication — you want to overwrite invalid elements without shifting.
**Complexity:** O(n) time, O(1) space
**Problems:** Remove Duplicates from Sorted Array (#26), Remove Element (#27)
**Common mistake:** Returning `slow` instead of `slow + 1` (or vice versa) — track whether `slow` is the count or the next write index.

```python
slow = 0
for fast in range(len(nums)):
    if nums[fast] != val:   # keep this element
        nums[slow] = nums[fast]
        slow += 1
return slow  # number of valid elements
```

### Two-Pointer Reduction (kSum)
**When to use:** Find all unique tuples that sum to a target. Sort first, fix the outer k-2 elements with loops, then run two pointers on the remaining subarray.
**Complexity:** O(n log n + n^(k-1)) — O(n²) for 3Sum, O(n³) for 4Sum
**Problems:** 3Sum (#15), 4Sum (#18)
**Common mistake:** Not skipping duplicate values after moving pointers — leads to duplicate triplets in the output.

```python
nums.sort()
res = []
for i in range(len(nums) - 2):
    if i > 0 and nums[i] == nums[i - 1]:  # skip outer duplicates
        continue
    left, right = i + 1, len(nums) - 1
    while left < right:
        s = nums[i] + nums[left] + nums[right]
        if s == 0:
            res.append([nums[i], nums[left], nums[right]])
            while left < right and nums[left] == nums[left + 1]: left += 1
            while left < right and nums[right] == nums[right - 1]: right -= 1
            left += 1; right -= 1
        elif s < 0: left += 1
        else: right -= 1
```

### Merging from the Right
**When to use:** Merging two sorted arrays into a buffer that already has enough space at the end — filling from the right avoids overwriting unread elements.
**Complexity:** O(n + m) time, O(1) space
**Problems:** Merge Sorted Array (#88)
**Common mistake:** Merging from the left and overwriting nums1 elements before reading them.

```python
i, j, k = m - 1, n - 1, m + n - 1  # i=last of nums1, j=last of nums2, k=write pos
while i >= 0 and j >= 0:
    if nums1[i] > nums2[j]:
        nums1[k] = nums1[i]; i -= 1
    else:
        nums1[k] = nums2[j]; j -= 1
    k -= 1
while j >= 0:  # remaining nums2 elements
    nums1[k] = nums2[j]; j -= 1; k -= 1
```

---

## Syntax Reference

### Setting up two pointers

```python
left, right = 0, len(nums) - 1   # start at both ends
while left < right:               # strict — when they meet, no pair remains
    ...
```

### Sorting before two pointers

```python
nums.sort()              # in-place, O(n log n)
arr = sorted(nums)       # returns new list, original unchanged
```

### Skipping duplicates after a match

Used in 3Sum/4Sum to avoid duplicate tuples in the output. Always advance past the duplicate first, then do the final step.

```python
# after recording a match at (left, right):
while left < right and nums[left] == nums[left + 1]:
    left += 1
while left < right and nums[right] == nums[right - 1]:
    right -= 1
left += 1
right -= 1
```

### Skipping outer-loop duplicates (kSum)

```python
for i in range(len(nums)):
    if i > 0 and nums[i] == nums[i - 1]:  # i > 0 prevents out-of-bounds on first element
        continue
```

### Alphanumeric check for palindrome problems

```python
# str.isalnum() returns True for letters and digits, False for spaces/punctuation
s = ''.join(c.lower() for c in s if c.isalnum())
```

### Parallel iteration (two arrays)

```python
i, j = 0, 0
result = []
while i < len(a) and j < len(b):
    result.append(a[i]); i += 1
    result.append(b[j]); j += 1
# append leftovers from whichever array is longer
result.extend(a[i:])
result.extend(b[j:])
```
