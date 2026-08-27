# 06. Linked Lists
*Pointer surgery: reverse, dummy head, fast/slow.*

[← Prev](05b-sorting.md) · [🗺 Roadmap](../../roadmap.md) · [Next →](07-trees.md)

---

Linked lists trade O(1) index access for O(1) splicing anywhere you hold a pointer. Most problems are really about careful pointer manipulation — and two reusable tricks tame the edge cases: the **dummy head** (so the first node isn't special) and **fast/slow pointers** (for cycles and midpoints).

## Concept

### Linked List

```
  Singly Linked List:
  head
   ↓
  [1] → [3] → [5] → [7] → None
   ↑              ↑
  O(1) insert   O(n) to reach
  at head        any node

  Doubly Linked List:
  None ← [1] ↔ [3] ↔ [5] ↔ [7] → None
          ↑                    ↑
         head                 tail
       O(1) at both ends (with tail pointer)

  Node structure:
  ┌──────┬──────┐
  │ val  │ next │
  └──────┴──────┘
```

**What it is:** A sequence of nodes where each node holds a value and a pointer to the next node (singly) or both next and previous nodes (doubly). There is no index-based access.

**Key Properties:**
- No random access — must traverse from head → O(n)
- O(1) insert/delete at a known node (just rewire pointers)
- Finding a node first takes O(n)
- Cycle detection is a classic linked list problem

**Complexity:**

| Operation | Singly | Doubly |
|-----------|--------|--------|
| Access node | O(n) | O(n) |
| Insert at head | O(1) | O(1) |
| Insert at tail | O(n) without tail ptr | O(1) with tail ptr |
| Insert at known position | O(1) | O(1) |
| Delete at head | O(1) | O(1) |
| Delete at known node | O(1)* | O(1) |
| Search | O(n) | O(n) |
| Space | O(n) | O(n) |

*For singly, you need the previous node too.

**Use when:**
- You need O(1) insertions/deletions at the head or at a known position
- You don't need random access
- Implementing stacks/queues from scratch
- Problems explicitly about linked lists (reverse, cycle, merge)

**Python:**
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# Build: 1 -> 2 -> 3
head = ListNode(1, ListNode(2, ListNode(3)))

# Traverse
cur = head
while cur:
    print(cur.val)
    cur = cur.next

# Dummy head trick (simplifies edge cases)
dummy = ListNode(0)
dummy.next = head
```

## The Pattern

### Fast and Slow Pointers

```
  Linked list cycle detection (Floyd's algorithm):

  List: 1 → 2 → 3 → 4 → 5 → 3 (cycle back to node 3)
                        ↑_______↑

  slow moves 1 step, fast moves 2 steps:
  Start: slow=1, fast=1
  Step1: slow=2, fast=3
  Step2: slow=3, fast=5
  Step3: slow=4, fast=4   ← MEET! cycle detected

  Find middle of linked list:
  List: 1 → 2 → 3 → 4 → 5 → None

  slow=1, fast=1
  Step1: slow=2, fast=3
  Step2: slow=3, fast=5
  fast.next = None → STOP → slow=3 is the MIDDLE

  For even length: 1 → 2 → 3 → 4 → None
  Step1: slow=2, fast=3
  Step2: slow=3, fast=None → STOP → slow=3 (second middle)
```

**What it is:** Two pointers moving at different speeds through a linked list (or array). The key insight: if there is a cycle, the fast pointer must eventually lap the slow pointer and they will meet.

**Use this when:**
- [ ] Detect a cycle in a linked list
- [ ] Find the start of a cycle
- [ ] Find the middle node of a linked list
- [ ] Check if a linked list is a palindrome (find middle, reverse second half)
- [ ] Happy number (detect cycle in sequence of digit-square-sums)

**Python:**
```python
# Cycle detection
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False

# Find start of cycle (after detecting meeting point)
def cycle_start(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            break
    else:
        return None   # no cycle
    # reset slow to head; both move 1 step at a time
    slow = head
    while slow is not fast:
        slow = slow.next
        fast = fast.next
    return slow   # start of cycle

# Find middle node
def find_middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow   # middle (or second middle for even length)

# Happy number (cycle detection on numbers)
def is_happy(n):
    def digit_square_sum(n):
        return sum(int(d)**2 for d in str(n))
    slow = fast = n
    while True:
        slow = digit_square_sum(slow)
        fast = digit_square_sum(digit_square_sum(fast))
        if slow == fast:
            return slow == 1
```

**Complexity:** O(n) time, O(1) space (no extra data structures).

**Blind 75 examples:** Linked List Cycle · (Reorder List uses find middle)

## The Template

The reusable code skeleton for this pattern lives in [`appendix/templates/linked-list/`](../appendix/templates/linked-list/). Read the README (when to reach for it, variations, common bugs), then type out [`template.py`](../appendix/templates/linked-list/template.py) from memory before you drill problems.

## Practice

Work the guided set with hints & solutions: [**Linked Lists — Practice →**](../rmap-practice/06-linked-list.md). Easy → hard, top to bottom; when the pattern feels automatic, move on — don’t grind it forever. Want more volume? See the [recommended list](../../lists/recommended.md#6-linked-list-20-problems).

## Check Yourself

- [ ] I can reverse a linked list iteratively from memory, tracking prev/curr/next.
- [ ] I can explain the dummy-head trick and when it removes edge cases.
- [ ] I can use fast/slow pointers to find the middle and detect a cycle.
- [ ] I solved a 🔴 Hard linked-list problem (e.g. Merge k Sorted Lists or Reverse Nodes in k-Group).

---

**Up next:** [Trees & Binary Search Trees](07-trees.md) — dFS = base → recurse → combine. BFS = level by level.

[← Prev](05b-sorting.md) · [🗺 Roadmap](../../roadmap.md) · [Next →](07-trees.md)

