# SortedList (sortedcontainers)

```python
from sortedcontainers import SortedList   # pre-installed on LeetCode

sl = SortedList([5, 1, 3])                # SortedList([1, 3, 5])
sl.add(4)                                 # insert in order, O(log n)
sl.remove(3)                              # delete by value, O(log n)
sl[0], sl[-1]                             # min, max — it's indexable!
sl.bisect_left(4)                         # rank queries, like bisect
sl.irange(2, 5)                           # iterate values in [2, 5]
```

The "always-sorted list with O(log n) everything" that Python's stdlib famously lacks — the practical stand-in for a [balanced BST](balanced-bst.md) / C++ `std::multiset`. Reach for it when a problem needs **order statistics under insertions and deletions**: sliding-window median, count of smaller elements after self, my-calendar booking conflicts. Cheaper tools win when they suffice: [heap](heap.md) if you only ever need the min/max, [bisect](../syntax/bisect-module.md) on a plain list if there are no mid-stream deletions. Third-party (`pip install sortedcontainers` locally — see [virtual-environments](../guides/virtual-environments.md)), but LeetCode has it available to import.

**Complexity:** add/remove/contains O(log n) · index `sl[k]` O(log n) · min/max effectively O(1).

**Related:** [balanced-bst](balanced-bst.md) · [heap](heap.md) · [bisect-module (syntax)](../syntax/bisect-module.md)
