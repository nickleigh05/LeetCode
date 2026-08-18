"""

3726. Remove Zeros in Decimal Representation

Easy

You are given a positive integer n.
Return the integer obtained by removing all zeros from the decimal representation of n.

Example 1:

    Input: n = 1020030

    Output: 123

    Explanation:

    After removing all zeros from 1020030, we get 123.

Example 2:

    Input: n = 1

    Output: 1

    Explanation:

    1 has no zero in its decimal representation. Therefore, the answer is 1.

Constraints:

    1 <= n <= 1015

"""

### My original solution ###

class Solution:
    def removeZeros(self, n: int) -> int:
        
        result = []
        digits = str(n)
    
        for digit in digits:
            if digit != '0':
                result.append(digit)
        return int("".join(result))







### Alternative solutions ###

class Solution:
    def removeZeros(self, n: int) -> int:
        result = 0
        place = 1
        
        while n > 0:
            digit = n % 10
            if digit != 0:
                result += digit * place
                place *= 10
            n //= 10
            
        return result








### One liner ###

class Solution:
    def removeZeros(self, n: int) -> int:
        return int(str(n).replace("0", ""))







        