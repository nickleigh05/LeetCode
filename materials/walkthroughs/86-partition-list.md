# 86. Partition List

**Medium** · [LeetCode](https://leetcode.com/problems/partition-list/) · [Solution file (no hints)](../../problems/0001-0499/86.py)

[📖 06. Linked List lesson](../learning/06-linked-list.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 06. Linked List problems](../rmap-practice/06-linked-list.md)

---

Given the head of a linked list and a value `x`, partition it so that all nodes **less than `x`** come before nodes **greater than or equal to `x`**. You must **preserve the original relative order** within each partition.

```
head = [1,4,3,2,5,2], x = 3  →  [1,2,2,4,3,5]
head = [2,1],         x = 2  →  [1,2]
```

**Constraints:** `0 <= number of nodes <= 200` · `-100 <= Node.val <= 100` · `-200 <= x <= 200`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "less than `x`" before "**≥ `x`**" | Two groups, split by a strict `<` test. Note `x` itself belongs in the **second** group |
| "**preserve relative order**" | ⚠️ A **stable** partition. This is the constraint that rules out the swap tricks from [Sort Colors](75-sort-colors.md) |
| "partition", not "sort" | You don't need the values ordered — just the two groups separated |
| `0 <= nodes` | Empty list must work |
| singly linked | Forward-only; you can't swap positions cheaply |

**Why the array tricks don't apply.** On an array, [Sort Colors](75-sort-colors.md) partitions in place by swapping elements across the array — but swapping destroys relative order, and here order must be preserved. On a linked list you also can't index, so there's no obvious in-place two-pointer partition.

**The idea that makes it easy — and it's much simpler than fighting the list in place:**

> **Build two separate lists** as you walk: one for nodes `< x`, one for nodes `>= x`. Then join them.

```
input:  1 → 4 → 3 → 2 → 5 → 2      x = 3

less:   1 → 2 → 2
greater: 4 → 3 → 5

join:   1 → 2 → 2 → 4 → 3 → 5   ✅
```

**Stability is free.** Because you append to each list in the order you encounter nodes, relative order within each group is automatically preserved. You never have to think about it — which is exactly why this decomposition beats trying to rearrange the original list.

**Two dummy nodes.** Each output list needs a head you can build from, and both lists may start empty. Sentinels remove every "is this list empty yet?" branch — the same pattern as [Remove Linked List Elements](203-remove-linked-list-elements.md), applied twice.

🤔 **Before you open the next section:** when you join the two lists at the end, what must you do to the tail of the second one — and why is it essential?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Collect values, sort/partition, rewrite | Copy to an array, partition, write back | O(n) | **O(n)** | ⚠️ Correct, but it's a value rewrite, not pointer work |
| In-place swaps | Move nodes around the original list | — | — | ❌ Destroys relative order |
| Insertion-style rearrangement | Splice each small node to the front region | O(n²) | O(1) | ⚠️ Correct but quadratic and fiddly |
| **Two lists + two dummies** | Split while walking, then concatenate | **O(n)** | **O(1)** | ✅ |

**The decision: two dummy-headed lists, built in one pass, then joined.**

Four pointers, and naming them clearly is most of the work:

| Pointer | Role |
|---|---|
| `less_dummy` | sentinel heading the `< x` list |
| `less_tail` | where to append the next small node |
| `greater_dummy` | sentinel heading the `>= x` list |
| `greater_tail` | where to append the next large node |

Walk the input once; each node goes onto exactly one tail. Then:

```python
greater_tail.next = None            # ⚠️ terminate — see below
less_tail.next = greater_dummy.next # join
return less_dummy.next
```

**Why `greater_tail.next = None` is mandatory** — and it's *the* bug on this problem:

The nodes are the **original** nodes, still carrying their original `next` pointers. The last node you append to the `greater` list probably still points somewhere back in the input. Without explicitly terminating it, you get a list that runs off into old links — often producing a **cycle** and an infinite loop when the judge traverses your answer.

On `[1,4,3,2,5,2]` with `x = 3`: the greater list ends at node `5`, whose original `next` is the final `2`. Leave it and the output is `1→2→2→4→3→5→2`, with that trailing `2` also reachable from the less list — a corrupted structure.

**Does `less_tail` need terminating too?** No — it gets overwritten by the join (`less_tail.next = greater_dummy.next`). Only the *final* tail of the combined list needs an explicit `None`.

**Why two dummies rather than tracking heads manually.** Without sentinels you'd need `if less_head is None: less_head = node else: less_tail.next = node` on every append — two branches, duplicated for both lists. The dummies collapse all of that into one unconditional `tail.next = node`.

**Why not partition in place?** Any in-place approach either loses stability (swaps) or degenerates to O(n²) (repeated splicing to a moving boundary). Building two lists is O(n), stable, and uses only a constant number of extra nodes.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
less_dummy = ListNode(0)
greater_dummy = ListNode(0)
less_tail = less_dummy
greater_tail = greater_dummy
```

**Two sentinels and two tails.** Each `tail` marks where the next node of its group gets appended; each `dummy` remembers where that group starts.

Starting both tails *at* their dummies is what makes the first append branch-free.
→ [class-basics](../syntax/class-basics.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
current = head
while current is not None:
```

One pass over the input list.
→ [while-loop](../syntax/while-loop.md) · [none-type](../syntax/none-type.md)

```python
    if current.val < x:
        less_tail.next = current
        less_tail = current
    else:
        greater_tail.next = current
        greater_tail = current
```

**Append to the appropriate list, then advance that tail.**

Note the test is strictly `<`, so a node equal to `x` goes to the **greater** list — matching "less than `x`" before "greater than **or equal to** `x`".

Because nodes are appended in encounter order, **stability is automatic**. There's no extra work to preserve relative order.
→ [comparison-operators](../syntax/comparison-operators.md) · [elif-else](../syntax/elif-else.md)

```python
    current = current.next
```

Advance **before** the next iteration rewires anything.

⚠️ This read is safe *now*, but it's why the termination step below matters: we're reusing the original nodes, and their old `next` pointers are still live until overwritten.

```python
greater_tail.next = None
```

**Terminate the greater list — the critical line.**

The last appended node still carries its original `next`, which may point back into the input. Setting it to `None` cuts that stale link and prevents a cycle.
→ [none-type](../syntax/none-type.md)

```python
less_tail.next = greater_dummy.next
```

**Join.** The less list's tail now points at the greater list's first *real* node (skipping its sentinel).

If the greater list is empty, `greater_dummy.next` is `None`, and this correctly terminates the combined list — no special case.

```python
return less_dummy.next
```

The head of the joined list — or `None` if the input was empty, or the greater list's head if no node was `< x`. All three cases fall out of the sentinel design.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def partition(self, head: Optional[ListNode], x: int) -> Optional[ListNode]:

        less_dummy = ListNode(0)
        greater_dummy = ListNode(0)
        less_tail = less_dummy
        greater_tail = greater_dummy

        current = head
        while current is not None:
            if current.val < x:
                less_tail.next = current
                less_tail = current
            else:
                greater_tail.next = current
                greater_tail = current
            current = current.next

        greater_tail.next = None
        less_tail.next = greater_dummy.next

        return less_dummy.next
```

</details>

**Trace it** — `head = [1,4,3,2,5,2]`, `x = 3`:

| `current` | `< 3`? | Appended to | less list | greater list |
|---|---|---|---|---|
| 1 | ✅ | less | `1` | — |
| 4 | ❌ | greater | `1` | `4` |
| 3 | ❌ (3 is not < 3) | greater | `1` | `4→3` |
| 2 | ✅ | less | `1→2` | `4→3` |
| 5 | ❌ | greater | `1→2` | `4→3→5` |
| 2 | ✅ | less | `1→2→2` | `4→3→5` |

*Terminate:* `greater_tail` is node `5`, whose original `next` was the final `2`. Setting `greater_tail.next = None` severs that stale link.

*Join:* `less_tail` (the final `2`) → `greater_dummy.next` (node `4`).

Result: **`[1,2,2,4,3,5]`** ✅

Both groups kept their input order — `1,2,2` and `4,3,5` — which is the stability requirement, achieved without any extra logic.

**What happens without the termination line:** node `5` would still point at the last `2`, which is also the tail of the less list. The output would loop back on itself and the judge would hang.

**The `x = 2` case** — `[2,1]`:

| `current` | `< 2`? | List |
|---|---|---|
| 2 | ❌ | greater: `2` |
| 1 | ✅ | less: `1` |

Terminate `2 → None`, join `1 → 2`. Return **`[1,2]`** ✅

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

A single traversal, visiting each node exactly once. Each iteration does one comparison and two pointer assignments — all O(1). The final termination and join are O(1).

Total: exactly `n` iterations, no nesting, no re-scanning.

**Compare to the alternatives:**

| | Time |
|---|---|
| Repeated splicing to a moving boundary | O(n²) |
| Collect values → partition → rewrite | O(n), but O(n) space |
| **Two lists** | **O(n)** ✅ |

Optimal — every node must be examined to be classified.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).**

Two dummy nodes and four pointers — a fixed count, independent of `n`. **No nodes are created for the data**: the original nodes are relinked, not copied.

That last point matters. A common misreading is that "building two lists" implies allocating `n` new nodes. It doesn't — you're re-threading the existing ones through different `next` pointers, which is why this is O(1) rather than O(n).

| | Space |
|---|---|
| Copy values to an array | O(n) |
| Build two lists of **new** nodes | O(n) |
| **Relink the existing nodes** | **O(1)** ✅ |

**The transferable idea:**

> **When a partition must be stable and you can't index, build the output groups separately and concatenate.** Stability comes free from append order, and with a linked list you pay nothing to do it, because relinking is O(1) per node.

The same decomposition solves [Odd Even Linked List](https://leetcode.com/problems/odd-even-linked-list/) and underlies the merge step of [merge sort](../algorithms/merge-sort.md) on lists.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Relative order must be preserved, so the in-place swap approach from Sort Colors is out — swapping breaks stability. Instead I build two lists while walking once: nodes less than `x` go on one, nodes greater than or equal go on the other. Each gets a dummy head so appending is branch-free even when a list is still empty, and because I append in encounter order, stability is automatic. At the end I **must** set the greater list's tail to `None` — those are the original nodes and its last node still carries a stale `next` that would create a cycle — then join the less tail to the greater list's first real node. O(n) time, O(1) space, since I'm relinking existing nodes rather than allocating new ones."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why terminate the greater list?" | **The key question.** The nodes are the originals; the last one's stale `next` points back into the input, creating a cycle. |
| "Do you need to terminate the *less* list too?" | No — the join overwrites `less_tail.next`. Only the final tail needs `None`. |
| "Why not partition in place with swaps?" | Swapping destroys relative order, which the problem requires. |
| "Three-way partition (`<`, `==`, `>`)?" | Three lists and three dummies, joined in order. The Dutch-flag analogue — see [Sort Colors](75-sort-colors.md). |
| "What if the input is empty?" | The loop never runs, `greater_tail` is still `greater_dummy`, and `less_dummy.next` ends up `None`. Correct for free. |
| "What if all nodes are `< x`?" | The greater list stays empty, `greater_dummy.next` is `None`, and the join terminates the list correctly. |
| "Is this stable?" | Yes — append order within each group is the input order. |

**Traps:**

- **Forgetting `greater_tail.next = None`.** *The* bug — produces a cycle and hangs the judge. Always sever the final tail.
- **Using `<=` instead of `<`.** Nodes equal to `x` must go to the **greater** group.
- **Joining to `greater_dummy` instead of `greater_dummy.next`.** Splices the sentinel into the output.
- **Returning `head`.** The head almost certainly changed.
- **Allocating new nodes.** Unnecessary and turns O(1) space into O(n) — relink the existing ones.
- **Tracking heads without dummies.** Forces an `is this list empty?` branch on every append, for both lists.

**This same move shows up in:** [Sort Colors](75-sort-colors.md) (partitioning an array, where order is free so swaps are allowed — the instructive contrast) · [Remove Linked List Elements](203-remove-linked-list-elements.md) (the dummy-node pattern) · [Merge Two Sorted Lists](21-merge-two-sorted-lists.md) (dummy-headed list building) · [Odd Even Linked List](https://leetcode.com/problems/odd-even-linked-list/) (the same two-list split and join).

</details>

---
