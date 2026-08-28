# 145. Binary Tree Postorder Traversal

**Easy** · [LeetCode](https://leetcode.com/problems/binary-tree-postorder-traversal/) · [Solution file (no hints)](../../problems/0001-0499/145.py)

[📖 07. Trees lesson](../learning/07-trees.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 07. Trees problems](../rmap-practice/07-trees.md)

---

Given the root of a binary tree, return the **postorder** traversal of its nodes' values — left subtree, right subtree, node.

```
root = [1,null,2,3]  →  [3,2,1]
root = []            →  []
root = [1]           →  [1]
```

**Constraints:** `0 <= number of nodes <= 100` · `-100 <= Node.val <= 100`

**Follow-up:** the recursive solution is trivial — can you do it **iteratively**?

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**postorder**" | Visit **left → right → node**. The node comes **last**, after both subtrees |
| "return the values" | A flat list in visit order |
| `0 <= nodes` | Empty tree returns `[]` |
| follow-up: **iteratively** | ⚠️ Genuinely the hardest of the three orders to do with a stack — hence the trick below |

**Why postorder is the awkward one.** Compare when each order records a node:

| Order | Record the node… | Iterative difficulty |
|---|---|---|
| [Preorder](144-binary-tree-preorder-traversal.md) | **immediately** on arrival | trivial — flat loop |
| [Inorder](94-binary-tree-inorder-traversal.md) | after the **left** subtree | moderate — dive-left loop |
| **Postorder** | after **both** subtrees | **hard** — you must return to a node twice |

The difficulty is that a node must be revisited: once on the way down, and again after both children are done. A naive stack can't distinguish "first time here" from "children finished," so the honest solution needs either a visited-flag per entry or two stacks.

**The trick that avoids all of that:**

> Postorder is **left, right, node**.
> Reverse it and you get **node, right, left** — which is just preorder with the children swapped.

So: run a preorder-style traversal that visits **node, right, left**, then **reverse the result**.

```
target postorder:      left, right, node
reversed:              node, right, left   ← easy: flat stack loop
so: produce node,right,left  →  reverse  →  postorder ✅
```

That converts the hardest traversal into the easiest one plus an O(n) reverse. It's a genuinely elegant reduction, and worth recognizing as a general move: **when a traversal order is awkward, check whether its reverse is easy.**

🤔 **Before you open the next section:** if a stack pops the most recent push, and you want to produce *node, right, left*, which child should you push first?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Recursion | Recurse left, recurse right, append | O(n) | O(h) implicit | ✅ Trivial, dodges the follow-up |
| Stack with visited flags | Push `(node, visited)` pairs | O(n) | O(h) | ✅ Correct, more bookkeeping |
| Two stacks | Build reversed order on a second stack | O(n) | O(n) | ✅ Correct, extra structure |
| **One stack + final reverse** | Produce node-right-left, then reverse | **O(n)** | **O(h)** | ✅✅ Shortest and clearest |

**The decision: a preorder-shaped loop that emits *node, right, left*, followed by `result.reverse()`.**

Compare directly with [preorder](144-binary-tree-preorder-traversal.md) — the code is **identical except for two things**:

```python
# Preorder (node, left, right)          # Postorder (this solution)
stack.append(node.right)                stack.append(node.left)     ← swapped
stack.append(node.left)                 stack.append(node.right)    ← swapped
                                        result.reverse()            ← added
```

Swapping the pushes turns *node, left, right* into *node, right, left*; reversing that yields *left, right, node* — postorder.

**Why push left first here.** The stack is LIFO, so the last push is popped first. To emit *node, right, left* you need `right` popped before `left`, which means pushing **left first, then right** — the mirror of preorder's rule.

**Why the reversal is legitimate and not a hack.** It's an exact identity: for any binary tree,

> `reverse(node-right-left order)` **==** `left-right-node order`

Every node's position flips symmetrically, and because *node, right, left* is the exact mirror of *left, right, node*, the reversal restores it precisely. Worth being able to state that cleanly, because interviewers do ask "why does that work?"

**The alternative with visited flags**, for when someone rules out the reverse:

```python
stack = [(root, False)]
while stack:
    node, visited = stack.pop()
    if not node: continue
    if visited:
        result.append(node.val)          # second visit → record
    else:
        stack.append((node, True))       # revisit after children
        stack.append((node.right, False))
        stack.append((node.left, False))
```

Genuinely postorder with no reversal, at the cost of tuple bookkeeping and pushing each node twice. Know it, but write the reverse.

**Why `result.reverse()` over `result[::-1]`.** `reverse()` mutates in place — O(1) extra space. Slicing builds a second list — O(n). Minor, but the in-place version is the right habit.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
result = []
stack = [root]
```

Seed with the root. As in [preorder](144-binary-tree-preorder-traversal.md), `root = None` is safe — the guard below rejects it and the loop ends with `[]`.
→ [list-basics](../syntax/list-basics.md)

```python
while stack:
    node = stack.pop()
    if node:
```

Flat loop, no nesting. The `if node:` filter discards `None` placeholders pushed for absent children.
→ [while-loop](../syntax/while-loop.md) · [none-type](../syntax/none-type.md)

```python
        result.append(node.val)
```

Record on arrival — exactly like preorder. At this point `result` is being built in **node, right, left** order, which is *not* the answer yet.

```python
        stack.append(node.left)
        stack.append(node.right)
```

**Left first, then right — the mirror of preorder.**

LIFO means `right` (pushed last) pops first, producing *node, right, left*.

This is the only structural difference from [preorder](144-binary-tree-preorder-traversal.md), and swapping these two lines back would give you preorder instead — which, after the reverse below, would be wrong.
→ [list-methods](../syntax/list-methods.md)

```python
result.reverse()
return result
```

**The reversal that converts *node, right, left* into *left, right, node*.**

`reverse()` mutates in place in O(n) time and O(1) extra space. `result[::-1]` would allocate a second list.
→ [list-methods](../syntax/list-methods.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:

        result = []
        stack = [root]

        while stack:
            node = stack.pop()
            if node:
                result.append(node.val)
                stack.append(node.left)
                stack.append(node.right)

        result.reverse()
        return result
```

</details>

<details>
<summary>The recursive version, for comparison</summary>

```python
class Solution:
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        result = []

        def visit(node):
            if not node:
                return
            visit(node.left)
            visit(node.right)
            result.append(node.val)

        visit(root)
        return result
```

The definition written directly — note the append comes **after** both recursive calls.

</details>

**Trace it** — `root = [1,null,2,3]` (node 1 has right = 2; node 2 has left = 3):

| Step | Pop | Append | Pushed (left, then right) | `stack` after | `result` |
|---|---|---|---|---|---|
| start | — | — | — | `[1]` | `[]` |
| 1 | 1 | 1 | `None` (left), `2` (right) | `[None, 2]` | `[1]` |
| 2 | 2 | 2 | `3` (left), `None` (right) | `[None, 3, None]` | `[1,2]` |
| 3 | `None` | skip | — | `[None, 3]` | `[1,2]` |
| 4 | 3 | 3 | `None`, `None` | `[None, None, None]` | `[1,2,3]` |
| 5–7 | `None` ×3 | skip | — | `[]` | `[1,2,3]` |

Intermediate result: `[1,2,3]` — that's **node, right, left** order.

**Reverse** → **`[3,2,1]`** ✅

**A fuller tree** — `[1,2,3,4,5]`:

```
     1
    / \
   2   3
  / \
 4   5
```

| Pop | Append | `result` so far |
|---|---|---|
| 1 | 1 | `[1]` |
| 3 | 3 | `[1,3]` |
| 2 | 2 | `[1,3,2]` |
| 5 | 5 | `[1,3,2,5]` |
| 4 | 4 | `[1,3,2,5,4]` |

Intermediate = `[1,3,2,5,4]` (node, right, left). Reversed → **`[4,5,2,3,1]`** ✅

Check against the definition: left subtree postorder (`4,5,2`), then right subtree (`3`), then root (`1`) ✅

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

- Traversal: each node pushed once and popped once, plus up to `n + 1` `None` placeholders — O(n) stack operations, each O(1).
- Reversal: one O(n) pass.

Total O(n) + O(n) = **O(n)**.

The extra reverse pass is why this is sometimes described as "two passes," but both are linear so the class is unchanged.

**Compared to the visited-flag version:** that pushes each real node **twice** (once to descend, once to record), so it does roughly 2× the stack traffic but avoids the reversal. Same O(n); the reverse-based version is shorter and generally faster in practice, since `list.reverse()` is a tight C-level loop.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(h)</summary>

**O(h)** for the stack, where `h` is the tree height, plus O(1) for the in-place reversal.

| Tree shape | Stack depth |
|---|---|
| Balanced | **O(log n)** |
| Degenerate | **O(n)** |

**Excluding the output**, which is O(n) and required.

Note `result.reverse()` is **in place** — O(1) extra. Writing `return result[::-1]` would allocate a whole second list, doubling peak memory for no benefit.

**Comparison across the three orders:**

| | Iterative structure | Extra cost |
|---|---|---|
| [Preorder](144-binary-tree-preorder-traversal.md) | flat loop | none |
| [Inorder](94-binary-tree-inorder-traversal.md) | dive-left inner loop | none |
| **Postorder** | flat loop, pushes swapped | **one O(n) reverse** |

The reversal is the price of turning the hardest traversal into the easiest one. It's a very good trade — and the underlying idea (**solve the reverse problem, then flip the answer**) recurs well beyond trees.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Postorder is left, right, node — the awkward one iteratively, because a node has to be revisited after both subtrees finish, and a plain stack can't tell a first visit from a second. The trick is to notice that the **reverse** of postorder is node, right, left, which is just preorder with the children swapped — and that's a trivial flat stack loop. So I run the preorder skeleton but push **left before right**, so right pops first and I emit node-right-left, then reverse the result in place at the end. O(n) time, O(h) space. If reversing were off-limits I'd push `(node, visited)` pairs and record on the second pop, which is true postorder but pushes every node twice."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Do it iteratively." | **The stated follow-up** — swapped-push preorder plus a reverse. |
| "Why does the reversal work?" | `reverse(node-right-left)` is exactly `left-right-node`. The orders are precise mirrors. |
| "Do it **without** reversing." | Push `(node, visited)` tuples; on popping an unvisited node, re-push it as visited then push its children; record on the visited pop. |
| "How does this differ from preorder?" | Two lines: the child pushes are swapped, and a reverse is added. |
| "Why is postorder useful?" | Bottom-up computation — deleting a tree, evaluating expression trees, computing subtree sizes/heights. Anything where a node needs its children's results first. |
| "`result.reverse()` vs `result[::-1]`?" | `reverse()` is in place, O(1) extra. Slicing allocates a second list. |
| "Two stacks instead?" | Push visited nodes onto a second stack, then pop it all off. Same idea, O(n) extra space instead of an in-place reverse. |

**Traps:**

- **Pushing right before left.** That gives node-left-right, which reverses to right-left-node — not postorder. The push order must be the *mirror* of preorder's.
- **Forgetting the reverse.** You'd return node-right-left, which looks like a plausible traversal and is wrong.
- **Reversing with `[::-1]` and discarding it.** `result[::-1]` returns a new list; it must be returned or assigned.
- **Recording on the wrong pop in the visited-flag variant.** Append only when the flag says the children are done.
- **Omitting the `if node:` guard** while pushing `None`s. `AttributeError`.
- **Assuming postorder works for BST-sorted output.** That's **inorder**.

**This same move shows up in:** [Binary Tree Preorder Traversal](144-binary-tree-preorder-traversal.md) (the near-identical skeleton this modifies) · [Binary Tree Inorder Traversal](94-binary-tree-inorder-traversal.md) (the third order, needing a dive-left loop) · [Maximum Depth of Binary Tree](104-maximum-depth-of-binary-tree.md) (a bottom-up computation, the natural home of postorder) · [Diameter of Binary Tree](543-diameter-of-binary-tree.md) (postorder logic — combine children's results at each node).

</details>

---
