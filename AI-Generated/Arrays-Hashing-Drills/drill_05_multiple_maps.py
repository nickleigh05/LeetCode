"""
DRILL 05: Multiple Hash Sets/Maps

Concept: Using multiple hash structures to track different properties

Problem: Intersection and Union
Given two integer arrays nums1 and nums2, return their intersection and union.
- Intersection: elements that appear in both arrays
- Union: all unique elements from both arrays

Each element should appear only once in the result.

Example 1:
Input: nums1 = [1, 2, 2, 1], nums2 = [2, 2]
Output:
  intersection = [2]
  union = [1, 2]

Example 2:
Input: nums1 = [4, 9, 5], nums2 = [9, 4, 9, 8, 4]
Output:
  intersection = [4, 9] or [9, 4]
  union = [4, 5, 8, 9] (any order)

Constraints:
- 1 <= len(nums1), len(nums2) <= 1000
- 0 <= nums1[i], nums2[i] <= 1000

Target Complexity:
Time: O(n + m) where n, m are lengths of arrays
Space: O(n + m)

HINTS:
1. Convert both arrays to sets
2. Use set operations: intersection (&) and union (|)
3. Alternative: iterate and check membership
"""

from typing import List, Tuple

class Solution:
    def intersectionAndUnion(self, nums1: List[int], nums2: List[int]) -> Tuple[List[int], List[int]]:
        """
        Returns (intersection, union) as tuple of lists
        """
        # Your code here
        pass


# Test cases
def test_drill_05():
    solution = Solution()

    # Test case 1
    intersection, union = solution.intersectionAndUnion([1, 2, 2, 1], [2, 2])
    assert sorted(intersection) == [2]
    assert sorted(union) == [1, 2]

    # Test case 2
    intersection, union = solution.intersectionAndUnion([4, 9, 5], [9, 4, 9, 8, 4])
    assert sorted(intersection) == [4, 9]
    assert sorted(union) == [4, 5, 8, 9]

    # Test case 3
    intersection, union = solution.intersectionAndUnion([1, 2, 3], [4, 5, 6])
    assert intersection == []
    assert sorted(union) == [1, 2, 3, 4, 5, 6]

    print("✓ All test cases passed!")

if __name__ == "__main__":
    test_drill_05()
