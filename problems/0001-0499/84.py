"""

84. Largest Rectangle in Histogram

Hard

Given an array of integers heights representing the histogram's bar height where the width of each bar is 1, 
return the area of the largest rectangle in the histogram.

Example 1:

    Input: heights = [2,1,5,6,2,3]
    Output: 10
    Explanation: The above is a histogram where width of each bar is 1.
    The largest rectangle is shown in the red area, which has an area = 10 units.

Example 2:

    Input: heights = [2,4]
    Output: 4

Constraints:

    1 <= heights.length <= 105
    0 <= heights[i] <= 104

"""

class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
                
        stack = []
        max_area = 0
        n = len(heights)

        for i in range(n + 1):
            current_height = heights[i] if i < n else 0

            while stack and heights[stack[-1]] > current_height:
                top_index = stack.pop()
                height = heights[top_index]
                if stack:
                    width = i - stack[-1] - 1
                else:
                    width = i
                area = height * width
                if area > max_area:
                    max_area = area

            stack.append(i)

        return max_area
    











