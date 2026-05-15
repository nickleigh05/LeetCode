"""

2160. Minimum Sum of Four Digit Number After Splitting Digits

Easy

You are given a positive integer num consisting of exactly four digits. Split num into two new integers new1 and new2 by using the digits found in num. Leading zeros are allowed in new1 and new2, and all the digits found in num must be used.

    For example, given num = 2932, you have the following digits: two 2's, one 9 and one 3. Some of the possible pairs [new1, new2] are [22, 93], [23, 92], [223, 9] and [2, 329].

Return the minimum possible sum of new1 and new2.

Example 1:

    Input: num = 2932
    Output: 52
    Explanation: Some possible pairs [new1, new2] are [29, 23], [223, 9], etc.
    The minimum sum can be obtained by the pair [29, 23]: 29 + 23 = 52.

Example 2:

    Input: num = 4009
    Output: 13
    Explanation: Some possible pairs [new1, new2] are [0, 49], [490, 0], etc. 
    The minimum sum can be obtained by the pair [4, 9]: 4 + 9 = 13.

Constraints:

    1000 <= num <= 9999

"""

class Solution:
    def minimumSum(self, num: int) -> int:
        
        n = sorted(str(num))

        new1 = int(n[0] + n[2])
        new2 = int(n[1] + n[3])

        return new1 + new2
    







### Other solutions ###

class Solution:
    def minimumSum(self, num: int) -> int:
        # Unpack the 4 sorted characters into 4 variables
        a, b, c, d = sorted(str(num))
        
        # a and b are the smallest, c and d are the largest
        return int(a + c) + int(b + d)
    




class Solution:
    def minimumSum(self, num: int) -> int:
        # Extract all 4 digits mathematically
        digits = []
        while num > 0:
            digits.append(num % 10)
            num //= 10
            
        # Sort the 4 integers
        digits.sort()
        
        # Combine them using place value math: (10 * tens) + ones
        # digits[0] and digits[1] are our tens places
        return (digits[0] * 10 + digits[2]) + (digits[1] * 10 + digits[3])
    




class Solution:
    def minimumSum(self, num: int) -> int:
        digits = []
        # Repeatedly split the last digit off mathematically
        for _ in range(4):
            num, digit = divmod(num, 10)
            digits.append(digit)
            
        digits.sort()
        return (digits[0] * 10 + digits[2]) + (digits[1] * 10 + digits[3])
    






