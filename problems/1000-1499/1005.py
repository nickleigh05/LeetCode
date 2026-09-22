"""

1005. Maximize Sum Of Array After K Negations

Easy

Given an integer array nums and an integer k, modify the array in the following way:

    choose an index i and replace nums[i] with -nums[i].

You should apply this process exactly k times. Note you can choose the same index i multiple times.

Return the largest possible sum of the array after modifying it in this way.

Example 1:

    Input: nums = [4,2,3], k = 1
    Output: 5
    Explanation: Choose index 1 and nums becomes [4,-2,3].

Example 2:

    Input: nums = [3,-1,0,2], k = 3
    Output: 6
    Explanation: Choose indices (1, 2, 2) and nums becomes [3,1,0,2].

Example 3:

    Input: nums = [2,-3,-1,5,-4], k = 2
    Output: 13
    Explanation: Choose indices (1, 4) and nums becomes [2,3,-1,5,4].

Constraints:

    1 <= nums.length <= 10^4
    -100 <= nums[i] <= 100
    1 <= k <= 10^4

"""

class Solution:
    def largestSumAfterKNegations(self, nums: List[int], k: int) -> int:

        nums.sort()
        i = 0
        n = len(nums)
        while i < n and nums[i] < 0 and k > 0:
            nums[i] = -nums[i]
            i += 1
            k -= 1
        
        total = sum(nums)
        
        if k % 2 == 1:
            total -= 2 * min(nums)
        
        return total












    