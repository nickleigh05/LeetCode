# None

```python
x = None
if x is None:
    ...
```

`None` is Python's "no value" singleton — the sole instance of `NoneType`. Use `is None` / `is not None` to check for it, not `== None` (works, but `is` is the convention since `None` is a singleton).

Common in linked-list/tree problems as the "empty" sentinel (`node.next is None`), and as a default return when nothing was found.

**Related:** [identity-operators](identity-operators.md) · [default-arguments](default-arguments.md) · [truthy-falsy-values](truthy-falsy-values.md)
