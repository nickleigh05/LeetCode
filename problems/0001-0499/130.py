"""

130. Surrounded Regions

Medium

You are given an m x n matrix board containing letters 'X' and 'O', capture regions that are surrounded:

    Connect: A cell is connected to adjacent cells horizontally or vertically.
    Region: To form a region connect every 'O' cell.
    Surround: A region is surrounded if none of the 'O' cells in that region are on the edge of the board. Such regions are completely enclosed by 'X' cells.

To capture a surrounded region, replace all 'O's with 'X's in-place within the original board. You do not need to return anything.

Example 1:

    Input: board = [["X","X","X","X"],["X","O","O","X"],["X","X","O","X"],["X","O","X","X"]]

    Output: [["X","X","X","X"],["X","X","X","X"],["X","X","X","X"],["X","O","X","X"]]

Explanation:

    +---+---+---+---+       +---+---+---+---+
    | X | X | X | X |       | X | X | X | X |
    +---+---+---+---+       +---+---+---+---+
    | X | O | O | X |  ==>  | X | X | X | X |
    +---+---+---+---+       +---+---+---+---+
    | X | X | O | X |       | X | X | X | X |
    +---+---+---+---+       +---+---+---+---+
    | X | O | X | X |       | X | O | X | X |
    +---+---+---+---+       +---+---+---+---+

    In the above diagram, the bottom region is not captured because it is on the edge of the board and cannot be surrounded.

Example 2:

    Input: board = [["X"]]

    Output: [["X"]]

Constraints:

    m == board.length
    n == board[i].length
    1 <= m, n <= 200
    board[i][j] is 'X' or 'O'.

"""

class Solution:
    def solve(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """

        if not board:
            return

        rows = len(board)
        cols = len(board[0])

        def mark_safe(start_row, start_col):
            stack = [(start_row, start_col)]
            board[start_row][start_col] = "S"
            while stack:
                cell = stack.pop()
                row = cell[0]
                col = cell[1]
                if row > 0 and board[row - 1][col] == "O":
                    board[row - 1][col] = "S"
                    stack.append((row - 1, col))
                if row < rows - 1 and board[row + 1][col] == "O":
                    board[row + 1][col] = "S"
                    stack.append((row + 1, col))
                if col > 0 and board[row][col - 1] == "O":
                    board[row][col - 1] = "S"
                    stack.append((row, col - 1))
                if col < cols - 1 and board[row][col + 1] == "O":
                    board[row][col + 1] = "S"
                    stack.append((row, col + 1))

        for row in range(rows):
            if board[row][0] == "O":
                mark_safe(row, 0)
            if board[row][cols - 1] == "O":
                mark_safe(row, cols - 1)

        for col in range(cols):
            if board[0][col] == "O":
                mark_safe(0, col)
            if board[rows - 1][col] == "O":
                mark_safe(rows - 1, col)

        for row in range(rows):
            for col in range(cols):
                if board[row][col] == "O":
                    board[row][col] = "X"
                elif board[row][col] == "S":
                    board[row][col] = "O"















