# 02. Two Pointers — Practice

The Roadmap follows a curated list called the NeetCode 150 for practice problems. If you want more or fewer problems, check the other lists in [lists/](../../lists/).

[← Back to the lesson](../learning/02-two-pointers.md) · [🗺 Roadmap](../../roadmap.md)

---

### 125. Valid Palindrome — Easy
[LeetCode](https://leetcode.com/problems/valid-palindrome/)  
[Solution file (no hints)](../../problems/0001-0499/125.py)

Given a string, determine if it's a palindrome after ignoring non-alphanumeric characters and case. How could two cursors, one at each end, let you check this in one pass without building a cleaned copy first?

<details>
<summary>Hint</summary>

Walk two pointers inward from each end of the string (see [Two Pointers](../learning/02-two-pointers.md)). Skip non-alphanumeric characters as you go, and compare the remaining characters case-insensitively.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def isPalindrome(self, s: str) -> bool:

        left = 0
        right = len(s) - 1

        while left < right:
            while left < right and not s[left].isalnum():
                left += 1
            while right > left and not s[right].isalnum():
                right -= 1

            if s[left].lower() != s[right].lower():
                return False
            else:
                left += 1
                right -= 1
        return True
```

Building blocks: [while-loop](../syntax/while-loop.md) · [string-methods](../syntax/string-methods.md) (`.isalnum()`, `.lower()`) · [if-return](../syntax/if-return.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — each pointer crosses the string at most once.
**Space: O(1)** — only two index variables, no extra copy of the string.
</details>

---

### 167. Two Sum II (Input Array Is Sorted) — Medium
[LeetCode](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)  
[Solution file (no hints)](../../problems/0001-0499/167.py)

Given a sorted array, find two numbers that add up to a target. Since the array is sorted, how could moving a low and high pointer toward each other let you skip a hashmap entirely?

<details>
<summary>Hint</summary>

Start pointers at both ends (see [Two Pointers](../learning/02-two-pointers.md)). If the sum is too big, move the right pointer left; if too small, move the left pointer right.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:

        left = 0
        right = len(numbers) - 1

        while left < right:
            if numbers[left] + numbers[right] < target:
                left += 1
            elif numbers[left] + numbers[right] > target:
                right -= 1
            else:
                return [left + 1, right + 1]
```

Building blocks: [while-loop](../syntax/while-loop.md) · [if-return](../syntax/if-return.md) · [elif-else](../syntax/elif-else.md) · [comparison-operators](../syntax/comparison-operators.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — the pointers together traverse the array once.
**Space: O(1)** — no extra data structure needed.
</details>

---

### 15. 3Sum — Medium
[LeetCode](https://leetcode.com/problems/3sum/)  
[Solution file (no hints)](../../problems/0001-0499/15.py)

Given an array, find all unique triplets that sum to zero. How does sorting first let you fix one number and turn the rest of the problem into a two-pointer search — while also making duplicates easy to skip?

<details>
<summary>Hint</summary>

Sort the array. Fix each number `nums[i]` in turn, then run the two-pointer technique from [167](#167-two-sum-ii-input-array-is-sorted--medium) on the remainder of the array to find pairs that sum to `-nums[i]`. Skip over repeated values to avoid duplicate triplets.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:

        nums.sort()
        result = []

        for i in range(len(nums)):

            if i > 0 and nums[i] == nums[i - 1]:
                continue

            left = i + 1
            right = len(nums) - 1

            while left < right:
                if nums[i] + nums[left] + nums[right] < 0:
                    left += 1
                elif nums[i] + nums[left] + nums[right] > 0:
                    right -= 1
                else:
                    result.append([nums[i], nums[left], nums[right]])
                    left += 1
                    right -= 1

                    while left < right and nums[left] == nums[left - 1]:
                        left += 1

        return result
```

Building blocks: [list-methods](../syntax/list-methods.md) (`.sort()`, `.append()`) · [for-loop](../syntax/for-loop.md) · [break-continue](../syntax/break-continue.md) (`continue`) · [while-loop](../syntax/while-loop.md) · [elif-else](../syntax/elif-else.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n²)** — sorting is O(n log n), then an O(n) outer loop each running an O(n) two-pointer scan.
**Space: O(1)** extra beyond the output (or O(n) / O(log n) depending on the sort's implementation).
</details>

---

### 11. Container With Most Water — Medium
[LeetCode](https://leetcode.com/problems/container-with-most-water/)  
[Solution file (no hints)](../../problems/0001-0499/11.py)

Given heights at each index, find two lines that, with the x-axis, form the container holding the most water. Why is it always safe to move the pointer at the *shorter* line inward?

<details>
<summary>Hint</summary>

Start with pointers at both ends (see [Two Pointers](../learning/02-two-pointers.md)). The container's area is capped by the shorter line, so moving the taller line inward can only shrink the width without any chance of a taller wall — always move the shorter one instead.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def maxArea(self, height: List[int]) -> int:

        left = 0
        right = len(height) - 1
        max_area = 0

        while left < right:
            area = (right - left) * min(height[left], height[right])
            max_area = max(max_area, area)

            if height[left] < height[right]:
                left += 1
            else:
                right -= 1

        return max_area
```

Building blocks: [while-loop](../syntax/while-loop.md) · [comparison-operators](../syntax/comparison-operators.md) (`min()`, `max()`) · [elif-else](../syntax/elif-else.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — the pointers together traverse the array once.
**Space: O(1)** — only a few running variables.
</details>

---

### 42. Trapping Rain Water — Hard
[LeetCode](https://leetcode.com/problems/trapping-rain-water/)  
[Solution file (no hints)](../../problems/0001-0499/42.py)

Given elevation heights, compute how much rain water is trapped between the bars. At each position, water depth is bounded by the shorter of the tallest wall to its left and right — how do two pointers track both maxes without precomputing arrays?

<details>
<summary>Hint</summary>

Track a running `left_max` and `right_max` while moving two pointers inward (see [Two Pointers](../learning/02-two-pointers.md)). Whichever side has the smaller max is the one that determines trapped water at that pointer, so advance that pointer.
</details>

<details>
<summary>Solution</summary>

```python
class Solution:
    def trap(self, height: List[int]) -> int:

        left = 0
        right = len(height) - 1
        left_max = height[left]
        right_max = height[right]
        rain = 0

        while left < right:
            if left_max < right_max:
                left += 1
                left_max = max(left_max, height[left])
                rain += left_max - height[left]
            else:
                right -= 1
                right_max = max(right_max, height[right])
                rain += right_max - height[right]

        return rain
```

Building blocks: [while-loop](../syntax/while-loop.md) · [comparison-operators](../syntax/comparison-operators.md) (`max()`) · [arithmetic-operators](../syntax/arithmetic-operators.md) (`+=`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — a single pass with two pointers.
**Space: O(1)** — only a few running variables, no precomputed left/right max arrays.
</details>
