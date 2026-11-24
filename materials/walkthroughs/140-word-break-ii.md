# 140. Word Break II

**Hard** · [LeetCode](https://leetcode.com/problems/word-break-ii/) · [Solution file (no hints)](../../problems/0001-0499/140.py)

[📖 10. Backtracking lesson](../learning/10-backtracking.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 10. Backtracking problems](../rmap-practice/10-backtracking.md)

---

Given a string `s` and a dictionary `wordDict`, **insert spaces** into `s` to form sentences in which every word is in the dictionary. Return **all** such sentences, in any order. A dictionary word may be reused.

```
s = "catsanddog",  wordDict = ["cat", "cats", "and", "sand", "dog"]
→ ["cats and dog", "cat sand dog"]

s = "pineapplepenapple",  wordDict = ["apple", "pen", "applepen", "pine", "pineapple"]
→ ["pine apple pen apple", "pineapple pen apple", "pine applepen apple"]

s = "catsandog",  wordDict = ["cats", "dog", "sand", "and", "cat"]   →  []
```

**Constraints:** `1 <= s.length <= 20` · `1 <= wordDict.length <= 1000` · `1 <= word.length <= 10` · lowercase letters · dictionary words are unique

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "return **all** sentences" | Not yes/no: you must **enumerate** every valid segmentation (backtracking) |
| words can be reused | No "used" bookkeeping. Any word can follow any other |
| "insert spaces" | A segmentation is a list of cut points. Each piece must be a dictionary word |
| `s.length <= 20` | The number of answers can be large (exponential), so the output is the limit |
| returns `[]` if none | Dead ends must produce empty results, not errors |

This is [Word Break](139-word-break.md) (a yes/no DP) upgraded to list the answers. The recursion is the natural one: from position `start`, try every word `s[start:end]` that's in the dictionary, and then segment the rest.

**The danger is repetition.** The suffix starting at index 5 may be reachable by many different earlier choices, and each time you'd re-solve it. **Memoise on `start`**: store the full list of sentences for `s[start:]`. The first call does the work, and later calls reuse it.

🤔 **Before you open the next section:** what should `helper(len(s))` (the empty suffix) return, so the sentences get built correctly by the caller?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Time | Verdict |
|---|---|---|
| Plain backtracking from `start` | exponential, with repeated work on shared suffixes | ⚠️ Correct, but can blow up on strings like `aaaa…` |
| **Backtracking + memo on `start`** | output-sensitive: each suffix solved once | ✅ |
| Boolean DP first, then backtrack only through feasible positions | prunes dead ends | ✅ Useful when many prefixes can't be completed |

**The decision: top-down recursion with memoisation, where `helper(start)` returns the list of every sentence that can be made from `s[start:]`.** It's [backtracking](../algorithms/backtracking.md) and [DP](../algorithms/dynamic-programming.md) together: the recursion enumerates, the memo stops re-enumeration.

The recursion: for each `end` where `s[start:end]` is a word, take each sentence in `helper(end)` and put the word in front of it. The empty suffix returns `[""]`, a list with **one empty sentence**, so words at the end of `s` attach cleanly with no trailing space.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
words = set(wordDict)
memo = {}
```

A set makes the "is it a word?" test O(1) average. `memo[start]` will hold the list of sentences for `s[start:]`.
→ [set-basics](../syntax/set-basics.md) · [dict-basics](../syntax/dict-basics.md) · [functools-cache](../syntax/functools-cache.md)

```python
def helper(start: int) -> List[str]:
    if start in memo:
        return memo[start]
    if start == len(s):
        return [""]
```

Return a cached answer if there is one. **Base case:** past the end of the string there's exactly one way to finish, the empty sentence `""`. (Returning `[]` would mean "impossible" and would kill every valid answer.)
→ [membership-operators](../syntax/membership-operators.md) · [recursion-basics](../syntax/recursion-basics.md) · [closures](../syntax/closures.md)

```python
    result = []
    for end in range(start + 1, len(s) + 1):
        word = s[start:end]
        if word in words:
```

Try every prefix of the remaining string. Only prefixes that are dictionary words continue.
→ [for-loop](../syntax/for-loop.md) · [list-slicing](../syntax/list-slicing.md)

```python
            for rest in helper(end):
                if rest == "":
                    result.append(word)
                else:
                    result.append(word + " " + rest)
```

Combine the word with each sentence for the rest. When `rest` is the empty sentence the word is last, so add no space. Otherwise join with one space.
→ [string-join-slice](../syntax/string-join-slice.md) · [elif-else](../syntax/elif-else.md)

```python
    memo[start] = result
    return result

return helper(0)
```

Cache **before** returning, so any later path to this suffix is instant. A dead end stores `[]`, which also memoises *failure*.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> List[str]:
        words = set(wordDict)
        memo = {}

        def helper(start: int) -> List[str]:
            if start in memo:
                return memo[start]
            if start == len(s):
                return [""]

            result = []
            for end in range(start + 1, len(s) + 1):
                word = s[start:end]
                if word in words:
                    for rest in helper(end):
                        if rest == "":
                            result.append(word)
                        else:
                            result.append(word + " " + rest)

            memo[start] = result
            return result

        return helper(0)
```

</details>

**Trace it.** `s = "catsanddog"`, words `cat, cats, and, sand, dog`:

| Call | Words that match here | Result |
|---|---|---|
| `helper(7)` (`"dog"`) | `dog` → `helper(10) = [""]` | `["dog"]` |
| `helper(3)` (`"sanddog"`) | `sand` → `helper(7)`: `["sand dog"]`. (`and` starts at 4, not 3) | `["sand dog"]` |
| `helper(4)` (`"anddog"`) | `and` → `helper(7)`: `["and dog"]` | `["and dog"]` |
| `helper(0)` | `cat` → `helper(3)`: `"cat sand dog"`; `cats` → `helper(4)`: `"cats and dog"` | `["cat sand dog", "cats and dog"]` ✅ |

`helper(7)` is reached from two different routes and computed only once.

</details>

<details>
<summary><b>4 · Time complexity</b> — output-sensitive, O(n² + total output)</summary>

Without memoisation the work is exponential, and the *output itself* can be exponential, since a string like `"aaaa…a"` with words `a, aa, aaa, …` has exponentially many sentences. With memoisation each suffix is expanded once: **O(n²)** substring checks, plus the cost of building every output sentence. You can't beat the size of the answer.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(total output)</summary>

The memo stores the sentence list for every suffix: bounded by the sum of all those lists' sizes. The recursion depth is at most `n`. If many answers exist, this dominates.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "I need every segmentation, so I recurse from a start index: for each prefix that is a dictionary word, I recurse on the rest and prepend the word to every sentence it returns. The empty suffix returns a list containing one empty sentence so the last word attaches without a trailing space. Many prefixes lead to the same suffix, so I memoise on the start index, storing the full list of sentences for that suffix. That's backtracking with DP caching. The work is bounded by the output size, which can be exponential."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Faster when there's no answer?" | Run [Word Break](139-word-break.md)'s boolean DP first and return `[]` immediately if `s` can't be segmented. Otherwise the recursion may explore huge dead ends |
| "Avoid building the strings repeatedly?" | Build lists of words and join at the end, or only memoise feasibility and reconstruct paths |
| "Use a trie?" | Yes: walk the trie from `start` and only continue while a prefix exists. Saves scanning every `end` |
| "Why return `[""]`, not `[]`, at the end?" | `[]` means "no sentence possible" and would erase valid ones. `[""]` means "one way: nothing left to add" |
| "Related?" | [Word Break](139-word-break.md) · [Extra Characters in a String](2707-extra-characters-in-a-string.md) · [Palindrome Partitioning](131-palindrome-partitioning.md) (another "list every cut") |

**Traps:**

- **Returning `[]` for the empty suffix.** Every answer disappears.
- **A trailing or leading space** from joining `word + " " + rest` when `rest` is empty.
- **No memo.** It passes small examples and times out on `aaaa…`.
- **Forgetting that failure is cacheable too.** Store `[]` for dead-end suffixes.

**This same move shows up in:** [Word Break](139-word-break.md) · [Palindrome Partitioning](131-palindrome-partitioning.md) · [Letter Combinations of a Phone Number](17-letter-combinations-of-a-phone-number.md) (generate all combinations).

</details>

---
