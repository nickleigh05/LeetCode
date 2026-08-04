"""

131. Palindrome Partitioning

Medium

Given a string s, partition s such that every substring of the partition is a palindrome. Return all possible palindrome partitioning of s.

Substring: A substring is a contiguous non-empty sequence of characters within a string.
Palindrome: A palindrome is a string that reads the same forward and backward.

Example 1:

    Input: s = "aab"
    Output: [["a","a","b"],["aa","b"]]

Example 2:

    Input: s = "a"
    Output: [["a"]]

Constraints:

    1 <= s.length <= 16
    s contains only lowercase English letters.

"""

class Solution:
    def partition(self, s: str) -> List[List[str]]:

        result = []
        path = []
        n = len(s)

        def is_palindrome(left, right):
            while left < right:
                if s[left] != s[right]:
                    return False
                left += 1
                right -= 1
            return True

        def backtrack(start):
            if start == n:
                result.append(path[:])
                return
            end = start
            while end < n:
                if is_palindrome(start, end):
                    path.append(s[start:end + 1])
                    backtrack(end + 1)
                    path.pop()
                end += 1

        backtrack(0)
        return result












