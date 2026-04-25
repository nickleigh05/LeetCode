"""

42. Trapping Rain Water

Hard

Given n non-negative integers representing an elevation map where the 
width of each bar is 1, compute how much water it can trap after raining.

Example 1:

    Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
    Output: 6
    Explanation: The above elevation map (black section) is represented by array [0,1,0,2,1,0,1,3,2,1,2,1]. In this case, 6 units of rain water (blue section) are being trapped.

Example 2:

    Input: height = [4,2,0,3,2,5]
    Output: 9

Constraints:

    n == height.length
    1 <= n <= 2 * 104
    0 <= height[i] <= 105

"""

class Solution:
    def trap(self, height: List[int]) -> int:

        left = 0
        right = len(height) - 1
        leftmax = height[left]
        rightmax = height[right]
        rain = 0

        while left < right:

                if leftmax < rightmax:
                    left += 1
                    leftmax = max(leftmax, height[left])

                    rain += leftmax - height[left]
                else:
                    right -= 1
                    rightmax = max(rightmax, height[right])
                    rain += rightmax - height[right]
                    
        return rain
    


















