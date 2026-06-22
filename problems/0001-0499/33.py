"""

33. Search in Rotated Sorted Array

Medium

There is an integer array nums sorted in ascending order (with distinct values).

Prior to being passed to your function, nums is possibly left rotated at an unknown index k (1 <= k < nums.length) such that the resulting array is [nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]] (0-indexed). For example, [0,1,2,4,5,6,7] might be left rotated by 3 indices and become [4,5,6,7,0,1,2].

Given the array nums after the possible rotation and an integer target, return the index of target if it is in nums, or -1 if it is not in nums.

You must write an algorithm with O(log n) runtime complexity.

Example 1:

    Input: nums = [4,5,6,7,0,1,2], target = 0
    Output: 4

Example 2:

    Input: nums = [4,5,6,7,0,1,2], target = 3
    Output: -1

Example 3:

    Input: nums = [1], target = 0
    Output: -1

Constraints:

    1 <= nums.length <= 5000
    -104 <= nums[i] <= 104
    All values of nums are unique.
    nums is an ascending array that is possibly rotated.
    -104 <= target <= 104

"""

class Solution:
    def search(self, nums: List[int], target: int) -> int:

        left_index: int = 0
        right_index: int = len(nums) - 1

        while left_index <= right_index:
            middle_index: int = (left_index + right_index) // 2

            if nums[middle_index] == target:
                return middle_index

            left_half_is_sorted: bool = nums[left_index] <= nums[middle_index]

            if left_half_is_sorted:
                target_in_left_half: bool = nums[left_index] <= target < nums[middle_index]
                if target_in_left_half:
                    right_index = middle_index - 1
                else:
                    left_index = middle_index + 1
            else:
                target_in_right_half: bool = nums[middle_index] < target <= nums[right_index]
                if target_in_right_half:
                    left_index = middle_index + 1
                else:
                    right_index = middle_index - 1

        return -1
    











    