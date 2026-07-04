# Regex Basics (re module)

```python
import re

re.findall(r"\d+", "a1b22c333")      # ['1', '22', '333'] — all matches
re.sub(r"[^a-z0-9]", "", s.lower())  # strip non-alphanumerics (Valid Palindrome prep)
re.split(r"[,;\s]+", "a, b;c  d")    # ['a', 'b', 'c', 'd'] — split on several delimiters
re.match(r"[a-z]+\d*$", s)           # None or a match — validate a whole string

# the 20% of syntax that does 80%:  \d digit  \w word-char  \s whitespace
# + one-or-more  * zero-or-more  ? optional  [] char class  [^] negated  $ end  () group
```

Pattern matching over strings. LeetCode rarely *requires* regex — and interviewers usually want the manual loop to see your logic — but for parsing-flavored tasks (log files, Advent of Code, validating formats) a one-line `findall` replaces fifteen lines of index-walking. Keep patterns in raw strings (`r"..."`) so backslashes survive. If a pattern grows beyond one line of symbols, write the explicit loop instead; unreadable regex is a bug you haven't met yet.

**Related:** [string-methods](string-methods.md) · [string-basics](string-basics.md) · [import-basics](import-basics.md)
