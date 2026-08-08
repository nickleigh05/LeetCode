"""

329. Longest Increasing Path in a Matrix

Hard

Given an m x n integers matrix, return the length of the longest increasing path in matrix.
From each cell, you can either move in four directions: left, right, up, or down. You may not 
move diagonally or move outside the boundary (i.e., wrap-around is not allowed).

Example 1:

+---------+---------+---------+
|    9    |    9    |    4    |
+---------+---------+---------+
|    6    |    6    |    8    |
+---------+---------+---------+
|    2    |    1    |    1    |
+---------+---------+---------+

    Input: matrix = [[9,9,4],[6,6,8],[2,1,1]]
    Output: 4
    Explanation: The longest increasing path is [1, 2, 6, 9].

Example 2:

+---------+---------+---------+
|    3    |    4    |    5    |
+---------+---------+---------+
|    3    |    2    |    6    |
+---------+---------+---------+
|    2    |    2    |    1    |
+---------+---------+---------+

    Input: matrix = [[3,4,5],[3,2,6],[2,2,1]]
    Output: 4
    Explanation: The longest increasing path is [3, 4, 5, 6]. Moving diagonally is not allowed.

Example 3:

    Input: matrix = [[1]]
    Output: 1

Constraints:

    m == matrix.length
    n == matrix[i].length
    1 <= m, n <= 200
    0 <= matrix[i][j] <= 231 - 1

"""

class Solution:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:

        if not matrix or not matrix[0]:
            return 0

        rows = len(matrix)
        cols = len(matrix[0])
        cache = [[0] * cols for _ in range(rows)]

        def dfs(r, c):
            if cache[r][c] != 0:
                return cache[r][c]

            best = 1
            if r > 0 and matrix[r - 1][c] > matrix[r][c]:
                candidate = 1 + dfs(r - 1, c)
                if candidate > best:
                    best = candidate
            if r < rows - 1 and matrix[r + 1][c] > matrix[r][c]:
                candidate = 1 + dfs(r + 1, c)
                if candidate > best:
                    best = candidate
            if c > 0 and matrix[r][c - 1] > matrix[r][c]:
                candidate = 1 + dfs(r, c - 1)
                if candidate > best:
                    best = candidate
            if c < cols - 1 and matrix[r][c + 1] > matrix[r][c]:
                candidate = 1 + dfs(r, c + 1)
                if candidate > best:
                    best = candidate

            cache[r][c] = best
            return best

        result = 0
        for r in range(rows):
            for c in range(cols):
                length = dfs(r, c)
                if length > result:
                    result = length

        return result




