# 1448. Count Good Nodes in Binary Tree

**Medium** · [LeetCode](https://leetcode.com/problems/count-good-nodes-in-binary-tree/)

[📖 07. Trees lesson](../learning/07-trees.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 07. Trees problems](../rmap-practice/07-trees.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Given a binary tree, a node `X` is **good** if, on the path from the root to `X`, there are **no nodes with a value greater than X**.

Return the number of good nodes.

```
        3          →  4 good nodes
      /   \
     1     4          3 (root — always good)
    /     / \         4 (3→4, nothing bigger)
   3     1   5        5 (3→4→5, nothing bigger)
                      3 (3→1→3, the max on the path is 3, and 3 >= 3 ✅)
                      1 and 1 are NOT good — a 3 or 4 precedes them
```

**Constraints:** `1 <= nodes <= 10⁵` · `-10⁴ <= Node.val <= 10⁴`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "on the path **from the root**" | ⚠️ Only **ancestors** matter — not siblings, not the whole tree. Each node's answer depends on its own root-to-node path |
| "no nodes with a value **greater than** X" | So `X >= max(ancestors)`. **Ties count as good** — "greater than", not "greater than or equal" |
| "**count** the good nodes" | Sum over the whole tree; no early exit |
| the root is always good | It has no ancestors, so vacuously nothing exceeds it |
| n up to 10⁵ | O(n) needed; and a skewed tree would be 10⁵ deep — mind the recursion limit |

**The important reframe.** You don't need the whole ancestor list — only the **maximum** value among them. A node is good exactly when its value is at least that running maximum.

And that maximum updates trivially as you descend:

```
new_max = max(old_max, current_value)
```

This is a **top-down** problem, which makes it the odd one out in this unit:

| Direction | Information flows | Examples |
|---|---|---|
| **Bottom-up** | children's results → parent (via `return`) | [104](104-maximum-depth-of-binary-tree.md), [543](543-diameter-of-binary-tree.md), [110](110-balanced-binary-tree.md) |
| **Top-down** | ancestors' context → children (via **parameters**) | **1448**, [98](98-validate-binary-search-tree.md) |

Here you carry context *down* as an extra argument, and count on the way back up. Recognizing which direction a problem needs is most of the battle in tree recursion.

🤔 **Before you open the next section:** what should the initial "max so far" be when you call the function on the root — and why does the answer make the root automatically good?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| For each node, walk back to the root | Check ancestors per node | O(n·h) | ❌ Re-walks paths; needs parent pointers |
| Carry the full ancestor **list** down | Pass a list, take its max | O(n·h) time, O(h) space | ⚠️ Correct but wasteful — you only need the max |
| **Carry the running max down** | One extra parameter | **O(n)** | ✅ |

**The decision: DFS passing the path maximum down as a parameter.**

At each node:
1. **Is it good?** `node.val >= max_so_far` → count 1, else 0.
2. **Update the max** for everything below: `new_max = max(max_so_far, node.val)`.
3. **Recurse** into both children with that new max, and sum the three counts.

**Why carrying just the max is enough.** "No ancestor is greater than me" is precisely "I'm ≥ all of them", and comparing against the maximum answers that in one operation. The rest of the ancestor list is irrelevant — a genuine instance of *finding the minimal state that answers the question*, the same instinct as [Generate Parentheses](22-generate-parentheses.md) needing only two counters instead of the string built so far.

**Why each branch gets its own max, independently.** The parameter is passed *by value* down each subtree, so the left and right branches carry separate maxima. A large value on the left path can't affect nodes on the right. That's automatic with parameters — and it's precisely what a shared mutable variable would get **wrong**.

**Why `>=` and not `>`.** The definition says no ancestor is *greater than* X, so an ancestor **equal** to X is fine. In the example, the deep `3` under `1` is good because the path max is 3 and `3 >= 3`. Using `>` would wrongly exclude it.

**Initialize with `root.val`.** Then the root satisfies `root.val >= root.val` and counts as good, matching the definition with no special case. *(`float("-inf")` works identically.)*

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
def dfs(node, max_so_far):
    if not node:
        return 0
```

The helper takes **two** arguments — the node, and the context inherited from its ancestors. That second parameter is the whole technique.

An empty subtree contributes 0 good nodes.
→ [function-basics](../syntax/function-basics.md) · [closures](../syntax/closures.md) · [truthy-falsy-values](../syntax/truthy-falsy-values.md)

```python
    good = 1 if node.val >= max_so_far else 0
```

**The goodness test.** `>=` because ties count — an ancestor equal to this value isn't *greater than* it.

The ternary reads as "1 if good, else 0" so it can be summed directly with the subtree counts below.
→ [ternary-expression](../syntax/ternary-expression.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
    new_max = max(max_so_far, node.val)
```

**Update the context for the descendants.** Everything below this node has it as an ancestor, so the path maximum must account for it.

Computed into a new variable rather than reassigning `max_so_far` — either works, but this makes it clear the parent's value is untouched.
→ [min-max-key](../syntax/min-max-key.md)

```python
    good += dfs(node.left, new_max)
    good += dfs(node.right, new_max)
    return good
```

**Recurse and sum.** Each child gets `new_max` — and crucially, **each subtree receives its own copy**, so the left branch's discoveries never leak into the right.

The total is this node's contribution plus both subtrees'. Information flows **down** as a parameter and **up** as a return value, simultaneously.
→ [recursion-basics](../syntax/recursion-basics.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
return dfs(root, root.val)
```

**Seed with `root.val`.** The root then satisfies `root.val >= root.val` and is counted as good — matching "the root is always good" with no special case.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def goodNodes(self, root: TreeNode) -> int:

        def dfs(node, max_so_far):
            if not node:
                return 0

            good = 1 if node.val >= max_so_far else 0
            new_max = max(max_so_far, node.val)

            good += dfs(node.left, new_max)
            good += dfs(node.right, new_max)
            return good

        return dfs(root, root.val)
```

</details>

**Trace it** — the example tree:

```
        3
      /   \
     1     4
    /     / \
   3     1   5
```

| Node | Path from root | `max_so_far` on entry | `val >= max`? | Good? |
|---|---|---|---|---|
| **3** (root) | 3 | 3 | 3 ≥ 3 | ✅ |
| 1 | 3→1 | 3 | 1 ≥ 3 ✗ | ❌ |
| **3** | 3→1→3 | 3 | 3 ≥ 3 | ✅ |
| **4** | 3→4 | 3 | 4 ≥ 3 | ✅ |
| 1 | 3→4→1 | **4** | 1 ≥ 4 ✗ | ❌ |
| **5** | 3→4→5 | **4** | 5 ≥ 4 | ✅ |

Total: **4** ✅

Two rows are worth pausing on:

- The deep `3` (row 3) is good **because of `>=`**. Its path max is 3, and equal counts.
- The two `1`s have *different* `max_so_far` values — 3 on the left path, 4 on the right. Each branch carried its own context down, which is exactly what passing by parameter gives you.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

Every node is visited exactly once, doing O(1) work: one comparison, one `max`, two additions.

n × O(1) = **O(n)**.

**Versus carrying the whole ancestor list.** Passing a list and calling `max()` on it costs O(h) per node → **O(n·h)**, which is O(n²) on a skewed tree — 10¹⁰ at the constraint limit. **Reducing the carried state from a list to a single number is what makes it linear.**

**Versus walking back to the root per node.** Also O(n·h), and it needs parent pointers the problem doesn't provide.

**No early exit** — every node must be classified, since you're counting rather than searching.

**The comparison with [110 Balanced Binary Tree](110-balanced-binary-tree.md) is instructive:** that problem could short-circuit because a single failure decided a boolean. Here the answer is a **count**, so every node contributes and nothing can be skipped. *Yes/no questions can bail; counting and extremum questions can't.*

</details>

<details>
<summary><b>5 · Space complexity</b> — O(h)</summary>

**O(h)** for the recursion stack — **O(log n)** balanced, **O(n)** skewed.

The carried context is a **single integer per frame**, so the parameter adds O(1) per level, not O(h). Carrying the full ancestor list instead would make it O(h) *per frame* and O(h²) overall in the worst case.

⚠️ **At n = 10⁵ the recursion limit is a real concern.** A skewed tree means 10⁵ frames, well past Python's default of 1000 → `RecursionError`. The iterative fix is straightforward here, because this is a **top-down** problem: push `(node, max_so_far)` pairs onto an explicit stack.

```python
stack = [(root, root.val)]
count = 0
while stack:
    node, mx = stack.pop()
    if not node: continue
    if node.val >= mx: count += 1
    new_mx = max(mx, node.val)
    stack.append((node.left, new_mx))
    stack.append((node.right, new_mx))
```

**Top-down problems convert to iteration easily** — you just carry the context in the stack entry. Bottom-up ones ([543](543-diameter-of-binary-tree.md), [110](110-balanced-binary-tree.md)) are much fiddlier, because a node can't be finished until both children are.
→ [recursion-limit](../syntax/recursion-limit.md)

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "A node is good if it's at least as large as every ancestor — and to check that I don't need the whole ancestor list, just their maximum. So this is a top-down traversal: I pass the running path maximum down as a parameter, test `node.val >= max_so_far` at each node, then recurse into both children with the updated max. Because it's a parameter, each subtree gets its own copy, so a large value on the left branch doesn't affect the right. The counts come back up as return values, so information flows down as context and up as results. I seed with `root.val` so the root is automatically good, and I use `>=` because the definition says no ancestor is *greater than* — ties count. O(n) time, O(h) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why carry only the max, not all ancestors?" | **The question.** "No ancestor is greater" is exactly "≥ the max". Carrying a list makes it O(n·h). |
| "Why `>=` and not `>`?" | The definition forbids ancestors *greater than* X, so an equal ancestor is fine. The example's deep `3` depends on this. |
| "How does the left branch avoid affecting the right?" | The max is a parameter, passed by value — each subtree gets its own. A shared mutable variable would be wrong here. |
| "Count nodes where no ancestor is **smaller**?" | Carry the running **minimum** instead. Same structure. |
| "Return the good nodes, not the count?" | Accumulate them into a list rather than summing integers. |
| "What if the tree is 10⁵ deep?" | Recursion blows the stack. Convert to an explicit stack of `(node, max)` pairs — easy, because this is top-down. |
| "Top-down or bottom-up — how do you tell?" | Ask whether a node's answer depends on its **ancestors** (top-down, use parameters) or its **descendants** (bottom-up, use return values). |

**Traps:**

- **Using a shared mutable `max_so_far`** (an instance attribute or `nonlocal`). The left subtree's maximum would leak into the right. **This must be a parameter.**
- **`>` instead of `>=`** — undercounts every node tied with its path maximum.
- **Seeding with 0** instead of `root.val` or `-inf`. Node values can be negative, so a negative root would be miscounted.
- **Updating the max before the goodness test.** `new_max` would already include `node.val`, making every node trivially good.
- **Trying to compute it bottom-up.** Goodness depends on ancestors, which children know nothing about.
- **Passing the full ancestor list** — correct but O(n·h).

**This same move shows up in:** [Validate Binary Search Tree](98-validate-binary-search-tree.md) (the other top-down problem in this unit — carries bounds instead of a max) · [Maximum Depth](104-maximum-depth-of-binary-tree.md) (bottom-up, for contrast) · [Path Sum](../learning/07-trees.md) (carrying a running total down) · [dfs](../algorithms/dfs.md).

</details>
