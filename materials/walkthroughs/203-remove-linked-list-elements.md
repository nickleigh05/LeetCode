# 203. Remove Linked List Elements

**Easy** · [LeetCode](https://leetcode.com/problems/remove-linked-list-elements/) · [Solution file (no hints)](../../problems/0001-0499/203.py)

[📖 06. Linked List lesson](../learning/06-linked-list.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 06. Linked List problems](../rmap-practice/06-linked-list.md)

---

Given the head of a linked list and an integer `val`, remove **all** nodes with `Node.val == val` and return the new head.

```
head = [1,2,6,3,4,5,6], val = 6  →  [1,2,3,4,5]
head = [],              val = 1  →  []
head = [7,7,7,7],       val = 7  →  []
```

**Constraints:** `0 <= number of nodes <= 10⁴` · `1 <= Node.val <= 50` · `0 <= val <= 50`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "remove **all** nodes" | Not just the first — and matches can be consecutive |
| "return the **new head**" | ⚠️ The head itself may be deleted, so the return value can differ from the input |
| `[7,7,7,7]` → `[]` | **Every** node can be removed, including all leading ones |
| `0 <= nodes` | The list can start empty |
| singly linked | You can only move forward, and you need the **previous** node to unlink something |

**The core mechanic.** Removing a node from a singly linked list means making its predecessor skip over it:

```
before:   prev → [target] → next
after:    prev ──────────→ next
```

So you always need a handle on the **previous** node. That's easy in the middle of the list and awkward at the head — because the head has no predecessor.

**The head problem, concretely.** Consider `[7,7,7,7]` with `val = 7`. Every node goes, including the head, and then the head goes again, and again. Handling that with special-case code means a loop like:

```python
while head and head.val == val:    # peel off leading matches
    head = head.next
# ...then a different loop for the rest
```

Two loops, two sets of conditions, two chances to get it wrong.

**The fix — a dummy node:**

> Create a fake node **before** the head. Now every real node — including the original head — has a predecessor, so one uniform loop handles all of them.

```
dummy → [1] → [2] → [6] → [3] ...
  ↑
never removed, always a valid "previous"
```

At the end, return `dummy.next` rather than `head`, since the head may have changed.

This is the **dummy head** (or sentinel) pattern, and it's the single most useful trick in linked-list problems. It shows up again in [Remove Nth Node From End](19-remove-nth-node-from-end-of-list.md), [Merge Two Sorted Lists](21-merge-two-sorted-lists.md), [Partition List](86-partition-list.md), and [Swap Nodes in Pairs](24-swap-nodes-in-pairs.md).

🤔 **Before you open the next section:** if every node might be deleted, what should your function return — and how do you know what it is without tracking the head separately?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Rebuild a new list | Copy surviving nodes into a fresh list | O(n) | **O(n)** | ⚠️ Correct, allocates unnecessarily |
| Two loops (peel head, then scan) | Special-case leading matches | O(n) | O(1) | ⚠️ Correct, duplicated logic |
| **Dummy node + single loop** | One uniform pass | **O(n)** | **O(1)** | ✅ |
| Recursion | `head.next = removeElements(head.next, val)` | O(n) | **O(n)** stack | ⚠️ Elegant; risks overflow at 10⁴ nodes |

**The decision: a dummy head node with one traversal.**

Why it's worth the one extra allocation:

1. **Uniformity.** Every node has a predecessor, so there is exactly one removal code path.
2. **Correct return.** `dummy.next` is always the true head, whether or not the original was deleted.
3. **Consecutive matches handled free.** `[7,7,7]` needs no extra logic — `prev` simply stays put while `current` walks on.

**The key detail: when do you advance `prev`?**

```python
if current.val == val:
    prev.next = current.next     # unlink — prev does NOT move
else:
    prev = current               # keep — prev moves up
current = current.next           # current always moves
```

`prev` advances **only when a node survives**. That's what makes runs of consecutive matches work: after unlinking node A, `prev` is still the same node, ready to unlink node B as well.

Advancing `prev` unconditionally is the defining bug here — on `[1,6,6,2]` it would unlink the first 6, then set `prev` to that already-removed node, and the second 6 would silently survive.

**Why recursion is risky.** The recursive form is genuinely pretty:

```python
if not head: return None
head.next = self.removeElements(head.next, val)
return head.next if head.val == val else head
```

But it uses O(n) stack depth, and with up to 10⁴ nodes it will hit Python's default recursion limit (~1000). Mention it as elegant, then note why the iterative version is the safe choice. See [recursion-limit](../syntax/recursion-limit.md).

**Why not rebuild?** Allocating a parallel list is O(n) extra memory for something achievable by pointer rewiring alone.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
dummy = ListNode(-1)
dummy.next = head
```

**The sentinel.** A throwaway node placed before the real head, giving the head a predecessor.

Its value is irrelevant — `-1` here, but anything works, since the node is never inspected and never returned.
→ [class-basics](../syntax/class-basics.md) · [init-method](../syntax/init-method.md)

```python
previous_node = dummy
current_node = head
```

`previous_node` trails one behind `current_node`. Starting it at `dummy` means even the original head can be unlinked through it.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
while current_node is not None:
```

Walk to the end. `is not None` rather than a truthiness test is the precise check — see the trap about falsy values below.
→ [while-loop](../syntax/while-loop.md) · [none-type](../syntax/none-type.md) · [identity-operators](../syntax/identity-operators.md)

```python
    if current_node.val == val:
        previous_node.next = current_node.next
```

**Unlink.** Point the predecessor past the current node.

Note `previous_node` is deliberately **not** advanced — it must stay in place to handle a possible run of consecutive matches.

There's no need to clear `current_node.next`; Python's garbage collector reclaims the orphaned node once nothing references it.
→ [comparison-operators](../syntax/comparison-operators.md)

```python
    else:
        previous_node = current_node
```

**Keep.** The node survives, so it becomes the new predecessor.
→ [elif-else](../syntax/elif-else.md)

```python
    current_node = current_node.next
```

Outside the branch — `current_node` advances on **every** iteration regardless of what happened.

This still works after an unlink because `current_node.next` is read from the node itself, which is intact even though nothing points to it any more.

```python
return dummy.next
```

**Return `dummy.next`, not `head`.** If the original head was removed, `head` now points at a detached node. `dummy.next` always reflects the current true head — that's the whole reason the sentinel exists.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def removeElements(self, head: Optional[ListNode], val: int) -> Optional[ListNode]:

        dummy = ListNode(-1)
        dummy.next = head

        previous_node = dummy
        current_node = head

        while current_node is not None:
            if current_node.val == val:
                previous_node.next = current_node.next
            else:
                previous_node = current_node
            current_node = current_node.next

        return dummy.next
```

</details>

**Trace it** — `head = [1,2,6,3,4,5,6]`, `val = 6`:

| `current` | Match? | Action | List after | `prev` |
|---|---|---|---|---|
| 1 | no | keep | `d→1→2→6→3→4→5→6` | 1 |
| 2 | no | keep | unchanged | 2 |
| **6** | ✅ | `prev.next = 3` | `d→1→2→3→4→5→6` | **2** (unmoved) |
| 3 | no | keep | unchanged | 3 |
| 4 | no | keep | unchanged | 4 |
| 5 | no | keep | unchanged | 5 |
| **6** | ✅ | `prev.next = None` | `d→1→2→3→4→5` | **5** (unmoved) |

`return dummy.next` = **`[1,2,3,4,5]`** ✅

**The all-match case** — `[7,7,7,7]`, `val = 7`:

| `current` | Action | `prev` | List |
|---|---|---|---|
| 7₁ | unlink | dummy | `d→7₂→7₃→7₄` |
| 7₂ | unlink | dummy | `d→7₃→7₄` |
| 7₃ | unlink | dummy | `d→7₄` |
| 7₄ | unlink | dummy | `d→None` |

`return dummy.next` = **`None`** = `[]` ✅

`prev` never moved off `dummy` — exactly the behaviour that makes consecutive removals work, and the case that would break if `prev` advanced unconditionally.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

One traversal, and each node is visited exactly once. Every operation inside the loop — a comparison and one or two pointer assignments — is O(1).

`current_node` advances on every iteration and never revisits a node, so the loop runs exactly `n` times.

Unlinking is **O(1)** in a linked list, which is its main advantage over an array: removing from the middle of an array is O(n) because everything shifts. Here it's a single pointer write. That contrast is worth stating — it's why linked lists exist.

**Best and worst cases are identical** — you must examine every node to know whether it matches, so there's no early exit.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).**

The dummy node is a single allocation, independent of list length, and the two pointers are constant.

Some would call this "O(1) plus one node," but a fixed number of allocations is O(1) by definition.

**The alternatives cost real memory:**

| | Space |
|---|---|
| Rebuild a new list | O(n) — a full parallel list |
| Recursion | **O(n)** stack — and it will overflow at 10⁴ nodes |
| **Dummy + iteration** | **O(1)** ✅ |

The recursion point is practical, not theoretical: Python's default limit is around 1000 frames, and the constraints allow 10⁴ nodes. A recursive submission would raise `RecursionError` on large inputs.

**The takeaway:** one sentinel node buys you uniform logic and a correct return value for constant cost. That's an exceptionally good trade, and it's why the pattern is ubiquitous.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Removing a node from a singly linked list means pointing its predecessor past it, so I always need the previous node — which is awkward at the head, since the head has none, and the head itself might be removed. So I create a dummy node before the head. Now every real node has a predecessor and one uniform loop handles everything, including runs of consecutive matches and the case where all nodes are deleted. The key detail is that `prev` only advances when a node **survives** — if I advanced it after an unlink, consecutive matches would be skipped. At the end I return `dummy.next` rather than `head`, because the head may no longer be part of the list. O(n) time, O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why a dummy node?" | **The key question.** It gives the head a predecessor, so removal is uniform and the true head is always `dummy.next`. |
| "Solve it without a dummy." | Peel leading matches in a `while head and head.val == val` loop first, then scan the rest. Correct but duplicated logic. |
| "Do it recursively." | `head.next = removeElements(head.next, val); return head.next if head.val == val else head`. Elegant, but O(n) stack — overflows at 10⁴ nodes. |
| "Remove nodes matching a **predicate**?" | Replace `current.val == val` with `predicate(current)`. Same skeleton. |
| "Remove **duplicates** instead?" | Compare against the previous kept value — [Remove Duplicates from Sorted List](83-remove-duplicates-from-sorted-list.md). |
| "Why is unlinking O(1) here but O(n) in an array?" | Arrays shift every subsequent element; a linked list rewires one pointer. |
| "Should you free the removed node?" | In Python, garbage collection handles it. In C/C++ you'd `free`/`delete` it — and you'd need to save the pointer before unlinking. |

**Traps:**

- **Advancing `prev` after an unlink.** *The* bug. `[1,6,6,2]` keeps the second 6. `prev` moves only when a node survives.
- **Returning `head` instead of `dummy.next`.** Wrong whenever the original head was removed — and `[7,7,7,7]` catches it immediately.
- **Forgetting `dummy.next = head`.** The dummy points nowhere and you return an empty list.
- **Using `while current:` when values could be falsy.** Here values are ≥ 1 so it's safe, but `is not None` is the precise check and generalizes.
- **Not handling an empty list.** `head = None` means the loop never runs and `dummy.next` is `None` — correct for free.
- **Recursion on large inputs.** `RecursionError` at 10⁴ nodes.

**This same move shows up in:** [Remove Nth Node From End of List](19-remove-nth-node-from-end-of-list.md) (dummy node so removing the head is uniform) · [Merge Two Sorted Lists](21-merge-two-sorted-lists.md) (dummy as the build-up anchor) · [Partition List](86-partition-list.md) (two dummies, one per output list) · [Remove Duplicates from Sorted List](83-remove-duplicates-from-sorted-list.md) (the same unlink mechanic without needing a sentinel).

</details>

---
