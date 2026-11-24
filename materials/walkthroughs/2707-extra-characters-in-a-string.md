# 2707. Extra Characters in a String

**Medium** · [LeetCode](https://leetcode.com/problems/extra-characters-in-a-string/) · [Solution file (no hints)](../../problems/2500-2999/2707.py)

[📖 08. Tries lesson](../learning/08-tries.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 08. Tries problems](../rmap-practice/08-tries.md)

---

Given a string `s` and a list of words `dictionary`, break `s` into **non-overlapping substrings**, each either a word from the dictionary or an "extra" leftover character. Return the **minimum number of extra characters**.

```
s = "leetscode",  dictionary = ["leet", "code", "leetcode"]   →  1
    "leet" + (s) + "code"      the 's' is the one extra character

s = "sayhelloworld",  dictionary = ["hello", "world"]         →  3
    "say" are extras, then "hello", "world"
```

**Constraints:** `1 <= s.length <= 50` · `1 <= dictionary.length <= 50` · `1 <= dictionary[i].length <= 50` · lowercase letters · words are distinct

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "non-overlapping substrings" | A **partition** of `s` into pieces, left to right |
| each piece is a word or extra characters | Every position is either covered by a dictionary word or counted as 1 extra |
| "minimum extras" | Optimisation over many ways to cut: **DP** |
| `n <= 50` | Small: an `O(n²)` DP with substring checks is fine |

This is [Word Break](139-word-break.md) with an optimisation twist. Word Break asks *can* the whole string be covered. Here a position can always be skipped at a cost of 1, so the question becomes *how cheaply*.

**State:** `dp[i]` = the minimum extra characters in the **first `i` characters** `s[:i]`. The answer is `dp[n]`.

**Transitions** for each end position `i`:

- **Skip character `i-1`:** `dp[i] = dp[i-1] + 1`.
- **End a dictionary word at `i`:** for any start `j < i` where `s[j:i]` is a word, `dp[i] = min(dp[i], dp[j])` (the word costs nothing).

🤔 **Before you open the next section:** what's `dp[0]`, and why does it have to be 0?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Time | Space | Verdict |
|---|---|---|---|
| Brute force over every cut (recursion) | O(2ⁿ) | O(n) | ❌ Same subproblems repeat |
| Top-down memo on the start index | O(n²·L) | O(n) | ✅ Equivalent to the table |
| **Bottom-up [DP](../algorithms/dynamic-programming.md) with a `set`** | **O(n²·L)**, `L` = word length | **O(n + total dictionary)** | ✅ |
| DP + [trie](../data-structures/trie.md) walk | O(n·L) | O(total dictionary) | ✅ Faster, with more code. This is why the problem sits in the Tries unit |

**The decision: bottom-up DP, with the dictionary in a [hash set](../data-structures/hashset.md).** The set makes "is `s[j:i]` a word?" an O(L) average check (hashing the slice). For `n <= 50` that's tiny.

Mention the trie as the upgrade: instead of slicing every `s[j:i]`, walk the trie from each start `j` and stop as soon as no word has that prefix, which avoids the checks that can't match.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
words = set(dictionary)
n = len(s)
dp = [0] * (n + 1)
```

The set gives O(1)-average membership. `dp[i]` is the best answer for `s[:i]`. `dp[0] = 0` is the empty prefix: zero characters, zero extras. The array has `n + 1` slots so `dp[n]` is the answer.
→ [set-basics](../syntax/set-basics.md) · [list-basics](../syntax/list-basics.md) · [dynamic-programming](../algorithms/dynamic-programming.md)

```python
for i in range(1, n + 1):
    dp[i] = dp[i - 1] + 1
```

Start from the always-available option: the last character is an extra, so it costs one more than the best for the prefix before it.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md)

```python
    for j in range(i):
        if s[j:i] in words:
            dp[i] = min(dp[i], dp[j])
```

Try every possible start `j` for a word ending at `i`. If `s[j:i]` is in the dictionary, we can reach position `i` for the cost of `dp[j]` (the word itself is free). Keep the minimum.
→ [list-slicing](../syntax/list-slicing.md) · [membership-operators](../syntax/membership-operators.md) · [min-max-key](../syntax/min-max-key.md)

```python
return dp[n]
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def minExtraChar(self, s: str, dictionary: List[str]) -> int:
        words = set(dictionary)
        n = len(s)

        dp = [0] * (n + 1)

        for i in range(1, n + 1):
            dp[i] = dp[i - 1] + 1

            for j in range(i):
                if s[j:i] in words:
                    dp[i] = min(dp[i], dp[j])

        return dp[n]
```

</details>

**Trace it.** `s = "leetscode"`, `dictionary = ["leet", "code", "leetcode"]`:

| `i` | prefix | skip option | word ending here | `dp[i]` |
|---|---|---|---|---|
| 0 | `""` | | | 0 |
| 1-3 | `l`, `le`, `lee` | `dp[i-1]+1` | none | 1, 2, 3 |
| 4 | `leet` | 4 | `leet` (j=0): `dp[0] = 0` | **0** |
| 5 | `leets` | `dp[4]+1 = 1` | none | **1** |
| 6-8 | `leetsc…` | 2, 3, 4 | none | 2, 3, 4 |
| 9 | `leetscode` | `dp[8]+1 = 5` | `code` (j=5): `dp[5] = 1` | **1** ✅ |


</details>

<details>
<summary><b>4 · Time complexity</b> — O(n² · L)</summary>

Two nested loops give `n²/2` pairs `(j, i)`. Each does a slice and a hash lookup, both O(L) in the slice length (up to `n`). So **O(n³)** by the crude bound, and **O(n² · L)** if you cap word length. For `n = 50`, that's a few thousand operations.

With a trie, each start `j` walks forward at most `L_max` characters: **O(n · L_max)**.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n + D)</summary>

`dp` is O(n), and the set holds the dictionary: O(D), where `D` is the total number of characters across all words. A trie also costs O(D).

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "I'll define `dp[i]` as the fewest extra characters in the first `i` letters. The base is `dp[0] = 0`. For each `i`, the default is that the last character is extra: `dp[i-1] + 1`. Then I check every start `j`: if `s[j:i]` is a dictionary word, I can reach `i` at the cost of `dp[j]`, so I take the minimum. The answer is `dp[n]`. With a hash set that's O(n²·L) for a tiny `n`. A trie would cut the repeated checks down to O(n·L)."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Use the trie?" | Insert all words. From each start `j`, walk down the trie character by character, and whenever you hit a word end at index `i`, update `dp[i+1]`. Stop when the path leaves the trie |
| "How's it different from Word Break?" | [Word Break](139-word-break.md) asks for a yes/no (boolean DP). This minimises a count, so the DP stores numbers and every position has a "skip" option |
| "Top-down?" | `f(i)` = min extras from `s[i:]`: either `1 + f(i+1)` or `f(j)` for each word `s[i:j]`. Memoise on `i` |
| "Return the actual split?" | Store the choice (parent pointer) for each `i` and walk back from `n` |
| "Longer strings?" | Trie, plus only trying word lengths that exist in the dictionary |

**Traps:**

- **Greedily taking the longest matching word.** `"leetscode"` with `leet`, `leetcode`: greedy may pick wrongly. DP considers all.
- **Forgetting the skip option** `dp[i-1] + 1`. A string with no dictionary matches then has no value.
- **Off-by-one:** `s[j:i]` is exclusive of `i`, which is why `dp` has `n + 1` entries.
- **Setting `dp[0] = 1` or leaving it uninitialised.**

**This same move shows up in:** [Word Break](139-word-break.md) (boolean version) · [Word Break II](140-word-break-ii.md) (return every split) · [Decode Ways](91-decode-ways.md) (a similar left-to-right DP over a string).

</details>

---
