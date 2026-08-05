# 242. Valid Anagram

**Easy** · [LeetCode](https://leetcode.com/problems/valid-anagram/) · [Solution file (no hints)](../../problems/0001-0499/242.py)

[📖 01. Arrays & Hashing lesson](../learning/01-arrays-hashing.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 01. Arrays & Hashing problems](../rmap-practice/01-arrays-hashing.md)

---

Given two strings `s` and `t`, return `true` if `t` is an anagram of `s` — the same letters, the same number of each, in any order.

```
s = "anagram", t = "nagaram"  →  true
s = "rat",     t = "car"      →  false
```

**Constraints:** `1 <= s.length, t.length <= 5·10⁴` · `s` and `t` consist of lowercase English letters

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "same letters, **in any order**" | Order is irrelevant → you're comparing **multisets**, not sequences. Position carries no information |
| "the same **number of each**" | Not just *which* letters — **how many**. This is a counting problem |
| lengths up to 5·10⁴ | O(n²) (checking each letter against the whole other string) is out. You want O(n) or O(n log n) |
| "**lowercase English letters**" | The alphabet is **fixed at 26**. That's a promise you can exploit — anything sized by the alphabet is O(1), not O(n) |

The insight worth pausing on: an anagram is exactly *"both strings have identical letter counts."* Once you phrase it that way, the solution is a mechanical consequence.

And a free early exit: **different lengths can never be anagrams.**

🤔 **Before you open the next section:** how would you represent "the letter counts of a string" so that two of them can be compared in one step?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Brute force | For each char in `s`, find and remove it from `t` | O(n²) | O(n) | ❌ Too slow at 5·10⁴ |
| Sort both | `sorted(s) == sorted(t)` — anagrams share a sorted form | O(n log n) | O(n) | ⚠️ Correct and a great one-liner, but the log n is unnecessary |
| Two hash maps | Count each string, compare the maps | O(n) | O(1)† | ✅ |
| One array of 26 | `+1` walking `s`, `-1` walking `t`; all zeros ⇒ anagram | O(n) | O(1) | ✅ Same idea, tighter |

† Bounded by the 26-letter alphabet, so constant — see the space section.

**The decision: two [hash maps](../data-structures/hashmap.md) of character counts.**

Counting is a single pass per string, and comparing two dicts is one operation. It expresses the insight from section 1 literally — *"do these two strings have identical letter counts?"* — which makes it easy to say out loud and hard to get subtly wrong.

**Why not sort?** `sorted(s) == sorted(t)` is genuinely good code and worth mentioning in an interview. But sorting produces *total order*, and you only needed *counts* — you're paying O(n log n) for information you throw away. The rule of thumb: **if you only need to know "how many", never buy "in what order."**

The 26-element array is the same algorithm with the dict swapped for a fixed list. Reach for it if asked to optimize constants; the dict version reads better.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
if len(s) != len(t):
    return False
```

The early exit. Different lengths can't possibly be anagrams — and this guard is load-bearing later, because it means that if every count in `s` matches `t`, no leftover letters can be hiding in `t`.
→ [if-return](../syntax/if-return.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
count_s = {}
count_t = {}
```

One frequency map per string: character → how many times it appears.
→ [dict-basics](../syntax/dict-basics.md)

```python
for char in s:
    count_s[char] = count_s.get(char, 0) + 1
```

The counting idiom. Iterating a string yields its characters one at a time. `.get(char, 0)` returns the current count, **or 0 if we've never seen this character** — which is what saves you from a `KeyError` on first sight of a letter.
→ [for-loop](../syntax/for-loop.md) · [dict-methods](../syntax/dict-methods.md) · [string-basics](../syntax/string-basics.md)

```python
for char in t:
    count_t[char] = count_t.get(char, 0) + 1
```

Identical pass over the second string. Two independent tallies, no interaction yet.

```python
return count_s == count_t
```

`==` on two dicts is a **full structural comparison**: same keys, and the same value under every key. That single operator is the entire comparison step.
→ [comparison-operators](../syntax/comparison-operators.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:

        if len(s) != len(t):
            return False

        count_s = {}
        count_t = {}

        for char in s:
            count_s[char] = count_s.get(char, 0) + 1

        for char in t:
            count_t[char] = count_t.get(char, 0) + 1

        return count_s == count_t
```

</details>

**Trace it** — `s = "aab"`, `t = "aba"`:

| Pass | Reading | Map after |
|---|---|---|
| `s` | `a`, `a`, `b` | `{a: 2, b: 1}` |
| `t` | `a`, `b`, `a` | `{a: 2, b: 1}` |
| compare | | equal ⇒ `True` |

**Shorter, same algorithm:** `return Counter(s) == Counter(t)`. `Counter` is a dict subclass built for exactly this loop.
→ [counter](../syntax/counter.md)

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)**, where n is the length of the strings.

- `len()` on a Python string is O(1) — the length is stored, not counted.
- Pass over `s`: n iterations, each doing an O(1) hash lookup and insert → O(n).
- Pass over `t`: another O(n).
- The final `==`: compares at most 26 keys → **O(1)**, since the alphabet is bounded.

O(n) + O(n) + O(1) = **O(n)**. Sequential passes *add*, they don't multiply — two loops in a row is still linear, and calling this O(n²) is a classic misread.

**Versus sorting:** the sort-based one-liner is O(n log n). For n = 5·10⁴ both are instant, but naming the difference is the point of the exercise.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — and this one is worth understanding, because it *looks* like O(n).

The maps grow with the number of **distinct characters**, not with the length of the string. The constraints promise lowercase English letters, so each map holds **at most 26 entries** whether n is 10 or 50,000. A quantity with a fixed ceiling that doesn't depend on n is constant space.

**The moment that changes:** drop the lowercase-letters constraint and it becomes **O(k)** for an alphabet of size k — approaching O(n), since you can't have more distinct characters than characters. If you claim O(1) in an interview, say *why*: "O(1), bounded by the 26-letter alphabet." Claiming it without the justification looks like a guess.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "An anagram means both strings have identical letter counts, so I'll count each string with a hash map and compare the maps. A length check first as an early exit. That's two linear passes — O(n) time — and O(1) space, because the alphabet is fixed at 26 lowercase letters. I could also sort both and compare, but that's O(n log n) for ordering information I don't need."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Do it with one hash map." | Increment walking `s`, decrement walking `t`; return `True` if every value is 0. Halves the memory. |
| "What if the strings are Unicode?" | The 26-letter assumption dies. The algorithm is unchanged, but space becomes O(k) for the distinct characters seen — a dict handles this already, a 26-slot array would not. |
| "What if you can't use extra space at all?" | Sort both in place and compare — O(n log n) time, O(1) space. The usual time-for-space trade, run backwards. |
| "Group *many* strings by anagram." | That's [Group Anagrams](49-group-anagrams.md) — same signature idea, used as a dict *key* instead of a comparison. |
| "Is it case-sensitive? Whitespace?" | Ask this *before* coding. Real-world anagram problems usually want normalization (`.lower()`, strip spaces) first. |

**Traps:**

- **`count[char] += 1` on a fresh key raises `KeyError`.** Use `.get(char, 0) + 1`, a [`defaultdict(int)`](../syntax/defaultdict.md), or a [`Counter`](../syntax/counter.md).
- **Skipping the length check** and only verifying that every letter of `s` appears in `t` with the right count. `s = "ab"`, `t = "aab"` would sneak through.
- **Comparing only the keys** (`count_s.keys() == count_t.keys()`) — that checks *which* letters, never *how many*. `"aab"` and `"abb"` would pass.
- **Calling it O(n) space** without noticing the bounded alphabet.

**This same move shows up in:** [Contains Duplicate](217-contains-duplicate.md) (a set when counts aren't needed) · [Group Anagrams](49-group-anagrams.md) (the count signature as a bucket key) · [Top K Frequent Elements](347-top-k-frequent-elements.md) (build a frequency map, then rank it).

</details>

---
