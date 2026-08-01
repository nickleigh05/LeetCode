"""

5. Longest Palindromic Substring

Medium

Given a string s, return the longest palindromic substring in s.

Palindromic : A string is palindromic if it reads the same forward and backward.

Example 1:

    Input: s = "babad"
    Output: "bab"
    Explanation: "aba" is also a valid answer.

Example 2:

    Input: s = "cbbd"
    Output: "bb"

Constraints:

    1 <= s.length <= 1000
    s consist of only digits and English letters.

"""

class Solution:
    def longestPalindrome(self, s: str) -> str:
        if len(s) < 1:
            return ""

        self.start = 0
        self.maxLength = 1

        for i in range(len(s)):
            self.expandAroundCenter(s, i, i)
            self.expandAroundCenter(s, i, i + 1)

        return s[self.start:self.start + self.maxLength]

    def expandAroundCenter(self, s, left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1

        currentLength = right - left - 1
        if currentLength > self.maxLength:
            self.maxLength = currentLength
            self.start = left + 1


















