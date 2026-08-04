# 49. Group Anagrams

**Medium** · [LeetCode](https://leetcode.com/problems/group-anagrams/) · [Solution file (no hints)](../../problems/0001-0499/49.py)

[📖 01. Arrays & Hashing lesson](../learning/01-arrays-hashing.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 01. Arrays & Hashing problems](../rmap-practice/01-arrays-hashing.md)

---

Given an array of strings `strs`, group the anagrams together. Return the groups in any order.

```
strs = ["eat","tea","tan","ate","nat","bat"]
  →  [["eat","tea","ate"], ["tan","nat"], ["bat"]]

strs = [""]      →  [[""]]
strs = ["a"]     →  [["a"]]
```

**Constraints:** `1 <= strs.length <= 10⁴` · `0 <= strs[i].length <= 100` · lowercase English letters (**empty strings are allowed**)

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**group** the anagrams together" | Not a yes/no like [Valid Anagram](242-valid-anagram.md) — you're **bucketing**. Something must serve as the bucket label |
| "in **any order**" | No sorting of the output, no ordering logic to write. Pure grouping |
| n up to 10⁴ | Comparing every word to every other word is 10⁸ *anagram checks*, each itself O(k). Dead. You need to touch each word **once** |
| word length ≤ 100 | Per-word work is cheap and bounded — you can afford to do real work on each word, just not on each *pair* |
| lowercase letters, and `""` is valid | A 26-slot count is viable, and your code must not choke on the empty string |

The key move: stop thinking about *comparing* words. Instead give each word a **canonical form** — a label that is identical for anagrams and different for everything else. Then grouping is just "put words with the same label in the same bucket."

For "eat", "tea", "ate" that label could be `"aet"` — sort the letters and they all collapse to the same string.

🤔 **Before you open the next section:** what could you compute *from a single word* that comes out identical for all its anagrams? Can you name two different options?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

The real decision here isn't the data structure — it's obviously a [hash map](../data-structures/hashmap.md) of label → list of words. **The decision is what to use as the label.**

| Signature | How it works | Time | Verdict |
|---|---|---|---|
| Pairwise comparison | Compare every word to every group's representative | O(n²·k) | ❌ 10⁸ anagram checks |
| **Sorted string** | `"".join(sorted(word))` — anagrams share a sorted form | O(n·k log k) | ✅ Simplest to write and to explain |
| **26-letter count tuple** | `tuple` of how many of each letter | O(n·k) | ✅ Asymptotically better; more code |
| Product of primes | Map each letter to a prime, multiply | O(n·k) | ❌ Cute, but overflows and reads as a trick |

**The decision: the sorted string as a hash-map key.**

Two words are anagrams *precisely* when their sorted forms are equal, so the label is exact — no false groupings possible. One pass, one `sorted()` per word, done.

**Why not the count tuple, if it's faster?** It genuinely is — O(k) beats O(k log k), and with k ≤ 100 the count version wins in a benchmark. But `log 100` is under 7, so it's a small constant on already-cheap work, and the sorted version is dramatically easier to write correctly under pressure. **Mention the count-tuple optimization out loud; implement the sorted one unless asked.** That's the trade an interviewer wants to hear you make explicitly.

**Why a tuple and not a list for the count key?** Lists are mutable and therefore unhashable — `{[1,0,2]: ...}` raises `TypeError`. Dict keys must be immutable, which is why the alternative uses `tuple(counts)`.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
hashmap = {}
```

The buckets: **signature → list of the original words** that share it.
→ [dict-basics](../syntax/dict-basics.md)

```python
for word in strs:
```

One pass over the words. Crucially, no inner loop over *other words* — every word is handled purely on its own, and the map does the matching.
→ [for-loop](../syntax/for-loop.md)

```python
    key = "".join(sorted(word))
```

The canonical form, and the heart of the solution. `sorted("eat")` gives the **list** `['a','e','t']`, so `"".join(...)` glues it back into the string `"aet"`. "tea" and "ate" produce that identical string — which is exactly what makes them land in the same bucket.

The `join` isn't optional: a list can't be a dict key.
→ [sorting-key](../syntax/sorting-key.md) · [string-join-slice](../syntax/string-join-slice.md) · [list-basics](../syntax/list-basics.md)

```python
    if key not in hashmap:
        hashmap[key] = []
```

First sighting of a signature ⇒ create its (empty) bucket. Without this, the next line would raise `KeyError` on a brand-new key.
→ [membership-operators](../syntax/membership-operators.md)

```python
    hashmap[key].append(word)
```

Append the **original** word, not the sorted key — the output wants the real strings. `hashmap[key]` fetches the list, `.append` mutates it in place.
→ [list-methods](../syntax/list-methods.md)

```python
return list(hashmap.values())
```

Back out of the loop — every word has been bucketed. The keys were only ever scaffolding. The answer is the buckets themselves, and `.values()` gives them — wrapped in `list()` because it returns a view, not a list.
→ [dict-methods](../syntax/dict-methods.md) · [type-conversion](../syntax/type-conversion.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:

        hashmap = {}

        for word in strs:
            key = "".join(sorted(word))

            if key not in hashmap:
                hashmap[key] = []

            hashmap[key].append(word)

        return list(hashmap.values())
```

</details>

**Trace it** — `strs = ["eat", "tea", "tan", "bat"]`:

| `word` | `key` | Map after |
|---|---|---|
| `eat` | `aet` | `{aet: [eat]}` |
| `tea` | `aet` | `{aet: [eat, tea]}` |
| `tan` | `ant` | `{aet: [eat, tea], ant: [tan]}` |
| `bat` | `abt` | `… , abt: [bat]}` |

Result: `[["eat","tea"], ["tan"], ["bat"]]`.

**Two ways to shorten the create-then-append dance:**

```python
hashmap = defaultdict(list)      # missing key auto-creates []
hashmap[key].append(word)
```
→ [defaultdict](../syntax/defaultdict.md) · or [`dict.setdefault`](../syntax/dict-methods.md)

**The O(n·k) variant**, using counts instead of sorting:

```python
count = [0] * 26
for c in word:
    count[ord(c) - ord("a")] += 1
key = tuple(count)
```
→ [ord-chr](../syntax/ord-chr.md) · [tuple-basics](../syntax/tuple-basics.md)

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n · k log k)</summary>

