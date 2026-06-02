"""

69. Sqrt(x)

Easy

Given a non-negative integer x, return the square root of x rounded down to the nearest integer. 
The returned integer should be non-negative as well.
You must not use any built-in exponent function or operator.

    For example, do not use pow(x, 0.5) in c++ or x ** 0.5 in python.

Example 1:

    Input: x = 4
    Output: 2
    Explanation: The square root of 4 is 2, so we return 2.

Example 2:

    Input: x = 8
    Output: 2
    Explanation: The square root of 8 is 2.82842..., and since we round it down to the nearest integer, 2 is returned.

Constraints:

    0 <= x <= 231 - 1

"""

class Solution:
    def mySqrt(self, x: int) -> int:
        
        left = 0 
        right = x 
        tmp = 0

        while left <= right:
            mid = (left + right) // 2

            if mid * mid == x:
                return mid
            elif mid * mid < x:
                result = mid
                left = mid + 1  
            else:
                right = mid - 1 
            
        return result 
    




### Newtons Method ###

class Solution:
    def mySqrt(self, x: int) -> int:
        if x < 2: return x
        
        guess = x // 2
        while guess * guess > x:
            # The Newton formula: (guess + x/guess) / 2
            guess = (guess + x // guess) // 2
            
        return guess

### Bit Manipulation ###

class Solution:
    def mySqrt(self, x: int) -> int:
        if x < 2:
            return x
        
        res = 0
        # We start at the highest possible bit for a 32-bit integer square root.
        # Since x is up to 2^31 - 1, the sqrt is at most ~46340.
        # The highest bit for that range is 2^15 (32768).
        bit = 1 << 15 
        
        while bit > 0:
            # Try to "set" the current bit in our result
            candidate = res | bit
            
            # If the square of the candidate is still within x, keep the bit
            if candidate * candidate <= x:
                res = candidate
            
            # Move to the next bit (divide by 2)
            bit >>= 1
            
        return res







