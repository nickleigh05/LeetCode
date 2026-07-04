# Suffix Array

```python
# suffixes of "banana", sorted:          suffix array = start indices
# 5: a                                   sa = [5, 3, 1, 0, 4, 2]
# 3: ana
# 1: anana        any substring is a prefix of some suffix —
# 0: banana       so substring search becomes binary search over sa
# 4: na
# 2: nana

sa = sorted(range(len(s)), key=lambda i: s[i:])   # O(n² log n) teaching version
```

The sorted list of a string's suffixes (stored as start indices). Because every substring is a prefix of a suffix, sorting the suffixes turns hard string questions into array questions: substring search in O(m log n) via [binary search](../algorithms/binary-search.md), and — paired with the **LCP array** (longest common prefix of neighbors, buildable in O(n)) — counting distinct substrings, longest repeated substring, longest common substring of two strings.

The naive build above is fine for grasping the idea and for small inputs; the real constructions (O(n log n) doubling with radix sort, or O(n) SA-IS) are serious competitive-programming machinery. Know the *concept* tier here: what it is, what it unlocks, and that [tries](trie.md)/[rolling hashes](../algorithms/rabin-karp.md) are the lighter tools that usually suffice on LeetCode.

**Complexity:** build O(n log n) (proper) · substring query O(m log n) · space O(n).

**Related:** [trie](trie.md) · [rabin-karp (algorithms)](../algorithms/rabin-karp.md) · [binary-search (algorithms)](../algorithms/binary-search.md)
