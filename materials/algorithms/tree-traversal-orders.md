# Tree Traversal Orders

```python
def preorder(node):    # node, left, right
    if not node: return
    visit(node)
    preorder(node.left)
    preorder(node.right)

def inorder(node):      # left, node, right
    if not node: return
    inorder(node.left)
    visit(node)
    inorder(node.right)

def postorder(node):     # left, right, node
    if not node: return
    postorder(node.left)
    postorder(node.right)
    visit(node)
```

Three orders for visiting every node in a [binary tree](../data-structures/binary-tree.md), all just [DFS](dfs.md) with the "visit" step moved to a different position. **Inorder** on a [BST](../data-structures/binary-search-tree.md) visits values in sorted order. **Postorder** is the right choice whenever a node's answer depends on its children's answers first (e.g. computing subtree height/sum bottom-up).

**Complexity:** O(n) time to visit every node, O(h) space for the recursion stack (h = tree height).

**Related:** [dfs](dfs.md) · [binary-tree (data-structures)](../data-structures/binary-tree.md) · [recursion-basics (syntax)](../syntax/recursion-basics.md)
