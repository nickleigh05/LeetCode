# KMP (Knuth-Morris-Pratt)

```python
def build_lps(p):                     # lps[i] = length of longest proper prefix
    lps, k = [0] * len(p), 0          #          of p[:i+1] that's also a suffix
    for i in range(1, len(p)):
        while k and p[i] != p[k]:
            k = lps[k - 1]            # fall back to the next-shorter border
        if p[i] == p[k]:
            k += 1
        lps[i] = k
    return lps

def kmp_search(text, p):              # first occurrence of p in text (LC 28)
    lps, k = build_lps(p), 0
    for i, c in enumerate(text):
        while k and c != p[k]:
            k = lps[k - 1]
        if c == p[k]:
            k += 1
        if k == len(p):
            return i - k + 1
    return -1
```

String matching in guaranteed O(n + m), versus the naive method's O(n·m) on adversarial inputs like `"aaaa…"`. The insight: when a match breaks after k characters, those k characters are *known* — the `lps` ("longest prefix-suffix") table says exactly how much of them still counts as matched, so the text pointer **never moves backward**. The `lps` table is valuable solo: it powers Shortest Palindrome (LC 214) and Repeated Substring Pattern (LC 459). Interview reality: quoting the idea and complexity usually suffices — few interviewers expect flawless `lps` code live — and [Rabin-Karp](rabin-karp.md) is the easier-to-derive alternative.

**Complexity:** O(n + m) time · O(m) space.

**Related:** [rabin-karp](rabin-karp.md) · [z-algorithm](z-algorithm.md) · [string-basics (syntax)](../syntax/string-basics.md)
