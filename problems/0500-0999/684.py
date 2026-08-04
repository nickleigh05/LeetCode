"""

684. Redundant Connection

Medium

In this problem, a tree is an undirected graph that is connected and has no cycles.
You are given a graph that started as a tree with n nodes labeled from 1 to n, with 
one additional edge added. The added edge has two different vertices chosen from 1 
to n, and was not an edge that already existed. The graph is represented as an array 
edges of length n where edges[i] = [ai, bi] indicates that there is an edge between 
nodes ai and bi in the graph. Return an edge that can be removed so that the resulting
graph is a tree of n nodes. If there are multiple answers, return the answer that occurs 
last in the input.

Example 1:

  ( 1 )-------( 2 )
    |       /
    |     /
    |   /
  ( 3 )

    Input: edges = [[1,2],[1,3],[2,3]]
    Output: [2,3]

Example 2:

  ( 2 )-------( 1 )-------( 5 )
    |           |
    |           |
    |           |
  ( 3 )-------( 4 )

    Input: edges = [[1,2],[2,3],[3,4],[1,4],[1,5]]
    Output: [1,4]

Constraints:

    n == edges.length
    3 <= n <= 1000
    edges[i].length == 2
    1 <= ai < bi <= edges.length
    ai != bi
    There are no repeated edges.
    The given graph is connected.

"""

class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        
        n = len(edges)
        parent = list(range(n + 1))
        rank = [0] * (n + 1)

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(x, y):
            rootX = find(x)
            rootY = find(y)
            if rootX == rootY:
                return False
            if rank[rootX] < rank[rootY]:
                parent[rootX] = rootY
            elif rank[rootX] > rank[rootY]:
                parent[rootY] = rootX
            else:
                parent[rootY] = rootX
                rank[rootX] += 1
            return True

        result = []
        for edge in edges:
            node1 = edge[0]
            node2 = edge[1]
            if not union(node1, node2):
                result = edge

        return result