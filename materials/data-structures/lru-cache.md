# LRU Cache

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.od = OrderedDict()               # key → value, oldest first

    def get(self, key):
        if key not in self.od:
            return -1
        self.od.move_to_end(key)              # mark as most recently used
        return self.od[key]

    def put(self, key, value):
        if key in self.od:
            self.od.move_to_end(key)
        self.od[key] = value
        if len(self.od) > self.cap:
            self.od.popitem(last=False)       # evict the least-recently-used
```

A fixed-capacity key→value store that evicts the **l**east-**r**ecently-**u**sed entry when full — the classic "design a data structure" interview question (LC 146). The requirement is O(1) `get` *and* `put`, which forces the two-structure combo: a [hash map](hashmap.md) for instant lookup **+** a [doubly linked list](doubly-linked-list.md) for instant reordering/eviction (the map's values point at list nodes). `OrderedDict` bundles exactly that pair, so know both: the hand-rolled version proves you understand it; the OrderedDict version ships it in 15 lines.

**Complexity:** get/put O(1) · space O(capacity).

**Related:** [hashmap](hashmap.md) · [doubly-linked-list](doubly-linked-list.md) · [ordered-dict-notes (syntax)](../syntax/ordered-dict-notes.md)
