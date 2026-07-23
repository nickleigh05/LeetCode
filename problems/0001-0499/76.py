"""

76. Minimum Window Substring

Hard

Given two strings s and t of lengths m and n respectively, return the minimum window substring of s 
such that every character in t (including duplicates) is included in the window. If there is no such 
substring, return the empty string "".

substring - A substring is a contiguous non-empty sequence of characters within a string.

The testcases will be generated such that the answer is unique.

Example 1:

    Input: s = "ADOBECODEBANC", t = "ABC"
    Output: "BANC"
    Explanation: The minimum window substring "BANC" includes 'A', 'B', and 'C' from string t.

Example 2:

    Input: s = "a", t = "a"
    Output: "a"
    Explanation: The entire string s is the minimum window.

Example 3:

    Input: s = "a", t = "aa"
    Output: ""
    Explanation: Both 'a's from t must be included in the window.
    Since the largest window of s only has one 'a', return empty string.

Constraints:

    m == s.length
    n == t.length
    1 <= m, n <= 105
    s and t consist of uppercase and lowercase English letters.

Follow up: Could you find an algorithm that runs in O(m + n) time?

"""

class Solution:
    def minWindow(self, s: str, t: str) -> str:
        
        if not s or not t:
            return ""

        need = {}
        for ch in t:
            need[ch] = need.get(ch, 0) + 1

        required = len(need)
        formed = 0
        window_counts = {}

        best_len = float("inf")
        best_left = 0
        best_right = 0

        left = 0
        for right in range(len(s)):
            ch = s[right]
            window_counts[ch] = window_counts.get(ch, 0) + 1

            if ch in need and window_counts[ch] == need[ch]:
                formed += 1

            while formed == required:
                window_len = right - left + 1
                if window_len < best_len:
                    best_len = window_len
                    best_left = left
                    best_right = right

                left_ch = s[left]
                window_counts[left_ch] -= 1
                if left_ch in need and window_counts[left_ch] < need[left_ch]:
                    formed -= 1

                left += 1

        if best_len == float("inf"):
            return ""

        return s[best_left:best_right + 1]
    










