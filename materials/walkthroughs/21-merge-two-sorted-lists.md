# 21. Merge Two Sorted Lists

**Easy** · [LeetCode](https://leetcode.com/problems/merge-two-sorted-lists/) · [Solution file (no hints)](../../problems/0001-0499/21.py)

[📖 06. Linked List lesson](../learning/06-linked-list.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 06. Linked List problems](../rmap-practice/06-linked-list.md)

---

You're given the heads of two sorted linked lists. Merge them into **one sorted list**, spliced together from the nodes of the original two lists. Return the head of the merged list.

```
list1 = [1,2,4], list2 = [1,3,4]  →  [1,1,2,3,4,4]
list1 = [],      list2 = []       →  []
list1 = [],      list2 = [0]      →  [0]
```

**Constraints:** `0 <= nodes in each list <= 50` · `-100 <= Node.val <= 100` · both lists sorted **non-decreasing**

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| both lists **sorted** | ⚠️ The smaller of the two heads is *always* the next node overall. You never search — you just compare two candidates |
| "**spliced** from the nodes of the original lists" | Relink existing nodes; don't allocate new ones. O(1) space |
| "non-decreasing" | Duplicates are allowed — `[1,2,4]` and `[1,3,4]` both start with 1 |
| either list can be **empty** | Both-empty, one-empty, and unequal-length cases must all work |
| ≤ 50 nodes | Tiny. This is about clean pointer handling, not performance |

The algorithm is almost obvious: repeatedly take whichever list's head is smaller and append it to the result. Because both are sorted, that greedy choice is always correct — nothing smaller can appear later in either list.

**The awkward part isn't the logic, it's the bookkeeping.** To append a node you write `tail.next = node`. But at the very start there *is* no tail — the result is empty. So you'd need something like:

```python
if result_head is None:
    result_head = node
    tail = node
else:
    tail.next = node
    tail = tail.next
```

That branch runs once and clutters every iteration. And you must separately remember the head to return it, since `tail` has walked away from it.

🤔 **Before you open the next section:** what if the result list started with one throwaway node that nobody looks at? What would that do to the special case?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Collect values, sort, rebuild | Extract, `sort()`, make new nodes | O((n+m) log(n+m)) | O(n+m) | ❌ Throws away the sortedness and allocates |
| Recursion | Pick the smaller head, recurse on the rest | O(n+m) | **O(n+m)** stack | ⚠️ Very elegant; mention it |
| Iterative, track head separately | Special-case the first node | O(n+m) | O(1) | ⚠️ Correct but branchy |
| **Iterative with a dummy head** | A throwaway node removes the special case | **O(n+m)** | **O(1)** | ✅ |

**The decision: iterative merge with a [dummy head](../data-structures/linked-list.md) node.**

The dummy is a real node that holds no meaningful value and exists purely so that **`current.next` is always a valid place to attach something** — even before the result has a first real node.

```
dummy → [1] → [1] → [2] → ...
  ↑      ↑
throw   the actual answer: return dummy.next
away
```

Two problems solved by one node:

1. **No first-node special case.** Every append is just `current.next = node`, uniformly.
2. **The head is never lost.** `current` walks forward, but `dummy` stays put — and `dummy.next` is the real head, available at the end.

**This is the single most useful linked-list idiom**, and it recurs constantly: any time you're *building* a list, or might *remove the first node*, a dummy head eliminates the edge case. You'll see it again in [Remove Nth Node](19-remove-nth-node-from-end-of-list.md), [Add Two Numbers](2-add-two-numbers.md), and [Reverse Nodes in k-Group](25-reverse-nodes-in-k-group.md).

**The leftover-tail shortcut.** When one list runs out, the other is *already a sorted linked list* — so you attach the whole remainder with a single pointer assignment rather than looping through it. That's a genuine advantage of linked lists over arrays: appending a whole tail is O(1).

**Why not recursion?** It's beautiful — three lines — but O(n+m) stack. Worth naming as an alternative.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
dummy = ListNode(0)
current = dummy
```

The dummy node. Its value `0` is never read — only its `next` matters. `current` is the **tail** of the result being built, starting at the dummy so the first append has somewhere to go.
→ [class-basics](../syntax/class-basics.md) · [linked-list](../data-structures/linked-list.md)

```python
while list1 is not None and list2 is not None:
```

Run only while **both** lists still have nodes — once either is exhausted, the comparison is meaningless and the remainder is handled after the loop.

`is not None` is the explicit identity check. `while list1 and list2` also works, but `is None` is the conventional style for node pointers because it can't be confused with a falsy *value*.
→ [while-loop](../syntax/while-loop.md) · [identity-operators](../syntax/identity-operators.md) · [logical-operators](../syntax/logical-operators.md)

```python
    if list1.val <= list2.val:
        current.next = list1
        list1 = list1.next
```

**The greedy choice.** `list1`'s head is smaller (or equal), so it's the next node of the merged list — nothing smaller can exist in either list, since both are sorted.

Attach it, then advance `list1` past the node just consumed.

**`<=` rather than `<`** makes the merge **stable** — equal values keep `list1`'s node first, preserving relative order. It doesn't change correctness here, but stability matters when nodes carry more than a value, and mentioning it shows care.
→ [comparison-operators](../syntax/comparison-operators.md)

```python
    else:
        current.next = list2
        list2 = list2.next
```

Mirror image for `list2`.
→ [elif-else](../syntax/elif-else.md)

```python
    current = current.next
```

Advance the tail onto the node just attached, so the next append lands in the right place. Runs on both branches.

```python
if list1 is not None:
    current.next = list1
else:
    current.next = list2
```

**The leftover tail, in one assignment.** The loop ended because one list emptied — whatever remains in the other is already sorted and correctly linked, so attaching its head attaches *all of it*.

No loop needed. And if both are empty, `current.next` becomes `None`, terminating the list correctly.

*(This is equivalent to the one-liner `current.next = list1 if list1 else list2`.)*
→ [none-type](../syntax/none-type.md)

```python
return dummy.next
```

**`dummy.next`, never `dummy`.** The dummy is scaffolding — the real head is the node after it. Returning `dummy` prepends a spurious `0` to the answer.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:

        dummy = ListNode(0)
        current = dummy

        while list1 is not None and list2 is not None:
            if list1.val <= list2.val:
                current.next = list1
                list1 = list1.next
            else:
                current.next = list2
                list2 = list2.next
            current = current.next

        if list1 is not None:
            current.next = list1
        else:
            current.next = list2

        return dummy.next
```

</details>

**Trace it** — `list1 = [1,2,4]`, `list2 = [1,3,4]`:

| Step | `list1` head | `list2` head | Take | Result so far |
|---|---|---|---|---|
| 1 | 1 | 1 | `list1` (1 ≤ 1) | `dummy → 1` |
| 2 | 2 | 1 | `list2` | `dummy → 1 → 1` |
| 3 | 2 | 3 | `list1` | `… → 2` |
| 4 | 4 | 3 | `list2` | `… → 3` |
| 5 | 4 | 4 | `list1` (4 ≤ 4) | `… → 4` |
| exit | — | 4 | `list1` empty | attach `list2`'s remaining `[4]` |

Result: `dummy → 1 → 1 → 2 → 3 → 4 → 4`, and we return `dummy.next` = the first `1`. ✅

Note step 5 → exit: after taking `list1`'s 4, `list1` is `None`, so the loop stops and the single remaining node is attached with one assignment.

**The recursive version:**

```python
def mergeTwoLists(self, l1, l2):
    if not l1: return l2
    if not l2: return l1
    if l1.val <= l2.val:
        l1.next = self.mergeTwoLists(l1.next, l2)
        return l1
    l2.next = self.mergeTwoLists(l1, l2.next)
    return l2
```
→ [recursion-basics](../syntax/recursion-basics.md)

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n + m)</summary>

