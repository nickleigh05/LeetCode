"""
DRILL 10: Challenge Problems

Concept: Combining multiple techniques

This drill contains 3 challenge problems that combine various array and hashing techniques.
Try to solve all three!

================================================================================
CHALLENGE 1: Top K Frequent Elements
================================================================================

Given an integer array nums and an integer k, return the k most frequent elements.
You may return the answer in any order.

Example 1:
Input: nums = [1,1,1,2,2,3], k = 2
Output: [1,2]

Example 2:
Input: nums = [1], k = 1
Output: [1]

Constraints:
- 1 <= len(nums) <= 10^5
- -10^4 <= nums[i] <= 10^4
- k is in range [1, number of unique elements]
- Answer is guaranteed to be unique

Target: O(n) time using bucket sort technique

HINTS:
1. Count frequencies with hash map
2. Create buckets where index = frequency
3. Iterate buckets from high to low frequency
"""

from typing import List
from collections import defaultdict

class Challenge1:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        # Your code here
        pass


"""
================================================================================
CHALLENGE 2: Longest Consecutive Sequence
================================================================================

Given an unsorted array of integers nums, return the length of the longest
consecutive elements sequence.

You must write an algorithm that runs in O(n) time.

Example 1:
Input: nums = [100,4,200,1,3,2]
Output: 4
Explanation: The longest consecutive sequence is [1, 2, 3, 4].

Example 2:
Input: nums = [0,3,7,2,5,8,4,6,0,1]
Output: 9
Explanation: [0,1,2,3,4,5,6,7,8]

Constraints:
- 0 <= len(nums) <= 10^5
- -10^9 <= nums[i] <= 10^9

HINTS:
1. Convert array to set for O(1) lookups
2. For each number, check if it's the start of a sequence (num-1 not in set)
3. If it's a start, count how long the sequence extends
4. Track the maximum length found
"""

class Challenge2:
    def longestConsecutive(self, nums: List[int]) -> int:
        # Your code here
        pass


"""
================================================================================
CHALLENGE 3: Valid Sudoku
================================================================================

Determine if a 9x9 Sudoku board is valid. Only the filled cells need to be
validated according to the following rules:
1. Each row must contain digits 1-9 without repetition
2. Each column must contain digits 1-9 without repetition
3. Each of the nine 3x3 sub-boxes must contain digits 1-9 without repetition

Note: Empty cells are represented by '.'

Example 1:
Input: board =
[["5","3",".",".","7",".",".",".","."]
,["6",".",".","1","9","5",".",".","."]
,[".","9","8",".",".",".",".","6","."]
,["8",".",".",".","6",".",".",".","3"]
,["4",".",".","8",".","3",".",".","1"]
,["7",".",".",".","2",".",".",".","6"]
,[".","6",".",".",".",".","2","8","."]
,[".",".",".","4","1","9",".",".","5"]
,[".",".",".",".","8",".",".","7","9"]]
Output: true

Constraints:
- board.length == 9
- board[i].length == 9
- board[i][j] is a digit 1-9 or '.'

HINTS:
1. Use three hash sets: rows, cols, boxes
2. For each cell, create unique keys for row, col, and box
3. Box index can be calculated as: (row // 3) * 3 + (col // 3)
4. Check if number already exists in any set before adding
"""

class Challenge3:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        # Your code here
        pass


# Test cases
def test_challenge_1():
    solution = Challenge1()
    result = solution.topKFrequent([1,1,1,2,2,3], 2)
    assert sorted(result) == [1, 2]
    print("✓ Challenge 1 passed!")

def test_challenge_2():
    solution = Challenge2()
    assert solution.longestConsecutive([100,4,200,1,3,2]) == 4
    assert solution.longestConsecutive([0,3,7,2,5,8,4,6,0,1]) == 9
    print("✓ Challenge 2 passed!")

def test_challenge_3():
    solution = Challenge3()
    board = [
        ["5","3",".",".","7",".",".",".","."],
        ["6",".",".","1","9","5",".",".","."],
        [".","9","8",".",".",".",".","6","."],
        ["8",".",".",".","6",".",".",".","3"],
        ["4",".",".","8",".","3",".",".","1"],
        ["7",".",".",".","2",".",".",".","6"],
        [".","6",".",".",".",".","2","8","."],
        [".",".",".","4","1","9",".",".","5"],
        [".",".",".",".","8",".",".","7","9"]
    ]
    assert solution.isValidSudoku(board) == True
    print("✓ Challenge 3 passed!")

if __name__ == "__main__":
    test_challenge_1()
    test_challenge_2()
    test_challenge_3()
    print("\n🎉 All challenges completed!")
