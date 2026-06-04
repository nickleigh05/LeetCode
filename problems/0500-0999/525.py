"""

525. Contiguous Array

Medium

Given a binary array nums, return the maximum length of a contiguous subarray with an equal number of 0 and 1.

Example 1:

    Input: nums = [0,1]
    Output: 2
    Explanation: [0, 1] is the longest contiguous subarray with an equal number of 0 and 1.

Example 2:

    Input: nums = [0,1,0]
    Output: 2
    Explanation: [0, 1] (or [1, 0]) is a longest contiguous subarray with equal number of 0 and 1.

Example 3:

    Input: nums = [0,1,1,1,1,1,0,0,0]
    Output: 6
    Explanation: [1,1,1,0,0,0] is the longest contiguous subarray with equal number of 0 and 1.

Constraints:

    1 <= nums.length <= 105
    nums[i] is either 0 or 1.

"""

class Solution:
    def findMaxLength(self, nums: List[int]) -> int:
        
        sum_map = {0: -1}
        max_len = 0
        running_sum = 0
        
        for i, num in enumerate(nums):
            running_sum += 1 if num == 1 else -1
            if running_sum in sum_map:
                max_len = max(max_len, i - sum_map[running_sum])
            else:
                sum_map[running_sum] = i
        return max_len
    











### Array solution for speed ###

class Solution:
    def findMaxLength(self, nums: List[int]) -> int:

        n = len(nums)
        first_indices = [-2] * (2 * n + 1)
        first_indices[0 + n] = -1
        max_len = 0
        running_sum = 0
        
        for i, num in enumerate(nums):
            running_sum += 1 if num == 1 else -1
            idx = running_sum + n
            if first_indices[idx] != -2:
                max_len = max(max_len, i - first_indices[idx])
            else:
                first_indices[idx] = i
        return max_len
    










### Brute force solution ###

class Solution:
    def findMaxLength(self, nums: List[int]) -> int:

        n = len(nums)
        max_len = 0
        
        for i in range(n):
            zeros = 0
            ones = 0
            for j in range(i, n):
                if nums[j] == 0:
                    zeros += 1
                else:
                    ones += 1
                if zeros == ones:
                    max_len = max(max_len, j - i + 1)  
        return max_len
    





