"""

43. Multiply Strings

Medium

Given two non-negative integers num1 and num2 represented as strings, return the product of num1 and num2, also represented as a string.

Note: You must not use any built-in BigInteger library or convert the inputs to integer directly.

Example 1:

    Input: num1 = "2", num2 = "3"
    Output: "6"

Example 2:

    Input: num1 = "123", num2 = "456"
    Output: "56088"

Constraints:

    1 <= num1.length, num2.length <= 200
    num1 and num2 consist of digits only.
    Both num1 and num2 do not contain any leading zero, except the number 0 itself.

"""

class Solution:
    def multiply(self, num1: str, num2: str) -> str:

        if num1 == "0" or num2 == "0":
            return "0"

        n1 = len(num1)
        n2 = len(num2)
        result = [0] * (n1 + n2)

        for i in range(n1 - 1, -1, -1):
            digit1 = ord(num1[i]) - ord('0')
            for j in range(n2 - 1, -1, -1):
                digit2 = ord(num2[j]) - ord('0')
                product = digit1 * digit2
                pos_low = i + j + 1
                pos_high = i + j
                total = product + result[pos_low]
                result[pos_low] = total % 10
                result[pos_high] += total // 10

        start = 0
        while start < len(result) - 1 and result[start] == 0:
            start += 1

        digits = result[start:]
        chars = []
        for d in digits:
            chars.append(chr(d + ord('0')))

        return "".join(chars)










