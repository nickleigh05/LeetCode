"""

212. Word Search II

Hard

Given an m x n board of characters and a list of strings words, return all words on the board.
Each word must be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once in a word.

Example 1:

+---+---+---+---+
| o | a | a | n |
+---+---+---+---+
| e | t | a | e |
+---+---+---+---+
| i | h | k | r |
+---+---+---+---+
| i | f | l | v |
+---+---+---+---+

    Input: board = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]], words = ["oath","pea","eat","rain"]
    Output: ["eat","oath"]

Example 2:

+---+---+
| a | b |
+---+---+
| c | d |
+---+---+

    Input: board = [["a","b"],["c","d"]], words = ["abcb"]
    Output: []

Constraints:

    m == board.length
    n == board[i].length
    1 <= m, n <= 12
    board[i][j] is a lowercase English letter.
    1 <= words.length <= 3 * 104
    1 <= words[i].length <= 10
    words[i] consists of lowercase English letters.
    All the strings of words are unique.

"""

class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None

class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:

        root = TrieNode()
        for word in words:
            node = root
            for ch in word:
                if ch not in node.children:
                    node.children[ch] = TrieNode()
                node = node.children[ch]
            node.word = word

        rows = len(board)
        cols = len(board[0])
        result = []

        def dfs(r, c, node):
            ch = board[r][c]
            if ch not in node.children:
                return

            nextNode = node.children[ch]
            if nextNode.word is not None:
                result.append(nextNode.word)
                nextNode.word = None

            board[r][c] = "#"

            if r > 0:
                dfs(r - 1, c, nextNode)
            if r + 1 < rows:
                dfs(r + 1, c, nextNode)
            if c > 0:
                dfs(r, c - 1, nextNode)
            if c + 1 < cols:
                dfs(r, c + 1, nextNode)

            board[r][c] = ch

            if not nextNode.children:
                del node.children[ch]

        for r in range(rows):
            for c in range(cols):
                dfs(r, c, root)

        return result









