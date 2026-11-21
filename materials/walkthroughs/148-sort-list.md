# 148. Sort List

**Medium** · [LeetCode](https://leetcode.com/problems/sort-list/) · [Solution file (no hints)](../../problems/0001-0499/148.py)

[📖 06. Linked List lesson](../learning/06-linked-list.md) · [📖 Sorting](../learning/05b-sorting.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 06. Linked List problems](../rmap-practice/06-linked-list.md)

---

Given the `head` of a linked list, return the list **sorted in ascending order**.

```
4 → 2 → 1 → 3          →   1 → 2 → 3 → 4
-1 → 5 → 3 → 4 → 0     →   -1 → 0 → 3 → 4 → 5
(empty)                →   (empty)
```

**Constraints:** `0 <= nodes <= 5·10⁴` · `-10⁵ <= Node.val <= 10⁵`

**Follow-up:** can you sort it in **O(n log n) time** and **O(1) memory**?

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| sort a **linked list** | No random access. You can't jump to index `i` in O(1) |
| up to 5·10⁴ nodes | O(n²) sorts (insertion, bubble) are about 2.5·10⁹ steps. You need O(n log n) |
| follow-up O(1) memory | You can't copy values into an array. Even recursion's O(log n) stack doesn't count as O(1) |

**Which O(n log n) sort fits a linked list?**

- **Quicksort** depends on partitioning around a pivot, which a list can do, but its worst case is O(n²) and choosing a good pivot needs random access.
- **Heapsort** needs an array to index into.
- **Merge sort** only ever touches data **sequentially**: split, sort each half, merge two sorted runs. Lists are good at exactly that. Merging two sorted lists is [Merge Two Sorted Lists](21-merge-two-sorted-lists.md), and it's O(1) extra space for lists because you relink nodes instead of copying into a buffer.

So merge sort is the natural choice. Arrays need an O(n) buffer to merge, but lists don't.

**Finding the middle to split.** Use slow and fast pointers. `fast` moves two steps for every one step of `slow`, so when `fast` reaches the end, `slow` is in the middle. Then cut the list after `slow`.

🤔 **Before you open the next section:** with a two-node list `1 → 2`, where must `slow` stop so that cutting after it gives two non-empty halves, rather than one half that's the whole list?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Copy to array, sort, rebuild | `vals.sort()`, write values back | O(n log n) | O(n) | ⚠️ Works, sidesteps the problem |
| Insertion sort on the list | Insert each node into a sorted prefix | O(n²) | O(1) | ❌ Too slow |
| **Top-down merge sort** | Split at the middle, sort halves, merge | **O(n log n)** | O(log n) stack | ✅ The expected answer |
| Bottom-up merge sort | Merge runs of size 1, 2, 4, … iteratively | O(n log n) | **O(1)** | ✅ Answers the strict follow-up |

**The decision: top-down [merge sort](../algorithms/merge-sort.md)** on the [linked list](../data-structures/linked-list.md).

It's the clearest O(n log n) solution, and it reuses two skills you already have: finding the middle ([Middle of the Linked List](876-middle-of-the-linked-list.md)) and merging ([Merge Two Sorted Lists](21-merge-two-sorted-lists.md)).

**On the follow-up.** Top-down recursion uses O(log n) stack, which interviewers usually accept. For *strict* O(1), use bottom-up merge sort: no recursion, just repeated passes that merge adjacent runs of length 1, then 2, then 4, and so on. It's the same merge step with more bookkeeping. Mention it, and write it only if pushed.

**Why `fast` starts at `head.next`.** With two nodes, starting `fast = head` would move `slow` to the second node, so cutting after it would leave the first "half" as the whole list, and the recursion would never get smaller. Starting `fast` one ahead makes `slow` stop at the **first** middle, so both halves are always strictly smaller.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
if head is None or head.next is None:
    return head
```

**The base case.** An empty or single-node list is already sorted. This is what stops the recursion.
→ [none-type](../syntax/none-type.md) · [logical-operators](../syntax/logical-operators.md) · [if-return](../syntax/if-return.md)

```python
slow = head
fast = head.next
while fast is not None and fast.next is not None:
    slow = slow.next
    fast = fast.next.next
```

**Find the middle.** `fast` covers ground twice as quickly, so when it runs out, `slow` is at the end of the first half. Starting `fast` one node ahead puts `slow` on the **left** middle for even lengths, which guarantees both halves are non-empty.
→ [while-loop](../syntax/while-loop.md)

```python
second = slow.next
slow.next = None
```

**Cut the list in two.** Save where the second half starts, then end the first half. Without `slow.next = None`, the "first half" would still run on through the whole list.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
left = self.sortList(head)
right = self.sortList(second)
```

**Sort each half recursively.** Trust that each call returns a sorted list. Each is about half the size, so the recursion is O(log n) deep.
→ [recursion-basics](../syntax/recursion-basics.md)

```python
dummy = ListNode()
tail = dummy
while left is not None and right is not None:
    if left.val <= right.val:
        tail.next = left
        left = left.next
    else:
        tail.next = right
        right = right.next
    tail = tail.next
```

**Merge the two sorted halves.** A dummy head avoids special-casing the first node. Each step attaches the smaller front node to `tail` and moves on. `<=` (rather than `<`) takes from the left first on ties, which makes the sort **stable**.
→ [class-basics](../syntax/class-basics.md) · [elif-else](../syntax/elif-else.md)

```python
tail.next = left if left is not None else right
return dummy.next
```

One half has run out. The other is already sorted, so attach the rest of it in one step. The merged list starts at `dummy.next`.
→ [ternary-expression](../syntax/ternary-expression.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head

        slow = head
        fast = head.next
        while fast is not None and fast.next is not None:
            slow = slow.next
            fast = fast.next.next

        second = slow.next
        slow.next = None

        left = self.sortList(head)
        right = self.sortList(second)

        dummy = ListNode()
        tail = dummy
        while left is not None and right is not None:
            if left.val <= right.val:
                tail.next = left
                left = left.next
            else:
                tail.next = right
                right = right.next
            tail = tail.next

        tail.next = left if left is not None else right
        return dummy.next
```

</details>

**Trace it.** `4 → 2 → 1 → 3`:

```
split:        4 → 2 → 1 → 3
             /             \
          4 → 2           1 → 3
          /   \           /   \
         4     2         1     3        ← single nodes: base case
          \   /           \   /
          2 → 4           1 → 3         ← merge pairs
             \             /
          1 → 2 → 3 → 4                 ← final merge
```

The final merge of `2 → 4` and `1 → 3`:

| Compare | Take | Result so far |
|---|---|---|
| 2 vs 1 | 1 | 1 |
| 2 vs 3 | 2 | 1 → 2 |
| 4 vs 3 | 3 | 1 → 2 → 3 |
| right empty | attach 4 | 1 → 2 → 3 → 4 ✅ |

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n log n)</summary>

**O(n log n).**

- The list is halved at each level, so there are **log n levels** of recursion.
- At each level, the middle-finding and merging together touch every node a constant number of times, so **O(n per level**).

log n levels × O(n) work = O(n log n). That's guaranteed, with no bad worst case, unlike quicksort.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(log n)</summary>

**O(log n)** for the recursion stack. Nodes are relinked, not copied, so merging needs no buffer. That's the advantage over array merge sort, which needs O(n) to merge.

**For strict O(1):** bottom-up merge sort. Count the length, then for `size = 1, 2, 4, …` walk the list, cut off two runs of length `size`, merge them, and attach the result. No recursion, so O(1) extra space.

| | Time | Extra space |
|---|---|---|
| Copy to array + sort | O(n log n) | O(n) |
| **Top-down merge sort** | O(n log n) | O(log n) |
| Bottom-up merge sort | O(n log n) | O(1) |

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Merge sort fits linked lists because it only needs sequential access, and merging two lists is O(1) extra space since I relink nodes. I find the middle with slow and fast pointers, starting fast one ahead so a two-node list splits into one and one. I cut the list there, sort each half recursively, and merge with a dummy head, using `<=` to keep it stable. O(n log n) time, O(log n) stack. If they need strict O(1), I'd do bottom-up merge sort, merging runs of size 1, 2, 4, and so on."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Strict O(1) space?" | Bottom-up merge sort, iterative, doubling the run size each pass. |
| "Why not quicksort?" | Worst case O(n²), and good pivot choice needs random access. Merge sort is O(n log n) guaranteed and suits sequential access. |
| "Why does `fast` start at `head.next`?" | So `slow` stops on the left middle. Otherwise a two-node list never splits and the recursion never ends. |
| "Is it stable?" | Yes, if the merge takes from the left on ties (`<=`). |
| "Merge k sorted lists?" | [Merge k Sorted Lists](23-merge-k-sorted-lists.md). Use a heap, or merge pairs repeatedly, which is this merge step again. |

**Traps:**

- **Forgetting `slow.next = None`.** The halves aren't separated, and the recursion runs forever.
- **`fast = head` with this loop.** A two-node list splits into "both nodes" and "nothing," which is infinite recursion.
- **Copying into an array.** It works, but it's what the problem is asking you not to do.
- **Insertion sort.** Correct, but O(n²) at 5·10⁴ nodes.
- **Losing the merged head.** Return `dummy.next`, not `tail`.

**This same move shows up in:** [Merge Two Sorted Lists](21-merge-two-sorted-lists.md) (the merge step on its own) · [Middle of the Linked List](876-middle-of-the-linked-list.md) (the slow/fast split) · [Merge k Sorted Lists](23-merge-k-sorted-lists.md) (merging generalised to many lists) · [Count of Smaller Numbers After Self](315-count-of-smaller-numbers-after-self.md) (merge sort doing extra work during the merge).

</details>

---
