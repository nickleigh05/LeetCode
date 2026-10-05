"""

149. Max Points on a Line

Hard

Given an array of points where points[i] = [xi, yi] represents a point on the X-Y plane, return the maximum number of points that lie on the same straight line.

Example 1:

    Input: points = [[1,1],[2,2],[3,3]]
    Output: 3

Example 2:

    Input: points = [[1,1],[3,2],[5,3],[4,1],[2,3],[1,4]]
    Output: 4

Constraints:

    1 <= points.length <= 300
    points[i].length == 2
    -10^4 <= xi, yi <= 10^4
    All the points are unique.

"""

class Solution:
    def maxPoints(self, points: List[List[int]]) -> int:

        n = len(points)
        if n <= 2:
            return n

        best = 0
        for i in range(n):
            slopes = defaultdict(int)
            local_best = 0
            x1 = points[i][0]
            y1 = points[i][1]
            for j in range(i + 1, n):
                dx = points[j][0] - x1
                dy = points[j][1] - y1
                g = gcd(dx, dy)
                dx = dx // g
                dy = dy // g

                if dx < 0:
                    dx = -dx
                    dy = -dy
                elif dx == 0:
                    dy = 1
                slopes[(dx, dy)] += 1
                if slopes[(dx, dy)] > local_best:
                    local_best = slopes[(dx, dy)]
            if local_best + 1 > best:
                best = local_best + 1

            if best > n - i - 1:
                break

        return best

















    