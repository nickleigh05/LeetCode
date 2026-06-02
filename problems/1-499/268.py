"""

268. Missing Number

Easy

Given an array nums containing n distinct numbers in the range [0, n], return the only number in the range that is missing from the array.

Example 1:

    Input: nums = [3,0,1]

    Output: 2

Explanation:

    n = 3 since there are 3 numbers, so all numbers are in the range [0,3]. 2 is the missing number in the range since it does not appear in nums.

    Example 2:

    Input: nums = [0,1]

    Output: 2

Explanation:

    n = 2 since there are 2 numbers, so all numbers are in the range [0,2]. 2 is the missing number in the range since it does not appear in nums.

Example 3:

    Input: nums = [9,6,4,2,3,5,7,0,1]

    Output: 8

Explanation:

    n = 9 since there are 9 numbers, so all numbers are in the range [0,9]. 8 is the missing number in the range since it does not appear in nums.

Constraints:

    n == nums.length
    1 <= n <= 104
    0 <= nums[i] <= n
    All the numbers of nums are unique.

Follow up: Could you implement a solution using only O(1) extra space complexity and O(n) runtime complexity?

"""

### Sum formula solution ###

class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        n = len(nums)

        expected_sum = n * (n + 1) // 2

        actual_sum = sum(nums)
        
        return expected_sum - actual_sum













### Sorting solution ### 

class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        
        sort = sorted(nums)
        missing = None

        for i, num in enumerate(sort):
            if num != i:
                return i
        return len(nums)











### Bitwise xor solution ###

class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        missing = len(nums)
        for i, num in enumerate(nums):
            # XOR the index and the value together
            missing ^= i ^ num
        return missing











### Hash set solution ###

class Solution:
    def missingNumber(self, nums: List[int]) -> int:

        num_set = set(nums)
        n = len(nums)

        for i in range(n + 1):
            if i not in num_set:
                return i











### Hash map solution ###

class Solution:
    def missingNumber(self, nums: List[int]) -> int:

        counts = {}

        for num in nums:
            counts[num] = True

        for i in range(len(nums) + 1):
            if i not in counts:
                return i
            









