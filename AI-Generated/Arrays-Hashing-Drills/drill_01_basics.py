"""
DRILL 01: Basic Array Traversal & Hash Set Operations

Concept: Understanding when to use a hash set for O(1) lookups

Problem: Find All Missing Elements
Given an array nums containing n integers in the range [1, n+k] where some
numbers appear multiple times and others are missing. Find all numbers in
the range [1, n] that don't appear in nums.

Example 1:
Input: nums = [4, 3, 2, 7, 8, 2, 1]
Output: [5, 6]
Explanation: n=7, the array should contain 1-7, but 5 and 6 are missing.

Example 2:
Input: nums = [1, 1, 2, 3]
Output: [4]
Explanation: n=4, numbers 1-4 should be there, but 4 is missing.

Constraints:
- 1 <= len(nums) <= 10^4
- 1 <= nums[i] <= len(nums) + 1000

Target Complexity:
Time: O(n)
Space: O(n)

HINTS (try without looking first!):
1. What data structure gives you O(1) lookup?
2. Convert the array to a set first
3. Then check which numbers from 1 to n are not in the set
"""

from typing import List

class Solution:
    def findMissingNumbers(self, nums: List[int]) -> List[int]:
        # Your code here
        hashset = set()
        count = 0

        for num in nums:
            hashset.add(num)
            count += 1 
            if count != nums:
                return nums

        pass


# Test cases
def test_drill_01():
    solution = Solution()

    # Test case 1
    assert sorted(solution.findMissingNumbers([4, 3, 2, 7, 8, 2, 1])) == [5, 6]

    # Test case 2
    assert solution.findMissingNumbers([1, 1, 2, 3]) == [4]

    # Test case 3
    assert solution.findMissingNumbers([1, 2, 3, 4, 5]) == []

    # Test case 4
    assert solution.findMissingNumbers([2, 2, 2]) == [1, 3]

    print("✓ All test cases passed!")

if __name__ == "__main__":
    test_drill_01()
