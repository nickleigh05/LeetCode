"""
217. Contains Duplicate

Easy

Given an integer array nums, return true if any value appears at least 
twice in the array, and return false if every element is distinct.

    Example 1:

    Input: nums = [1,2,3,1]
    Output: true

    Explanation:
    The element 1 occurs at the indices 0 and 3.

    Example 2:

    Input: nums = [1,2,3,4]
    Output: false

    Explanation:
    All elements are distinct.

    Example 3:

    Input: nums = [1,1,1,3,3,4,3,2,4,2]
    Output: true

Constraints:
1 <= nums.length <= 10^5
-10^9 <= nums[i] <= 10^9
"""

class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        # Code solution below

        hashset = set()
        for num in nums:
            if num in hashset:
                return True
            else:
                hashset.add(num)
        return False
    
# Creates an empty set to store unique numbers we've seen so far

# Loop through each number in the nums array

# Check if the current number already exists in our hashset
# If it does, we found a duplicate - return True immediately

# If the number is not in the hashset, add it to the set
# so we can detect it if we see it again later

# If we've gone through all numbers without finding any duplicates, return False