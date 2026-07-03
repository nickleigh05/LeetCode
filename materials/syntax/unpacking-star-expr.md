# Star Unpacking (`*rest`)

```python
first, *rest = [1, 2, 3, 4]      # first=1, rest=[2, 3, 4]
*init, last = [1, 2, 3, 4]        # init=[1, 2, 3], last=4
a, *mid, b = [1, 2, 3, 4]          # a=1, mid=[2, 3], b=4

def total(*args):                  # collects extra positional args into a tuple
    return sum(args)
```

`*name` in an unpacking assignment scoops up "everything else" into a list, letting you grab the first/last element(s) without slicing. The same `*` syntax collects variadic function arguments — see [args-kwargs](args-kwargs.md).

**Related:** [tuple-unpacking](tuple-unpacking.md) · [args-kwargs](args-kwargs.md) · [list-slicing](list-slicing.md)
