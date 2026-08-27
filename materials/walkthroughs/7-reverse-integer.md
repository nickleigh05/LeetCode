# 7. Reverse Integer

**Medium** · [LeetCode](https://leetcode.com/problems/reverse-integer/)

[📖 18. Bit Manipulation lesson](../learning/18-bit-manipulation.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 18. Bit Manipulation problems](../rmap-practice/18-bit-manipulation.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Given a **signed 32-bit** integer `x`, return `x` with its **digits reversed**. If reversing causes the value to fall **outside** the range `[−2³¹, 2³¹ − 1]`, return **0**.

Assume the environment does **not** allow storing 64-bit integers.

```
x = 123     →  321
x = -123    →  -321      the sign is preserved, not reversed
x = 120     →  21        trailing zeros vanish
x = 1534236469  →  0     reversed is 9646324351, which overflows
```

**Constraints:** `-2³¹ <= x <= 2³¹ − 1`.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| reverse the **digits** | Decimal digits, not bits — so `% 10` and `// 10`, the same idiom as [Happy Number](202-happy-number.md) |
| **signed** 32-bit | Negatives are in scope, and the sign must be preserved rather than reversed |
| return **0** on overflow | The real content of the problem. Reversing can push a valid input out of range |
| "cannot store 64-bit integers" | You're forbidden from computing the result in a wider type and *then* checking. **The check must happen before or during the reversal** in a strict reading |
| range is **asymmetric** | `[−2147483648, 2147483647]` — the negative bound is one larger in magnitude. That asymmetry catches naive checks |

The reversal itself is the standard digit loop:

- **`x % 10`** — take the last digit.
- **`x //= 10`** — drop it.
- **`result = result * 10 + digit`** — append it to the growing result.

That third line is the reversal: each new digit is pushed onto the *low* end of `result` while everything already there shifts up a place. The **first** digit extracted (the input's last) ends up multiplied by the highest power of ten — so it lands at the front.

Two details need care.

**Trailing zeros vanish, and that's correct.** `120` reverses to `021`, which as a number is `21`. The `result * 10 + digit` construction handles this automatically: leading zeros in a number simply aren't represented.

**The overflow check is the actual problem.** `1534236469` is a perfectly valid 32-bit integer, but reversed it's `9646324351` — beyond 2³¹ − 1. So the answer is 0.

And the range is **asymmetric**: `−2³¹ = −2147483648` but `2³¹ − 1 = 2147483647`. A check like `abs(result) > 2**31 - 1` would wrongly reject a result of exactly `−2147483648`. **Both bounds must be tested separately.**

🤔 **Before you open the next section:** the problem says you can't store 64-bit integers, yet the solution below computes the full reversed value and *then* range-checks it. Is that cheating — and what would a strict implementation look like?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| String reversal | `int(str(abs(x))[::-1]) * sign` | O(d) | **O(d)** | ⚠️ Works, and it's short — but it allocates, and it sidesteps the arithmetic the problem is about |
| **Digit loop, check at the end** | Build the result, then range-check | **O(d)** | **O(1)** | ✅ |
| Digit loop, check **before each append** | Test whether the next `result * 10 + digit` would overflow *before* computing it | O(d) | O(1) | ✅ The strict answer — no oversized value ever exists |

**The decision:** the **digit loop with a range check**, noting the pre-check variant as the strictly-compliant form.

**Is checking at the end cheating?** — the answer to section 1's question. Partly, and it's worth being honest about.

In Python, integers are arbitrary-precision, so `result` can hold `9646324351` without difficulty and the final comparison is valid. **In C or Java, that intermediate value would already have overflowed** — wrapping to garbage — and the check would test a corrupted number. So the end-check version is correct *in Python* and would be wrong in a fixed-width language.

**The strictly-portable version checks before appending:**

```python
if result > (INT_MAX - digit) // 10:
    return 0
result = result * 10 + digit
```

This asks *"would this multiplication overflow?"* using only values already known to be in range — division rather than multiplication, so nothing oversized is ever computed. **That's what you'd write in C.**

Which to present? Write the readable end-check version, then say: *"this relies on Python's arbitrary-precision integers; in a fixed-width language I'd check before the multiplication, since the intermediate would already have overflowed."* **Naming the limitation is worth more than silently writing either one.**

**Why handle the sign separately** rather than relying on Python's `%` and `//` for negatives? Because Python's modulo **follows the sign of the divisor**, not the dividend:

```python
-123 % 10   →  7     not -3
-123 // 10  →  -13   floors toward negative infinity, not toward zero
```

So the digit loop on a negative number produces wrong digits. Extracting the sign and working with `abs(x)` sidesteps it entirely. **In C, `%` truncates toward zero and `-123 % 10` is `-3`, so the loop works directly on negatives** — another language difference worth knowing.

**Why not the string version?** `int(str(abs(x))[::-1])` is genuinely concise and correct. But it allocates O(d) for the string and treats the number as text rather than doing arithmetic — and the problem is in the bit-manipulation unit precisely to exercise digit extraction.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
sign = -1 if x < 0 else 1
x = abs(x)
```
**Extract the sign and work with the magnitude.**

This isn't cosmetic — it's a correctness requirement in Python. Because Python's `%` returns a result with the **divisor's** sign, `-123 % 10` is `7`, not `-3`, and `-123 // 10` floors to `-13` rather than truncating to `-12`. **Running the digit loop directly on a negative number would produce nonsense.**

Taking `abs(x)` makes every subsequent operation work on a non-negative value, and the sign is reapplied at the end.

The [ternary](../syntax/ternary-expression.md) reads directly as "negative if x is negative, otherwise positive."
→ [ternary-expression](../syntax/ternary-expression.md) · [integer-division-modulo](../syntax/integer-division-modulo.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
result = 0
while x:
```
The accumulator, and a loop that runs until every digit has been consumed. `while x:` relies on `0` being [falsy](../syntax/truthy-falsy-values.md) — the loop ends when the division has exhausted the number.

Note this correctly handles `x = 0`: the loop body never executes and `result` stays 0.
→ [while-loop](../syntax/while-loop.md) · [truthy-falsy-values](../syntax/truthy-falsy-values.md)

```python
    digit = x % 10
    x //= 10
```
**Peel off the last digit and discard it** — the standard extraction idiom, identical to [Happy Number](202-happy-number.md) and [Number of 1 Bits](191-number-of-1-bits.md)'s decimal cousin.

`% 10` gives the units digit; `//= 10` shifts everything right by one decimal place.
→ [integer-division-modulo](../syntax/integer-division-modulo.md)

```python
    result = result * 10 + digit
```
**The reversal itself.**

Multiplying `result` by 10 shifts every digit already collected **up** one place, opening a slot at the bottom for the new digit. So digits enter at the low end and get pushed leftward as more arrive.

The consequence: the **first** digit extracted — the input's *last* digit — is multiplied by 10 once per remaining iteration, ending up in the highest position. **The order inverts automatically**, which is why no explicit index arithmetic is needed.

This is also where trailing zeros disappear. For `120`, the first digit is 0, so `result = 0 * 10 + 0 = 0` — the zero contributes nothing and simply never appears in the output.
→ [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
result *= sign
```
Reapply the sign that was stripped at the start. `-123` → magnitude reversed to `321` → **−321**.
→ [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
INT_MIN = -2**31
INT_MAX = 2**31 - 1
if result < INT_MIN or result > INT_MAX:
    return 0
```
**The overflow check, with both bounds tested separately.**

The 32-bit signed range is **asymmetric**: `−2147483648` to `2147483647`. Testing `abs(result) > INT_MAX` would wrongly reject a legitimate result of exactly `INT_MIN` — so each bound needs its own comparison.

Naming the constants rather than inlining `2**31` makes the intent obvious and the boundary auditable.

**As noted in section 2, this check happens *after* the full value exists**, which is valid in Python but wouldn't be in a fixed-width language.
→ [comparison-operators](../syntax/comparison-operators.md) · [logical-operators](../syntax/logical-operators.md) · [if-return](../syntax/if-return.md)

```python
return result
```
→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def reverse(self, x: int) -> int:

        sign = -1 if x < 0 else 1
        x = abs(x)

        result = 0
        while x:
            digit = x % 10
            x //= 10
            result = result * 10 + digit

        result *= sign

        INT_MIN = -2**31
        INT_MAX = 2**31 - 1
        if result < INT_MIN or result > INT_MAX:
            return 0

        return result
```
</details>

**Trace it** — `x = -123` (expected −321)

`sign = -1`, `x = 123`.

| iteration | `x` | `digit = x % 10` | `x` after `//= 10` | `result * 10 + digit` | `result` |
|---|---|---|---|---|---|
| 1 | 123 | **3** | 12 | 0 × 10 + 3 | **3** |
| 2 | 12 | **2** | 1 | 3 × 10 + 2 | **32** |
| 3 | 1 | **1** | 0 | 32 × 10 + 1 | **321** |
| — | 0 → loop ends | | | | |

`result *= sign` → **−321**. In range → return **−321** ✅

The digit `3` was extracted first and ended up multiplied by 100 (once per subsequent iteration), landing at the front. **That's the reversal, produced by the arithmetic rather than by any explicit repositioning.**

**And trailing zeros** — `x = 120`:

| iteration | `x` | `digit` | `x` after | `result` |
|---|---|---|---|---|
| 1 | 120 | **0** | 12 | 0 × 10 + 0 = **0** |
| 2 | 12 | **2** | 1 | 0 × 10 + 2 = **2** |
| 3 | 1 | **1** | 0 | 2 × 10 + 1 = **21** |

Return **21** ✅ — the leading zero of `021` simply has no representation as a number, and the `result * 10 + digit` form never creates one.

**And the overflow case** — `x = 1534236469`:

The loop builds `9646324351` digit by digit. Then:

```
INT_MAX = 2147483647
9646324351 > 2147483647  ✓  → return 0
```

Return **0** ✅

In Python that intermediate value exists without difficulty. **In C, the multiplication would have wrapped around long before the check ran** — which is exactly why the strict version tests `result > (INT_MAX - digit) // 10` *before* each append.

**And the asymmetric boundary** — `x = -2147483648` (which is `INT_MIN`):

`sign = -1`, `abs(x) = 2147483648`. Reversing the digits gives `8463847412`, then `× -1` = `-8463847412`. That's below `INT_MIN`, so return **0** ✅

</details>

<details>
<summary><b>4 · Time complexity</b> — O(log₁₀ x)</summary>

**O(d)**, where d is the number of digits — equivalently **O(log₁₀ x)**.

- The loop removes one digit per iteration, and a number `x` has **⌊log₁₀ x⌋ + 1** digits.
- Each iteration does a modulo, a floor division, a multiplication, and an addition — all **O(1)**.
- **O(log x)** total.

For a 32-bit integer that's **at most 10 iterations**, so it's effectively O(1) given the constraints.

**Against the string version:** `str(abs(x))[::-1]` is also O(d) — converting to a string touches every digit, and reversing touches them again. Same asymptotic cost, but with allocation overhead the arithmetic version avoids.

**Faster?** No. Every digit must be read to be repositioned, so **Ω(d)** is a lower bound.

**No early exit** — the loop can't terminate before consuming every digit, since the last digit extracted becomes the most significant. Even in the overflow case, this implementation builds the full value first. **The strict pre-checking variant *can* exit early**, returning 0 the moment it detects the next multiplication would overflow — a small practical improvement on top of being portable.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — four integers (`sign`, `x`, `result`, `digit`) plus two named constants. Nothing is allocated.

| Approach | Space | Why |
|---|---|---|
| String reversal | **O(d)** | Builds a string of up to 11 characters |
| **Digit arithmetic** | **O(1)** | Scalars only |

The string version's O(d) is bounded (11 characters at most) so it hardly matters in practice — but the arithmetic version genuinely allocates nothing, and in a language without garbage collection that difference is real.

**A Python caveat worth stating:** `result` can temporarily hold values outside the 32-bit range — `9646324351` in the overflow example. Python accommodates that transparently, but it means **the algorithm as written is relying on a language feature the problem statement explicitly disallows** ("cannot store 64-bit integers").

**The strictly-compliant version** never creates an oversized value:

```python
if result > (INT_MAX - digit) // 10:
    return 0
result = result * 10 + digit
```

The condition uses **division** on values already known to be in range, so it answers "would this multiplication overflow?" without performing it. **That's O(1) space in the strong sense** — no intermediate ever exceeds the representable range.

Worth writing the readable version and mentioning this one, rather than the reverse: the pre-check is harder to read and its correctness argument is less obvious, so it's better as a stated refinement than as the primary answer.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The reversal is the standard digit loop: take the last digit with `% 10`, drop it with `// 10`, and build the result as `result * 10 + digit`. That inverts the order automatically, because the first digit extracted gets multiplied by ten once per remaining iteration and ends up at the front. I extract the sign and work with the absolute value, because Python's modulo takes the sign of the divisor — `-123 % 10` is 7, not −3 — so the loop would produce wrong digits on negatives. Trailing zeros disappear on their own, since a leading zero has no numeric representation. The real content is the overflow check: the range is asymmetric, −2³¹ to 2³¹−1, so I test both bounds separately rather than using `abs`. One honest caveat — I'm building the full value and then checking it, which works because Python has arbitrary-precision integers. In C the multiplication would already have overflowed, so I'd check `result > (INT_MAX - digit) // 10` *before* each append instead."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why handle the sign separately?" | Python's `%` takes the divisor's sign, so `-123 % 10` is 7 and `-123 // 10` floors to −13. The digit loop would produce garbage. In C, `%` truncates toward zero and the loop works directly on negatives. |
| "Isn't checking overflow at the end cheating?" | In Python it's valid, since the intermediate fits. In a fixed-width language it wouldn't — you'd check `result > (INT_MAX - digit) // 10` before multiplying, using only in-range values. |
| "Why test both bounds instead of `abs(result) > INT_MAX`?" | The range is asymmetric: −2147483648 to 2147483647. An `abs` check would wrongly reject a legitimate result of exactly INT_MIN. |
| "What happens to trailing zeros?" | They vanish, correctly — `120` → `21`. A leading zero has no numeric representation, and `result * 10 + 0` contributes nothing. |
| "Why not just reverse the string?" | `int(str(abs(x))[::-1]) * sign` works and is shorter, but it allocates and treats the number as text rather than exercising digit arithmetic. |
| "Can you exit early on overflow?" | With the pre-check version, yes — return 0 as soon as the next multiplication would overflow, without finishing the loop. |
| "What about `x = 0`?" | The loop never runs, `result` stays 0, and 0 is returned. No special case needed. |
| "What if the environment had 64-bit integers?" | Then the end-check is entirely legitimate — build the reversed value in a `long` and range-check it. The restriction is what forces the pre-check. |

**Traps:**
- **Running the digit loop on a negative number in Python.** `-123 % 10` is 7, and the result is wrong in a way that's easy to miss if you only test positives.
- **Using `abs(result) > INT_MAX`** — rejects a valid `INT_MIN` result because of the asymmetric range.
- **Forgetting the overflow check entirely** — returns oversized values that should be 0.
- Checking overflow before reapplying the sign, which misreads which bound applies.
- Assuming trailing zeros need special handling. They don't.
- Using `int(str(x)[::-1])` on a negative without stripping the sign — the `-` ends up at the *end* of the string and the conversion fails.

**This same move shows up in:** [Happy Number](202-happy-number.md) (the same `% 10` / `// 10` digit-extraction idiom) · [Plus One](66-plus-one.md) (digit-level arithmetic with careful boundary handling) · [Reverse Bits](190-reverse-bits.md) (the same reversal shape, on bits instead of digits, with the same fixed-width simulation issue) · [Multiply Strings](43-multiply-strings.md) (arithmetic on a number's representation rather than its value).

</details>

---
