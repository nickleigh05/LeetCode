# `__init__`

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

node = ListNode(5)      # val=5, next=None (using the default)
```

`__init__` is the constructor — Python calls it automatically right after creating a new instance, to set up its starting attributes. It never explicitly `return`s anything (returning a value from `__init__` is an error).

**Related:** [class-basics](class-basics.md) · [default-arguments](default-arguments.md)