**O(n · k log k)**, where n is the number of words and k is the maximum word length.

Per word:
- `sorted(word)` → **O(k log k)** — this dominates.
- `"".join(...)` → O(k).
- Hashing the key → O(k), because hashing a string reads all its characters.
- The dict lookup and `.append` → O(1) each (append is amortized O(1)).

So O(k log k) per word × n words = **O(n · k log k)**.

**The subtlety most people miss:** dict operations are O(1) in the *number of entries*, but hashing a **string** key costs O(k). It's genuinely O(1) only for fixed-size keys like ints. Here it's dominated by the sort anyway, so it doesn't change the answer — but knowing why is what separates a memorized complexity from an understood one.

**The count-tuple version is O(n · k)** — it drops the log by never sorting.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n · k)</summary>

**O(n · k).**

- Every input word is stored exactly once across the buckets → O(n · k).
- The keys add at most one k-length signature per group → also O(n · k) worst case, when no two words are anagrams and every word is its own group.

There's no way around this bound: **the output alone is O(n · k)**, since it contains every input string. When the answer is required to be that large, you can't do better — a useful thing to say out loud, because it shows you're distinguishing *auxiliary* space from *output* space.

**Auxiliary space** (everything beyond the required output) is just the keys, O(n · k) worst case — and the count-tuple variant shrinks that to O(n · 26) = **O(n)**, since every key is a fixed 26 slots regardless of word length.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Comparing every pair of words is O(n²·k) and won't scale. Instead of comparing words to each other, I'll give each word a canonical signature that's identical for anagrams — the sorted string. Then it's one pass, bucketing into a hash map keyed by that signature, and I return the buckets. O(n·k log k) time, O(n·k) space. If I want to drop the log, I can key on a 26-letter count tuple instead of sorting, which makes it O(n·k)."

The transferable idea: **when you need to group by an equivalence, find a canonical form and use it as a key.** That's the same trick behind deduplication, memoization keys, and database indexes.

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Can you beat O(n·k log k)?" | Yes — the 26-slot count tuple as the key. O(n·k), and the keys become fixed-size. |
| "What if the alphabet is Unicode?" | The 26-array dies; sorting still works unchanged. Or use a `Counter`'s items as a frozen key — but that's O(k log k) again to canonicalize the order. |
| "What if the strings are enormous, k ≫ n?" | Sorting per word starts to hurt; counting wins outright. Beyond that, hash the count vector to shrink the keys. |
| "Return groups sorted by size?" | `sorted(hashmap.values(), key=len, reverse=True)` — see [min-max-key](../syntax/min-max-key.md). |
| "What about the empty string?" | It works: `"".join(sorted(""))` is `""`, a perfectly good key. All empty strings group together, which is correct. |
| "Can you do it without extra space?" | Not meaningfully — the output *is* the grouping. |

**Traps:**

- **Appending the key instead of the word.** You'd return `["aet","aet"]` instead of `["eat","tea"]`.
- **Using a list as the key** in the count variant — unhashable, `TypeError`. Convert with `tuple(...)`.
- **Forgetting `"".join`** — `sorted(word)` is a list, so it can't be a key either.
- **`hashmap[key].append(word)` without creating the bucket** → `KeyError`. Use the `if not in` guard, `defaultdict(list)`, or `setdefault`.
- **Returning `hashmap.values()` directly.** It's a view object, not a list; wrap it.

**This same move shows up in:** [Valid Anagram](242-valid-anagram.md) (the same signature, compared instead of used as a key) · [Top K Frequent Elements](347-top-k-frequent-elements.md) (bucketing by a derived value) · [Valid Sudoku](36-valid-sudoku.md) (a derived key per row/column/box).

</details>
