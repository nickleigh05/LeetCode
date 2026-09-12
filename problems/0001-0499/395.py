"""

395. Longest Substring with At Least K Repeating Characters

Medium

Given a string s and an integer k, return the length of the longest substring of s such that the frequency of each character in this substring is greater than or equal to k.

if no such substring exists, return 0.

Example 1:

    Input: s = "aaabb", k = 3
    Output: 3
    Explanation: The longest substring is "aaa", as 'a' is repeated 3 times.

Example 2:

    Input: s = "ababbc", k = 2
    Output: 5
    Explanation: The longest substring is "ababb", as 'a' is repeated 2 times and 'b' is repeated 3 times.

Constraints:

    1 <= s.length <= 104
    s consists of only lowercase English letters.
    1 <= k <= 105

"""

class Solution:
    def longestSubstring(self, s: str, k: int) -> int:

        if len(s) == 0:
            return 0

        counts = {}
        for ch in s:
            counts[ch] = counts.get(ch, 0) + 1

        for ch, count in counts.items():
            if count < k:
                parts = s.split(ch)
                best = 0
                for part in parts:
                    result = self.longestSubstring(part, k)
                    if result > best:
                        best = result
                return best

        return len(s)








    