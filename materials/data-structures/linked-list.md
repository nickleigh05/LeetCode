# Linked List

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

head = ListNode(1, ListNode(2, ListNode(3)))   # 1 -> 2 -> 3
```

A chain of nodes where each node holds a value and a pointer to the next node — no contiguous memory required, unlike an [array](array.md). Inserting/deleting at a known node is O(1) (just rewire pointers), but there's no random access: reaching the k-th node means walking k pointers from the head, O(k).

**Complexity:** access by index O(n) · insert/delete at a known node O(1) · search O(n).

**Related:** [init-method (syntax)](../syntax/init-method.md) · [array](array.md) · [stack](stack.md)
