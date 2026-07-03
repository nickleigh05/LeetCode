# Shallow Copy vs. Deep Copy

```python
import copy

original = [[1, 2], [3, 4]]
shallow = original[:]                 # or list(original), or copy.copy(original)
shallow[0].append(99)                  # mutates original[0] too! same inner list object

deep = copy.deepcopy(original)          # fully independent, recursively copied
deep[0].append(99)                       # original is untouched
```

A shallow copy duplicates the outer container but still points to the *same* nested objects inside — mutating a nested list through the copy mutates it through the original too. `copy.deepcopy()` recursively copies everything, giving full independence, at the cost of more time/memory.

**Related:** [nested-lists](nested-lists.md) · [list-slicing](list-slicing.md)
