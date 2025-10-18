"""
DRILL 07: String Hashing Patterns

Concept: Applying hash maps to string problems

Problem: Group Anagrams
Given an array of strings, group all anagrams together.
An anagram is a word formed by rearranging letters of another word.

Example 1:
Input: strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
Output: [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
(Order doesn't matter)

Example 2:
Input: strs = [""]
Output: [[""]]

Example 3:
Input: strs = ["a"]
Output: [["a"]]

Constraints:
- 1 <= len(strs) <= 10^4
- 0 <= len(strs[i]) <= 100
- strs[i] consists of lowercase English letters

Target Complexity:
Time: O(n * k) where n is number of strings, k is max length
Space: O(n * k)

HINTS:
1. Anagrams have the same characters when sorted
2. Use sorted string as a key in hash map
3. Group strings that have the same sorted key
4. Alternative: use character frequency as key (more efficient)
"""

from typing import List
from collections import defaultdict

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        # Your code here
        pass


# Test cases
def test_drill_07():
    solution = Solution()

    # Test case 1
    result = solution.groupAnagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    # Sort each group and sort the list of groups for comparison
    result_sorted = sorted([sorted(group) for group in result])
    expected = sorted([sorted(["eat", "tea", "ate"]), sorted(["tan", "nat"]), sorted(["bat"])])
    assert result_sorted == expected

    # Test case 2
    result = solution.groupAnagrams([""])
    assert result == [[""]]

    # Test case 3
    result = solution.groupAnagrams(["a"])
    assert result == [["a"]]

    # Test case 4
    result = solution.groupAnagrams(["cab", "tin", "pew", "duh", "may", "ill", "buy", "bar", "max", "doc"])
    assert len(result) == 10  # All unique, no anagrams

    print("✓ All test cases passed!")

if __name__ == "__main__":
    test_drill_07()
