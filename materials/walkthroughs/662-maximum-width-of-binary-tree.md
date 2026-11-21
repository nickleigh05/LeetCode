# 662. Maximum Width of Binary Tree

**Medium** · [LeetCode](https://leetcode.com/problems/maximum-width-of-binary-tree/) · [Solution file (no hints)](../../problems/0500-0999/662.py)

[📖 07. Trees lesson](../learning/07-trees.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 07. Trees problems](../rmap-practice/07-trees.md)

---

Given the `root` of a binary tree, return its **maximum width**: the largest width over all levels.

A level's **width** is the distance between its **leftmost and rightmost non-null nodes**, counting the `null` gaps between them **as if the tree were complete**.

```
            1
          /   \
         3     2
        / \     \
       5   3     9

→ 4     (level 3: 5, 3, null, 9 → positions 0..3, width 4)

            1
           / \
          3   2
         /     \
        5       9
       /         \
      6           7

→ 7     (level 4: 6, null, null, null, null, null, 7)
```

**Constraints:** `1 <= nodes <= 3000` · `-100 <= Node.val <= 100` · the answer fits in a **32-bit signed integer**

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| width **per level** | Look at the tree **level by level**, which points to BFS |
| leftmost to rightmost **non-null** | Gaps *between* real nodes count, but gaps outside them don't |
| "**as if** the tree were complete" | Give each node the position it *would* have in a complete tree, then subtract positions |
| answer fits in 32 bits | A hint that the raw positions might *not*. A deep, skinny tree makes them grow as 2^depth |

**The numbering trick.** Number positions like a heap stored in an array:

- The root is position `0`.
- A node at position `i` has its left child at `2i` and its right child at `2i + 1`.

Every node then gets the position it would have in a complete tree, gaps included. A level's width is just:

```
width = rightmost position − leftmost position + 1
```

You never need to store the `null`s. The numbers account for them.

**The overflow worry.** A tree that's 3000 nodes deep but only two nodes wide doubles its positions on every level, reaching about 2³⁰⁰⁰. Python's integers don't overflow, but huge numbers are slow, and in Java or C++ they'd break. The fix: **re-base each level** by subtracting the level's first position before computing the children. Width only depends on *differences*, so shifting every position on a level by the same amount changes nothing.

🤔 **Before you open the next section:** if a level's positions are `[12, 13, 15]`, what's its width, and what happens to it if you subtract 12 from each?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Fill in real `None` placeholders level by level | Add a placeholder for every missing child | Exponential | Exponential | ❌ Blows up on skinny trees |
| DFS with positions | Record the first position seen at each depth, compare as you go | O(n) | O(h) | ✅ Also fine |
| **BFS with positions** | Queue `(node, position)`, measure first and last on each level | **O(n)** | O(w) | ✅ Natural for "per level" |

**The decision: level-order [BFS](../algorithms/bfs.md) carrying positions**, using a [deque](../data-structures/deque.md).

BFS hands you each level as a contiguous chunk of the queue. At the start of a level, the queue holds exactly that level, so `queue[0]` is its leftmost node and `queue[-1]` its rightmost. That's one subtraction per level.

**The DFS alternative, briefly.** Recurse with `(node, depth, position)`. The first time you reach each depth, record its position as that depth's leftmost (DFS goes left first, so the first visit is the leftmost). At every node, compute `position − leftmost[depth] + 1` and keep the maximum. It's equally valid. BFS is just closer to the "per level" wording.

**Where the re-basing goes.** When you pop a node, subtract the level's first position from its index *before* computing its children. The children then start near 0, and the numbers stay small.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
best = 0
queue = deque([(root, 0)])
```

The root sits at position 0. Each queue entry is a `(node, position)` pair. The constraints guarantee at least one node, so `root` isn't `None`.
→ [deque-basics](../syntax/deque-basics.md) · [tuple-basics](../syntax/tuple-basics.md)

```python
while queue:
    level_size = len(queue)
    _, first = queue[0]
    _, last = queue[-1]
    best = max(best, last - first + 1)
```

**Measure the level before processing it.** At this moment the queue holds exactly one full level, in left-to-right order. Width is `last − first + 1`. `_` is the conventional name for a value you don't need, here the node.

`level_size` freezes the count, so the loop below processes only this level, even though children are added to the same queue.
→ [tuple-unpacking](../syntax/tuple-unpacking.md) · [min-max-key](../syntax/min-max-key.md) · [while-loop](../syntax/while-loop.md)

```python
    for _ in range(level_size):
        node, idx = queue.popleft()
        idx -= first
```

**Re-base.** Subtract the level's first position so this level runs from 0 upwards. Every position on the level shifts by the same amount, so widths are unchanged, and the numbers never grow huge.
→ [range-function](../syntax/range-function.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
        if node.left:
            queue.append((node.left, 2 * idx))
        if node.right:
            queue.append((node.right, 2 * idx + 1))
```

**Heap-style child positions.** Left is `2i`, right is `2i + 1`. Missing children are never queued. Their positions are skipped, which is exactly what counts the gaps.
→ [truthy-falsy-values](../syntax/truthy-falsy-values.md)

```python
return best
```

<details>
<summary>The whole thing together</summary>

```python
from collections import deque

class Solution:
    def widthOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        best = 0
        queue = deque([(root, 0)])

        while queue:
            level_size = len(queue)
            _, first = queue[0]
            _, last = queue[-1]
            best = max(best, last - first + 1)

            for _ in range(level_size):
                node, idx = queue.popleft()
                idx -= first
                if node.left:
                    queue.append((node.left, 2 * idx))
                if node.right:
                    queue.append((node.right, 2 * idx + 1))

        return best
```

</details>

**Trace it.** The first example:

| Level | Queue at start `(value, position)` | Width | Children queued (after re-basing) |
|---|---|---|---|
| 1 | (1, 0) | 0−0+1 = 1 | 3 → 0, 2 → 1 |
| 2 | (3, 0), (2, 1) | 1−0+1 = 2 | 5 → 0, 3 → 1, 9 → 3 |
| 3 | (5, 0), (3, 1), (9, 3) | 3−0+1 = **4** | none |

Answer **4** ✅. The missing left child of `2` is the gap at position 2. It's never queued, but the jump from 1 to 3 accounts for it.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).** Each node is enqueued and dequeued once, with O(1) work. Measuring a level is O(1), because it only peeks at the two ends of the deque.

**Why re-basing matters for time in Python.** Without it, a 3000-deep chain makes positions around 2³⁰⁰⁰, numbers about 900 digits long. Arithmetic on those isn't O(1). With re-basing, positions stay below about twice the level's width.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(w)</summary>

**O(w)**, where w is the largest number of real nodes on one level. The queue holds at most about two levels' worth of nodes. That's O(n) in the worst case (a complete tree's bottom level holds about n/2 nodes) and O(1) for a chain.

The DFS version uses O(h) for the recursion stack plus an array of leftmost positions per depth.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Width counts the gaps as if the tree were complete, so I'll give each node its heap position: root 0, children 2i and 2i+1. Then a level's width is last position minus first plus one. I do a level-order BFS carrying positions. At the start of each level the queue holds exactly that level, so I read the first and last positions straight off it. To keep the numbers small on deep, skinny trees, I subtract the level's first position before computing children. O(n) time, O(w) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why re-base?" | Positions double every level, so a deep chain reaches 2^depth. Differences are what matter, so shifting a level doesn't change its width. |
| "DFS version?" | Track `(depth, position)`. The first visit to a depth is its leftmost, since you go left first. Compare each node against that. |
| "Count only real nodes per level?" | Then it's just `len(queue)` at each level start, and no positions are needed. |
| "Is a tree complete?" | Number nodes the same way. It's complete if and only if the maximum position equals the node count minus one. |

**Traps:**

- **Counting real nodes instead of positions.** That gives 3, not 4, on the first example.
- **Measuring the level after the loop.** By then the queue holds the *next* level.
- **Re-basing with the wrong value.** Subtract the level's **first** position, not the parent's.
- **Filling in real `None` placeholders.** Exponential on a skinny tree.
- **Ignoring overflow in Java or C++.** Without re-basing, positions overflow 64 bits after about 63 levels.

**This same move shows up in:** [Binary Tree Level Order Traversal](102-binary-tree-level-order-traversal.md) (the level-by-level BFS loop) · [Binary Tree Right Side View](199-binary-tree-right-side-view.md) (reading the last node of each level) · [Binary Tree Zigzag Level Order Traversal](103-binary-tree-zigzag-level-order-traversal.md) (level BFS with a per-level twist) · [Kth Largest Element in an Array](215-kth-largest-element-in-an-array.md) (heap array indexing, where children of `i` live at fixed offsets).

</details>

---