**O(n + m)**, where n and m are the two list lengths.

Each loop iteration consumes exactly one node from one list and does O(1) work — one comparison, two pointer assignments. Since a node is consumed every iteration and never revisited, the loop runs at most n + m times.

The leftover attachment is **O(1)** — a single pointer assignment splices in an arbitrarily long remainder. That's a linked-list superpower an array can't match; concatenating arrays requires copying.

**O(n + m)** total, which is optimal: any merge must at least look at every node.

**Versus collect-and-sort:** O((n+m) log(n+m)) — you'd be paying to re-derive an ordering the input already gave you. The same mistake as sorting in [Valid Anagram](242-valid-anagram.md) when counts suffice.

**This routine is a building block.** [Merge k Sorted Lists](23-merge-k-sorted-lists.md) calls it repeatedly (or uses a heap to generalize it), and it's the merge step of [merge sort](../algorithms/merge-sort.md).

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).**

Two pointer variables plus one dummy node — a constant, independent of input size. **No new nodes are allocated for the result**; the existing nodes are relinked, which is exactly what "spliced together from the nodes of the original lists" asks for.

| Approach | Space | Why |
|---|---|---|
| **Iterative + dummy** | **O(1)** | Relinks in place |
| Recursive | O(n+m) | One stack frame per node |
| Collect, sort, rebuild | O(n+m) | New array *and* new nodes |

