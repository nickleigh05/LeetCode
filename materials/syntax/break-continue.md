# `break` / `continue`

```python
for num in nums:
    if num < 0:
        continue      # skip the rest of this iteration, go to next
    if num == 0:
        break          # exit the loop entirely
    print(num)
```

`continue` jumps to the next iteration immediately. `break` exits the nearest enclosing loop immediately, skipping any remaining iterations. Both work in `for` and `while` loops.

**Related:** [for-loop](for-loop.md) · [while-loop](while-loop.md) · [pass-statement](pass-statement.md)
