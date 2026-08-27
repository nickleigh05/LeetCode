# 1768. Merge Strings Alternately

**Easy** · [LeetCode](https://leetcode.com/problems/merge-strings-alternately/) · [Solution file (no hints)](../../problems/1500-1999/1768.py)

[📖 02. Two Pointers lesson](../learning/02-two-pointers.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 02. Two Pointers problems](../rmap-practice/02-two-pointers.md)

---

You are given two strings `word1` and `word2`. Merge them by adding letters in **alternating order**, starting with `word1`. If one string is longer, append the extra letters to the end.

```
word1 = "abc",  word2 = "pqr"    →  "apbqcr"
word1 = "ab",   word2 = "pqrs"   →  "apbqrs"
word1 = "abcd", word2 = "pq"     →  "apbqcd"
```

**Constraints:** `1 <= word1.length, word2.length <= 100` · lowercase English letters

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**alternating**, starting with `word1`" | Fixed pattern: `w1[0], w2[0], w1[1], w2[1], …` — no decisions to make |
| "if one is **longer**, append the extra" | ⚠️ The only real complexity. Lengths may differ, and the tail must survive |
| result length | Always exactly `len(word1) + len(word2)` — nothing is dropped |
| both ≥ 1 character | Neither is empty, though handling that costs nothing anyway |
| ≤ 100 characters | Trivially small; write the clearest version |

The entire problem is **handling unequal lengths gracefully**. The alternation itself is mechanical.

Three ways to think about the tail:

1. **Loop while *either* has characters left**, guarding each append individually. One loop, no separate cleanup.
2. **Zip the common prefix**, then append both remainders (one of which is empty).
3. **Loop to `max(len1, len2)`**, guarding each index.

All are fine. The first is what the solution file leads with, and it's the one that generalizes best.

🤔 **Before you open the next section:** if you loop while *either* string still has characters, what must you check before each individual append?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| **Two pointers, `or` condition** | Loop while either remains; guard each append | O(n+m) | ✅ Handles the tail with no special case |
| `zip` + remainders | Zip pairs the common prefix; append both leftovers | O(n+m) | ✅ Most Pythonic |
| Single index to `max` | One counter, guard both indexes | O(n+m) | ✅ Compact |
| String `+=` in a loop | Concatenate onto a string | **O((n+m)²)** | ❌ Quadratic — see below |

**The decision: any of the first three.** There's no algorithmic trade-off; pick the one you can write correctly under pressure. The solution file carries all three.

**The one thing that genuinely matters: build a list, then `''.join()`.**

Python strings are [immutable](../syntax/string-immutability.md), so `result += ch` **creates a whole new string** each time, copying everything accumulated so far. Doing that `k` times costs `1 + 2 + 3 + … + k` = **O(k²)** character copies.

Appending to a list is amortized O(1), and `''.join(list)` does a single pass that pre-computes the total size and fills once — **O(k)**.

| | Time for k characters |
|---|---|
| `result += ch` | O(k²) |
| `list.append` + `''.join` | **O(k)** |

At k = 200 nobody notices. At k = 10⁶ it's the difference between instant and minutes. It's the single most important Python performance idiom for string building, and this problem is a good place to lock it in.

**Why `zip` is elegant here:** `zip` stops at the **shorter** input automatically, so it handles the common prefix with no length arithmetic. Then `word1[len(word2):]` and `word2[len(word1):]` grab the remainders — and exactly one of them is non-empty, with slicing safely returning `""` when the start index is past the end. No `if` needed anywhere.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

**Approach A — two pointers** (the primary)

```python
array = []
i = 0
j = 0
```

A list accumulator (not a string — see above) plus one index per word.
→ [list-basics](../syntax/list-basics.md)

```python
while i < len(word1) or j < len(word2):
```

**`or`, not `and` — this is the crux.** With `and`, the loop would stop as soon as the *shorter* word ran out, silently dropping the longer word's tail. With `or`, it continues until **both** are exhausted.

The cost of `or` is that inside the loop, neither index is guaranteed valid — hence the individual guards below.
→ [while-loop](../syntax/while-loop.md) · [logical-operators](../syntax/logical-operators.md)

```python
    if i < len(word1):
        array.append(word1[i])
        i += 1
```

Take from `word1` **if it still has characters**. Once exhausted, this block is skipped and only `word2` contributes — which is precisely the "append the extra letters" behaviour, achieved with no separate cleanup phase.
→ [list-methods](../syntax/list-methods.md)

```python
    if j < len(word2):
        array.append(word2[j])
        j += 1
```

Same for `word2`. Two independent `if`s, not `if/else` — on most iterations **both** fire, which is what produces the alternation.
→ [elif-else](../syntax/elif-else.md)

```python
return ''.join(array)
```

One O(k) pass to build the final string.
→ [string-join-slice](../syntax/string-join-slice.md)

<details>
<summary>Approach A together</summary>

```python
class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:

        array = []
        i = 0
        j = 0

        while i < len(word1) or j < len(word2):
            if i < len(word1):
                array.append(word1[i])
                i += 1
            if j < len(word2):
                array.append(word2[j])
                j += 1

        return ''.join(array)
```

</details>

---

**Approach B — `zip` plus remainders**

```python
result = []
for c1, c2 in zip(word1, word2):
    result.append(c1)
    result.append(c2)
result.append(word1[len(word2):])
result.append(word2[len(word1):])
return "".join(result)
```

`zip` pairs characters and **stops at the shorter word** — handling the common prefix with zero length arithmetic.

Then the two slices grab whatever's left. Exactly one is non-empty; the other is `""`, because slicing past the end of a string returns empty rather than raising. Appending `""` to the list is harmless, so no branching is needed.

Note this appends whole *strings* rather than single characters — `join` handles both identically.
→ [zip-function](../syntax/zip-function.md) · [list-slicing](../syntax/list-slicing.md)

<details>
<summary>Approach B together</summary>

```python
### using zip ###
class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        result = []
        for c1, c2 in zip(word1, word2):
            result.append(c1)
            result.append(c2)
        result.append(word1[len(word2):])
        result.append(word2[len(word1):])
        return "".join(result)
```

</details>

**Trace approach A** — `word1 = "ab"`, `word2 = "pqrs"`:

| Iter | `i` | `j` | `i < 2`? | append | `j < 4`? | append | `array` |
|---|---|---|---|---|---|---|---|
| 1 | 0 | 0 | ✅ | `a` | ✅ | `p` | `[a,p]` |
| 2 | 1 | 1 | ✅ | `b` | ✅ | `q` | `[a,p,b,q]` |
| 3 | 2 | 2 | ❌ | — | ✅ | `r` | `[a,p,b,q,r]` |
| 4 | 2 | 3 | ❌ | — | ✅ | `s` | `[a,p,b,q,r,s]` |
| 5 | 2 | 4 | both false → loop ends | | | | |

Result `"apbqrs"` ✅

Iterations 3 and 4 show the tail handling: `word1` is spent, so only `word2` appends — no special case required.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n + m)</summary>

