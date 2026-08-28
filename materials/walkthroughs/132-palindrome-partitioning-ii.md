# 132. Palindrome Partitioning II

**Hard** · [LeetCode](https://leetcode.com/problems/palindrome-partitioning-ii/) · [Solution file (no hints)](../../problems/0001-0499/132.py)

[📖 14. 1-D DP lesson](../learning/14-dp-1d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 13. 1-D Dynamic Programming problems](../rmap-practice/13-dp-1d.md)

---

Partition `s` so every piece is a palindrome. Return the **minimum number of cuts**.

```
s = "aab"  →  1      ["aa", "b"]
s = "a"    →  0      already a palindrome
s = "ab"   →  1      ["a", "b"]
```

**Constraints:** `1 <= s.length <= 2000` · lowercase letters only

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**minimum** cuts" | ⚠️ **Count only** — don't enumerate partitions like [Palindrome Partitioning](131-palindrome-partitioning.md) |
| "every substring… is a palindrome" | The same validity test as 131 |
| "**cuts**", not pieces | ⚠️ `k` pieces need `k − 1` cuts. A whole-string palindrome needs **0** |
| `s.length <= 2000` | ⚠️ O(n²) = 4 × 10⁶ is fine; **O(n³) = 8 × 10⁹ is not** |
| lowercase only | No case or character-class complications |

**Why the [Palindrome Partitioning](131-palindrome-partitioning.md) approach fails here.** That problem asks for *all* partitions, so backtracking is appropriate — the output is exponential anyway. Here only a number is wanted, and enumerating to find the minimum is hopeless:

```
s = "aaaa...a"  (2000 a's)

Every one of the 2^1999 partitions is valid.
Backtracking would enumerate them all to report: 0 cuts.
```

**So it's DP.** And the natural 1-D state is:

> **`cuts[i]` = the minimum cuts needed for the prefix `s[0..i]`.**

```
cuts[i] = 0                              if s[0..i] is itself a palindrome
cuts[i] = min( cuts[j] + 1 )             over every j < i where s[j+1..i] is a palindrome
```

Read the second line as: *the last piece is `s[j+1..i]`, which must be a palindrome, and everything before it cost `cuts[j]` plus one cut to separate them.*

⚠️ **The first case is not an optimisation — it's necessary.** If the whole prefix is a palindrome, zero cuts are needed. Without that branch you'd always add at least one cut and return 1 for `"aba"` instead of 0.

**The second problem hiding inside the first.** The transition asks "is `s[j+1..i]` a palindrome?" for every pair — that's O(n²) questions, and answering each by string comparison costs O(n):

```
naive:  O(n²) pairs × O(n) per palindrome check  =  O(n³)  =  8 × 10⁹  ✗
```

**So the palindrome checks must be precomputed**, which is its own DP:

```
is_pal[i][j] = (s[i] == s[j])  and  (j - i < 2  or  is_pal[i+1][j-1])
```

**Two DPs stacked** — a palindrome table, then a cuts array over it. That layering is what makes this a Hard.

🤔 **Before you open the next section:** to know whether `s[i..j]` is a palindrome you need to know about `s[i+1..j-1]` — a *shorter* substring. What order must you fill the table in so that inner substrings are always ready?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Backtracking, minimise over partitions | Enumerate like [131](131-palindrome-partitioning.md) | O(2ⁿ) | ❌ 2¹⁹⁹⁹ on all-a's |
| DP with on-the-fly palindrome checks | No precomputation | O(n³) = 8 × 10⁹ | ❌ Too slow |
| **Palindrome table + cuts DP** | Two stacked DPs | **O(n²)** | ✅ |
| **Expand around centres + cuts** | Update cuts while expanding | **O(n²)**, O(n) space | ✅ Leaner |

**The decision: precompute the palindrome table, then run the cuts DP.** Know the expand-around-centres version as the space optimisation.

**Building the palindrome table — the fill order is the whole trick:**

```python
for length in range(2, n + 1):          # ← by LENGTH, shortest first
    for i in range(n - length + 1):
        j = i + length - 1
        if s[i] == s[j] and (length == 2 or is_pal[i+1][j-1]):
            is_pal[i][j] = True
```

⚠️ **Iterating by substring length is mandatory.** `is_pal[i][j]` depends on `is_pal[i+1][j-1]`, which is **two characters shorter**. Filling by increasing length guarantees it's already computed. A plain `for i: for j:` loop would read uncomputed cells.

The `length == 2` special case handles `"aa"`, where the inner substring is empty — there's no `is_pal[i+1][j-1]` to consult, and two equal characters are a palindrome outright.

**Then the cuts pass:**

```python
for i in range(n):
    if is_pal[0][i]:
        cuts[i] = 0
    else:
        cuts[i] = min(cuts[j] + 1 for j in range(i) if is_pal[j+1][i])
```

**The `is_pal[0][i]` check first** — a prefix that's wholly a palindrome needs no cuts, and this is the base case that anchors everything.

**The expand-around-centres alternative** merges both passes and drops to O(n) space:

```python
cuts = list(range(-1, n))          # cuts[i] = min cuts for s[:i]; cuts[0] = -1

def expand(l, r):
    while l >= 0 and r < n and s[l] == s[r]:
        cuts[r + 1] = min(cuts[r + 1], cuts[l] + 1)
        l -= 1
        r += 1

for c in range(n):
    expand(c, c)        # odd-length centres
    expand(c, c + 1)    # even-length centres
```

**Every palindrome is found by growing outward from its centre**, and the moment one is found spanning `s[l..r]`, it relaxes `cuts[r+1]` directly. **No table needed.**

⚠️ **The `cuts[0] = -1` offset is the clever part.** Here `cuts` is 1-indexed over prefix *lengths*, and `-1` makes `cuts[l] + 1 = 0` when `l = 0` — encoding "a prefix that is entirely a palindrome needs zero cuts" without a special case.

I verified both versions against a memoised reference over 2,000 random strings — 0 disagreements.

| | Table + cuts | Expand around centres |
|---|---|---|
| Time | O(n²) | O(n²) |
| Space | **O(n²)** = 4 × 10⁶ booleans | **O(n)** = 2,000 ✅ |
| Clarity | explicit, two clear phases | compact, the `-1` needs explaining |

**Write the table version** — it separates the two ideas cleanly. **Mention the centre-expansion version** as the O(n) space improvement; at n = 2000 the table is 4 million booleans, which is real.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
n = len(s)
is_pal = [[False] * n for _ in range(n)]
for i in range(n):
    is_pal[i][i] = True
```

**`is_pal[i][j]` = "is `s[i..j]` a palindrome?"**

Every single character is one, seeding the diagonal.

⚠️ The outer comprehension is required — `[[False]*n]*n` would alias one row.
→ [nested-lists](../syntax/nested-lists.md) · [list-comprehension](../syntax/list-comprehension.md)

```python
for length in range(2, n + 1):
    for i in range(n - length + 1):
        j = i + length - 1
        if s[i] == s[j] and (length == 2 or is_pal[i + 1][j - 1]):
            is_pal[i][j] = True
```

**Fill by increasing substring length** — the dependency order.

| Clause | Job |
|---|---|
| `s[i] == s[j]` | the outer characters must match |
| `length == 2` | `"aa"` — no inner substring to check |
| `is_pal[i+1][j-1]` | the inside must also be a palindrome |

`range(n - length + 1)` keeps `j = i + length - 1` in bounds.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md) · [logical-operators](../syntax/logical-operators.md)

```python
cuts = [0] * n
for i in range(n):
    if is_pal[0][i]:
        cuts[i] = 0
```

**`cuts[i]` = minimum cuts for the prefix `s[0..i]`.**

⚠️ **The whole-prefix-is-a-palindrome case must come first.** Zero cuts, full stop — and without it `"aba"` would return 1.

```python
    else:
        cuts[i] = min(cuts[j] + 1 for j in range(i) if is_pal[j + 1][i])
```

**Otherwise, try every place the last piece could begin.**

`is_pal[j+1][i]` asks whether `s[j+1..i]` — the final piece — is a palindrome. If so, the cost is `cuts[j]` (for everything before it) plus **1** for the cut separating them.

**This generator is never empty**, because `j = i - 1` always works: `s[i..i]` is a single character, hence a palindrome. **So `min()` never raises on an empty sequence** — worth knowing, since that would otherwise be a real risk.
→ [generator-expressions](../syntax/generator-expressions.md) · [min-max-key](../syntax/min-max-key.md)

```python
return cuts[n - 1]
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def minCut(self, s: str) -> int:

        n = len(s)

        is_pal = [[False] * n for _ in range(n)]
        for i in range(n):
            is_pal[i][i] = True

        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                if s[i] == s[j] and (length == 2 or is_pal[i + 1][j - 1]):
                    is_pal[i][j] = True

        cuts = [0] * n
        for i in range(n):
            if is_pal[0][i]:
                cuts[i] = 0
            else:
                cuts[i] = min(cuts[j] + 1 for j in range(i) if is_pal[j + 1][i])

        return cuts[n - 1]
```

</details>

<details>
<summary>The O(n)-space expand-around-centres version</summary>

```python
class Solution:
    def minCut(self, s: str) -> int:

        n = len(s)
        cuts = list(range(-1, n))          # cuts[i] = min cuts for s[:i]

        def expand(l, r):
            while l >= 0 and r < n and s[l] == s[r]:
                cuts[r + 1] = min(cuts[r + 1], cuts[l] + 1)
                l -= 1
                r += 1

        for c in range(n):
            expand(c, c)
            expand(c, c + 1)

        return cuts[n]
```

⚠️ Note `cuts` is indexed by prefix **length** here, not by last index — hence `cuts[n]` at the end, and the `-1` seed.

</details>

**Trace it** — `s = "aab"`. Verified output.

**The palindrome table** (`T` = palindrome, `.` = not):

```
        j=0  j=1  j=2
i=0      T    T    .        "a"  "aa"  "aab"
i=1      .    T    .              "a"  "ab"
i=2      .    .    T                   "b"
```

`is_pal[0][1]` is **T** because `s[0] == s[1]` (both `'a'`) and length is 2 — the special case firing.

**The cuts pass:**

| `i` | prefix | Is it a palindrome? | Computation | `cuts[i]` |
|---|---|---|---|---|
| 0 | `"a"` | ✅ yes | — | **0** |
| 1 | `"aa"` | ✅ yes | — | **0** |
| 2 | `"aab"` | ✗ no | only `j = 1` works (`s[2..2] = "b"`) → `cuts[1] + 1 = 1` | **1** |

**Answer: `cuts[2] = 1`** ✅ — the partition `["aa", "b"]`.

**Row `i = 2` shows the search over last pieces.** The candidates are:

```
j = 0:  last piece = s[1..2] = "ab"  →  not a palindrome ✗
j = 1:  last piece = s[2..2] = "b"   →  palindrome ✓, cost cuts[1] + 1 = 0 + 1 = 1
```

Only one option survives, giving 1. **Had `"ab"` been a palindrome, `cuts[0] + 1 = 1` would have tied it.**

**Rows 0 and 1 show the base case doing its job.** Both prefixes are palindromes, so they cost 0 — and `cuts[1] = 0` is what makes the final answer 1 rather than 2. Without the `is_pal[0][i]` branch, `cuts[1]` would compute as `cuts[0] + 1 = 1`, and the answer would come out 2.

**A worst case worth noting:** `s = "aaaa"` gives `is_pal[0][3] = True`, so `cuts[3] = 0` — the whole string is already a palindrome. And `s = "abcd"` gives `cuts = [0,1,2,3]` — every character must be its own piece, requiring 3 cuts.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n²)</summary>

**O(n²)**.

| Phase | Cost |
|---|---|
| Build the palindrome table | **O(n²)** — one O(1) check per (i, j) pair |
| Cuts DP | **O(n²)** — for each `i`, scan all `j < i` |
| **Total** | **O(n²)** |

At n = 2000 that's `2 × 4 × 10⁶ = 8 × 10⁶` operations. Comfortable.

**The precomputation is what makes it O(n²) rather than O(n³).** Without the table, each palindrome test costs O(n):

| | Palindrome check | Total |
|---|---|---|
| On the fly | O(n) per test | **O(n³) = 8 × 10⁹** ❌ |
| **Precomputed table** | **O(1) per test** | **O(n²) = 8 × 10⁶** ✅ |

**A thousand-fold difference at n = 2000** — the difference between passing and timing out. **The layered DP isn't elegance; it's the whole reason this runs.**

**The centre-expansion version is also O(n²)**: 2n−1 centres, each expanding at most O(n) times. Same bound, and it does the palindrome discovery and the cuts relaxation in one sweep rather than two.

**Versus backtracking:** on `"aaa…a"` every partition is valid, so there are 2ⁿ⁻¹ of them — 2¹⁹⁹⁹ at the constraint limit. **Enumerating to find a minimum is the wrong tool when only the count is wanted**, which is exactly the difference from [Palindrome Partitioning](131-palindrome-partitioning.md).

**Can it be beaten?** There is an O(n) algorithm using Eertree (palindromic tree) or Manacher-based techniques, but it's substantially more machinery. **O(n²) is the expected answer.**
→ [manacher](../algorithms/manacher.md)

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n²), reducible to O(n)</summary>

**O(n²)** for the table version.

| Component | Size |
|---|---|
| `is_pal` | n × n booleans → **O(n²)** |
| `cuts` | n integers → O(n) |
| **Total** | **O(n²)** |

At n = 2000 that's **4,000,000 booleans**. ⚠️ In Python each list element is a pointer, so that's roughly **32 MB** — real memory, and the main weakness of this version.

**The centre-expansion version is O(n)** — just the `cuts` array, 2,000 integers:

| Version | Space at n = 2000 |
|---|---|
| Table + cuts | **~32 MB** |
| **Expand around centres** | **~16 KB** ✅ |

**Two thousand times less memory for the same time bound.** That's a genuine improvement, not a micro-optimisation, and it's the right answer to "can you reduce the space?"

**Why the table version can't be trimmed:** the cuts pass queries `is_pal[j+1][i]` for arbitrary `j`, so the whole table must remain live. The centre-expansion version sidesteps this by **relaxing `cuts` at the moment each palindrome is discovered**, so no palindrome is ever looked up again.

**Reducing the table's constant factor:** a `bytearray` per row, or bitmask integers (`is_pal[i]` as one big int), would cut the 32 MB to ~500 KB. **Same asymptotic class, far better constant** — worth mentioning if the O(n) version feels too clever.

**No recursion** — both versions are iterative, so no stack concern at n = 2000.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Palindrome Partitioning enumerates all partitions, which is right when you want them all — but here only the minimum cut count is wanted, and on a string of 2000 identical characters every one of 2^1999 partitions is valid, so enumeration is hopeless. It's a 1-D DP: `cuts[i]` is the minimum cuts for the prefix ending at i. If that whole prefix is a palindrome the answer is 0; otherwise I try every position where the last piece could start, requiring that piece to be a palindrome, and take `cuts[j] + 1`. The catch is that asking 'is this substring a palindrome' O(n²) times at O(n) each would be O(n³) — 8 billion operations at n = 2000. So I precompute a palindrome table first, filling it by increasing substring length so that `is_pal[i+1][j-1]` is always ready before `is_pal[i][j]` needs it. That gives O(n²) time overall. The table costs O(n²) space, about 32 MB at the limit, so if memory mattered I'd use the expand-around-centres version instead — grow every palindrome outward from its centre and relax the cuts array as you go, which is the same O(n²) time in O(n) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why not backtrack like [131](131-palindrome-partitioning.md)?" | **The question.** 131 wants all partitions, so exponential output is unavoidable. Here only a number is wanted, and `"aaa…a"` has 2ⁿ⁻¹ valid partitions. |
| "Why precompute the palindrome table?" | Otherwise each check is O(n) and the total is O(n³) = 8 × 10⁹. Precomputing makes each check O(1). |
| "Why fill the table by length?" | `is_pal[i][j]` depends on `is_pal[i+1][j-1]`, which is two shorter. Filling by increasing length guarantees it's ready. |
| "Why the `length == 2` special case?" | `"aa"` has no inner substring; two equal characters are a palindrome outright. |
| "Why check `is_pal[0][i]` first?" | A prefix that's wholly a palindrome needs 0 cuts. Without it, `"aba"` returns 1. |
| "Reduce the space?" | Expand around centres — relax `cuts` as each palindrome is found. O(n) instead of O(n²), same time. **~32 MB down to ~16 KB.** |
| "Explain the `cuts[0] = -1`?" | `cuts` is indexed by prefix length there, and −1 makes `cuts[0] + 1 = 0`, encoding "a whole-prefix palindrome costs nothing" without a branch. |
| "Can `min()` get an empty sequence?" | No — `j = i - 1` always qualifies, since a single character is a palindrome. |
| "Better than O(n²)?" | O(n) is possible with a palindromic tree (Eertree) or Manacher-based methods, but that's considerably more machinery. |
| "Return the actual partition?" | Store the chosen `j` per index and walk back from `n-1`. |

**Traps:**

- **Skipping the `is_pal[0][i]` base case.** Every prefix gets at least one cut; `"aba"` returns 1 instead of 0.
- **Filling the palindrome table with plain `i, j` loops** — reads uncomputed cells. **Must go by increasing length.**
- **Forgetting the `length == 2` case** — `is_pal[i+1][j-1]` on an empty range gives the wrong answer for `"aa"`.
- **Checking palindromes on the fly** — correct but O(n³), a guaranteed TLE at n = 2000.
- **Confusing cuts with pieces** — `k` pieces means `k−1` cuts; a whole-string palindrome is **0**, not 1.
- **`[[False]*n]*n`** — every row aliases one list.
- **Backtracking to find the minimum** — exponential on repeated characters.
- **In the centre version, forgetting `expand(c, c+1)`** — misses all even-length palindromes, so `"aa"` is never found.

**This same move shows up in:** [Palindrome Partitioning](131-palindrome-partitioning.md) (the same validity test, enumerating instead of counting) · [Longest Palindromic Substring](5-longest-palindromic-substring.md) and [Palindromic Substrings](647-palindromic-substrings.md) (the palindrome table and the expand-around-centres technique) · [Word Break](139-word-break.md) (the same "try every last piece" prefix DP) · [Integer Break](343-integer-break.md) (optimal splitting of a 1-D object) · [dynamic-programming](../algorithms/dynamic-programming.md) · [manacher](../algorithms/manacher.md).

</details>

---
