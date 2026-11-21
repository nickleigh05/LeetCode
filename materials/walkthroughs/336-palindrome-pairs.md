# 336. Palindrome Pairs

**Hard** · [LeetCode](https://leetcode.com/problems/palindrome-pairs/) · [Solution file (no hints)](../../problems/0001-0499/336.py)

[📖 01. Arrays & Hashing lesson](../learning/01-arrays-hashing.md) · [📖 08. Tries lesson](../learning/08-tries.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 01. Arrays & Hashing problems](../rmap-practice/01-arrays-hashing.md)

---

You're given a 0-indexed array of **unique** strings `words`. A **palindrome pair** is a pair of indices `(i, j)` with `i != j` such that `words[i] + words[j]` is a palindrome. Return **all** palindrome pairs.

```
words = ["abcd","dcba","lls","s","sssll"]
→ [[0,1],[1,0],[3,2],[2,4]]
   "abcddcba", "dcbaabcd", "slls", "llssssll"

words = ["bat","tab","cat"]
→ [[0,1],[1,0]]

words = ["a",""]
→ [[0,1],[1,0]]
```

**Constraints:** `1 <= words.length <= 5000` · `0 <= words[i].length <= 300` · lowercase English letters · all words are **unique**

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| `words[i] + words[j]` | **Order matters.** `(0,1)` and `(1,0)` are different pairs |
| `i != j` | A palindrome word can't pair with itself |
| up to 5000 words | All pairs is 2.5·10⁷ concatenations × 300 characters. Far too slow |
| words up to 300 long | Work **per word** that's O(k²) for word length k is fine |
| the empty string can appear | `""` pairs with every palindrome, in both orders |

**What makes `A + B` a palindrome?** Suppose `A` is the longer one. Split `A` into a **prefix** and a **suffix**. Then `A + B` reads the same both ways exactly when:

```
A = [ prefix ][ suffix ]        B = reverse(prefix)
A + B = prefix · suffix · reverse(prefix)
```

The outer parts mirror each other automatically, so the only remaining requirement is that the **suffix** reads the same both ways.

> **`A + B` is a palindrome if `A = prefix + suffix`, the suffix is a palindrome, and `B` is the reverse of the prefix.**

There's a mirror case for `B + A`: if the **prefix** of `A` is a palindrome and `B` is the reverse of the **suffix**, then `B + A` is a palindrome.

**So for each word, try every split point.** For each of its k + 1 splits, check if one part is a palindrome, and look up whether the **reverse of the other part** exists as a word. A hash map from `reversed word → index` makes that lookup O(k).

🤔 **Before you open the next section:** for `A = "sssll"`, which split gives a palindrome *prefix*, and which word would have to exist for `B + A` to be a palindrome?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Try all pairs | Concatenate and check each `(i, j)` | O(n² · k) | O(k) | ❌ ~7·10⁹ at the limits |
| **Hash map of reversed words + split each word** | For each split, check one side is a palindrome, look up the other reversed | **O(n · k²)** | O(n · k) | ✅ |
| Trie of reversed words | Walk the trie along each word; store "rest is a palindrome" lists at nodes | O(n · k²) | O(n · k) | ✅ Same bound, more code |

**The decision: a [hash map](../data-structures/hashmap.md) from each word's reverse to its index, then try every split.**

**The two checks at each split** of `word` into `prefix + suffix`. The map stores `reverse(B) → index of B`, so looking up a string `x` finds a word `B` whose reverse is `x`.

| Check | Condition | Other word `B` | Palindrome formed | Pair |
|---|---|---|---|---|
| **B goes first** | `prefix` is a palindrome and `suffix` is a key | `reverse(B) == suffix` | `B + word` = `reverse(suffix) · prefix · suffix` | `[index of B, i]` |
| **B goes second** | `suffix` is a palindrome and `prefix` is a key | `reverse(B) == prefix` | `word + B` = `prefix · suffix · reverse(prefix)` | `[i, index of B]` |

In both rows the outer parts mirror each other, and the middle part is the palindrome you checked.

**Avoiding duplicates.** When `B` is the exact reverse of `word`, the first check finds it at `cut = 0` (empty prefix), and the second check would find it again at `cut = len(word)` (empty suffix). So the second check skips the last cut. Also skip `index == i`, so a palindrome word can't pair with itself.

**The trie version** builds a [trie](../data-structures/trie.md) of reversed words and walks each word down it. It has the same complexity, but there are more edge cases to handle. The hash map is easier to get right.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
index = {word[::-1]: i for i, word in enumerate(words)}
result = []
```

**The lookup table: reversed word → its index.** Looking up a string `x` here asks "is there a word whose reverse is `x`?" The words are unique, so their reverses are unique too.
→ [dict-comprehension](../syntax/dict-comprehension.md) · [list-slicing](../syntax/list-slicing.md) · [enumerate](../syntax/enumerate.md)

```python
for i, word in enumerate(words):
    for cut in range(len(word) + 1):
        prefix = word[:cut]
        suffix = word[cut:]
```

**Every split point**, including the two ends: `cut = 0` makes the prefix empty, and `cut = len(word)` makes the suffix empty. That's k + 1 splits for a word of length k.
→ [range-function](../syntax/range-function.md) · [string-join-slice](../syntax/string-join-slice.md)

```python
        if prefix == prefix[::-1] and suffix in index and index[suffix] != i:
            result.append([index[suffix], i])
```

**`B + word` is a palindrome.** The prefix reads the same both ways, and there's a word `B` whose reverse is the suffix. Then `B + word` = `reverse(suffix) + prefix + suffix`, which is a palindrome. `B` goes **first**, so the pair is `[index of B, i]`. `index[suffix] != i` stops a palindrome pairing with itself.
→ [membership-operators](../syntax/membership-operators.md) · [logical-operators](../syntax/logical-operators.md)

```python
        if cut != len(word) and suffix == suffix[::-1] and prefix in index and index[prefix] != i:
            result.append([i, index[prefix]])
```

**`word + B` is a palindrome.** The suffix reads the same both ways, and some `B` reversed equals the prefix. Then `word + B` = `prefix + suffix + reverse(prefix)`. `B` goes **second**: `[i, index of B]`.

`cut != len(word)` skips the empty-suffix split, because the whole-word reverse match it would find is already found by the first check at `cut = 0`. Without it, those pairs would appear twice.
→ [comparison-operators](../syntax/comparison-operators.md)

```python
return result
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def palindromePairs(self, words: List[str]) -> List[List[int]]:
        index = {word[::-1]: i for i, word in enumerate(words)}
        result = []

        for i, word in enumerate(words):
            for cut in range(len(word) + 1):
                prefix = word[:cut]
                suffix = word[cut:]

                if prefix == prefix[::-1] and suffix in index and index[suffix] != i:
                    result.append([index[suffix], i])

                if cut != len(word) and suffix == suffix[::-1] and prefix in index and index[prefix] != i:
                    result.append([i, index[prefix]])

        return result
```

</details>

**Trace it.** `words = ["abcd","dcba","lls","s","sssll"]`

`index = {"dcba":0, "abcd":1, "sll":2, "s":3, "llsss":4}`

Out of every split of every word, exactly four produce a pair. All four come from the "B goes first" check:

| `i` | word | cut | prefix / suffix | Why it matches | Palindrome | Pair |
|---|---|---|---|---|---|---|
| 0 | abcd | 0 | `""` / `abcd` | `""` is a palindrome; `abcd` is a key → word 1 | `"dcba" + "abcd"` | **[1, 0]** |
| 1 | dcba | 0 | `""` / `dcba` | `""` is a palindrome; `dcba` is a key → word 0 | `"abcd" + "dcba"` | **[0, 1]** |
| 2 | lls | 2 | `ll` / `s` | `ll` is a palindrome; `s` is a key → word 3 | `"s" + "lls"` = `"slls"` | **[3, 2]** |
| 4 | sssll | 2 | `ss` / `sll` | `ss` is a palindrome; `sll` is a key → word 2 | `"lls" + "sssll"` = `"llssssll"` | **[2, 4]** |

**A near miss.** For `"sssll"` at `cut = 3`, the prefix `"sss"` is a palindrome, but `"ll"` isn't a key, since no word is `"ll"` reversed. So nothing is added.

**Where the duplicate guard matters.** At `i = 0`, `cut = 4`, the suffix `""` is a palindrome and the prefix `"abcd"` is a key, so without `cut != len(word)` the second check would add `[0, 1]` again.

All four pairs: `[1,0], [0,1], [3,2], [2,4]` ✅. The order differs from the example, which is allowed.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n · k²)</summary>

**O(n · k²)**, where n is the number of words and k is the maximum word length.

- For each of n words, there are k + 1 splits.
- Each split slices, reverses and compares strings of length up to k, and does two hash lookups. Each of those costs O(k), since hashing a string costs its length.

So n · k · k. At the limits that's 5000 · 300² ≈ 4.5·10⁸ character operations in the worst case, but Python's string slicing and comparison run in C, so in practice it passes. **The all-pairs approach** is O(n² · k) ≈ 7.5·10⁹, which doesn't.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n · k)</summary>

**O(n · k)** for the reversed-word map, which stores every word reversed. Each split creates O(k) temporary slices, freed straight away. The output can hold up to O(n²) pairs in theory (many palindromes plus the empty string), and it's usually counted separately.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Checking all pairs is O(n² k), too slow. Instead I use the structure of a palindrome. If I split a word into prefix and suffix, and the suffix is a palindrome, then the word followed by the reverse of the prefix is a palindrome. Symmetrically, if the prefix is a palindrome, the reverse of the suffix followed by the word is one. So I map each word's reverse to its index, try every split of every word, and look up the other part. I skip self-pairs, and I skip the empty-suffix split in one of the checks so whole-word reverses aren't counted twice. O(n · k²) time, O(n · k) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "How does the empty string get handled?" | For a palindrome word, the split with an empty side looks up `""` in the map, so `""` pairs in both orders automatically. |
| "Why skip `cut == len(word)` in the second check?" | The empty-suffix split finds the full reverse of the word, which the first check already found at `cut = 0`. Without skipping it, those pairs appear twice. |
| "Trie version?" | Insert reversed words into a trie. At each node, also store which words have a palindromic remainder from there. Walk each word down the trie, collecting matches. Same O(n · k²). |
| "Just count the pairs?" | The same loops, incrementing a counter instead of appending. |
| "Is a single string a palindrome?" | [Valid Palindrome](125-valid-palindrome.md), with two pointers. |

**Traps:**

- **Counting `[i, i]`.** A palindrome word would pair with itself. Check `index != i`.
- **Duplicate pairs from whole-word reverses.** `"abcd"` and `"dcba"` get found twice without the `cut != len(word)` guard.
- **Getting the order backwards.** `[index[suffix], i]` versus `[i, index[prefix]]`. Write out `B + word` and `word + B` to check.
- **Forgetting the empty-string splits.** `cut` must range over `0` to `len(word)` inclusive.
- **All pairs.** Correct, but far too slow at 5000 words.

**This same move shows up in:** [Two Sum](1-two-sum.md) (look up the complement in a hash map instead of checking all pairs) · [Valid Palindrome](125-valid-palindrome.md) (the palindrome check itself) · [Longest Palindrome](409-longest-palindrome.md) (reasoning about palindrome structure) · [Implement Trie (Prefix Tree)](208-implement-trie-prefix-tree.md) (the alternative structure for this problem).

</details>

---