**O(n + m)**, where `n = |word1|` and `m = |word2|`.

Each loop iteration consumes at least one character, and there are `n + m` characters total, so the loop runs at most `n + m` times with O(1) work each. The final `''.join` is one more O(n + m) pass.

This is optimal — the output has `n + m` characters, so you must write that many.

**The complexity that would bite you:** using `result += ch` makes it **O((n+m)²)**. Same loop, same logic, quadratically worse, purely from Python's string immutability. Worth knowing cold.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n + m)</summary>

**O(n + m)** for the output, which is unavoidable — you're asked to return a string of that length.

**O(n + m) auxiliary** for the intermediate list too, though it's freed once `join` completes. If you wanted to be pedantic about auxiliary space you could write into a preallocated buffer, but in Python the list-then-join idiom is both idiomatic and near-optimal.

Two integer indices are O(1).

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Two pointers, one per word, looping while **either** still has characters — `or`, not `and`, so the longer word's tail isn't dropped. Inside, I guard each append separately, so once one word is exhausted only the other contributes, which handles the leftover automatically without a cleanup phase. I accumulate into a list and `join` at the end rather than using `+=`, since string concatenation in a loop is O(k²) in Python. O(n+m) time and space. A `zip`-based version is a bit tidier — zip stops at the shorter word, then I append both remainders and one is just empty."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Merge **k** strings alternately." | Cycle through a list of indices, one per string, skipping exhausted ones — `itertools.zip_longest` with `fillvalue=''` is the clean version. |
| "Why not `+=`?" | Strings are immutable, so each `+=` copies the whole accumulated string — O(k²). List + `join` is O(k). |
| "Start with `word2` instead?" | Swap the two `if` blocks, or call `mergeAlternately(word2, word1)`. |
| "Alternate in chunks of `k`?" | Same skeleton, but advance each index by `k` and append slices instead of single characters. |
| "What if one string is empty?" | The `or` condition and the guards handle it — you get the other string unchanged. |
| "Do it without extra space?" | Not in Python; strings are immutable, so any result requires a new allocation. In C you could write into a preallocated buffer. |
| "Interleave two **lists** instead?" | Identical logic; `join` becomes list concatenation, or use `itertools.chain`. |

**Traps:**

- **Using `and` in the loop condition.** Stops at the shorter word and silently truncates the tail. The single most common bug here — test with different lengths.
- **`if / else` instead of two `if`s.** Only one character per iteration, producing the wrong interleaving.
- **`result += ch`.** Quadratic. Correct output, bad habit.
- **Looping to `min(len1, len2)` and forgetting the remainder.** Truncates silently.
- **Indexing without guarding.** `word1[i]` after `word1` is exhausted raises `IndexError`.
- **Assuming equal lengths.** The examples deliberately include both longer-first and longer-second cases.

**This same move shows up in:** [Merge Two Sorted Lists](21-merge-two-sorted-lists.md) (two pointers over two sequences, with tail handling) · [Merge Sorted Array](88-merge-sorted-array.md) (the same "one runs out first" cleanup problem) · [Is Subsequence](392-is-subsequence.md) (two pointers advancing at different rates) · [Encode and Decode Strings](271-encode-and-decode-strings.md) (list-then-join string building).

</details>

---
