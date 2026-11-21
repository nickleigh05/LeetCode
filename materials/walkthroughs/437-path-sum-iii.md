# 437. Path Sum III

**Medium** · [LeetCode](https://leetcode.com/problems/path-sum-iii/) · [Solution file (no hints)](../../problems/0001-0499/437.py)

[📖 07. Trees lesson](../learning/07-trees.md) · [📖 Prefix sums](../learning/01b-prefix-sums.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 07. Trees problems](../rmap-practice/07-trees.md)

---

Given the `root` of a binary tree and an integer `targetSum`, return the **number of paths** where the node values add up to `targetSum`.

A path **doesn't need to start at the root or end at a leaf**, but it must go **downwards**, from a parent to its children only.

```
            10
           /  \
          5    -3
         / \     \
        3   2     11
       / \   \
      3  -2   1

targetSum = 8  →  3      (5→3, 5→2→1, -3→11)
```

```
root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22  →  3
```

**Constraints:** `0 <= nodes <= 1000` · `-10⁹ <= Node.val <= 10⁹` · `-1000 <= targetSum <= 1000`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| start and end **anywhere** | Not just root-to-leaf. Any downward segment of any root-to-node path counts |
| must go **downwards** | On any single root-to-node path, a valid path is a **contiguous slice** of it |
| return the **number** | Count them. You don't need to list them |
| values can be **negative** | No early pruning, the same as [Subarray Sum Equals K](560-subarray-sum-equals-k.md) |

**The key reframe.** Stand at any node and look at the path from the root down to it. It's just a **list of numbers**. Downward paths *ending at this node* are the **suffixes** of that list. So the question at each node is:

> How many contiguous suffixes of the root-to-here list add up to the target?

That's exactly [Subarray Sum Equals K](560-subarray-sum-equals-k.md), applied to the list you're currently standing on. Its solution was **prefix sums plus a hash map of counts**:

> a slice ending here sums to `target` ⟺ some earlier prefix sum equals `current_sum − target`

**The tree twist: undo when you leave a branch.** In an array, prefixes only ever accumulate. In a tree, when you finish a node's subtree and go back up, that node's prefix sum is **no longer on your path**. A node in the right subtree must not match a prefix from the left subtree. So after exploring a node's children, **decrement its count** in the map. It's the same choose / explore / un-choose rhythm as backtracking.

🤔 **Before you open the next section:** why would a count left over from the left subtree give a wrong answer for nodes in the right subtree?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Double DFS | From every node, DFS downwards counting paths from it | O(n²) worst, O(n log n) balanced | O(h) | ⚠️ Works at n = 1000, but wasteful |
| **Prefix sums + hash map + backtracking** | One DFS; count matches against the root-to-here prefix sums | **O(n)** | O(h) | ✅ |

**The decision: one [DFS](../algorithms/dfs.md) carrying a running sum, with a [hash map](../data-structures/hashmap.md) of prefix-sum counts** that's updated on the way down and undone on the way back up.

**Seed with `{0: 1}`.** For the same reason as in the array version: it represents the empty prefix, before the root. A path that starts at the root needs `current_sum − target == 0` to find a match.

**Order inside the visit:**
1. Add this node to `current_sum`.
2. **Look up** `current_sum − target`, counting paths that end here.
3. **Record** `current_sum`, so descendants can use it.
4. Recurse into the children.
5. **Un-record** `current_sum` on the way out.

Looking up before recording matters when `target == 0`. Otherwise a node's own prefix would match itself and count an empty path.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
prefix_counts = {0: 1}
```

**Prefix sum → how many times it appears on the current root-to-node path.** It's seeded with the empty prefix so that paths starting at the root are counted.
→ [dict-basics](../syntax/dict-basics.md)

```python
def dfs(node, current_sum):
    if not node:
        return 0
```

The helper returns the **number of valid paths ending inside this subtree**. An empty subtree has none.
→ [closures](../syntax/closures.md) · [truthy-falsy-values](../syntax/truthy-falsy-values.md) · [recursion-basics](../syntax/recursion-basics.md)

```python
    current_sum += node.val
    count = prefix_counts.get(current_sum - targetSum, 0)
```

**Count paths ending at this node.** Each earlier prefix equal to `current_sum − targetSum` marks a starting point. The slice from there to here sums to exactly the target. `.get(…, 0)` handles "no such prefix."
→ [dict-methods](../syntax/dict-methods.md)

```python
    prefix_counts[current_sum] = prefix_counts.get(current_sum, 0) + 1
```

**Record this node's prefix** for its descendants. It's added **after** the lookup, so a node can't match itself.
→ [dict-methods](../syntax/dict-methods.md)

```python
    count += dfs(node.left, current_sum)
    count += dfs(node.right, current_sum)
```

**Explore both subtrees** and add up the paths found below. `current_sum` is an integer passed by value, so each child gets its own copy. Only the shared map needs undoing.

```python
    prefix_counts[current_sum] -= 1
    return count
```

**Undo the record.** This node is leaving the current path, so its prefix must not be visible to nodes in other branches.

```python
return dfs(root, 0)
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def pathSum(self, root: TreeNode | None, targetSum: int) -> int:

        prefix_counts = {0: 1}

        def dfs(node, current_sum):
            if not node:
                return 0

            current_sum += node.val
            count = prefix_counts.get(current_sum - targetSum, 0)
            prefix_counts[current_sum] = prefix_counts.get(current_sum, 0) + 1
            count += dfs(node.left, current_sum)
            count += dfs(node.right, current_sum)
            prefix_counts[current_sum] -= 1

            return count

        return dfs(root, 0)
```

</details>

**Trace it.** The first example, `targetSum = 8`, following the three matching paths:

| Node | Path from root | `current_sum` | Look for `sum − 8` | Found in map? | Path counted |
|---|---|---|---|---|---|
| 10 | 10 | 10 | 2 | no | |
| 5 | 10, 5 | 15 | 7 | no | |
| 3 | 10, 5, 3 | 18 | 10 | **yes** (the 10 prefix) | **5 → 3** |
| 3 (leaf) | 10, 5, 3, 3 | 21 | 13 | no | |
| −2 | 10, 5, 3, −2 | 16 | 8 | no | |
| 2 | 10, 5, 2 | 17 | 9 | no | |
| 1 | 10, 5, 2, 1 | 18 | 10 | **yes** | **5 → 2 → 1** |
| −3 | 10, −3 | 7 | −1 | no | |
| 11 | 10, −3, 11 | 18 | 10 | **yes** | **−3 → 11** |

Total **3** ✅. When the search moves from the left subtree into `−3`, the prefixes 15, 18, 21, 16, 17 and 18 have all been decremented back to zero. That's why the right subtree only sees `{0, 10}` plus its own prefixes.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).** Each node is visited once, and each visit does a constant number of O(1)-average dict operations: a lookup, an increment and a decrement.

**Compare the double DFS:** starting a fresh downward search from every node costs O(n · h). That's O(n²) on a skewed tree. At n = 1000 it would pass, but the prefix-sum version is the one interviewers are looking for.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(h)</summary>

**O(h)** for both the recursion stack and the map. Because counts are undone on the way out, the map only ever holds prefixes from the **current** root-to-node path, which is at most h + 1 distinct sums.

(Entries that drop to 0 stay as keys. Over a whole run the map can collect up to n keys, but at most h + 1 have non-zero counts at any moment. Deleting keys at zero would keep it strictly O(h).)

- Balanced: O(log n).
- Skewed: O(n), with 1000 levels of recursion, which is right at Python's default recursion limit. Raise it with `sys.setrecursionlimit` if needed.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Any downward path ending at a node is a suffix of the root-to-node path, so at each node this is Subarray Sum Equals K on that path. I carry the running sum down the tree and keep a map from prefix sum to how many times it's on the current path, seeded with {0: 1}. At each node I add the count of `sum − target` to the answer, then record my sum, recurse, and decrement it on the way out so other branches don't see it. Each node does O(1) dict work, so it's O(n) time and O(h) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why `{0: 1}`?" | It's the empty prefix, so paths starting at the root get counted. |
| "Why decrement after the children?" | That prefix is no longer on the path. Leaving it in would let nodes in a different branch match it. |
| "Return the paths themselves?" | Keep the path values in a list (as in [Path Sum II](113-path-sum-ii.md)) and, at each match, walk back to find where the slice starts. The output can be large. |
| "Only root-to-leaf paths?" | [Path Sum II](113-path-sum-ii.md). A simpler DFS, checking at leaves only. |
| "Paths that can go up and down?" | That's [Binary Tree Maximum Path Sum](124-binary-tree-maximum-path-sum.md) territory, a different technique. |

**Traps:**

- **Forgetting to undo the count.** It produces matches across branches that aren't on one downward path.
- **Recording before looking up.** With `target == 0`, every node matches itself.
- **Missing `{0: 1}`.** Every path that starts at the root is missed.
- **Pruning when the sum exceeds the target.** Negative values make that wrong.
- **Treating it as root-to-leaf only.** Re-read the problem: paths can start and end anywhere.

**This same move shows up in:** [Subarray Sum Equals K](560-subarray-sum-equals-k.md) (the same prefix-sum counting on an array) · [Path Sum II](113-path-sum-ii.md) (root-to-leaf paths with backtracking) · [Path Sum](112-path-sum.md) (the yes/no root-to-leaf version) · [Contiguous Array](525-contiguous-array.md) (prefix sums plus a hash map, storing first indices instead of counts).

</details>

---
