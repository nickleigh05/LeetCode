"""

132. Palindrome Partitioning II

Hard

Given a string s, partition s such that every substring of the partition is a palindrome.

Return the minimum cuts needed for a palindrome partitioning of s.

Example 1:

    Input: s = "aab"
    Output: 1
    Explanation: The palindrome partitioning ["aa","b"] could be produced using 1 cut.

Example 2:

    Input: s = "a"
    Output: 0

Example 3:

    Input: s = "ab"
    Output: 1

Constraints:

    1 <= s.length <= 2000
    s consists of lowercase English letters only.

"""

class Solution:
    def minCut(self, s: str) -> int:

        n = len(s)
        cuts = list(range(-1, n))

        for center in range(n):
            l = center
            r = center
            while l >= 0 and r < n and s[l] == s[r]:
                cuts[r + 1] = min(cuts[r + 1], cuts[l] + 1)
                l -= 1
                r += 1

            l = center
            r = center + 1
            while l >= 0 and r < n and s[l] == s[r]:
                cuts[r + 1] = min(cuts[r + 1], cuts[l] + 1)
                l -= 1
                r += 1

        return cuts[n]














    