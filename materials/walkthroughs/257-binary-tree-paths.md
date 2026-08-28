# 257. Binary Tree Paths

**Easy** · [LeetCode](https://leetcode.com/problems/binary-tree-paths/) · [Solution file (no hints)](../../problems/0001-0499/257.py)

[📖 07. Trees lesson](../learning/07-trees.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 07. Trees problems](../rmap-practice/07-trees.md)

---

Given the root of a binary tree, return **all root-to-leaf paths** in any order, each formatted as `"1->2->5"`. A **leaf** is a node with no children.

```
root = [1,2,3,null,5]  →  ["1->2->5", "1->3"]
root = [1]             →  ["1"]
```

**Constraints:** `1 <= number of nodes <= 100` · `-100 <= Node.val <= 100`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**root-to-leaf**" | ⚠️ Paths must start at the root **and end at a leaf** — the same distinction as [Path Sum](112-path-sum.md) |
| "**all** paths" | Enumerate every one, so no early exit |
| "a **leaf** has no children" | Both `left` and `right` are `None` — a one-child node is not a leaf |
| formatted `"1->2->5"` | Join values with `"->"`; the output is strings, not lists |
| "in any order" | No sorting required |
| `1 <= nodes` | Never empty, though guarding costs nothing |

**Why this is the natural next step after [Path Sum](112-path-sum.md).** That problem asked *does a qualifying path exist?* — a boolean, answerable while descending. This asks for **the paths themselves**, which means you must **carry state down** and **record it at each leaf**.

That's the essence of backtracking on a tree:

> Build a partial path as you descend. When you reach a leaf, the path is complete — record it. Then **undo** your addition before returning, so the sibling branch starts from a clean state.

**The `None`-vs-leaf distinction, again.** As in [Path Sum](112-path-sum.md) and [Minimum Depth](111-minimum-depth-of-binary-tree.md), a node with one child is **not** a leaf. If you recorded a path whenever you hit `None`, then this tree:

```
  1
 /
2
```

would produce `["1->2"]` (correct, from node 2's `None` children) — but node 1's *right* `None` would also fire, emitting a bogus `"1"`. Recording must happen at **leaves**, not at empty children.

**Why the output is strings.** The `"->"` join is cosmetic, but it dictates one real decision: accumulate values as a **list** and join once at the leaf, rather than concatenating strings all the way down. Same reasoning as [Merge Strings Alternately](1768-merge-strings-alternately.md) — repeated string concatenation is O(k²).

🤔 **Before you open the next section:** if you add the current node to a shared path list before recursing into both children, what must happen between the two recursive calls?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| **DFS with backtracking** | Shared list; append, recurse, pop | **O(n·h)** | **O(h)** working | ✅ Classic, minimal allocation |
| DFS passing a new list | Pass `path + [val]` to each child | O(n·h) | O(h) per call | ✅ Simpler, more allocation |
| DFS passing a string | Pass `path + "->" + str(val)` | O(n·h²) | O(h) | ⚠️ Repeated concatenation |
| BFS with paths in the queue | Queue `(node, path)` pairs | O(n·h) | **O(w·h)** | ⚠️ Correct, heavier |

**The decision: DFS carrying a path list, with backtracking.**

The three-step rhythm — and this is the pattern to internalize, because it recurs throughout [Backtracking](../learning/10-backtracking.md):

```python
path.append(node.val)          # choose
    ... recurse into children ...   # explore
path.pop()                     # un-choose  ← the backtrack
```

**Why the `pop()` matters.** The list is **shared** across the whole traversal. After finishing the left subtree, the path still holds everything that branch appended. Without popping, the right subtree would inherit that garbage and produce paths that never existed.

**Why passing a new list is a legitimate alternative:**

```python
def dfs(node, path):
    if not node: return
    path = path + [str(node.val)]     # new list — nothing to undo
    if not node.left and not node.right:
        result.append("->".join(path))
        return
    dfs(node.left, path)
    dfs(node.right, path)
```

Each call gets its own list, so there's no shared state and no `pop()` needed. It's easier to reason about and harder to get wrong — at the cost of allocating a fresh O(h) list per node. At `n = 100` that's irrelevant; at scale, backtracking wins.

**Say both**, and note the trade: *"backtracking avoids the per-node allocation; passing copies avoids the shared-state bug. At these constraints either is fine."*

**Why accumulate a list rather than a string.** Building `"1->2->5"` by concatenation at every level re-copies the whole prefix each time — O(h²) per path. Collecting values in a list and calling `"->".join(...)` **once** at each leaf is O(h) per path. Strings are [immutable](../syntax/string-immutability.md) in Python, so concatenation always copies.

**Why not BFS?** It works — enqueue `(node, path_so_far)` — but each queue entry carries its own path copy, so memory is O(w·h) rather than O(h). DFS naturally matches the "one path at a time" structure.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
def binaryTreePaths(self, root: Optional[TreeNode]) -> List[str]:
    result = []
    path = []
```

- `result` — the finished path strings
- `path` — the current root-to-node values, shared and mutated during traversal

→ [list-basics](../syntax/list-basics.md)

```python
    def dfs(node):
        if not node:
            return
```

**Empty subtree → nothing to do.** Note this returns without recording anything — recording happens only at leaves, which is what prevents the bogus `"1"` case described above.
→ [function-basics](../syntax/function-basics.md) · [closures](../syntax/closures.md)

```python
        path.append(str(node.val))
```

**Choose.** Add this node to the current path.

Converting to `str` here means the final `join` needs no conversion pass.
→ [type-conversion](../syntax/type-conversion.md) · [list-methods](../syntax/list-methods.md)

```python
        if not node.left and not node.right:
            result.append("->".join(path))
```

**At a leaf, the path is complete — record it.**

`and`, not `or` — a leaf has **both** children absent.

`"->".join(path)` builds the string in one O(h) pass. This is the only place a result is emitted.
→ [logical-operators](../syntax/logical-operators.md) · [string-join-slice](../syntax/string-join-slice.md)

```python
        else:
            dfs(node.left)
            dfs(node.right)
```

**Explore both subtrees.** The `else` skips recursion at leaves, though recursing into two `None`s would be harmless — the guard just makes the intent explicit.

```python
        path.pop()
```

**Un-choose — the backtrack.**

Remove this node before returning to the parent, so the sibling branch sees the path exactly as it was.

This line runs on **every** exit path, including after a leaf is recorded. Placing it outside the `if/else` is what guarantees that.
→ [list-methods](../syntax/list-methods.md)

```python
    dfs(root)
    return result
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def binaryTreePaths(self, root: Optional[TreeNode]) -> List[str]:

        result = []
        path = []

        def dfs(node):
            if not node:
                return

            path.append(str(node.val))

            if not node.left and not node.right:
                result.append("->".join(path))
            else:
                dfs(node.left)
                dfs(node.right)

            path.pop()

        dfs(root)
        return result
```

</details>

<details>
<summary>The copy-passing version (no backtracking needed)</summary>

```python
class Solution:
    def binaryTreePaths(self, root: Optional[TreeNode]) -> List[str]:
        result = []

        def dfs(node, path):
            if not node:
                return

            path = path + [str(node.val)]     # a fresh list each call

            if not node.left and not node.right:
                result.append("->".join(path))
                return

            dfs(node.left, path)
            dfs(node.right, path)

        dfs(root, [])
        return result
```

No shared state, so no `pop()` — at the cost of an O(h) allocation per node.

</details>

**Trace it** — `root = [1,2,3,null,5]`:

```
    1
   / \
  2   3
   \
    5
```

| Step | Node | `path` after append | Leaf? | Action |
|---|---|---|---|---|
| 1 | 1 | `[1]` | no | recurse left |
| 2 | 2 | `[1,2]` | no (has right child) | recurse left → `None`, returns |
| 3 | 5 | `[1,2,5]` | ✅ | record **`"1->2->5"`**, then pop → `[1,2]` |
| 4 | — | `[1]` | — | node 2 pops on exit |
| 5 | 3 | `[1,3]` | ✅ | record **`"1->3"`**, then pop → `[1]` |
| 6 | — | `[]` | — | node 1 pops on exit |

Return **`["1->2->5", "1->3"]`** ✅

**Step 4 is the backtrack doing its job.** After node 2's subtree finished, `path` was `[1,2]`; popping node 2 restored it to `[1]`, so node 3 started from the correct prefix. Without that pop, step 5 would have produced `"1->2->3"` — a path that doesn't exist in the tree.

**The one-child case** — `[1,2]` (node 1 has only a left child):

| Node | `path` | Leaf? | Action |
|---|---|---|---|
| 1 | `[1]` | no — `node.right` is `None` but `node.left` exists | recurse |
| 2 | `[1,2]` | ✅ both children `None` | record `"1->2"` |

Return `["1->2"]` ✅ — and node 1's `None` right child returned immediately at the base case without emitting anything, which is exactly why the leaf check must test both children rather than firing at every `None`.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n · h)</summary>

**O(n · h)**, where `h` is the tree height.

Two components:

- **Traversal:** every node visited once, with O(1) append/pop — O(n)
- **String building:** at each leaf, `"->".join(path)` costs O(h) to build a path of length ≤ `h`

With up to `n/2` leaves in a balanced tree, the joins total O(n · h) — which **dominates** the traversal.

| Tree shape | Cost |
|---|---|
| Balanced | O(n log n) |
| Degenerate | O(n) — only one leaf, one path of length `n` |

**This is optimal**, because the *output itself* is that large: the combined length of all path strings is Θ(n·h) in the worst case. You cannot produce Θ(n·h) characters in less time.

**The version to avoid:** passing a concatenated string down (`path + "->" + str(val)`) rebuilds the whole prefix at every level, giving O(h) work per node along each path and **O(n·h²)** overall. Accumulate into a list; join once.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(h) working, O(n·h) output</summary>

**O(h) auxiliary** — the recursion stack plus the shared `path` list, both bounded by the tree height.

**O(n·h) for the output**, which the problem requires.

| | Working space |
|---|---|
| **Backtracking (shared list)** | **O(h)** — one list, reused |
| Copy-passing | O(h) per frame → O(h) live, but O(n·h) total allocation churn |
| BFS with paths in the queue | **O(w·h)** — every queued node carries a path copy |

**Why backtracking is the memory-efficient choice.** A single list is mutated in place, so at any moment only one root-to-node path exists. The copy-passing version keeps a distinct list alive per active frame — the same O(h) depth, but with `n` allocations over the run rather than one.

At `n = 100` this is immaterial and clarity should win. The pattern matters because it's the foundation of [Unit 10](../rmap-practice/10-backtracking.md), where search spaces are exponential and the per-step allocation genuinely dominates:

> **choose → explore → un-choose.** One mutable state object, restored on the way out.

The same rhythm drives [Subsets](78-subsets.md), [Permutations](46-permutations.md), [Combination Sum](39-combination-sum.md), and [N-Queens](51-n-queens.md).

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "This needs the actual paths, not just a yes/no, so I carry state down and record it at each leaf. I do a DFS with a shared path list: append the node on the way in, and if it's a leaf — both children `None` — I join the path with `\"->\"` and record it; otherwise I recurse into both children. Then I **pop** before returning, so the sibling branch sees the path as it was. That's the choose–explore–un-choose backtracking rhythm. Recording must happen at leaves rather than at `None` children, or a one-child node would emit a bogus partial path. I accumulate values in a list and join once per leaf rather than concatenating strings on the way down, which would be quadratic. O(n·h) time — dominated by building the output, which is itself that large — and O(h) working space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why pop after recursing?" | **The key question.** The list is shared; without the pop, the right subtree inherits the left branch's leftovers. |
| "Avoid backtracking entirely?" | Pass `path + [val]` — a fresh list per call, so nothing needs undoing. Simpler, but O(h) allocation per node. |
| "Why not build the string as you descend?" | Concatenation copies the prefix each time — O(n·h²). Join once at the leaf. |
| "Only paths summing to a target?" | [Path Sum II](https://leetcode.com/problems/path-sum-ii/) — same skeleton, plus a running sum checked at the leaf. |
| "Why record at leaves rather than at `None`?" | A one-child node would emit a partial path. `[1,2]` would wrongly yield `\"1\"`. |
| "Do it iteratively." | Stack of `(node, path_string)` pairs — correct, but each entry carries its own path. |
| "Count the paths instead of listing them?" | Count the leaves — O(n) time, O(h) space, no strings needed. |

**Traps:**

- **Forgetting `path.pop()`.** *The* bug — paths bleed across branches and you get routes that don't exist.
- **Placing the pop inside the `else`.** It must run on every exit, including after recording a leaf.
- **Recording at `None` instead of at leaves.** Emits partial paths for one-child nodes.
- **Using `or` in the leaf test.** Misclassifies one-child nodes as leaves.
- **Concatenating strings down the tree.** O(n·h²) instead of O(n·h).
- **Appending `path` itself to `result`.** You'd store a reference to the shared list, and every entry would end up identical (and empty). Join it into a string, or append `path[:]`.

**This same move shows up in:** [Path Sum](112-path-sum.md) (the same root-to-leaf structure, returning a boolean instead of the paths) · [Subsets](78-subsets.md) and [Permutations](46-permutations.md) (the choose–explore–un-choose rhythm on non-tree search spaces) · [Combination Sum](39-combination-sum.md) (backtracking with a shared partial solution) · [Minimum Depth of Binary Tree](111-minimum-depth-of-binary-tree.md) (the same `None`-is-not-a-leaf distinction).

</details>

---
