"""

34. Find First and Last Position of Element in Sorted Array

Medium

Given an array of integers nums sorted in non-decreasing order, 
find the starting and ending position of a given target value.
If target is not found in the array, return [-1, -1].
You must write an algorithm with O(log n) runtime complexity.

Example 1:

    Input: nums = [5,7,7,8,8,10], target = 8
    Output: [3,4]

Example 2:

    Input: nums = [5,7,7,8,8,10], target = 6
    Output: [-1,-1]

Example 3:

    Input: nums = [], target = 0
    Output: [-1,-1]

Constraints:

    0 <= nums.length <= 105
    -109 <= nums[i] <= 109
    nums is a non-decreasing array.
    -109 <= target <= 109

"""

class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:

        def bound(first: bool) -> int:

            left = 0
            right = len(nums) - 1
            found = -1

            while left <= right:

                mid = left + (right - left) // 2

                if nums[mid] == target:
                    found = mid
                    if first:
                        right = mid - 1
                    else:
                        left = mid + 1
                elif nums[mid] < target:
                    left = mid + 1
                else:
                    right = mid - 1

            return found

        return [bound(True), bound(False)]




### additional solution ###

from bisect import bisect_left, bisect_right

class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:

        start = bisect_left(nums, target)

        if start == len(nums) or nums[start] != target:
            return [-1, -1]

        return [start, bisect_right(nums, target) - 1]
