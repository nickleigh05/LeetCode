"""
DRILL 03: Two-Pointer Techniques with Arrays

Concept: Combining array traversal with hash sets

Problem: Pair with Target Sum
Given a sorted array nums and a target value, find if there exists a pair
of numbers that sum to the target. Return True if such a pair exists.

Example 1:
Input: nums = [1, 2, 3, 4, 6], target = 6
Output: True
Explanation: 2 + 4 = 6

Example 2:
Input: nums = [1, 2, 3, 4, 6], target = 11
Output: False
Explanation: No pair sums to 11.

Example 3:
Input: nums = [2, 5, 9, 11], target = 7
Output: True
Explanation: 2 + 5 = 7

Constraints:
- 2 <= len(nums) <= 10^4
- -10^9 <= nums[i] <= 10^9
- -10^9 <= target <= 10^9
- nums is sorted in ascending order

Target Complexity:
Time: O(n)
Space: O(n) for hash set approach OR O(1) for two-pointer approach

HINTS:
1. Approach 1: Use a hash set to store seen numbers, check if (target - num) exists
2. Approach 2: Since array is sorted, use two pointers (left and right)
3. Try implementing both approaches!
"""

from typing import List

class Solution:
    def hasPairWithSum(self, nums: List[int], target: int) -> bool:
        # Your code here - try the hash set approach first
        pass

    def hasPairWithSumTwoPointers(self, nums: List[int], target: int) -> bool:
        # Bonus: Try the two-pointer approach
        pass


# Test cases
def test_drill_03():
    solution = Solution()

    # Test case 1
    assert solution.hasPairWithSum([1, 2, 3, 4, 6], 6) == True

    # Test case 2
    assert solution.hasPairWithSum([1, 2, 3, 4, 6], 11) == False

    # Test case 3
    assert solution.hasPairWithSum([2, 5, 9, 11], 7) == True

    # Test case 4
    assert solution.hasPairWithSum([-1, 0, 2, 3], 2) == True

    # Test case 5
    assert solution.hasPairWithSum([1, 1], 2) == True

    print("✓ All test cases passed!")

if __name__ == "__main__":
    test_drill_03()
