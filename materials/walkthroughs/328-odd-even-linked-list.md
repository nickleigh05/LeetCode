# 328. Odd Even Linked List

**Medium** · [LeetCode](https://leetcode.com/problems/odd-even-linked-list/) · [Solution file (no hints)](../../problems/0001-0499/328.py)

[📖 06. Linked List lesson](../learning/06-linked-list.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 06. Linked List problems](../rmap-practice/06-linked-list.md)

---

Given the `head` of a singly linked list, group all nodes at **odd positions** together, followed by all nodes at **even positions**, and return the reordered list. The first node is position 1 (odd), the second is position 2 (even), and so on.

Keep the **relative order** inside each group. You must use **O(1) extra space** and **O(n) time**.

```
1 → 2 → 3 → 4 → 5           →   1 → 3 → 5 → 2 → 4
2 → 1 → 3 → 5 → 6 → 4 → 7   →   2 → 3 → 6 → 7 → 1 → 5 → 4
```

**Constraints:** `0 <= nodes <= 10⁴` · `-10⁶ <= Node.val <= 10⁶`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| odd/even **positions** | It's about the node's **index**, not its value. The second example's values make that clear |
| keep **relative order** | Within each group, nodes stay in their original sequence |
| O(1) extra space | No copying values into a list. You must **relink** the existing nodes |
| O(n) time | One pass |
| list may be empty | `None` → `None` |

**The picture.** Think of two threads woven together: odd nodes `1, 3, 5, …` and even nodes `2, 4, …`, alternating. You want to pull them apart into two separate chains, then tie the end of the odd chain to the start of the even chain.

```
odd :  1 ───→ 3 ───→ 5
even:     2 ───→ 4
result: 1 → 3 → 5 → 2 → 4
```

**Two pointers, hopping over each other.** Keep `odd` on the latest odd node and `even` on the latest even node. Each step:

- `odd.next = even.next`: the odd node skips over its even neighbour to the next odd node.
- `even.next = odd.next`: the even node skips over the new odd node to the next even node.

Each pointer jumps two places, building its own chain as it goes.

**Remember where the even chain starts.** Once the walk is done you need to attach the even chain to the end of the odd chain, so save `even_head` before you begin. Otherwise it's lost.

🤔 **Before you open the next section:** what condition should stop the walk, so that neither `odd.next = even.next` nor `even.next = odd.next` reads past the end?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Copy values to a list | Collect values, rearrange, write back | O(n) | O(n) | ❌ Breaks the O(1) rule |
| Two dummy heads | Append each node to an odd or even chain, then join | O(n) | O(1) | ✅ Works, slightly more code |
| **Weave two pointers in place** | `odd` and `even` each skip one node per step | **O(n)** | **O(1)** | ✅ |

**The decision: two [linked-list](../data-structures/linked-list.md) pointers relinked in place.**

It needs no dummy nodes. The two chains already exist inside the list, alternating, and the walk just separates them.

**The stopping condition.** The `even` pointer is always one step ahead. Stop when `even` is `None` (the list had an odd length) or `even.next` is `None` (an even length). In either case, there's no further odd node to move to.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
if head is None:
    return None
```

An empty list has nothing to reorder, and the next lines read `head.next`, which would crash on `None`.
→ [none-type](../syntax/none-type.md) · [identity-operators](../syntax/identity-operators.md) · [if-return](../syntax/if-return.md)

```python
odd = head
even = head.next
even_head = even
```

`odd` starts at position 1 and `even` at position 2. **`even_head` saves the start of the even chain**, which you'll need at the very end. With a one-node list, `even` is `None`, and the loop below simply doesn't run.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
while even is not None and even.next is not None:
    odd.next = even.next
    odd = odd.next
```

**The odd pointer moves forward.** Link the current odd node to the next odd node, which comes straight after `even`, then step onto it.

The loop condition checks `even` first. If `even` is `None`, Python stops evaluating, so `even.next` is never read on `None`.
→ [while-loop](../syntax/while-loop.md) · [logical-operators](../syntax/logical-operators.md)

```python
    even.next = odd.next
    even = even.next
```

**The even pointer moves forward**, skipping over the odd node that was just reached. It's fine if `odd.next` is `None` here. That just ends the even chain.

The order matters: `odd` moves **first**, so `even.next = odd.next` uses the new odd node.

```python
odd.next = even_head
return head
```

**Tie the chains together.** The end of the odd chain points at the start of the even chain. The head never changes, since position 1 stays first.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def oddEvenList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None:
            return None

        odd = head
        even = head.next
        even_head = even

        while even is not None and even.next is not None:
            odd.next = even.next
            odd = odd.next
            even.next = odd.next
            even = even.next

        odd.next = even_head
        return head
```

</details>

**Trace it.** `1 → 2 → 3 → 4 → 5`:

| Step | `odd` | `even` | odd chain | even chain |
|---|---|---|---|---|
| start | 1 | 2 | 1 | 2 |
| loop 1 | 3 | 4 | 1 → 3 | 2 → 4 |
| loop 2 | 5 | `None` | 1 → 3 → 5 | 2 → 4 → `None` |
| stop | `even is None` | | | |
| join | | | 1 → 3 → 5 → **2 → 4** | |

Result `1 → 3 → 5 → 2 → 4` ✅.

**Even length.** With `1 → 2 → 3 → 4`, after loop 1 `odd = 3` and `even = 4`, but `even.next` is `None`, so the loop stops. Joining gives `1 → 3 → 2 → 4` ✅.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).** Each loop iteration moves both pointers forward by two nodes, so every node is visited once. Each step is a constant number of pointer updates.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).** Three pointers (`odd`, `even`, `even_head`), however long the list is. No nodes are created and no values are copied, which is exactly what the problem asks for.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Odd- and even-position nodes alternate, so I can separate them into two chains in place. I keep an `odd` pointer and an `even` pointer and save the head of the even chain. Each step, odd links to the node after even and moves onto it, then even links to the node after the new odd and moves onto it. I stop when even or even.next is None, then attach the odd chain's tail to the saved even head. O(n) time, O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Group by odd/even **value** instead?" | Use two dummy heads and append each node to the matching chain by its value. That's [Partition List](86-partition-list.md) with a different test. |
| "Why save `even_head`?" | After the walk, `even` is at or past the end. Without the saved head, the start of the even chain is unreachable. |
| "Why `even and even.next` as the condition?" | `even` is always one node ahead. If it or its `next` is `None`, there's no further odd node. |
| "Interleave two lists (the reverse problem)?" | [Reorder List](143-reorder-list.md) merges two halves alternately with the same kind of pointer juggling. |

**Traps:**

- **Losing `even_head`.** Saving it at the start is the step people forget.
- **Grouping by value.** Re-read the problem: it's positions.
- **Updating `even` before `odd`.** Then `even.next = odd.next` uses the old odd node, and the chains get tangled.
- **Wrong loop condition.** `while odd.next` reads past the end in some cases and creates cycles in others.
- **Missing the `head is None` check.** `head.next` crashes on an empty list.

**This same move shows up in:** [Partition List](86-partition-list.md) (splitting a list into two chains and rejoining them) · [Reorder List](143-reorder-list.md) (weaving two chains together, the opposite operation) · [Swap Nodes in Pairs](24-swap-nodes-in-pairs.md) (pointer juggling two nodes at a time) · [Reverse Linked List](206-reverse-linked-list.md) (the basic in-place relinking skill).

</details>

---
