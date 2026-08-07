"""

297. Serialize and Deserialize Binary Tree

Hard

Serialization is the process of converting a data structure or object into a sequence of bits so that it can be stored in a file or memory buffer, or transmitted across a network connection link to be reconstructed later in the same or another computer environment.
Design an algorithm to serialize and deserialize a binary tree. There is no restriction on how your serialization/deserialization algorithm should work. You just need to ensure that a binary tree can be serialized to a string and this string can be deserialized to the original tree structure.
Clarification: The input/output format is the same as how LeetCode serializes a binary tree. You do not necessarily need to follow this format, so please be creative and come up with different approaches yourself.

Example 1:

       (1)
      /   \
    (2)   (3)
          /   \
        (4)   (5)

    Input: root = [1,2,3,null,null,4,5]
    Output: [1,2,3,null,null,4,5]

Example 2:

    Input: root = []
    Output: []

Constraints:

    The number of nodes in the tree is in the range [0, 104].
    -1000 <= Node.val <= 1000

"""

# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Codec:

    def serialize(self, root):
        """Encodes a tree to a single string.

        :type root: TreeNode
        :rtype: str
        """
        values = []
        self._serializeHelper(root, values)
        return ",".join(values)

    def _serializeHelper(self, node, values):
        if node is None:
            values.append("#")
            return
        values.append(str(node.val))
        self._serializeHelper(node.left, values)
        self._serializeHelper(node.right, values)

    def deserialize(self, data):
        """Decodes your encoded data to tree.

        :type data: str
        :rtype: TreeNode
        """
        values = data.split(",")
        self.index = 0
        return self._deserializeHelper(values)

    def _deserializeHelper(self, values):
        value = values[self.index]
        self.index += 1
        if value == "#":
            return None
        node = TreeNode(int(value))
        node.left = self._deserializeHelper(values)
        node.right = self._deserializeHelper(values)
        return node
        

# Your Codec object will be instantiated and called as such:
# ser = Codec()
# deser = Codec()
# ans = deser.deserialize(ser.serialize(root))














