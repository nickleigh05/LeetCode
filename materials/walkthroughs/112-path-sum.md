# 112. Path Sum

**Easy** · [LeetCode](https://leetcode.com/problems/path-sum/) · [Solution file (no hints)](../../problems/0001-0499/112.py)

[📖 07. Trees lesson](../learning/07-trees.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 07. Trees problems](../rmap-practice/07-trees.md)

---

Given the root of a binary tree and an integer `targetSum`, return `true` if the tree has a **root-to-leaf** path whose values sum to `targetSum`. A **leaf** is a node with no children.

```
root = [5,4,8,11,null,13,4,7,2,null,null,null,1], targetSum = 22  →  true   (5→4→11→2)
root = [1,2,3], targetSum = 5   →  false
root = [],      targetSum = 0   →  false
```

**Constraints:** `0 <= number of nodes <= 5000` · `-1000 <= Node.val <= 1000` · `-1000 <= targetSum <= 1000`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**root-to-leaf**" | ⚠️ The path must start at the root **and end at a leaf**. Partial paths don't count |
| "a **leaf** has no children" | Both `left` and `right` must be `None` — not just one |
| return `true`/`false` | Existence only, so you can **short-circuit** on the first success |
| values can be **negative** | ⚠️ You cannot prune when the running sum exceeds the target — a negative later could still rescue it |
| `0 <= nodes` | An empty tree has no paths ⇒ always `false`, even when `targetSum` is 0 |

**The recursive shape.** Tree problems decompose naturally: *"can I answer this for the whole tree using answers about the subtrees?"* Here, yes:

> A path summing to `T` exists from `node` **iff** a path summing to `T - node.val` exists from `node.left` **or** from `node.right`.

Each step subtracts the current node's value and asks the same question one level down. That's a **top-down** recursion, carrying a running remainder — as opposed to the **bottom-up** style of [Maximum Depth](104-maximum-depth-of-binary-tree.md), where children return values that get combined.

**The two base cases**, and both are easy to get subtly wrong:

1. **`node is None`** → `false`. An empty subtree contains no root-to-leaf path. Critically this is **not** "check whether the remainder is 0" — see the trap below.
2. **`node` is a leaf** → `true` iff `node.val == remaining`. This is the only place success can be declared, because only a leaf terminates a valid path.

**Why the empty-tree case can't test the remainder.** Consider `[1,2]` with `targetSum = 1`:

```
  1
 /
2
```

Node 1 is *not* a leaf (it has a left child), so the path can't stop there. If the `None` base case returned `remaining == 0`, then recursing into node 1's **right** child (`None`) with `remaining = 0` would return `true` — wrongly reporting a path that ends mid-tree. Returning `false` for `None` and checking leaf-ness explicitly is what prevents that.

🤔 **Before you open the next section:** why can't you stop as soon as the running sum equals the target — what does the problem require beyond hitting the number?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Enumerate all paths | Build every root-to-leaf list, sum each | O(n·h) | O(n·h) | ⚠️ Correct, wasteful |
| **Recursive DFS with a remainder** | Subtract as you descend | **O(n)** | **O(h)** | ✅ |
| Iterative DFS with a stack | Push `(node, remaining)` pairs | O(n) | O(h) | ✅ Avoids recursion limits |
| BFS with a queue | Same, level by level | O(n) | O(n) | ⚠️ Correct, more memory |

**The decision: recursive DFS, subtracting the node's value as you descend.**

Two equivalent framings — subtract down, or accumulate down:

```python
# subtract (used here)              # accumulate
remaining = targetSum - node.val    running = acc + node.val
... leaf: return node.val == rem    ... leaf: return running == targetSum
```

Subtracting is marginally tidier because the target stays in one variable and the leaf test compares two numbers you already have.

**Why `or` gives short-circuiting for free.** `self.hasPathSum(left, rem) or self.hasPathSum(right, rem)` — Python evaluates the right operand only if the left is falsy. So the moment any path succeeds, the entire remaining search is skipped. That's an early exit with no extra code, and it's why the average case is much better than the O(n) bound suggests.

**Why you can't prune on the running sum.** With all-positive values you could stop descending once the remainder went negative. But values range down to −1000, so a path that looks hopeless can be rescued by a negative node further down. **Any pruning heuristic based on the remainder's sign is wrong here** — a genuinely important detail, and exactly the kind of constraint interviewers plant deliberately.

**Why not enumerate all paths?** Building the actual lists costs O(h) per path and O(n·h) overall, and you only need a boolean. That approach becomes appropriate for [Path Sum II](https://leetcode.com/problems/path-sum-ii/), which asks for the paths themselves.

**Recursion depth:** with up to 5000 nodes, a degenerate tree is 5000 deep — **beyond Python's default limit of ~1000**. That's a real risk here, and the iterative stack version is the safe answer if raised. Mention it.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
if not root:
    return False
```

**Base case 1: empty subtree.**

An empty tree contains no root-to-leaf path, so the answer is `false` — **regardless of the remaining sum**. This is what stops a path from "ending" at a missing child of a non-leaf node.

It also handles the empty-tree input directly: `hasPathSum(None, 0)` is `false`, as required.
→ [truthy-falsy-values](../syntax/truthy-falsy-values.md) · [if-return](../syntax/if-return.md)

```python
if not root.left and not root.right:
    return root.val == targetSum
```

**Base case 2: leaf.**

A leaf has **both** children absent — `and`, not `or`. A node with one child is not a leaf and the path must continue through it.

Here the value is compared against `targetSum` directly (rather than subtracting first), because at a leaf the remaining target *is* what this node must contribute.

This is the **only** place `True` can originate.
→ [logical-operators](../syntax/logical-operators.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
remaining = targetSum - root.val
```

**Consume this node's value.** The subtrees must now supply `remaining`.
→ [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
return self.hasPathSum(root.left, remaining) or self.hasPathSum(root.right, remaining)
```

**Recurse into both subtrees.**

`or` means *either* side succeeding is enough — and short-circuits, so if the left subtree finds a path the right is never explored.
→ [recursion-basics](../syntax/recursion-basics.md) · [logical-operators](../syntax/logical-operators.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:

        if not root:
            return False

        if not root.left and not root.right:
            return root.val == targetSum

        remaining = targetSum - root.val

        return self.hasPathSum(root.left, remaining) or self.hasPathSum(root.right, remaining)
```

</details>

<details>
<summary>The iterative version (safe on deep trees)</summary>

```python
class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        if not root:
            return False

        stack = [(root, targetSum)]
        while stack:
            node, remaining = stack.pop()
            if not node.left and not node.right and node.val == remaining:
                return True
            if node.left:
                stack.append((node.left, remaining - node.val))
            if node.right:
                stack.append((node.right, remaining - node.val))

        return False
```

Carries the remainder alongside each node on the stack. O(n) time, O(h) space, and immune to Python's recursion limit — which matters at 5000 nodes.

</details>

**Trace it** — `targetSum = 22` on:

```
        5
       / \
      4   8
     /   / \
   11  13   4
   / \       \
  7   2       1
```

| Call | `targetSum` | Node | Leaf? | Action |
|---|---|---|---|---|
| 1 | 22 | 5 | no | `remaining = 17`, recurse left |
| 2 | 17 | 4 | no | `remaining = 13`, recurse left |
| 3 | 13 | 11 | no | `remaining = 2`, recurse left |
| 4 | 2 | 7 | ✅ | `7 == 2`? **no** → `False` |
| 5 | 2 | 2 | ✅ | `2 == 2`? **YES** → `True` ⭐ |

Call 3 returns `False or True` = `True`, which propagates up through calls 2 and 1.

Return **`True`** ✅ — the path `5 → 4 → 11 → 2` sums to 22.

Note the short-circuit: once call 5 returned `True`, the entire right subtree of node 5 (nodes 8, 13, 4, 1) was **never visited**.

**A false case** — `[1,2,3]`, `targetSum = 5`:

| Call | `targetSum` | Node | Leaf? | Result |
|---|---|---|---|---|
| 1 | 5 | 1 | no | `remaining = 4`, recurse both |
| 2 | 4 | 2 | ✅ | `2 == 4`? no → `False` |
| 3 | 4 | 3 | ✅ | `3 == 4`? no → `False` |

`False or False` → **`False`** ✅

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** worst case — every node is visited once, doing O(1) work.

**Better in practice**, thanks to the short-circuiting `or`: as soon as any path succeeds, the rest of the tree is skipped. A matching path in the leftmost branch means only O(h) nodes are examined.

| Case | Nodes visited |
|---|---|
| Match on the first path | O(h) |
| No match anywhere | O(n) |

**Why you can't do better than O(n) in the worst case:** with negative values allowed, no subtree can be ruled out without examining it. If all values were positive you could prune whenever the remainder went negative — a genuine optimization that this problem's constraints deliberately block.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(h)</summary>

**O(h)** for the recursion stack, where `h` is the tree height.

| Tree shape | `h` | Space |
|---|---|---|
| Balanced | `log n` | **O(log n)** ≈ 13 at n = 5000 |
| Degenerate | `n` | **O(n)** = 5000 ⚠️ |

**The degenerate case is a real hazard here.** With 5000 nodes in a single chain, the recursion is 5000 frames deep — well past Python's default limit of ~1000, giving a `RecursionError` rather than a wrong answer.

Two responses if this comes up:

1. Use the **iterative stack version** above — same complexity, no frame limit.
2. Raise the limit with `sys.setrecursionlimit(...)` — works, but it's a workaround, not a fix, and risks a real stack overflow.

Nothing beyond the stack is allocated: no path lists, no visited set. Contrast [Path Sum II](https://leetcode.com/problems/path-sum-ii/), which must build the actual paths and therefore costs O(n·h) in the worst case.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "This decomposes recursively: a path summing to `T` exists from a node exactly when a path summing to `T − node.val` exists from one of its children. So I subtract as I descend. Two base cases — an empty subtree returns `false`, and a **leaf** returns whether its value equals the remaining target. The empty case must return `false` rather than checking the remainder, otherwise a path could 'end' at a missing child of a non-leaf node and report a false positive. I combine the subtrees with `or`, which short-circuits, so the search stops at the first success. O(n) worst case, O(h) space. One caveat: values can be negative, so I can't prune when the remainder goes negative — and with 5000 nodes a degenerate tree would exceed Python's recursion limit, so I'd use an explicit stack carrying `(node, remaining)` pairs."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Return **all** such paths." | [Path Sum II](https://leetcode.com/problems/path-sum-ii/) — backtracking, carrying the current path and appending a copy at a matching leaf. O(n·h). |
| "Count paths summing to `T` **anywhere** (not root-to-leaf)?" | [Path Sum III](https://leetcode.com/problems/path-sum-iii/) — prefix sums in a hash map along the current path. O(n). |
| "Why does the `None` case return `false`?" | Otherwise a path could terminate at a missing child of a non-leaf node. `[1,2]` with target 1 exposes it. |
| "Could you prune early?" | Only if all values were positive. Negatives are allowed, so a large remainder can still be met later. |
| "What about deep trees?" | 5000 nodes in a chain exceeds Python's ~1000-frame limit — use the iterative stack version. |
| "Why `and` in the leaf check?" | A leaf has **both** children absent. `or` would treat a one-child node as a leaf. |
| "Does an empty tree with `targetSum = 0` return true?" | No — there are no root-to-leaf paths at all. |

**Traps:**

- **Returning `targetSum == 0` for the `None` case.** Reports paths that end at a missing child. The `[1,2]`, target 1 case catches it.
- **Using `or` in the leaf test.** A node with one child would be misclassified as a leaf.
- **Checking the sum at every node instead of only at leaves.** Accepts partial paths.
- **Pruning on a negative remainder.** Wrong here — negative values can recover.
- **Forgetting to subtract before recursing.** Every level then tests against the original target.
- **Recursing on a 5000-node chain.** `RecursionError`.

**This same move shows up in:** [Maximum Depth of Binary Tree](104-maximum-depth-of-binary-tree.md) (the same DFS skeleton, combining bottom-up instead of carrying state down) · [Minimum Depth of Binary Tree](111-minimum-depth-of-binary-tree.md) (the same leaf-vs-`None` distinction, and the same trap) · [Binary Tree Paths](257-binary-tree-paths.md) (root-to-leaf enumeration with backtracking) · [Binary Tree Maximum Path Sum](124-binary-tree-maximum-path-sum.md) (the Hard relative, where paths needn't touch the root).

</details>

---
