# 139. Word Break

**Medium** · [LeetCode](https://leetcode.com/problems/word-break/)

[📖 14. 1-D Dynamic Programming lesson](../learning/14-dp-1d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 14. 1-D Dynamic Programming problems](../rmap-practice/14-dp-1d.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Given a string `s` and a dictionary `wordDict`, return `true` if `s` can be **segmented** into a space-separated sequence of one or more dictionary words. The same word may be **reused any number of times**.

```
s = "leetcode",  wordDict = ["leet","code"]          →  true    "leet code"
s = "applepenapple", wordDict = ["apple","pen"]      →  true    "apple pen apple" — "apple" reused
s = "catsandog", wordDict = ["cats","dog","sand","and","cat"]  →  false
```

**Constraints:** `1 <= s.length <= 300` · `1 <= wordDict.length <= 1000` · `1 <= wordDict[i].length <= 20` · all dictionary words are **unique** · lowercase English letters only.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "return **true/false**" | A **feasibility** question, not counting and not optimizing. The combining operator is `or` — one working split is enough |
| "segmented into a sequence of words" | You're choosing **split points**. With n−1 possible gaps, that's 2ⁿ⁻¹ ways to cut the string |
| "may be **reused** any number of times" | Unbounded — no need to track which words you've spent. That keeps the state one-dimensional, same as [Coin Change](322-coin-change.md) |
| dictionary words are **unique** | A `set` loses nothing and buys O(1) lookup |
| word length `<= 20` | A useful bound: from any position only 20 prefixes are worth testing, not all n |
| `n <= 300`, dict size `<= 1000` | O(n²·m) ≈ 300² × 1000 is on the high side; O(n² ) or O(n·m·L) is comfortable |

Example 3 is the one to study. `"catsandog"` with `["cats","dog","sand","and","cat"]` — it looks segmentable. `"cats"` + `"and"` leaves `"og"`. Dead end. Back up: `"cat"` + `"sand"` leaves `"og"`. Dead end again. **A greedy left-to-right match fails**, because the right first word depends on what happens much later.

That's the DP signal, and now the standard question: stand at position `i` and ask about the **first word**.

If `s[i:]` can be segmented, then some dictionary word matches at position `i`, and the **remainder after it** can also be segmented. Try every word:

```
canBreak(i) = OR over words w of
                  ( s starts with w at position i  AND  canBreak(i + len(w)) )
```

Compare to [Coin Change](322-coin-change.md): there, `amount` was consumed by coins; here, the string is consumed by words. Same unbounded structure. The difference is that coins subtract a value while words must *match characters* — so each branch has a verification step attached.

🤔 **Before you open the next section:** what should `canBreak(n)` be — can the empty remainder be segmented? Compare your reasoning to `ways("") = 1` in [Decode Ways](91-decode-ways.md). What goes wrong if you say `False`?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Greedy longest-match | At each position take the longest matching word | O(n·m) | O(1) | ❌ **Wrong.** `"catsandog"` — `"cats"` looks right and dead-ends; the correct first word can only be known later |
| Backtracking, no memo | Try every word at every position, recurse | **O(2ⁿ)** | O(n) | ❌ Exponential. `"aaaa…a"` with `["a","aa","aaa"]` is the killer input |
| Backtracking + memo | Same, cached by index | O(n²·m) | O(n) + stack | ⚠️ Correct; recursion up to 300 deep |
| **Bottom-up DP array** | `dp[i]` = "is `s[i:]` breakable?", filled from the end | O(n²·m) | O(n + dict) | ✅ |
| DP + [trie](../data-structures/trie.md) | Walk a trie of the dictionary from each position | O(n² + dict) | O(dict) | ✅ Better constant; the right answer for a huge dictionary |

**The decision:** **bottom-up DP** over an array of suffix positions.

**Why greedy fails, concretely.** `"catsandog"`: matching longest-first gives `"cats"` → `"andog"` → `"and"` → `"og"` ✗. Matching shortest-first gives `"cat"` → `"sandog"` → `"sand"` → `"og"` ✗. Both fail, and the answer really is `false` — but greedy would also fail on `"catsanddog"` where the answer *is* `true`, because the correct choice of first word depends on the entire rest of the string. **A local match tells you nothing about global feasibility.**

**Why the subproblems overlap.** From `"applepenapple"`, both `"apple"`-first and (hypothetically) other paths converge on the same suffixes. Position 5 gets asked about repeatedly along different branches. There are only **n+1 distinct suffixes**, so caching turns 2ⁿ into O(n·something).

**Why the state is one-dimensional.** Because words are reusable and you always consume a prefix of the remaining string, the only thing describing a subproblem is **where you are**. Not which words you've used, not how many. Exactly the [Coin Change](322-coin-change.md) situation — and exactly why it's *not* a 2-D DP.

**Why bottom-up over memoized recursion?** Same complexity, no stack. n = 300 wouldn't overflow Python's limit, so this is a milder preference here than in Coin Change — but the iterative version is still easier to reason about, and the base case sits visibly at the top.

**The base case, answering section 1's question: `dp[n] = True`.** The empty remainder *is* segmentable — into zero words. If you set it `False`, every chain terminates in failure and the answer is always `false`. It's the same "reaching the end is success" seed as [Decode Ways](91-decode-ways.md), and it's the value the entire array is built from.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
word_set = set(wordDict)
n = len(s)
```
Converting the list to a [set](../data-structures/hashset.md) gives **O(1) average membership**, which matters because the dictionary is consulted at every position. (In this particular implementation the set is *iterated* rather than searched, so the win is smaller — but it also deduplicates and it's the form you'd want if you switched to the prefix-lookup variant.)
→ [set-basics](../syntax/set-basics.md) · [hashset](../data-structures/hashset.md)

```python
dp = [False] * (n + 1)
dp[n] = True   # empty remainder is always breakable
```
`dp[i]` answers *"can `s[i:]` be segmented?"* — one slot per position **plus one** for the empty suffix, hence `n + 1`.

Everything starts `False` (assume not breakable until proven), and `dp[n] = True` is the seed: **the empty string is breakable into zero words.** This single value is what the whole array is built from — flip it to `False` and the function returns `false` for every input.
→ [list-basics](../syntax/list-basics.md) · [boolean-basics](../syntax/boolean-basics.md)

```python
for i in range(n - 1, -1, -1):
```
Walk **backwards** from the last character to position 0. Backwards because `dp[i]` depends on `dp[i + len(word)]`, which is always to the *right* — so it must already be computed.
→ [range-function](../syntax/range-function.md) · [for-loop](../syntax/for-loop.md)

```python
    for word in word_set:
```
Try **every** dictionary word as the first word of `s[i:]`. No greedy shortcut — as example 3 shows, you can't tell which is right without checking what follows.
→ [for-loop](../syntax/for-loop.md)

```python
        if i + len(word) <= n and s[i:i + len(word)] == word and dp[i + len(word)]:
```
**Three conditions, in a deliberate order**, connected by [`and`](../syntax/logical-operators.md) so each short-circuits the next:

1. `i + len(word) <= n` — **does the word even fit** in the remaining string? Cheapest check, so it goes first. Without it you'd slice past the end (harmless in Python, but it would compare a short slice against a longer word and quietly fail) and index `dp` out of range.
2. `s[i:i + len(word)] == word` — **does it actually match** at this position? This is the string-verification step that [Coin Change](322-coin-change.md) doesn't have.
3. `dp[i + len(word)]` — **is the remainder breakable?** The recursive part. Already computed, because you're going backwards.

All three must hold. Ordering them cheapest-first isn't just tidiness — it's what keeps the O(n) slice from running when the word obviously doesn't fit.
→ [logical-operators](../syntax/logical-operators.md) · [list-slicing](../syntax/list-slicing.md) · [string-join-slice](../syntax/string-join-slice.md)

```python
            dp[i] = True
            break
```
One working first word is enough — this is an **existence** question, so [`break`](../syntax/break-continue.md) out immediately rather than testing the remaining words. That's the `or` semantics from section 1, and it's a real saving on strings that segment easily.
→ [break-continue](../syntax/break-continue.md) · [dynamic-programming](../algorithms/dynamic-programming.md)

```python
return dp[0]
```
"Can `s[0:]` — the whole string — be segmented?"
→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:

        word_set = set(wordDict)
        n = len(s)
        dp = [False] * (n + 1)
        dp[n] = True   # empty remainder is always breakable

        for i in range(n - 1, -1, -1):
            for word in word_set:
                if i + len(word) <= n and s[i:i + len(word)] == word and dp[i + len(word)]:
                    dp[i] = True
                    break

        return dp[0]
```
</details>

**Trace it** — `s = "leetcode"` (n = 8), `wordDict = ["leet", "code"]`

`dp` starts as `[F,F,F,F,F,F,F,F,T]` — index 8 is the seed.

| `i` | `s[i:]` | tries | result |
|---|---|---|---|
| 7 | `"e"` | neither word fits | `dp[7] = False` |
| 6 | `"de"` | neither fits | `False` |
| 5 | `"ode"` | neither fits | `False` |
| 4 | `"code"` | `"code"` matches, `dp[8]` = **True** ✓ | **`dp[4] = True`** |
| 3 | `"tcode"` | `"code"` doesn't match at 3 | `False` |
| 2 | `"etcode"` | no match | `False` |
| 1 | `"eetcode"` | no match | `False` |
| 0 | `"leetcode"` | `"leet"` matches, `dp[0+4] = dp[4]` = **True** ✓ | **`dp[0] = True`** |

Return **true** ✅ — and notice the chain: `dp[0]` is true *because* `dp[4]` was already true, which was true because of the `dp[8]` seed. The whole answer traces back to "the empty string is breakable."

**And `s = "catsandog"` (n = 9)**, dict `["cats","dog","sand","and","cat"]`:

| `i` | `s[i:]` | tries | result |
|---|---|---|---|
| 7 | `"og"` | nothing matches | `False` |
| 6 | `"dog"` | `"dog"` matches, `dp[9]` = **True** ✓ | **`dp[6] = True`** |
| 5 | `"ndog"` | no match | `False` |
| 4 | `"andog"` | `"and"` matches → needs `dp[7]` = **False** ✗ | `False` |
| 3 | `"sandog"` | `"sand"` matches → needs `dp[7]` = **False** ✗ | `False` |
| 0 | `"catsandog"` | `"cat"` → `dp[3]` = False ✗; `"cats"` → `dp[4]` = False ✗ | **`dp[0] = False`** |

Return **false** ✅

Rows 4 and 3 are the point. `"and"` and `"sand"` both *match* — a greedy matcher would happily take either — but both lead to `dp[7]`, and position 7 leaves the unbreakable `"og"`. The DP checks the consequence before accepting the match; greedy doesn't.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n² · m)</summary>

**O(n² · m)** in the general bound, where n = `len(s)` and m = the number of dictionary words.

- The outer loop runs **n** times.
- The inner loop runs **m** times.
- Each iteration does a slice-and-compare of up to `len(word)` characters — **O(n)** in the general case.
- n × m × O(n) = **O(n² · m)**.

**But the constraints tighten it substantially.** Word length is capped at **20**, so the slice-and-compare is O(20) = O(1), and the real bound is **O(n · m · L)** with L ≤ 20 → 300 × 1000 × 20 = 6 × 10⁶. Fast. Quoting the loose n²·m bound and then noting the L cap is the more accurate answer.

**Against the alternatives:** unmemoized backtracking is **O(2ⁿ)** — the classic killer being `s = "aaaa…ab"` with `["a","aa","aaa"]`, where every split is explored and every one fails at the last character. Memoization brings it to the same O(n²·m) as this, because there are only n+1 distinct suffixes.

**The better variant:** instead of iterating all m words at each position, iterate the **lengths** — check `s[i:j]` against the set for each `j` up to `i + 20`. That's **O(n · L)** set lookups, or with a [trie](../data-structures/trie.md), walk characters from `i` and stop as soon as no word shares the prefix: **O(n²)** worst case with a much better constant, and clearly better when the dictionary is large.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n + total dictionary size)</summary>

**O(n + D)**, where D is the total number of characters across all dictionary words.

- `dp` — an array of `n + 1` booleans → **O(n)**.
- `word_set` — holds every word → **O(D)**. With the given limits that's up to 1000 × 20 = 20,000 characters.
- The slice `s[i:i + len(word)]` allocates a transient string of at most 20 characters → **O(1)**.
- No recursion, so no stack.

**Why this can't collapse to O(1)** like [Climbing Stairs](70-climbing-stairs.md) or [House Robber](198-house-robber.md): `dp[i]` reads `dp[i + len(word)]` for **every** word, and words vary in length up to 20. So the lookback window is bounded by `max(word length)` rather than being a fixed 2 — which means you could technically keep just the last 20 entries in a rolling buffer for **O(20) = O(1)** space, since word length is capped.

That's a genuinely correct optimization here, unlike in [Coin Change](322-coin-change.md) where coin values are unbounded. Worth mentioning; not worth writing, since the O(n) array is clearer and n is only 300.

**What you'd need extra state for:** returning the actual segmentation ([Word Break II](https://leetcode.com/problems/word-break-ii/)) requires storing which word succeeded at each position — and listing *all* segmentations can be exponentially large, so that's a backtracking problem rather than a DP one.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Greedy matching doesn't work — with `"catsandog"`, both `"cat"` and `"cats"` match at the start and both dead-end, so the right first word depends on the whole rest of the string. So I ask: can `s[i:]` be segmented? Yes, if some dictionary word matches at position i *and* the remainder after it can also be segmented. Words are reusable and I always consume a prefix, so the only state is the position — one-dimensional, same shape as Coin Change. I fill the array backwards since `dp[i]` depends on positions to its right, and the base case is `dp[n] = True`: the empty remainder is segmentable into zero words. That seed is what everything else is built from. It's a feasibility question, so one match is enough and I break early. O(n·m·L) with L capped at 20, and O(n + dictionary) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why is `dp[n] = True`?" | The empty string is segmentable into zero words — reaching the end means you consumed everything successfully. Set it `False` and every chain terminates in failure, so the answer is always `false`. |
| "Why doesn't greedy work?" | `"catsandog"` — `"cats"` and `"cat"` both match at position 0 and both dead-end. Feasibility of a first word depends on the entire remainder, which is not knowable locally. |
| "Return the actual segmentation." | Store the winning word at each position and walk forward from 0. Returning *all* segmentations is [Word Break II](https://leetcode.com/problems/word-break-ii/) — exponential output, so backtracking with memoized suffix results. |
| "Optimize for a huge dictionary." | Build a [trie](../data-structures/trie.md) and walk it character by character from each position, stopping as soon as no word shares the prefix. Avoids testing words that can't possibly match. |
| "Iterate lengths instead of words?" | Yes, and it's usually better: for each `j` from `i+1` to `i+20`, check `s[i:j] in word_set`. That's O(n · 20) lookups and doesn't scale with dictionary size. |
| "What if words could *not* be reused?" | Now you'd need to track which words are spent — the state stops being one-dimensional, and it becomes a much harder (bitmask or matching) problem. |
| "Can you do it forwards?" | Yes — define `dp[i]` = "are the first i characters breakable", with `dp[0] = True`, and `dp[i] = any(dp[j] and s[j:i] in word_set)`. Equivalent; the base case just moves to the front. |
| "Worst case input?" | `s = "aaaa…aab"` with `["a","aa","aaa"]` — everything matches, nothing completes. It's what makes unmemoized recursion blow up and what proves the DP necessary. |

**Traps:**
- **Seeding `dp[n] = False`** (or forgetting to seed it). The answer is then always `false`.
- **Omitting the `i + len(word) <= n` bounds check.** Slicing past the end is silent in Python, but `dp[i + len(word)]` raises `IndexError` — or worse, with a negative-ish index, reads the wrong entry.
- **Checking only that the word matches**, without also checking `dp[i + len(word)]`. That's greedy in disguise, and `"catsandog"` catches it.
- Sizing `dp` as `n` instead of `n + 1` — no room for the base case.
- Iterating forwards while using a suffix-based recurrence. The dependency direction must match the fill order.
- Forgetting the `break`. Correct but wasteful — and it signals you haven't noticed this is an existence question.

**This same move shows up in:** [Coin Change](322-coin-change.md) (the same unbounded consume-a-piece structure, minimizing instead of testing feasibility) · [Decode Ways](91-decode-ways.md) (suffix DP over a string with guarded branches, counting instead of testing) · [Palindrome Partitioning](131-palindrome-partitioning.md) (splitting a string at valid boundaries, enumerating rather than deciding) · [Implement Trie](208-implement-trie-prefix-tree.md) (the structure that makes the dictionary lookups fast).

</details>

---
