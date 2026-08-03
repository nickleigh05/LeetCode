"""

7. Reverse Integer

Medium

Given a signed 32-bit integer x, return x with its digits reversed. If reversing x causes the value to go outside the signed 32-bit integer range [-2^31, 2^31 - 1], then return 0.

Assume the environment does not allow you to store 64-bit integers (signed or unsigned).

Example 1:

    Input: x = 123
    Output: 321

Example 2:

    Input: x = -123
    Output: -321

Example 3:

    Input: x = 120
    Output: 21

Constraints:

    -2^31 <= x <= 2^31 - 1

"""

class Solution:
    def reverse(self, x: int) -> int:

        INT_MIN = -2**31
        INT_MAX = 2**31 - 1

        sign = 1
        if x < 0:
            sign = -1
            x = -x

        result = 0
        while x != 0:
            digit = x % 10
            x = x // 10
            result = result * 10 + digit

        result = result * sign

        if result < INT_MIN or result > INT_MAX:
            return 0

        return result










