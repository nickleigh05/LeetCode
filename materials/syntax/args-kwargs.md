# `*args` / `**kwargs`

```python
def total(*args):            # args becomes a tuple of positional extras
    return sum(args)
total(1, 2, 3)                # 6

def show(**kwargs):           # kwargs becomes a dict of keyword extras
    for k, v in kwargs.items():
        print(k, v)
show(a=1, b=2)
```

`*args` collects any number of extra positional arguments into a tuple; `**kwargs` collects extra keyword arguments into a dict. Used when a function needs to accept a variable, unknown-ahead-of-time number of inputs.

**Related:** [function-basics](function-basics.md) · [tuple-basics](tuple-basics.md) · [dict-basics](dict-basics.md) · [unpacking-star-expr](unpacking-star-expr.md)
