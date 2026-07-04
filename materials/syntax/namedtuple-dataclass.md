# namedtuple & dataclass

```python
from collections import namedtuple
Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
p.x, p.y            # 3, 4 — readable field access
x, y = p            # still unpacks like a tuple, still hashable, still comparable

from dataclasses import dataclass
@dataclass
class Node:
    val: int
    left: "Node | None" = None
    right: "Node | None" = None       # __init__ and __repr__ written for you

n = Node(5)         # Node(val=5, left=None, right=None) — free nice printing
```

Both remove boilerplate for "a small bundle of fields." `namedtuple` = a real [tuple](tuple-basics.md) with names: immutable, hashable (usable in [sets](set-basics.md)/as dict keys), zero weight — nice for coordinates or states. `@dataclass` = a real [class](class-basics.md) with `__init__`/`__repr__`/`__eq__` auto-generated: mutable, extensible — nice for local `ListNode`/`TreeNode` definitions when [testing locally](../guides/testing-locally.md). LeetCode never *requires* either, but they make helper code shorter and debug output readable.

**Related:** [tuple-basics](tuple-basics.md) · [class-basics](class-basics.md) · [init-method](init-method.md) · [type-hints](type-hints.md)
