# 14. Longest Common Prefix

**Easy** · [LeetCode](https://leetcode.com/problems/longest-common-prefix/) · [Solution file (no hints)](../../problems/0001-0499/14.py)

[📖 01. Arrays & Hashing lesson](../learning/01-arrays-hashing.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 01. Arrays & Hashing problems](../rmap-practice/01-arrays-hashing.md)

---

Write a function to find the longest common prefix string amongst an array of strings. If there is no common prefix, return the empty string `""`.

```
strs = ["flower","flow","flight"]   →  "fl"
strs = ["dog","racecar","car"]      →  ""     (no common prefix)
```

**Constraints:** `1 <= strs.length <= 200` · `0 <= strs[i].length <= 200` · lowercase English letters

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**prefix**" | Anchored at index 0. Not a substring, not a subsequence — it starts at the front or it doesn't count |
| "**common** … amongst an array" | It must hold for **every** string. One dissenter kills it — which makes this an *intersection*, not a search |
| "**longest**" | Prefixes are nested: if `"fl"` is common then so is `"f"`. So the answers form a chain, and you want the deepest link that survives |
| "return `""` if none" | The empty string is always a valid common prefix, so there's **no failure case** — the answer is just 0 in the worst case |
| `strs[i]` can be **length 0** | An empty string in the input forces the answer to `""` immediately. Your code must not crash or loop forever on it |
| `strs.length >= 1` | You never get an empty array, so `strs[0]` is always safe to touch |

The structural insight: the answer can never be longer than the **shortest** string in the array, and it can only ever **shrink** as you look at more strings. That monotonicity is what makes a simple, greedy, non-backtracking loop correct.

🤔 **Before you open the next section:** if you started by *assuming* the whole first string is the answer, what's the only operation you'd ever need to perform on your candidate as you scan the rest?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

Let n = number of strings, m = length of the shortest string.

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| **Horizontal scan** | Assume `strs[0]` is the answer; shrink it against each next string | O(n·m) | ✅ Shortest code, no index bookkeeping |
| Vertical scan | Compare character `i` across *all* strings, then `i+1`, … | O(n·m) | ✅ Equally good; exits earlier on a mismatch at position 0 |
| Sort, compare ends | Sort lexicographically, compare only first and last | O(n·m·log n) | ⚠️ Cute and correct, but you added a sort for nothing |
| Divide and conquer | Split, solve halves, intersect the two results | O(n·m) | ⚠️ Same bound, much more machinery |
| [Trie](../data-structures/trie.md) | Insert all, walk down while exactly one child and no word ends | O(n·m) | ⚠️ Right answer, wildly over-built for one query |

**The decision: the horizontal scan.**

Two properties make it work, and both are worth saying out loud:

1. **The answer is bounded by `strs[0]`.** The common prefix must be a prefix of *every* string, so it is certainly a prefix of the first one. Starting there costs nothing and gives you a concrete candidate to attack.
2. **The candidate only ever shrinks.** Each new string can invalidate characters but can never add them back — so one pass with no backtracking is enough.

**Why not sort?** Sorting works because lexicographic order puts the most-different strings at the two ends, so the first and last string bracket everything between them. It's a genuinely clever observation and worth *mentioning* — but you've paid a log n factor to avoid a loop you were going to write anyway.

**Why not a trie?** A trie is the right answer when you'll ask **many** prefix questions about the same word set — see [Implement Trie](208-implement-trie-prefix-tree.md). Building an entire tree to answer one question is a bad trade, and interviewers read it as pattern-matching rather than thinking.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
if not strs:
    return ""
```

A guard the constraints don't strictly require (`strs.length >= 1`), but it costs one line and makes the function total — safe on any input, not just LeetCode's.
→ [truthy-falsy-values](../syntax/truthy-falsy-values.md)

```python
prefix = strs[0]
```

**The optimistic start.** Assume the entire first string is the answer, then let the other strings chip away at it. This is the whole strategy in one line: begin with the largest thing that *could* be right, and shrink toward the truth.
→ [list-basics](../syntax/list-basics.md)

```python
for i in range(1, len(strs)):
```

Start at **1**, not 0 — string 0 is already baked into `prefix`, and testing it against itself is guaranteed to pass.
→ [range-function](../syntax/range-function.md)

```python
    while not strs[i].startswith(prefix):
        prefix = prefix[:-1]
```

The engine. While the current string does **not** begin with our candidate, chop the last character off the candidate and ask again.

`while`, not `if` — one string can invalidate many characters at once. Against `"flight"`, the candidate `"flower"` has to shrink four times (`flowe` → `flow` → `flo` → `fl`) before it fits.

`prefix[:-1]` is "everything except the final character" — the standard Python idiom for shortening from the right.
→ [while-loop](../syntax/while-loop.md) · [string-methods](../syntax/string-methods.md) · [list-slicing](../syntax/list-slicing.md)

```python
        if not prefix:
            return ""
```

**The early exit.** Once the candidate is empty, no future string can make it longer — the answer is locked in. Returning here skips the remaining strings entirely.

It's also what keeps the `while` loop safe: `""` is a prefix of every string, so `startswith("")` is always `True` and the loop would terminate anyway. But bailing out immediately is both faster and clearer about the intent.
→ [if-return](../syntax/if-return.md)

```python
return prefix
```

Survived every string ⇒ it's common to all of them.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:

        if not strs:
            return ""

        prefix = strs[0]

        for i in range(1, len(strs)):
            while not strs[i].startswith(prefix):

                prefix = prefix[:-1]
                if not prefix:
                    return ""

        return prefix
```

</details>

**Trace it** — `strs = ["flower", "flow", "flight"]`:

| `i` | string | `prefix` on entry | Shrink steps | `prefix` after |
|---|---|---|---|---|
| 1 | `"flow"` | `"flower"` | `flowe` → `flow` ✅ | `"flow"` |
| 2 | `"flight"` | `"flow"` | `flo` → `fl` ✅ | `"fl"` |

Return `"fl"`.

And the no-prefix case, `strs = ["dog", "racecar", "car"]`:

| `i` | string | `prefix` on entry | Shrink steps | Result |
|---|---|---|---|---|
| 1 | `"racecar"` | `"dog"` | `do` → `d` → `""` | early `return ""` |

Note it never even looks at `"car"` — the early exit paid for itself.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n · m)</summary>

