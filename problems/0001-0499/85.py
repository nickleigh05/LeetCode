"""

85. Maximal Rectangle

Hard

Given a rows x cols binary matrix filled with 0's and 1's, find the largest rectangle
containing only 1's and return its area.

Example 1:

    Input: matrix = [["1","0","1","0","0"],
                     ["1","0","1","1","1"],
                     ["1","1","1","1","1"],
                     ["1","0","0","1","0"]]
    Output: 6
    Explanation: The maximal rectangle is shown in the above picture.

Example 2:

    Input: matrix = [["0"]]
    Output: 0

Example 3:

    Input: matrix = [["1"]]
    Output: 1

Constraints:

    rows == matrix.length
    cols == matrix[i].length
    1 <= row, cols <= 200
    matrix[i][j] is '0' or '1'.

"""

class Solution:
    def maximalRectangle(self, matrix: List[List[str]]) -> int:

        if not matrix or not matrix[0]:
            return 0

        cols = len(matrix[0])
        heights = [0] * (cols + 1)
        max_area = 0

        for row in matrix:
            for i in range(cols):
                if row[i] == "1":
                    heights[i] += 1
                else:
                    heights[i] = 0

            stack = [-1]
            for i in range(cols + 1):
                while heights[i] < heights[stack[-1]]:
                    height = heights[stack.pop()]
                    width = i - stack[-1] - 1
                    area = height * width
                    if area > max_area:
                        max_area = area
                stack.append(i)

        return max_area









    