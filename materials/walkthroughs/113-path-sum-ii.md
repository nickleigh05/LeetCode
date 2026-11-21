# 113. Path Sum II

**Medium** · [LeetCode](https://leetcode.com/problems/path-sum-ii/) · [Solution file (no hints)](../../problems/0001-0499/113.py)

[📖 07. Trees lesson](../learning/07-trees.md) · [📖 10. Backtracking lesson](../learning/10-backtracking.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 07. Trees problems](../rmap-practice/07-trees.md)

---

Given the `root` of a binary tree and an integer `targetSum`, return **all root-to-leaf paths** where the sum of the node values equals `targetSum`. Each path is a list of node **values**. A **leaf** is a node with no children.

```
            5
           / \
          4   8
         /   / \
        11  13  4
       /  \    / \
      7    2  5   1

targetSum = 22  →  [[5,4,11,2], [5,8,4,5]]
```

```
root = [1,2,3], targetSum = 5  →  []
root = [1,2],   targetSum = 0  →  []
```

**Constraints:** `0 <= nodes <= 5000` · `-1000 <= Node.val <= 1000` · `-1000 <= targetSum <= 1000`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**root-to-leaf**" | Paths must start at the root and end at a **leaf**. Stopping partway down doesn't count |
| "**all** paths" | Collect every match, so you can't stop at the first one |
| return the **values** | You need the path itself, not just a yes/no. That's what separates it from [Path Sum](112-path-sum.md) |
| values can be **negative** | You **can't** prune when the running sum overshoots, since a later negative could bring it back |
| tree can be empty | `None` → `[]` |

**This is Path Sum plus a record of the path.** In [Path Sum](112-path-sum.md) you carry a running total down the tree and check at each leaf. Here you also need to know *which* nodes got you there. So carry a `path` list as you go down.

**The backtracking pattern.** Use **one** shared `path` list:
1. **Choose:** append the current node's value.
2. **Explore:** recurse into the children.
3. **Un-choose:** pop the value off before returning to the parent.

That last step is what lets a single list serve the whole search. When you come back up from the left subtree, the path is exactly as it was before you went down, ready for the right subtree.

**Copy when you save.** When a leaf matches, append `path[:]` (a copy), **not** `path`. The shared list keeps changing, so saving it directly would leave you with many references to one list that ends up empty.

🤔 **Before you open the next section:** after exploring a node's left and right children, why must you remove that node from `path` before returning?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| New list per call | Pass `path + [node.val]` down | O(n·h) copies on every call | O(n·h) | ⚠️ Correct, wasteful |
| **DFS + shared path + backtrack** | Append, recurse, pop; copy only at matching leaves | **O(n·h)** worst case | O(h) + output | ✅ |
| BFS with paths in the queue | Store `(node, path, sum)` per entry | O(n·h) | O(n·h) | ⚠️ Lots of copying |

**The decision: recursive [DFS](../algorithms/dfs.md) with [backtracking](../algorithms/backtracking.md).**

Root-to-leaf paths are exactly what DFS walks. The shared list only copies when it finds an answer, while the "new list per call" version copies at *every* node.

**Track what's remaining, not the sum so far.** Subtract each node's value from `remaining` on the way down. At a leaf, the path matches if `remaining == 0`. That's a little tidier than carrying a sum and comparing it with `targetSum`.

**Why the leaf check matters.** Consider `[1, 2]` with `targetSum = 1`. The root's value alone is 1, but the root isn't a leaf (it has a left child), so `[1]` isn't a valid path. Checking for a match before checking for a leaf is the classic bug here.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
result = []
path = []
```

`result` collects matching paths. `path` is the **one** list that holds the current root-to-node path as the search moves around.
→ [list-basics](../syntax/list-basics.md)

```python
def dfs(node, remaining):
    if node is None:
        return
```

A nested helper so it can see `result`, `path` and `targetSum` without passing them in. The base case: an empty subtree contributes nothing.
→ [closures](../syntax/closures.md) · [none-type](../syntax/none-type.md) · [recursion-basics](../syntax/recursion-basics.md)

```python
    path.append(node.val)
    remaining -= node.val
```

**Choose.** Add this node to the path and subtract its value from what's still needed.
→ [list-methods](../syntax/list-methods.md)

```python
    if node.left is None and node.right is None and remaining == 0:
        result.append(path[:])
```

**Check only at leaves.** Both children missing means it's a leaf. If the remaining amount is exactly 0, this path is an answer.

`path[:]` makes a **copy** of the list. Appending `path` itself would store a reference to the shared list, which will be emptied by later pops.
→ [list-slicing](../syntax/list-slicing.md) · [copy-vs-deepcopy](../syntax/copy-vs-deepcopy.md) · [logical-operators](../syntax/logical-operators.md)

```python
    dfs(node.left, remaining)
    dfs(node.right, remaining)
    path.pop()
```

**Explore, then un-choose.** Recurse into both children. Calling on `None` children is safe, because the base case returns. Then pop this node so the path matches the parent's again.

`remaining` is an integer and each call has its own copy, so it doesn't need undoing. Only the shared list does.
→ [list-methods](../syntax/list-methods.md)

```python
dfs(root, targetSum)
return result
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        result = []
        path = []

        def dfs(node, remaining):
            if node is None:
                return

            path.append(node.val)
            remaining -= node.val

            if node.left is None and node.right is None and remaining == 0:
                result.append(path[:])

            dfs(node.left, remaining)
            dfs(node.right, remaining)
            path.pop()

        dfs(root, targetSum)
        return result
```

</details>

**Trace it.** The example tree with `targetSum = 22`, following the left branch first:

| Visit | `path` | `remaining` | Leaf? | Action |
|---|---|---|---|---|
| 5 | [5] | 17 | no | go down |
| 4 | [5,4] | 13 | no | go down |
| 11 | [5,4,11] | 2 | no | go down |
| 7 | [5,4,11,7] | −5 | yes | no match, pop |
| 2 | [5,4,11,2] | 0 | yes | **save a copy** ✅, pop |
| back at 11, 4 | [5] | | | both popped |
| 8 | [5,8] | 9 | no | go down |
| 13 | [5,8,13] | −4 | yes | no match |
| 4 | [5,8,4] | 5 | no | go down |
| 5 | [5,8,4,5] | 0 | yes | **save a copy** ✅ |
| 1 | [5,8,4,1] | 4 | yes | no match |

Result `[[5,4,11,2], [5,8,4,5]]` ✅. Note the path drops back to `[5]` between the two branches. That's the backtracking.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n·h)</summary>

**O(n) to visit every node, plus the cost of copying matching paths.**

Each node is visited once, with O(1) work apart from the copy. A copy costs O(h), the path length.

**Worst case O(n²)** for a skewed tree, or **O(n log n)** for a balanced one, if many leaves match. A balanced tree has about n/2 leaves, each with a path of length log n, and every one could match (think of all-zero values with target 0).

You can't do better than the size of the output, since writing out every matching path is part of the job.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(h), plus the output</summary>

**O(h)** working space: the recursion stack and the shared `path` both grow to the tree's height.

- Balanced tree: O(log n).
- Skewed tree (a linked list in disguise): O(n). At 5000 nodes, that's past Python's default recursion limit of 1000. Either raise it with `sys.setrecursionlimit` or switch to an iterative DFS with an explicit stack.

The **output** itself can be O(n log n) to O(n²), as above. It's usually counted separately.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "I need every root-to-leaf path with the right sum, so it's DFS with backtracking. I keep one shared path list: append the node, subtract its value from the remaining target, and at a leaf with remaining equal to zero I save a copy of the path. Then I recurse into both children and pop the node on the way back. Values can be negative, so I can't prune early, and I only check at leaves. It's O(n) visits plus O(h) per saved path, and O(h) stack space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Paths can start and end anywhere going down?" | That's [Path Sum III](437-path-sum-iii.md). Use prefix sums on the root-to-node path, with a hash map of counts. |
| "Just return whether one exists?" | That's [Path Sum](112-path-sum.md). Same DFS, return early on the first match, no path list. |
| "Why `path[:]`?" | `path` is one list that keeps changing. Saving it directly stores a reference that later pops will empty. |
| "Can you prune early?" | Only if all values are non-negative. Negatives can bring an overshoot back. |
| "Avoid recursion?" | An explicit stack of `(node, remaining, path)` works, at the cost of copying paths. |

**Traps:**

- **Saving `path` instead of `path[:]`.** You end up with a list of empty lists.
- **Forgetting `path.pop()`.** Values from the left subtree leak into the right subtree's paths.
- **Checking the sum at non-leaf nodes.** `[1, 2]` with target 1 would wrongly return `[[1]]`.
- **Stopping when the sum is exceeded.** Wrong with negative values.
- **Recursion depth on skewed trees.** 5000 nodes in a line will overflow Python's default stack.

**This same move shows up in:** [Path Sum](112-path-sum.md) (the yes/no version) · [Path Sum III](437-path-sum-iii.md) (any downward path, counted with prefix sums) · [Binary Tree Paths](257-binary-tree-paths.md) (collect every root-to-leaf path) · [Subsets](78-subsets.md) (the same append-recurse-pop backtracking shape).

</details>

---
