"""
1. Two Sum

Easy

Hint
Given an array of integers nums and an integer target, return indices of the two 
numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not 
use the same element twice.

You can return the answer in any order.

    Example 1:

    Input: nums = [2,7,11,15], target = 9
    Output: [0,1]
    Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

    Example 2:
    Input: nums = [3,2,4], target = 6
    Output: [1,2]

    Example 3:
    Input: nums = [3,3], target = 6
    Output: [0,1]
 
Constraints:

2 <= nums.length <= 104
-109 <= nums[i] <= 109
-109 <= target <= 109
Only one valid answer exists.
"""

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # Code solution below
        
        hashmap = {}
        
        for i, n in enumerate(nums):
            diff = target - n
            if diff in hashmap:
                return [hashmap[diff], i]
            hashmap[n] = i

# Creates an empty dictionary that will store numbers as keys and their indices as values

# Loops through the nums list, where:
#   i is the current index (0, 1, 2, ...)
#   n is the value at that index
#   enumerate() gives us both the index and value at the same time

# Calculates what number we need to add to n to reach the target
# For example, if target is 9 and n is 2, then diff is 7

# Checks if the complement number (diff) has already been seen and stored in our hashmap

# If we found the complement, return a list containing:
#   hashmap[diff] - the index where we previously saw the complement
#   i - the current index

# If we didn't find a match, store the current number n as a key 
# with its index i as the value, so we can find it later if needed