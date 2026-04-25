# Binary Search

## 5. Binary Search (7 problems)

| Problem # | Difficulty | Problem Name | LeetCode Link |
|-----------|------------|--------------|---------------|
| 704 | Easy | Binary Search | [Link](https://leetcode.com/problems/binary-search/) |
| 74 | Medium | Search a 2D Matrix | [Link](https://leetcode.com/problems/search-a-2d-matrix/) |
| 875 | Medium | Koko Eating Bananas | [Link](https://leetcode.com/problems/koko-eating-bananas/) |
| 153 | Medium | Find Minimum in Rotated Sorted Array | [Link](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/) |
| 33 | Medium | Search in Rotated Sorted Array | [Link](https://leetcode.com/problems/search-in-rotated-sorted-array/) |
| 981 | Medium | Time Based Key-Value Store | [Link](https://leetcode.com/problems/time-based-key-value-store/) |
| 4 | Hard | Median of Two Sorted Arrays | [Link](https://leetcode.com/problems/median-of-two-sorted-arrays/) |

---

## Data Structures

### Sorted Array
Binary search requires the search space to be sorted (or at least have a monotonic property). You maintain `left` and `right` boundaries and repeatedly halve the search space by checking the midpoint. Each iteration eliminates half the remaining candidates, giving O(log n).

---

## Core Patterns

### Classic Binary Search
`left = 0, right = len - 1`. Compute `mid = (left + right) // 2`. If `nums[mid] == target` you're done. If `nums[mid] < target`, search right half (`left = mid + 1`). Otherwise search left half (`right = mid - 1`). Used in Binary Search, Time Based Key-Value Store.

### Binary Search on Answer Space
Instead of searching an array, search for a value that satisfies a condition. The answer space itself is sorted (monotone), so you binary search on it. Ask "is X a valid answer?" and use that to move your bounds. Used in Koko Eating Bananas — binary search on the eating speed from 1 to max(piles).

### Rotated Array Search
One half of a rotated sorted array is always fully sorted. Check which half is sorted by comparing `nums[mid]` to `nums[left]` or `nums[right]`. Use the sorted half to decide which side to eliminate. Used in Find Minimum in Rotated Sorted Array and Search in Rotated Sorted Array.

### Flatten 2D Matrix
Treat a sorted 2D matrix as a 1D sorted array. Map index `i` to row `i // cols` and column `i % cols`. Then apply classic binary search. Used in Search a 2D Matrix.

### Partition / Median of Two Arrays
Find the correct partition point across two arrays such that the left halves together have the right total count and all left-half values ≤ all right-half values. Binary search on the smaller array's partition point. O(log(min(m, n))). Used in Median of Two Sorted Arrays.
