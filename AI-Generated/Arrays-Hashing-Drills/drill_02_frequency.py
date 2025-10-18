"""
DRILL 02: Hash Map for Frequency Counting

Concept: Using hash maps to count occurrences

Problem: First Unique Character
Given a string s, find the first character that appears exactly once.
Return its index, or -1 if no such character exists.

Example 1:
Input: s = "leetcode"
Output: 0
Explanation: 'l' appears once and is at index 0.

Example 2:
Input: s = "loveleetcode"
Output: 2
Explanation: 'v' is the first character that appears once at index 2.

Example 3:
Input: s = "aabb"
Output: -1
Explanation: All characters appear more than once.

Constraints:
- 1 <= len(s) <= 10^5
- s consists of only lowercase English letters

Target Complexity:
Time: O(n)
Space: O(1) - at most 26 letters

HINTS:
1. Make two passes: first count frequencies, then find first unique
2. Use a hash map to store character frequencies
3. On second pass through string, check the frequency map
"""

class Solution:
    def firstUniqChar(self, s: str) -> int:
        # Your code here
        pass


# Test cases
def test_drill_02():
    solution = Solution()

    # Test case 1
    assert solution.firstUniqChar("leetcode") == 0

    # Test case 2
    assert solution.firstUniqChar("loveleetcode") == 2

    # Test case 3
    assert solution.firstUniqChar("aabb") == -1

    # Test case 4
    assert solution.firstUniqChar("z") == 0

    # Test case 5
    assert solution.firstUniqChar("aabbbcccc") == -1

    print("✓ All test cases passed!")

if __name__ == "__main__":
    test_drill_02()
