# 116. Populating Next Right Pointers in Each Node

**Medium** · [LeetCode](https://leetcode.com/problems/populating-next-right-pointers-in-each-node/) · [Solution file (no hints)](../../problems/0001-0499/116.py)

[📖 07. Trees lesson](../learning/07-trees.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 07. Trees problems](../rmap-practice/07-trees.md)

---

You are given a **perfect binary tree** — all leaves on the same level, every parent has two children. Populate each `next` pointer to point to its **next right node** on the same level; where none exists, set it to `NULL`. All `next` pointers start as `NULL`.

```
root = [1,2,3,4,5,6,7]  →  [1,#,2,3,#,4,5,6,7,#]

        1 → NULL
      /   \
     2  →  3 → NULL
    / \   / \
   4 → 5→6 → 7 → NULL
```

**Constraints:** `0 <= number of nodes <= 2¹² − 1` · `-1000 <= Node.val <= 1000`

**Follow-up:** use only **constant extra space** (recursion's implicit stack doesn't count).

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**perfect** binary tree" | ⚠️ **The crucial gift.** Every node has either two children or none, and all leaves are at the same depth |
| "**next right** node on the same level" | Horizontal links across each level |
| "`NULL` at the end of each level" | Already true — pointers start `NULL`, so the rightmost node needs no action |
| follow-up: **constant space** | Rules out a BFS queue, which is O(w) = O(n/2) |
| `0 <= nodes` | Empty tree must work |

**The obvious solution is BFS** — traverse level by level and link consecutive nodes. That's O(n) time but **O(w) space** for the queue, which fails the follow-up.

**The insight that gets you to O(1):**

> Once level `k` is fully linked, you can traverse it horizontally using the `next` pointers you just built — and use that traversal to link level `k+1`.

The `next` pointers become the queue. You never need to store anything.

**The two links to establish for each node**, and the second is the interesting one:

```
        node
        /  \
   left → right          link 1: node.left.next = node.right   (same parent — easy)
              ↓
           node.next
            /
      node.next.left      link 2: node.right.next = node.next.left   (across parents)
```

1. **Within a parent:** `node.left.next = node.right`. Trivially available.
2. **Across parents:** `node.right.next = node.next.left`. This is where the already-built level above does the work — `node.next` is the parent's right neighbour, reachable only because level `k` was linked first.

**Why "perfect" is load-bearing.** In a perfect tree, if `node.next` exists then `node.next.left` **definitely** exists. No gaps, no missing children, no searching. That's what makes link 2 a single dereference.

Drop that guarantee and you get [LeetCode 117](https://leetcode.com/problems/populating-next-right-pointers-in-each-node-ii/), where you must scan rightward along the parent level looking for the next node that actually *has* a child — meaningfully harder.

🤔 **Before you open the next section:** if every node on the current level already knows its right neighbour, how do you reach the node immediately right of `node.right`?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| BFS with a queue | Level order; link consecutive nodes | O(n) | **O(w)** = O(n/2) | ⚠️ Correct, fails the follow-up |
| Recursive DFS | Link `left→right` and `right→next.left` while descending | O(n) | O(h) stack | ✅ Allowed (implicit stack is exempt) |
| **Level-by-level using `next`** | Walk each finished level to build the one below | **O(n)** | **O(1)** | ✅✅ |

**The decision: iterate level by level, using the previously built `next` pointers to traverse.**

Two pointers do all the work:

- **`leftmost`** — the first node of the level currently being processed; descends one level per outer iteration
- **`node`** — walks horizontally across that level via `next`

For each `node`, set the two links described above, then advance with `node = node.next`. When the row is exhausted, drop to `leftmost = leftmost.left` and repeat.

**Why you stop at `leftmost.left` being `None`.** In a perfect tree, if a node has no left child it has no children at all and is a leaf — so the entire level is leaves and there's nothing below to link. That single check is the loop's termination condition, and it works only because the tree is perfect.

**Why the rightmost node needs no special handling.** `node.next` is `None` for the last node in a row, so `node.right.next = node.next.left` would raise. The loop guard `while node:` handles the horizontal walk, and the link-2 assignment is guarded by `if node.next:` — leaving the rightmost child's `next` as its initial `None`, which is exactly correct.

**The recursive alternative** is shorter and legitimate here, since the problem explicitly exempts the implicit stack:

```python
def connect(self, root):
    if not root or not root.left:
        return root
    root.left.next = root.right
    if root.next:
        root.right.next = root.next.left
    self.connect(root.left)
    self.connect(root.right)
    return root
```

Same two links, applied top-down. It's O(h) stack — allowed by the wording, but the iterative version is genuinely O(1) and only a few lines longer. Know both; the iterative one is the stronger answer.

**Why the BFS queue fails the follow-up.** A perfect tree's last level holds `n/2` nodes, so the queue peaks at O(n) — precisely what "constant extra space" excludes. The elegance here is realizing the tree can hold that information *itself*, in the pointers you're already building.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
if not root:
    return root
```

**Empty tree → nothing to link.** Returns `None`, matching the expected empty output.
→ [truthy-falsy-values](../syntax/truthy-falsy-values.md)

```python
leftmost = root
```

The first node of the level being processed. Starts at the root (level 0, which has no horizontal links to make but does have children to connect).
→ [variables-assignment](../syntax/variables-assignment.md)

```python
while leftmost.left:
```

**Descend while a level below exists.**

In a perfect tree, `leftmost.left` being `None` means `leftmost` is a leaf — and since all leaves share a depth, the whole level is leaves. Nothing below to link, so stop.

This is where "perfect" is doing real work: one check settles the question for the entire level.
→ [while-loop](../syntax/while-loop.md)

```python
    node = leftmost
    while node:
```

**Walk horizontally across the current level** using the `next` pointers built on the previous outer iteration (or, for level 0, the trivial single-node row).
→ [while-loop](../syntax/while-loop.md)

```python
        node.left.next = node.right
```

**Link 1 — siblings under the same parent.** Both children exist (perfect tree), so no guard is needed.
→ [class-basics](../syntax/class-basics.md)

```python
        if node.next:
            node.right.next = node.next.left
```

**Link 2 — across the parent boundary.**

`node.next` is the parent's right neighbour on the current level. Its left child is exactly the node sitting immediately right of `node.right`.

The `if node.next:` guard handles the **rightmost** node of the row, whose `right.next` correctly stays `None`.

This link is only possible because the current level was already connected — which is the whole idea.
→ [none-type](../syntax/none-type.md)

```python
        node = node.next
```

Advance along the row.

```python
    leftmost = leftmost.left
```

**Drop to the next level**, whose leftmost node is the current leftmost's left child.

```python
return root
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def connect(self, root: 'Optional[Node]') -> 'Optional[Node]':

        if not root:
            return root

        leftmost = root

        while leftmost.left:
            node = leftmost

            while node:
                node.left.next = node.right

                if node.next:
                    node.right.next = node.next.left

                node = node.next

            leftmost = leftmost.left

        return root
```

</details>

<details>
<summary>The recursive version (allowed by the follow-up's wording)</summary>

```python
class Solution:
    def connect(self, root: 'Optional[Node]') -> 'Optional[Node]':
        if not root or not root.left:
            return root

        root.left.next = root.right
        if root.next:
            root.right.next = root.next.left

        self.connect(root.left)
        self.connect(root.right)
        return root
```

The same two links, applied top-down. Correct and shorter, but O(h) implicit stack — the problem exempts it, though the iterative version is genuinely O(1).

</details>

**Trace it** — `root = [1,2,3,4,5,6,7]`:

```
        1
      /   \
     2     3
    / \   / \
   4   5 6   7
```

**Outer iteration 1** — `leftmost = 1`, linking level 2:

| `node` | Link 1 (`left.next = right`) | `node.next`? | Link 2 |
|---|---|---|---|
| 1 | `2.next = 3` | `None` | skipped (rightmost) |

Level 2 now: `2 → 3 → NULL` ✅

**Outer iteration 2** — `leftmost = 2`, linking level 3. The horizontal walk uses the links just built:

| `node` | Link 1 | `node.next`? | Link 2 |
|---|---|---|---|
| 2 | `4.next = 5` | **3** | `5.next = 3.left = 6` ⭐ |
| 3 | `6.next = 7` | `None` | skipped (rightmost) |

Level 3 now: `4 → 5 → 6 → 7 → NULL` ✅

**Outer iteration 3** — `leftmost = 4`, but `4.left` is `None` → loop ends.

Final structure:

```
        1 → NULL
      /   \
     2  →  3 → NULL
    / \   / \
   4 → 5→6 → 7 → NULL
```

✅ matching `[1,#,2,3,#,4,5,6,7,#]`

The starred step is the whole technique: linking `5 → 6` crosses from node 2's subtree into node 3's, and it was only possible because `2.next = 3` had been established on the previous iteration.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

Every node is visited exactly once by the horizontal walk, doing O(1) work — one or two pointer assignments and an advance.

The nested loops don't multiply: the outer loop runs once per **level** (`log n` times), and the inner loop's total iterations across all levels sum to `n`, since each node is walked once. So it's `O(n)`, not `O(n log n)`.

That's the same "nested loops with a global work budget" accounting as the monotonic-stack and sliding-window problems.

**Compare:**

| | Time | Space |
|---|---|---|
| BFS with a queue | O(n) | O(n/2) |
| Recursive DFS | O(n) | O(h) = O(log n) |
| **Level-by-level via `next`** | **O(n)** | **O(1)** ✅ |

All three are O(n) time — the follow-up is purely about space, and this is the only one that achieves true constant.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — exactly two pointers, `leftmost` and `node`, regardless of tree size.

This is the point of the problem, and the mechanism is worth stating in general terms:

> **The `next` pointers you're building double as the traversal structure for the level below.** The tree stores its own frontier, so no external queue is needed.

That's why BFS's O(w) queue is avoidable: the queue's job — "remember this level's nodes in order" — is already being done by the pointers you're required to create.

**The space comparison in concrete terms.** For a perfect tree with `n = 2¹² − 1 = 4095` nodes, the last level holds 2048 nodes — so a BFS queue peaks at ~2048 entries, while this uses two.

**A reusable idea beyond this problem:** when an algorithm's output is itself a linking structure, check whether it can be traversed as it's built. The same flavour of trick appears in threaded binary trees and in Morris traversal (mentioned in [Inorder Traversal](94-binary-tree-inorder-traversal.md)), which reuses spare right pointers to walk a tree in O(1) space.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The obvious answer is BFS, linking consecutive nodes on each level — but that's O(w) space for the queue, and the follow-up wants constant. The insight is that once a level is fully linked, its `next` pointers *are* a traversal structure for that level, so I can walk it horizontally to build the level below. For each node I set two links: `node.left.next = node.right` for siblings, and `node.right.next = node.next.left` to cross the parent boundary — that second one only works because the level above is already connected. The tree being **perfect** is what makes it clean: if `node.next` exists, its left child definitely exists, so there's no searching. I descend with a `leftmost` pointer and stop when it has no left child, which means the whole level is leaves. O(n) time, O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Constant space?" | **The stated follow-up** — use the `next` pointers of the finished level to traverse and build the next one. |
| "What if the tree **isn't perfect**?" | [LeetCode 117](https://leetcode.com/problems/populating-next-right-pointers-in-each-node-ii/) — you must scan rightward along the parent level for the next node that has a child, and use a dummy head to track the next level's start. Noticeably harder. |
| "Why does 'perfect' matter?" | If `node.next` exists, `node.next.left` is guaranteed to exist — no gaps, so link 2 is a single dereference. |
| "Solve it recursively." | Set both links at each node, then recurse into both children. O(h) implicit stack, which the problem explicitly permits. |
| "Why isn't the nested loop O(n log n)?" | The inner loop's iterations sum to `n` across all levels — each node is walked once. |
| "How does the rightmost node get `NULL`?" | Pointers start `NULL`, and the `if node.next:` guard skips the assignment there. |
| "Could you do this on a general graph?" | No — the technique relies on the tree's level structure and the fact that you're building the very links you traverse. |

**Traps:**

- **Using a BFS queue.** Correct output, but O(w) space — it fails the follow-up, which is the entire point.
- **Omitting the `if node.next:` guard.** `AttributeError` on the rightmost node of every level.
- **Trying to link the next level before the current one is connected.** Link 2 depends on the level above already being linked — order matters.
- **Looping `while leftmost:` instead of `while leftmost.left:`.** On the leaf level, `node.left.next` would raise.
- **Assuming this works on a non-perfect tree.** `node.next.left` may not exist. That's problem 117.
- **Forgetting to return `root`.** The tree is modified in place, but the signature returns it.

**This same move shows up in:** [Binary Tree Level Order Traversal](102-binary-tree-level-order-traversal.md) (the BFS this deliberately avoids) · [Binary Tree Zigzag Level Order Traversal](103-binary-tree-zigzag-level-order-traversal.md) (level-boundary handling with a queue) · [Binary Tree Inorder Traversal](94-binary-tree-inorder-traversal.md) (Morris traversal — the same "reuse pointers instead of a stack" idea) · [Binary Tree Right Side View](199-binary-tree-right-side-view.md) (per-level rightmost nodes, which these pointers make trivial to find).

</details>

---
