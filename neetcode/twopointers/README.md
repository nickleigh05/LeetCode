# Two Pointers

## 2. Two Pointers (5 problems)

| Problem # | Difficulty | Problem Name | LeetCode Link |
|-----------|------------|--------------|---------------|
| 125 | Easy | Valid Palindrome | [Link](https://leetcode.com/problems/valid-palindrome/) |
| 167 | Medium | Two Sum II | [Link](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) |
| 15 | Medium | 3Sum | [Link](https://leetcode.com/problems/3sum/) |
| 11 | Medium | Container With Most Water | [Link](https://leetcode.com/problems/container-with-most-water/) |
| 42 | Hard | Trapping Rain Water | [Link](https://leetcode.com/problems/trapping-rain-water/) |

---

## Data Structures

### Array / String
Two pointers work directly on arrays or strings. No extra data structure is needed — you just maintain two index variables (`left` and `right`) and move them based on conditions. The power comes from exploiting the fact that the input is **sorted** or has some structural symmetry (like a palindrome).

---

## Core Patterns

### Converging Pointers (Opposite Ends)
Start `left = 0` and `right = len - 1`. Move them toward each other based on a comparison. Because the array is sorted, moving the smaller pointer inward increases the sum and moving the larger pointer inward decreases it — this lets you hit a target without checking every pair. O(n) instead of O(n²). Used in Two Sum II, 3Sum, Container With Most Water.

### Mirror / Palindrome Check
Start both pointers at opposite ends and walk inward, comparing characters. If they always match, it's a palindrome. Skip non-alphanumeric characters as needed. Used in Valid Palindrome.

### Fix One, Search with Two Pointers
Sort the array first. Fix one element `nums[i]`, then run converging two pointers on the rest of the array to find pairs that sum to a target. This is how 3Sum reduces O(n³) brute force to O(n²). Sorting first also makes it easy to skip duplicates.

### Left Max / Right Max (Trapping Water)
For each position, the water it can hold equals `min(max_left, max_right) - height[i]`. Track running max from both sides with two pointers — you can process whichever side has the smaller max because the water level at that side is already determined. Used in Trapping Rain Water.
