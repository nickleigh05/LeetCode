"""

16. 3Sum Closest

Medium

Given an integer array nums of length n and an integer target, find three integers at distinct indices in nums such that the sum is closest to target.

Return the sum of the three integers.

You may assume that each input would have exactly one solution.

Example 1:

    Input: nums = [-1,2,1,-4], target = 1
    Output: 2
    Explanation: The sum that is closest to the target is 2. (-1 + 2 + 1 = 2).

Example 2:

    Input: nums = [0,0,0], target = 1
    Output: 0
    Explanation: The sum that is closest to the target is 0. (0 + 0 + 0 = 0).

Constraints:

    3 <= nums.length <= 500
    -1000 <= nums[i] <= 1000
    -104 <= target <= 104

"""

class Solution:
    def threeSumClosest(self, nums: List[int], target: int) -> int:

        nums.sort()
        res = sum(nums[:3])

        for i in range(len(nums) - 2):
            l, r = i + 1, len(nums) - 1
            while l < r:
                s = nums[i] + nums[l] + nums[r]
                if abs(s - target) < abs(res - target): res = s
                if s < target: l += 1
                elif s > target: r -= 1
                else: return s
        return res
    











### Brute force ###

class Solution:
    def threeSumClosest(self, nums: List[int], target: int) -> int:
        n = len(nums)
        closest = float('inf')
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    s = nums[i] + nums[j] + nums[k]
                    if abs(s - target) < abs(closest - target):
                        closest = s
        return closest
    






### Binary search ###

from bisect import bisect_left

class Solution:
    def threeSumClosest(self, nums: List[int], target: int) -> int:

        nums.sort()
        n = len(nums)
        res = float('inf')

        for i in range(n - 2):
            for j in range(i + 1, n - 1):
                rem = target - (nums[i] + nums[j])
                idx = bisect_left(nums, rem, j + 1)
                
                for k in [idx - 1, idx]:
                    if j < k < n:
                        s = nums[i] + nums[j] + nums[k]
                        if abs(s - target) < abs(res - target):
                            res = s
        return res
    







