"""

47. Permutations II

Medium

Given a collection of numbers, nums, that might contain duplicates, return all possible unique permutations in any order.

Example 1:

    Input: nums = [1,1,2]
    Output:
    [[1,1,2],
     [1,2,1],
     [2,1,1]]

Example 2:

    Input: nums = [1,2,3]
    Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]

Constraints:

    1 <= nums.length <= 8
    -10 <= nums[i] <= 10

"""

class Solution:
    def permuteUnique(self, nums: List[int]) -> List[List[int]]:

        nums.sort()
        n = len(nums)
        used = [False] * n
        current = []
        result = []

        def backtrack():
            if len(current) == n:
                result.append(current[:])
                return
            for i in range(n):
                if used[i]:
                    continue
                if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                    continue
                used[i] = True
                current.append(nums[i])
                backtrack()
                current.pop()
                used[i] = False

        backtrack()
        return result















    