**O(n · m)**, where n is the number of strings and m is the length of the shortest string. Equivalently: **O(S)**, where S is the total number of characters across all input — you can't beat that, since a correct answer requires looking at every string at least once.

Where it comes from:

- The `for` loop runs n − 1 times.
- Inside, `startswith(prefix)` costs O(len(prefix)) ≤ O(m).
- The `while` shrinks `prefix` — and here's the key: **`prefix` never grows back.** Across the *entire* run it can shrink at most m times in total, not m times per iteration.

So the shrinking is O(m) summed over everything, and the comparisons are O(n·m). Total: **O(n · m)**.

**Say it out loud like this:** *"Nested loops, but the inner one only ever shortens a candidate that never regrows — so total shrinking work is bounded by m, and the cost is dominated by the n comparisons of length ≤ m."*

**Best case** is O(n): if the first characters already disagree, every `startswith` fails fast and `prefix` collapses to `""` on the first string.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(m)</summary>

**O(m)** — or **O(1) auxiliary**, depending on how you count the output.

`prefix` is the only thing allocated, and it's at most as long as the shortest string. Since `prefix` *is* the return value, many people call this O(1) extra space — you're not using memory beyond what the answer itself requires.

The one Python-specific wrinkle worth knowing: strings are [immutable](../syntax/string-immutability.md), so `prefix = prefix[:-1]` **builds a new string** rather than truncating in place. That's an O(m) allocation each time it runs. It doesn't change the asymptotic answer, but if an interviewer pushes on constant factors, the fix is to track an integer length and slice once at the end:

```python
length = len(prefix)
while not strs[i].startswith(prefix[:length]):
    length -= 1
```

...or better, switch to the vertical scan, which never allocates at all until the final slice.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The common prefix has to be a prefix of the first string, so I'll start by assuming `strs[0]` is the whole answer and shrink it. For each remaining string, while it doesn't start with my candidate, I chop a character off the end. The candidate only ever shrinks, so one pass with no backtracking is correct — and if it hits empty I can return immediately, since nothing can lengthen it again. O(n·m) time where m is the shortest length, O(m) space for the candidate."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Do it without shrinking a string." | Vertical scan: fix a character index `i`, compare `strs[0][i]` against every string's `i`-th char, stop at the first mismatch or when any string ends. Same O(n·m), zero allocation. |
| "What if you had to answer this repeatedly for many subsets?" | Build a [trie](../data-structures/trie.md) once, then each query is a walk down from the root while there's exactly one child. Amortizes the build cost across queries. |
| "Longest common **suffix**?" | Reverse every string, run this unchanged, reverse the result. |
| "Longest common **substring** (not anchored)?" | Completely different and much harder — [DP](../algorithms/dynamic-programming.md) over pairs, or suffix automata. Say so; don't pretend it's a tweak. |
| "Why does sorting work?" | Lexicographic order puts the two most-different strings at the ends, so `strs[0]` and `strs[-1]` bracket everything. Compare just those two. O(n·m·log n) — correct but slower. |
| "Can you parallelize it?" | Yes — divide and conquer: prefix of the left half, prefix of the right half, then intersect the two. Same total work, splits cleanly across workers. |

**Traps:**

- **Using `if` instead of `while`.** One string can invalidate several characters at once; a single chop leaves the candidate too long and the answer wrong.
- **Forgetting the empty-candidate exit** and then indexing `prefix[0]` on an empty string — `IndexError`. (`startswith` itself is safe, but hand-rolled character comparisons are not.)
- **An empty string in the input.** `["", "abc"]` must return `""`. The `while` handles it correctly — `startswith` on `""` fails until the candidate is empty — but hand-written index loops often walk off the end.
- **Starting the loop at `i = 0`.** Harmless but wasted work, and it signals you didn't think about why index 0 is special.
- **Assuming `strs[0]` is the shortest.** It isn't, and it doesn't need to be — the shrinking handles it. But don't write code that *depends* on it.

**This same move shows up in:** [Valid Anagram](242-valid-anagram.md) (comparing strings by structure rather than searching) · [Implement Trie](208-implement-trie-prefix-tree.md) (the same prefix relationship, made into a data structure) · [Encode and Decode Strings](271-encode-and-decode-strings.md) (character-level reasoning about string boundaries).

</details>

---
