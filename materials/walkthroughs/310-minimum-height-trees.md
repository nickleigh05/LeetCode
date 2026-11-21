# 310. Minimum Height Trees

**Medium** · [LeetCode](https://leetcode.com/problems/minimum-height-trees/) · [Solution file (no hints)](../../problems/0001-0499/310.py)

[📖 11. Graphs lesson](../learning/11-graphs.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 11. Graphs problems](../rmap-practice/11-graphs.md)

---

A tree is an undirected graph in which any two nodes are connected by **exactly one** path. You're given a tree of `n` nodes labelled `0` to `n - 1` and a list of `n - 1` `edges`.

You can choose **any** node as the root. The tree's **height** is then the number of edges on the longest path from the root down to a leaf. Return **all** roots that give the **minimum height**, in any order.

```
n = 4, edges = [[1,0],[1,2],[1,3]]              →  [1]

        0                     1
        |                   / | \
        1          →       0  2  3     height 1
       / \
      2   3

n = 6, edges = [[3,0],[3,1],[3,2],[3,4],[5,4]]  →  [3, 4]
```

**Constraints:** `1 <= n <= 2·10⁴` · `edges.length == n - 1` · all pairs are distinct · the input is **guaranteed to be a tree**

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| guaranteed **tree** | Connected, no cycles, exactly n − 1 edges. You don't need a visited set to avoid loops |
| choose **any** node as root | You're comparing n candidate roots |
| height = longest root-to-leaf path | A root's height is its distance to the **farthest** node |
| return **all** minimum roots | There may be a tie. In fact the answer is always **1 or 2** nodes |
| n up to 2·10⁴ | BFS from every node is O(n²) = 4·10⁸. Too slow. Aim for O(n) |

**The brute force is clear but slow.** BFS from each node, measure the height, keep the minimum. That's n BFS runs of O(n) each.

**The insight: the best roots are in the middle.** A root's height is its distance to the farthest leaf. To make that small, you want a node that's central, as far from the edges as possible. The tree's **longest path** (its diameter) decides this. The best root sits in the middle of that path, and its height is about half the diameter.

- If the diameter has an **even** number of edges, there's one middle node.
- If it has an **odd** number of edges, there are two middle nodes, and both give the same height.

That's why the answer is always one or two nodes.

**How to find the middle without computing the diameter: peel the tree like an onion.** Remove every leaf at once. The leaves of what's left are one step further in. Keep peeling layer by layer, and the last one or two nodes standing are the centre. Every layer you remove takes one step off both ends of every longest path, so the middle is what survives.

🤔 **Before you open the next section:** when you remove a layer of leaves, how do you know which nodes have just *become* leaves?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| BFS from every node | Measure each root's height | O(n²) | O(n) | ❌ Too slow at 2·10⁴ |
| Find the diameter | Two BFS runs find the longest path, return its middle | O(n) | O(n) | ✅ Works, more bookkeeping |
| **Leaf trimming** | Repeatedly remove all current leaves until ≤ 2 nodes remain | **O(n)** | O(n) | ✅ Clean |

**The decision: layer-by-layer leaf trimming.** It's a variant of [topological sort](../algorithms/topological-sort.md) (Kahn's algorithm). Instead of in-degree 0, you're looking for **degree 1**, and you process a whole layer at a time.

**Why stop at 2, not 1?** If two adjacent nodes remain, they're both centres. Removing "both leaves" would leave nothing and lose the answer. Once `remaining ≤ 2`, whatever is left is the answer.

**Using sets for neighbours.** Each node's neighbours are kept in a [set](../data-structures/hashset.md), so removing a leaf from its neighbour's set is O(1). A leaf has exactly one neighbour, and `set.pop()` hands it to you directly.

**The special case.** `n == 1` has no edges, so no node has degree 1 and the loop never finds a leaf. Handle it up front: the only node is the answer.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
if n == 1:
    return [0]
```

A single node with no edges is its own minimum-height root. Without this check, `leaves` would start empty and the function would return `[]`.
→ [if-return](../syntax/if-return.md)

```python
neighbors = [set() for _ in range(n)]
for a, b in edges:
    neighbors[a].add(b)
    neighbors[b].add(a)
```

**An undirected adjacency list.** Each edge goes in both directions. A set's size is the node's **degree**, which is the number you'll be watching.

Use the comprehension. `[set()] * n` would share one set between every node.
→ [list-comprehension](../syntax/list-comprehension.md) · [set-basics](../syntax/set-basics.md) · [tuple-unpacking](../syntax/tuple-unpacking.md)

```python
leaves = [i for i in range(n) if len(neighbors[i]) == 1]
remaining = n
```

**The first layer.** Every node with degree 1 is a leaf. `remaining` tracks how many nodes are still in the tree.
→ [list-comprehension](../syntax/list-comprehension.md)

```python
while remaining > 2:
    remaining -= len(leaves)
    new_leaves = []
