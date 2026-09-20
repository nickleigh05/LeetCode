"""

343. Integer Break

Medium

Given an integer n, break it into the sum of k positive integers, where k >= 2, and maximize the product of those integers.

Return the maximum product you can get.

Example 1:

    Input: n = 2
    Output: 1
    Explanation: 2 = 1 + 1, 1 x 1 = 1.

Example 2:

    Input: n = 10
    Output: 36
    Explanation: 10 = 3 + 3 + 4, 3 x 3 x 4 = 36.

Constraints:

    2 <= n <= 58

"""

class Solution:
    def integerBreak(self, n: int) -> int:

        if n <= 3:
            return n - 1

        q = n // 3
        r = n % 3

        if r == 0:
            return 3 ** q
        if r == 1:
            return 3 ** (q - 1) * 4
        return 3 ** q * 2

















    