# Manacher's Algorithm

```python
def longest_palindrome(s):
    t = "#" + "#".join(s) + "#"        # interleave sentinels: every palindrome
    n = len(t)                         # in t is now odd-length
    p = [0] * n                        # p[i] = palindrome radius centered at i
    c = r = 0                          # center & right edge of rightmost palindrome
    for i in range(n):
        if i < r:
            p[i] = min(r - i, p[2 * c - i])    # steal the mirror position's answer
        while i - p[i] - 1 >= 0 and i + p[i] + 1 < n and t[i - p[i] - 1] == t[i + p[i] + 1]:
            p[i] += 1                           # extend past what's proven
        if i + p[i] > r:
            c, r = i, i + p[i]
    k = max(range(n), key=lambda i: p[i])
    return s[(k - p[k]) // 2 : (k + p[k]) // 2]
```

Longest palindromic substring in **O(n)** — the mastery-tier upgrade over expand-around-center's O(n²) (which, to be clear, passes LC 5 and is what you should write in an interview). The trick mirrors the [Z-algorithm](z-algorithm.md)'s: inside a known palindrome, position i's answer starts as its mirror's answer, so characters are never re-compared from scratch; the `#` sentinels fold the odd/even-length cases into one. Know the tiering: expand-around-center to *solve*, Manacher to *win arguments about optimality* (and the rare follow-up: "can you do it linear?").

**Complexity:** O(n) time · O(n) space.

**Related:** [z-algorithm](z-algorithm.md) · [Two Pointers lesson](../learning/02-two-pointers.md) · [string-join-slice (syntax)](../syntax/string-join-slice.md)
