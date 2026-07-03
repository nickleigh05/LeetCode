# List Methods

```python
nums = [1, 2, 3]
nums.append(4)        # [1, 2, 3, 4] — add to end, O(1) amortized
nums.pop()              # removes & returns last item, O(1)
nums.pop(0)              # removes & returns index 0, O(n) — shifts everything
nums.insert(1, 99)       # insert at index, O(n) — shifts everything after
nums.remove(2)           # removes first value equal to 2, O(n)
nums.extend([5, 6])      # append all items from another iterable
nums.reverse()            # reverses in place
```

`.append()`/`.pop()` (from the end) are O(1); anything that touches the front or middle (`.insert()`, `.pop(0)`, `.remove()`) is O(n) because the rest of the list has to shift.

**Related:** [list-basics](list-basics.md) · [sorting-key](sorting-key.md)
