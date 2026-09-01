# 12. Integer to Roman

**Medium** · [LeetCode](https://leetcode.com/problems/integer-to-roman/) · [Solution file (no hints)](../../problems/0001-0499/12.py)

[📖 17. Math & Geometry lesson](../learning/19-math-geometry.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 17. Math & Geometry problems](../rmap-practice/17-math-geometry.md)

---

Convert an integer to its Roman numeral.

```
num = 3749  →  "MMMDCCXLIX"     MMM + DCC + XL + IX
num = 58    →  "LVIII"          L + VIII
num = 1994  →  "MCMXCIV"        M + CM + XC + IV
```

**Symbols:** `I`=1 `V`=5 `X`=10 `L`=50 `C`=100 `D`=500 `M`=1000
**Subtractive forms (the only six):** `IV`=4 `IX`=9 `XL`=40 `XC`=90 `CD`=400 `CM`=900
**Rule:** `I`, `X`, `C`, `M` repeat at most 3 times; `V`, `L`, `D` never repeat.

**Constraints:** `1 <= num <= 3999`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "highest to lowest place value" | Process **descending** — greedy from the biggest symbol |
| "if it starts with 4 or 9, use the subtractive form" | ⚠️ **Or: put 4, 9, 40, 90, 400, 900 in the table and stop special-casing** |
| "I, X, C, M at most 3 times" | Automatic once 4 and 9 are table entries |
| "V, L, D never repeat" | Same — `VV` never arises if `X` is in the table above `V` |
| `1 <= num <= 3999` | ⚠️ **`MMM` is the ceiling.** No vinculum, no zero, no negatives |

**The rules read like a pile of special cases. They aren't — they're one table.**

**The move that dissolves the problem:** treat the six subtractive forms as *symbols in their own right*. Then the whole thing is a plain greedy over 13 values in descending order:

```
1000 M    900 CM    500 D    400 CD
 100 C     90 XC     50 L     40 XL
  10 X      9 IX      5 V      4 IV
   1 I
```

**Now "if it starts with 4 or 9" is gone.** You never test for it — the table entry for `4` simply wins before `1` gets a chance.

```
1994
 −1000 → M      remaining 994
 −900  → CM     remaining  94
 −90   → XC     remaining   4
 −4    → IV     remaining   0
             MCMXCIV  ✅
```

**Why greedy is safe here.** Each rule about repetition is enforced *by construction*:

- **`I` can't appear 4 times** — at 4 the table's `IV` entry fires first, leaving 0.
- **`V` can't appear twice** — two `V`s would be 10, and `X` sits above `V` in the table.

⚠️ **This is the property that makes the numeral system "canonical" for greedy.** It is *not* automatic — greedy coin change fails for coin sets like `{1, 3, 4}` (making 6 greedily gives `4+1+1`, three coins, versus `3+3`). **Roman's 13 values happen to be greedy-safe, and saying why is the interesting part of this problem.**

🤔 **Before you open the next section:** `3749` needs `MMM` — three of the same symbol. How does a single pass produce three `M`s?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Rule-by-rule with `if`s for 4 and 9 | Transcribe the statement | O(1) | O(1) | ❌ A dozen branches, easy to get wrong |
| **Greedy over a 13-entry table** | Subtract the largest that fits | **O(1)** | **O(1)** | ✅ **The answer** |
| Place-value lookup tables | Four arrays of 10 strings each | **O(1)** | O(1) | ✅ Fastest, table-heavy |
| Recursion on the table | Same greedy, recursive | O(1) | O(d) stack | ⚠️ No benefit |
| Build from [13](13-roman-to-integer.md) by search | Try numerals until one parses | ❌ | ❌ | ❌ Absurd |

**The decision: greedy over the 13-value table.**

**Why the 13-entry table beats transcribing the rules.** The statement describes three interacting rules; the table encodes all three in data. **Data you can eyeball is safer than branches you have to trace** — and this is the general lesson, not a Roman-numeral trick.

**The place-value alternative is worth knowing** because it is genuinely the fastest and completely branch-free:

```python
THOUSANDS = ["", "M", "MM", "MMM"]
HUNDREDS  = ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"]
TENS      = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"]
ONES      = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]

return THOUSANDS[num // 1000] + HUNDREDS[num // 100 % 10] + TENS[num // 10 % 10] + ONES[num % 10]
```

**Four indexings and three concatenations — no loop at all.** ⚠️ **It only works because `num <= 3999`**, which caps the thousands table at four entries. **That's the trade: it hard-codes the constraint.** The greedy table doesn't — extend it and it keeps working.

**I used this exact place-value version as the independent reference** when checking the greedy one. **Verified: identical output for every integer from 1 to 3,999.**

**Why greedy is provably correct here** — the argument an interviewer wants:

> At each step, let `v` be the largest table value `<= num`. Suppose an optimal numeral doesn't use `v`. Then it builds at least `v` from strictly smaller table values — but the Roman table is constructed so that **no legal combination of values below `v` reaches `v`** without violating a repetition rule (three `C`s max is 300 < 400 = `CD`; three `X`s max is 30 < 40 = `XL`, and so on). **So `v` must be used.** Induct on the remainder.

**Note where that argument would break.** ⚠️ Remove `CD` and `CM` from the table and greedy would emit `CCCC` for 400 — **still 400, but not a legal numeral**. **The table's completeness is load-bearing.**

**Why not recursion.** `intToRoman(num) = symbol + intToRoman(num - value)` is elegant and adds stack depth for nothing. **The loop is the same algorithm without the frames.**
→ [list-basics](../syntax/list-basics.md) · [tuple-basics](../syntax/tuple-basics.md)

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
VALUES = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100,  "C"), (90,  "XC"), (50,  "L"), (40,  "XL"),
    (10,   "X"), (9,   "IX"), (5,   "V"), (4,   "IV"),
    (1,    "I"),
]
```

**Thirteen pairs, strictly descending.**

⚠️ **The six subtractive forms are ordinary entries.** `900 → "CM"` sits between `1000` and `500` exactly where its value puts it. **This is the entire trick** — once they're in the table there are no special cases left.

⚠️ **Descending order is mandatory.** Greedy takes the first entry that fits, so a mis-ordered table silently produces wrong numerals — `4` before `5` in the list would never let `V` fire.
→ [list-basics](../syntax/list-basics.md) · [tuple-basics](../syntax/tuple-basics.md)

```python
result = []
```

**Collect the pieces in a list, join at the end.** ⚠️ **Not `result = ""` with `+=`** — repeated string concatenation is O(n²) in the worst case because each `+=` copies the whole string. **`"".join(...)` is the idiom.**
→ [string-join-slice](../syntax/string-join-slice.md) · [string-immutability](../syntax/string-immutability.md)

```python
for value, symbol in VALUES:
    if num == 0:
        break
    count, num = divmod(num, value)
    result.append(symbol * count)
