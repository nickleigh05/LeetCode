# 10. Regular Expression Matching

**Hard** · [LeetCode](https://leetcode.com/problems/regular-expression-matching/)

[📖 15. 2-D Dynamic Programming lesson](../learning/15-dp-2d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 15. 2-D Dynamic Programming problems](../rmap-practice/15-dp-2d.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Given an input string `s` and a pattern `p`, implement regular expression matching with support for:

- **`.`** — matches any single character
- **`*`** — matches **zero or more** of the *preceding* element

The match must cover the **entire** input string, not a partial one.

```
s = "aa",    p = "a"      →  false    "a" doesn't cover both characters
s = "aa",    p = "a*"     →  true     'a' repeated twice
s = "ab",    p = ".*"     →  true     "any character, zero or more times"
s = "aab",   p = "c*a*b"  →  true     c repeated zero times, a twice, then b
s = "mississippi", p = "mis*is*p*."  →  false
```

**Constraints:** `1 <= s.length <= 20` · `1 <= p.length <= 20` · `s` is lowercase letters · `p` is lowercase letters, `.`, and `*` · **every `*` has a valid preceding element**.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "return true/false" | **Feasibility.** The combining operator is `or` — one successful way to match is enough |
| two strings, progress in each | The state is `(position in s, position in p)` — the Unit 14 shape, but one side is a **pattern**, not text |
| "`*` matches **zero or more**" | The hard part. `*` isn't a character to match — it's a **quantifier on the element before it**, and it can consume nothing at all |
| "must cover the **entire** string" | An anchored match. Running out of pattern with input left over is failure, and vice versa |
| "every `*` has a valid preceding element" | You'll never see `p` starting with `*`, so `p[j-1]` is always safe when `p[j] == '*'` |
| lengths ≤ 20 | Tiny. So the difficulty is entirely **case analysis**, not performance |

The crucial realization is that **`*` is never processed on its own.** The atomic unit of a pattern isn't a character — it's either a single character (or `.`), or a **two-character `x*` pair**. So when standing at position `j` in the pattern, the first thing to ask is: *is the next character a `*`?* That question determines everything.

**Case A — no `*` follows** (`p[j]` is a plain character or `.`). Then `p[j]` must match `s[i]` exactly once. Match and advance both, or fail:

```
dp(i, j) = (s[i] matches p[j]) and dp(i+1, j+1)
```

**Case B — `p[j+1]` is `*`.** Now `p[j]*` can match **any number** of characters, including zero, and you can't know in advance how many. Two options, and either succeeding is enough:

```
dp(i, j) = dp(i, j+2)                              ← use ZERO of p[j]: skip the whole "x*" pair
        or (s[i] matches p[j]) and dp(i+1, j)      ← use ONE more: consume s[i], STAY at j
```

That second branch is the subtle one. After consuming one character you stay at the **same** pattern position `j`, because `x*` may match more. **The `*` isn't "used up"** — it stays available, which is exactly how "zero or more" gets expressed as a recursion.

And "matches" means `p[j] == s[i]` **or** `p[j] == '.'`, with the additional requirement that `s[i]` exists at all.

🤔 **Before you open the next section:** the zero-occurrence branch (`dp(i, j+2)`) doesn't look at `s[i]` at all. Why must it be tried even when `s` is completely exhausted? Think about `s = ""` with `p = "a*b*"`.

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Greedy — let `*` consume as much as possible | Match maximally, then continue | O(m+n) | O(1) | ❌ **Wrong.** `s = "aab"`, `p = "a*ab"` — greedy lets `a*` eat both `a`s and then `ab` has nothing to match |
| Two pointers with special cases | Hand-roll the logic linearly | — | — | ❌ No linear scan handles the branching; `*` genuinely requires trying both options |
| Plain recursion, no memo | Try both branches at every `*` | **O(2^(m+n))** | O(m+n) | ⚠️ Correct, and at m,n ≤ 20 it *passes* — but it's exponential on the classic `"aaaaaaaaaaaaaaaaaaaa"` / `"a*a*a*a*..."` pattern |
| **Memoized recursion on `(i, j)`** | Same recursion, cached | O(m·n) | O(m·n) | ✅ |
| Bottom-up 2-D table | Fill an `(m+1) × (n+1)` boolean grid | O(m·n) | O(m·n) | ✅ Equivalent; the index arithmetic is fussier |
| Build an NFA / Thompson's construction | Compile the pattern, simulate it | O(m·n) | O(n) | ⚠️ What a real regex engine does. Far more machinery than the problem needs |

**The decision:** **memoized recursion on `(i, j)`** — the case analysis written directly, with a cache.

**Why greedy fails.** With `s = "aab"` and `p = "a*ab"`, letting `a*` match greedily consumes both `a`s, leaving `"b"` against `"ab"` → failure. But matching just **one** `a` leaves `"ab"` against `"ab"` → success. **How many characters a `*` should consume depends on everything that follows it**, which is unknowable locally. That's the DP signal, and it's the same shape as the failures in [Word Break](139-word-break.md) and [Interleaving String](97-interleaving-string.md).

**Why memoization matters despite the tiny constraints.** At n = 20 the plain recursion passes, so this isn't about the given limits. It's that `s = "aaaaaaaaaaaaaaaaaaab"` with `p = "a*a*a*a*a*a*a*a*a*a*b"` is a genuinely exponential case — many different splits of the `a`s among the `a*` groups reach the same `(i, j)`. **Caching collapses them**, and this specific input is the classic denial-of-service pattern against naive backtracking regex engines, which is worth knowing about.

**Why recursion rather than a bottom-up table.** They're equivalent, but the recursion mirrors the case analysis exactly — "look ahead for a `*`, then branch" — while the table version needs careful 1-indexed offsets and a separate initialization for the first row (patterns like `a*b*` matching an empty string). **Write the recursion; mention the table.**

**Why the zero-occurrence branch comes first** and is unconditional — answering section 1's question. `dp(i, j+2)` skips the whole `x*` pair without consuming any input, and it must be available **even when `s` is exhausted**. With `s = ""` and `p = "a*b*"`, the only path to success is skipping both pairs. Guarding that branch behind a character match would make every trailing-`*` pattern fail on an empty remainder.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
memo = {}
```
The cache, keyed on `(i, j)` — position in `s`, position in `p`. That pair fully describes the remaining problem; how you arrived doesn't matter.
→ [dict-basics](../syntax/dict-basics.md) · [hashmap](../data-structures/hashmap.md)

```python
def dp(i, j):
    if (i, j) in memo:
        return memo[(i, j)]
    if j == len(p):
        return i == len(s)
```
**The base case, and it's an equality rather than a `True`.** Running out of pattern is a success **only if** the input is also exhausted — the match must cover the entire string. If `s` has characters left, the pattern ran out too early → `False`.

Note the cache check sits *before* the base case here. Harmless (the base case is O(1) anyway), though checking the base case first would be marginally tidier.
→ [function-basics](../syntax/function-basics.md) · [comparison-operators](../syntax/comparison-operators.md) · [recursion-basics](../syntax/recursion-basics.md)

```python
    match = i < len(s) and p[j] in (s[i], ".")
```
**"Does the current pattern element match the current character?"** — computed once and reused by both branches below.

Two conditions:
- `i < len(s)` — there *is* a character left. This must come first; without it `s[i]` raises `IndexError`. And it's genuinely reachable, because a `*` can leave the pattern with input exhausted.
- `p[j] in (s[i], ".")` — a compact way to write "the pattern character equals the input character, **or** the pattern character is a wildcard." The [membership test](../syntax/membership-operators.md) against a two-element tuple reads more cleanly than `p[j] == s[i] or p[j] == "."`.

Crucially `match` is only about **one** character — the `*` logic is handled separately below.
→ [membership-operators](../syntax/membership-operators.md) · [logical-operators](../syntax/logical-operators.md) · [tuple-basics](../syntax/tuple-basics.md)

```python
    if j + 1 < len(p) and p[j + 1] == "*":
        result = dp(i, j + 2) or (match and dp(i + 1, j))   # skip "char*", or consume one char
```
**The `*` case — look *ahead*, not at the current character.** This is the structural insight: `*` is never processed on its own, only as the second half of an `x*` pair, so you detect it by peeking at `p[j+1]`.

Two options, joined by `or` because either succeeding is enough:

- **`dp(i, j + 2)` — zero occurrences.** Skip the entire `x*` pair. `j + 2` steps over both the character and the star. **No input is consumed**, and no character match is required — which is what lets `"a*b*"` match `""`.
- **`(match and dp(i + 1, j))` — one more occurrence.** If the current character matches, consume it and **stay at `j`**. Staying is what allows further repetitions; the `*` is not used up.

Python's [`or`](../syntax/logical-operators.md) short-circuits, so if the zero-occurrence branch succeeds the second is never explored.
→ [logical-operators](../syntax/logical-operators.md) · [recursion-basics](../syntax/recursion-basics.md) · [dynamic-programming](../algorithms/dynamic-programming.md)

```python
    else:
        result = match and dp(i + 1, j + 1)
```
**The plain case.** No `*` follows, so `p[j]` must match exactly one character. Consume it and advance **both** positions — no branching, no choice.
→ [elif-else](../syntax/elif-else.md) · [logical-operators](../syntax/logical-operators.md)

```python
    memo[(i, j)] = result
    return result
```
Cache and return.
→ [dict-basics](../syntax/dict-basics.md)

```python
return dp(0, 0)
```
Start at the beginning of both.
→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def isMatch(self, s: str, p: str) -> bool:

        memo = {}

        def dp(i, j):
            if (i, j) in memo:
                return memo[(i, j)]
            if j == len(p):
                return i == len(s)

            match = i < len(s) and p[j] in (s[i], ".")

            if j + 1 < len(p) and p[j + 1] == "*":
                result = dp(i, j + 2) or (match and dp(i + 1, j))   # skip "char*", or consume one char
            else:
                result = match and dp(i + 1, j + 1)

            memo[(i, j)] = result
            return result

        return dp(0, 0)
```
</details>

**Trace it** — `s = "aab"`, `p = "c*a*b"` (the case greedy struggles with)

| call | pattern at `j` | what happens | result |
|---|---|---|---|
| `dp(0,0)` | `c*` | `match`: `'c'` vs `'a'` ✗. Only the zero branch → `dp(0,2)` | **True** |
| `dp(0,2)` | `a*` | zero branch → `dp(0,4)`; one-more branch → `dp(1,2)` | **True** |
| `dp(0,4)` | `b` (plain) | `'b'` vs `s[0]='a'` ✗ | False |
| `dp(1,2)` | `a*` | zero → `dp(1,4)`; one-more: `'a'` vs `s[1]='a'` ✓ → `dp(2,2)` | **True** |
| `dp(1,4)` | `b` | `'b'` vs `s[1]='a'` ✗ | False |
| `dp(2,2)` | `a*` | zero → `dp(2,4)` | **True** |
| `dp(2,4)` | `b` | `'b'` vs `s[2]='b'` ✓ → `dp(3,5)` | **True** |
| `dp(3,5)` | end of pattern | `i=3 == len(s)=3` ✓ | **True** |

Return **true** ✅

Two things to notice. `dp(0,0)` uses `c*` **zero** times even though `c` matches nothing — that branch is unconditional, which is precisely why it works. And `a*` is used **twice** by staying at `j = 2` across two consecutions before finally taking the zero branch at `dp(2,2)`.

**And the greedy counterexample**, `s = "aab"`, `p = "a*ab"`:

| call | pattern at `j` | result |
|---|---|---|
| `dp(0,0)` | `a*` | zero → `dp(0,2)`; one-more → `dp(1,0)` | |
| `dp(0,2)` | `a` plain | `'a'`✓ → `dp(1,3)`: `'b'` vs `s[1]='a'` ✗ | False |
| `dp(1,0)` | `a*` | zero → `dp(1,2)` | **True** |
| `dp(1,2)` | `a` plain | `'a'` vs `s[1]='a'` ✓ → `dp(2,3)` | **True** |
| `dp(2,3)` | `b` plain | `'b'` vs `s[2]='b'` ✓ → `dp(3,4)` = end, `i == len(s)` ✓ | **True** |

Return **true** ✅ — and the winning path has `a*` matching **exactly one** `a`, not two. A greedy engine that consumed both would report false. **The DP finds it because it tries both counts.**

</details>

<details>
<summary><b>4 · Time complexity</b> — O(m · n)</summary>

**O(m · n)**, where m = `len(s)` and n = `len(p)`.

Using **states × work per state**:

- **States:** `(i, j)` with `i` in `0..m` and `j` in `0..n` → **(m+1)(n+1) = O(m·n)**.
- **Work per state:** one character comparison, one lookahead, and at most two recursive calls that are each O(1) after the first time → **O(1)**.
- **O(m · n)** total.

At the limits, 20 × 20 = **400** states. Trivial.

**Without the memo it's exponential.** The classic adversarial input is `s = "aaaaaaaaaaaaaaaaaaab"` with `p = "a*a*a*a*a*a*a*a*a*a*b"`: each `a*` can absorb any number of the `a`s, so there are exponentially many ways to distribute them, and all of them fail at the final `b`. A naive backtracker explores every distribution.

That's not just a puzzle — it's **ReDoS**, the regular-expression denial-of-service class of vulnerability, and it's why production engines like RE2 use an NFA simulation with guaranteed linear time rather than backtracking. Being able to name that connection is a genuinely strong signal on this problem.

**Faster?** For this restricted syntax, O(m·n) is the standard bound and each state must be considered in the worst case. A compiled NFA simulation achieves the same O(m·n) with **O(n)** space.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(m · n)</summary>

**O(m · n)**, from two sources:

- The **memo** holds up to (m+1)(n+1) entries → O(m·n).
- The **recursion stack** nests at most once per character consumed or pattern element skipped → **O(m + n)** frames.

The memo dominates. At 20 × 20, all of this is negligible.

| Version | Space | Notes |
|---|---|---|
| Plain recursion | **O(m+n)** | Just the stack — but exponential time |
| **Memoized recursion** | **O(m·n)** | One entry per state, plus O(m+n) stack |
| Bottom-up 2-D table | **O(m·n)** | Same table, no stack |
| Rolling row | **O(n)** | `dp[i][j]` reads only rows `i` and `i+1` |
| NFA simulation | **O(n)** | What real engines do — state set proportional to pattern length |

**The rolling-row reduction does apply here**, unlike in [Burst Balloons](312-burst-balloons.md). In the bottom-up formulation `dp[i][j]` depends on `dp[i][j+2]` (same row) and `dp[i+1][j]` (next row), so two rows suffice → **O(n)**. It's not worth writing at these constraints, but it's the right answer to "can you reduce the space."

**Why the recursion depth is safe here:** each call either consumes a character of `s` or advances `j` by 2, so depth is bounded by O(m + n) = 40. Contrast [Longest Increasing Path in a Matrix](329-longest-increasing-path-in-a-matrix.md), where depth could reach 40,000.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The key structural point is that `*` is never processed on its own — the atomic unit of the pattern is either a single character or a two-character `x*` pair. So at each pattern position I look *ahead* to see whether the next character is a star. If it isn't, the current element must match exactly one character and I advance both positions. If it is, I have two options and either working is enough: skip the whole `x*` pair for zero occurrences, or — if the character matches — consume one character of the input and **stay** at the same pattern position, since the star may match more. The zero branch has to be unconditional, because `a*b*` needs to match an empty string. Greedy fails here: with `"aab"` against `"a*ab"`, letting the star eat both a's breaks the match, and the right count can't be decided locally. I memoize on `(i, j)`, which turns an exponential search into O(m·n). That exponential case is real — it's the ReDoS pattern that takes down backtracking regex engines."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why look ahead at `p[j+1]` instead of handling `*` when you reach it?" | Because `*` modifies the element *before* it. By the time you're standing on the star you've already consumed its operand. Looking ahead keeps the pair together. |
| "Why does the one-more branch stay at `j`?" | Because `x*` can match any number of characters. Staying leaves the star available for another repetition; advancing would allow exactly one. |
| "Why is the zero branch unconditional?" | It consumes no input, so it must be available even when `s` is exhausted. `s = ""` with `p = "a*b*"` succeeds only by taking it twice. |
| "Why does greedy fail?" | `s = "aab"`, `p = "a*ab"`. Consuming both a's leaves `"b"` against `"ab"`. The correct count is one, and it's only knowable from what follows. |
| "What's the worst case without memoization?" | `s = "aaaa…ab"`, `p = "a*a*a*…b"` — exponentially many ways to split the a's among the stars, all failing. That's ReDoS, and it's why RE2 avoids backtracking. |
| "Add support for `+`?" | `x+` is `x` followed by `x*` — rewrite it, or add a branch requiring at least one match before behaving like `*`. |
| "Reduce the space." | Bottom-up with two rolling rows → O(n), since each cell reads only the current and next row. |
| "How do real regex engines do this?" | Compile to an NFA (Thompson's construction) and simulate all active states at once — O(m·n) time, O(n) space, with no backtracking and therefore no ReDoS. |
| "What about `.*` — does it always match?" | It matches any string including empty, yes. The recursion handles it via the same two branches; `match` is always true for `.` when input remains. |

**Traps:**
- **Checking `p[j] == '*'` instead of looking ahead at `p[j+1]`.** The star belongs to the element before it; processing it in isolation makes the logic unworkable.
- **Advancing `j` in the one-more branch.** `dp(i+1, j+1)` would let `x*` match exactly one character — it must stay at `j`.
- **Guarding the zero branch behind `match`.** Every pattern ending in `*` then fails on an empty remainder.
- Omitting `i < len(s)` before `s[i]` — `IndexError`, and it's genuinely reachable.
- Base case returning `True` when the pattern is exhausted. It must be `i == len(s)`; a partial match is not a match.
- `j + 2` written as `j + 1` when skipping the pair — leaves a dangling `*` that gets processed on its own.
- Assuming the pattern can start with `*`. The constraints rule it out, so `p[j-1]` style lookbacks are safe — but this solution looks *ahead*, so it never needs that guarantee.

**This same move shows up in:** [Edit Distance](72-edit-distance.md) (the same two-string grid, minimizing over branches instead of testing feasibility) · [Interleaving String](97-interleaving-string.md) (a two-string feasibility grid with `or` semantics) · [Word Break](139-word-break.md) (matching a string against a set of patterns, where greedy also fails) · [Wildcard Matching](https://leetcode.com/problems/wildcard-matching/) (the sibling problem where `*` stands alone and matches any sequence — subtly easier) · [Distinct Subsequences](115-distinct-subsequences.md) (a grid where one side's characters are optional).

</details>

---
