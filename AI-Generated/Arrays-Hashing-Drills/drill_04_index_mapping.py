"""
DRILL 04: Hash Map for Index Mapping (Two Sum Pattern)

Concept: Storing values with their indices for lookups

Problem: Two Sum with Indices
Given an array of integers nums and a target, return the indices of the
two numbers that add up to target. You may assume exactly one solution exists.

Example 1:
Input: nums = [2, 7, 11, 15], target = 9
Output: [0, 1]
Explanation: nums[0] + nums[1] = 2 + 7 = 9

Example 2:
Input: nums = [3, 2, 4], target = 6
Output: [1, 2]
Explanation: nums[1] + nums[2] = 2 + 4 = 6

Example 3:
Input: nums = [3, 3], target = 6
Output: [0, 1]

Constraints:
- 2 <= len(nums) <= 10^4
- -10^9 <= nums[i] <= 10^9
- -10^9 <= target <= 10^9
- Exactly one solution exists

Target Complexity:
Time: O(n)
Space: O(n)

HINTS:
1. Use a hash map to store {value: index}
2. For each number, check if (target - number) exists in the map
3. If it exists, return both indices
4. If not, add current number and its index to the map
"""

from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # Your code here
        pass


# Test cases
def test_drill_04():
    solution = Solution()

    # Test case 1
    result = solution.twoSum([2, 7, 11, 15], 9)
    assert sorted(result) == [0, 1]

    # Test case 2
    result = solution.twoSum([3, 2, 4], 6)
    assert sorted(result) == [1, 2]

    # Test case 3
    result = solution.twoSum([3, 3], 6)
    assert sorted(result) == [0, 1]

    # Test case 4
    result = solution.twoSum([-1, -2, -3, -4, -5], -8)
    assert sorted(result) == [2, 4]

    print("✓ All test cases passed!")

if __name__ == "__main__":
    test_drill_04()
