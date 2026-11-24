# 953. Verifying an Alien Dictionary

**Easy** · [LeetCode](https://leetcode.com/problems/verifying-an-alien-dictionary/) · [Solution file (no hints)](../../problems/0500-0999/953.py)

[📖 11. Graphs lesson](../learning/11-graphs.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 11. Graphs problems](../rmap-practice/11-graphs.md)

---

An alien language uses the lowercase English letters, but in a **different alphabetical order**. Given `words` and the alien `order` (a permutation of the 26 letters), return `True` if `words` are sorted lexicographically in that language.

```
words = ["hello", "leetcode"],  order = "hlabcdefgijkmnopqrstuvwxyz"   →  True    ('h' comes before 'l')
words = ["word", "world", "row"],  order = "worldabcefghijkmnpqstuvxyz"  →  False   ('d' comes after 'l', so "word" > "world")
words = ["apple", "app"],  order = "abcdefghijklmnopqrstuvwxyz"         →  False   (a prefix must come first)
```

**Constraints:** `1 <= words.length <= 100` · `1 <= words[i].length <= 20` · `order.length == 26` · all characters are lowercase letters

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "sorted lexicographically" | Each word must be `<=` the next. You only compare **adjacent** pairs |
| a custom `order` | Letters have a **rank** you look up: `rank['h'] < rank['l']` |
| a prefix case (`"app"` before `"apple"`) | If one word is a prefix of the other, the **shorter** must come first |
| `order` is a permutation | Every letter has a unique rank, so a lookup table is complete |

**Why adjacent pairs are enough.** Order is transitive: if `w1 <= w2` and `w2 <= w3`, then `w1 <= w3`. So checking neighbours proves the whole list.

**Comparing two words** is the usual dictionary rule: find the **first position where the letters differ**. Whichever letter has the lower rank decides which word is smaller. If there is no differing position, the words are equal up to the shorter length, so the shorter one must come first.

This is a graph-section problem because the ranks encode an order, the same idea as [Alien Dictionary](269-alien-dictionary.md), where you *derive* the order. Here you are *given* it, so it's only a lookup.

🤔 **Before you open the next section:** what's the cheapest data structure for "rank of this letter", and what should you do when the first `min(len)` letters of two words match?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Time | Space | Verdict |
|---|---|---|---|
| Map letters to ranks, **compare adjacent pairs** | O(total characters) | O(1) (26 entries) | ✅ |
| Translate every word to a standard alphabet, then `sorted()` check | O(total characters) | O(total characters) | ✅ Simple, uses extra memory |
| Sort with a custom key and compare to the input | O(n log n · L) | O(n) | ⚠️ More work than needed |

**The decision: a `rank` [hash map](../data-structures/hashmap.md) and a pairwise comparison.** The map is built once from `order`, then each adjacent pair is compared character by character.

For the comparison, `zip(a, b)` pairs the letters up to the shorter length. The first mismatching pair decides: if `rank[x] > rank[y]` the words are out of order, otherwise they're fine and we stop looking at this pair. If the loop finds no mismatch, fall through to the **prefix rule**: `len(a) > len(b)` means "bigger word first", which is out of order.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
rank = {letter: i for i, letter in enumerate(order)}
```

A dictionary from each letter to its position in the alien alphabet. `rank['h'] < rank['l']` then means `h` sorts before `l`.
→ [dict-comprehension](../syntax/dict-comprehension.md) · [enumerate](../syntax/enumerate.md) · [hashmap](../data-structures/hashmap.md)

```python
for a, b in zip(words, words[1:]):
```

Every adjacent pair of words. Zipping the list against itself shifted by one is the idiomatic way to walk neighbours.
→ [zip-function](../syntax/zip-function.md) · [list-slicing](../syntax/list-slicing.md) · [tuple-unpacking](../syntax/tuple-unpacking.md)

```python
    for x, y in zip(a, b):
        if x != y:
            if rank[x] > rank[y]:
                return False
            break
```

Walk the two words together. At the **first letters that differ**, compare their ranks. If the earlier word's letter is later in the alphabet, the list is unsorted: `False`. Otherwise this pair is fine, and `break` stops: letters after the first difference don't matter.
→ [for-loop](../syntax/for-loop.md) · [break-continue](../syntax/break-continue.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
    else:
        if len(a) > len(b):
            return False
```

A `for … else` runs the `else` only if the loop **finished without `break`**: the words matched on every shared letter. Then one is a prefix of the other, and the longer word coming first is wrong (`"apple"` before `"app"`).
→ [for-else](../syntax/for-else.md) · [if-return](../syntax/if-return.md)

```python
return True
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def isAlienSorted(self, words: List[str], order: str) -> bool:
        rank = {letter: i for i, letter in enumerate(order)}

        for a, b in zip(words, words[1:]):
            for x, y in zip(a, b):
                if x != y:
                    if rank[x] > rank[y]:
                        return False
                    break
            else:
                if len(a) > len(b):
                    return False

        return True
```

</details>

**Trace it.** `words = ["word", "world", "row"]`, `order = "worldabcefghijkmnpqstuvxyz"` (ranks: w0 o1 r2 l3 d4 …):

| Pair | First difference | Ranks | Verdict |
|---|---|---|---|
| `word` vs `world` | index 3: `d` vs `l` | `rank[d] = 4 > rank[l] = 3` | **`False`** ✅ |

For `["apple", "app"]`: `zip` finds no difference, the `else` runs, and `len 5 > 3` returns `False`.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(total characters)</summary>

**O(N)**, where `N` is the total number of characters across all words. Each adjacent pair is compared up to the length of the shorter word, and each word participates in at most two comparisons. Building `rank` is O(26) = O(1).

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).** The rank table has 26 entries regardless of input size. (`words[1:]` makes a shallow list copy of references: O(n) in the number of words. If that matters, index with `range(len(words) - 1)`.)

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Sortedness is transitive, so I only need to check each adjacent pair. I build a rank map from the alien order. For each pair I find the first position where the letters differ, and if the first word's letter has the higher rank, the list isn't sorted. If there's no difference, one word is a prefix of the other, and the longer one must not come first. That's O(total characters) time and O(1) extra space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "What if the order isn't given?" | That's [Alien Dictionary](269-alien-dictionary.md): derive ordering edges from adjacent words, then topologically sort |
| "Why only adjacent pairs?" | Transitivity of the order |
| "Equal words, `["a", "a"]`?" | Allowed: `<=` is what's required. The loop finds no difference and lengths are equal |
| "Letters outside `order`?" | Handle `KeyError`, or validate first. The problem guarantees they're all present |
| "Sort with the custom order?" | `sorted(words, key=lambda w: [rank[c] for c in w])`, then compare. Simpler, but O(n log n) |

**Traps:**

- **Forgetting the prefix case** (`"apple"` before `"app"`). The most common failed test.
- **Continuing after the first difference.** Only the *first* differing letter matters.
- **Comparing letters with `<`/`>` directly** instead of through `rank`.
- **Checking only the first and last words.** Middle words can be out of order.

**This same move shows up in:** [Alien Dictionary](269-alien-dictionary.md) · [Valid Anagram](242-valid-anagram.md) (comparing via a lookup table) · [Largest Number](179-largest-number.md) (a custom comparison order).

</details>

---
