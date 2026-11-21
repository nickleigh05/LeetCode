"""

179. Largest Number

Medium

Given a list of non-negative integers nums, arrange them such that they form the largest number and return it.

Since the result may be very large, so you need to return a string instead of an integer.

Example 1:

    Input: nums = [10,2]
    Output: "210"

Example 2:

    Input: nums = [3,30,34,5,9]
    Output: "9534330"

Constraints:

    1 <= nums.length <= 100
    0 <= nums[i] <= 10^9

"""

from functools import cmp_to_key

class Solution:
    def largestNumber(self, nums: list[int]) -> str:

        strs = []

        for n in nums:
            strs.append(str(n))

        def compare(a, b):
            if a + b > b + a:
                return -1
            if a + b < b + a:
                return 1
            return 0

        strs.sort(key=cmp_to_key(compare))

        if strs[0] == "0":
            return "0"

        return "".join(strs)














    









    