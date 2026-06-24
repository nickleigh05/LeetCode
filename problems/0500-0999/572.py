"""

572. Subtree of Another Tree

Easy

Given the roots of two binary trees root and subRoot, return true if there is a subtree of root with the same structure and node values of subRoot and false otherwise.

A subtree of a binary tree tree is a tree that consists of a node in tree and all of this node's descendants. The tree tree could also be considered as a subtree of itself.

Example 1:

      root
        3
       / \       subroot
      4   5         4
     / \           / \  
    1   2         1   2

    Input: root = [3,4,5,1,2], subRoot = [4,1,2]
    Output: true

Example 2:

      root
        3
       / \       subroot
      4   5         4
     / \           / \  
    1   2         1   2
       /
      0

    Input: root = [3,4,5,1,2,null,null,null,null,0], subRoot = [4,1,2]
    Output: false

Constraints:

    The number of nodes in the root tree is in the range [1, 2000].
    The number of nodes in the subRoot tree is in the range [1, 1000].
    -104 <= root.val <= 104
    -104 <= subRoot.val <= 104

"""

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        
        def sameTree(p, q):
            if not p and not q:
                return True
            if not p or not q or p.val != q.val:
                return False
            return sameTree(p.left, q.left) and sameTree(p.right, q.right)

        if not root:
            return subRoot is None
        if sameTree(root, subRoot):
            return True
        return self.isSubtree(root.left, subRoot) or self.isSubtree(root.right, subRoot)
    







### serialize both trees & with delimiters ###

class Solution:
    def isSubtree(self, root, subRoot):
        def serialize(node):
            if not node:
                return "#"
            return f"^{node.val},{serialize(node.left)},{serialize(node.right)}"

        return serialize(subRoot) in serialize(root)
    








