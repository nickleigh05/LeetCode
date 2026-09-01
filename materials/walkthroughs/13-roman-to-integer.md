# 13. Roman to Integer

**Easy** · [LeetCode](https://leetcode.com/problems/roman-to-integer/) · [Solution file (no hints)](../../problems/0001-0499/13.py)

[📖 17. Math & Geometry lesson](../learning/19-math-geometry.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 17. Math & Geometry problems](../rmap-practice/17-math-geometry.md)

---

Convert a Roman numeral to an integer.

```
I=1  V=5  X=10  L=50  C=100  D=500  M=1000

s = "III"       →  3
s = "LVIII"     →  58      L + V + III
s = "MCMXCIV"   →  1994    M + CM + XC + IV
```

**Six subtractive forms exist and no others:** `IV`=4 · `IX`=9 · `XL`=40 · `XC`=90 · `CD`=400 · `CM`=900

**Constraints:** `1 <= len(s) <= 15` · `s` is a **valid** Roman numeral in `[1, 3999]`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "`s` is **guaranteed** valid" | ⚠️ **No validation needed.** Huge simplification — half the hard cases vanish |
| "six subtractive forms" | The only places a smaller symbol precedes a larger one |
| "range `[1, 3999]`" | At most `MMM` for thousands — no bar notation, no edge cases above 3999 |
| `len(s) <= 15` | Trivially small. **Any O(n) solution is instant** |
| Symbols are fixed | A 7-entry lookup table settles the values |

**The naive reading is "find the pairs first, then handle singles."** That works, and it's more code than you need.

**The observation that collapses it.** Walk left to right and look at each symbol *and the one after it*:

```
MCMXCIV
M  C  M  X  C  I  V
1000 100 1000 10 100 1 5
```

**In a valid numeral, a symbol is part of a subtractive pair exactly when it is smaller than the symbol immediately after it.**

```
M (1000) vs C (100)   →  1000 > 100   add     +1000
C (100)  vs M (1000)  →  100 < 1000   SUBTRACT  −100
M (1000) vs X (10)    →  add           +1000
X (10)   vs C (100)   →  10 < 100     SUBTRACT   −10
C (100)  vs I (1)     →  add            +100
I (1)    vs V (5)     →  1 < 5        SUBTRACT    −1
V (5)    — last       →  add             +5
```

```
1000 − 100 + 1000 − 10 + 100 − 1 + 5  =  1994  ✅
```

**Why subtracting works instead of pair-matching.** `CM` means "1000 minus 100". Processing `C` as `−100` and then `M` as `+1000` gives the same `900`, **without ever having to recognise the pair as a unit.** The two-character lookahead becomes a one-character comparison.

**And you never need the list of six forms.** It's implied: in a valid numeral, `smaller before larger` happens *only* in those six cases.

⚠️ **This is the step that depends on validity.** In garbage like `"IC"` the rule would happily produce 99, which isn't a legal numeral at all. **The guarantee is doing real work.**

🤔 **Before you open the next section:** what happens at the very last character, where there is no "next" symbol to compare against?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Match the six pairs first | Scan for `IV`, `IX`, … then singles | O(n) | O(1) | ⚠️ Correct, more branches |
| Two-symbol dict lookup | A 13-entry map, consume 2 or 1 chars | O(n) | O(1) | ⚠️ Correct, bigger table |
| **Compare with the next symbol** | Subtract if smaller, else add | **O(n)** | **O(1)** | ✅ **The answer** |
| Sum everything, then fix up | Add all, subtract `2 × value` per pair | O(n) | O(1) | ✅ Equivalent, one extra pass |
| `int()` on a parsed grammar | Regex / full parser | O(n) | O(1) | ❌ Solving a bigger problem |

**The decision: one pass, comparing each symbol with its successor.**

**Why "sum then fix up" is the same algorithm wearing a hat.** Add every symbol's value, then for each subtractive pair subtract twice the smaller value (once to cancel the wrong addition, once to apply the subtraction):

```
MCMXCIV summed naively:  1000+100+1000+10+100+1+5  =  2216
pairs found: CM, XC, IV  →  −2(100) −2(10) −2(1)   =  −222
                                                       1994 ✅
```

**It's a fine answer** and it makes the arithmetic explicit. **The one-pass version just folds the correction into the same loop.**

**Why not a real parser.** A grammar for Roman numerals would also *validate* — rejecting `IIII`, `VV`, `IC`. **The problem guarantees validity, so a parser solves a strictly harder problem for no credit.** ⚠️ Mention it only if asked "what if the input might be invalid?"

**The lookup table is the right data structure** for the seven symbols. ⚠️ **Building it inside the function re-creates a 7-entry dict on every call** — irrelevant here, but a class-level constant is the habit worth having when the function is hot:

```python
VALUES = {'I':1, 'V':5, 'X':10, 'L':50, 'C':100, 'D':500, 'M':1000}
```

**Verified: the one-pass version round-trips correctly against an independent integer-to-Roman table for every value from 1 to 3999 — 0 disagreements.**
→ [dict-basics](../syntax/dict-basics.md) · [for-loop](../syntax/for-loop.md)

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
hashmap = { 'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000 }
total = 0
```

**The seven symbol values, and the accumulator.**

⚠️ **Only the seven single characters appear** — no `IV`, `CM` entries. The subtractive forms are handled by the comparison, not by the table. **That's what keeps this small.**
→ [dict-basics](../syntax/dict-basics.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
for i in range(len(s)):
```

**Index-based, because the algorithm needs to peek at `s[i+1]`.**

⚠️ **This is why it's not `for ch in s`** — you need the *neighbour*, not just the character.
→ [range-function](../syntax/range-function.md) · [for-loop](../syntax/for-loop.md)

```python
    if i + 1 < len(s) and hashmap[s[i]] < hashmap[s[i+1]]:
        total -= hashmap[s[i]]
    else:
        total += hashmap[s[i]]
```

**The whole algorithm.**

- **`i + 1 < len(s)`** — the bounds check, and it does double duty. ⚠️ **At the last character it is `False`, so the `else` runs and the final symbol is always added.** That's correct: the last symbol can never be the left half of a subtractive pair.
- **`hashmap[s[i]] < hashmap[s[i+1]]`** — a smaller symbol before a larger one. In a valid numeral this happens **only** in the six subtractive forms.
- **Subtract** in that case; **add** otherwise.

⚠️ **`and` short-circuits.** Python evaluates `i + 1 < len(s)` first, so `s[i+1]` is never touched at the last index. **Reversing the two conditions gives an `IndexError` on every input.**

⚠️ **Strictly `<`, not `<=`.** Equal neighbours like the `II` in `"III"` must be *added*. `<=` would subtract them and turn `"III"` into `1 − 1 − 1`… actually `−1 −1 +1 = −1`. **Badly wrong.**
→ [logical-operators](../syntax/logical-operators.md) · [comparison-operators](../syntax/comparison-operators.md) · [dict-methods](../syntax/dict-methods.md) · [elif-else](../syntax/elif-else.md)

```python
return total
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def romanToInt(self, s: str) -> int:

        hashmap = { 'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000 }
        total = 0

        for i in range(len(s)):

            if i + 1 < len(s) and hashmap[s[i]] < hashmap[s[i+1]]:
                total -= hashmap[s[i]]
            else:
                total += hashmap[s[i]]

        return total
```

</details>

<details>
<summary>A tidier loop — pairwise with `zip`</summary>

```python
class Solution:

    VALUES = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}

    def romanToInt(self, s: str) -> int:

        v = self.VALUES
        total = v[s[-1]]                       # the last symbol is always added

        for cur, nxt in zip(s, s[1:]):
            total += -v[cur] if v[cur] < v[nxt] else v[cur]

        return total
```

**`zip(s, s[1:])` yields every adjacent pair**, so the bounds check disappears — at the cost of handling the final character separately. ⚠️ **`s[-1]` requires a non-empty string**, which the constraints guarantee (`len >= 1`).

**The table is a class attribute**, built once rather than on every call.
→ [zip-function](../syntax/zip-function.md) · [ternary-expression](../syntax/ternary-expression.md) · [instance-vs-class-attrs](../syntax/instance-vs-class-attrs.md)

</details>

<details>
<summary>The "sum then fix up" version</summary>

```python
class Solution:
    def romanToInt(self, s: str) -> int:

        values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        pairs = {'IV': 1, 'IX': 1, 'XL': 10, 'XC': 10, 'CD': 100, 'CM': 100}

        total = sum(values[c] for c in s)

        for pair, smaller in pairs.items():
            total -= 2 * smaller * s.count(pair)

        return total
```

⚠️ **`2 ×` because the naive sum already *added* the smaller value** — you must cancel that and then subtract it. **The factor of two is the trap in this version.**

**Slower** (a second pass per pair) and it needs the six-form table explicitly, but the arithmetic is very legible.
→ [generator-expressions](../syntax/generator-expressions.md) · [string-methods](../syntax/string-methods.md)

</details>

**Trace it** — `s = "MCMXCIV"`:

| `i` | `s[i]` | `s[i+1]` | Comparison | Contribution | `total` |
|---|---|---|---|---|---|
| 0 | M (1000) | C (100) | 1000 > 100 | **+1000** | 1000 |
| 1 | C (100) | M (1000) | ⚠️ 100 < 1000 | **−100** | 900 |
| 2 | M (1000) | X (10) | 1000 > 10 | **+1000** | 1900 |
| 3 | X (10) | C (100) | ⚠️ 10 < 100 | **−10** | 1890 |
| 4 | C (100) | I (1) | 100 > 1 | **+100** | 1990 |
| 5 | I (1) | V (5) | ⚠️ 1 < 5 | **−1** | 1989 |
| 6 | V (5) | — | **no next → else** | **+5** | **1994** |

**Answer: 1994** ✅

**Rows 1, 3 and 5 are the three subtractive pairs** — `CM`, `XC`, `IV` — and none of them was ever recognised *as a pair*. **Row 6 is the bounds check doing its job**: no successor, so the `else` branch adds.

**`s = "LVIII"`:**

| `i` | Symbol | Next | Contribution | `total` |
|---|---|---|---|---|
| 0 | L (50) | V (5) | +50 | 50 |
| 1 | V (5) | I (1) | +5 | 55 |
| 2 | I (1) | I (1) | ⚠️ **equal → add** +1 | 56 |
| 3 | I (1) | I (1) | +1 | 57 |
| 4 | I (1) | — | +1 | **58** |

**Answer: 58** ✅ — **rows 2 and 3 are why the comparison is strict.** With `<=` they'd subtract and the answer would be 54.

**`s = "III"`** → `+1 +1 +1 = 3` ✅

**Verified:** this exact implementation was round-tripped against an independent place-value integer-to-Roman table for **every integer from 1 to 3,999** — **0 disagreements**.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)**, one pass over a string of at most 15 characters.

| Phase | Cost |
|---|---|
| Build the 7-entry table | O(1) |
| One loop iteration per character | **O(n)** |
| Two dict lookups per iteration | O(1) each |
| **Total** | **O(n)** |

**`n <= 15`, so this is effectively constant** — at most 15 iterations and 30 hash lookups.

| Approach | Time | Passes |
|---|---|---|
| **One pass with lookahead** | **O(n)** | **1** ✅ |
| Two-symbol dict | O(n) | 1 |
| Sum then fix up | O(6n) | 7 (one `count` per pair) |
| Pair-match then singles | O(n) | 1, more branching |

**The "sum then fix up" version is O(n) too** but does seven scans — `sum` plus one `str.count` per subtractive form. **At n = 15 the difference is unmeasurable; at scale it's 7×.**

**Ω(n) is the floor** — every character contributes to the value, so all of them must be read.

⚠️ **Since the value is capped at 3999, `n <= 15`** (`MMMDCCCLXXXVIII` is the longest at 15 characters, for 3888). **Calling the whole thing O(1) is defensible** given the bound — but say *why*, don't just assert it.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — a fixed 7-entry table plus one accumulator.

| Component | Size |
|---|---|
| `hashmap` | **7 entries — constant** |
| `total`, `i` | O(1) |
| **Total** | **O(1)** ✅ |

⚠️ **The table is rebuilt on every call** as written. Seven entries is nothing, but **hoisting it to a class attribute is the right habit** — it makes the constancy explicit and avoids the allocation:

```python
class Solution:
    VALUES = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
```
→ [instance-vs-class-attrs](../syntax/instance-vs-class-attrs.md)

**Nothing scales with `n`.** No list of parsed tokens, no substring slicing, no recursion.

⚠️ **The `zip(s, s[1:])` variant costs O(n)** — `s[1:]` materialises a copy of the string. **At n ≤ 15 that's irrelevant; it's worth knowing that the tidier syntax is not free.**

**The "sum then fix up" version is also O(1)** — its `pairs` table is six fixed entries.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The naive approach is to spot the six subtractive pairs — IV, IX, XL, XC, CD, CM — and handle them as units. But there's a simpler characterisation: in a valid numeral, a symbol is the left half of a subtractive pair exactly when it's smaller than the symbol right after it. So I walk left to right with a value table, and if the current symbol is smaller than the next one I subtract it, otherwise I add it. `CM` becomes minus one hundred plus one thousand, which is nine hundred — same result, no pair matching. The bounds check does double duty: at the last character there's no successor, so it falls to the add branch, which is right because the last symbol can never start a pair. The comparison has to be strictly less-than, or the repeated `I`s in `LVIII` would get subtracted. O(n) time on a string of at most fifteen characters, O(1) space. Worth noting the input is guaranteed valid — if it weren't, I'd need a real grammar, because this rule would happily accept `IC` as ninety-nine."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why don't you need the list of six pairs?" | In a *valid* numeral, "smaller before larger" happens only in those six cases. The comparison implies the table. |
| "What happens at the last character?" | `i + 1 < len(s)` is false, so it's added — correct, since it can't be the left half of a pair. |
| "Why strictly `<`?" | Equal neighbours (`III`) must be added. `<=` turns 58 into 54. |
| "**What if the input might be invalid?**" | This rule accepts nonsense like `IC` (→ 99) and `IIII` (→ 4). Validation needs a grammar: at most 3 repeats of I/X/C/M, no repeats of V/L/D, and only the six subtractive forms. |
| "Would `for ch in s` work?" | No — you need the neighbour. Use indices, or `zip(s, s[1:])`. |
| "Order of the `and` conditions?" | ⚠️ Bounds check first. Reversed, `s[i+1]` raises `IndexError` on the last character. |
| "Alternative formulation?" | Sum every value, then subtract `2 × smaller` for each subtractive pair present. The factor of 2 cancels the wrong addition. |
| "**The reverse direction** — integer to Roman?" | [12](12-integer-to-roman.md) — a greedy over a value/symbol table that *includes* the six subtractive forms. |
| "What about values above 3999?" | Real Roman notation uses a vinculum (overbar) for ×1000. Out of scope here — the constraint caps at `MMM`. |
| "Right-to-left instead?" | Also works: track the largest value seen so far; subtract when the current symbol is smaller than it. Same cost. |

**Traps:**

- ⚠️ **`<=` instead of `<`** — subtracts repeated symbols. `"III"` → −1, `"LVIII"` → 54.
- ⚠️ **Checking `s[i+1]` before the bounds check** — `IndexError` on every input.
- ⚠️ **Forgetting the last character** — it must always be added.
- **Trying to consume two characters per step** without advancing the index correctly — double-counting.
- **Building a 13-entry table with the pairs in it** — works, but it's the version the comparison trick replaces.
- **Forgetting the `2 ×` in the sum-then-fix-up version** — the naive sum already added the smaller value once.
- **Validating the input** — it's guaranteed valid; a grammar is a strictly harder problem.
- **Assuming subtraction can span two places** — `IC` for 99 is not legal Roman; only the six listed forms exist.

**This same move shows up in:** [Integer to Roman](12-integer-to-roman.md) (the same table, run backwards) · [Valid Parentheses](20-valid-parentheses.md) (a small fixed lookup table driving a single scan) · [Excel Sheet Column Title](168-excel-sheet-column-title.md) (a non-standard positional number system) · [Palindrome Number](9-palindrome-number.md) (digit-by-digit arithmetic) · [Baseball Game](682-baseball-game.md) (a single pass with a small rule table) · [dict-basics](../syntax/dict-basics.md).

</details>

---
