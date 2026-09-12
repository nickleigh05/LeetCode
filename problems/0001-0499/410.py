"""

410. Split Array Largest Sum

Hard

Given an integer array nums and an integer k, split nums into k non-empty subarrays
such that the largest sum of any subarray is minimized.

Return the minimized largest sum of the split.

A subarray is a contiguous part of the array.

Example 1:

    Input: nums = [7,2,5,10,8], k = 2
    Output: 18
    Explanation: There are four ways to split nums into two subarrays.
    The best way is to split it into [7,2,5] and [10,8], where the largest sum
    among the two subarrays is only 18.

Example 2:

    Input: nums = [1,2,3,4,5], k = 2
    Output: 9

Example 3:

    Input: nums = [1,4,4], k = 3
    Output: 4

Constraints:

    1 <= nums.length <= 1000
    0 <= nums[i] <= 10^6
    1 <= k <= min(50, nums.length)

"""

class Solution:
    def splitArray(self, nums: List[int], k: int) -> int:

        def can_split(max_sum):
            count = 1
            current = 0
            for num in nums:
                if current + num > max_sum:
                    count += 1
                    current = num
                else:
                    current += num
            return count <= k

        lo = max(nums)
        hi = sum(nums)

        while lo < hi:
            mid = (lo + hi) // 2
            if can_split(mid):
                hi = mid
            else:
                lo = mid + 1

        return lo










    