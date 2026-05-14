"""

169. Majority Element

Easy

Given an array nums of size n, return the majority element.

The majority element is the element that appears more than ⌊n / 2⌋ times. You may assume that the majority element always exists in the array.

Example 1:

    Input: nums = [3,2,3]
    Output: 3

Example 2:

    Input: nums = [2,2,1,1,1,2,2]
    Output: 2

Constraints:

    n == nums.length
    1 <= n <= 5 * 104
    -109 <= nums[i] <= 109
    The input is generated such that a majority element will exist in the array.
 
Follow-up: Could you solve the problem in linear time and in O(1) space?
 
"""

class Solution:
    def majorityElement(self, nums: List[int]) -> int:

        counts = {}
        threshold = len(nums) // 2
    
        for num in nums:
            counts[num] = counts.get(num, 0) + 1
            
            if counts[num] > threshold:
                return num







### Boyer Moore Voting Algorithm ###

class Solution:
    def majorityElement(self, nums: List[int]) -> int:

        candidate = None
        count = 0

        for num in nums:

            if count == 0:
                candidate = num

            if num == candidate:
                count += 1
            else:
                count -= 1

        return candidate
    










