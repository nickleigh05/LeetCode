# 144. Binary Tree Preorder Traversal

**Easy** · [LeetCode](https://leetcode.com/problems/binary-tree-preorder-traversal/) · [Solution file (no hints)](../../problems/0001-0499/144.py)

[📖 07. Trees lesson](../learning/07-trees.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 07. Trees problems](../rmap-practice/07-trees.md)

---

Given the root of a binary tree, return the **preorder** traversal of its nodes' values — node, left subtree, right subtree.

```
root = [1,null,2,3]  →  [1,2,3]
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
| "**preorder**" | Visit **node → left → right**. The node comes **first**, before either subtree |
| "return the values" | A flat list in visit order |
| `0 <= nodes` | Empty tree returns `[]` |
| follow-up: **iteratively** | The exercise — and preorder is by far the easiest of the three to do with a stack |

**Why preorder is the simplest iterative traversal.** In [inorder](94-binary-tree-inorder-traversal.md), a node must wait for its entire left subtree before being visited — so the stack holds *deferred* nodes and the code needs a dive-left inner loop. In preorder there's no deferral:

> **Visit the node the moment you reach it**, then deal with its children.

That means the stack only ever holds "subtrees I still need to process," never "nodes I've descended past but haven't recorded." The result is a flat loop with no nesting.

**The one thing to get right: push order.**

A stack is LIFO, so the **last** thing pushed is the **first** thing popped. Preorder needs the left child processed before the right, so:

> **Push right first, then left.**

```
pop node → visit it
push right   ← goes to the bottom
push left    ← goes on top, popped next ✅
```

Push left first and you'd get node, right, left — a mirrored traversal. This inversion trips people up precisely because it looks backwards.

🤔 **Before you open the next section:** if a stack pops the most recently pushed item, and you want the left child handled before the right, which one must you push first?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Recursion | Append, recurse left, recurse right | O(n) | O(h) implicit | ✅ Trivial, dodges the follow-up |
| **Explicit stack** | Pop, visit, push right then left | **O(n)** | **O(h)** | ✅ |
| Morris traversal | Thread the tree | O(n) | O(1) | ⚠️ Possible, but fiddlier than for inorder |

**The decision: an explicit stack, seeded with the root.**

The loop is four lines and has no inner loop, which is what makes preorder the natural starting point for learning iterative traversal:

```python
stack = [root]
while stack:
    node = stack.pop()
    if node:
        result.append(node.val)
        stack.append(node.right)
        stack.append(node.left)
```

**Why the `if node:` guard rather than checking before pushing.** This implementation pushes children **unconditionally** — including `None` — and filters them on pop. Two consequences:

- **Simpler push logic.** No `if node.left:` / `if node.right:` branches.
- **`root = None` works for free.** The stack starts as `[None]`, one iteration pops it, the guard rejects it, and the loop ends with `result = []`.

The alternative — guarding on push — is also correct and keeps the stack slightly smaller:

```python
if not root: return []
stack = [root]
while stack:
    node = stack.pop()
    result.append(node.val)
    if node.right: stack.append(node.right)
    if node.left:  stack.append(node.left)
```

Both are fine. The pop-side guard trades a marginally larger stack for fewer branches and no empty-tree special case.

**Why no dive-left loop.** Compare with [inorder](94-binary-tree-inorder-traversal.md), which needs `while curr: stack.append(curr); curr = curr.left`. That inner loop exists to defer nodes until their left subtrees complete. Preorder has no deferral, so the structure collapses to a single flat loop.

That contrast is the real lesson:

| | When is the node recorded? | Structure |
|---|---|---|
| **Preorder** | immediately on pop | flat loop ✅ |
| [Inorder](94-binary-tree-inorder-traversal.md) | after its left subtree | dive-left inner loop |
| [Postorder](145-binary-tree-postorder-traversal.md) | after **both** subtrees | reversal trick, or two stacks |

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
result = []
stack = [root]
```

**Seed the stack with the root.** Even if `root` is `None`, this is safe — the guard below handles it, so no empty-tree special case is needed.
→ [list-basics](../syntax/list-basics.md)

```python
while stack:
```

Process until nothing is pending. Unlike [inorder](94-binary-tree-inorder-traversal.md), a single condition suffices — there's no separate "still descending" state to track.
→ [while-loop](../syntax/while-loop.md) · [truthy-falsy-values](../syntax/truthy-falsy-values.md)

```python
    node = stack.pop()
    if node:
```

Pop the next subtree to process. `pop()` with no argument takes from the **end** — O(1).

The `if node:` filter discards the `None` placeholders pushed for absent children.
→ [list-methods](../syntax/list-methods.md) · [none-type](../syntax/none-type.md)

```python
        result.append(node.val)
```

**Visit immediately.** This is what makes it *preorder* — the node is recorded before either child is touched.

```python
        stack.append(node.right)
        stack.append(node.left)
```

**Right first, then left — and the order is the whole trick.**

The stack is LIFO, so `left` (pushed last) sits on top and is popped next. That produces node → left-subtree → right-subtree.

Reverse these two lines and you get node → right → left, a mirror-image traversal. It's the single most common bug here, and it produces plausible-looking output that's simply backwards.
→ [list-methods](../syntax/list-methods.md)

```python
return result
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:

        result = []
        stack = [root]

        while stack:
            node = stack.pop()
            if node:
                result.append(node.val)
                stack.append(node.right)
                stack.append(node.left)

        return result
```

</details>

<details>
<summary>The recursive version, for comparison</summary>

```python
class Solution:
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        result = []

        def visit(node):
            if not node:
                return
            result.append(node.val)
            visit(node.left)
            visit(node.right)

        visit(root)
        return result
```

The definition, written out directly.

</details>

**Trace it** — `root = [1,null,2,3]`:

```
1
 \
  2
 /
3
```

Here node 1 has `left = None`, `right = 2`; node 2 has `left = 3`, `right = None`.

| Step | Pop | Visit | Pushed (right, then left) | `stack` after | `result` |
|---|---|---|---|---|---|
| start | — | — | — | `[1]` | `[]` |
| 1 | 1 | ✅ 1 | `2` (right), `None` (left) | `[2, None]` | `[1]` |
| 2 | `None` | skip | — | `[2]` | `[1]` |
| 3 | 2 | ✅ 2 | `None` (right), `3` (left) | `[None, 3]` | `[1,2]` |
| 4 | 3 | ✅ 3 | `None`, `None` | `[None, None, None]` | `[1,2,3]` |
| 5–7 | `None` ×3 | skip | — | `[]` | `[1,2,3]` |

Return **`[1,2,3]`** ✅

Step 1 shows the push order doing its job: `2` goes on first and `None` lands on top, so the (empty) left side is dealt with before the right subtree — which is exactly left-before-right.

**A fuller tree** — `[1,2,3,4,5]`:

```
     1
    / \
   2   3
  / \
 4   5
```

| Pop | Visit | Stack after (top on the right) |
|---|---|---|
| 1 | 1 | `[3, 2]` |
| 2 | 2 | `[3, 5, 4]` |
| 4 | 4 | `[3, 5]` (+ two `None`s) |
| 5 | 5 | `[3]` (+ `None`s) |
| 3 | 3 | `[]` (+ `None`s) |

Return **`[1,2,4,5,3]`** ✅ — node, then the whole left subtree, then the right.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

Each real node is pushed once and popped once. `None` placeholders are also pushed and popped — at most `n + 1` of them, since a tree with `n` nodes has `n + 1` empty child slots — so the total stack operations are bounded by about `2(2n + 1)`, still **O(n)**.

Each operation is O(1): a pop, a truthiness check, an append, two pushes.

Optimal, since every node's value must appear in the output.

**The `None`-pushing cost** is the one thing to note: it roughly doubles the stack traffic compared with guarding on push. Asymptotically irrelevant, and the payoff is simpler code with no empty-tree special case. If constants mattered you'd guard before pushing.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(h)</summary>

**O(h)** where `h` is the tree height — plus the `None` placeholders, which add a constant factor.

| Tree shape | Stack depth |
|---|---|
| Balanced | **O(log n)** |
| Degenerate (all left children) | **O(n)** |

Note the asymmetry: because we push **right first**, a left-leaning tree accumulates one pending right-`None` per level, so the stack grows with depth. A right-leaning tree pops each node immediately after visiting, keeping the stack shallow.

**Excluding the output**, which is O(n) and required.

**Compared to the siblings:**

| | Extra structure needed |
|---|---|
| **Preorder** | one stack, flat loop |
| [Inorder](94-binary-tree-inorder-traversal.md) | one stack + a dive-left inner loop |
| [Postorder](145-binary-tree-postorder-traversal.md) | one stack + a final reverse (or two stacks) |

Preorder is the cheapest to implement iteratively, which is why it's the one to reach for when you need an explicit-stack DFS — for instance to avoid recursion limits on a deep tree, or to support early termination.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Preorder is node, left, right — the node is recorded the moment you reach it, so there's no deferral and the iterative version is a flat loop with no nesting. I seed a stack with the root, then pop, visit, and push the children. The key detail is pushing **right first, then left**, because a stack is LIFO — pushing left last means it's popped next, which gives left-before-right. I push children unconditionally including `None` and filter on pop, which keeps the push logic branch-free and makes an empty tree work without a special case. O(n) time, O(h) space — O(log n) balanced, O(n) for a degenerate tree."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Do it iteratively." | **The stated follow-up** — the stack version above. |
| "Why push right before left?" | LIFO. Pushing left last puts it on top, so it's popped first, giving left-before-right. |
| "How does this compare to inorder?" | Inorder must defer each node until its left subtree finishes, so it needs a dive-left inner loop. Preorder visits immediately, so the loop is flat. |
| "Postorder iteratively?" | Do a *node, right, left* traversal and **reverse** the result — see [problem 145](145-binary-tree-postorder-traversal.md). |
| "Why push `None` children?" | It avoids branches on push and handles `root = None` for free. Guarding on push is equally valid and uses a smaller stack. |
| "O(1) space?" | Morris traversal is adaptable to preorder, but it's noticeably fiddlier than the inorder version. |
| "When would you prefer iterative over recursive?" | Deep trees (Python's ~1000-frame limit), or when you need to pause/resume or terminate early. |

**Traps:**

- **Pushing left before right.** *The* bug — yields a mirrored traversal that looks superficially reasonable.
- **Appending after popping the children.** That's no longer preorder.
- **Forgetting the `if node:` guard** while still pushing `None`s. `AttributeError` on `node.val`.
- **Special-casing the empty tree unnecessarily.** With the pop-side guard, `stack = [root]` handles `None` already.
- **Using `pop(0)`.** That turns the stack into a queue and gives you BFS ([level order](102-binary-tree-level-order-traversal.md)) — and it's O(n) per call.
- **Assuming preorder output is sorted on a BST.** It isn't — that's **inorder**.

**This same move shows up in:** [Binary Tree Inorder Traversal](94-binary-tree-inorder-traversal.md) (the deferred-visit sibling) · [Binary Tree Postorder Traversal](145-binary-tree-postorder-traversal.md) (solved by reversing a modified preorder) · [Binary Tree Level Order Traversal](102-binary-tree-level-order-traversal.md) (swap the stack for a queue and you get BFS) · [Construct Binary Tree from Preorder and Inorder](105-construct-binary-tree-from-preorder-and-inorder-traversal.md) (why knowing the orders matters).

</details>

---
