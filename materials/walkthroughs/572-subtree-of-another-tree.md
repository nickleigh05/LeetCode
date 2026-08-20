# 572. Subtree of Another Tree

**Easy** · [LeetCode](https://leetcode.com/problems/subtree-of-another-tree/) · [Solution file (no hints)](../../problems/0500-0999/572.py)

[📖 08. Trees lesson](../learning/08-trees.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 08. Trees problems](../rmap-practice/08-trees.md)

---

Given the roots of two binary trees `root` and `subRoot`, return `true` if there is a subtree of `root` with the **same structure and node values** as `subRoot`.

A subtree of a tree consists of a node in that tree **and all of its descendants** — the whole thing, not a partial match.

```
root = [3,4,5,1,2], subRoot = [4,1,2]        →  true
root = [3,4,5,1,2,null,null,null,null,0], subRoot = [4,1,2]  →  false
```

**Constraints:** `1 <= root nodes <= 2000` · `1 <= subRoot nodes <= 1000` · `-10⁴ <= Node.val <= 10⁴`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "a node **and all of its descendants**" | ⚠️ **The whole subtree**, not a partial match. The second example fails precisely because an extra node `0` hangs below |
| "same structure **and** values" | Exactly the [Same Tree](100-same-tree.md) test |
| "**a** subtree of `root`" | Any node could be the match — you must try them all |
| n ≤ 2000, m ≤ 1000 | O(n·m) = 2·10⁶ — comfortably fast |

The decomposition is two questions stacked:

1. *"Are these two trees identical?"* → [problem 100](100-same-tree.md), already solved.
2. *"Is `subRoot` identical to the tree rooted at **some** node of `root`?"* → try question 1 at every node.

So the shape is: **walk `root`; at each node, run the same-tree check.**

**The trap in the second example is worth staring at.** `root`'s node 4 has children `[1, 2]` — matching `subRoot` — *except* node 1 has an extra child `0`. A partial-match check would say yes; the full same-tree check correctly says no, because "subtree" means *everything below that node*.

**The second insight — matching values aren't enough.** Finding a node whose value equals `subRoot.val` is necessary but not sufficient; you still have to verify the entire structure below it. And a tree can contain many nodes with the same value, so you can't stop at the first one.

🤔 **Before you open the next section:** you're combining two recursions — one walking `root` and one comparing two trees. Which logical operator joins "match here" with "match somewhere in a child"?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| **DFS + same-tree check at each node** | Try [100](100-same-tree.md) everywhere | **O(n·m)** | ✅ |
| Serialize both, substring search | Turn trees into strings, check containment | O(n + m) with KMP | ✅ Faster, but needs careful encoding |
| Compare only where values match | Skip nodes whose value ≠ `subRoot.val` | O(n·m) worst case | ⚠️ A useful optimization, same bound |

**The decision: DFS over `root`, calling the same-tree check at every node.**

Two recursions, doing different jobs — and keeping them separate is what makes the solution readable:

- **`same_tree(p, q)`** — are these two trees identical? Pure comparison, from [problem 100](100-same-tree.md).
- **`isSubtree(root, subRoot)`** — walk `root` looking for a starting point.

The outer logic per node:

```
match here?  OR  match in the left subtree?  OR  match in the right subtree?
```

**`or` is the right combiner** — you need the match to exist *somewhere*, not everywhere. (Contrast with [100](100-same-tree.md), where `and` was correct because *every* corresponding pair had to match.) And `or` short-circuits, so once a match is found, nothing further is explored.
→ [logical-operators](../syntax/logical-operators.md)

**⚠️ Don't fuse the two recursions.** A tempting-but-wrong shortcut is to compare nodes and, on mismatch, "keep descending in `root`" within the same function. That conflates *searching for a start point* with *verifying a match*, and produces false positives on partial matches. **Two functions, two jobs.**

**The serialization alternative is genuinely better asymptotically.** Serialize both trees with explicit null markers and value delimiters, then ask whether `subRoot`'s string is a substring of `root`'s — O(n + m) with [KMP](../algorithms/kmp.md). The catch is that a sloppy encoding creates false matches (e.g. value `12` matching inside `123`), so you need delimiters *and* null markers. **Worth naming as the optimal answer; the O(n·m) version is what you'd write.**

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
def same_tree(p, q):
    if not p and not q:
        return True
    if not p or not q or p.val != q.val:
        return False
    return same_tree(p.left, q.left) and same_tree(p.right, q.right)
```

**[Problem 100](100-same-tree.md), verbatim** — just with the three base cases compressed into two lines.

Note the ordering is still preserved: both-null first, then the combined "one is null **or** values differ" check. `or` short-circuits left to right, so `p.val` is only evaluated once both `not p` and `not q` have failed — meaning both nodes exist. **The safety comes from the evaluation order.**
→ [function-basics](../syntax/function-basics.md) · [logical-operators](../syntax/logical-operators.md) · [recursion-basics](../syntax/recursion-basics.md)

```python
if not root:
    return subRoot is None
```

**Base case for the search.** Ran out of tree to search.

If `subRoot` is also `None`, an empty tree is trivially a subtree → `True`. Otherwise there's nowhere left to look → `False`.

*(The constraints guarantee `subRoot` is non-empty, so this reduces to `False` in practice — but writing it this way is correct in general and costs nothing.)*
→ [truthy-falsy-values](../syntax/truthy-falsy-values.md) · [identity-operators](../syntax/identity-operators.md)

```python
if same_tree(root, subRoot):
    return True
```

**Try matching at the current node.** If the tree rooted *here* is identical to `subRoot`, we're done.

This is the full-structure check — which is why the extra-node case in example 2 correctly fails.
→ [if-return](../syntax/if-return.md)

```python
return self.isSubtree(root.left, subRoot) or self.isSubtree(root.right, subRoot)
```

**No match here, so search the children.** `or` because a match on *either* side is enough.

The short-circuit means that once the left subtree finds a match, the right is never searched.

Note `subRoot` is passed **unchanged** to both calls — you're moving the search position within `root` while the pattern stays fixed. Accidentally descending into `subRoot` too is the classic error.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:

        def same_tree(p, q):
            if not p and not q:
                return True
            if not p or not q or p.val != q.val:
                return False
            return same_tree(p.left, q.left) and same_tree(p.right, q.right)

        if not root:
            return subRoot is None
        if same_tree(root, subRoot):
            return True
        return self.isSubtree(root.left, subRoot) or self.isSubtree(root.right, subRoot)
```

</details>

**Trace it** — `root = [3,4,5,1,2]`, `subRoot = [4,1,2]`:

```
root:        3              subRoot:   4
           /   \                      / \
          4     5                    1   2
         / \
        1   2
```

| Node visited | `same_tree(node, subRoot)` | Action |
|---|---|---|
| 3 | 3 ≠ 4 → **False** | search children |
| **4** | 4 = 4, then (1,1) ✅ and (2,2) ✅ → **True** | **`return True`** ✅ |

The right subtree (node 5) is never searched — `or` short-circuited.

**And the false case** — `root`'s node 1 has an extra child `0`:

```
root:        3              subRoot:   4
           /   \                      / \
          4     5                    1   2
         / \
        1   2
       /
      0
```

| Node | `same_tree` | Why |
|---|---|---|
| 3 | False | 3 ≠ 4 |
| **4** | **False** | 4=4 ✅, but comparing node 1: `root`'s 1 has left child **0** while `subRoot`'s 1 has `None` → one-is-null → False |
| 1, 2, 0, 5 | False | values don't match 4 |

Result: **`False`** ✅ — exactly the "and all of its descendants" requirement being enforced.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n · m)</summary>

