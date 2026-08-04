"""

79. Word Search

Medium

Given an m x n grid of characters board and a string word, return true if word exists in the grid.
The word can be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once.

Example 1:

+---+---+---+---+
|(A)|(B)|(C)| E |
+---+---+---+---+
| S | F |(C)| S |
+---+---+---+---+
| A |(D)|(E)| E |
+---+---+---+---+

    Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCCED"
    Output: true

Example 2:

+---+---+---+---+
| A | B | C | E |
+---+---+---+---+
| S | F | C |(S)|
+---+---+---+---+
| A | D |(E)|(E)|
+---+---+---+---+

    Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "SEE"
    Output: true

Example 3:

+---+---+---+---+
| A | B | C | E |
+---+---+---+---+
| S | F | C | S |
+---+---+---+---+
| A | D | E | E |
+---+---+---+---+

    Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCB"
    Output: false

Constraints:

    m == board.length
    n = board[i].length
    1 <= m, n <= 6
    1 <= word.length <= 15
    board and word consists of only lowercase and uppercase English letters.

Follow up: Could you use search pruning to make your solution faster with a larger board?

"""

class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:

        rows = len(board)
        cols = len(board[0])

        def dfs(r, c, i):

            if i == len(word):
                return True
            if r < 0 or r >= rows or c < 0 or c >= cols:
                return False
            if board[r][c] != word[i]:
                return False

            temp = board[r][c]
            board[r][c] = "#"

            found = dfs(r + 1, c, i + 1)
            if not found:
                found = dfs(r - 1, c, i + 1)
            if not found:
                found = dfs(r, c + 1, i + 1)
            if not found:
                found = dfs(r, c - 1, i + 1)

            board[r][c] = temp
            return found

        for r in range(rows):
            for c in range(cols):
                if dfs(r, c, 0):
                    return True

        return False














    