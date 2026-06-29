# 02. Two Pointers
*One scan, two cursors closing in. The trick is knowing which condition moves which pointer.*

[← Prev](01-arrays-hashing.md) · [🗺 Roadmap](../roadmap.md) · [Next →](03-sliding-window.md)

---

> **Builds on:** arrays from [Lesson 01 — Arrays & Hashing](01-arrays-hashing.md). No new data structure here — just a smarter way to scan one.

Once an array is **sorted**, you rarely need a hash map — two indices walking toward each other can find a pair, triple, or sub-range in O(n) with O(1) extra space. This is the first "aha" pattern: the search space halves itself because monotonicity tells you which way to move.

## The Pattern

### Two Pointers

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

## The Template

The reusable code skeleton for this pattern lives in [`appendix/templates/two-pointers/`](../appendix/templates/two-pointers/). Read the README (when to reach for it, variations, common bugs), then type out [`template.py`](../appendix/templates/two-pointers/template.py) from memory before you drill problems.

## Practice

Work the matching set in the curated list: [**Two Pointers problems →**](../../lists/recommended.md#2-two-pointers-14-problems). Easy → hard, top to bottom. When the pattern feels automatic, move on — don't grind it forever.

## Check Yourself

- [ ] I can explain this topic simply, in my own words.
- [ ] I can write the template from scratch without looking.
- [ ] I solved a 🔴 Hard variant of this pattern.

---

**Up next:** [Sliding Window](03-sliding-window.md) — a moving boundary over contiguous ranges — O(n) where brute force is O(n²).

[← Prev](01-arrays-hashing.md) · [🗺 Roadmap](../roadmap.md) · [Next →](03-sliding-window.md)

