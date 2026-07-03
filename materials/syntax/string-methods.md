# String Methods

```python
"  hi  ".strip()          # "hi" — trims whitespace both ends
"a,b,c".split(",")         # ['a', 'b', 'c']
"cat".replace("c", "b")    # "bat"
"cat".find("t")            # 2, or -1 if not found
"cat".index("t")           # 2, raises ValueError if not found
"CAT".lower()               # "cat"
"cat".upper()                # "CAT"
"cat".startswith("ca")      # True
"cat".isdigit()              # False
```

These all return **new** strings (or new lists, for `.split()`) — none mutate the original since strings are immutable. `.find()` vs `.index()`: same job, different failure mode (returns `-1` vs raises).

**Related:** [string-immutability](string-immutability.md) · [string-basics](string-basics.md)
