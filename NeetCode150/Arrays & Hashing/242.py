"""
242. Valid Anagram

Easy

Given two strings s and t, return true if t is an anagram of s, and false otherwise.

    Example 1:

    Input: s = "anagram", t = "nagaram"
    Output: true

    Example 2:

    Input: s = "rat", t = "car"
    Output: false

    Constraints:
    1 <= s.length, t.length <= 5 * 104
    s and t consist of lowercase English letters.
 
Follow up: What if the inputs contain Unicode characters? How would you adapt your solution to such a case?
"""

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        # Code solution below
        
        if len(s) != len(t):
            return False

        hashmap1 = {}
        hashmap2 = {}

        for i in range(len(s)):
            hashmap1[s[i]] = 1 + hashmap1.get(s[i], 0)
            hashmap2[t[i]] = 1 + hashmap2.get(t[i], 0)
        return hashmap1 == hashmap2 
    
# If the strings have different lengths, they can't be anagrams
# Return False immediately

# Creates an empty dictionary to count the frequency of each character in string s

# Creates an empty dictionary to count the frequency of each character in string t

# Loop through each index from 0 to the length of s (both strings have same length at this point)
#   For string s at index i:
#     hashmap1.get(s[i], 0) gets the current count of character s[i], or 0 if it doesn't exist yet
#     Add 1 to that count and store it back in hashmap1
#   For string t at index i:
#     hashmap2.get(t[i], 0) gets the current count of character t[i], or 0 if it doesn't exist yet
#     Add 1 to that count and store it back in hashmap2

# Compare the two hashmaps
# If they're equal (same characters with same frequencies), the strings are anagrams - return True
# Otherwise return False