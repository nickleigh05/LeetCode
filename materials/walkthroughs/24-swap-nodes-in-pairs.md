# 24. Swap Nodes in Pairs

**Medium** · [LeetCode](https://leetcode.com/problems/swap-nodes-in-pairs/) · [Solution file (no hints)](../../problems/0001-0499/24.py)

[📖 06. Linked List lesson](../learning/06-linked-list.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 06. Linked List problems](../rmap-practice/06-linked-list.md)

---

Given a linked list, swap every two adjacent nodes and return its head. You must solve it **without modifying the values** in the nodes — only the nodes themselves may be changed.

```
head = [1,2,3,4]  →  [2,1,4,3]
head = []         →  []
head = [1]        →  [1]
head = [1,2,3]    →  [2,1,3]
```

**Constraints:** `0 <= number of nodes <= 100` · `0 <= Node.val <= 100`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "swap every **two adjacent** nodes" | Process the list in pairs: (1,2), (3,4), … |
| "**without modifying the values**" | ⚠️ The whole point. Swapping `.val` fields is trivial and forbidden — you must rewire `.next` pointers |
| "only nodes may be changed" | Real pointer surgery |
| `[1,2,3]` → `[2,1,3]` | ⚠️ An **odd** leftover node stays in place, unswapped |
| `0 <= nodes` | Empty list must work |
| the **head changes** | The second node becomes the new head ⇒ a dummy node earns its place |

**Why the value-swap ban matters.** The one-liner would be `a.val, b.val = b.val, a.val` walking in steps of two. It's correct output-wise and takes 30 seconds. The problem forbids it because the *exercise* is pointer manipulation — the skill that transfers to [Reverse Nodes in k-Group](25-reverse-nodes-in-k-group.md), [Reverse Linked List II](92-reverse-linked-list-ii.md), and real data-structure work where nodes carry payloads you can't just overwrite.

**What a swap actually requires.** To swap nodes `a` and `b`, three pointers must change:

```
before:   prev → [a] → [b] → rest
after:    prev → [b] → [a] → rest
```

1. `prev.next = b` — the predecessor now points at `b`
2. `a.next = b.next` — `a` skips over `b` to the rest
3. `b.next = a` — `b` points back at `a`

**Order matters.** Do step 2 before step 3, or you'll have already overwritten `b.next` and lost the rest of the list. (Alternatively, save `b.next` first — the same "save before you destroy" discipline as in [Reverse Linked List](206-reverse-linked-list.md).)

**Why a dummy node.** The head becomes the *second* node, so `head` is no longer the right return value — and the first pair has no predecessor to rewire. A sentinel before the head solves both, exactly as in [Remove Linked List Elements](203-remove-linked-list-elements.md).

🤔 **Before you open the next section:** after swapping a pair, which node is now the predecessor of the *next* pair?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Swap `.val` fields | Walk in twos, exchange values | O(n) | O(1) | ❌ **Explicitly forbidden** |
| Recursion | Swap the first pair, recurse on the rest | O(n) | **O(n)** stack | ✅ Very clean; stack cost |
| **Iterative with a dummy** | Rewire each pair in place | **O(n)** | **O(1)** | ✅ |

**The decision: iterative pointer rewiring with a dummy head.**

The loop invariant, which is what makes it easy to reason about:

> **`prev` always points at the node immediately before the next pair to swap.**

Each iteration:

1. Identify `first = prev.next` and `second = prev.next.next`
2. Rewire the three pointers
3. Advance `prev` to `first` — because after the swap, `first` is the **last** node of the completed pair, hence the predecessor of the next pair

Step 3 is the one people get wrong. After swapping, the order is `prev → second → first → rest`, so `first` is now the trailing node and becomes the new `prev`. Advancing to `second` (the intuitive choice, since it *was* second) leaves you one node short and produces garbage.

**The loop condition: `while prev.next and prev.next.next`.**

Both are needed — a swap requires **two** nodes. If only one remains (`prev.next.next` is `None`), it's the odd leftover and stays untouched, which is exactly the `[1,2,3]` → `[2,1,3]` behaviour. The condition handles the odd case with no special branch.

**Why recursion is genuinely attractive here:**

```python
def swapPairs(self, head):
    if not head or not head.next:
        return head
    second = head.next
    head.next = self.swapPairs(second.next)
    second.next = head
    return second
```

Four lines, and it reads almost like the problem statement. At `n <= 100` the O(n) stack is completely safe, so this is a legitimate answer — arguably the more elegant one. Mention it. The iterative version is what you'd want for a list of a million nodes, and it's the version that generalizes cleanly to k-groups.

**Why not swap values?** Beyond being forbidden: in real systems, nodes often carry large payloads or are referenced elsewhere, so moving pointers is cheap and moving data is not.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
dummy = ListNode(0)
dummy.next = head
prev = dummy
```

**The sentinel.** The head is about to change, so `dummy.next` becomes the reliable handle on the true head. `prev` starts here so the first pair has a predecessor to rewire.
→ [class-basics](../syntax/class-basics.md) · [init-method](../syntax/init-method.md)

```python
while prev.next and prev.next.next:
```

**A swap needs two nodes.** If fewer than two remain, we're done — and a single leftover node correctly stays in place.

Short-circuiting ensures `prev.next.next` is only evaluated once `prev.next` is known non-`None`.
→ [while-loop](../syntax/while-loop.md) · [logical-operators](../syntax/logical-operators.md)

```python
    first = prev.next
    second = prev.next.next
```

Name the pair. Naming them before rewiring is what keeps the next three lines readable — without it you're juggling `prev.next.next.next` expressions that are very easy to misread.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
    first.next = second.next
    second.next = first
    prev.next = second
```

**The three-pointer rewire.**

1. `first.next = second.next` — `first` jumps over `second` to the rest. **Do this first**, while `second.next` still points at the rest.
2. `second.next = first` — `second` now precedes `first`.
3. `prev.next = second` — the predecessor adopts the new front of the pair.

Reorder these and you lose the tail: setting `second.next = first` before reading `second.next` overwrites the only reference to the remainder of the list.

```python
    prev = first
```

**Advance — and note it's `first`, not `second`.**

After the swap the layout is `prev → second → first → rest`, so `first` is the trailing node of the completed pair and therefore the predecessor of the next one.

```python
return dummy.next
```

The new head — which is the original second node, or the original head if the list had fewer than two nodes.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:

        dummy = ListNode(0)
        dummy.next = head
        prev = dummy

        while prev.next and prev.next.next:
            first = prev.next
            second = prev.next.next

            first.next = second.next
            second.next = first
            prev.next = second

            prev = first

        return dummy.next
```

</details>

<details>
<summary>The recursive version (equally valid at these constraints)</summary>

```python
class Solution:
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:
            return head

        second = head.next
        head.next = self.swapPairs(second.next)
        second.next = head
        return second
```

Reads almost like the problem statement: swap the first pair, recurse on the rest, return the new front. O(n) stack — fine at `n <= 100`, risky at 10⁵.

</details>

**Trace it** — `head = [1,2,3,4]`:

Start: `dummy → 1 → 2 → 3 → 4`, `prev = dummy`

**Iteration 1** — `first = 1`, `second = 2`:

| Step | Operation | List state |
|---|---|---|
| 1 | `first.next = second.next` (1 → 3) | `dummy → 1 → 3 → 4`, with 2 → 3 |
| 2 | `second.next = first` (2 → 1) | 2 → 1 → 3 → 4 |
| 3 | `prev.next = second` | `dummy → 2 → 1 → 3 → 4` ✅ |
| 4 | `prev = first` | `prev` = node 1 |

**Iteration 2** — `prev.next` = 3, `prev.next.next` = 4, so `first = 3`, `second = 4`:

| Step | Operation | List state |
|---|---|---|
| 1 | `first.next = second.next` (3 → None) | 3 → None |
| 2 | `second.next = first` (4 → 3) | 4 → 3 → None |
| 3 | `prev.next = second` (1 → 4) | `dummy → 2 → 1 → 4 → 3` ✅ |
| 4 | `prev = first` | `prev` = node 3 |

**Iteration 3:** `prev.next` is `None` → loop ends.

`return dummy.next` = **`[2,1,4,3]`** ✅

**The odd case** — `[1,2,3]`:

After iteration 1 the list is `dummy → 2 → 1 → 3` with `prev` = node 1. Then `prev.next` = 3 exists but `prev.next.next` is `None`, so the loop exits and node 3 is left in place.

Return **`[2,1,3]`** ✅ — the leftover handled with no special-case code.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

Each iteration handles one pair and advances `prev` past two nodes, so the loop runs `⌊n/2⌋` times with O(1) work each — three pointer assignments and one advance.

Roughly `n/2` iterations × 4 operations ≈ `2n` pointer writes. **O(n)**, and optimal: every node must be visited to be repositioned.

**The recursive version is also O(n)** in time, with one call frame per pair — `n/2` frames deep.

**Compare to the forbidden value swap:** also O(n), with `n/2` value exchanges instead of `2n` pointer writes. Slightly fewer operations, which is part of why it's tempting — and precisely why the problem rules it out.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** for the iterative version — the dummy node plus three pointers, independent of list length.

**O(n) for the recursive version** — `n/2` stack frames. At `n <= 100` that's ~50 frames, entirely safe. But the same code on a 10⁵-node list would raise `RecursionError`, so the iterative form is the one that scales.

| | Time | Space |
|---|---|---|
| Value swap | O(n) | O(1) | ❌ forbidden |
| **Iterative + dummy** | **O(n)** | **O(1)** | ✅ |
| Recursive | O(n) | O(n) stack | ✅ at these limits |

**What the dummy bought:** the head changes, so without a sentinel you'd need a special case to swap the first pair and separately track the new head. One extra node removes both problems — the same value it provides in [Remove Linked List Elements](203-remove-linked-list-elements.md) and [Partition List](86-partition-list.md).

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Values can't be swapped, so this is pointer surgery. Since the head becomes the second node, I use a dummy sentinel — that gives the first pair a predecessor and makes `dummy.next` the reliable return value. I keep `prev` pointing at the node before the next pair, and loop while there are two nodes left. For each pair I name `first` and `second`, then rewire three pointers: `first.next = second.next` **first**, so I don't lose the rest of the list, then `second.next = first`, then `prev.next = second`. Finally I advance `prev` to `first`, because after the swap `first` is the trailing node of the pair. The loop condition handles an odd leftover automatically — with only one node left it just exits and leaves it in place. O(n) time, O(1) space. A recursive version is four lines and very readable, but it's O(n) stack."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Generalize to **k** nodes per group." | [Reverse Nodes in k-Group](25-reverse-nodes-in-k-group.md) — same skeleton, but reverse a k-length sublist and check a full group exists before starting. |
| "Why advance `prev` to `first`?" | After the swap the order is `prev → second → first`, so `first` trails the pair and precedes the next one. |
| "Why does the pointer order matter?" | `first.next = second.next` must come first; otherwise `second.next` is overwritten and the tail is lost. |
| "Do it recursively." | Swap the first pair, recurse on `second.next`, return `second`. O(n) stack. |
| "Why not swap values?" | Forbidden here — and in practice nodes may carry large payloads or be referenced elsewhere. |
| "What about an odd number of nodes?" | The last one stays put; the two-node loop condition handles it with no branch. |
| "Empty list?" | `prev.next` is `None`, the loop never runs, and `dummy.next` is `None`. Correct for free. |

**Traps:**

- **Advancing `prev` to `second`.** After the swap `second` is the *front* of the pair, so this lands one node short and corrupts the next iteration.
- **Rewiring in the wrong order.** Setting `second.next = first` before reading `second.next` destroys the link to the rest of the list.
- **Only checking `prev.next`.** `prev.next.next` then raises on an odd-length list.
- **Omitting the dummy.** You'd need a special case for the first pair and separate tracking of the new head.
- **Returning `head`.** After the first swap, `head` is the *second* node in the output. Return `dummy.next`.
- **Swapping values anyway.** Passes the judge, fails the actual requirement.

**This same move shows up in:** [Reverse Nodes in k-Group](25-reverse-nodes-in-k-group.md) (the k-way generalization of this exact structure) · [Reverse Linked List II](92-reverse-linked-list-ii.md) (rewiring a sublist with a dummy and a fixed predecessor) · [Remove Linked List Elements](203-remove-linked-list-elements.md) (the dummy-node pattern) · [Reverse Linked List](206-reverse-linked-list.md) (the save-before-you-overwrite discipline).

</details>

---