**O(n · m)**, where n = nodes in `root`, m = nodes in `subRoot`.

- The outer DFS visits each of n nodes.
- At each, `same_tree` costs up to **O(m)** — it can't exceed the size of `subRoot`, since it returns as soon as the structures diverge.

n × O(m) = **O(n·m)** → 2000 × 1000 = 2·10⁶ at the limits. Fast.

**Why the worst case is rarely hit.** `same_tree` usually returns on the first value comparison — a mismatch at the root of the check is O(1). The full O(m) only occurs when a large portion genuinely matches. A pathological input like `root` = 2000 nodes all valued `1` and `subRoot` = 1000 nodes all valued `1` would actually reach it.

**A free optimization worth mentioning:** skip the `same_tree` call unless `root.val == subRoot.val`. Same worst case, but it eliminates almost all calls on real inputs.

**The O(n + m) alternative:** serialize both trees (with null markers and delimiters) and run [KMP](../algorithms/kmp.md) substring search. Genuinely better asymptotically — worth naming as the optimal approach even if you write the simpler one.

**⚠️ Note this breaks the unit's pattern.** Every previous tree problem was O(n) because each node did O(1) work. Here each node does O(m) work. **"Visit every node" doesn't automatically mean O(n)** — check what happens *at* each node.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(h)</summary>

