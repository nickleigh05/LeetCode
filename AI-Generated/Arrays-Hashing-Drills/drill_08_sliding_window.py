"""
DRILL 08: Advanced - Sliding Window with Hashing

Concept: Combining sliding window technique with hash maps

Problem: Longest Substring Without Repeating Characters
Given a string s, find the length of the longest substring without
repeating characters.

Example 1:
Input: s = "abcabcbb"
Output: 3
Explanation: "abc" is the longest substring without repeating characters.

Example 2:
Input: s = "bbbbb"
Output: 1
Explanation: "b" is the longest.

Example 3:
Input: s = "pwwkew"
Output: 3
Explanation: "wke" is the longest.

Example 4:
Input: s = ""
Output: 0

Constraints:
- 0 <= len(s) <= 5 * 10^4
- s consists of English letters, digits, symbols and spaces

Target Complexity:
Time: O(n)
Space: O(min(m, n)) where m is charset size

HINTS:
1. Use a hash map to store {character: last_seen_index}
2. Use two pointers: left (start of window) and right (current position)
3. When you see a repeated character, move left pointer past its last occurrence
4. Track the maximum window size seen
"""

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        # Your code here
        pass


# Test cases
def test_drill_08():
    solution = Solution()

    # Test case 1
    assert solution.lengthOfLongestSubstring("abcabcbb") == 3

    # Test case 2
    assert solution.lengthOfLongestSubstring("bbbbb") == 1

    # Test case 3
    assert solution.lengthOfLongestSubstring("pwwkew") == 3

    # Test case 4
    assert solution.lengthOfLongestSubstring("") == 0

    # Test case 5
    assert solution.lengthOfLongestSubstring("abcdef") == 6

    # Test case 6
    assert solution.lengthOfLongestSubstring("aab") == 2

    print("✓ All test cases passed!")

if __name__ == "__main__":
    test_drill_08()
