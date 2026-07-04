# Comments & Docstrings

```python
# a comment: Python ignores everything after the #
count = 0  # can sit at the end of a line too

def two_sum(nums, target):
    """Return indices of the two numbers adding to target.

    A docstring: a string as the first line of a function/class/module.
    Tools and help() read it; Python otherwise ignores it.
    """
    ...
```

Comments explain **why**, not what — `i += 1  # increment i` is noise, `# shrink window until valid again` earns its place. In interview code, one comment per non-obvious block is plenty; clear [names](variables-assignment.md) beat comments. There is no block-comment syntax in Python — a triple-quoted string not assigned to anything works but is really just a stray docstring; prefer stacked `#` lines.

**Related:** [function-basics](function-basics.md) · [pass-statement](pass-statement.md) · [type-hints](type-hints.md)
