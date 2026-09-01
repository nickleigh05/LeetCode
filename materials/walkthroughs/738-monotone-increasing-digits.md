# 738. Monotone Increasing Digits

**Medium** · [LeetCode](https://leetcode.com/problems/monotone-increasing-digits/) · [Solution file (no hints)](../../problems/0500-0999/738.py)

[📖 16. Greedy lesson](../learning/16-greedy.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 15. Greedy problems](../rmap-practice/15-greedy.md)

---

Return the **largest** number `≤ n` whose digits are **monotone increasing** (each digit ≤ the next).

```
n = 10    →  9
n = 1234  →  1234      already monotone
n = 332   →  299
```

**Constraints:** `0 <= n <= 10^9`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "each pair `x <= y`" | Non-strict — `1123` is fine, repeated digits allowed |
| "**largest** number ≤ n" | Stay as close to `n` as possible |
| `n <= 10^9` | ⚠️ Only **10 digits**. Counting down from `n` is 10⁹ steps — far too slow |
| `0 <= n` | `n = 0` is legal and returns 0 |

**Work on the digits, not the number.** With at most 10 digits, the whole problem is a short string manipulation.

**Where a violation occurs, and what to do about it:**

```
n = 332

digits:  3  3  2
              ↑ 3 > 2 — violation at this pair
```

**You must reduce something.** The largest number ≤ 332 that's monotone can't start `33`, because any `33x` needs `x ≥ 3`, making it > 332. **So the prefix must come down**:

```
borrow: reduce the 3 before the violation to 2  →  3 2 ?
then maximise the rest: set everything after to 9  →  3 2 9  = 329?
```

⚠️ **But `329` isn't monotone** — `3 > 2`. **Lowering one digit can create a new violation to its left**, which is why a single pass isn't enough:

```
3 3 2  →  lower the second 3  →  3 2 9   ✗ now 3 > 2
       →  lower the first 3   →  2 9 9   ✓ 299 ✅
```

> **Scan right to left, and each time `digits[i-1] > digits[i]`, decrement `digits[i-1]` and remember that everything from position `i` onward becomes 9.**

**Right-to-left is what makes one pass sufficient.** A decrement at position `i-1` can only create a violation with position `i-2`, which the scan visits **next** — so cascading fixes happen naturally.

```
n = 332,  scanning i = 2 then i = 1

i=2:  digits[1]=3 > digits[2]=2  →  digits[1] = 2,  mark = 2     [3,2,2]
i=1:  digits[0]=3 > digits[1]=2  →  digits[0] = 2,  mark = 1     [2,2,2]
then set positions 1.. to 9                                       [2,9,9] = 299 ✅
```

⚠️ **`mark` must track the *leftmost* position where the nines begin.** Each new violation moves it further left, and only the final value is used.

🤔 **Before you open the next section:** why set the suffix to all 9s rather than leaving the original digits? And why is that always still ≤ n?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Count down from `n` | Test each for monotonicity | O(n · d) | O(1) | ❌ 10⁹ iterations |
| Construct digit by digit with backtracking | Try each position | O(d · 10) | O(d) | ✅ Works, more code |
| **Right-to-left scan + fill with 9s** | One pass | **O(d)** | **O(d)** | ✅ ← |

**The decision: the right-to-left scan.** With `d ≤ 10` it's essentially constant time.

**Why right-to-left rather than left-to-right.** A left-to-right scan finds the *first* violation, but fixing it may break something to the left — which it has already passed:

```
n = 3321,  left-to-right

first violation at index 1 (3 > 2). Lower digits[1] to 2 → 3 2 9 9
                                    ⚠️ now digits[0]=3 > digits[1]=2 — already passed it
```

**You'd have to restart or scan again.** Right-to-left visits position `i-2` immediately after modifying `i-1`, so the cascade resolves in the same pass.

**Why the suffix becomes all 9s.** Once a digit has been decremented, the number is already strictly below `n`'s prefix — so **every later digit is free to be as large as possible**, and 9 is both the largest digit and trivially ≥ its predecessor:

```
n = 332
after lowering to 2 at position 0: any number starting "2" is < 332
                                   so 299 is safe, and it's the largest such
```

⚠️ **This is the greedy's key argument.** You lose nothing by maximising the suffix, because the prefix decrement already guarantees you're under `n`.

**Why `mark` starts at `len(digits)`.** If no violation is found, the fill loop `range(mark, len(digits))` is **empty** — leaving `n` unchanged:

```python
mark = len(digits)          # "no nines needed"
```

**That's how `n = 1234` returns 1234 with no special case.**

**The counting-down approach** deserves a moment: it's the natural brute force, and at `n = 10⁹` it's up to a billion iterations each doing a 10-digit check. ⚠️ **The `n <= 10^9` constraint is precisely what rules it out** — but note that a *good* answer is often found quickly (monotone numbers aren't that rare), so it might pass weak tests and fail on adversarial ones like `n = 999999999` minus a little.

**A subtlety with leading zeros.** After the cascade, the first digit may become 0:

```
n = 100  →  digits [1,0,0]
i=2: 0 > 0? no
i=1: 1 > 0 → digits[0] = 0, mark = 1
result: [0, 9, 9] = "099"
int("099") = 99 ✅
```

⚠️ **`int()` discards the leading zero automatically** — no special handling needed, which is a genuine convenience of working with strings and converting at the end.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
digits = list(str(n))
mark = len(digits)
```

**Convert to a mutable list of digit characters.**

⚠️ **`mark = len(digits)`** means "no positions need to become 9". If no violation is found, the fill loop below does nothing.
→ [type-conversion](../syntax/type-conversion.md) · [string-basics](../syntax/string-basics.md) · [list-basics](../syntax/list-basics.md)

```python
for i in range(len(digits) - 1, 0, -1):
```

**Scan right to left**, comparing each digit to the one before it.

⚠️ **Stops at `i = 1`** (the `0` bound is exclusive), because the comparison uses `digits[i-1]` — going to `i = 0` would index `digits[-1]`, the last digit.
→ [range-function](../syntax/range-function.md) · [for-loop](../syntax/for-loop.md)

```python
        if digits[i-1] > digits[i]:
            digits[i-1] = str(int(digits[i-1]) - 1)
            mark = i
```

**A violation: borrow from the left.**

⚠️ **Comparing characters works here** because `'0'` through `'9'` are consecutive in ASCII, so string comparison matches numeric comparison **for single digits**. (It would break for multi-character strings — `'10' < '9'` — but every element here is one character.)

The decrement needs a round-trip through `int` since the digits are stored as strings.

⚠️ **`mark = i`, not `mark = min(mark, i)`.** The scan moves leftward, so each new violation has a *smaller* `i` — the assignment naturally keeps the leftmost. **Using `min` would be equivalent but redundant.**
→ [comparison-operators](../syntax/comparison-operators.md) · [type-conversion](../syntax/type-conversion.md)

```python
for i in range(mark, len(digits)):
    digits[i] = '9'
```

**Everything from `mark` onward becomes 9** — the largest possible suffix, safe because the prefix decrement already put the number below `n`.

```python
return int(''.join(digits))
```

**Rejoin and convert.** ⚠️ `int()` strips any leading zero produced by the cascade.
→ [string-join-slice](../syntax/string-join-slice.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def monotoneIncreasingDigits(self, n: int) -> int:

        digits = list(str(n))
        mark = len(digits)

        for i in range(len(digits) - 1, 0, -1):
            if digits[i-1] > digits[i]:
                digits[i-1] = str(int(digits[i-1]) - 1)
                mark = i

        for i in range(mark, len(digits)):
            digits[i] = '9'

        return int(''.join(digits))
```

</details>

**Trace it** — `n = 332`. Verified output:

| Step | `i` | Comparison | Action | `digits` | `mark` |
|---|---|---|---|---|---|
| init | — | — | — | `['3','3','2']` | 3 |
| 1 | 2 | `digits[1]='3' > digits[2]='2'` ✓ | decrement, mark | `['3','2','2']` | **2** |
| 2 | 1 | `digits[0]='3' > digits[1]='2'` ✓ | decrement, mark | `['2','2','2']` | **1** |
| fill | — | positions 1..2 → `'9'` | | `['2','9','9']` | |

**Result: `299`** ✅

**Step 2 is the cascade** — and it's why right-to-left matters. Lowering `digits[1]` from 3 to 2 in step 1 **created** the violation `3 > 2` at positions 0–1, and the scan hits it immediately on the next iteration. **A left-to-right pass would have already moved past position 0.**

**Note `mark` moved from 2 to 1**, so the nines start one position further left — `299`, not `329`. **The final `mark` is the leftmost violation point after all cascading.**

**Example 1** (`n = 10`):

```
digits: ['1','0'],  mark = 2
i=1:  '1' > '0' ✓  →  digits[0] = '0', mark = 1     ['0','0']
fill: position 1 → '9'                               ['0','9']
int("09") = 9 ✅
```

⚠️ **The leading zero appears and is discarded by `int()`** — exactly the case mentioned above.

**Example 2** (`n = 1234`): no violations, so `mark` stays at 4, the fill loop `range(4, 4)` is empty, and the answer is **1234** ✅ — **unchanged, with no special case.**

**A larger check:** `n = 10^9` = `1000000000`:

```
i=9..2: all '0' > '0'? no
i=1:    '1' > '0' ✓  →  digits[0] = '0', mark = 1
fill:   positions 1..9 → '9'
result: "0999999999"  →  999999999 ✅
```

**And `n = 120`:**

```
i=2: '2' > '0' ✓ → digits[1] = '1', mark = 2      ['1','1','0']
i=1: '1' > '1'? no
fill: position 2 → '9'                             ['1','1','9']
result: 119 ✅
```

⚠️ **Here the cascade stops after one step** — the decremented digit no longer violates its left neighbour. **The scan handles both cases uniformly.**

**Verified exhaustively:** this implementation matches a brute-force descending search for **every `n` from 0 to 2,999** — 0 disagreements.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(d), effectively O(1)</summary>

**O(d)** where `d` is the number of digits — **at most 10**, so effectively constant.

| Phase | Cost |
|---|---|
| `str(n)` and `list(...)` | **O(d)** |
| Right-to-left scan | **O(d)** |
| Fill with 9s | **O(d)** |
| `int(''.join(...))` | **O(d)** |
| **Total** | **O(d)** = O(log n) |

At `n = 10⁹` that's **10 digits** — a handful of operations.

**Expressed in terms of `n` it's O(log₁₀ n)**, which is the honest way to say it: the input's *size* is its digit count, not its value.

**Versus counting down from `n`:**

| Approach | Complexity | At n = 10⁹ |
|---|---|---|
| Count down, test each | O(n · d) | ⚠️ up to **10¹⁰** ❌ |
| **Digit scan** | **O(d)** | **~10** ✅ |

⚠️ **The counting-down approach can be deceptively fast on easy inputs** — monotone numbers are common enough that a random `n` often has one nearby. **But adversarial inputs like `1000000000` require walking back through hundreds of millions of values.** The digit scan is uniformly fast.

**Only one pass over the digits is needed**, precisely because scanning right-to-left resolves cascades in place. **A left-to-right approach would need up to `d` passes** — still O(d²) = 100, fine here, but the wrong instinct at scale.

**This is optimal** — you must at least read all `d` digits. **Ω(d) is the lower bound.**

</details>

<details>
<summary><b>5 · Space complexity</b> — O(d)</summary>

**O(d)** — the digit list, at most 10 characters.

| Component | Size |
|---|---|
| `digits` | d characters → **O(d)** |
| `mark` | one integer → O(1) |
| **Total** | **O(d)** = O(log n) |

At `n = 10⁹` that's a 10-element list. **Effectively O(1)** for any input the constraints allow.

**Strings are immutable in Python**, so `list(str(n))` is necessary to modify digits in place. **Working with the integer directly** — using `//` and `%` to extract digits — would be O(1) space but far more error-prone:

| Approach | Space | Clarity |
|---|---|---|
| **Digit list** | O(d) | ✅ clear |
| Arithmetic on the integer | O(1) | ⚠️ fiddly, easy to get wrong |

**The list is the right trade** at 10 digits.
→ [string-immutability](../syntax/string-immutability.md)

**No recursion, no auxiliary structures.** The input `n` is an immutable int and is never modified.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Counting down from n is out — at 10⁹ that's up to a billion checks. So I work on the digits directly, and there are only ten of them. I scan right to left, and whenever a digit is greater than the one after it, I decrement it and record that position. Right-to-left is the important choice: decrementing a digit can create a new violation with its *left* neighbour, and scanning that direction means I visit that neighbour next, so cascades resolve in a single pass. A left-to-right scan would have already passed it. Then everything from the leftmost violation onward becomes 9 — that's safe because the decrement already put the number below n, so the suffix is free to be maximal. I initialise the marker past the end of the string, so if there are no violations the fill loop does nothing and n comes back unchanged. And if the cascade zeroes the leading digit, `int()` strips it automatically. O(d) time and space, which is O(log n) — effectively constant at ten digits."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why scan right to left?" | **The question.** Decrementing creates a violation with the *left* neighbour, which right-to-left visits next. Left-to-right would need multiple passes. |
| "Why fill the suffix with 9s?" | The decrement already puts the number below `n`'s prefix, so the rest is free to be maximal — and 9 is both largest and trivially non-decreasing. |
| "Why does `mark` start past the end?" | So a violation-free number produces an empty fill loop and comes back unchanged. |
| "What about leading zeros?" | `n = 10` produces `"09"`, and `int()` discards the zero. No special handling needed. |
| "Why can you compare digit characters directly?" | `'0'`–`'9'` are consecutive in ASCII, so for **single** characters string order matches numeric order. |
| "Why not count down from `n`?" | Up to 10⁹ iterations. It may look fast on random inputs but is catastrophic on adversarial ones like `1000000000`. |
| "Can you do it without strings?" | Yes, with `//` and `%` on the integer — O(1) space but considerably fiddlier. |
| "**Strictly** increasing instead?" | The digits would have to be distinct, so at most 10 digits and a different construction — you'd cap each digit at one below the next. |
| "What about the smallest monotone number ≥ n?" | Different problem — round *up* instead: find the violation and raise the suffix to match the prefix's last digit. |

**Traps:**

- **Scanning left to right** — misses the cascade, so `332` gives `329`, which isn't monotone. **The defining bug.**
- **Not filling the suffix with 9s** — you'd return a valid but non-maximal answer, e.g. `322` instead of `299`.
- **Setting `mark = min(mark, i)`** — harmless but redundant; the scan already moves leftward.
- **Initialising `mark = 0`** — fills the whole number with 9s, so `1234` becomes `9999` (which exceeds `n`).
- **Looping `range(len(digits)-1, -1, -1)`** — at `i = 0`, `digits[-1]` reads the last digit and compares it to the first.
- **Forgetting `int()` at the end** — returns a string, and leaves the leading zero.
- **Counting down from `n`** — passes small tests, times out on large ones.

**This same move shows up in:** [Minimum Deletions to Make Character Frequencies Unique](1647-minimum-deletions-to-make-character-frequencies-unique.md) (a greedy where each fix can cascade) · [Maximize Sum Of Array After K Negations](1005-maximize-sum-of-array-after-k-negations.md) (a provable greedy with a leftover-budget rule) · Remove K Digits (LeetCode 402) and Next Permutation (LeetCode 31) both scan from the right to find where the pattern breaks, then maximise the suffix · [string-basics](../syntax/string-basics.md).

</details>

---