```

**One pass over the table.**

- **`divmod(num, value)`** returns `(how many fit, what's left)` in one call. For `num = 3749, value = 1000` that's `(3, 749)`.
- **`symbol * count`** repeats the symbol — `"M" * 3` is `"MMM"`. ⚠️ **This is how a single pass emits three `M`s**, and `count` is `0` for every entry that doesn't fit, giving the empty string.
- **`break` when `num` hits 0** — a pure optimisation; the remaining entries would all contribute `""`.

⚠️ **`count` reaches 3 for exactly four entries — `I`, `X`, `C`, `M` — and is never above 1 for the other nine.** Measured across all 3,999 inputs. That's the repetition rule enforcing itself: a fourth `I` would mean a remainder of 4, which the `(4, "IV")` entry above it already consumed, and a second `V` would mean 10, which `(10, "X")` already took. **You never write those rules down.**
→ [for-loop](../syntax/for-loop.md) · [tuple-unpacking](../syntax/tuple-unpacking.md) · [integer-division-modulo](../syntax/integer-division-modulo.md) · [string-basics](../syntax/string-basics.md)

```python
return "".join(result)
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:

    VALUES = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100,  "C"), (90,  "XC"), (50,  "L"), (40,  "XL"),
        (10,   "X"), (9,   "IX"), (5,   "V"), (4,   "IV"),
        (1,    "I"),
    ]

    def intToRoman(self, num: int) -> str:

        result = []

        for value, symbol in self.VALUES:
            if num == 0:
                break
            count, num = divmod(num, value)
            result.append(symbol * count)

        return "".join(result)
```

</details>

<details>
<summary>The while-loop phrasing — same algorithm, more explicit</summary>

```python
class Solution:
    def intToRoman(self, num: int) -> str:

        values  = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
        symbols = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]

        result = []
        for i in range(len(values)):
            while num >= values[i]:
                result.append(symbols[i])
                num -= values[i]

        return "".join(result)
```

**"Subtract while it fits"** rather than `divmod`. ⚠️ **Two parallel lists must stay in sync** — a single misalignment produces plausible-looking garbage. **The list of tuples is safer.**
→ [while-loop](../syntax/while-loop.md)

</details>

<details>
<summary>The place-value version — no loop at all</summary>

```python
class Solution:

    THOUSANDS = ["", "M", "MM", "MMM"]
    HUNDREDS  = ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"]
    TENS      = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"]
    ONES      = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]

    def intToRoman(self, num: int) -> str:
        return (self.THOUSANDS[num // 1000]
              + self.HUNDREDS[num // 100 % 10]
              + self.TENS[num // 10 % 10]
              + self.ONES[num % 10])
```

**Four lookups, three concatenations, zero branches — the fastest version.**

⚠️ **It hard-codes `num <= 3999`**: `THOUSANDS` has exactly four entries, so `num = 4000` would raise `IndexError`. **The greedy table degrades gracefully; this one doesn't.**

⚠️ **Note `num // 100 % 10`** — extract the hundreds *digit*, not the hundreds *count*. Writing `num // 100` alone gives 37 for 3749 and indexes out of range.

**This was the independent reference used to verify the greedy version across all 3,999 inputs.**
→ [instance-vs-class-attrs](../syntax/instance-vs-class-attrs.md) · [integer-division-modulo](../syntax/integer-division-modulo.md)

</details>

**Trace it** — `num = 3749`:

| Table entry | `divmod(num, value)` | `symbol * count` | `num` after |
|---|---|---|---|
| (1000, M) | (3, 749) | **"MMM"** ⚠️ three at once | 749 |
| (900, CM) | (0, 749) | "" | 749 |
| (500, D) | (1, 249) | **"D"** | 249 |
| (400, CD) | (0, 249) | "" | 249 |
| (100, C) | (2, 49) | **"CC"** | 49 |
| (90, XC) | (0, 49) | "" | 49 |
| (50, L) | (0, 49) | "" | 49 |
| (40, XL) | (1, 9) | **"XL"** | 9 |
| (10, X) | (0, 9) | "" | 9 |
| (9, IX) | (1, 0) | **"IX"** | **0** |
| — | — | `break` | — |

**`"MMM" + "D" + "CC" + "XL" + "IX"` = `"MMMDCCXLIX"`** ✅ — matching the expected output.

**Row 1 answers the earlier question:** `divmod` gives `count = 3`, and `"M" * 3` emits all three at once.

**Rows 8 and 10 are the subtractive forms firing as ordinary table entries.** ⚠️ **At `num = 49`, the entry `(50, L)` does not fit, so `(40, XL)` takes it — which is exactly why `IL` is never produced.**

**`num = 1994`:**

```
1000 → "M"    (994)
 900 → "CM"   ( 94)
  90 → "XC"   (  4)
   4 → "IV"   (  0)   →  "MCMXCIV" ✅
```

**`num = 58`:**

```
50 → "L"   (8)
 5 → "V"   (3)
 1 → "III" (0)   →  "LVIII" ✅
```

⚠️ **`"I" * 3` gives exactly three `I`s** — never four, because the `(4, "IV")` entry sits above `(1, "I")` and would have consumed a remainder of 4.

**Verified:** the greedy table version was checked against the independent place-value implementation for **every integer from 1 to 3,999** — **0 disagreements**. Both were additionally round-tripped through the [Roman to Integer](13-roman-to-integer.md) parser, recovering the original number in all 3,999 cases.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(1)</summary>

**O(1)** — the input is bounded, so everything here is bounded.

| Phase | Cost |
|---|---|
| Loop over the table | **13 iterations, fixed** |
| `divmod` per iteration | O(1) |
| `symbol * count` | **≤ 3 repeats** — verified over all 3,999 inputs |
| `"".join` | **≤ 15 characters** |
| **Total** | **O(1)** |

**The longest possible output is 15 characters** — `MMMDCCCLXXXVIII` for 3888. **So the work is bounded no matter what.**

**If you insist on a variable:** `O(log num)` for the number of symbols, since each table entry roughly divides the remainder by a constant.

| Approach | Time | Operations |
|---|---|---|
| Place-value tables | **O(1)** | **4 lookups + 3 joins** ✅✅ |
| **Greedy over 13 entries** | **O(1)** | **13 iterations** ✅ |
| While-loop subtraction | O(1) | up to 15 appends |

**The place-value version is measurably faster** — no loop, no `divmod`. ⚠️ **The greedy version is the one to write in an interview**, because it explains itself and doesn't bake in the 3999 cap.

⚠️ **Don't say "O(n)" without saying what `n` is.** There is no array here; the only input is a single bounded integer.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — a fixed table plus an output of at most 15 characters.

| Component | Size |
|---|---|
| `VALUES` | **13 entries — constant** |
| `result` | ≤ 13 fragments, ≤ 15 characters total |
| **Total** | **O(1)** ✅ |

⚠️ **Building `VALUES` inside the method re-creates 13 tuples on every call.** Harmless here; **a class-level constant is the right habit** and makes the constancy explicit.
→ [instance-vs-class-attrs](../syntax/instance-vs-class-attrs.md)

⚠️ **`result = []` then `"".join(result)` rather than `result += symbol`.** Strings are immutable, so `+=` allocates a fresh string each time — **O(k²) character copies for a k-character result**. At 15 characters this is invisible; **the habit matters when the output is large.**
→ [string-immutability](../syntax/string-immutability.md) · [string-join-slice](../syntax/string-join-slice.md)

**The place-value version stores 4 tables totalling 34 strings** — also constant, and it builds the answer with three concatenations of tiny strings.

**No recursion.** The recursive phrasing would add up to 15 stack frames for no gain.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The rules look like a pile of special cases — four and nine become subtractive forms, I/X/C/M repeat at most three times, V/L/D never repeat — but they collapse into one table if I treat the six subtractive forms as symbols in their own right. So I have thirteen value-symbol pairs in descending order, and I greedily take the largest that fits, using divmod so a count of three emits `MMM` in one step. Every repetition rule is then enforced by construction: I can't emit four `I`s because the entry for four fires first, and I can't emit two `V`s because ten is `X`. Greedy is provably correct here because no legal combination of smaller values can reach the next table value — three `C`s is three hundred, short of four hundred. That's not automatic; greedy coin change fails on a set like one, three, four. It's O(1) — the input is capped at 3999, so at most fifteen characters out. There's also a branch-free place-value version with four lookup tables that's faster, but it hard-codes the 3999 bound in the thousands table."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "**Why is greedy correct?**" | **The question.** No legal combination of table values below `v` reaches `v` — three `C`s is 300 < 400. So the largest fitting value must be used. Induct on the remainder. |
| "Is greedy always correct for such systems?" | **No.** Coin set `{1,3,4}`, target 6: greedy gives `4+1+1`, optimal is `3+3`. The Roman table happens to be canonical. |
| "What if you drop `CD` and `CM` from the table?" | Greedy still totals 400 — as `CCCC`, which isn't a legal numeral. **The table's completeness is load-bearing.** |
| "Why `divmod` instead of a `while`?" | One step per table entry instead of one per symbol, and it makes "three `M`s" a single operation. |
| "How does it produce `MMM`?" | `divmod(3749, 1000)` → count 3, and `"M" * 3`. |
| "Handle numbers above 3999?" | Real Roman uses a vinculum (overbar) for ×1000. Extend the table with those symbols — the greedy loop needs no other change; **the place-value version would need a new table.** |
| "Faster?" | The place-value tables: four indexings, no loop. Trades generality for speed. |
| "**Reverse direction?**" | [13](13-roman-to-integer.md) — compare each symbol with its successor and subtract when smaller. |
| "Validate a numeral?" | Convert it with [13](13-roman-to-integer.md), convert back with this, and check you get the original string. **A neat round-trip validator** — and exactly how both were verified here. |
| "Why `join` rather than `+=`?" | Strings are immutable; `+=` copies. O(k²) versus O(k). |

**Traps:**

- ⚠️ **Special-casing 4 and 9 with `if`s** instead of putting them in the table — a dozen branches where one table entry would do.
- ⚠️ **A table not in strictly descending order** — greedy takes the first fit, so order *is* the algorithm.
- ⚠️ **`num // 100` instead of `num // 100 % 10`** in the place-value version — gives 37 for 3749 and indexes out of range.
- **Two parallel lists drifting out of sync** — use tuples.
- **`result += symbol`** — quadratic string building.
- **Emitting `IL` for 49 or `IC` for 99** — happens if you invent subtractive forms beyond the six; the table prevents it.
- **Forgetting `break`/`if num == 0`** — harmless (later entries contribute `""`), but it wastes the tail of the loop.
- **Assuming the place-value version generalises** — `THOUSANDS` has exactly four entries.

**This same move shows up in:** [Roman to Integer](13-roman-to-integer.md) (the same table, parsed instead of built) · [Coin Change](322-coin-change.md) (where greedy on a value table *fails* — the contrast worth knowing) · [Excel Sheet Column Title](168-excel-sheet-column-title.md) (converting an integer to a non-standard positional system) · [Add Strings](415-add-strings.md) (building a digit string with `join`) · [Palindrome Number](9-palindrome-number.md) (digit extraction with `divmod`) · [Maximize Sum Of Array After K Negations](1005-maximize-sum-of-array-after-k-negations.md) (a greedy that needs its exchange argument stated).

</details>

---
