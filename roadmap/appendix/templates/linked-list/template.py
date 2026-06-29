"""
Linked List — Reversal, Dummy Head, and Fast/Slow Skeletons

Linked lists have no indices, so every technique comes down to carefully
reshuffling `.next` pointers without losing the rest of the list. Three
skeletons cover the overwhelming majority of problems:

  1. REVERSE in place      — the prev / current / next_node three-pointer dance.
  2. DUMMY HEAD            — a sentinel before head so the real head is never a
                             special case when inserting or deleting.
  3. FAST / SLOW pointers  — two speeds to find the middle, detect a cycle, or
                             locate the k-th node from the end.

Golden rule: before you overwrite a `.next`, save whatever it pointed to — or
you will lose the entire tail of the list.
"""

from typing import Optional


class ListNode:
    """Singly linked list node (matches the LeetCode definition)."""

    def __init__(self, val: int = 0, next: Optional["ListNode"] = None) -> None:
        self.val = val
        self.next = next


def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """Reverse a singly linked list in place.

    Time:      O(n)
    Space:     O(1)
    Invariant: `previous_node` heads the already-reversed prefix and
               `current_node` heads the untouched suffix. Each step moves one
               node from the front of the suffix to the front of the prefix.
    """

    previous_node: Optional[ListNode] = None
    current_node = head

    while current_node is not None:
        # Save the next link BEFORE clobbering it, or the rest is unreachable.
        next_node = current_node.next

        # Flip this node's pointer back toward the prefix.
        current_node.next = previous_node

        # Slide both pointers one step along the original list.
        previous_node = current_node
        current_node = next_node

    # current_node is now None, so previous_node is the new head.
    return previous_node


def dummy_head_filter(head: Optional[ListNode]) -> Optional[ListNode]:
    """Build or filter a list behind a sentinel so the head needs no special case.

    Time:      O(n)
    Space:     O(1)
    Invariant: `tail` always points at the last node of the result-so-far; the
               dummy guarantees `tail` is never None, even before the first
               keeper is appended.
    """

    dummy = ListNode(0)  # sentinel; dummy.next will be the real result head
    tail = dummy
    current_node = head

    while current_node is not None:
        # TODO: problem-specific test for keeping / skipping / rewiring a node.
        keep_current = True

        if keep_current:
            tail.next = current_node
            tail = current_node

        current_node = current_node.next

    # Terminate the result so any skipped trailing nodes are cut loose.
    tail.next = None
    return dummy.next


def fast_slow_midpoint(head: Optional[ListNode]) -> Optional[ListNode]:
    """Find the middle node with two pointers moving at different speeds.

    Time:      O(n)
    Space:     O(1)
    Invariant: `fast` advances twice for every step of `slow`, so when `fast`
               falls off the end, `slow` has covered exactly half the distance.
               For even length this returns the second of the two middle nodes.
    """

    slow = head
    fast = head

    # Guard BOTH `fast` and `fast.next` so the double hop never dereferences
    # None. This is the most copy-pasted condition in all of linked lists.
    while fast is not None and fast.next is not None:
        slow = slow.next       # one step
        fast = fast.next.next  # two steps

    return slow
