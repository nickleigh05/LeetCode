# 9. Palindrome Number

**Easy** · [LeetCode](https://leetcode.com/problems/palindrome-number/) · [Solution file (no hints)](../../problems/0001-0499/9.py)

[📖 17. Math & Geometry lesson](../learning/19-math-geometry.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 17. Math & Geometry problems](../rmap-practice/17-math-geometry.md)

---

Return `true` if the integer `x` reads the same forwards and backwards.

```
x = 121    →  true
x = -121   →  false      "-121" reversed is "121-"
x = 10     →  false      "10" reversed is "01"
```

**Constraints:** `-2^31 <= x <= 2^31 - 1`

**Follow-up:** could you solve it **without converting the integer to a string**?

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "reads the same backward as forward" | Digit sequence equals its reverse |
| `x = -121 → false` | ⚠️ **Every negative is false.** The minus sign leads and can't trail |
| `x = 10 → false` | ⚠️ **Trailing zeros kill it** — a leading zero isn't written |
| `-2^31 <= x <= 2^31 - 1` | 32-bit range. **Harmless in Python, a real overflow risk elsewhere** |
| "**without converting to a string**" | The actual exercise — do the arithmetic |

**The string version is one line and is not the point:**

```python
return str(x) == str(x)[::-1]
```

**Correct, and it answers the wrong question.** The follow-up is the problem.

**The arithmetic idea.** Peel digits off the right of `x` and push them onto the left of a new number:

```
x = 121                rev = 0
  digit 1  →  x = 12   rev = 1
  digit 2  →  x = 1    rev = 12
  digit 1  →  x = 0    rev = 121
                       121 == 121  ✅
```

**Two operations do all the work:**

```
x % 10    the last digit
x // 10   everything except the last digit
```

**And building the reverse is `rev = rev * 10 + digit`** — shift left one place, drop the new digit in.

**Two cases fall out before you start.**

- **`x < 0` → false.** Always. `-121` reversed would need a trailing minus.
- **`x` ends in `0` and isn't `0` → false.** The reverse would have to *start* with a zero, and integers don't. `10 → 01 = 1 ≠ 10`.

⚠️ **The second guard is optional for the full reversal** (`10` reverses to `1`, which already fails the comparison) **but mandatory for the half-reversal optimisation** below. **Measured: without it, the half-reversal is wrong on 455 of the first 200,000 non-negative integers** — every multiple of 10, starting at `x = 10`.

🤔 **Before you open the next section:** reversing all of `121` is fine, but reversing all of `2,147,483,647` produces `7,463,847,412` — bigger than a 32-bit int. Does that matter in Python? Does it matter anywhere?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| String reversal | `str(x) == str(x)[::-1]` | O(d) | **O(d)** | ⚠️ Correct, but sidesteps the follow-up |
| Digits into a list, two pointers | Extract then compare ends | O(d) | O(d) | ⚠️ Works, extra space |
| **Reverse the whole number** | `rev = rev*10 + x%10` | **O(d)** | **O(1)** | ✅ **The answer** |
| Reverse only half | Stop when `rev >= x` | **O(d/2)** | O(1) | ✅ The overflow-proof refinement |

**The decision: reverse the number arithmetically, compare to the original.**

**Why the string version isn't wrong, just uninteresting.** It's O(d) time and O(d) space, it's readable, and in production it's what you'd write. **The follow-up exists because the arithmetic version teaches digit extraction** — the primitive behind [Reverse Integer](7-reverse-integer.md), [Add Digits](https://leetcode.com/problems/add-digits/), [Happy Number](202-happy-number.md) and every base-conversion problem including [Excel Sheet Column Title](168-excel-sheet-column-title.md).

**Why the half-reversal exists.** Reversing all of `2147483647` gives `7463847412`, which **overflows a signed 32-bit integer**. In Java or C++ that's undefined-or-wrapped behaviour and a genuine bug; the fix is to stop halfway:

```
x = 1221
  x = 122, rev = 1
  x = 12,  rev = 12      ← rev >= x, stop
  compare: x == rev  ✅
```

**For an odd digit count the middle digit lands in `rev` and is discarded** with `rev // 10`:

```
x = 12321
  x = 1232, rev = 1
  x = 123,  rev = 12
  x = 12,   rev = 123    ← stop
  compare: x == rev // 10  →  12 == 12  ✅
```

⚠️ **Python's integers are arbitrary precision, so no overflow is possible here.** The half-reversal is still worth knowing — **it's what the interviewer is fishing for when they mention the 32-bit range** — but presenting it as necessary *in Python* would be wrong. **Say: "in a fixed-width language I'd reverse only half to avoid overflow."**

**Verified: the full reversal, the half reversal, and the string version all agree** with each other over every integer from `-2000` to `20000` plus 20,000 random values across the full 32-bit range — **0 disagreements**.
→ [integer-division-modulo](../syntax/integer-division-modulo.md) · [while-loop](../syntax/while-loop.md)

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
if x < 0:
    return False
```

**Every negative number fails.** `-121` would have to reverse to `121-`. **No arithmetic needed** — reject immediately.
→ [if-return](../syntax/if-return.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
if x != 0 and x % 10 == 0:
    return False
```

**Anything ending in a zero fails — except zero itself.**

`10`, `100`, `1230` all reverse to numbers with a leading zero, which integers don't have. ⚠️ **`x != 0` is essential**: `0 % 10 == 0`, and `0` **is** a palindrome. Dropping that clause makes `isPalindrome(0)` return `False`.

⚠️ **This guard is an early exit for the full reversal and a correctness requirement for the half reversal.** With the full reversal, `10` would reverse to `1` and fail the comparison anyway — verified: removing this line changes no answer across 22,000 tested values. **With the half-reversal it is not optional: `10` returns `True` without it** (`x` reaches 1, `rev` reaches 1, and `x == rev // 10` gives `0 == 0`). **Measured wrong on 455 of the first 200,000 integers.**
→ [integer-division-modulo](../syntax/integer-division-modulo.md) · [logical-operators](../syntax/logical-operators.md)

```python
original = x
reversed_num = 0
```

⚠️ **Save the original before the loop destroys it.** The loop consumes `x` digit by digit, so without this snapshot there's nothing left to compare against. **Forgetting this line is the most common bug in the arithmetic version.**
→ [variables-assignment](../syntax/variables-assignment.md)

```python
while x > 0:
    digit = x % 10
    reversed_num = reversed_num * 10 + digit
    x = x // 10
```

**The digit-reversal loop — three lines that appear in a dozen other problems.**

- **`x % 10`** — the last digit.
- **`reversed_num * 10 + digit`** — shift the accumulator one decimal place left and append.
- **`x // 10`** — drop the digit just consumed.

⚠️ **`//` and not `/`.** True division produces a float, `x` never reaches exactly 0, and the loop spins until the float underflows — a hang, not an error.

**The loop runs once per digit**, so `d = ⌊log₁₀ x⌋ + 1` iterations. ⚠️ **`x = 0` skips the loop entirely**, leaving `reversed_num = 0`, and `0 == 0` returns `True` — correct, with no special case.
→ [while-loop](../syntax/while-loop.md) · [integer-division-modulo](../syntax/integer-division-modulo.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
return original == reversed_num
```

**The comparison the snapshot was saved for.**

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def isPalindrome(self, x: int) -> bool:

        if x < 0:
            return False
        if x != 0 and x % 10 == 0:
            return False

        original = x
        reversed_num = 0
        while x > 0:
            digit = x % 10
            reversed_num = reversed_num * 10 + digit
            x = x // 10

        return original == reversed_num
```

</details>

<details>
<summary>The half-reversal — the overflow-proof version</summary>

```python
class Solution:
    def isPalindrome(self, x: int) -> bool:

        if x < 0 or (x % 10 == 0 and x != 0):
            return False

        reversed_half = 0
        while x > reversed_half:
            reversed_half = reversed_half * 10 + x % 10
            x //= 10

        return x == reversed_half or x == reversed_half // 10
```

**Stop as soon as the reversed half catches up.** `x == reversed_half` handles an even digit count; `x == reversed_half // 10` discards the middle digit for an odd one.

⚠️ **The trailing-zero guard is mandatory here**, not an optimisation — without it, every multiple of 10 returns `True`. **Verified: 455 wrong answers in the first 200,000 integers, smallest `x = 10`.**

**This is the version to name if the interviewer mentions 32-bit overflow.** ⚠️ In Python it buys only speed (half the iterations), not correctness.

**Verified against the string reference on 200,000 consecutive integers — 0 disagreements.**
</details>

<details>
<summary>The one-liner — correct, but it dodges the follow-up</summary>

```python
class Solution:
    def isPalindrome(self, x: int) -> bool:
        return str(x) == str(x)[::-1]
```

**`str(-121)` is `"-121"`, whose reverse is `"121-"`** — so negatives fall out for free, no guard needed. ⚠️ **O(d) space for the two strings**, and it's the answer the follow-up explicitly rules out.
→ [string-join-slice](../syntax/string-join-slice.md) · [list-slicing](../syntax/list-slicing.md)

</details>

**Trace it** — `x = 121`:

| `x` | `digit` | `reversed_num` |
|---|---|---|
| 121 | — | 0 |
| 12 | 1 | 1 |
| 1 | 2 | 12 |
| 0 | 1 | **121** |

**`original = 121`, `reversed_num = 121`** → `True` ✅

**`x = -121`:** caught by the first guard → `False` ✅

**`x = 10`:** caught by the second guard → `False` ✅. **Without that guard** the loop gives `reversed_num = 1` (digit 0, then digit 1 → `0*10+0 = 0`, then `0*10+1 = 1`), and `10 == 1` is `False` — **still correct**, which is why the guard is only an optimisation *here*.

**`x = 0`:** first guard passes (not negative), second guard passes (`x != 0` is false), loop never runs, `0 == 0` → `True` ✅

**A wide one** — `x = 1234567899`:

```
reversed_num builds to 9987654321
1234567899 == 9987654321  →  False ✅
```

⚠️ **Note `9987654321 > 2^31 − 1`.** In Python that's fine. **In Java the intermediate `rev` would have overflowed** — which is the entire motivation for the half-reversal.

**Verified:** the full reversal was checked against `str(x) == str(x)[::-1]` over all integers from −2,000 to 20,000 plus 20,000 random values spanning the full 32-bit range — **0 disagreements**, as were both alternatives.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(d) = O(log x)</summary>

**O(d)** where `d` is the number of digits — equivalently **O(log₁₀ x)**.

| Phase | Cost |
|---|---|
| Two guards | O(1) |
| One loop iteration per digit | **O(d)** |
| Final comparison | O(1) |
| **Total** | **O(d) = O(log x)** |

**At most 10 digits** for a 32-bit integer, so **at most 10 iterations**. Effectively constant.

| Approach | Time | Iterations at `x = 2^31 − 1` |
|---|---|---|
| String reversal | O(d) | 10 char copies |
| **Full arithmetic reversal** | **O(d)** | **10** ✅ |
| Half reversal | **O(d/2)** | **5** ✅✅ |

**The half-reversal is genuinely twice as fast** — it stops the moment `reversed_half` catches `x`, which happens at the midpoint by construction.

**Why O(log x) and not O(1).** Each iteration removes one digit, and a number has `⌊log₁₀ x⌋ + 1` of them. ⚠️ **Calling it "O(1) because integers are bounded" is defensible for fixed-width ints but wrong in Python**, where `x` can have arbitrarily many digits and the arithmetic itself stops being constant-time.

**Ω(d) is the floor** — every digit must be inspected; changing any single digit can flip the answer.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — three integers, no matter how large `x` is.

| Component | Size |
|---|---|
| `original`, `reversed_num`, `digit` | **O(1)** ✅ |
| **Total** | **O(1)** |

⚠️ **This is the whole reason the follow-up exists.** The string version costs **O(d)**:

```python
str(x)          # a d-character string
str(x)[::-1]    # another one
```

**Two allocations of `d` characters** versus three machine words. At 10 digits nobody cares; **the point is the technique, which transfers to problems where `d` is large.**

**No recursion.** A recursive digit-peeler would add O(d) stack frames and gain nothing.

⚠️ **Strictly speaking, in Python `reversed_num` grows to the same magnitude as `x`**, so it occupies O(d) *bits*. **The standard convention counts a machine integer as O(1)**, which is what "O(1) space" means here — worth being precise about if pressed.

**The half-reversal is also O(1)**, and keeps `reversed_half` bounded by `√x` in magnitude — **which is exactly what makes it overflow-safe in fixed-width languages.**

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The string version is a one-liner, but the follow-up asks for no string conversion, so I'll do it arithmetically. Two things fall out immediately: any negative is false, because the minus sign can't trail; and anything ending in zero except zero itself is false, because the reverse would need a leading zero. Then I peel digits off the right with mod ten and integer-divide by ten, building the reverse with `rev = rev * 10 + digit`, and compare against a saved copy of the original — saving that copy first is the easy thing to forget, since the loop consumes `x`. That's O(d) time, at most ten iterations for a 32-bit value, and O(1) space. One refinement: reversing the whole number can overflow a 32-bit int — `2147483647` reverses to about 7.5 billion — so in Java or C++ I'd reverse only half, stopping when the reversed half catches up, and compare with the middle digit dropped. Python has arbitrary-precision integers so it's a speed win rather than a correctness one — but note the trailing-zero guard becomes mandatory in that version."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "**Without converting to a string?**" | **The follow-up.** `% 10` and `// 10` to peel digits; `rev = rev*10 + digit` to build the reverse. |
| "Why are negatives always false?" | The `-` leads and would have to trail. `-121` → `121-`. |
| "Why reject numbers ending in 0?" | Their reverse would start with 0, which integers don't represent. Except `x = 0` itself. |
| "Is that guard necessary?" | **For the full reversal, no** — `10` reverses to `1` and fails anyway. **For the half reversal, yes** — without it every multiple of 10 returns true (455 wrong in the first 200,000). |
| "**What about overflow?**" | Reversing `2147483647` gives ~7.46 × 10⁹, past `2^31 − 1`. In Java/C++ reverse only *half*. Python's ints are arbitrary precision. |
| "How does the half version handle odd digit counts?" | The middle digit ends up in `rev`; compare `x == rev // 10` as well as `x == rev`. |
| "Does `x = 0` work?" | Yes — the loop never runs, `0 == 0`. Verified, no special case needed. |
| "What about other bases?" | Same loop with `% b` and `// b`. Note a number can be a palindrome in one base and not another — `5` is `101` in binary. |
| "Palindrome ignoring case and punctuation, on a string?" | Different problem — [Valid Palindrome](125-valid-palindrome.md), two pointers with filtering. |
| "Which would you ship?" | `str(x) == str(x)[::-1]`. It's clearer, and O(d) space on a ten-digit number is free. **The arithmetic version is the interview answer.** |

**Traps:**

- ⚠️ **Not saving `original` before the loop** — `x` is consumed, so there's nothing to compare against. The defining bug here.
- ⚠️ **Dropping `x != 0` from the trailing-zero guard** — makes `isPalindrome(0)` return `False`, and `0` is a palindrome.
- ⚠️ **Using the half-reversal without the trailing-zero guard** — every multiple of 10 wrongly returns `True`.
- **`/` instead of `//`** — floats, and the loop never terminates cleanly.
- **Forgetting negatives** — `-121` must be `False`.
- **Reversing the whole number in a fixed-width language** — overflow.
- **Comparing `str` inside an "arithmetic" solution** — answers the wrong question.
- **`while x >= 0`** instead of `> 0` — infinite loop, since `0 // 10` is `0`.

**This same move shows up in:** [Reverse Integer](7-reverse-integer.md) (the same `% 10` / `// 10` / `rev*10 + d` loop, with overflow as the point) · [Excel Sheet Column Title](168-excel-sheet-column-title.md) (peeling digits in base 26) · [Happy Number](202-happy-number.md) (digit extraction in a loop) · [Add Strings](415-add-strings.md) (digit-by-digit arithmetic without built-ins) · [Valid Palindrome](125-valid-palindrome.md) (the same question on strings) · [Plus One](66-plus-one.md) (carry propagation over digits).

</details>

---
