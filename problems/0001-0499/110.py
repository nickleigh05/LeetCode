"""

110. Balanced Binary Tree

Easy

Given a binary tree, determine if it is height balanced.

Example 1:

        3
       / \
      9   20
          / \
         15  7

    Input: root = [3,9,20,null,null,15,7]
    Output: true

Example 2:

            1
           / \
          2   2
         / \
        3   3
       / \ 
      4   4

    Input: root = [1,2,2,3,3,null,null,4,4]
    Output: false

Example 3:

    Input: root = []
    Output: true

Constraints:

    The number of nodes in the tree is in the range [0, 5000].
    -104 <= Node.val <= 104

"""

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        
        def height(node):
            if not node:
                return 0
            left = height(node.left)
            if left == -1:
                return -1
            right = height(node.right)
            if right == -1:
                return -1
            if abs(left - right) > 1:
                return -1
            return max(left, right) + 1

        return height(root) != -1
    










