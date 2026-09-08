"""

1985. Find the Kth Largest Integer in the Array

Medium

You are given an array of strings nums and an integer k. Each string in nums represents an
integer without leading zeros.

Return the string that represents the kth largest integer in nums.

Note: Duplicate numbers should be counted distinctly. For example, if nums is ["1","2","2"],
"2" is the first largest integer, "2" is the second-largest integer, and "1" is the
third-largest integer.

Example 1:

    Input: nums = ["3","6","7","10"], k = 4
    Output: "3"

Example 2:

    Input: nums = ["2","21","12","1"], k = 3
    Output: "2"

Example 3:

    Input: nums = ["0","0"], k = 2
    Output: "0"

Constraints:

    1 <= k <= nums.length <= 10^4
    1 <= nums[i].length <= 100
    nums[i] consists of only digits.
    nums[i] will not have any leading zeros.

"""

class Solution:
    def kthLargestNumber(self, nums: List[str], k: int) -> str:

        n = len(nums)

        def compare(num1, num2):
            len1 = len(num1)
            len2 = len(num2)

            if len1 != len2:
                if len1 < len2:
                    return -1
                else:
                    return 1

            if num1 < num2:
                return -1
            elif num1 > num2:
                return 1
            else:
                return 0

        nums_sorted = sorted(nums, key=functools.cmp_to_key(compare))

        index = n - k
        result = nums_sorted[index]

        return result










### Alternative solution using built-in sorting with a custom key ###

    class Solution:
    def kthLargestNumber(self, nums: List[str], k: int) -> str:
        nums_sorted = sorted(nums, key=lambda x: (len(x), x))
        return nums_sorted[len(nums_sorted) - k]






    