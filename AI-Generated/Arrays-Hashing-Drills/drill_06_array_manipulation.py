"""
DRILL 06: Array Manipulation with Hashing

Concept: Modifying arrays while tracking seen elements

Problem: Remove Duplicates and Return Result
Given an array nums, remove all duplicates in-place such that each element
appears only once. Return the new array with unique elements only (not in-place).

Additionally, return a list of all elements that were duplicates.

Example 1:
Input: nums = [1, 1, 2, 3, 3, 4]
Output:
  unique = [1, 2, 3, 4]
  duplicates = [1, 3]

Example 2:
Input: nums = [1, 2, 3]
Output:
  unique = [1, 2, 3]
  duplicates = []

Example 3:
Input: nums = [5, 5, 5, 5]
Output:
  unique = [5]
  duplicates = [5, 5, 5]

Constraints:
- 1 <= len(nums) <= 10^4
- -10^4 <= nums[i] <= 10^4

Target Complexity:
Time: O(n)
Space: O(n)

HINTS:
1. Use a set to track seen elements
2. Maintain a result list for unique elements
3. When you see a number for the first time, add to unique list
4. When you see it again, add to duplicates list
"""

from typing import List, Tuple

class Solution:
    def removeDuplicates(self, nums: List[int]) -> Tuple[List[int], List[int]]:
        """
        Returns (unique_elements, duplicate_elements)
        """
        # Your code here
        pass


# Test cases
def test_drill_06():
    solution = Solution()

    # Test case 1
    unique, duplicates = solution.removeDuplicates([1, 1, 2, 3, 3, 4])
    assert unique == [1, 2, 3, 4]
    assert sorted(duplicates) == [1, 3]

    # Test case 2
    unique, duplicates = solution.removeDuplicates([1, 2, 3])
    assert unique == [1, 2, 3]
    assert duplicates == []

    # Test case 3
    unique, duplicates = solution.removeDuplicates([5, 5, 5, 5])
    assert unique == [5]
    assert len(duplicates) == 3

    # Test case 4
    unique, duplicates = solution.removeDuplicates([1, 2, 1, 3, 2, 4])
    assert unique == [1, 2, 3, 4]
    assert sorted(duplicates) == [1, 2]

    print("✓ All test cases passed!")

if __name__ == "__main__":
    test_drill_06()
