"""

191. Number of 1 Bits

Easy

Given a positive integer n, write a function that returns the number of in its binary representation (also known as the Hamming weight).

Example 1:

    Input: n = 11

    Output: 3

Explanation:

    The input binary string 1011 has a total of three set bits.

Example 2:

    Input: n = 128

    Output: 1

Explanation:

    The input binary string 10000000 has a total of one set bit.

Example 3:

    Input: n = 2147483645

    Output: 30

Explanation:

    The input binary string 1111111111111111111111111111101 has a total of thirty set bits.

Constraints:

    1 <= n <= 231 - 1

Follow up: If this function is called many times, how would you optimize it?

"""

class Solution:
    def hammingWeight(self, n: int) -> int:
        
        count = 0

        while n > 0:
            count += n & 1
            n >>= 1 
        return count 







### one liner using built in function bin() ###

class Solution:
    def hammingWeight(self, n: int) -> int:
        
        return bin(n).count('1')
    


### Brian Kernighan’s Algorithm ###

class Solution:
    def hammingWeight(self, n: int) -> int:
        count = 0
        while n > 0:
            n &= n - 1  # Magic: clears the lowest 1-bit
            count += 1
        return count
    








