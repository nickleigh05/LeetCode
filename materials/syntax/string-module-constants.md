# string Module Constants

```python
import string

string.ascii_lowercase    # 'abcdefghijklmnopqrstuvwxyz'
string.ascii_uppercase    # 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
string.ascii_letters      # both, lower first
string.digits             # '0123456789'
string.punctuation        # '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

for c in string.ascii_lowercase:      # try every next letter (Word Ladder mutation)
    candidate = word[:i] + c + word[i + 1:]
```

Prewritten alphabet strings — nothing more, but they read better and typo less than hand-typing `'abcdefghijklmnopqrstuvwxyz'`. Typical DSA cameos: iterating candidate letters in Word Ladder-style BFS, building character→index maps, and checking membership (`ch in string.digits` — though the [string *methods*](string-methods.md) `ch.isdigit()` / `.isalpha()` are the more idiomatic test). Pairs naturally with [ord/chr](ord-chr.md) when you need positions instead of characters.

**Related:** [ord-chr](ord-chr.md) · [string-methods](string-methods.md) · [string-basics](string-basics.md)
