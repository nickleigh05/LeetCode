# 94. Binary Tree Inorder Traversal

**Easy** · [LeetCode](https://leetcode.com/problems/binary-tree-inorder-traversal/) · [Solution file (no hints)](../../problems/0001-0499/94.py)

[📖 07. Trees lesson](../learning/07-trees.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 07. Trees problems](../rmap-practice/07-trees.md)

---

Given the root of a binary tree, return the **inorder** traversal of its nodes' values — left subtree, node, right subtree.

```
root = [1,null,2,3]  →  [1,3,2]
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
| "**inorder**" | Visit **left → node → right**. The node is processed *between* its subtrees |
| "return the values" | A flat list, in visit order |
| `0 <= nodes` | Empty tree returns `[]` |
| follow-up: **iteratively** | ⚠️ The actual exercise. Recursion is four lines; the iterative version teaches how recursion works |

**The three traversal orders** differ only in *when* you record the node relative to its children:

| Order | Sequence | On a BST |
|---|---|---|
| **Preorder** | node, left, right | — |
| **Inorder** | left, **node**, right | ⚠️ yields values in **sorted order** |
| **Postorder** | left, right, node | — |

That BST property is why inorder matters more than the other two: it's the reason [Validate Binary Search Tree](98-validate-binary-search-tree.md) and [Kth Smallest Element in a BST](230-kth-smallest-element-in-a-bst.md) both reduce to an inorder walk.

**Why the iterative version is the interesting one.** Recursion is:

```python
def inorder(node):
    if not node: return
    inorder(node.left)
    result.append(node.val)
    inorder(node.right)
```

Correct and obvious — but the call stack is doing invisible work. The iterative version makes that stack **explicit**, and understanding it is what makes [Kth Smallest in a BST](230-kth-smallest-element-in-a-bst.md) solvable with early termination (you can stop after `k` nodes, which recursion can't do cleanly).

**The mechanism.** Inorder means you can't process a node until its entire left subtree is done. So:

1. Walk as far **left** as possible, pushing every node onto a stack
2. Pop — that node's left subtree is exhausted, so **visit it**
3. Move to its **right** child and repeat

The stack holds nodes whose left subtrees are finished but whose right subtrees haven't been explored — "unfinished business," exactly what the call stack would hold.

🤔 **Before you open the next section:** when you pop a node off the stack, what do you know about the part of the tree you've already visited?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Recursion | Natural definition | O(n) | O(h) implicit stack | ✅ Trivial, but dodges the follow-up |
| **Explicit stack** | Simulate the call stack | **O(n)** | **O(h)** | ✅ The intended answer |
| Morris traversal | Thread the tree using spare right pointers | O(n) | **O(1)** | ✅✅ Optimal space; mutates the tree temporarily |

**The decision: an explicit stack.**

The loop condition `while curr or stack` is the part worth understanding — it encodes **two different reasons to keep going**:

- **`curr` is non-`None`** — there's a subtree still to descend into
- **`stack` is non-empty** — there are nodes waiting to be visited, even if `curr` is `None`

Either alone is insufficient. After popping a leaf and setting `curr = curr.right` (which is `None`), `curr` is falsy — but the stack still holds ancestors that need visiting. Conversely, at the very start the stack is empty but `curr` is the root.

**The inner `while curr` loop** dives all the way left, pushing as it goes. This is the "go as deep as possible before doing anything" behaviour that recursion gets for free.

**Why `curr = curr.right` after popping.** Once you've visited a node, its left subtree and the node itself are done — only the right subtree remains. Setting `curr` to the right child restarts the dive-left process on that subtree. If the right child is `None`, the outer loop simply pops the next ancestor.

**Morris traversal**, worth naming for the follow-up-to-the-follow-up: it achieves **O(1) space** by temporarily rewiring each node's rightmost left-descendant to point back at the node, creating threads that let you return without a stack. It's O(n) time and genuinely clever, but it mutates the tree during traversal (restoring it as it goes), which is unacceptable in concurrent settings. Mention it as the O(1) answer; write the stack version.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
result = []
stack = []
curr = root
```

- `result` — the output, in visit order
- `stack` — nodes whose left subtrees are finished but which haven't been visited yet
- `curr` — the node we're currently descending from

→ [list-basics](../syntax/list-basics.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
while curr or stack:
```

**Two termination conditions in one.**

- `curr` non-`None` — a subtree remains to descend
- `stack` non-empty — ancestors remain to visit

The traversal is finished only when **both** are exhausted. Using `while stack` alone would exit immediately (the stack starts empty); using `while curr` alone would exit as soon as you hit a leaf's `None` child.
→ [while-loop](../syntax/while-loop.md) · [truthy-falsy-values](../syntax/truthy-falsy-values.md)

```python
    while curr:
        stack.append(curr)
        curr = curr.left
```

**Dive all the way left**, pushing every node passed.

This is the "defer the node until its left subtree is done" rule made explicit. When this inner loop ends, `curr` is `None` and the stack's top is the **leftmost unvisited node**.
→ [list-methods](../syntax/list-methods.md)

```python
    curr = stack.pop()
    result.append(curr.val)
```

**Visit.** The popped node's left subtree is fully processed — that's exactly what being on the stack means — so now is the moment to record it.

This placement is what makes it *inorder*. Recording before the dive would give preorder.

```python
    curr = curr.right
```

**Move right.** The node and its left subtree are done; only the right subtree remains.

If it's `None`, the next iteration's inner `while` does nothing and we immediately pop the next ancestor — which is precisely the correct behaviour.

```python
return result
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:

        result = []
        stack = []
        curr = root

        while curr or stack:
            while curr:
                stack.append(curr)
                curr = curr.left

            curr = stack.pop()
            result.append(curr.val)
            curr = curr.right

        return result
```

</details>

<details>
<summary>The recursive version, for comparison</summary>

```python
class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        result = []

        def visit(node):
            if not node:
                return
            visit(node.left)
            result.append(node.val)
            visit(node.right)

        visit(root)
        return result
```

Three lines of logic, and the shape of the definition is visible. But the stack is implicit, and you can't stop early — which matters for [Kth Smallest in a BST](230-kth-smallest-element-in-a-bst.md).

</details>

**Trace it** — `root = [1,null,2,3]`, i.e.

```
1
 \
  2
 /
3
```

| Step | `curr` | Action | `stack` | `result` |
|---|---|---|---|---|
| 1 | 1 | dive left: push 1, `curr` = `None` | `[1]` | `[]` |
| 2 | `None` | pop 1, **visit**, `curr` = 1.right = 2 | `[]` | `[1]` |
| 3 | 2 | dive left: push 2, `curr` = 3; push 3, `curr` = `None` | `[2,3]` | `[1]` |
| 4 | `None` | pop 3, **visit**, `curr` = 3.right = `None` | `[2]` | `[1,3]` |
| 5 | `None` | pop 2, **visit**, `curr` = 2.right = `None` | `[]` | `[1,3,2]` |
| 6 | `None` | both empty → exit | `[]` | `[1,3,2]` |

Return **`[1,3,2]`** ✅

Step 5 is where the `or stack` clause earns its place: `curr` was `None`, but node 2 was still waiting. A `while curr` condition would have stopped at step 4 and returned `[1,3]`.

**On a BST** — `[4,2,7,1,3]`:

```
      4
     / \
    2   7
   / \
  1   3
```

Inorder yields **`[1,2,3,4,7]`** — sorted ✅. That's the property [Validate BST](98-validate-binary-search-tree.md) and [Kth Smallest](230-kth-smallest-element-in-a-bst.md) both exploit.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

Each node is **pushed exactly once and popped exactly once**, and each push/pop does O(1) work. With `n` nodes that's `2n` stack operations plus `n` appends — **O(n)**.

The nested `while` doesn't make it quadratic: the inner loop's total iterations across the whole run are bounded by the number of pushes, which is `n`. Same amortized argument as the monotonic-stack problems in [Unit 04](../rmap-practice/04-stack.md).

You can't beat O(n) — every node's value must appear in the output.

**Recursion is also O(n)**, with `n` function calls instead of `n` push/pop pairs. Similar constants; the iterative version avoids call overhead.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(h)</summary>

**O(h)**, where `h` is the tree's **height** — not the node count.

The stack holds the current root-to-node path, which is at most `h` deep:

| Tree shape | `h` | Stack space |
|---|---|---|
| Balanced | `log n` | **O(log n)** |
| Degenerate (a linked list) | `n` | **O(n)** |

So the worst case is O(n) — an entirely left-leaning tree pushes every node before popping any — but a balanced tree is only O(log n).

**Excluding the output**, which is O(n) and required.

**Recursion has the same O(h)** bound, just as call frames rather than list entries. The practical difference: Python's recursion limit (~1000) means a degenerate tree of 10⁵ nodes would raise `RecursionError`, while the explicit stack keeps working. At `n <= 100` here, both are safe.

**Morris traversal achieves O(1)** by threading the tree — temporarily pointing each subtree's rightmost node back at its successor, then undoing it. Optimal space, but it mutates the tree mid-traversal.

| | Time | Space |
|---|---|---|
| Recursion | O(n) | O(h) stack |
| **Explicit stack** | **O(n)** | **O(h)** |
| Morris | O(n) | **O(1)** — mutates temporarily |

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Inorder means left, node, right — so a node can't be visited until its whole left subtree is done. Recursively that's three lines, but the follow-up asks for iteration, which means making the call stack explicit. I dive as far left as I can, pushing every node; then I pop, and popping means that node's left subtree is finished, so I visit it; then I move to its right child and repeat. The loop condition is `while curr or stack` — two reasons to continue: a subtree left to descend, or ancestors left to visit. Either alone terminates too early. O(n) time since each node is pushed and popped once, and O(h) space for the stack — O(log n) balanced, O(n) for a degenerate tree. Morris traversal would get it to O(1) by threading the tree, at the cost of temporarily mutating it."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Do it iteratively." | **The stated follow-up** — the explicit stack above. |
| "O(1) space?" | Morris traversal — thread each subtree's rightmost node to its inorder successor, then restore. O(n) time, O(1) space. |
| "Why does inorder matter more than pre/post?" | On a **BST** it yields sorted order — the basis for [Validate BST](98-validate-binary-search-tree.md) and [Kth Smallest](230-kth-smallest-element-in-a-bst.md). |
| "Find the `k`-th smallest in a BST." | Run this traversal and stop after `k` pops — early termination the recursive form can't do cleanly. [Problem 230](230-kth-smallest-element-in-a-bst.md). |
| "Why `while curr or stack`?" | `curr` covers "descend further", `stack` covers "ancestors pending". Both are needed. |
| "Preorder / postorder iteratively?" | [Preorder](144-binary-tree-preorder-traversal.md) is a simple stack; [postorder](145-binary-tree-postorder-traversal.md) has a neat reversal trick. |
| "What about very deep trees?" | Recursion hits Python's ~1000-frame limit; the explicit stack does not. |

**Traps:**

- **Using `while stack` alone.** The stack starts empty, so the loop never runs and you return `[]`.
- **Using `while curr` alone.** Exits as soon as you reach a `None` child, dropping every pending ancestor.
- **Appending before the dive.** That produces **preorder**, not inorder. The append must follow the pop.
- **Forgetting `curr = curr.right`.** Infinite loop — you'd re-push and re-pop the same node forever.
- **Pushing the right child explicitly.** Unnecessary; setting `curr` to it and letting the outer loop handle the dive is what keeps the code short.
- **Recursion on a degenerate tree.** Fine at `n = 100`, `RecursionError` at 10⁵.

**This same move shows up in:** [Binary Tree Preorder Traversal](144-binary-tree-preorder-traversal.md) and [Postorder](145-binary-tree-postorder-traversal.md) (the sibling orders) · [Kth Smallest Element in a BST](230-kth-smallest-element-in-a-bst.md) (inorder with early termination) · [Validate Binary Search Tree](98-validate-binary-search-tree.md) (inorder must be strictly increasing) · [Binary Tree Level Order Traversal](102-binary-tree-level-order-traversal.md) (the BFS counterpart, using a queue instead of a stack).

</details>

---
