# 863. All Nodes Distance K in Binary Tree

**Medium** · [LeetCode](https://leetcode.com/problems/all-nodes-distance-k-in-binary-tree/) · [Solution file (no hints)](../../problems/0500-0999/863.py)

[📖 07. Trees lesson](../learning/07-trees.md) · [📖 11. Graphs lesson](../learning/11-graphs.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 07. Trees problems](../rmap-practice/07-trees.md)

---

Given the `root` of a binary tree, a `target` node in it, and an integer `k`, return the **values of all nodes at distance `k` from `target`**, in any order. Distance is the number of edges between two nodes.

```
            3
          /   \
         5     1
        / \   / \
       6   2 0   8
          / \
         7   4

target = 5, k = 2  →  [7, 4, 1]
```

`7` and `4` are two steps **down**. `1` is one step **up** (to 3) and one step **across** (to 1).

```
root = [1], target = 1, k = 3  →  []
```

**Constraints:** `1 <= nodes <= 500` · values are **unique** · `target` is a node in the tree · `0 <= k <= 1000`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| distance from `target`, not the root | You start in the **middle** of the tree |
| any node at distance k | Answers can be **below**, **above**, or **above and then down another branch** |
| binary tree nodes have only `left` and `right` | You can't move **up** without help |
| `k` up to 1000, 500 nodes | k can exceed the tree's size. Then the answer is simply `[]` |

**The core difficulty: trees only point downwards.** From `target = 5` you can reach 6, 2, 7 and 4 by following child pointers. But `1` is reached by going **up** to 3 and then down, and a `TreeNode` has no `parent` field.

**The fix: turn the tree into an undirected graph.** Record each node's parent in a dictionary with one DFS. Now every node has up to **three** neighbours: `left`, `right` and `parent`. Distance in the tree is distance in this graph.

**Then it's a plain BFS from `target`.** Expand ring by ring. The ring at distance k is the answer. You need a visited set, because the graph now has edges in both directions, and without one you'd bounce between a node and its parent forever.

🤔 **Before you open the next section:** once every node knows its parent, why does a BFS from `target` need a `visited` set when a normal tree traversal doesn't?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| **Parent map + BFS** | One DFS records parents; BFS from `target` over left/right/parent | **O(n)** | O(n) | ✅ Clearest |
| Build an adjacency list, then BFS | Convert the whole tree to `node → [neighbours]` | O(n) | O(n) | ✅ Same idea, more setup |
| Single DFS with distances | Return the distance to target from each subtree; collect "k − d" nodes in the other branch | O(n) | O(h) | ✅ Elegant, much harder to get right |

**The decision: a parent map, then [BFS](../algorithms/bfs.md).** It converts a [binary tree](../data-structures/binary-tree.md) problem into a [graph](../data-structures/graph.md) problem, which is the cleanest way to handle "moving up."

**Why BFS over DFS for the second phase?** BFS processes nodes in order of distance, so when you reach distance k, you've collected exactly the ring you want. You can also stop expanding from those nodes. DFS with a depth counter works too, but BFS matches "all nodes at distance k" directly.

**Use nodes as keys, not values.** Python objects are hashable by identity, so the parent map and the visited set can hold `TreeNode` objects directly. (Values are unique here, so values would also work, but nodes are the safer habit.)

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
parent = {}

def link_parents(node, par):
    if node is None:
        return
    parent[node] = par
    link_parents(node.left, node)
    link_parents(node.right, node)

link_parents(root, None)
```

**Phase 1: record every node's parent.** A preorder DFS passes each node's parent down to it. The root's parent is `None`. After this, `parent[node]` lets you move up from any node.
→ [dict-basics](../syntax/dict-basics.md) · [recursion-basics](../syntax/recursion-basics.md) · [closures](../syntax/closures.md)

```python
queue = deque([(target, 0)])
visited = {target}
result = []
```

**Phase 2: BFS from `target`.** Each queue entry is `(node, distance)`. `target` is visited from the start.
→ [deque-basics](../syntax/deque-basics.md) · [set-basics](../syntax/set-basics.md)

```python
while queue:
    node, dist = queue.popleft()
    if dist == k:
        result.append(node.val)
        continue
```

**Collect the ring at distance k.** A node at exactly k is an answer, and its neighbours would be at k + 1, so `continue` skips expanding it. This also means the BFS stops naturally once the k-th ring is drained.
→ [while-loop](../syntax/while-loop.md) · [break-continue](../syntax/break-continue.md) · [tuple-unpacking](../syntax/tuple-unpacking.md)

```python
    for nb in (node.left, node.right, parent[node]):
        if nb is not None and nb not in visited:
            visited.add(nb)
            queue.append((nb, dist + 1))
```

**Three neighbours: down-left, down-right, and up.** Skip missing ones (`None`) and ones already seen. Without `visited`, going up to the parent and back down to the child would loop forever.
→ [tuple-basics](../syntax/tuple-basics.md) · [identity-operators](../syntax/identity-operators.md) · [membership-operators](../syntax/membership-operators.md)

```python
return result
```

If k is bigger than any distance in the tree, the queue empties before reaching k, and `result` is `[]`.

<details>
<summary>The whole thing together</summary>

```python
from collections import deque

class Solution:
    def distanceK(self, root: TreeNode, target: TreeNode, k: int) -> List[int]:
        parent = {}

        def link_parents(node, par):
            if node is None:
                return
            parent[node] = par
            link_parents(node.left, node)
            link_parents(node.right, node)

        link_parents(root, None)

        queue = deque([(target, 0)])
        visited = {target}
        result = []

        while queue:
            node, dist = queue.popleft()
            if dist == k:
                result.append(node.val)
                continue
            for nb in (node.left, node.right, parent[node]):
                if nb is not None and nb not in visited:
                    visited.add(nb)
                    queue.append((nb, dist + 1))

        return result
```

</details>

**Trace it.** `target = 5`, `k = 2`:

| Distance | Nodes popped | Neighbours queued |
|---|---|---|
| 0 | 5 | 6, 2 (children), 3 (parent) |
| 1 | 6 | — (no children; parent 5 already visited) |
| 1 | 2 | 7, 4 |
| 1 | 3 | 1 (5 is visited, 3 has no parent) |
| 2 | 7, 4, 1 | collected, not expanded |

Result **`[7, 4, 1]`** ✅. `1` was reached by going **up** to 3 and then down, which needed the parent map.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

- Building the parent map visits every node once.
- The BFS visits each node at most once, because of `visited`, and checks three neighbours each.

Both phases are linear. The BFS often stops early, after the k-th ring.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n).**

- `parent`: one entry per node.
- `visited` and `queue`: up to n nodes.
- The DFS recursion stack: O(h). At 500 nodes, it's well under Python's recursion limit.

The single-DFS alternative avoids the parent map and uses O(h), but its logic is considerably harder to get right in an interview.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The answers can be above the target, and tree nodes can't move up, so I first do a DFS to record every node's parent. That turns the tree into an undirected graph where each node has up to three neighbours: left, right and parent. Then I BFS from the target with a visited set, since edges now go both ways. When I pop a node at distance k, I record it and don't expand it. O(n) time and space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Without the parent map?" | One DFS returning the distance from each subtree to target (or −1). When an ancestor is at distance d, collect nodes at depth k − d − 1 in its **other** subtree. O(h) space, but fiddly. |
| "Why not a regular tree traversal?" | Tree traversals only go down. The parent edge creates cycles (child ↔ parent), so you need `visited`. |
| "Nodes within distance k (≤ k)?" | Collect every node popped with `dist <= k`. |
| "Target given as a value, not a node?" | Find the node during the parent-map DFS. |
| "Amount of Time for Binary Tree to Be Infected?" | LeetCode 2385. The same parent map plus BFS, returning the number of rings. |

**Traps:**

- **Only searching downward from `target`.** You miss every answer above it, like `1` in the example.
- **No `visited` set.** Infinite loop between parent and child.
- **Expanding nodes at distance k.** Harmless but wasteful. `continue` stops it.
- **Assuming k ≤ height.** k can be 1000 on a 3-node tree. The queue just empties and you return `[]`.

**This same move shows up in:** [Binary Tree Level Order Traversal](102-binary-tree-level-order-traversal.md) (BFS rings on a tree) · [Clone Graph](133-clone-graph.md) (BFS with a visited map over node objects) · [Lowest Common Ancestor of a Binary Tree](236-lowest-common-ancestor-of-a-binary-tree.md) (reasoning about paths that go up then down) · [01 Matrix](542-01-matrix.md) (BFS distances in rings).

</details>

---
