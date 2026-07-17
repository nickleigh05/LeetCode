"""

9. Palindrome Number

Easy

Given an integer x, return true if x is a palindrome, and false otherwise.

Palindrome - An integer is a palindrome when it reads the same forward and backward. For example, 121 is a palindrome while 123 is not.

Example 1:

    Input: x = 121
    Output: true
    Explanation: 121 reads as 121 from left to right and from right to left.

Example 2:

    Input: x = -121
    Output: false
    Explanation: From left to right, it reads -121. From right to left, it becomes 121-. Therefore it is not a palindrome.

Example 3:

    Input: x = 10
    Output: false
    Explanation: Reads 01 from right to left. Therefore it is not a palindrome.

Constraints:

    -231 <= x <= 231 - 1

Follow up: Could you solve it without converting the integer to a string?
 
"""

class Solution:
    def isPalindrome(self, x: int) -> bool:
        
        if x < 0:
            return False
        if x != 0 and x % 10 == 0:
            return False

        original = x
        reversed_num = 0
        while x > 0:
            digit = x % 10
            reversed_num = reversed_num * 10 + digit
            x = x // 10

        return original == reversed_num

















