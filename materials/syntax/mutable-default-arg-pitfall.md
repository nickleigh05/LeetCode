# The Mutable Default Argument Pitfall

```python
def append_to(item, bucket=[]):     # BUG: bucket is created ONCE at def time
    bucket.append(item)
    return bucket

append_to(1)     # [1]
append_to(2)     # [1, 2]  — surprise! same list reused across calls

def append_to(item, bucket=None):    # correct fix
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket
```

Default argument values are evaluated once, when the function is defined — not fresh on every call. Using a mutable default (`[]`, `{}`, `set()`) means every call that omits the argument shares and mutates the *same* object. Always default to `None` and create the mutable object inside the function body instead.

**Related:** [default-arguments](default-arguments.md) · [none-type](none-type.md)
