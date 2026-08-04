# 143. Reorder List

**Medium** · [LeetCode](https://leetcode.com/problems/reorder-list/) · [Solution file (no hints)](../../problems/0001-0499/143.py)

[📖 06. Linked List lesson](../learning/06-linked-list.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 06. Linked List problems](../rmap-practice/06-linked-list.md)

---

Given the head of a singly linked list `L₀ → L₁ → … → Lₙ₋₁ → Lₙ`, reorder it to:

```
L₀ → Lₙ → L₁ → Lₙ₋₁ → L₂ → Lₙ₋₂ → …
```

You may **not** modify the values in the nodes — only the nodes themselves may be changed.

```
[1,2,3,4]    →  [1,4,2,3]
[1,2,3,4,5]  →  [1,5,2,4,3]
```

**Constraints:** `1 <= number of nodes <= 5·10⁴` · `1 <= Node.val <= 1000` · modify **in place**, return nothing

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "L₀ → Lₙ → L₁ → Lₙ₋₁ …" | Alternate from the **front** and the **back**, converging in the middle |
| "may **not modify the values**" | ⚠️ No copying values around — you must relink actual nodes |
| "**singly** linked" | ⚠️ **The core difficulty.** You can't walk backwards, so "the last node", "the second-to-last"… are each an O(n) walk |
| in place, returns `None` | Mutate the given list; O(1) space is expected |
| n up to 5·10⁴ | O(n²) = 2.5·10⁹ → too slow. Need **O(n)** |

The naive approach fails instructively: to place `Lₙ` after `L₀` you walk to the end — O(n). Then `Lₙ₋₁` after `L₁` — another O(n). Total **O(n²)**, and at 5·10⁴ that's dead.

The problem is that a singly linked list is fundamentally *forward-only*, and the target order needs backward access.

**So make the backward part forward.** If you reversed the second half, then walking *forward* through it would visit `Lₙ, Lₙ₋₁, Lₙ₋₂, …` — exactly the sequence you need. Now both halves are traversed front-to-back, and you can interleave them with two simple pointers.

That decomposes into three routines you already have:

```
1. Find the middle          →  fast/slow pointers
2. Reverse the second half  →  problem 206
3. Zipper the two halves    →  alternate, like problem 21's merge
```

🤔 **Before you open the next section:** how do you find the middle of a list in one pass, without first counting its length?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Repeatedly find the last node | Walk to the end each time | **O(n²)** | O(1) | ❌ 2.5·10⁹ operations |
| Store nodes in an array | Index from both ends, relink | O(n) | **O(n)** | ⚠️ Correct and much easier — mention it |
| Deque of nodes | Pop from both ends alternately | O(n) | O(n) | ⚠️ Same trade |
| **Find middle → reverse → merge** | Three linear passes | **O(n)** | **O(1)** | ✅ |

**The decision: the three-phase in-place transformation.**

**Phase 1 — find the middle with [fast/slow pointers](../data-structures/linked-list.md).** `slow` advances one node per step, `fast` two. When `fast` reaches the end, `slow` is at the midpoint. One pass, no length count needed.

This is the other essential linked-list idiom alongside the dummy head, and it reappears in [Linked List Cycle](141-linked-list-cycle.md) and [Remove Nth Node](19-remove-nth-node-from-end-of-list.md).

**Phase 2 — reverse the second half.** Exactly [problem 206](206-reverse-linked-list.md)'s loop, applied to the sublist after `slow`.

**Phase 3 — zipper.** Walk both halves forward, alternating: take one from the front half, one from the reversed back half.

**Why splitting the list matters.** After finding the middle you set `slow.next = None`, cutting the list in two. Without that cut, the first half still runs into the second and the merge would loop forever or build a cycle. **The cut is what makes the two halves independent.**

**Why the array approach is worth mentioning.** Store every node in a list, then relink using indices from both ends — far simpler to write, O(n) space. If you're stuck in an interview, *say it, write it, then optimize*. The O(1)-space version is what they want, but a working O(n)-space solution beats nothing.

**Half-lengths and the odd case.** With an odd count the first half ends up one longer, which is exactly right: `[1,2,3,4,5]` splits into `[1,2,3]` and `[5,4]`, zippering to `1,5,2,4,3` ✅. The loop condition handles it naturally, as the trace shows.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
if head is None or head.next is None:
    return
```

Lists of 0 or 1 nodes are already correctly ordered. The guard also protects the phase-1 loop, which dereferences `head.next`.
→ [identity-operators](../syntax/identity-operators.md) · [logical-operators](../syntax/logical-operators.md) · [none-type](../syntax/none-type.md)

```python
slow = head
fast = head
while fast.next is not None and fast.next.next is not None:
    slow = slow.next
    fast = fast.next.next
```

**Phase 1 — find the middle.** `fast` moves twice as fast, so when it reaches the end `slow` is halfway.

The condition checks `fast.next` **and** `fast.next.next` — testing one step ahead so `slow` lands on the **end of the first half** rather than the start of the second. On `[1,2,3,4]` slow stops at node 2; on `[1,2,3,4,5]` it stops at node 3.

Order matters in the `and`: `fast.next` must be verified before `fast.next.next` is evaluated, or you'd dereference `None`. Python short-circuits, so this is safe.
→ [while-loop](../syntax/while-loop.md) · [logical-operators](../syntax/logical-operators.md)

```python
second_half_head = slow.next
slow.next = None
```

**The cut.** Save where the second half begins, then sever the link. Now there are two independent lists.

Forgetting `slow.next = None` is the classic bug here — the merge would then run into itself and build a cycle.

```python
previous_node = None
current_node = second_half_head
while current_node is not None:
    next_node = current_node.next
    current_node.next = previous_node
    previous_node = current_node
    current_node = next_node
second_half_head = previous_node
```

**Phase 2 — reverse the second half.** This is [problem 206](206-reverse-linked-list.md) verbatim: save the next node, flip the pointer, advance both.

`previous_node` ends on the original tail, which is the reversed half's head — hence the reassignment on the last line.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
first_pointer = head
second_pointer = second_half_head
```

**Phase 3 — zipper.** One pointer into each half, both walking forward.

```python
while second_pointer is not None:
    first_next = first_pointer.next
    second_next = second_pointer.next
```

**Save both next nodes before relinking** — the same save-then-destroy discipline as problem 206, now doubled because two pointers are about to be overwritten.

Loop on `second_pointer` because the second half is the **shorter or equal** one; when it's exhausted, the interleaving is complete.

```python
    first_pointer.next = second_pointer
    second_pointer.next = first_next
```

**The splice.** Insert the back-half node directly after the front-half node:

```
before:  [1] → [2]...      [4] → [3]
after:   [1] → [4] → [2]...
```

```python
    first_pointer = first_next
    second_pointer = second_next
```

Advance both to the saved positions and repeat.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:

        if head is None or head.next is None:
            return

        slow = head
        fast = head
        while fast.next is not None and fast.next.next is not None:
            slow = slow.next
            fast = fast.next.next

        second_half_head = slow.next
        slow.next = None

        previous_node = None
        current_node = second_half_head
        while current_node is not None:
            next_node = current_node.next
            current_node.next = previous_node
            previous_node = current_node
            current_node = next_node
        second_half_head = previous_node

        first_pointer = head
        second_pointer = second_half_head

        while second_pointer is not None:
            first_next = first_pointer.next
            second_next = second_pointer.next

            first_pointer.next = second_pointer
            second_pointer.next = first_next

            first_pointer = first_next
            second_pointer = second_next
```

</details>

**Trace it** — `[1,2,3,4,5]`:

**Phase 1** — `slow` ends at node 3, `fast` at node 5:
```
1 → 2 → 3 → 4 → 5
        ↑slow    ↑fast
```

**Cut:** `first = [1,2,3]`, `second = [4,5]`

**Phase 2** — reverse the second half: `second = [5,4]`

**Phase 3** — zipper:

| Step | `first` | `second` | Action | Result so far |
|---|---|---|---|---|
| 1 | 1 | 5 | `1→5`, `5→2` | `1 → 5 → 2 → 3` |
| 2 | 2 | 4 | `2→4`, `4→3` | `1 → 5 → 2 → 4 → 3` |
| 3 | 3 | None | loop ends | ✅ |

Final: `[1,5,2,4,3]` ✅

Note the odd case resolves itself — the first half had 3 nodes, the second 2, so node 3 ends up as the tail with nothing to interleave after it.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

| Phase | Cost |
|---|---|
| Find the middle | O(n/2) — `fast` traverses the whole list |
| Reverse the second half | O(n/2) |
| Zipper | O(n/2) iterations |

Three **sequential** passes: O(n) + O(n) + O(n) = **O(n)**. Sequential work adds, so three linear phases stay linear — the same accounting as [Valid Anagram](242-valid-anagram.md)'s two loops.

**Versus the naive O(n²).** Repeatedly walking to the tail costs 1 + 2 + 3 + … + n/2 = O(n²) → 2.5·10⁹ at the constraint limit. The reversal converts "walk backwards" — impossible in a singly linked list — into "walk forwards through a reversed half," which is where the whole speedup comes from.

**The generalizable idea:** *when a structure only supports one direction and you need the other, reverse it once (O(n)) instead of re-traversing repeatedly (O(n²)).*

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).**

Every phase uses a fixed handful of pointers — `slow`, `fast`, `previous_node`, `current_node`, `next_node`, `first_pointer`, `second_pointer`, and two temporaries. **No allocation**; only the arrows between existing nodes change, which is precisely what "may not modify the values in the nodes" demands.

**Compared to the array approach:**

```python
nodes = []
node = head
while node:
    nodes.append(node)
    node = node.next
# then relink using nodes[i] and nodes[-1-i]
```

That's O(n) space and much easier to get right — indexing from both ends is trivial, whereas the three-phase version has three separate places to make a pointer mistake.

**The trade is real:** O(n) space buys you significantly simpler code. The in-place version is what interviewers ask for, but **if you're stuck, write the array version, state its space cost, and then optimize.** A working O(n)-space solution is worth far more than a half-finished O(1) one.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The target order alternates front, back, front, back — but a singly linked list can't walk backwards, so naively fetching the last node each time is O(n²). The fix is to make the backward traversal forward: reverse the second half, and then walking it front-to-back visits the nodes in exactly the order I need. So it's three phases — find the middle with fast/slow pointers, reverse the second half, then zipper the two halves together, splicing one node from each alternately. I cut the list at the midpoint so the halves are independent, otherwise the merge builds a cycle. Three linear passes, so O(n) time and O(1) space. There's a much simpler O(n)-space version that stores the nodes in an array and indexes from both ends."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why reverse instead of walking back?" | **The question.** Singly linked lists are forward-only. Reversing once is O(n); repeatedly walking to the tail is O(n²). |
| "Show the simpler solution." | Store nodes in an array, relink with `nodes[i]` and `nodes[-1-i]`. O(n) space, far less pointer surgery. |
| "What if it were **doubly** linked?" | Trivial — walk from both ends simultaneously, no reversal needed. |
| "Why cut the list at the middle?" | Without `slow.next = None` the first half still points into the second, and the zipper creates a cycle. |
| "Odd vs even lengths?" | The loop condition puts the extra node in the *first* half, which is what the target order requires. Trace `[1,2,3]` → `[1,3,2]`. |
| "Check if the list is a palindrome." | Same first two phases — find the middle, reverse the second half — then compare instead of zipper. LeetCode 234. |

**Traps:**

- **Forgetting `slow.next = None`.** The most common bug: the halves stay connected and you build a cycle or loop forever.
- **Wrong fast/slow condition.** `while fast and fast.next` puts `slow` at the *start* of the second half rather than the end of the first — off by one, and the split lands in the wrong place.
- **Not saving both `next` pointers** in the zipper. You're overwriting two links per iteration, so you need two temporaries.
- **Looping on `first_pointer`** instead of `second_pointer` — the first half is the longer one, so you'd dereference `None`.
- **Swapping values instead of nodes.** Explicitly forbidden by the problem.
- **Trying to do it in one pass.** The interleaving genuinely needs the reversal first; there's no single-pass trick.

**This same move shows up in:** [Reverse Linked List](206-reverse-linked-list.md) (phase 2, verbatim) · [Linked List Cycle](141-linked-list-cycle.md) (fast/slow pointers) · [Remove Nth Node From End](19-remove-nth-node-from-end-of-list.md) (two pointers with a gap, to reach "from the end" in one pass) · [Merge Two Sorted Lists](21-merge-two-sorted-lists.md) (the interleaving discipline).

</details>
