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
        
        if len(s) != len(t):
            return False
            
        smap = {}
        tmap = {}
        
        for i in range(len(s)):
            smap[s[i]] = 1 + smap.get(s[i], 0)
            tmap[t[i]] = 1 + tmap.get(t[i], 0)
        return smap == tmap