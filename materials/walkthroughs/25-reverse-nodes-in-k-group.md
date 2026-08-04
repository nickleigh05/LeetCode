# 25. Reverse Nodes in k-Group

**Hard** · [LeetCode](https://leetcode.com/problems/reverse-nodes-in-k-group/)

[📖 06. Linked List lesson](../learning/06-linked-list.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 06. Linked List problems](../rmap-practice/06-linked-list.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Given the head of a linked list, reverse the nodes **k at a time** and return the modified list.

`k` is a positive integer less than or equal to the list's length. If the number of nodes is not a multiple of `k`, the **leftover nodes at the end stay as they are**.

You may not alter the values in the nodes — only the nodes themselves.

```
head = [1,2,3,4,5], k = 2  →  [2,1,4,3,5]
head = [1,2,3,4,5], k = 3  →  [3,2,1,4,5]
```

**Constraints:** `1 <= k <= n <= 5000` · `0 <= Node.val <= 1000` · **follow-up: O(1) extra memory**

> **Try it yourself first.** This is the hardest pointer manipulation in the unit — take it in pieces.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "reverse **k at a time**" | Chop the list into k-sized chunks and reverse each — [problem 206](206-reverse-linked-list.md) applied repeatedly |
| "leftover nodes **stay as they are**" | ⚠️ You must **check before reversing** whether k nodes remain. A partial group is left untouched |
| "may not alter the **values**" | Real pointer surgery; no value swapping |
| "**O(1)** memory" follow-up | No recursion (that's O(n/k) stack), no node array |
| n up to 5000 | O(n) expected |

The decomposition is straightforward:

```
[1,2,3,4,5], k = 2

  [1,2]   [3,4]   [5]
  reverse reverse leave
   ↓       ↓       ↓
  [2,1]   [4,3]   [5]        then reconnect:  2→1→4→3→5
```

**Reversing a chunk you already know how to do.** The difficulty is entirely in the **seams** — after reversing a group, its head and tail have swapped roles, and you must:

1. Point the **previous** group's tail at the reversed group's **new head**.
2. Point the reversed group's **new tail** at whatever follows.
3. Remember where the *next* group starts, before the reversal destroys that information.

Get any one of those wrong and the list fragments or loops.

**The other trap:** you can only reverse a group *after confirming k nodes exist*. Reverse first and discover the group was short, and you've already corrupted the list — with no easy way back in a singly linked list.

🤔 **Before you open the next section:** after reversing `[1,2]` to `[2,1]`, which node is the group's new tail — and what did it point to before you touched anything?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Collect nodes into an array | Reverse index ranges, relink | O(n) | **O(n)** | ⚠️ Much easier; fails the follow-up |
| Recursion | Reverse one group, recurse on the rest | O(n) | **O(n/k)** stack | ⚠️ Elegant, but not O(1) |
| **Iterative with a dummy head** | Reverse each group, stitch the seams | **O(n)** | **O(1)** | ✅ |

**The decision: iterate group by group, with a [dummy head](21-merge-two-sorted-lists.md) and four carefully-named pointers.**

The four pointers per group — naming them well is most of the battle:

| Pointer | Meaning |
|---|---|
| `group_prev` | The node **before** the current group (starts at the dummy) |
| `kth` | The group's **last** node, found by walking k steps |
| `group_next` | The node **after** the group (`kth.next`) — saved before reversing |
| `group_tail` | The group's **original first** node, which becomes its tail after reversal |

**The check-first discipline.** `get_kth` walks k steps and returns `None` if it falls off the end. That's the guard: **no k-th node ⇒ fewer than k remain ⇒ stop, leaving the remainder untouched.** Verifying before mutating is what makes the partial-group rule easy instead of painful.

**The trick that makes the reversal seamless.** In [problem 206](206-reverse-linked-list.md), `prev` started at `None` because the reversed list's tail should terminate. Here, initializing `prev = group_next` instead means **the group's new tail automatically points at the next group** — one of the three seam-fixes handled for free by a single initialization.

**Why the dummy head is required, not optional.** The first group's reversal changes the list's head. Without a dummy there's no `group_prev` for the first group, forcing a special case. With one, every group — including the first — has a predecessor.

**Why not recursion?** Genuinely clean, and worth mentioning: reverse the first k nodes, then set the new tail's `next` to the recursive result. But it's O(n/k) stack, failing the follow-up. And the array version, while easiest, is O(n) space — **say it exists if you're stuck, then push toward the iterative one.**

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
def get_kth(node, steps):
    while node and steps > 0:
        node = node.next
        steps -= 1
    return node
```

**The lookahead guard.** Walk `steps` nodes forward, returning `None` if you run off the end.

Called as `get_kth(group_prev, k)` — starting from the node *before* the group, so k steps lands exactly on the group's **last** node. Returning `None` is the signal that fewer than k nodes remain.
→ [function-basics](../syntax/function-basics.md) · [while-loop](../syntax/while-loop.md) · [truthy-falsy-values](../syntax/truthy-falsy-values.md)

```python
dummy = ListNode(0, head)
group_prev = dummy
```

The dummy precedes the real head, giving the first group a predecessor. `group_prev` always sits just before the group being processed.
→ [class-basics](../syntax/class-basics.md) · [linked-list](../data-structures/linked-list.md)

```python
while True:
    kth = get_kth(group_prev, k)
    if not kth:
        break
    group_next = kth.next
```

**Check, then commit.** If `kth` is `None`, fewer than k nodes remain — stop, leaving them in place.

`group_next` is saved **now**, before the reversal, because `kth.next` is about to be overwritten. This is the save-before-destroy discipline from [206](206-reverse-linked-list.md), applied to a boundary rather than a single node.
→ [break-continue](../syntax/break-continue.md) · [none-type](../syntax/none-type.md)

```python
    prev = group_next
    curr = group_prev.next
```

**The elegant initialization.** In [206](206-reverse-linked-list.md), `prev` started at `None`. Here it starts at `group_next`, so when the first node of the group gets flipped to point at `prev`, **it points at the next group** — becoming a correctly-connected tail with no extra work.

`curr` starts at the group's first node.

```python
    while curr != group_next:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node
```

**[Problem 206](206-reverse-linked-list.md)'s loop, bounded.** Identical four lines — save, flip, advance, advance — but the stopping condition is `curr != group_next` rather than `curr is None`, so it reverses **exactly this group** and no further.

When it ends, `prev` is on the group's **last** node, which is now its head.
→ [variables-assignment](../syntax/variables-assignment.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
    group_tail = group_prev.next
    group_prev.next = kth
    group_prev = group_tail
```

**The seam, in three lines — and the order is critical.**

1. `group_tail = group_prev.next` — **before** overwriting, capture the group's original first node. After reversal it's the group's *tail*, and therefore the `group_prev` for the next iteration.
2. `group_prev.next = kth` — connect the previous group to this one's new head (`kth`, the old last node).
3. `group_prev = group_tail` — advance to the next group's predecessor.

Swap lines 1 and 2 and `group_prev.next` is already `kth`, so `group_tail` would be wrong and the next group would be processed from the wrong position.

```python
return dummy.next
```

The head changed during the first reversal, so `dummy.next` — not `head` — is the answer.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:

        def get_kth(node, steps):
            while node and steps > 0:
                node = node.next
                steps -= 1
            return node

        dummy = ListNode(0, head)
        group_prev = dummy

        while True:
            kth = get_kth(group_prev, k)
            if not kth:
                break
            group_next = kth.next

            prev = group_next
            curr = group_prev.next

            while curr != group_next:
                next_node = curr.next
                curr.next = prev
                prev = curr
                curr = next_node

            group_tail = group_prev.next
            group_prev.next = kth
            group_prev = group_tail

        return dummy.next
```

</details>

**Trace it** — `[1,2,3,4,5]`, `k = 2`:

**Group 1** — `group_prev` = dummy:
- `kth` = node **2**, `group_next` = node **3**
- Reverse `1,2` with `prev` starting at node 3: `2 → 1 → 3`
- `group_tail` = node **1**; `dummy.next = 2`; `group_prev` = node **1**

```
dummy → 2 → 1 → 3 → 4 → 5
                ↑ group_prev is node 1
```

**Group 2** — `group_prev` = node 1:
- `kth` = node **4**, `group_next` = node **5**
- Reverse `3,4`: `4 → 3 → 5`
- `group_tail` = node **3**; `1.next = 4`; `group_prev` = node **3**

```
dummy → 2 → 1 → 4 → 3 → 5
                        ↑ group_prev is node 3
```

**Group 3** — `get_kth(node 3, 2)` walks to node 5, then off the end → **`None`** → `break`.

Node 5 is left untouched ✅

Final: `[2,1,4,3,5]` ✅

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

Per group of k nodes:
- `get_kth` walks k nodes → O(k)
- The reversal walks k nodes → O(k)
- The seam fix-up → O(1)

So O(2k) per group × (n/k) groups = **O(2n) = O(n)**.

Every node is visited a **constant** number of times — twice, once by the lookahead and once by the reversal. That constant is why the lookahead is affordable: checking before mutating costs a second pass over each group, not a re-pass over the whole list.

**Can the lookahead be avoided?** Only by knowing the length in advance (one extra O(n) pass) — same complexity, no benefit. **Or** by reversing optimistically and reversing back on a short group, which is more code and more risk. The check-first version is both simplest and fastest.

**The final partial group is O(k)** — one failed `get_kth` walk, then done.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — satisfying the follow-up.

Six pointers (`group_prev`, `kth`, `group_next`, `prev`, `curr`, `next_node`, `group_tail`) plus the dummy node. Constant, regardless of n or k. **No allocation**; only the arrows between existing nodes change, as required by "may not alter the values".

| Approach | Time | Space |
|---|---|---|
| **Iterative** | O(n) | **O(1)** |
| Recursive | O(n) | **O(n/k)** stack |
| Array of nodes | O(n) | **O(n)** |

**The recursion cost is real, not theoretical.** With k = 1 the recursion depth is n = 5000 — well past Python's default limit of 1000, so it would raise `RecursionError`. Same practical hazard as [problem 206](206-reverse-linked-list.md).
→ [recursion-limit](../syntax/recursion-limit.md)

**The array version is the honest fallback:** store every node, reverse index ranges, relink. Far easier to get right, O(n) space. **If the pointer surgery isn't coming together in an interview, write that, state the trade, then attempt the O(1) version** — a working solution beats a broken one.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The core is reversing a linked list, applied to fixed-size chunks — the difficulty is the seams between groups and the partial group at the end. I use a dummy head so the first group has a predecessor, and for each group I first walk k steps to check that a k-th node exists; if it doesn't, fewer than k remain and I stop, leaving them untouched. Checking before mutating is what makes the partial-group rule easy. Then I save the node after the group and run the standard reversal loop, but initializing `prev` to that saved node so the group's new tail automatically connects forward. Finally I point the previous group's tail at the new head and advance. Every node is visited twice, so O(n) time and O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why check for k nodes *before* reversing?" | **The question.** Reversing first and discovering the group was short leaves a corrupted list you can't easily undo in a singly linked list. |
| "Why initialize `prev = group_next`?" | So the group's first node — which becomes its tail — automatically points at the next group. One of the three seam-fixes, free. |
| "What if leftovers should also be reversed?" | Drop the `get_kth` guard and reverse whatever remains. That's LeetCode 25's variant, sometimes asked as a twist. |
| "Recursive version?" | Reverse the first k, then set the new tail's `next` to `reverseKGroup(group_next, k)`. Cleaner to read, O(n/k) stack. |
| "Simplify with O(n) space." | Store nodes in an array and reverse index slices. Much easier; fails the follow-up. |
| "What if k = 1, or k = n?" | k = 1 reverses nothing (each group of one is its own reverse); k = n reverses the entire list once. Both fall out of the same code. |
| "Swap nodes **pairwise**?" | The k = 2 case. LeetCode 24, and this solution handles it directly. |

**Traps:**

- **Reversing before checking the group length.** The list is corrupted and the remainder can't be restored.
- **Wrong order in the seam.** `group_tail` must be read *before* `group_prev.next` is overwritten.
- **`prev = None`** in the inner loop, copying [206](206-reverse-linked-list.md) verbatim. Each group's tail would then terminate the list, truncating everything after it.
- **`while curr` instead of `while curr != group_next`** — reverses the entire remaining list rather than just this group.
- **Returning `head`** instead of `dummy.next`. The head moved during the first reversal.
- **Forgetting the dummy** and special-casing the first group. It's doable but error-prone.

**This same move shows up in:** [Reverse Linked List](206-reverse-linked-list.md) (the inner loop, verbatim) · [Reorder List](143-reorder-list.md) (reverse-a-portion then reconnect) · [Merge Two Sorted Lists](21-merge-two-sorted-lists.md) (the dummy-head idiom) · [Remove Nth Node From End](19-remove-nth-node-from-end-of-list.md) (lookahead by a fixed number of steps).

</details>
