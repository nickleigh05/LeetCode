"""

67. Add Binary

Easy

Given two binary strings a and b, return their sum as a binary string.

Example 1:

    Input: a = "11", b = "1"
    Output: "100"

Example 2:

    Input: a = "1010", b = "1011"
    Output: "10101"

Constraints:

    1 <= a.length, b.length <= 104
    a and b consist only of '0' or '1' characters.
    Each string does not contain leading zeros except for the zero itself.

"""

class Solution:
    def addBinary(self, a: str, b: str) -> str:

        i = len(a) - 1
        j = len(b) - 1
        carry = 0
        result_digits = []

        while i >= 0 or j >= 0 or carry > 0:
            digit_a = int(a[i]) if i >= 0 else 0
            digit_b = int(b[j]) if j >= 0 else 0

            total = digit_a + digit_b + carry
            current_digit = total % 2
            carry = total // 2

            result_digits.append(str(current_digit))

            i -= 1
            j -= 1

        result_digits.reverse()
        result = "".join(result_digits)
        return result
    













# Approach 2: lean on Python's arbitrary-precision int + built-in base conversion
class Solution:
    def addBinary(self, a: str, b: str) -> str:
        num_a = int(a, 2)
        num_b = int(b, 2)
        total = num_a + num_b
        result = bin(total)[2:]  # strip the "0b" prefix
        return result
    




# Approach 3: bitwise addition using XOR/AND, no + operator at all
class Solution:
    def addBinary(self, a: str, b: str) -> str:
        num_a = int(a, 2)
        num_b = int(b, 2)

        while num_b != 0:
            sum_without_carry = num_a ^ num_b
            carry = (num_a & num_b) << 1
            num_a = sum_without_carry
            num_b = carry

        result = bin(num_a)[2:]
        return result
    







