# Trees

*Most tree problems are DFS in disguise. Learn the base-case → recurse → combine shape cold and pick your traversal order; the rest follows.*

## Recognize this pattern when...

- The input is a **binary tree** (or any tree) and the answer depends on subtrees.
- You're asked for **depth, height, diameter, sum, or a path** through the tree.
- The wording is **"level by level"**, **"right side view"**, or **"shortest path"** → BFS.
- It's a **BST** and you need sorted order, a range, or the k-th element → in-order DFS.
- You're comparing **two trees** or searching for a subtree → parallel recursion.

## Variations

1. **Post-order "return info up"** — children's answers combine into the parent's; track a global for path-through-node answers. *(Maximum Depth, Diameter)*
2. **Pre-order "pass info down"** — carry running state (depth, path sum, valid range) as a parameter. *(Path Sum, Validate BST with bounds)*
3. **In-order on a BST** — yields values in sorted order, perfect for k-th smallest / validation. *(Kth Smallest Element in a BST)*
4. **BFS level-order** — queue + frozen level size for anything phrased per-level. *(Level Order Traversal, Right Side View)*
5. **Two-tree parallel recursion** — recurse both trees in lockstep. *(Same Tree, Symmetric Tree, Subtree of Another Tree)*

## Representative problems

| # | Difficulty | Problem |
|---|------------|---------|
| 104 | Easy | Maximum Depth of Binary Tree |
| 226 | Easy | [Invert Binary Tree](../../../../problems/0001-0499/226.py) |
| 543 | Easy | Diameter of Binary Tree |
| 102 | Medium | Binary Tree Level Order Traversal |
| 98 | Medium | Validate Binary Search Tree |
| 124 | Hard | Binary Tree Maximum Path Sum |

## Common bugs & traps

- **Wrong base-case identity.** The empty-subtree return value must be neutral for your combine step (`0` for sums/heights, `True` for all-must-hold, `-inf` for max-path).
- **Return value vs. global answer.** For diameter / max-path-sum, what you *return to the parent* (a single downward branch) differs from what you *record globally* (the path bending through the node). Mixing them is the classic bug.
- **Validating a BST with only parent comparisons.** You must thread a `(low, high)` range down — a node can beat its parent yet violate an ancestor.
- **BFS level size captured too late.** Read `len(queue)` *before* you enqueue children, or the loop bleeds into the next level.
- **Missing None checks.** Guard `node is None` at the top of DFS and before appending children in BFS.
- **Forgetting empty input.** A `None` root should usually return `0` / `[]`, not crash.
---

*See also: [Lesson 07 →](../../../learning/07-trees.md) · [🗺 Roadmap](../../../../roadmap.md) · [problem lists](../../../../lists/)*
