# ord() & chr()

```python
ord('a')            # 97  — character → its Unicode code point
chr(97)             # 'a' — code point → character

ord('c') - ord('a')          # 2 — letter's position in the alphabet (0-indexed)
chr(ord('a') + 2)            # 'c' — shift a letter (Caesar cipher, +k problems)

counts = [0] * 26            # the classic frequency array
for ch in word:
    counts[ord(ch) - ord('a')] += 1
```

Characters *are* numbers underneath; `ord`/`chr` convert between the two views. The bread-and-butter DSA use is mapping `'a'…'z'` to array indices `0…25` — a 26-slot list is a faster, fixed-size [Counter](counter.md) for lowercase-letter problems (anagrams, character frequencies). Useful anchors: `'a'` = 97, `'A'` = 65, `'0'` = 48 — and `int(ch)` converts a digit character properly, no ord math needed.

**Related:** [string-basics](string-basics.md) · [counter](counter.md) · [string-module-constants](string-module-constants.md) · [type-conversion](type-conversion.md)
