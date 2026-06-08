"""

567. Permutation in String

Medium

Given two strings s1 and s2, return true if s2 contains a of s1, or false otherwise.

In other words, return true if one of s1's permutations is the substring of s2.

Example 1:

    Input: s1 = "ab", s2 = "eidbaooo"
    Output: true
    Explanation: s2 contains one permutation of s1 ("ba").

Example 2:

    Input: s1 = "ab", s2 = "eidboaoo"
    Output: false

Constraints:

    1 <= s1.length, s2.length <= 104
    s1 and s2 consist of lowercase English letters.

"""

class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:

        if len(s1) > len(s2):
            return False

        s1_count = [0] * 26
        window  = [0] * 26

        for ch in s1:
            s1_count[ord(ch) - ord('a')] += 1

        for ch in s2[:len(s1)]:
            window[ord(ch) - ord('a')] += 1

        if s1_count == window:
            return True

        for right in range(len(s1), len(s2)):
            window[ord(s2[right])           - ord('a')] += 1
            window[ord(s2[right - len(s1)]) - ord('a')] -= 1

            if s1_count == window:
                return True

        return False
    









