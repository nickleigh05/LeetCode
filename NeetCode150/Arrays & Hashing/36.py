"""
36. Valid Sudoku

Medium

Determine if a 9 x 9 Sudoku board is valid. Only the filled cells need to be validated according to the following rules:

Each row must contain the digits 1-9 without repetition.
Each column must contain the digits 1-9 without repetition.
Each of the nine 3 x 3 sub-boxes of the grid must contain the digits 1-9 without repetition.
Note:

A Sudoku board (partially filled) could be valid but is not necessarily solvable.
Only the filled cells need to be validated according to the mentioned rules.

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

    Example 2:

    Input: board = 
    [["8","3",".",".","7",".",".",".","."]
    ,["6",".",".","1","9","5",".",".","."]
    ,[".","9","8",".",".",".",".","6","."]
    ,["8",".",".",".","6",".",".",".","3"]
    ,["4",".",".","8",".","3",".",".","1"]
    ,["7",".",".",".","2",".",".",".","6"]
    ,[".","6",".",".",".",".","2","8","."]
    ,[".",".",".","4","1","9",".",".","5"]
    ,[".",".",".",".","8",".",".","7","9"]]

    Output: false

    Explanation: Same as Example 1, except with the 5 in the top left corner being modified to 8. Since there are two 8's in the top left 3x3 sub-box, it is invalid.

Constraints:

board.length == 9
board[i].length == 9
board[i][j] is a digit 1-9 or '.'.
"""

