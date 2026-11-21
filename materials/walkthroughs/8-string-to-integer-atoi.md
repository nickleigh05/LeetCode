# 8. String to Integer (atoi)

**Medium** · [LeetCode](https://leetcode.com/problems/string-to-integer-atoi/) · [Solution file (no hints)](../../problems/0001-0499/8.py)

[📖 17. Math & Geometry lesson](../learning/19-math-geometry.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 17. Math & Geometry problems](../rmap-practice/17-math-geometry.md)

---

Implement `myAtoi(s)`, which converts a string to a 32-bit signed integer:

1. **Whitespace:** skip any leading spaces `' '`.
2. **Sign:** if the next character is `'-'` or `'+'`, read it. With no sign, the number is positive.
3. **Digits:** read digits until a non-digit or the end of the string. Leading zeros are fine. If no digits are read, the result is `0`.
4. **Rounding:** if the number is outside `[-2³¹, 2³¹ - 1]`, **clamp** it to the nearest bound.

```
s = "42"            →  42
s = "   -042"       →  -42
s = "1337c0d3"      →  1337       (stops at 'c')
s = "0-1"           →  0          (stops at '-')
s = "words and 987" →  0          (first non-space isn't a digit or sign)
s = "-91283472332"  →  -2147483648 (clamped)
```

**Constraints:** `0 <= s.length <= 200` · `s` contains English letters, digits, `' '`, `'+'`, `'-'` and `'.'`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

This problem is not about a clever algorithm. It's about **following a spec exactly**. Most failed attempts miss one of its rules, so read each rule as a step in a pipeline:

| The statement says | Which really means |
|---|---|
| skip leading whitespace | **Only** spaces, and **only** at the start. A space after the digits stops parsing |
| optional `'+'` or `'-'` | **At most one** sign, and only right after the whitespace. `"+-12"` → 0 |
| read digits **until a non-digit** | Stop at the first non-digit. Don't skip past it. `"12a34"` → 12 |
| no digits read → `0` | `"-"`, `"+"`, `"abc"` and `""` all give 0 |
| clamp to 32-bit range | Overflow returns `INT_MAX` or `INT_MIN`. It doesn't wrap or raise |

**The structure is a short pipeline with one index.** A single pointer `i` moves forward through four phases: spaces, sign, digits, done. Each phase advances `i` only while its condition holds.

**Overflow is the subtle part.** In Python, integers never overflow, so you could build the whole number and clamp at the end. But the interviewer often wants to see the check **before** the overflow happens, as you'd need in C++ or Java with 32-bit ints. The standard test is: before computing `result * 10 + digit`, check whether it would exceed `INT_MAX`.

🤔 **Before you open the next section:** to check `result * 10 + digit > INT_MAX` without ever computing a too-big number, how can you rearrange the inequality?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| `int(s.strip())` with try/except | Let Python parse it | — | — | ❌ Wrong rules: rejects `"12a"`, strips trailing space, accepts `"1_000"` |
| Regex `^ *[+-]?\d+` | Match the valid prefix, then convert and clamp | O(n) | O(n) | ⚠️ Correct, but hides the reasoning |
| Build in Python, clamp at end | Single pass, clamp once | O(n) | O(1) | ✅ Correct in Python only |
| **Single pass, check before overflow** | One index, four phases, overflow test before each digit | **O(n)** | **O(1)** | ✅ Correct in any language |

**The decision: a hand-written single pass with an index pointer**, checking for overflow *before* it happens.

**The overflow check, derived.** You want to know if `result * 10 + digit > INT_MAX` without computing the left side. Rearranged:

```
result * 10 + digit > INT_MAX
result * 10 > INT_MAX - digit
result > (INT_MAX - digit) / 10
```

With integer division the test becomes `result > (INT_MAX - digit) // 10`. Every value in it stays inside the 32-bit range, which is the whole point.

**Why one check covers both signs.** You accumulate the magnitude as a positive number. If the magnitude goes past `INT_MAX = 2147483647`, the positive answer clamps to `INT_MAX`. For negatives, `INT_MIN = -2147483648` has a magnitude one larger. So if the magnitude passes `2147483647`, the negative result is at or below `INT_MIN`, and clamping to `INT_MIN` is correct. Magnitude exactly `2147483648` with a minus sign clamps to `INT_MIN`, which is the same value anyway.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
INT_MAX = 2**31 - 1
INT_MIN = -2**31

i = 0
n = len(s)
```

The two bounds, and a single cursor `i` that will move forward through the phases. `**` is exponentiation, so `2**31 - 1` is 2147483647.
→ [arithmetic-operators](../syntax/arithmetic-operators.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
while i < n and s[i] == ' ':
    i += 1
```

**Phase 1: skip leading spaces.** `i < n` is checked **first**, so `s[i]` is never read past the end. That's short-circuit evaluation, and it's what makes an all-space string safe.
→ [while-loop](../syntax/while-loop.md) · [logical-operators](../syntax/logical-operators.md)

```python
sign = 1
if i < n and (s[i] == '-' or s[i] == '+'):
    if s[i] == '-':
        sign = -1
    i += 1
```

**Phase 2: at most one sign.** It's an `if`, not a `while`, so `"+-5"` reads the `+`, then sees `-` where a digit should be, and stops. The default `sign = 1` covers "no sign means positive."
→ [elif-else](../syntax/elif-else.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
result = 0
while i < n and '0' <= s[i] <= '9':
    digit = ord(s[i]) - ord('0')
```

**Phase 3: digits.** `'0' <= s[i] <= '9'` is a chained comparison on characters. Digits are consecutive in ASCII, so this is a digit test. `ord(s[i]) - ord('0')` turns the character into its value: `'7'` → 7.
→ [chained-comparisons](../syntax/chained-comparisons.md) · [ord-chr](../syntax/ord-chr.md)

```python
    if result > (INT_MAX - digit) // 10:
        if sign == 1:
            return INT_MAX
        return INT_MIN
```

**The overflow guard**, run before the multiply. If adding this digit would push the magnitude past `INT_MAX`, return the bound for the sign immediately. There's no need to read further digits, because the answer is already clamped.
→ [integer-division-modulo](../syntax/integer-division-modulo.md) · [if-return](../syntax/if-return.md)

```python
    result = result * 10 + digit
    i += 1

return sign * result
```

Shift the existing digits left one place and add the new one: building 1337 goes 1 → 13 → 133 → 1337. If no digits were read, `result` is still 0, and `sign * 0` is 0, which is the required answer.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def myAtoi(self, s: str) -> int:

        INT_MAX = 2**31 - 1
        INT_MIN = -2**31

        i = 0
        n = len(s)

        while i < n and s[i] == ' ':
            i += 1

        sign = 1
        if i < n and (s[i] == '-' or s[i] == '+'):
            if s[i] == '-':
                sign = -1
            i += 1

        result = 0
        while i < n and '0' <= s[i] <= '9':
            digit = ord(s[i]) - ord('0')

            if result > (INT_MAX - digit) // 10:
                if sign == 1:
                    return INT_MAX
                return INT_MIN

            result = result * 10 + digit
            i += 1

        return sign * result
```

</details>

**Trace it.** `s = "   -042"`:

| Phase | `i` | char | action | `sign` | `result` |
|---|---|---|---|---|---|
| spaces | 0→3 | `' '` ×3 | skip | 1 | 0 |
| sign | 3→4 | `-` | negative | −1 | 0 |
| digit | 4→5 | `0` | 0·10 + 0 | −1 | 0 |
| digit | 5→6 | `4` | 0·10 + 4 | −1 | 4 |
| digit | 6→7 | `2` | 4·10 + 2 | −1 | 42 |
| end | 7 | — | return −1 · 42 | | **−42** ✅ |

**The overflow trace.** `s = "2147483648"` (one more than `INT_MAX`): after nine digits `result = 214748364`. For the last digit 8, `(INT_MAX - 8) // 10 = 2147483639 // 10 = 214748363`. Since `214748364 > 214748363`, it returns **`INT_MAX`** ✅. The string `"2147483647"` passes the same check (`(INT_MAX - 7) // 10 = 214748364`, which isn't smaller) and returns exactly `INT_MAX`.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).** The index `i` only moves forward and never past `n`, and each step does O(1) work.

The overflow check can also return early, so a very long digit string stops after about 10 digits once it passes the bound.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).** A handful of integers: `i`, `sign`, `result`, `digit` and the two bounds.

No substrings are created. Calling `s.strip()` or slicing would copy the string and use O(n) space. The index pointer avoids that.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "This is a spec problem, so I'll follow it as a pipeline with one index. Skip leading spaces, read at most one sign, then read digits until a non-digit, building `result * 10 + digit`. Python ints don't overflow, but I'll check before the multiply so it works with 32-bit ints: if `result > (INT_MAX - digit) // 10`, I return INT_MAX or INT_MIN depending on the sign. No digits means result stays 0. O(n) time, O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why not just clamp at the end?" | That works in Python, but in a 32-bit language the intermediate value overflows before you can clamp. Checking first works everywhere. |
| "Why is one check enough for negatives?" | `INT_MIN`'s magnitude is `INT_MAX + 1`. Any magnitude above `INT_MAX` clamps to the right bound for its sign. |
| "Handle tabs and newlines as whitespace?" | Change the space check to `s[i].isspace()`. The spec here only skips `' '`. |
| "Support decimal points?" | Then it's float parsing, a different spec. `"3.14"` → 3 here, because `.` stops the digits. |
| "Reverse an integer with the same 32-bit rules?" | [Reverse Integer](7-reverse-integer.md) uses the same overflow guard. |

**Traps:**

- **`int(s.strip())`.** It rejects `"42abc"`, strips trailing spaces the spec doesn't care about, and accepts `"1_000"`.
- **Using `while` for the sign.** It accepts `"+-12"`, which should be 0.
- **Skipping spaces after the sign.** `"- 12"` is 0, because the space stops digit parsing.
- **Skipping non-digits mid-number.** `"12a34"` → 12, not 1234.
- **Reading `s[i]` without `i < n` first.** `"   "` or `"-"` raises `IndexError`.

**This same move shows up in:** [Reverse Integer](7-reverse-integer.md) (the same pre-overflow guard) · [Valid Palindrome](125-valid-palindrome.md) (character-class checks while scanning) · [Basic Calculator II](227-basic-calculator-ii.md) (building multi-digit numbers with `num * 10 + digit`) · [Add Strings](415-add-strings.md) (digit-by-digit arithmetic on strings).

</details>

---
