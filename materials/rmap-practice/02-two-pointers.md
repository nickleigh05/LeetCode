# 02. Two Pointers — Practice

The Roadmap follows a curated list called the NeetCode 150 for practice problems. If you want more or fewer problems, check the other lists in [lists/](../../lists/).

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
l, r = 0, len(s) - 1
while l < r:                         # while loop closing the gap
    while l < r and not s[l].isalnum():  # skip non-alphanumeric from the left
        l += 1
    while l < r and not s[r].isalnum():  # skip non-alphanumeric from the right
        r -= 1
    if s[l].lower() != s[r].lower():     # if the letters don't match, not a palindrome
        return False
    l += 1
    r -= 1
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
l, r = 0, len(numbers) - 1
while l < r:                         # while loop until pointers meet
    total = numbers[l] + numbers[r]
    if total == target:                # if we found the pair
        return [l + 1, r + 1]           # 1-indexed per problem spec
    elif total < target:               # sum too small, need a bigger left value
        l += 1
    else:                              # sum too big, need a smaller right value
        r -= 1
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
nums.sort()                          # sort so duplicates are adjacent and two-pointer works
res = []

for i in range(len(nums)):             # for loop fixing the first number
    if i > 0 and nums[i] == nums[i - 1]:  # skip duplicate first numbers
        continue
    if nums[i] > 0:                      # sorted + positive means no triplet can sum to 0
        break

    l, r = i + 1, len(nums) - 1
    while l < r:                          # two-pointer search for the remaining pair
        total = nums[i] + nums[l] + nums[r]
        if total > 0:
            r -= 1
        elif total < 0:
            l += 1
        else:
            res.append([nums[i], nums[l], nums[r]])
            l += 1
            while l < r and nums[l] == nums[l - 1]:  # skip duplicate second numbers
                l += 1

return res
```

Building blocks: [list-methods](../syntax/list-methods.md) (`.sort()`, `.append()`) · [for-loop](../syntax/for-loop.md) · [break-continue](../syntax/break-continue.md) · [while-loop](../syntax/while-loop.md) · [elif-else](../syntax/elif-else.md)
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
l, r = 0, len(height) - 1
best = 0
while l < r:                         # while loop until pointers meet
    area = (r - l) * min(height[l], height[r])   # width * shorter wall
    best = max(best, area)
    if height[l] < height[r]:          # move the shorter wall inward
        l += 1
    else:
        r -= 1
return best
```

Building blocks: [while-loop](../syntax/while-loop.md) · [comparison-operators](../syntax/comparison-operators.md) (`min()`, `max()`) · [if-return](../syntax/if-return.md)
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
l, r = 0, len(height) - 1
left_max, right_max = height[l], height[r]
water = 0

while l < r:                          # while loop until pointers meet
    if left_max < right_max:            # left wall is the limiting side
        l += 1
        left_max = max(left_max, height[l])
        water += left_max - height[l]     # water trapped above this bar
    else:                                # right wall is the limiting side
        r -= 1
        right_max = max(right_max, height[r])
        water += right_max - height[r]

return water
```

Building blocks: [while-loop](../syntax/while-loop.md) · [comparison-operators](../syntax/comparison-operators.md) (`max()`) · [arithmetic-operators](../syntax/arithmetic-operators.md) (`+=`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(n)** — a single pass with two pointers.
**Space: O(1)** — only a few running variables, no precomputed left/right max arrays.
</details>