**The single dummy node is O(1)** — one allocation regardless of list length. A cheap price for deleting an entire branch from the loop.

**Note the inputs are destroyed.** After merging, `list1` and `list2` no longer describe their original lists — their nodes now belong to the merged one. That's expected here ("spliced"), but always worth confirming with an interviewer, since it's a real API decision: merging *destructively* is O(1) space, merging *non-destructively* requires copying every node and costs O(n+m).

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Both lists are sorted, so the smaller of the two heads is always the next node of the merged list — no searching, just one comparison per step. The bookkeeping annoyance is the first node: before the result has a head, there's no tail to append to. I solve that with a dummy head — a throwaway node so `current.next` is always a valid attachment point, and `dummy.next` still holds the real head at the end. When one list empties, the other is already a sorted list, so I splice the whole remainder in with a single assignment. O(n+m) time, O(1) space, relinking existing nodes rather than allocating."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why a dummy node?" | **The question.** It removes the empty-result special case and preserves the head while `current` walks away. The single most useful linked-list idiom. |
| "Merge **k** sorted lists." | Either merge pairwise (O(nk)) or use a min-heap of the k current heads (O(n log k)). See [Merge k Sorted Lists](23-merge-k-sorted-lists.md). |
| "Recursive version?" | Return the smaller head with its `next` set to the merge of the rest. Three lines, O(n+m) stack. |
| "Merge without modifying the inputs?" | Allocate a new node per element — O(n+m) space. A real trade worth naming. |
| "Descending order?" | Flip the comparison to `>=`. |
| "Why `<=` and not `<`?" | Stability — equal values keep `list1`'s node first. Irrelevant for bare integers, important when nodes carry payloads. |
| "Merge two sorted **arrays** instead?" | Same two-pointer logic, but appending a leftover tail costs O(n) copying instead of O(1) relinking. |

**Traps:**

- **Returning `dummy` instead of `dummy.next`** — prepends a phantom node. The classic dummy-head bug.
- **Forgetting the leftover tail.** The loop stops as soon as *either* list empties; without the final attach you silently truncate the answer.
- **Advancing `current` inside only one branch.** The tail falls behind and nodes get overwritten.
- **Looping through the remainder** node by node. Correct but pointless — one assignment does it.
- **`while list1 or list2`** instead of `and` — you'd dereference `.val` on `None`.
- **Building new nodes** when the problem says splice.

**This same move shows up in:** [Merge k Sorted Lists](23-merge-k-sorted-lists.md) (this routine generalized) · [Add Two Numbers](2-add-two-numbers.md) (dummy head while building a result list) · [Remove Nth Node From End](19-remove-nth-node-from-end-of-list.md) (dummy head to handle removing the first node) · [merge-sort](../algorithms/merge-sort.md) (this is its merge step).

</details>

---
