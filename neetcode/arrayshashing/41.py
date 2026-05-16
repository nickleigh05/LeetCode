"""

41. First Missing Positive

Hard

Given an unsorted integer array nums. Return the smallest positive integer that is not present in nums.

You must implement an algorithm that runs in O(n) time and uses O(1) auxiliary space.

Example 1:

    Input: nums = [1,2,0]
    Output: 3
    Explanation: The numbers in the range [1,2] are all in the array.

Example 2:

    Input: nums = [3,4,-1,1]
    Output: 2
    Explanation: 1 is in the array but 2 is missing.

Example 3:

    Input: nums = [7,8,9,11,12]
    Output: 1
    Explanation: The smallest positive integer 1 is missing.

Constraints:

    1 <= nums.length <= 105
    -231 <= nums[i] <= 231 - 1

"""

class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:

        n = len(nums)

        for i in range(n):
            while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
                correct = nums[i] - 1
                nums[i], nums[correct] = nums[correct], nums[i]

        for i in range(n):
            if nums[i] != i + 1:
                return i + 1
                
        return n + 1









"""
For the constraints given (O(n) time, O(1) space) that's essentially the optimal solution.
 It's a well-known result that you can't do better.

If you drop the O(1) space constraint there are simpler approaches:

Set — O(n) time, O(n) space

        pythons = set(nums)
        i = 1
        while i in s:
            i += 1
        return i

Clean and readable but uses O(n) extra space.

Sort — O(n log n) time, O(1) space

        pythonnums.sort()
        res = 1
        for n in nums:
            if n == res:
                res += 1
        return res

Simpler logic but worse time complexity.
"""













