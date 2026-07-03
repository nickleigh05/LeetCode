# String Immutability

```python
s = "hello"
s[0] = "H"          # TypeError: 'str' object does not support item assignment

s = "H" + s[1:]     # correct way — build a *new* string
```

Strings can't be modified in place — every "modifying" operation (`.replace()`, `.upper()`, slicing, concatenation) returns a brand-new string, leaving the original untouched. For heavy character-by-character building, accumulate pieces in a list and `"".join()` at the end rather than repeatedly concatenating (repeated `+=` on strings is O(n) per operation, O(n²) overall).

**Related:** [string-basics](string-basics.md) · [string-join-slice](string-join-slice.md)