**O(h)** where h is the height of `root` — **O(log n)** balanced, **O(n)** skewed.

Two recursions are in play, but they don't stack multiplicatively: when `same_tree` runs, it goes at most `h_sub` deep, and it **returns before** the outer recursion descends further. So the peak stack is:

```
O(h_root + h_sub)  =  O(h)
```

not `O(h_root × h_sub)`. Worth being precise about, since "two nested recursions" sounds like it should multiply — but they're sequential in time, not nested in the stack.

Nothing is allocated; both trees are read-only.

**Compared to the serialization approach:** that builds two full strings, **O(n + m)** space. So the trade is explicit:

| Approach | Time | Space |
|---|---|---|
| **DFS + same-tree** | O(n·m) | **O(h)** |
| Serialize + KMP | **O(n+m)** | O(n+m) |

The usual shape — the faster algorithm buys its speed with memory.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "A subtree means a node *and all of its descendants*, so this is really 'is `subRoot` identical to the tree rooted at some node of `root`?' I already know how to check whether two trees are identical, so I keep that as a separate helper and walk `root`, trying it at every node. The outer logic is: does it match here, or in the left subtree, or in the right — combined with `or`, since I only need a match somewhere, and it short-circuits once found. Keeping the two recursions separate matters: fusing them would conflate searching for a start point with verifying a match, and would accept partial matches. O(n·m) time, since the same-tree check costs up to m at each of n nodes, and O(h) space. There's an O(n+m) alternative that serializes both trees and does a KMP substring search, but the encoding needs null markers and delimiters to avoid false matches."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Can you beat O(n·m)?" | Serialize with null markers and delimiters, then KMP substring search → O(n+m) time, O(n+m) space. |
| "Why do the serialized strings need null markers?" | Without them, structurally different trees serialize identically — the same ambiguity as [Encode and Decode Strings](271-encode-and-decode-strings.md). Delimiters also prevent `12` matching inside `123`. |
| "Optimize the common case." | Only call `same_tree` when `root.val == subRoot.val`. Same worst case, far fewer calls in practice. |
| "Why `or` here but `and` in Same Tree?" | Here a match *somewhere* suffices; there *every* corresponding pair had to match. |
| "What if a partial match counted?" | A different, easier problem — stop descending in `subRoot` once it's exhausted. Read the definition carefully; this problem explicitly wants the whole subtree. |
| "What if `subRoot` were empty?" | Conventionally `True` — an empty tree is a subtree of anything. The constraints exclude it, but say what you'd do. |

**Traps:**

- **Fusing the two recursions** into one function. Produces false positives on partial matches — the defining error here.
- **Descending into `subRoot`** in the outer search. `subRoot` is the fixed pattern; only the position in `root` moves.
- **Using `and` instead of `or`** in the combine — you'd require a match in *both* subtrees.
- **Stopping at the first node whose value matches.** Values repeat; you must keep searching if the full check fails.
- **Accepting a partial match** — example 2's extra node exists precisely to catch this.
- **Serializing without markers**, creating false substring matches.

**This same move shows up in:** [Same Tree](100-same-tree.md) (the helper, verbatim) · [Invert Binary Tree](226-invert-binary-tree.md) (the DFS skeleton) · [kmp](../algorithms/kmp.md) (the O(n+m) alternative) · [Serialize and Deserialize Binary Tree](297-serialize-and-deserialize-binary-tree.md) (unambiguous tree encoding).

</details>

---
