# 19. Remove Nth Node From End of List

**Medium** · [LeetCode](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) · [Solution file (no hints)](../../problems/0001-0499/19.py)

[📖 06. Linked List lesson](../learning/06-linked-list.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 06. Linked List problems](../rmap-practice/06-linked-list.md)

---

Given the head of a linked list, remove the **nth node from the end** and return the head.

```
head = [1,2,3,4,5], n = 2  →  [1,2,3,5]
head = [1],         n = 1  →  []
head = [1,2],       n = 1  →  [1]
head = [1,2],       n = 2  →  [2]      (removing the head)
```

**Constraints:** `1 <= size <= 30` · `1 <= n <= size` · **follow-up: can you do it in one pass?**

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "nth node **from the end**" | ⚠️ Counting backwards in a **forward-only** structure — the central difficulty |
| "**one pass**" follow-up | Rules out "count the length, then walk again". You must locate the position without knowing the length |
| `1 <= n <= size` | `n` is always valid — no out-of-range handling needed |
| removing the **head** is possible | ⚠️ When `n == size`. Deleting the first node is a special case… unless you plan for it |
| return the head | Which may be a *different* node than the one passed in |

**Deleting from a singly linked list requires the node *before* the target.** You remove `X` by writing `prev.next = X.next` — there's no way to unlink a node you're standing on, because you can't reach backwards to fix the pointer aimed at it.

So the real task: **find the node `n+1` from the end**, in one pass.

**The idea: a fixed gap between two pointers.** If `fast` is exactly `k` nodes ahead of `slow`, and you advance both in lockstep until `fast` falls off the end, then `slow` is left exactly `k` nodes from the end. The gap never changes — you're using the distance between two pointers as a ruler.

```
n = 2, gap = 3           ← n+1, so slow lands one before the target

[1] → [2] → [3] → [4] → [5] → None
 ↑                       ↑
slow                    fast

advance both until fast is None:

[1] → [2] → [3] → [4] → [5] → None
             ↑                  ↑
            slow               fast (None)

slow.next is [4] — the 2nd from the end. Remove it.
```

🤔 **Before you open the next section:** removing the head means there's no previous node to fix. What single trick from [problem 21](21-merge-two-sorted-lists.md) makes that stop being a special case?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Passes | Space | Verdict |
|---|---|---|---|---|
| Count, then walk again | Length first, then to position `size - n` | **2** | O(1) | ⚠️ Correct — but the follow-up asks for one |
| Store nodes in an array | Index directly to `len - n` | 1 | **O(n)** | ⚠️ Works, wastes memory |
| **Two pointers with a gap** | Fixed distance acts as a ruler | **1** | **O(1)** | ✅ |

**The decision: two pointers separated by `n + 1`, plus a [dummy head](../data-structures/linked-list.md).**

**Why the gap is `n + 1` and not `n`.** You need `slow` to stop at the node *before* the one being removed, so it can perform `slow.next = slow.next.next`. A gap of `n` would land `slow` **on** the target — too late to unlink it. One extra step of separation buys you the predecessor.

**Why the dummy head is essential here, not just convenient.** Consider `[1,2]` with `n = 2` — the head itself must go. Without a dummy there's no previous node, forcing a branch:

```python
if <removing the head>:
    return head.next
```

Start both pointers at a dummy whose `next` is `head`, and the head gains a predecessor like every other node. The special case **disappears** rather than being handled.

This is the second appearance of the dummy-head idiom, and note the different reason: [problem 21](21-merge-two-sorted-lists.md) used it while *building* a list; here it's for *deleting the first node*. Those two situations are exactly when to reach for it.

**Why `dummy.next` must be returned, not `head`.** If the head was removed, the local `head` variable still points at the now-detached node. `dummy.next` always reflects the current first node.

**Why not two passes?** Perfectly correct, and worth saying as your baseline. But the follow-up explicitly asks for one — and the gap technique is the transferable idea, not a micro-optimization: **the distance between two pointers is information.**

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
dummy = ListNode(0, head)
slow = dummy
fast = dummy
```

The dummy sits **before** the real head (`ListNode(0, head)` sets both value and `next`), giving the head a predecessor.

Both pointers start at the dummy — starting them together is what makes the gap below exactly `n + 1` *relative to the dummy*, which is the offset that lands `slow` on the predecessor.
→ [class-basics](../syntax/class-basics.md) · [linked-list](../data-structures/linked-list.md)

```python
for _ in range(n + 1):
    fast = fast.next
```

**Open the gap.** Advance `fast` by `n + 1`, leaving `slow` behind at the dummy.

`_` is the conventional name for a loop variable you never use — the count matters, not the value.

The `+ 1` is *the* detail of this problem. Off by one here and you delete the wrong node.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md)

```python
while fast is not None:
    fast = fast.next
    slow = slow.next
```

**Advance in lockstep**, preserving the gap, until `fast` runs past the end.

Because the separation is constant, when `fast` becomes `None` (one past the last node), `slow` is exactly `n + 1` positions back from there — sitting on the node just before the one to remove.
→ [while-loop](../syntax/while-loop.md) · [identity-operators](../syntax/identity-operators.md)

```python
slow.next = slow.next.next
```

**The deletion.** Route `slow`'s pointer around the target, skipping it. The removed node is now unreferenced (Python garbage-collects it; in C you'd free it).

This single line is why the whole `n + 1` gymnastics existed — it needs `slow` to be the *predecessor*.

```python
return dummy.next
```

**`dummy.next`, never `head`.** If the head was the node removed, `head` now points at a detached node. `dummy.next` is always the true current head — and it's `None` if the list is now empty.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:

        dummy = ListNode(0, head)
        slow = dummy
        fast = dummy

        for _ in range(n + 1):
            fast = fast.next

        while fast is not None:
            fast = fast.next
            slow = slow.next

        slow.next = slow.next.next

        return dummy.next
```

