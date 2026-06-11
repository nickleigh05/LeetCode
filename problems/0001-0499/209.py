"""

209. Minimum Size Subarray Sum

Medium

Given an array of positive integers nums and a positive integer target, return the minimal length of a 
subarray whose sum is greater than or equal to target. If there is no such subarray, return 0 instead.

Example 1:

    Input: target = 7, nums = [2,3,1,2,4,3]
    Output: 2
    Explanation: The subarray [4,3] has the minimal length under the problem constraint.

Example 2:

    Input: target = 4, nums = [1,4,4]
    Output: 1

Example 3:

    Input: target = 11, nums = [1,1,1,1,1,1,1,1]
    Output: 0

Constraints:

    1 <= target <= 109
    1 <= nums.length <= 105
    1 <= nums[i] <= 104

Follow up: If you have figured out the O(n) solution, try coding another solution of which the time complexity is O(n log(n)).

"""

class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:

        left = 0
        window_sum = 0
        min_len = float("inf")

        for right in range(len(nums)):
            window_sum += nums[right]

            while window_sum >= target:
                min_len = min(min_len, right - left + 1)
                window_sum -= nums[left]
                left += 1

        return 0 if min_len == float("inf") else min_len
    

















### Follow up ###

class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:

        n = len(nums)
        prefix = [0] * (n + 1)

        for i in range(n):
            prefix[i + 1] = prefix[i] + nums[i]

        min_len = float("inf")

        for i in range(n):
            needed = target + prefix[i]

            lo, hi = i + 1, n
            while lo <= hi:
                mid = (lo + hi) // 2
                if prefix[mid] >= needed:
                    min_len = min(min_len, mid - i)
                    hi = mid - 1
                else:
                    lo = mid + 1

        return 0 if min_len == float("inf") else min_len
    








