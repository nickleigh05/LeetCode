# 206. Reverse Linked List

**Easy** · [LeetCode](https://leetcode.com/problems/reverse-linked-list/) · [Solution file (no hints)](../../problems/0001-0499/206.py)

[📖 06. Linked List lesson](../learning/06-linked-list.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 06. Linked List problems](../rmap-practice/06-linked-list.md)

---

Given the `head` of a singly linked list, **reverse** the list and return the new head.

```
input:   1 → 2 → 3 → 4 → 5 → None
output:  5 → 4 → 3 → 2 → 1 → None

input:   []        →  []
input:   [1]       →  [1]
```

**Constraints:** `0 <= number of nodes <= 5000` · `-5000 <= Node.val <= 5000` · **follow-up: can you do it both iteratively and recursively?**

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

This is **the** foundational linked-list problem. The three-pointer dance you learn here appears inside half of Unit 06, so it's worth being able to write from muscle memory.

| The statement says | Which really means |
|---|---|
| "**singly** linked list" | ⚠️ Each node knows only its `next`. There's no way back — once you overwrite a pointer, whatever it referenced is unreachable unless you saved it |
| "**reverse**" | Every `next` pointer flips direction. The nodes themselves don't move |
| "return the **new head**" | The old tail becomes the head — and you must return it, since the caller's `head` is now the tail |
| 0 nodes allowed | Empty input must return `None`, not crash |
| "iteratively **and** recursively" | Both are expected. The trade is space |

**The core difficulty, stated plainly.** To reverse the link at `curr`, you write `curr.next = prev`. But `curr.next` was the *only* reference to the rest of the list — overwrite it and everything downstream is orphaned:

```
prev    curr
 ↓       ↓
None ←  1   →  2 → 3 → 4 → None
        
after curr.next = prev:

None ← 1        2 → 3 → 4 → None
                ↑ nothing points here any more. Lost.
```

So the sequence must be: **save the next node, flip the pointer, then advance.** Three variables, and the order of the four lines is the entire problem.

🤔 **Before you open the next section:** write the four assignment statements in the order they must happen. What breaks if you advance `curr` before flipping, or flip before saving?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Copy values to a list, rewrite | Read all values, write them back reversed | O(n) | **O(n)** | ⚠️ Works, but sidesteps the pointer manipulation being tested |
| Recursion | Reverse the rest, then fix the current link | O(n) | **O(n)** stack | ✅ Elegant; mention it |
| **Iterative three-pointer** | Walk once, flipping as you go | **O(n)** | **O(1)** | ✅ |

**The decision: the iterative three-pointer walk.**

Maintain:
- **`prev`** — the head of the already-reversed portion (starts `None`, because the original head becomes the tail and must point at `None`).
- **`curr`** — the node being processed.
- **`next_node`** — a temporary holding `curr.next` *before* it's overwritten.

The invariant, worth saying out loud:

> **Everything behind `curr` is already reversed and reachable from `prev`. Everything from `curr` onward is still the original forward list.**

Each iteration moves one node across that boundary.

**Why `prev` starts as `None`.** The original head becomes the new tail, and a tail's `next` must be `None`. Starting `prev = None` makes the very first flip do exactly that with no special case. It also means empty input returns `None` correctly — the loop never runs and `prev` is returned unchanged.

**Why not the value-copy approach?** It works and it's O(n) time — but the point of the problem is pointer surgery, and it costs O(n) space. Interviewers will ask for O(1).

**Why mention recursion?** The follow-up asks for it, and it's genuinely elegant. But it's O(n) stack space and, at 5000 nodes, close to Python's default recursion limit. **Iterative is strictly better here; know both, prefer the loop.**

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
prev = None
curr = head
```

`prev` is the reversed portion (empty so far, hence `None`). `curr` walks the original list from the front.

`prev = None` is load-bearing twice: it terminates the reversed list correctly, and it's the correct return value for empty input.
→ [none-type](../syntax/none-type.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
while curr:
```

Run until you fall off the end. A node object is truthy and `None` is falsy, so `while curr` reads naturally — though `while curr is not None` is more explicit and equally common.
→ [while-loop](../syntax/while-loop.md) · [truthy-falsy-values](../syntax/truthy-falsy-values.md)

```python
    next_node = curr.next
```

**Save before you destroy.** This is the line that makes the whole thing possible — after the next statement, `curr.next` no longer points forward, and this variable is the *only* remaining reference to the rest of the list.

Every linked-list problem in this unit has some version of this line.

```python
    curr.next = prev
```

**The flip.** `curr` now points backward. On the first iteration this sets the original head's `next` to `None`, correctly making it the new tail.

```python
    prev = curr
    curr = next_node
```

**Advance both, in this order.** `prev` moves onto the node just reversed (it's now the head of the reversed portion), and `curr` moves to the saved next node.

Do these two in the wrong order — `curr = next_node` before `prev = curr` — and `prev` would be assigned the *new* `curr`, skipping a node and corrupting the list.

```python
return prev
```

**`prev`, not `curr`.** The loop ends when `curr` is `None`, having walked off the end. `prev` is sitting on the last node processed — the original tail, which is the new head.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:

        prev = None
        curr = head

        while curr:
            next_node = curr.next
            curr.next = prev
            prev = curr
            curr = next_node

        return prev
```

</details>

**Trace it** — `1 → 2 → 3 → None`:

| Step | `prev` | `curr` | `next_node` | List state after the flip |
|---|---|---|---|---|
| start | None | 1 | — | `1 → 2 → 3 → None` |
| 1 | 1 | 2 | 2 | `None ← 1`   `2 → 3 → None` |
| 2 | 2 | 3 | 3 | `None ← 1 ← 2`   `3 → None` |
| 3 | 3 | None | None | `None ← 1 ← 2 ← 3` |
| exit | **3** | None | | `return 3` ✅ |

**The recursive version**, for the follow-up:

```python
def reverseList(self, head):
    if not head or not head.next:
        return head
    new_head = self.reverseList(head.next)
    head.next.next = head    # the node ahead now points back at me
    head.next = None         # and I become the tail
    return new_head
```

`head.next.next = head` is the flip: whatever `head` points at should point back. Clean, but O(n) stack.
→ [recursion-basics](../syntax/recursion-basics.md) · [recursion-limit](../syntax/recursion-limit.md)

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

One pass, visiting each node exactly once. Each iteration does four constant-time assignments — no traversal, no search, no allocation.

**O(n)** total, and it can't be beaten: reversing every pointer means touching every node at least once.

**No early exit** — every link must flip.

**The recursive version is also O(n)** time. It recurses to the end first, then does the flips while unwinding — same number of operations, just in reverse order. The only difference is space.

**A note on the constant factor:** each step is a handful of pointer writes with no memory allocation, so this is genuinely fast in practice. The value-copying approach does the same asymptotic work but allocates an n-element list, which is measurably slower and pointlessly so.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — three pointer variables, regardless of list length.

**This is why the iterative version is preferred**, and the comparison is worth having ready:

| Approach | Time | Space | Note |
|---|---|---|---|
| **Iterative** | O(n) | **O(1)** | ✅ |
| Recursive | O(n) | **O(n)** | One stack frame per node |
| Copy to array | O(n) | O(n) | Allocates, and dodges the real exercise |

**The recursion depth is a practical hazard, not just theoretical.** At the constraint's 5000 nodes, the recursive version sits near Python's default recursion limit of 1000 — it would actually raise `RecursionError`. That's a concrete reason to prefer the loop here, and a good thing to mention.
→ [recursion-limit](../syntax/recursion-limit.md)

**Nothing is allocated.** The nodes are reused in place; only the arrows between them change. That's the defining characteristic of linked-list problems — you rearrange references, you don't build new structures. Keep it in mind for the whole unit.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The obstacle is that in a singly linked list, `curr.next` is my only reference to the rest — so if I overwrite it to point backward, I lose everything downstream. The fix is three pointers: save `curr.next` in a temporary, flip `curr.next` to point at `prev`, then advance both `prev` and `curr`. `prev` starts as `None` because the original head becomes the tail and must terminate the list — and that also makes empty input return `None` for free. At the end `curr` has run off the end, so I return `prev`, which is sitting on the original tail. O(n) time, O(1) space. The recursive version is elegant but O(n) stack, and at 5000 nodes it would blow Python's recursion limit."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Write it recursively." | Recurse to the end, then `head.next.next = head; head.next = None`. O(n) stack — mention the depth risk. |
| "Reverse only nodes `m` to `n`." | Walk to position `m-1`, reverse the sublist, then reconnect both ends. The bookkeeping is the hard part. LeetCode 92. |
| "Reverse in groups of **k**." | Same core loop applied k nodes at a time, reconnecting groups. See [Reverse Nodes in k-Group](25-reverse-nodes-in-k-group.md). |
| "Check whether the list is a palindrome." | Find the middle, reverse the second half, compare. Uses this routine as a step. LeetCode 234. |
| "Why return `prev` and not `curr`?" | `curr` is `None` at exit — it walked off the end. `prev` holds the last real node. |
| "What if it were **doubly** linked?" | Swap each node's `prev` and `next`, then return the old tail. Easier, because you can always get back. |

**Traps:**

- **Forgetting to save `curr.next`.** You orphan the rest of the list on the very first iteration. *The* bug of this problem.
- **Wrong order in the two advance lines.** `curr = next_node` before `prev = curr` makes `prev` skip a node.
- **Returning `curr` or `head`.** `curr` is `None`; `head` is now the tail.
- **Starting `prev = head`.** Creates a cycle — the head would point to itself.
- **`while curr.next`** instead of `while curr` — stops one node early, leaving the last node unreversed.
- **Building a new list of nodes** instead of relinking. Works, wastes O(n).

**This same move shows up in:** [Reorder List](143-reorder-list.md) (uses this exact routine as phase 2) · [Reverse Nodes in k-Group](25-reverse-nodes-in-k-group.md) (this routine, applied k at a time) · [Add Two Numbers](2-add-two-numbers.md) (the same save-then-relink discipline) · [Merge Two Sorted Lists](21-merge-two-sorted-lists.md) (pointer surgery with a dummy head).

</details>
