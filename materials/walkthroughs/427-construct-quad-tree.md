# 427. Construct Quad Tree

**Medium** · [LeetCode](https://leetcode.com/problems/construct-quad-tree/) · [Solution file (no hints)](../../problems/0001-0499/427.py)

[📖 07. Trees lesson](../learning/07-trees.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 07. Trees problems](../rmap-practice/07-trees.md)

---

Given an `n × n` grid of `0`s and `1`s (with `n` a power of 2), build its **quad tree**. Every node has a `val` (`True` for `1`) and an `isLeaf` flag, and **internal nodes have four children**: `topLeft`, `topRight`, `bottomLeft`, `bottomRight`.

- If a region contains **all the same value**, it's a **leaf** with that value.
- Otherwise, split it into four equal quadrants and recurse. The node is internal (its `val` can be anything, so use `True`).

```
grid = [[0, 1],        →  internal root with four leaf children:
        [1, 0]]           topLeft = 0, topRight = 1, bottomLeft = 1, bottomRight = 0

grid = [[1, 1],        →  one leaf, val = True
        [1, 1]]
```

**Constraints:** `n == grid.length == grid[i].length` · `n == 2ˣ` with `0 <= x <= 6` · `grid[i][j]` is `0` or `1`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "quad tree", four children | Each region splits into **four equal quadrants**: a recursive, divide-and-conquer shape |
| "if all values are the same, it's a leaf" | The base cases are a 1×1 cell, or a uniform region |
| `n` is a power of 2 | Every split is exact: `n/2` is always a whole number, and you eventually reach size 1 |
| nodes have `val` and `isLeaf` | Build a custom node class for you. Leaves carry the colour, internal nodes ignore `val` |

The structure of the answer is the structure of the input: the tree of a region is made from the trees of its four quadrants. That's a recursion with the signature `build(row, col, size)`.

**One decision:** how do you know a region is uniform? Two options: scan the region first (O(size²) at each level), or **build the four children first, then check whether all four are leaves with the same value** and, if so, merge them into one leaf. The second needs no scanning.

🤔 **Before you open the next section:** if all four children come back as leaves, is that enough to merge them? What else must be true?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Scan region, then split | At each node, check every cell for uniformity, otherwise recurse | O(n² log n) | ✅ Correct and easy to read, but repeated scanning |
| **Recurse first, then merge** | Build four children bottom-up. If all are leaves with equal `val`, return one merged leaf | **O(n²)** | ✅ Each cell is visited once |

**The decision: [divide and conquer](../algorithms/dfs.md) recursion that merges on the way back up.** It's a post-order [tree](../data-structures/binary-tree.md) construction: children first, then decide about the parent.

The merge condition has **two parts**: all four children are leaves **and** they share the same value. Four leaves of different values can't merge. Four children where one is an internal node can't merge either, even if it contains the right colours.

The recursion bottoms out at size 1, where a single cell is trivially a leaf.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
def construct(self, grid: List[List[int]]) -> 'Node':
    def build(row: int, col: int, size: int) -> 'Node':
```

A helper that builds the node for the square whose top-left corner is `(row, col)` and whose side is `size`. The public method just starts it on the whole grid.
→ [function-basics](../syntax/function-basics.md) · [closures](../syntax/closures.md) · [recursion-basics](../syntax/recursion-basics.md)

```python
        if size == 1:
            return Node(grid[row][col] == 1, True)
```

**Base case.** A single cell is a leaf. `grid[row][col] == 1` turns the `0/1` into `False/True`. The four child pointers default to `None`.
→ [comparison-operators](../syntax/comparison-operators.md) · [boolean-basics](../syntax/boolean-basics.md)

```python
        half = size // 2
        top_left = build(row, col, half)
        top_right = build(row, col + half, half)
        bottom_left = build(row + half, col, half)
        bottom_right = build(row + half, col + half, half)
```

**Divide.** Four equal quadrants, each with half the side. Only the top-left corner coordinates shift: right by `half` for the right quadrants, down by `half` for the bottom ones.
→ [integer-division-modulo](../syntax/integer-division-modulo.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
        children = [top_left, top_right, bottom_left, bottom_right]
        if all(c.isLeaf for c in children) and len({c.val for c in children}) == 1:
            return Node(top_left.val, True)
```

**Merge on the way up.** If every child is a leaf *and* they all share one value, the whole region is uniform: replace the four children with a single leaf. The set comprehension `{c.val for c in children}` has size 1 exactly when all values match.
→ [any-all](../syntax/any-all.md) · [set-comprehension](../syntax/set-comprehension.md) · [list-basics](../syntax/list-basics.md)

```python
        return Node(True, False, top_left, top_right, bottom_left, bottom_right)

    return build(0, 0, len(grid))
```

Otherwise the region is mixed: an internal node (`isLeaf = False`) holding the four children. `val` is irrelevant for internal nodes, so use `True`.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def construct(self, grid: List[List[int]]) -> 'Node':
        def build(row: int, col: int, size: int) -> 'Node':
            if size == 1:
                return Node(grid[row][col] == 1, True)

            half = size // 2
            top_left = build(row, col, half)
            top_right = build(row, col + half, half)
            bottom_left = build(row + half, col, half)
            bottom_right = build(row + half, col + half, half)

            children = [top_left, top_right, bottom_left, bottom_right]
            if all(c.isLeaf for c in children) and len({c.val for c in children}) == 1:
                return Node(top_left.val, True)

            return Node(True, False, top_left, top_right, bottom_left, bottom_right)

        return build(0, 0, len(grid))
```

</details>

**Trace it.** `grid = [[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 1, 1], [0, 0, 1, 1]]`:

| Region | Children | Result |
|---|---|---|
| top-left 2×2 (all 1s) | four leaves, all `True` | **merged into one leaf, `True`** |
| top-right 2×2 (all 0s) | four leaves, all `False` | merged, leaf `False` |
| bottom-left 2×2 | four `False` leaves | merged, leaf `False` |
| bottom-right 2×2 | four `True` leaves | merged, leaf `True` |
| whole 4×4 | four leaves with values `T, F, F, T` | not all equal, so an **internal** root with four leaf children |

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n²)</summary>

**O(n²)**, where `n` is the side length (the grid has `n²` cells). The recursion visits `n²` base cases, and the number of nodes above them is at most a third more (1/4 + 1/16 + …). Each node does O(1) work: four comparisons and a set of size at most 4.

The scan-first version costs O(n² log n), because every level of the recursion re-scans all `n²` cells, and there are `log n` levels.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n²) for the tree, O(log n) for the stack</summary>

The worst case, a checkerboard, makes the tree have `~1.33 n²` nodes: **O(n²)** for the output. The recursion itself is only `log₂ n` frames deep, **O(log n)**.

Excluding the output, the working space is O(log n).

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "A quad tree is recursive by definition, so I'll write `build(row, col, size)`. A single cell is a leaf. Otherwise I build the four quadrants first, then check on the way back up: if all four are leaves with the same value, I collapse them into one leaf, and otherwise I return an internal node with those four children. Checking after building avoids re-scanning the region, so every cell is visited once. O(n²) time, O(log n) extra stack."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Avoid the merge logic?" | Scan the region first: if uniform, return a leaf, else split. Simpler to reason about, O(n² log n) |
| "Does the tree get *smaller* than the grid?" | Yes, uniform regions collapse. That's why quad trees compress images and spatial data |
| "Where are quad trees used?" | Image compression, collision detection, spatial indexing, map tiles |
| "Intersect two quad trees?" | [Quad Tree Intersection](../algorithms/dfs.md): recurse on both trees together, with leaf cases handling `OR` |
| "Non power-of-2 sizes?" | Pad the grid, or split unevenly with `ceil` and `floor` |

**Traps:**

- **Merging when children are leaves of *different* values.** The merge needs both conditions.
- **Merging when a child is an internal node** that happens to contain a uniform colour. It can't be (it would already have collapsed), but check `isLeaf` anyway.
- **Shifting the wrong coordinate:** the top-right quadrant moves the *column*, the bottom-left moves the *row*.
- **Using `size / 2`** (a float) instead of `size // 2`.

**This same move shows up in:** [Convert Sorted Array to BST](108-convert-sorted-array-to-binary-search-tree.md) (divide a range, build children, return the parent) · [Maximum Depth of Binary Tree](104-maximum-depth-of-binary-tree.md) (post-order combine) · [Merge Sort](912-sort-an-array.md) (divide in half, combine on the way up).

</details>

---
