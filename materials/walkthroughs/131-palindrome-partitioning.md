# 131. Palindrome Partitioning

**Medium** · [LeetCode](https://leetcode.com/problems/palindrome-partitioning/)

[📖 10. Backtracking lesson](../learning/10-backtracking.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 10. Backtracking problems](../rmap-practice/10-backtracking.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Given a string `s`, partition it such that **every substring of the partition is a palindrome**. Return **all possible** palindrome partitionings.

```
s = "aab"  →  [["a","a","b"], ["aa","b"]]
              note ["aab"] is not valid — "aab" isn't a palindrome

s = "a"    →  [["a"]]
```

**Constraints:** `1 <= s.length <= 16` · `s` contains only lowercase English letters

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**partition**" | ⚠️ Split into **contiguous** pieces covering the whole string, with no gaps or overlaps |
| "**every** substring is a palindrome" | A validity constraint on each piece — which is what makes pruning possible |
| "**all possible**" partitionings | Enumerate everything → backtracking |
| **`n <= 16`** | ⚠️ Tiny bound. There are 2^(n−1) ways to cut a string, so exponential is expected |
| single characters | Always palindromes, so a valid partitioning always exists |

**The reframe: partitioning is choosing where to cut.** A string of length n has n−1 possible cut positions, each independently taken or not — hence 2^(n−1) partitionings:

```
"aab"     cuts at:  a|a|b     a|ab     aa|b     aab
                     both      first    second    none
```

**But cast recursively it's simpler still.** Standing at position `start`, the only decision is *"where does the next piece end?"* Try every possible end, and if that piece is a palindrome, recurse from there:

```
"aab", start=0
├─ piece "a"   ✅ palindrome → recurse from 1
│  ├─ piece "a"  ✅ → recurse from 2
│  │  └─ piece "b" ✅ → start==3, done → ["a","a","b"] ✅
│  └─ piece "ab" ❌ not a palindrome — prune
├─ piece "aa"  ✅ → recurse from 2
│  └─ piece "b" ✅ → done → ["aa","b"] ✅
└─ piece "aab" ❌ not a palindrome — prune
```

**The palindrome check is a pruning condition, not a final filter.** An invalid piece kills that branch immediately — you never build partitions and then discard them. Same *prune at the branch, don't validate at the leaf* discipline as [Generate Parentheses](22-generate-parentheses.md).

**The structural difference from the earlier problems.** [Subsets](78-subsets.md) chose *which elements* to take; here you choose *where to cut*. But the skeleton is identical — the "choice" is just a substring length instead of an element.

🤔 **Before you open the next section:** the recursion advances by the length of the piece just taken. What does `start` reaching the end of the string tell you?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Verdict |
|---|---|---|
| Enumerate all 2^(n−1) cut patterns, filter | Generate every partitioning, keep the valid ones | ⚠️ Correct, but builds invalid partitions before discarding them |
| **Backtracking with a palindrome check** | Only extend branches whose next piece is valid | ✅ |
| Backtracking + precomputed palindrome table | DP table so `is_palindrome` is O(1) | ✅ The optimization |

**The decision: backtracking over cut positions, recursing only when the piece is a palindrome.**

The structure:

1. **Base case** — `start == len(s)`: the whole string is consumed, so `path` is a complete valid partitioning.
2. **Loop** — try every end position from `start + 1` to `len(s)`.
3. **Prune** — only recurse if `s[start:end]` is a palindrome.
4. **Choose → explore → un-choose** — the familiar skeleton.

**Why `start == len(s)` means success.** Each recursion consumes a prefix, so reaching the end means every character has been placed into exactly one piece — a complete partition with no gaps. **No separate validity check is needed at the base case**, because every piece was validated as it was added.

**Why the loop runs to `len(s) + 1`.** Python slices are end-exclusive, so `s[start:len(s)]` is the piece extending to the very end — and to generate that, `end` must reach `len(s)`. Since `range` is also exclusive, the bound is `len(s) + 1`. **Two off-by-ones cancelling**, and a classic place to slip.

**The pruning matters more than it looks.** In the trace above, `"ab"` and `"aab"` were rejected the moment they were formed — cutting off everything downstream. On a string with few palindromic substrings, most branches die immediately.

**The precomputed-table optimization**, worth naming:

```python
# dp[i][j] = True if s[i:j+1] is a palindrome
dp = [[False] * n for _ in range(n)]
for i in range(n - 1, -1, -1):
    for j in range(i, n):
        if s[i] == s[j] and (j - i < 2 or dp[i + 1][j - 1]):
            dp[i][j] = True
```

That drops each check from O(n) to **O(1)**, at O(n²) space. It's the [2-D DP](../learning/15-dp-2d.md) technique from Unit 14 applied as a preprocessing step — mention it, but at n ≤ 16 the simple check is fine.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
result = []
path = []
```

`result` collects complete partitionings; `path` is the shared list of pieces chosen so far.
→ [list-basics](../syntax/list-basics.md)

```python
def is_palindrome(piece):
    return piece == piece[::-1]
```

**The validity check.** `piece[::-1]` is Python's reverse-slice idiom; a string equal to its reverse is a palindrome.

Concise but **O(k)** in time *and* space for a piece of length k, since the reversal allocates a new string. The two-pointer version from [Valid Palindrome](125-valid-palindrome.md) would be O(1) space — and the DP table would make it O(1) time.
→ [list-slicing](../syntax/list-slicing.md) · [string-basics](../syntax/string-basics.md) · [function-basics](../syntax/function-basics.md)

```python
def backtrack(start):
    if start == len(s):
        result.append(path[:])
        return
```

**Base case: the string is fully consumed.** Every character has been placed into some piece, and every piece was validated on the way in — so this partitioning is complete and correct.

`path[:]` copies, for the usual reason.
→ [recursion-basics](../syntax/recursion-basics.md) · [if-return](../syntax/if-return.md)

```python
    for end in range(start + 1, len(s) + 1):
        piece = s[start:end]
```

**Try every possible end for the next piece.**

- `start + 1` — the shortest piece is one character (slices are end-exclusive).
- `len(s) + 1` — so that `end` can reach `len(s)`, giving the piece that runs to the string's end.

Each iteration considers a different length for the next piece.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md)

```python
        if is_palindrome(piece):
            path.append(piece)
            backtrack(end)
            path.pop()
```

**Prune, then choose → explore → un-choose.**

The palindrome test is the **pruning**: a non-palindromic piece means this branch can't lead to a valid partitioning, so it's abandoned before any recursion happens.

`backtrack(end)` continues from where this piece finished — `end` is both the exclusive end of the current piece and the inclusive start of the next. **That's why no `+1` is needed here**, unlike the index-based problems.

`path.pop()` restores before trying a different piece length.
→ [list-methods](../syntax/list-methods.md)

```python
backtrack(0)
return result
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def partition(self, s: str) -> List[List[str]]:

        result = []
        path = []

        def is_palindrome(piece):
            return piece == piece[::-1]

        def backtrack(start):
            if start == len(s):
                result.append(path[:])
                return

            for end in range(start + 1, len(s) + 1):
                piece = s[start:end]
                if is_palindrome(piece):
                    path.append(piece)
                    backtrack(end)
                    path.pop()

        backtrack(0)
        return result
```

</details>

**Trace it** — `s = "aab"`:

| Call | `end` | `piece` | Palindrome? | Action |
|---|---|---|---|---|
| `backtrack(0)` | 1 | `"a"` | ✅ | append, recurse from 1 |
| ⟶ `backtrack(1)` | 2 | `"a"` | ✅ | append, recurse from 2 |
| ⟶⟶ `backtrack(2)` | 3 | `"b"` | ✅ | append, recurse from 3 |
| ⟶⟶⟶ `backtrack(3)` | — | — | — | `start == 3 == len(s)` → **record `["a","a","b"]`** ✅ |
| ⟶⟶ back | | | | pop `"b"` |
| ⟶ back | 3 | `"ab"` | ❌ | **pruned** |
| back | | | | pop `"a"` |
| `backtrack(0)` | 2 | `"aa"` | ✅ | append, recurse from 2 |
| ⟶ `backtrack(2)` | 3 | `"b"` | ✅ | append, recurse from 3 |
| ⟶⟶ `backtrack(3)` | — | — | — | **record `["aa","b"]`** ✅ |
| back | | | | pop, pop |
| `backtrack(0)` | 3 | `"aab"` | ❌ | **pruned** |

Result: `[["a","a","b"], ["aa","b"]]` ✅

Two branches were pruned — `"ab"` and `"aab"` — and neither wasted any recursion. On longer strings with few palindromic substrings, that pruning eliminates the vast majority of the 2^(n−1) cut patterns.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n · 2ⁿ)</summary>

**O(n · 2ⁿ)**.

- **Up to 2^(n−1) partitionings** — each of the n−1 gaps is independently a cut or not.
- **O(n) per partitioning** to copy `path` into the result.
- **O(n) per palindrome check**, and there are O(n) checks per level.

The standard stated bound is **O(n · 2ⁿ)**.

At n = 16 that's 16 × 32,768 ≈ **5·10⁵** — instant. The constraint confirms exponential is expected.

**Why the true cost is much lower.** The palindrome check prunes branches before they're explored. A string like `"abcdefgh"` has almost no palindromic substrings beyond single characters, so only *one* partitioning exists and nearly every branch dies at the first check. The worst case is a string like `"aaaa…"`, where every substring is a palindrome and all 2^(n−1) partitions are valid.

**The precomputed-table optimization** makes each check O(1) instead of O(n), bringing the total to **O(2ⁿ)** plus O(n²) preprocessing. Worth naming; unnecessary at n ≤ 16.

**This is output-bound in the worst case** — with all-identical characters, every partitioning is valid, so you must produce 2^(n−1) results.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n) auxiliary</summary>

**O(n) auxiliary**, plus the output.

| Component | Size |
|---|---|
| `result` (required output) | up to 2^(n−1) partitionings → exponential |
| Recursion depth | at most n — one frame per piece, and pieces are ≥ 1 character → **O(n)** |
| `path` | at most n pieces → O(n) |
| Slices from `s[start:end]` | O(n) transient per level |

So: **"O(n) auxiliary, plus the exponential output."**

**Two hidden allocations worth noticing.** `s[start:end]` creates a new string each iteration, and `piece[::-1]` creates another for the reversal — so each check allocates O(k). Both are transient, but on a hot path they matter:

| Palindrome check | Time | Space |
|---|---|---|
| `piece == piece[::-1]` | O(k) | **O(k)** — allocates the reversal |
| Two pointers on `s[i..j]` | O(k) | **O(1)** — no allocation |
| Precomputed DP table | **O(1)** | O(n²) once |

The reverse-slice version is the most readable and perfectly fine here. **Knowing the two alternatives — and when each is worth it — is the point.**

**The recursion is n deep, not 2ⁿ.** Each frame consumes at least one character, so the deepest chain is n. The exponential is the number of root-to-leaf paths, only one of which is live at a time.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Partitioning means choosing where to cut, and recursively the only decision at any point is where the *next* piece ends. So I loop over every possible end position from the current start, and recurse only if that piece is a palindrome — the check is a pruning condition, not a filter applied at the end, so invalid branches die before any recursion. When `start` reaches the end of the string, every character has been placed into a validated piece, so the partitioning is complete. It's the usual choose-explore-un-choose skeleton, with the choice being a substring length instead of an element. O(n·2ⁿ) worst case, though pruning cuts most branches on realistic strings. I could precompute a DP table of which substrings are palindromes to make each check O(1) instead of O(n)."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Speed up the palindrome checks." | **The optimization.** Precompute a 2-D DP table where `dp[i][j]` says whether `s[i:j+1]` is a palindrome — O(n²) once, then O(1) per check. |
| "Why does `start == len(s)` mean success?" | Every character has been consumed into some piece, and every piece was validated as it was added. |
| "Why does the loop go to `len(s) + 1`?" | Slices are end-exclusive, so `end` must be able to reach `len(s)` to take the final piece. `range` is exclusive too, hence the `+1`. |
| "Find the **minimum** number of cuts instead?" | That's an optimization, not an enumeration — pure DP, O(n²). LeetCode 132, and notably harder. |
| "Just **count** the partitionings?" | DP again — no need to build them. Counting and listing are different problems. |
| "Make `is_palindrome` O(1) space?" | Two pointers over `s[start:end]` without slicing, as in [Valid Palindrome](125-valid-palindrome.md). |
| "What's the worst-case input?" | All identical characters — every substring is a palindrome, so all 2^(n−1) partitionings are valid and nothing prunes. |

**Traps:**

- **Looping to `len(s)` instead of `len(s) + 1`** — the final piece is never generated, so no partitioning ever completes.
- **`backtrack(end + 1)`** instead of `backtrack(end)`. `end` is already the next start, because slices are end-exclusive. The `+1` would skip a character.
- **Checking palindromes only at the base case** — correct but exponentially wasteful, and it misses the whole point of pruning.
- **Appending `path` instead of `path[:]`** — every result aliases the same list.
- **Forgetting `path.pop()`** — pieces accumulate across branches.
- **Off-by-one in the slice.** `s[start:end]` includes `start` and excludes `end`; verify on a single character.

**This same move shows up in:** [Subsets](78-subsets.md) (the skeleton, choosing elements instead of cuts) · [Combination Sum](39-combination-sum.md) (a `start` index advancing by a variable amount) · [Generate Parentheses](22-generate-parentheses.md) (pruning at the branch rather than validating at the leaf) · [Valid Palindrome](125-valid-palindrome.md) (the O(1)-space check) · [backtracking](../algorithms/backtracking.md).

</details>
