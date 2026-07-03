# Doubly Linked List

```python
class DListNode:
    def __init__(self, val=0):
        self.val = val
        self.prev = None
        self.next = None
```

Same idea as a [singly linked list](linked-list.md), but each node also points *back* to its predecessor — letting you traverse or delete in either direction without needing a reference to the previous node ahead of time. The extra `prev` pointer costs memory but is what makes O(1) removal-by-node-reference and structures like LRU Cache practical.

**Complexity:** insert/delete at a known node O(1) (both directions) · access by index O(n).

**Related:** [linked-list](linked-list.md) · [class-basics (syntax)](../syntax/class-basics.md)
