"""

1584. Min Cost to Connect All Points

Medium

You are given an array points representing integer coordinates of some points on a 2D-plane, where points[i] = [xi, yi].
The cost of connecting two points [xi, yi] and [xj, yj] is the manhattan distance between them: |xi - xj| + |yi - yj|, where |val| denotes the absolute value of val.
Return the minimum cost to make all points connected. All points are connected if there is exactly one simple path between any two points.

Example 1:

    Input: points = [[0,0],[2,2],[3,10],[5,2],[7,0]]
    Output: 20

Explanation: 

    We can connect the points as shown above to get the minimum cost of 20.
    Notice that there is a unique path between every pair of points.

Example 2:

    Input: points = [[3,12],[-2,5],[-4,1]]
    Output: 18

Constraints:

    1 <= points.length <= 1000
    -106 <= xi, yi <= 106
    All pairs (xi, yi) are distinct.

"""

class Solution:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:

        n = len(points)
        visited = [False] * n
        minEdge = [float('inf')] * n
        minEdge[0] = 0
        heap = [(0, 0)]
        totalCost = 0
        edgesUsed = 0

        while heap and edgesUsed < n:
            current = heapq.heappop(heap)
            cost = current[0]
            node = current[1]

            if visited[node]:
                continue

            visited[node] = True
            totalCost += cost
            edgesUsed += 1

            xi = points[node][0]
            yi = points[node][1]

            for next_node in range(n):
                if visited[next_node]:
                    continue

                xj = points[next_node][0]
                yj = points[next_node][1]
                dist = abs(xi - xj) + abs(yi - yj)

                if dist < minEdge[next_node]:
                    minEdge[next_node] = dist
                    heapq.heappush(heap, (dist, next_node))

        return totalCost







