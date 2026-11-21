# 409. Longest Palindrome

**Easy** · [LeetCode](https://leetcode.com/problems/longest-palindrome/) · [Solution file (no hints)](../../problems/0001-0499/409.py)

[📖 01. Arrays & Hashing lesson](../learning/01-arrays-hashing.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 01. Arrays & Hashing problems](../rmap-practice/01-arrays-hashing.md)

---

Given a string `s` of lowercase or uppercase letters, return the **length of the longest palindrome** that can be **built** with those letters. Letters are case-sensitive: `"Aa"` is not a palindrome.

```
s = "abccccdd"  →  7      (e.g. "dccaccd")
s = "a"         →  1
s = "Aa"        →  1      ('A' and 'a' are different letters)
```

**Constraints:** `1 <= s.length <= 2000` · `s` consists of lowercase and/or uppercase English letters only

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "can be **built** with those letters" | You choose and rearrange letters freely. This is **not** "find the longest palindromic substring" |
| return the **length** | You never need to build the palindrome itself, just count |
| **case-sensitive** | `'A'` and `'a'` are separate keys. Don't lowercase the string |
| length ≤ 2000 | Small, but the counting answer is O(n) anyway |

**What does a palindrome look like, by counts?** It mirrors around its centre. Every letter on the left has a twin on the right, so:

- Every letter appears an **even** number of times…
- …except **at most one** letter, which can sit alone in the middle.

So the question is: how many letters can you pair up, plus one for the centre if anything is left over?

For each letter with count `c`:
- You can use `c // 2` **pairs**, which is `(c // 2) * 2` letters.
- If `c` is odd, one copy is left over. Any one leftover letter, from any letter, can become the centre. Only one centre is allowed, so you add **1** at most once, however many odd counts there are.

🤔 **Before you open the next section:** with counts `{a:1, b:1, c:4, d:2}`, how many letters go into pairs, and can you add anything else?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Try arrangements | Generate subsets and permutations, test each | Exponential | — | ❌ Hopeless |
| Greedy pairing with a set | Toggle each char in a set; a removal means a pair formed | O(n) | O(1)* | ✅ Neat alternative |
| **Count, then sum pairs** | Frequency map → add pairs, add 1 if any count is odd | **O(n)** | O(1)* | ✅ Clearest |

\* At most 52 distinct letters.

**The decision: a [hash map](../data-structures/hashmap.md) of character counts, then a greedy sum.**

This is greedy in the simplest sense: using every available pair is always optimal, because pairs never conflict with each other. The only constraint is "one centre," and a single boolean handles that.

**The set-toggle alternative**, for comparison:

```python
seen = set()
pairs = 0
for ch in s:
    if ch in seen:
        seen.remove(ch)
        pairs += 1
    else:
        seen.add(ch)
return pairs * 2 + (1 if seen else 0)
```

It's one pass and just as fast. Whatever is left in `seen` at the end is the unpaired letters, and any one of them can be the centre. The count version is easier to explain from first principles, so that's the one built below.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
counts = {}
for char in s:
    counts[char] = counts.get(char, 0) + 1
```

Count each letter. `.get(char, 0)` returns 0 the first time a letter shows up, so the same line handles new letters and repeats. Uppercase and lowercase land in separate keys automatically.
→ [dict-basics](../syntax/dict-basics.md) · [dict-methods](../syntax/dict-methods.md) · [for-loop](../syntax/for-loop.md)

```python
length = 0
has_odd = False
```

`length` is the running total of letters placed in mirrored pairs. `has_odd` records whether *any* letter had a leftover copy that could be the centre.
→ [variables-assignment](../syntax/variables-assignment.md) · [boolean-basics](../syntax/boolean-basics.md)

```python
for c in counts.values():
    length += (c // 2) * 2
    if c % 2 == 1:
        has_odd = True
```

**The greedy step.** `c // 2` is how many complete pairs this letter gives, and `* 2` turns pairs back into letters. A count of 5 contributes 4, and a count of 4 contributes 4.

`c % 2 == 1` spots a leftover copy. You only need to know that **at least one** exists, so it's a flag rather than a counter.
→ [integer-division-modulo](../syntax/integer-division-modulo.md) · [dict-methods](../syntax/dict-methods.md)

```python
if has_odd:
    length += 1
return length
```

Add the single centre letter if one is available. It's at most once, because a palindrome has exactly one middle.
→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def longestPalindrome(self, s: str) -> int:

        counts = {}
        for char in s:
            counts[char] = counts.get(char, 0) + 1

        length = 0
        has_odd = False
        for c in counts.values():
            length += (c // 2) * 2
            if c % 2 == 1:
                has_odd = True

        if has_odd:
            length += 1
        return length
```

</details>

**Trace it.** `s = "abccccdd"` gives counts `{a:1, b:1, c:4, d:2}`:

| letter | count | pairs → letters | odd? | `length` | `has_odd` |
|---|---|---|---|---|---|
| a | 1 | 0 | yes | 0 | True |
| b | 1 | 0 | yes | 0 | True |
| c | 4 | 4 | no | 4 | True |
| d | 2 | 2 | no | 6 | True |
| centre | | | | **7** | |

Answer **7** ✅, for example `"dccaccd"`. Only one of `a`/`b` can take the centre. The other is simply left out.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).** One pass to count, then one pass over the distinct letters, of which there are at most 52, so that second loop is O(1).

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).** The map holds at most 52 keys (26 lowercase + 26 uppercase), however long `s` is.

If the alphabet were unbounded, this becomes O(k) for k distinct characters.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "I'm building a palindrome from the letters, not finding a substring, so only the counts matter. A palindrome is pairs mirrored around an optional single centre. For each letter I add `count // 2 * 2` for its pairs, and I remember whether any count was odd. At the end I add one if there was an odd count, because exactly one leftover letter can sit in the middle. O(n) time, O(1) space since there are at most 52 letters."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Can you do it in one pass?" | The set-toggle version above: a removal means a pair formed, and whatever's left at the end can supply the centre. |
| "Return the palindrome itself." | Build the left half from `c // 2` copies of each letter, add an odd letter for the middle, then append the reversed left half. |
| "Can a permutation of `s` be a palindrome?" | Same counting idea: **at most one** odd count. That's LeetCode 266. |
| "Longest palindromic **substring**?" | A completely different problem, solved with expand-around-centre. See [Longest Palindromic Substring](5-longest-palindromic-substring.md). |

**Traps:**

- **Adding 1 for every odd count.** Only one letter can be the centre. `"abc"` is 1, not 3.
- **Dropping odd counts entirely.** A count of 5 still gives 4 letters of pairs. Use `c // 2 * 2`, not "if even, add c".
- **Lowercasing the input.** The problem is case-sensitive, so `"Aa"` → 1.
- **Confusing it with substring problems.** Reading "palindrome" and reaching for expand-around-centre wastes the interview.

**This same move shows up in:** [Valid Anagram](242-valid-anagram.md) (frequency counting as the whole solution) · [Ransom Note](383-ransom-note.md) (counts that must cover a requirement) · [Longest Palindromic Substring](5-longest-palindromic-substring.md) (the contiguous version, which needs a different technique) · [Reorganize String](767-reorganize-string.md) (greedy reasoning on counts).

</details>

---