class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        # Code solution below
        
        cols = defaultdict(set)
        rows = defaultdict(set)
        squares = defaultdict(set)

        for r in range(9):
            for c in range(9):
                if board[r][c] == ".":
                    continue
                if ( board[r][c] in rows[r]
                    or board[r][c] in cols[c]
                    or board[r][c] in squares[(r // 3, c // 3)]):
                    return False

                cols[c].add(board[r][c])
                rows[r].add(board[r][c])
                squares[(r // 3, c // 3)].add(board[r][c])

        return True
            
"""
My thought process:

The question is asking me to validate if a 9x9 Sudoku board is valid according to three rules:
1. Each row must contain digits 1-9 without repetition
2. Each column must contain digits 1-9 without repetition  
3. Each 3x3 sub-box must contain digits 1-9 without repetition

cols = collections.defaultdict(set)     # track numbers in each column
rows = collections.defaultdict(set)     # track numbers in each row
squares = collections.defaultdict(set)  # track numbers in each 3x3 box

what is defaultdict(set)? It's a dictionary that automatically creates a new set when accessing a key that doesn't exist yet.

for r in range(9):                     # iterate through all rows (0-8)
    for c in range(9):                 # iterate through all columns (0-8)

if board[r][c] == ".":                 # skip empty cells
    continue

The key insight is using (r // 3, c // 3) to identify which 3x3 box a cell belongs to:
- Positions (0,0) to (2,2) belong to box (0,0)
- Positions (0,3) to (2,5) belong to box (0,1)
- And so on...

###########################################################################################   

Claude's thought process:

1. Problem Analysis:
   - Need to validate three constraints simultaneously
   - Only check filled cells (non-'.' cells)
   - Each constraint requires tracking seen digits
   - Return false immediately if any constraint violated

2. Approach Options:
   a) Three separate passes: Check rows, then columns, then boxes O(3n²)
   b) Single pass with tracking: Use sets to track seen digits O(n²)
   c) Brute force validation: Check each rule for each cell O(n⁴)

3. Optimal Solution (Single Pass with Sets):
   - Use three data structures to track seen digits
   - For each non-empty cell, check all three constraints
   - If any constraint violated, return false immediately
   - If all cells pass, return true

###########################################################################################   

Time complexity breakdown:

- Nested loops through 9x9 board: O(9²) = O(81) = O(1) constant time
- Set operations (lookup and insert): O(1) average case per operation
- Total: O(1) time complexity (since board size is fixed)

Space complexity: O(1) since we have at most 9 digits per row/column/box

Alternative approaches:
- Three separate passes: O(1) time, O(1) space
- Brute force: O(1) time but much slower constant factor
- Single pass approach: O(1) time, O(1) space (optimal)

###########################################################################################   

Code solution breakdown line by line with inline comments and explanations

class Solution:
    # Define a class called Solution (LeetCode requirement)
    
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        # Function signature:
        # - self: reference to the instance
        # - board: 9x9 2D list of strings (digits or '.')
        # - -> bool: returns True if valid, False otherwise
        
        cols = collections.defaultdict(set)
        # Dictionary to track digits seen in each column
        # Key: column index (0-8), Value: set of digits seen in that column
        # defaultdict(set) automatically creates empty set for new keys
        # Example: cols[0] = {'1', '5'} means column 0 has seen digits 1 and 5
        
        rows = collections.defaultdict(set)
        # Dictionary to track digits seen in each row
        # Key: row index (0-8), Value: set of digits seen in that row
        # Example: rows[0] = {'5', '3', '7'} means row 0 has seen digits 5, 3, and 7
        
        squares = collections.defaultdict(set)
        # Dictionary to track digits seen in each 3x3 sub-box
        # Key: tuple (box_row, box_col) where each is 0, 1, or 2
        # Value: set of digits seen in that 3x3 box
        # Example: squares[(0,0)] = {'5', '3', '6', '9', '8'} for top-left box
        
        for r in range(9):
            # Loop through all 9 rows of the sudoku board
            # r represents the current row index (0 to 8)
            
            for c in range(9):
                # Loop through all 9 columns for current row
                # c represents the current column index (0 to 8)
                # Together (r,c) gives us every cell in the 9x9 board
                
                if board[r][c] == ".":
                    # Skip empty cells - they don't need validation
                    # '.' represents an unfilled cell in the sudoku
                    continue
                
                if (board[r][c] in rows[r] or 
                    board[r][c] in cols[c] or 
                    board[r][c] in squares[(r // 3, c // 3)]):
                    # Check if current digit violates any of the three rules:
                    # 1. board[r][c] in rows[r]: digit already exists in this row
                    # 2. board[r][c] in cols[c]: digit already exists in this column  
                    # 3. board[r][c] in squares[(r//3, c//3)]: digit already exists in this 3x3 box
                    # 
                    # The key insight: (r//3, c//3) maps any cell to its 3x3 box:
                    # - Cells (0,0) to (2,2) map to box (0,0) - top-left
                    # - Cells (0,3) to (2,5) map to box (0,1) - top-middle
                    # - Cells (6,6) to (8,8) map to box (2,2) - bottom-right
                    
                    return False
                    # If any rule is violated, the sudoku is invalid
                    # Return False immediately - no need to check remaining cells
                
                cols[c].add(board[r][c])
                # Add current digit to the set of digits seen in this column
                # This tracks column constraint for future cells
                
                rows[r].add(board[r][c])
                # Add current digit to the set of digits seen in this row
                # This tracks row constraint for future cells
                
                squares[(r // 3, c // 3)].add(board[r][c])
                # Add current digit to the set of digits seen in this 3x3 box
                # This tracks 3x3 box constraint for future cells
        
        return True
        # If we've checked all cells without finding violations, sudoku is valid

# Example walkthrough with valid board:
# When we encounter '5' at position (0,0):
# - Check: '5' not in rows[0]={}, cols[0]={}, squares[(0,0)]={}  ✓
# - Add: rows[0]={'5'}, cols[0]={'5'}, squares[(0,0)]={'5'}
#
# When we encounter '3' at position (0,1):  
# - Check: '3' not in rows[0]={'5'}, cols[1]={}, squares[(0,0)]={'5'}  ✓
# - Add: rows[0]={'5','3'}, cols[1]={'3'}, squares[(0,0)]={'5','3'}
#
# If we later encounter '5' again in row 0, column 2:
# - Check: '5' IS in rows[0]={'5','3'}  ✗
# - Return False immediately - duplicate in same row violates sudoku rules

# 3x3 Box Mapping Examples:
# Position (0,0): box (0//3, 0//3) = (0,0) - top-left box
# Position (1,1): box (1//3, 1//3) = (0,0) - same top-left box  
# Position (4,5): box (4//3, 5//3) = (1,1) - center box
# Position (8,8): box (8//3, 8//3) = (2,2) - bottom-right box
"""