```

**Peel one layer.** Stop when two or fewer nodes remain, because those are the centres. Subtract the whole layer from `remaining` at the start, since every node in `leaves` is about to be removed.
→ [while-loop](../syntax/while-loop.md)

```python
    for leaf in leaves:
        nb = neighbors[leaf].pop()
        neighbors[nb].remove(leaf)
        if len(neighbors[nb]) == 1:
            new_leaves.append(nb)
    leaves = new_leaves
```

**Remove each leaf.** A leaf has exactly one neighbour, so `pop()` takes it from the set. Then remove the leaf from that neighbour's set too, which is the other half of the undirected edge.

If the neighbour's degree has dropped to **exactly 1**, it has just become a leaf of the smaller tree and joins the next layer. It's `== 1`, not `<= 1`, so a node is added to the next layer once, at the moment it becomes a leaf.
→ [set-operations](../syntax/set-operations.md) · [list-methods](../syntax/list-methods.md)

```python
return leaves
```

The last layer standing, with one or two nodes, is the answer.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]:
        if n == 1:
            return [0]

        neighbors = [set() for _ in range(n)]
        for a, b in edges:
            neighbors[a].add(b)
            neighbors[b].add(a)

        leaves = [i for i in range(n) if len(neighbors[i]) == 1]
        remaining = n

        while remaining > 2:
            remaining -= len(leaves)
            new_leaves = []
            for leaf in leaves:
                nb = neighbors[leaf].pop()
                neighbors[nb].remove(leaf)
                if len(neighbors[nb]) == 1:
                    new_leaves.append(nb)
            leaves = new_leaves

        return leaves
```

</details>

**Trace it.** `n = 6`, `edges = [[3,0],[3,1],[3,2],[3,4],[5,4]]`:

```
0   1   2
 \  |  /
    3 — 4 — 5
```

| Round | `leaves` | `remaining` after | Removed | New leaves |
|---|---|---|---|---|
| start | `[0, 1, 2, 5]` | 6 | — | — |
| 1 | `[0, 1, 2, 5]` | **2** | 0, 1, 2, 5 | 3 (degree 4→1), 4 (degree 2→1) |
| stop | `[3, 4]` | | `remaining == 2` | |

Answer **`[3, 4]`** ✅. Rooting at either gives height 2.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

- Building the adjacency sets: O(n), since there are n − 1 edges.
- Every node is removed **once**, as a member of exactly one layer, and each removal does O(1) set work.
- Every edge is removed once, from both ends.

So the total work is proportional to nodes plus edges, which is O(n) for a tree.

**Compare with BFS from every node:** O(n²). At n = 2·10⁴, that's 4·10⁸ operations against about 4·10⁴.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n).**

- `neighbors`: one set per node, with 2(n − 1) entries in total.
- `leaves` and `new_leaves`: at most n nodes.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "A root's height is its distance to the farthest leaf, so the best roots are the centre of the tree, the middle of its longest path. That's always one or two nodes. To find them in linear time I peel leaves layer by layer, like Kahn's algorithm but with degree 1 instead of in-degree 0. I remove all current leaves, decrement their neighbours' degrees, and any neighbour that drops to degree 1 forms the next layer. When two or fewer nodes remain, they're the answer. n = 1 is a special case. O(n) time and space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why at most two answers?" | The centre of the longest path is one node (even length) or two adjacent nodes (odd length). Any other root is farther from one end. |
| "Why `remaining > 2` and not `> 1`?" | With two adjacent centres left, both are leaves. Peeling them would leave nothing. |
| "Another O(n) approach?" | BFS from any node to find the farthest node u, BFS from u to find the farthest v. That u–v path is a diameter, and its middle node or nodes are the answer. |
| "What if the graph isn't a tree?" | The "centre" idea depends on unique paths. With cycles, you'd fall back to BFS from each node. |

**Traps:**

- **Missing `n == 1`.** Returns `[]` instead of `[0]`.
- **Peeling one leaf at a time.** You must peel a **whole layer** before recomputing. Mixing layers removes nodes unevenly from different sides.
- **Stopping at `remaining > 1`.** Destroys the two-centre case.
- **`[set()] * n`.** Every node shares a single set.
- **Adding a neighbour to `new_leaves` when its degree is `<= 1`.** A node can then be added twice. Use `== 1`.

**This same move shows up in:** [Course Schedule](207-course-schedule.md) (Kahn's algorithm, peeling in-degree-0 nodes) · [Course Schedule II](210-course-schedule-ii.md) (the same peeling, recording the order) · [Graph Valid Tree](261-graph-valid-tree.md) (reasoning about tree properties: n − 1 edges and connected) · [Diameter of Binary Tree](543-diameter-of-binary-tree.md) (the longest path that the centre sits in the middle of).

</details>

---
