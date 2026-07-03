# 05. Binary Search — Practice

The Roadmap follows a curated list called the NeetCode 150 for practice problems. If you want more or fewer problems, check the other lists in [lists/](../../lists/).

[← Back to the lesson](../learning/05-binary-search.md) · [🗺 Roadmap](../../roadmap.md)

---

### 704. Binary Search — Easy
[LeetCode](https://leetcode.com/problems/binary-search/)  
[Solution file (no hints)](../../problems/0500-0999/704.py)

Given a sorted array and a target, return its index or -1. What invariant do you keep about the search space so that each comparison eliminates half of it?

<details>
<summary>Hint</summary>

Keep `[l, r]` as the range that could still contain the target (see [Binary Search](../algorithms/binary-search.md)). Compare the target to the midpoint and discard the half that can't contain it.
</details>

<details>
<summary>Solution</summary>

```python
l, r = 0, len(nums) - 1
while l <= r:                        # while loop, search space still valid
    mid = (l + r) // 2
    if nums[mid] == target:
        return mid
    elif nums[mid] < target:           # target must be in the right half
        l = mid + 1
    else:                              # target must be in the left half
        r = mid - 1
return -1
```

Building blocks: [while-loop](../syntax/while-loop.md) · [integer-division-modulo](../syntax/integer-division-modulo.md) (`//`) · [if-return](../syntax/if-return.md) · [elif-else](../syntax/elif-else.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(log n)** — the search space halves every iteration.
**Space: O(1)** — only a few index variables.
</details>

---

### 74. Search a 2D Matrix — Medium
[LeetCode](https://leetcode.com/problems/search-a-2d-matrix/)  
[Solution file (no hints)](../../problems/0001-0499/74.py)

Given a matrix sorted row-by-row (and each row's first value greater than the previous row's last), find a target. How can you treat the whole matrix as one flat sorted array using just index math?

<details>
<summary>Hint</summary>

Run standard [binary search](../algorithms/binary-search.md) over a virtual index range `0..rows*cols-1`, converting each mid index to `(mid // cols, mid % cols)` to read the actual cell.
</details>

<details>
<summary>Solution</summary>

```python
rows, cols = len(matrix), len(matrix[0])
l, r = 0, rows * cols - 1

while l <= r:                         # while loop over the flattened index range
    mid = (l + r) // 2
    val = matrix[mid // cols][mid % cols]   # translate flat index back to (row, col)
    if val == target:
        return True
    elif val < target:
        l = mid + 1
    else:
        r = mid - 1

return False
```

Building blocks: [nested-lists](../syntax/nested-lists.md) · [while-loop](../syntax/while-loop.md) · [integer-division-modulo](../syntax/integer-division-modulo.md) (`//`, `%`) · [if-return](../syntax/if-return.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(log(rows · cols))** — binary search over the full flattened matrix.
**Space: O(1)** — only a few index variables.
</details>

---

### 875. Koko Eating Bananas — Medium
[LeetCode](https://leetcode.com/problems/koko-eating-bananas/)  
[Solution file (no hints)](../../problems/0500-0999/875.py)

Find the minimum eating speed `k` so Koko finishes all banana piles within `h` hours. Rather than searching the piles, what monotonic property of "hours needed" as a function of `k` lets you binary search on the *answer itself*?

<details>
<summary>Hint</summary>

The hours needed strictly decreases as `k` increases, so it's monotonic — a perfect fit for [binary search](../algorithms/binary-search.md) over the range of possible speeds `1..max(piles)`. For a candidate `k`, compute total hours and shrink the range accordingly.
</details>

<details>
<summary>Solution</summary>

```python
import math

l, r = 1, max(piles)
res = r

while l <= r:                         # while loop, binary searching on speed
    k = (l + r) // 2
    hours = sum(math.ceil(pile / k) for pile in piles)   # hours needed at speed k

    if hours <= h:                       # k works: try to go slower
        res = k
        r = k - 1
    else:                                # too slow: need to eat faster
        l = k + 1

return res
```

Building blocks: [while-loop](../syntax/while-loop.md) · [generator-expressions](../syntax/generator-expressions.md) (`sum(... for ...)`) · [math-module-basics](../syntax/math-module-basics.md) (`math.ceil()`) · [if-return](../syntax/if-return.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n log m)** — n piles summed at each of O(log m) binary search steps, where m is the largest pile.
**Space: O(1)** — a few running variables (ignoring the generator).
</details>

---

### 153. Find Minimum in Rotated Sorted Array — Medium
[LeetCode](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/)  
[Solution file (no hints)](../../problems/0001-0499/153.py)

A sorted array has been rotated at an unknown pivot. Find the minimum element in O(log n). At the midpoint, how do you tell which half is "still rotated" (and therefore contains the pivot/minimum)?

<details>
<summary>Hint</summary>

Compare `nums[mid]` to `nums[r]` (see [Binary Search](../algorithms/binary-search.md)). If `nums[mid] > nums[r]`, the minimum is to the right of mid; otherwise it's at or to the left of mid.
</details>

<details>
<summary>Solution</summary>

```python
l, r = 0, len(nums) - 1
while l < r:                          # while loop narrowing toward the minimum
    mid = (l + r) // 2
    if nums[mid] > nums[r]:             # pivot (and minimum) is in the right half
        l = mid + 1
    else:                                # minimum is at mid or to its left
        r = mid
return nums[l]
```

Building blocks: [while-loop](../syntax/while-loop.md) · [integer-division-modulo](../syntax/integer-division-modulo.md) (`//`) · [if-return](../syntax/if-return.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(log n)** — the search space halves every iteration.
**Space: O(1)** — only a few index variables.
</details>

---

### 33. Search in Rotated Sorted Array — Medium
[LeetCode](https://leetcode.com/problems/search-in-rotated-sorted-array/)  
[Solution file (no hints)](../../problems/0001-0499/33.py)

A rotated sorted array (no duplicates). Find the index of a target in O(log n). Even though the whole array isn't sorted, why is at least one of the two halves around any midpoint always sorted?

<details>
<summary>Hint</summary>

At each midpoint of your [binary search](../algorithms/binary-search.md), figure out which half (left or right of mid) is properly sorted, then check if the target falls in that sorted half's range to decide which side to keep searching.
</details>

<details>
<summary>Solution</summary>

```python
l, r = 0, len(nums) - 1
while l <= r:                          # while loop, search space still valid
    mid = (l + r) // 2
    if nums[mid] == target:
        return mid

    if nums[l] <= nums[mid]:             # left half is sorted
        if nums[l] <= target < nums[mid]:  # target is within the sorted left half
            r = mid - 1
        else:
            l = mid + 1
    else:                                 # right half is sorted
        if nums[mid] < target <= nums[r]:   # target is within the sorted right half
            l = mid + 1
        else:
            r = mid - 1

return -1
```

Building blocks: [while-loop](../syntax/while-loop.md) · [chained-comparisons](../syntax/chained-comparisons.md) · [if-return](../syntax/if-return.md) · [elif-else](../syntax/elif-else.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(log n)** — the search space halves every iteration.
**Space: O(1)** — only a few index variables.
</details>

---

### 981. Time Based Key-Value Store — Medium
[LeetCode](https://leetcode.com/problems/time-based-key-value-store/)  
Solution: not yet solved in this repo.

Design a store that sets a value for a key at a given timestamp, and can get the value for a key at (or just before) a given timestamp. Since sets for a key arrive in increasing timestamp order, how does that let a lookup avoid a linear scan?

<details>
<summary>Hint</summary>

Store, per key, a list of `(timestamp, value)` pairs in a [hashmap](../data-structures/hashmap.md) — timestamps arrive sorted, so a [binary search](../algorithms/binary-search.md) finds the largest timestamp that's `<=` the query timestamp.
</details>

<details>
<summary>Solution</summary>

```python
class TimeMap:
    def __init__(self):
        self.store = {}                     # key -> list of (timestamp, value)

    def set(self, key, value, timestamp):
        self.store.setdefault(key, []).append((timestamp, value))

    def get(self, key, timestamp):
        values = self.store.get(key, [])
        res = ""
        l, r = 0, len(values) - 1

        while l <= r:                         # binary search for latest timestamp <= query
            mid = (l + r) // 2
            if values[mid][0] <= timestamp:      # candidate answer, keep looking right
                res = values[mid][1]
                l = mid + 1
            else:
                r = mid - 1

        return res
```

Building blocks: [class-basics](../syntax/class-basics.md) · [dict-methods](../syntax/dict-methods.md) (`.setdefault()`, `.get()`) · [tuple-basics](../syntax/tuple-basics.md) · [while-loop](../syntax/while-loop.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(1)** for `set`; **O(log n)** for `get`, binary searching the timestamps for that key.
**Space: O(n)** — storing every set call across all keys.
</details>

---

### 4. Median of Two Sorted Arrays — Hard
[LeetCode](https://leetcode.com/problems/median-of-two-sorted-arrays/)  
Solution: not yet solved in this repo.

Given two sorted arrays, find the median of their combined data in O(log(min(m, n))). Instead of merging, how does binary searching a *partition point* in the smaller array let you find the median without ever materializing the merged array?

<details>
<summary>Hint</summary>

[Binary search](../algorithms/binary-search.md) on how many elements to take from the smaller array. A partition is correct when every element on the "left" side of both partitions is `<=` every element on the "right" side.
</details>

<details>
<summary>Solution</summary>

```python
A, B = nums1, nums2
if len(A) > len(B):                    # ensure A is the smaller array
    A, B = B, A

total = len(A) + len(B)
half = total // 2
l, r = 0, len(A) - 1

while True:                              # binary search for the correct partition
    i = (l + r) // 2 if len(A) > 0 else 0   # partition index in A
    j = half - i - 2                          # partition index in B

    a_left = A[i] if i >= 0 else float("-inf")
    a_right = A[i + 1] if (i + 1) < len(A) else float("inf")
    b_left = B[j] if j >= 0 else float("-inf")
    b_right = B[j + 1] if (j + 1) < len(B) else float("inf")

    if a_left <= b_right and b_left <= a_right:  # partition found
        if total % 2:                              # odd total length
            return min(a_right, b_right)
        return (max(a_left, b_left) + min(a_right, b_right)) / 2
    elif a_left > b_right:                        # took too much from A
        r = i - 1
    else:                                          # took too little from A
        l = i + 1
```

Building blocks: [while-loop](../syntax/while-loop.md) · [swap-tuple-assign](../syntax/swap-tuple-assign.md) · [chained-comparisons](../syntax/chained-comparisons.md) · [int-float-basics](../syntax/int-float-basics.md) (`float("inf")`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(log(min(m, n)))** — binary search over the smaller array's partition points.
**Space: O(1)** — only a few index and value variables.
</details>
