"""

448. Find All Numbers Disappeared in an Array

Easy

Given an array nums of n integers where nums[i] is in the range [1, n], return an array of all the integers in the range [1, n] that do not appear in nums.

Example 1:

    Input: nums = [4,3,2,7,8,2,3,1]
    Output: [5,6]

Example 2:

    Input: nums = [1,1]
    Output: [2]

Constraints:

    n == nums.length
    1 <= n <= 105
    1 <= nums[i] <= n

Follow up: Could you do it without extra space and in O(n) runtime? You may assume the returned list does not count as extra space.

"""

class Solution:
    def findDisappearedNumbers(self, nums: List[int]) -> List[int]:
        
        seen = set()
        result = []

        for num in nums:
            seen.add(num)

        for i in range(1, len(nums) + 1):
            if i not in seen:
                result.append(i)
        return result 
    







### Another solution that does not use extra space, but modifies the input array. ###

class Solution:
    def findDisappearedNumbers(self, nums: List[int]) -> List[int]:

        for num in nums:
            idx = abs(num) - 1
            if nums[idx] > 0:
                nums[idx] = -nums[idx]

        result = []
        for i in range(len(nums)):
            if nums[i] > 0:
                result.append(i + 1)

        return result