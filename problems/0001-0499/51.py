"""

51. N-Queens

Hard

The n-queens puzzle is the problem of placing n queens on an n x n chessboard such that no two queens attack each other.
Given an integer n, return all distinct solutions to the n-queens puzzle. You may return the answer in any order.
Each solution contains a distinct board configuration of the n-queens' placement, where 'Q' and '.' both indicate a queen and an empty space, respectively.

Example 1:

+---+---+---+---+       +---+---+---+---+
| . | Q | . | . |       | . | . | Q | . |
+---+---+---+---+       +---+---+---+---+
| . | . | . | Q |       | Q | . | . | . |
+---+---+---+---+       +---+---+---+---+
| Q | . | . | . |       | . | . | . | Q |
+---+---+---+---+       +---+---+---+---+
| . | . | Q | . |       | . | Q | . | . |
+---+---+---+---+       +---+---+---+---+

    Input: n = 4
    Output: [[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]
    Explanation: There exist two distinct solutions to the 4-queens puzzle as shown above

Example 2:

    Input: n = 1
    Output: [["Q"]]

Constraints:

    1 <= n <= 9

"""

class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:

        results = []
        cols = set()
        diag1 = set()
        diag2 = set()
        board = []
        for i in range(n):
            board.append(["."] * n)

        def backtrack(row):
            if row == n:
                solution = []
                for r in range(n):
                    solution.append("".join(board[r]))
                results.append(solution)
                return

            for col in range(n):
                if col in cols:
                    continue
                if (row - col) in diag1:
                    continue
                if (row + col) in diag2:
                    continue

                cols.add(col)
                diag1.add(row - col)
                diag2.add(row + col)
                board[row][col] = "Q"

                backtrack(row + 1)

                cols.remove(col)
                diag1.remove(row - col)
                diag2.remove(row + col)
                board[row][col] = "."

        backtrack(0)
        return results











