"""

1020. Number of Enclaves

Medium

You are given an m x n binary matrix grid, where 0 represents a sea cell and 1 represents a land cell.

A move consists of walking from one land cell to another adjacent (4-directionally) land cell or walking off the boundary of the grid.

Return the number of land cells in grid for which we cannot walk off the boundary of the grid in any number of moves.

Example 1:

    Input: grid = [[0,0,0,0],[1,0,1,0],[0,1,1,0],[0,0,0,0]]
    Output: 3
    Explanation: There are three 1s that are enclosed by 0s, and one 1 that is not enclosed because its on the boundary.

Example 2:

    Input: grid = [[0,1,1,0],[0,0,1,0],[0,0,1,0],[0,0,0,0]]
    Output: 0
    Explanation: All 1s are either on the boundary or can reach the boundary.

Constraints:

    m == grid.length
    n == grid[i].length
    1 <= m, n <= 500
    grid[i][j] is either 0 or 1.

"""

class Solution:
    def numEnclaves(self, grid: List[List[int]]) -> int:

        rows = len(grid)
        cols = len(grid[0])
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        stack = []

        for r in range(rows):
            for c in range(cols):
                if (r == 0 or r == rows - 1 or c == 0 or c == cols - 1) and grid[r][c] == 1:
                    grid[r][c] = 0
                    stack.append((r, c))

        while stack:
            r, c = stack.pop()
            for dr, dc in directions:
                nr = r + dr
                nc = c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 0
                    stack.append((nr, nc))

        count = 0
        for r in range(rows):
            for c in range(cols):
                count += grid[r][c]
        return count













    