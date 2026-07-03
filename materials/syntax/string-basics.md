# String Basics

```python
s = "hello"
s = 'hello'          # single or double quotes, no difference
len(s)               # 5
s[0]                 # 'h'
s + " world"         # concatenation → "hello world"
s * 3                # "hellohellohello"
```

Strings are sequences of characters — indexable and iterable just like lists — but **immutable**: no operation changes `s` in place, each one returns a new string.

**Related:** [string-immutability](string-immutability.md) · [string-methods](string-methods.md) · [string-join-slice](string-join-slice.md) · [f-strings](f-strings.md)
