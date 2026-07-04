# Rabin-Karp (Rolling Hash)

```python
def rabin_karp(text, p):
    B, MOD = 131, (1 << 61) - 1              # base & big prime modulus
    m = len(p)
    if m > len(text): return -1
    ph = th = 0
    power = pow(B, m - 1, MOD)               # for removing the leading char
    for i in range(m):
        ph = (ph * B + ord(p[i])) % MOD
        th = (th * B + ord(text[i])) % MOD
    for i in range(len(text) - m + 1):
        if th == ph and text[i:i + m] == p:  # verify to kill false positives
            return i
        if i + m < len(text):                # roll: drop left char, add right
            th = ((th - ord(text[i]) * power) * B + ord(text[i + m])) % MOD
    return -1
```

Compare strings by comparing **numbers**: treat a window as a base-B integer mod a big prime, and when the window slides one step, update the hash in O(1) — subtract the outgoing character's contribution, multiply, add the incoming one. Equal hashes are then verified (or, with a 2⁶¹-sized modulus, trusted). The payoff over [KMP](kmp.md) is flexibility: the same rolling hash searches *many* patterns at once, powers Longest Duplicate Substring (LC 1044 — [binary search](binary-search.md) on length + hash set of window hashes), detects repeated DNA sequences (LC 187), and pairs with two pointers for palindrome checks. It's the string trick that generalizes.

**Complexity:** O(n + m) expected · O(1) extra space (O(n) when storing window hashes).

**Related:** [kmp](kmp.md) · [Sliding Window lesson](../learning/03-sliding-window.md) · [ord-chr (syntax)](../syntax/ord-chr.md) · [suffix-array (data-structures)](../data-structures/suffix-array.md)
