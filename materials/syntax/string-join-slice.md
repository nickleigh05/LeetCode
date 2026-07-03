# String `.join()` / Slicing

```python
"".join(["a", "b", "c"])       # "abc"
",".join(["a", "b", "c"])      # "a,b,c"

s = "hello"
s[1:4]      # "ell"  — slice [start:stop), stop excluded
s[::-1]     # "olleh" — reversed, step -1
s[:3]       # "hel"  — from start
s[2:]       # "llo"  — to end
```

`.join()` builds a string from an iterable of strings using the separator it's called on — the idiomatic way to concatenate many pieces (faster than repeated `+`). Slicing `[start:stop:step]` never errors on out-of-range indices; it just clamps.

**Related:** [string-basics](string-basics.md) · [list-slicing](list-slicing.md) · [string-methods](string-methods.md)
