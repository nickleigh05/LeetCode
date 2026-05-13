# Linked List

## How to use this README

Problems are split into three tiers: Blind 75 is the core set every interviewer expects you to know cold. NeetCode 150 adds problems that sharpen the same patterns with more constraints or design requirements. NeetCode 250 introduces harder variants like partial reversal, circular buffers, and LFU caching. Work through tiers in order — the Core Patterns and Syntax Reference sections below map directly to the problems in each table, so when you hit a new problem, find the matching pattern first, then check the syntax.

---

## Problems

### Blind 75
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved |
|-----------|------------|--------------|---------------|--------|
| 206 | Easy | Reverse Linked List | [Link](https://leetcode.com/problems/reverse-linked-list/) | ☐ |
| 21 | Easy | Merge Two Sorted Lists | [Link](https://leetcode.com/problems/merge-two-sorted-lists/) | ☐ |
| 141 | Easy | Linked List Cycle | [Link](https://leetcode.com/problems/linked-list-cycle/) | ☐ |
| 143 | Medium | Reorder List | [Link](https://leetcode.com/problems/reorder-list/) | ☐ |
| 19 | Medium | Remove Nth Node From End of List | [Link](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) | ☐ |
| 23 | Hard | Merge K Sorted Lists | [Link](https://leetcode.com/problems/merge-k-sorted-lists/) | ☐ |

### NeetCode 150
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved |
|-----------|------------|--------------|---------------|--------|
| 138 | Medium | Copy List With Random Pointer | [Link](https://leetcode.com/problems/copy-list-with-random-pointer/) | ☐ |
| 2 | Medium | Add Two Numbers | [Link](https://leetcode.com/problems/add-two-numbers/) | ☐ |
| 287 | Medium | Find the Duplicate Number | [Link](https://leetcode.com/problems/find-the-duplicate-number/) | ☐ |
| 146 | Medium | LRU Cache | [Link](https://leetcode.com/problems/lru-cache/) | ☐ |
| 25 | Hard | Reverse Nodes in K-Group | [Link](https://leetcode.com/problems/reverse-nodes-in-k-group/) | ☐ |

### NeetCode 250
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved | Pattern |
|-----------|------------|--------------|---------------|--------|---------|
| 92 | Medium | Reverse Linked List II | [Link](https://leetcode.com/problems/reverse-linked-list-ii/) | ☐ | Partial reversal with dummy node |
| 622 | Medium | Design Circular Queue | [Link](https://leetcode.com/problems/design-circular-queue/) | ☐ | Array-backed ring buffer |
| 460 | Hard | LFU Cache | [Link](https://leetcode.com/problems/lfu-cache/) | ☐ | Design: freq map + doubly linked list |

---

## Complexity Reference

| Operation | Singly Linked List | Doubly Linked List | Notes |
|-----------|-------------------|-------------------|-------|
| Access by index | O(n) | O(n) | Must traverse from head |
| Search by value | O(n) | O(n) | No random access |
| Insert at head | O(1) | O(1) | Adjust head pointer |
| Insert at tail | O(n) / O(1)* | O(n) / O(1)* | O(1) only with a tail pointer |
| Insert at known node | O(1) | O(1) | Pointer surgery only |
| Delete at head | O(1) | O(1) | Advance head |
| Delete at known node | O(n) | O(1) | Singly needs prev; doubly has prev built in |
| Reverse entire list | O(n) | O(n) | One pass, in-place |
| Detect cycle | O(n) | O(n) | Floyd's two-pointer |

> \* O(1) tail insert requires maintaining a dedicated `tail` pointer alongside `head`.

---

## Data Structures

### Singly Linked List

Each node stores a value and a pointer to the next node. Nodes are scattered in memory — there is no contiguous block — so you cannot jump to index k directly; you must walk from `head` through k `.next` calls. The payoff is O(1) insert and delete at any position you already hold a pointer to: you only update two pointers regardless of list length.

```
head
  |
  v
+-----+------+    +-----+------+    +-----+------+    +-----+------+
| val | next |--->| val | next |--->| val | next |--->| val | None |
+-----+------+    +-----+------+    +-----+------+    +-----+------+
   1                  2                  3                  4
```

**When it matters:** Prefer a linked list over an array when you need frequent O(1) insert/delete at arbitrary positions and can afford O(n) lookup. Stacks and queues built on linked lists avoid the O(n) shift cost of array-based versions.

### Doubly Linked List

Each node carries both a `next` and a `prev` pointer. The extra pointer costs O(n) additional memory but enables O(1) deletion of any node you have a direct reference to — you no longer need to locate the predecessor by traversal. This property is essential for the LRU Cache design (#146), where you need to unlink the least-recently-used node in O(1).

```
head                                                          tail
  |                                                             |
  v                                                             v
+------+-----+------+    +------+-----+------+    +------+-----+------+
| prev | val | next |--->| prev | val | next |--->| prev | val | next |
| None |  1  |  o---|--->|  o   |  2  |  o---|--->|  o   |  3  | None |
+------+-----+------+    +------+-----+------+    +------+-----+------+
```

**When it matters:** Any problem that requires deleting a node by reference (not by value search) in O(1). Cache designs (LRU, LFU) pair a doubly linked list with a hash map: the map gives you the node reference in O(1), the doubly linked list deletes it in O(1).

### Dummy Head Node

A sentinel node prepended to the list with a placeholder value (typically 0). It is never part of the "real" data — it just ensures that even the first real node always has a predecessor. This eliminates the need to special-case operations on the head, because every operation can be written as "insert/delete after some node."

```
dummy → real_head → node_2 → node_3 → None
  |
  always exists, never removed
```

**When it matters:** Merge problems (#21, #23), remove-nth-from-end (#19), and any reversal where the head itself might change. Without a dummy, you need `if head is None` and `if prev is None` guards everywhere.

---

## Core Patterns

### Dummy Node
**When to use:** Whenever the head of the list might change, or when insertions/deletions happen at the front of the list.  
**Complexity:** O(n) time, O(1) space  
**Problems:** #21, #23, #19, #143, #25, #92  
**Common mistake:** Forgetting to return `dummy.next` at the end — returning `dummy` itself includes the sentinel.

```python
dummy = ListNode(0)
dummy.next = head
curr = dummy
# all modifications happen after curr, so head-change is handled automatically
return dummy.next  # real head of the modified list
```

### Two-Pointer / Floyd's Cycle Detection
**When to use:** Detect a cycle, find the cycle entry point, or find the middle of a list.  
**Complexity:** O(n) time, O(1) space  
**Problems:** #141, #287, #143, #19  
**Common mistake:** Checking `fast.next.next` without first verifying `fast.next` exists — causes an AttributeError on odd-length lists.

```python
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
    if slow is fast:            # pointers meet inside cycle
        slow2 = head
        while slow2 is not slow:
            slow = slow.next    # both advance one step to find cycle entry
            slow2 = slow2.next
        return slow             # cycle entry node
```

### Reversal In-Place
**When to use:** Reverse all or part of a linked list without allocating new nodes.  
**Complexity:** O(n) time, O(1) space  
**Problems:** #206, #25, #92, #143  
**Common mistake:** Losing the rest of the list by overwriting `curr.next` before saving it.

```python
prev = None
curr = head
while curr:
    nxt = curr.next      # save before the link is overwritten
    curr.next = prev     # reverse the pointer
    prev = curr          # advance both by one
    curr = nxt
return prev              # prev is the new head when curr falls off the end
```

### Merge Sorted Lists
**When to use:** Combine two or more sorted lists into one sorted list.  
**Complexity:** O(n + m) time for two lists; O(n log k) with a heap for k lists  
**Problems:** #21, #23  
**Common mistake:** Forgetting to attach the remaining tail after one list is exhausted — the shorter list drains first, leaving the other list dangling.

```python
dummy = ListNode(0)
curr = dummy
while l1 and l2:
    if l1.val <= l2.val:
        curr.next = l1
        l1 = l1.next
    else:
        curr.next = l2
        l2 = l2.next
    curr = curr.next
curr.next = l1 or l2     # attach whichever list still has nodes
return dummy.next
```

### Find Middle (Fast/Slow)
**When to use:** Split a list in half, or find the node at position n//2.  
**Complexity:** O(n) time, O(1) space  
**Problems:** #143, #23 (as a subroutine)  
**Common mistake:** Stopping when `fast is None` instead of `fast.next is None` — off-by-one puts slow one step past the true middle on even-length lists.

```python
slow = fast = head
while fast.next and fast.next.next:
    slow = slow.next
    fast = fast.next.next
# slow is now at the end of the first half
mid = slow.next
slow.next = None   # sever the list at the midpoint
```

---

## Syntax Reference

### ListNode class

The standard node definition used in virtually every linked list problem on LeetCode.

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next   # None signals end-of-list

# build a list [1 -> 2 -> 3] manually:
head = ListNode(1, ListNode(2, ListNode(3)))
```

### Traversal

Walk the list one node at a time. The loop condition `while curr` stops naturally when `curr` becomes `None` (end of list).

```python
curr = head
while curr:
    print(curr.val)
    curr = curr.next    # advance — forgetting this causes an infinite loop
```

### Two-pointer initialization

Both pointers start at the same node. Useful for cycle detection, nth-from-end, and middle-finding.

```python
slow = fast = head       # both reference the same object, not copies
```

### nth from end (gap trick)

Maintain a gap of exactly n nodes between two pointers. When the front pointer reaches the end, the back pointer is at the target.

```python
dummy = ListNode(0, head)
left, right = dummy, head
for _ in range(n):
    right = right.next   # advance right n steps to open the gap
while right:
    left = left.next
    right = right.next
left.next = left.next.next   # left is now just before the nth-from-end node
```

### deque as O(1) queue (for BFS on lists)

Python's `collections.deque` supports O(1) append and popleft, unlike a plain list where `list.pop(0)` is O(n).

```python
from collections import deque
q = deque()
q.append(node)       # enqueue — O(1)
node = q.popleft()   # dequeue — O(1), not O(n) like list.pop(0)
```

### heapq for Merge K Sorted Lists (#23)

A min-heap lets you always pull the smallest current head across k lists in O(log k) per pop.

```python
import heapq

heap = []
for i, node in enumerate(lists):
    if node:
        heapq.heappush(heap, (node.val, i, node))   # (value, tiebreak index, node)

dummy = ListNode(0)
curr = dummy
while heap:
    val, i, node = heapq.heappop(heap)
    curr.next = node
    curr = curr.next
    if node.next:
        heapq.heappush(heap, (node.next.val, i, node.next))
```

> The tiebreak index `i` prevents Python from comparing `ListNode` objects when two values are equal (nodes are not comparable).

### OrderedDict for LRU Cache (#146)

`OrderedDict` remembers insertion order and supports O(1) `move_to_end()` — exactly what LRU needs to track recency without building a doubly linked list from scratch.

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)   # mark as most recently used
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.cap:
            self.cache.popitem(last=False)  # evict least recently used (front)
```
