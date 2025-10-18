"""
DRILL 09: Advanced - Prefix Sum with Hashing

Concept: Using hash maps with cumulative sums

Problem: Subarray Sum Equals K
Given an array of integers nums and an integer k, return the total number
of subarrays whose sum equals k.

Example 1:
Input: nums = [1, 1, 1], k = 2
Output: 2
Explanation: [1, 1] appears twice (indices 0-1 and 1-2)

Example 2:
Input: nums = [1, 2, 3], k = 3
Output: 2
Explanation: [1, 2] and [3] both sum to 3

Example 3:
Input: nums = [1, -1, 0], k = 0
Output: 3
Explanation: [1, -1], [-1, 1], and [0] all sum to 0

Constraints:
- 1 <= len(nums) <= 2 * 10^4
- -1000 <= nums[i] <= 1000
- -10^7 <= k <= 10^7

Target Complexity:
Time: O(n)
Space: O(n)

HINTS:
1. Use prefix sum: sum from start to current index
2. If prefix_sum - k exists in our map, we found subarrays
3. Store {prefix_sum: count} in hash map
4. For each position, check if (current_prefix_sum - k) exists
5. This is a tricky problem - study the pattern!

KEY INSIGHT:
If prefix_sum[i] - prefix_sum[j] = k, then subarray from j+1 to i sums to k
"""

from typing import List
from collections import defaultdict

class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        # Your code here
        pass


# Test cases
def test_drill_09():
    solution = Solution()

    # Test case 1
    assert solution.subarraySum([1, 1, 1], 2) == 2

    # Test case 2
    assert solution.subarraySum([1, 2, 3], 3) == 2

    # Test case 3
    assert solution.subarraySum([1, -1, 0], 0) == 3

    # Test case 4
    assert solution.subarraySum([1], 1) == 1

    # Test case 5
    assert solution.subarraySum([1, 2, 1, 2, 1], 3) == 4

    print("✓ All test cases passed!")

if __name__ == "__main__":
    test_drill_09()
