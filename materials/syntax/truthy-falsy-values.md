# Truthy / Falsy Values

```python
if []: ...        # False — empty list is falsy
if {}: ...          # False — empty dict is falsy
if "": ...            # False — empty string is falsy
if 0: ...              # False
if None: ...             # False

if [1, 2]: ...             # True — non-empty is truthy
if "x": ...                  # True
```

In a boolean context (`if`, `while`, `and`/`or`), every object is either truthy or falsy — empty containers, `0`, `None`, and `False` are falsy; virtually everything else is truthy. This is why `if not stack:` is the idiomatic way to check "is this list/stack empty" instead of `if len(stack) == 0:`.

**Related:** [boolean-basics](boolean-basics.md) · [none-type](none-type.md) · [logical-operators](logical-operators.md)
