"""

738. Monotone Increasing Digits

Medium

An integer has monotone increasing digits if and only if each pair of adjacent digits x and y satisfy x <= y.

Given an integer n, return the largest number that is less than or equal to n with monotone increasing digits.

Example 1:

    Input: n = 10
    Output: 9

Example 2:

    Input: n = 1234
    Output: 1234

Example 3:

    Input: n = 332
    Output: 299

Constraints:

    0 <= n <= 10^9

"""

class Solution:
    def monotoneIncreasingDigits(self, n: int) -> int:

        digits = list(str(n))
        marker = len(digits)

        i = len(digits) - 1
        while i > 0:
            if digits[i - 1] > digits[i]:
                digits[i - 1] = str(int(digits[i - 1]) - 1)
                marker = i
            i -= 1

        j = marker
        while j < len(digits):
            digits[j] = '9'
            j += 1

        return int("".join(digits))
























    