"""

1876. Substrings of Size Three with Distinct Characters

Easy

A string is good if there are no repeated characters.
Given a string s, return the number of good substrings of length three in s.
Note that if there are multiple occurrences of the same substring, every occurrence should be counted.
A substring is a contiguous sequence of characters in a string.

Example 1:

    Input: s = "xyzzaz"
    Output: 1
    Explanation: There are 4 substrings of size 3: "xyz", "yzz", "zza", and "zaz". 
    The only good substring of length 3 is "xyz".

Example 2:

    Input: s = "aababcabc"
    Output: 4
    Explanation: There are 7 substrings of size 3: "aab", "aba", "bab", "abc", "bca", "cab", and "abc".
    The good substrings are "abc", "bca", "cab", and "abc".

Constraints:

    1 <= s.length <= 100
    s consists of lowercase English letters.

"""

class Solution:
    def countGoodSubstrings(self, s: str) -> int:

        count = 0
        
        for i in range(len(s) - 2):
            a = s[i]
            b = s[i+1]
            c = s[i+2]
            if a != b and b != c and a != c:
                count += 1
        return count
















### More "sliding window" like ###
class Solution:
    def countGoodSubstrings(self, s: str) -> int:

        left = 0
        right = 2  # End of our fixed window of size 3
        count = 0
        
        while right < len(s):
            # Inspect all 3 characters currently inside the window
            a = s[left]
            b = s[left + 1]
            c = s[right]
            
            if a != b and b != c and a != c:
                count += 1
            
            # Slide the window forward by 1 step
            left += 1
            right += 1
            
        return count

















    