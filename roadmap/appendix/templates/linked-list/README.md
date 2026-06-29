# Linked List

*Pointer arithmetic and in-place surgery. Draw it out — every single time. The bugs all come from overwriting a `.next` before you saved it.*

## Recognize this pattern when...

- The input is a **singly (or doubly) linked list** and you must rewire it, not just read values.
- The problem says **"in O(1) space"** or **"without modifying the values"** — that rules out copying to an array.
- You need the **middle**, the **k-th node from the end**, or to **detect / locate a cycle**.
- You're **merging, reordering, or reversing** part of a list.
- Insertions or deletions can happen **at the head**, making a sentinel worthwhile.

## Variations

1. **Iterative reversal** — prev / current / next_node; the backbone of half of all list problems. *(Reverse Linked List)*
2. **Dummy head build/merge** — sentinel + `tail` pointer so the head is never special. *(Merge Two Sorted Lists)*
3. **Fast/slow midpoint** — two speeds to land `slow` on the middle. *(Middle of the Linked List)*
4. **Floyd cycle detection** — fast/slow meet inside a cycle; reset one to head to find the entry. *(Linked List Cycle II)*
5. **Reverse a sublist / k-group** — reversal bounded by saved boundary nodes, stitched back in. *(Reverse Nodes in k-Group)*

## Representative problems

| # | Difficulty | Problem |
|---|------------|---------|
| 206 | Easy | [Reverse Linked List](../../../../problems/0001-0499/206.py) |
| 21 | Easy | [Merge Two Sorted Lists](../../../../problems/0001-0499/21.py) |
| 141 | Easy | [Linked List Cycle](../../../../problems/0001-0499/141.py) |
| 19 | Medium | Remove Nth Node From End of List |
| 143 | Medium | Reorder List |
| 25 | Hard | Reverse Nodes in k-Group |

## Common bugs & traps

- **Losing the tail.** Always `next_node = current.next` *before* reassigning `current.next`.
- **Null dereference in fast/slow.** The loop guard must be `fast and fast.next` — checking only `fast` crashes on the double hop.
- **Off-by-one for "nth from end".** Advance the lead pointer `n + 1` steps (from a dummy) so the trailing pointer stops *before* the target to delete it.
- **Returning the sentinel.** Return `dummy.next`, never `dummy`.
- **Forgetting `tail.next = None`.** A filtered/built list can keep pointing into skipped nodes and accidentally form a cycle.
- **First vs second middle.** Initializing `fast = head` lands on the second middle for even length; `fast = head.next` lands on the first. Pick deliberately.
---

*See also: [patterns.md](../../patterns.md) · [datastructures.md](../../../ds&a/datastructures.md) · [algorithms.md](../../../ds&a/algorithms.md) · [lists/](../../../../lists/)*
