# Z-Algorithm

```python
def z_array(s):                       # z[i] = length of longest substring starting
    n = len(s)                        #        at i that matches a PREFIX of s
    z = [0] * n
    z[0] = n
    l = r = 0                         # [l, r) = rightmost prefix-match window seen
    for i in range(1, n):
        if i < r:
            z[i] = min(r - i, z[i - l])    # reuse what the window already proved
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1                       # extend by direct comparison
        if i + z[i] > r:
            l, r = i, i + z[i]
    return z

# search: z = z_array(pattern + "#" + text); z[i] == len(pattern) → match
```

For every position, how many characters starting there match the string's own **prefix** — computed in O(n) by recycling previously-matched windows instead of re-comparing. Concatenate `pattern + "#" + text` (separator not in either) and every entry equal to `len(pattern)` marks an occurrence: string matching with code many find less finicky than [KMP](kmp.md)'s lps fallback loop. The Z-array itself answers period/border questions (Repeated Substring Pattern, Sum of Scores LC 2223). KMP, Z, and [rolling hash](rabin-karp.md) form the string-matching trio — one linear-time tool learned deeply beats three memorized shallowly, and Z is arguably the easiest to re-derive under pressure.

**Complexity:** O(n) time · O(n) space.

**Related:** [kmp](kmp.md) · [rabin-karp](rabin-karp.md) · [string-join-slice (syntax)](../syntax/string-join-slice.md)