</details>

**Trace it** — `[1,2,3,4,5]`, `n = 2`:

```
dummy → 1 → 2 → 3 → 4 → 5 → None
```

**Open the gap** (3 steps): `fast` → node 2. `slow` stays at dummy.

| `slow` at | `fast` at | Step |
|---|---|---|
| dummy | 2 | start |
| 1 | 3 | |
| 2 | 4 | |
| **3** | 5 | |
| 3 | **None** | loop ends |

`slow` is on node **3**, so `slow.next` is node **4** — the 2nd from the end ✅

`slow.next = slow.next.next` links 3 → 5. Result: `[1,2,3,5]` ✅

**The head-removal case** — `[1,2]`, `n = 2`:

Gap of 3: `fast` goes dummy → 1 → 2 → **None**. The `while` never runs, so `slow` is still on the **dummy**.

`slow.next = slow.next.next` sets `dummy.next = node 2`, removing node 1. `return dummy.next` → `[2]` ✅

**No special case was needed** — that's the dummy head earning its place.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(L)</summary>

**O(L)**, where L is the list length. (Calling it L avoids confusing it with the problem's `n`.)

- Opening the gap: `n + 1` steps, and `n <= L`.
- The lockstep walk: `fast` travels from position `n+1` to the end — `L - n` more steps.

Total pointer moves: `(n + 1) + (L - n) = L + 1` → **O(L)**.

**Genuinely one pass.** `fast` traverses the list exactly once and never revisits a node; `slow` covers a suffix of that same path. The two-pass version walks the list twice — same O(L), but literally double the traversals.

**Why the gap technique works at all:** you can't know "n from the end" without knowing the end — but you don't need the *length*, only a **fixed offset from the end**, and two pointers a constant distance apart give you that for free as one of them arrives.

**The generalizable idea:** *the distance between two pointers is itself information.* Same family as [Reorder List](143-reorder-list.md)'s fast/slow midpoint finder, where the ratio of speeds (rather than a fixed gap) does the measuring.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).**

Two pointers and one dummy node — constant, regardless of list length. No allocation proportional to the input; the list is modified in place by rerouting a single pointer.

| Approach | Passes | Space |
|---|---|---|
| **Two pointers + dummy** | **1** | **O(1)** |
| Count then walk | 2 | O(1) |
| Array of nodes | 1 | **O(n)** |

The array version is the tempting shortcut — store every node, then index `len - n`. It's one pass and easy, but O(n) space to answer a question that needs only two pointers.

**The dummy node is a single allocation**, O(1). Cheap price for deleting an entire branch of special-case logic — the same bargain as [problem 21](21-merge-two-sorted-lists.md).

**Nothing is copied.** As throughout this unit, you're rearranging arrows between existing nodes.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "To delete a node in a singly linked list I need the node *before* it, and I need to count from the end without knowing the length. Both fall out of two pointers with a fixed gap: I advance `fast` by `n + 1`, then move both together until `fast` runs off the end — at which point `slow` is sitting exactly on the predecessor of the node to remove. The `+1` is what makes it the predecessor rather than the target itself. I also start both at a dummy node placed before the head, so that removing the head isn't a special case — it gets a predecessor like every other node — and I return `dummy.next` rather than `head`, since the head may be the node I deleted. One pass, O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why a gap of `n + 1`?" | **The question.** A gap of `n` lands `slow` *on* the target, and you can't unlink the node you're standing on. One extra step gives you its predecessor. |
| "Why the dummy node?" | Removing the head has no predecessor. The dummy supplies one, deleting the special case entirely. Demo with `[1,2]`, `n = 2`. |
| "What if `n` could exceed the length?" | Guard the gap loop: if `fast` becomes `None` early, return `head` unchanged (or raise). The constraints exclude it here. |
| "Remove the nth from the **start**?" | Much easier — walk `n-1` steps and unlink. Still worth a dummy for `n = 1`. |
| "Remove **all** nodes with a given value?" | Same dummy-head idiom, walking the list and skipping matches. LeetCode 203. |
| "Two-pass version?" | Count the length, then walk to `length - n`. Same complexity, but the follow-up asked for one pass. |
| "Find the middle instead?" | Fast/slow with a 2× *speed* difference rather than a fixed gap — see [Reorder List](143-reorder-list.md). |

**Traps:**

- **Gap of `n` instead of `n + 1`.** Off by one — you land on the target and can't remove it.
- **No dummy node.** Head removal then needs a special branch, and it's easy to get wrong.
- **Returning `head` instead of `dummy.next`.** Returns a detached node when the head was removed.
- **Starting `slow` at `head` and `fast` at `dummy`** (or any mismatch). Both must start at the same place for the gap to mean what you think.
- **`while fast.next is not None`** instead of `while fast is not None` — stops one step early, so `slow` lands one node short.
- **Storing all nodes in an array** — works, but O(n) space when two pointers suffice.

**This same move shows up in:** [Reorder List](143-reorder-list.md) (fast/slow pointers, speed-based rather than gap-based) · [Linked List Cycle](141-linked-list-cycle.md) (two pointers at different speeds) · [Merge Two Sorted Lists](21-merge-two-sorted-lists.md) (the dummy-head idiom, for building instead of deleting) · [Reverse Nodes in k-Group](25-reverse-nodes-in-k-group.md) (dummy head plus careful offsets).

</details>

---
