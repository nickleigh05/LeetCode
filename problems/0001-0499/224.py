"""

224. Basic Calculator

Hard

Given a string s representing a valid expression, implement a basic calculator to evaluate it, and return the result of the evaluation.

Note: You are not allowed to use any built-in function which evaluates strings as mathematical expressions, such as eval().

Example 1:

    Input: s = "1 + 1"
    Output: 2

Example 2:

    Input: s = " 2-1 + 2 "
    Output: 3

Example 3:

    Input: s = "(1+(4+5+2)-3)+(6+8)"
    Output: 23

Constraints:

    1 <= s.length <= 3 * 10^5
    s consists of digits, '+', '-', '(', ')', and ' '.

    s represents a valid expression.
    '+' is not used as a unary operation (i.e., "+1" and "+(2 + 3)" is invalid).

    '-' could be used as a unary operation (i.e., "-1" and "-(2 + 3)" is valid).
    There will be no two consecutive operators in the input.

    Every number and running calculation will fit in a signed 32-bit integer.

"""

class Solution:
    def calculate(self, s: str) -> int:

        stack = []
        result = 0
        num = 0
        sign = 1

        for ch in s:
            if ch.isdigit():
                num = num * 10 + int(ch)

            elif ch == '+':
                result += sign * num
                num = 0
                sign = 1

            elif ch == '-':
                result += sign * num
                num = 0
                sign = -1

            elif ch == '(':
                stack.append(result)
                stack.append(sign)
                result = 0
                sign = 1

            elif ch == ')':
                result += sign * num
                num = 0
                result *= stack.pop()
                result += stack.pop()

        return result + sign * num
























    