# Floyd's Cycle Detection (Tortoise & Hare)

```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next               # 1 step
        fast = fast.next.next          # 2 steps
        if slow is fast:               # met inside the loop → cycle
            return True
    return False                       # fast fell off the end → no cycle

# phase 2 — find where the cycle STARTS (LC 142):
# reset slow to head; walk both 1 step at a time; they meet at the entrance.
```

Two pointers race through the list: if there's a cycle, the fast one enters the loop and gains one position per step on the slow one — on a circular track, it must lap it, so they meet. No cycle, and `fast` simply hits None. This replaces the obvious [visited-set](../data-structures/hashset.md) answer's O(n) memory with **O(1)**. The phase-2 reset trick (head-to-meeting distance math) finds the cycle's entry node, which is also the sneaky intended solution to Find the Duplicate Number (LC 287) — treat `i → nums[i]` as a linked list. The same slow/fast pair with no cycle involved finds a list's **middle** (slow is halfway when fast finishes) — see [lesson 06](../learning/06-linked-list.md).

**Complexity:** O(n) time · O(1) space.

**Related:** [linked-list (data-structures)](../data-structures/linked-list.md) · [Linked List lesson](../learning/06-linked-list.md) · [Two Pointers lesson](../learning/02-two-pointers.md)
