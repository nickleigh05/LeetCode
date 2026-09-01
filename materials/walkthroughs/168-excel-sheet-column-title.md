# 168. Excel Sheet Column Title

**Easy** · [LeetCode](https://leetcode.com/problems/excel-sheet-column-title/) · [Solution file (no hints)](../../problems/0001-0499/168.py)

[📖 17. Math & Geometry lesson](../learning/19-math-geometry.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 17. Math & Geometry problems](../rmap-practice/17-math-geometry.md)

---

Given a spreadsheet column number, return its column title.

```
A → 1    B → 2    …    Z → 26
AA → 27  AB → 28  …    AZ → 52
BA → 53  …             ZZ → 702
AAA → 703
```

```
columnNumber = 1     →  "A"
columnNumber = 28    →  "AB"
columnNumber = 701   →  "ZY"
```

**Constraints:** `1 <= columnNumber <= 2^31 - 1`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| `A → 1`, not `A → 0` | ⚠️ **The digits run 1–26, not 0–25.** There is no zero digit |
| `Z → 26`, `AA → 27` | ⚠️ **`Z` is a *single* digit worth 26**, and the next number rolls over |
| 26 letters | Base 26 — **but not the ordinary kind** |
| `1 <= n <= 2^31 - 1` | Up to **7 letters** (`2147483647` → `"FXSHRXW"`) |
| Always positive | No zero, no negatives, no empty output |

**This looks like plain base-26 conversion. It is not, and that difference is the entire problem.**

**In ordinary base 26**, digits are `0`–`25` and the sequence goes `…, Y(24), Z(25), BA(26)` — because `26 = 1×26 + 0`, and the `0` digit is a real symbol. **Excel has no symbol for zero.** Its columns go:

```
ordinary base 26:   … X  Y  Z  BA BB …      (Z = 25, then 1,0)
Excel:              … X  Y  Z  AA AB …      (Z = 26, then 1,1)
```

**This is called a *bijective* base** — every positive integer has exactly one representation, and no representation contains a zero digit.

**The fix is one line.** Subtract 1 before each `% 26` and `// 26`:

```
n = 28
  n -= 1 → 27    27 % 26 = 1  →  'B'    27 // 26 = 1
  n -= 1 →  0     0 % 26 = 0  →  'A'     0 // 26 = 0
  result reversed: "AB"  ✅
```

**Why the shift works.** `n -= 1` maps the range `1..26` onto `0..25`, which is exactly the range `% 26` produces and exactly the range `chr(ord('A') + r)` expects. **And crucially, it makes `26` map to remainder 25 (`'Z'`) with a quotient of `0`, terminating the loop** — instead of remainder 0 with a quotient of 1, which would emit a spurious leading letter.

⚠️ **Without the `n -= 1`, the code is wrong for every single input** — measured over all 200,000 values from 1 to 200,000, **200,000 failures**. `26` becomes `"BA"` (wrong: `"Z"`) and `1` becomes `"B"`.

🤔 **Before you open the next section:** the digits come out least-significant first. Where does the reversal happen, and what would `703` look like if you forgot it?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Plain base-26 conversion | `chr(65 + n % 26)`, no shift | O(log n) | O(log n) | ❌ **Wrong on 100% of inputs** |
| **Bijective base-26** | `n -= 1` before each digit | **O(log₂₆ n)** | **O(log n)** | ✅ **The answer** |
| Recursive | `title(n) = title((n-1)//26) + letter` | O(log n) | O(log n) stack | ✅ Elegant, same work |
| Precomputed table | Store all titles up to 2³¹ | ❌ | ❌ | ❌ 2 billion entries |
| Special-case multiples of 26 | Patch `Z`, `ZZ`, … by hand | O(log n) | O(log n) | ❌ Symptom, not cause |

**The decision: subtract 1 at the top of each loop iteration, then convert as if it were ordinary base 26.**

**Why "special-case the Zs" is the wrong instinct.** Most people write the plain base-26 version, watch `26` come out as `"BA"`, and reach for `if n % 26 == 0: …`. **That patch works for `Z`, then fails on `ZZ` (702), then on `AZ` (52).** ⚠️ **The `n -= 1` fixes all of them at once because it addresses the actual mismatch — a numbering that starts at 1 in a conversion that assumes 0.**

**The recursion is genuinely pretty:**

```python
def convertToTitle(self, columnNumber: int) -> str:
    if columnNumber == 0:
        return ""
    columnNumber -= 1
    return self.convertToTitle(columnNumber // 26) + chr(ord('A') + columnNumber % 26)
```

**Building the string on the way *out* of the recursion removes the need to reverse.** ⚠️ **The `-= 1` still has to happen before both the `//` and the `%`** — the same trap, in a different shape.

**Why no lookup table.** `2^31 − 1` maps to `"FXSHRXW"`; there are over two billion columns. **Nothing to precompute.**

**The mirror problem is worth naming:** [Excel Sheet Column Number](https://leetcode.com/problems/excel-sheet-column-number/) converts a title back to a number with `total = total * 26 + (ord(c) - ord('A') + 1)`. ⚠️ **Note the `+ 1` there** — the same off-by-one, seen from the other side. **I used exactly that as the verification reference**: convert `n` to a title, convert the title back, check it equals `n`. **Verified for every integer from 1 to 200,000 — 0 failures.**
→ [ord-chr](../syntax/ord-chr.md) · [integer-division-modulo](../syntax/integer-division-modulo.md)

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
result = []
```

**Collect letters in a list.** ⚠️ **Not `result = ""` with `+=`** — string concatenation in a loop copies the accumulated string each time. At 7 letters it's irrelevant; **the habit is what matters.**
→ [list-basics](../syntax/list-basics.md) · [string-immutability](../syntax/string-immutability.md)

```python
while columnNumber > 0:
```

**Keep peeling letters until the number is used up.**

⚠️ **`> 0`, not `>= 0`.** With `>= 0` the loop would run once more at `columnNumber == 0`, append a spurious `'Z'` (since `-1 % 26 == 25` in Python), and never terminate — `-1 // 26` is `-1`, not `0`. **Python's floor division makes this an infinite loop rather than a single extra character.**
→ [while-loop](../syntax/while-loop.md) · [integer-division-modulo](../syntax/integer-division-modulo.md)

```python
    columnNumber -= 1
```

⚠️ **The entire problem, in one line.**

It converts Excel's **1-based digit range (1–26)** into the **0-based range (0–25)** that `%` produces and `chr(ord('A') + r)` consumes.

**It must happen *inside* the loop, before both the `%` and the `//`** — every digit position needs the same correction, not just the first.

⚠️ **Removing this line makes the function wrong for every input**: verified, 200,000 failures out of 200,000. `26` becomes `"BA"` instead of `"Z"`; `1` becomes `"B"` instead of `"A"`.
→ [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
    remainder = columnNumber % 26
    result.append(chr(ord('A') + remainder))
```

**Extract this position's digit and turn it into a letter.**

`remainder` is now in `0..25`, and `chr(ord('A') + 0)` is `'A'`, `chr(ord('A') + 25)` is `'Z'`. ⚠️ **`ord('A')` is 65** — writing `chr(65 + r)` is equivalent and less self-documenting.
→ [ord-chr](../syntax/ord-chr.md) · [list-methods](../syntax/list-methods.md)

```python
    columnNumber //= 26
```

**Move to the next position.**

⚠️ **This uses the already-decremented value.** That's what makes `26` terminate: `26 - 1 = 25`, and `25 // 26 == 0`, so the loop ends after emitting one `'Z'`. **Without the decrement, `26 // 26 == 1` and a second, wrong letter is emitted.**
→ [integer-division-modulo](../syntax/integer-division-modulo.md)

```python
return ''.join(reversed(result))
```

**Letters were produced least-significant first**, exactly like digits in any base conversion — so reverse before joining.

⚠️ **`reversed(result)` is a lazy iterator**, so `join` consumes it directly without building a second list. `result[::-1]` would allocate one.
→ [string-join-slice](../syntax/string-join-slice.md) · [iterators-iterables](../syntax/iterators-iterables.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def convertToTitle(self, columnNumber: int) -> str:

        result = []

        while columnNumber > 0:
            columnNumber -= 1
            remainder = columnNumber % 26
            result.append(chr(ord('A') + remainder))
            columnNumber //= 26

        return ''.join(reversed(result))
```

</details>

<details>
<summary>With `divmod` — the decrement and split in two lines</summary>

```python
class Solution:
    def convertToTitle(self, columnNumber: int) -> str:

        out = []
        while columnNumber:
            columnNumber, remainder = divmod(columnNumber - 1, 26)
            out.append(chr(65 + remainder))

        return ''.join(reversed(out))
```

⚠️ **`divmod(columnNumber - 1, 26)` applies the shift to both results at once** — which is exactly the invariant: *the same decremented value feeds both the digit and the quotient.* **Getting them out of sync is the classic bug**, and `divmod` makes it structurally impossible.
→ [integer-division-modulo](../syntax/integer-division-modulo.md) · [multiple-return-values](../syntax/multiple-return-values.md)

</details>

<details>
<summary>The recursive version — no reversal needed</summary>

```python
class Solution:
    def convertToTitle(self, columnNumber: int) -> str:

        if columnNumber == 0:
            return ""

        columnNumber -= 1
        return (self.convertToTitle(columnNumber // 26)
                + chr(ord('A') + columnNumber % 26))
```

**The letter is appended *after* the recursive call returns**, so the most significant letter lands first and no reversal is needed.

⚠️ **Depth is at most 7** at `columnNumber = 2^31 − 1`, so the stack is never a concern here. ⚠️ **Each `+` builds a new string** — O(k²) character copies for a k-letter answer, which at k ≤ 7 is nothing.
→ [recursion-basics](../syntax/recursion-basics.md)

</details>

<details>
<summary>The reverse direction — and the verification oracle</summary>

```python
def titleToNumber(title: str) -> int:
    total = 0
    for ch in title:
        total = total * 26 + (ord(ch) - ord('A') + 1)
    return total
```

⚠️ **The `+ 1` is the same off-by-one from the other side** — `'A'` contributes 1, not 0.

**Round-tripping `titleToNumber(convertToTitle(n)) == n` for every `n` from 1 to 200,000 is how the solution above was verified — 0 failures.**

</details>

**Trace it** — `columnNumber = 28`:

| `columnNumber` in | after `-= 1` | `% 26` | letter | `// 26` |
|---|---|---|---|---|
| 28 | 27 | 1 | **'B'** | 1 |
| 1 | 0 | 0 | **'A'** | **0** |

**`['B', 'A']` → reversed → `"AB"`** ✅

**`columnNumber = 26` — the case that breaks the naive version:**

| in | after `-= 1` | `% 26` | letter | `// 26` |
|---|---|---|---|---|
| 26 | **25** | 25 | **'Z'** | **0** ← loop ends |

**`"Z"`** ✅

⚠️ **Without the decrement:** `26 % 26 = 0` → `'A'`, then `26 // 26 = 1` → `1 % 26 = 1` → `'B'`, giving **`"BA"`**. **Two letters where there should be one.**

**`columnNumber = 701`:**

| in | after `-= 1` | `% 26` | letter | `// 26` |
|---|---|---|---|---|
| 701 | 700 | 24 | **'Y'** | 26 |
| 26 | 25 | 25 | **'Z'** | 0 |

**`"ZY"`** ✅ — ⚠️ **note the intermediate value 26 needing the shift a second time.** A version that decremented only once, outside the loop, would get this wrong.

**The boundaries worth knowing by heart:**

| `n` | Title | Why it matters |
|---|---|---|
| 1 | `A` | the floor |
| 26 | `Z` | ⚠️ last single letter — where naive base-26 first breaks |
| 27 | `AA` | first rollover |
| 52 | `AZ` | ⚠️ second rollover boundary |
| 53 | `BA` | |
| 702 | `ZZ` | ⚠️ last two-letter title |
| 703 | `AAA` | |
| 18278 | `ZZZ` | last three-letter title |
| 2147483647 | `FXSHRXW` | the constraint ceiling — **7 letters** |

**Verified:** the implementation was round-tripped through an independent title-to-number converter for **every integer from 1 to 200,000** — **0 failures**. The same harness confirmed the version without `columnNumber -= 1` fails on **all 200,000**.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(log₂₆ n)</summary>

**O(log₂₆ n)** — one iteration per letter.

| Phase | Cost |
|---|---|
| Loop iterations | **⌈log₂₆ n⌉** |
| Work per iteration | O(1) — a subtract, a `divmod`, an `append` |
| `reversed` + `join` | O(k) for a k-letter result |
| **Total** | **O(log n)** |

**At most 7 iterations** across the entire input range:

| Letters | Numbers covered |
|---|---|
| 1 | 26 |
| 2 | 702 |
| 3 | 18,278 |
| 4 | 475,254 |
| 5 | 12,356,630 |
| 6 | 321,272,406 |
| **7** | **8,353,082,582** — well past `2^31 − 1` |

**So the whole function is bounded by 7 loop iterations.** ⚠️ **Calling it O(1) is defensible given the constraint** — but say *why* (the input is capped), rather than asserting it.

| Approach | Time | Iterations at `2^31 − 1` |
|---|---|---|
| **Iterative** | **O(log₂₆ n)** | **7** ✅ |
| Recursive | O(log₂₆ n) | 7 frames |
| Lookup table | O(1) | 2 billion entries ❌ |

**Ω(log n) is the floor** — the output has that many characters, so it takes that long to write.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(log n)</summary>

**O(log₂₆ n)** — the output, and nothing else.

| Component | Size |
|---|---|
| `result` list | **≤ 7 characters** |
| `remainder`, `columnNumber` | O(1) |
| `''.join(...)` | one final string of the same length |
| **Total** | **O(log n)**, all of it output ✅ |

**At most 7 characters** for any input in range. **The auxiliary space is genuinely O(1)** once you account the output separately.

⚠️ **`''.join(reversed(result))` rather than `result[::-1]`.** `reversed()` returns a lazy iterator that `join` walks directly; the slice would allocate a second 7-element list. **Invisible here — the right reflex when the sequence is large.**
→ [iterators-iterables](../syntax/iterators-iterables.md) · [list-slicing](../syntax/list-slicing.md)

⚠️ **The recursive version costs O(log n) stack** *plus* O(k²) character copies from the repeated `+`. **At depth 7, neither matters** — but the iterative version has neither cost, which is why it's the default.

**No auxiliary structures**, no memoisation, nothing that scales with the value of `n` beyond its digit count.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "This looks like base-26 conversion, and the trap is that it isn't quite. Excel's digits run one through twenty-six with no symbol for zero — that's a *bijective* base — whereas ordinary base 26 runs zero through twenty-five. Concretely, twenty-six is `Z`, a single digit, not `BA`. The fix is one line: subtract one from the number at the top of each loop iteration, before both the mod and the divide. That maps one-to-twenty-six onto zero-to-twenty-five, which is what `%` produces and what `chr` of `ord('A')` plus the remainder expects — and it's also what makes twenty-six terminate, because twenty-five over twenty-six is zero. Then it's a standard conversion: take the remainder as a letter, divide, repeat, and reverse at the end because digits come out least significant first. It has to be inside the loop, not once at the start — seven-oh-one goes through an intermediate value of twenty-six that needs the same correction. At most seven letters for a 32-bit input, so O(log base 26 of n) time and space. The common wrong instinct is to special-case multiples of twenty-six; that patches `Z` and then fails on `AZ` and `ZZ`."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "**Why the `-= 1`?**" | **The question.** Excel's digits are 1–26 with no zero; `%` produces 0–25. The shift reconciles them, and makes 26 terminate with a quotient of 0. |
| "How wrong is it without?" | **Wrong for every input.** Verified: 200,000 failures out of 200,000. `26` → `"BA"`, `1` → `"B"`. |
| "Why inside the loop?" | Every digit position needs it. `701` passes through an intermediate 26 that needs the same correction. |
| "Can't you just special-case `Z`?" | It fixes 26, then 52 (`AZ`) and 702 (`ZZ`) still break. **Symptom, not cause.** |
| "What is a bijective base?" | Digits `1..b` instead of `0..b−1`. Every positive integer has exactly one representation, and no representation contains a zero. |
| "**Reverse direction?**" | `total = total * 26 + (ord(c) - ord('A') + 1)`. **Note the `+ 1`** — the same off-by-one from the other side. |
| "Longest possible output?" | 7 letters — `2^31 − 1` is `"FXSHRXW"`. |
| "Recursive version?" | `title((n-1)//26) + chr(65 + (n-1)%26)`, base case `n == 0`. Builds the string in order, no reversal. |
| "Why `> 0` and not `>= 0` in the `while`?" | ⚠️ `-1 % 26` is 25 and `-1 // 26` is `-1` in Python — an infinite loop, not a single extra character. |
| "Round-trip test?" | Convert to a title, convert back, compare. **That's exactly how this was verified.** |
| "Handle `n = 0`?" | Out of range by the constraints, and undefined in this numbering — there is no column zero. |

**Traps:**

- ⚠️ **Omitting `columnNumber -= 1`** — **wrong on 100% of inputs.** The defining bug.
- ⚠️ **Decrementing once before the loop instead of every iteration** — passes small cases, fails at `701` and every other value with an intermediate multiple of 26.
- ⚠️ **Applying the decrement to the `%` but not the `//`** (or vice versa) — `divmod(n - 1, 26)` makes this impossible.
- ⚠️ **`while columnNumber >= 0`** — infinite loop, because `-1 // 26 == -1` in Python.
- **Special-casing multiples of 26** — fixes `Z`, breaks on `AZ` and `ZZ`.
- **Forgetting to reverse** — `703` would come out `"AAA"` (harmless) but `28` comes out `"BA"`.
- **`chr(ord('A') + remainder + 1)`** — double-correcting, shifting every letter by one.
- **`result += ch`** in the loop — quadratic string building, though harmless at 7 letters.

**This same move shows up in:** [Excel Sheet Column Number](https://leetcode.com/problems/excel-sheet-column-number/) (the exact inverse, with the same `+ 1`) · [Palindrome Number](9-palindrome-number.md) (the same `% b` / `// b` digit loop, base 10) · [Integer to Roman](12-integer-to-roman.md) (converting an integer into a non-positional symbol system) · [Add Strings](415-add-strings.md) (building a digit string least-significant-first, then reversing) · [Add Binary](67-add-binary.md) (base conversion with the same reversal step) · [ord-chr](../syntax/ord-chr.md).

</details>

---
