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
class Solution:
    def search(self, nums: List[int], target: int) -> int:

        left = 0
        right = len(nums) - 1

        while left <= right:
            mid = (left + right) // 2

            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
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
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:

        m = len(matrix)
        n = len(matrix[0])
        left = 0
        right = (m * n) - 1

        while left <= right:
            mid = (left + right) // 2
            row = mid // n
            col = mid % n

            mid_element = matrix[row][col]

            if mid_element == target:
                return True
            elif mid_element < target:
                left = mid + 1
            else:
                right = mid - 1

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
class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:

        left = 1
        right = max(piles)
        result = right

        while left <= right:
            mid = (left + right) // 2

            hours = 0
            for pile in piles:
                hours += (pile + mid - 1) // mid

            if hours <= h:
                result = mid
                right = mid - 1
            else:
                left = mid + 1

        return result
```

Building blocks: [while-loop](../syntax/while-loop.md) · [for-loop](../syntax/for-loop.md) · [integer-division-modulo](../syntax/integer-division-modulo.md) (`(pile + mid - 1) // mid` is ceiling division) · [comparison-operators](../syntax/comparison-operators.md) (`max()`)
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
class Solution:
    def findMin(self, nums: List[int]) -> int:

        left = 0
        right = len(nums) - 1

        while left < right:
            mid = left + (right - left) // 2

            if nums[mid] > nums[right]:
                left = mid + 1
            else:
                right = mid

        return nums[left]
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
class Solution:
    def search(self, nums: List[int], target: int) -> int:

        left = 0
        right = len(nums) - 1

        while left <= right:
            mid = (left + right) // 2

            if nums[mid] == target:
                return mid

            left_half_is_sorted = nums[left] <= nums[mid]

            if left_half_is_sorted:
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            else:
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1

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
        self.store = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        if key not in self.store:
            self.store[key] = []
        self.store[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        values = self.store.get(key, [])
        result = ""

        left = 0
        right = len(values) - 1

        while left <= right:
            mid = (left + right) // 2

            if values[mid][0] <= timestamp:
                result = values[mid][1]
                left = mid + 1
            else:
                right = mid - 1

        return result
```

Building blocks: [class-basics](../syntax/class-basics.md) · [init-method](../syntax/init-method.md) · [dict-methods](../syntax/dict-methods.md) (`.get()`) · [tuple-basics](../syntax/tuple-basics.md) · [while-loop](../syntax/while-loop.md)
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
class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:

        A, B = nums1, nums2
        if len(A) > len(B):
            A, B = B, A

        total = len(A) + len(B)
        half = total // 2

        left = 0
        right = len(A) - 1

        while True:
            i = (left + right) // 2
            j = half - i - 2

            a_left = A[i] if i >= 0 else float("-inf")
            a_right = A[i + 1] if (i + 1) < len(A) else float("inf")
            b_left = B[j] if j >= 0 else float("-inf")
            b_right = B[j + 1] if (j + 1) < len(B) else float("inf")

            if a_left <= b_right and b_left <= a_right:
                if total % 2:
                    return min(a_right, b_right)
                return (max(a_left, b_left) + min(a_right, b_right)) / 2
            elif a_left > b_right:
                right = i - 1
            else:
                left = i + 1
```

Building blocks: [while-loop](../syntax/while-loop.md) · [swap-tuple-assign](../syntax/swap-tuple-assign.md) · [ternary-expression](../syntax/ternary-expression.md) · [logical-operators](../syntax/logical-operators.md) (`and`) · [int-float-basics](../syntax/int-float-basics.md) (`float("inf")`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(log(min(m, n)))** — binary search over the smaller array's partition points.
**Space: O(1)** — only a few index and value variables.
</details>
