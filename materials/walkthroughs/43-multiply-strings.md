# 43. Multiply Strings

**Medium** · [LeetCode](https://leetcode.com/problems/multiply-strings/)

[📖 17. Math & Geometry lesson](../learning/19-math-geometry.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 17. Math & Geometry problems](../rmap-practice/17-math-geometry.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Given two non-negative integers `num1` and `num2` represented as **strings**, return their product, also as a string.

You must **not** use any built-in BigInteger library or convert the inputs to integers directly.

```
num1 = "2",   num2 = "3"     →  "6"
num1 = "123", num2 = "456"   →  "56088"
num1 = "0",   num2 = "9999"  →  "0"
```

**Constraints:** `1 <= num1.length, num2.length <= 200` · both consist of digits only · neither has leading zeros except `"0"` itself.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| numbers as **strings** | Up to 200 digits — far beyond any native integer type. The string representation is a necessity, not a formality |
| "**must not** convert to integers directly" | The rule that defines the exercise. In Python `int(num1) * int(num2)` would work perfectly, and it's explicitly forbidden |
| non-negative | No sign handling |
| no leading zeros in the input | But the **output** needs care — the result array will have them |
| `length <= 200` | 200 × 200 = 40,000 digit multiplications. Trivial |

Since you can't convert, you have to do what you did on paper in primary school: **long multiplication**. Multiply every digit of one number by every digit of the other, place each partial product in the right column, and add up the carries.

The whole problem is **getting the placement right**, so derive it rather than guessing.

Index the strings from the left, so `num1[i]` is at position `i`. Its **place value** — how many powers of ten it carries — is `m - 1 - i`, where `m = len(num1)`. Likewise `num2[j]` has place value `n - 1 - j`.

Multiplying them gives something at place value `(m - 1 - i) + (n - 1 - j)` = `m + n - 2 - i - j`.

Now, if the result array is also indexed from the left with length `m + n`, an entry at index `k` has place value `m + n - 1 - k`. Setting those equal:

```
m + n - 1 - k = m + n - 2 - i - j
            k = i + j + 1
```

**So `num1[i] × num2[j]` lands at result index `i + j + 1`**, with any carry going to `i + j` — the position immediately to its left.

That's the key fact, and it's worth deriving once rather than memorizing: **every digit pair has a fixed home, determined only by `i + j`.**

Two more things follow:

- **The result array needs `m + n` slots.** The product of an m-digit and an n-digit number has at most `m + n` digits (999 × 99 = 98,901: 3 + 2 = 5 digits), and at least `m + n - 1`. So `m + n` is always enough, and sometimes one too many — hence a leading zero to strip.
- **Order doesn't matter for accumulation.** Every pair contributes to its own `i + j + 1` slot, and carries always move left, so you can process the pairs in any order as long as carries propagate correctly.

🤔 **Before you open the next section:** the code adds `total // 10` to `result[i+j]` with `+=` rather than `=`. Why must it accumulate rather than overwrite — and can `result[pos_high]` grow beyond 9?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| `int(num1) * int(num2)` | Convert, multiply, stringify | O(m·n) | O(m+n) | ❌ **Explicitly forbidden**, and impossible in most languages |
| Repeated addition | Add `num1` to itself `num2` times | O(10ⁿ · m) | O(m) | ❌ Astronomically slow |
| Sum of shifted partial products | For each digit of `num2`, build a full partial product string, then add them | O(m·n) | O(m+n) | ⚠️ Correct — it's literally the paper layout — but it materializes n intermediate strings |
| **Digit-pair accumulation into one array** | Every `(i, j)` pair adds into `result[i+j+1]` | **O(m·n)** | **O(m+n)** | ✅ |
| Karatsuba multiplication | Divide and conquer on digit halves | O(n^1.585) | O(n) | ⚠️ Genuinely faster asymptotically, but only pays off around thousands of digits |

**The decision:** **accumulate every digit-pair product into a single result array**, indexed by `i + j + 1`.

**Why this beats the partial-products approach.** The paper method builds a separate row for each digit of `num2`, then adds all n rows together — which means allocating n strings of length up to m + n and running n additions. Same O(m·n) total, but with far more allocation and bookkeeping.

The single-array version collapses all of that: **since every partial product already knows exactly which column it belongs to, you can add them all into one array as you go.** No intermediate rows, one pass, one allocation.

**Why the carry handling is simpler than it looks.** You might expect to need a full carry-propagation pass at the end. You don't, because the code normalizes as it goes: after adding a product into `result[pos_low]`, it immediately reduces that slot to a single digit and pushes the overflow left. The invariant is that **every position to the right of the current one is already a single digit**.

**Why `result[pos_high]` can temporarily exceed 9** — part of the answer to section 1's question. The `+=` accumulates carries from multiple digit pairs before that position is itself processed. That's fine: when the loop later reaches `pos_high` as a `pos_low`, it does `total = digit_product + result[pos_low]`, and the `% 10` / `// 10` split normalizes whatever has accumulated there. **The array holds intermediate values that aren't valid digits, and that's by design** — they're all resolved before the join.

The `+=` rather than `=` is essential for the same reason: several pairs contribute carries to the same position, and overwriting would discard all but the last.

**Why not Karatsuba?** It's O(n^1.585) by splitting each number in half and using three multiplications instead of four. Real, and used in production big-integer libraries — but the crossover point is around 1,000 digits, and here n ≤ 200. Worth naming as the asymptotic improvement; the wrong answer to write.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
if num1 == "0" or num2 == "0":
    return "0"
```
**The zero shortcut**, and it's not just an optimization — it's a correctness guard.

Without it, `"0" × "9999"` produces a result array of all zeros, and the final `.lstrip("0")` would strip **every** character, returning the empty string `""` instead of `"0"`. Handling zero up front avoids needing a special case at the end.
→ [if-return](../syntax/if-return.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
m = len(num1)
n = len(num2)
result = [0] * (m + n)
```
The result array, sized **`m + n`** — the maximum possible number of digits in the product.

Working in a list of integers rather than a string matters: strings are [immutable](../syntax/string-immutability.md) in Python, so accumulating into one would mean rebuilding it on every update. A list allows O(1) in-place writes.
→ [list-basics](../syntax/list-basics.md) · [string-immutability](../syntax/string-immutability.md)

```python
for i in range(m - 1, -1, -1):
    for j in range(n - 1, -1, -1):
```
Iterate **both** strings from the least significant digit (rightmost) toward the most.

Right-to-left mirrors how you'd do it on paper, and it means carries flow toward positions not yet finalized. As noted in section 2, the accumulation is actually order-independent — but this order keeps the mental model aligned with the paper method.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md)

```python
        digit_product = int(num1[i]) * int(num2[j])
        pos_low = i + j + 1
        pos_high = i + j
```
**One digit times one digit**, at most 9 × 9 = 81 — so the product is always one or two digits.

`pos_low` and `pos_high` are the derivation from section 1 made concrete: the product's units go at `i + j + 1`, and its tens carry into `i + j`. Naming them rather than inlining the arithmetic is what keeps the next three lines readable.

[`int()`](../syntax/type-conversion.md) converts a single character — permitted, since it's not converting the whole number.
→ [type-conversion](../syntax/type-conversion.md) · [arithmetic-operators](../syntax/arithmetic-operators.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
        total = digit_product + result[pos_low]
```
**Add the new product to whatever is already in that column.** `result[pos_low]` may hold contributions from earlier digit pairs and carries from the right — all of them belong in the same column.

`total` can be large-ish (up to 81 plus accumulated carries), which is exactly why the next two lines split it.
→ [arithmetic-operators](../syntax/arithmetic-operators.md) · [list-basics](../syntax/list-basics.md)

```python
        result[pos_low] = total % 10
        result[pos_high] += total // 10
```
**Normalize this column and push the overflow left.**

- `total % 10` — the single digit that stays here.
- `total // 10` — everything above 9, carried one position left.

**`+=` on `pos_high`, not `=`** — the answer to section 1's question. Multiple digit pairs and multiple carries land on the same position, and overwriting would discard all but the most recent. Accumulating is what makes the column sums correct.

And yes, `result[pos_high]` can temporarily exceed 9. That's fine: it gets normalized when the loop reaches it as a `pos_low`, or — for the leftmost position — it's guaranteed to already be a single digit, because the product can't have more than `m + n` digits.
→ [integer-division-modulo](../syntax/integer-division-modulo.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
return "".join(map(str, result)).lstrip("0")
```
**Convert to a string and strip the leading zero.**

[`map(str, result)`](../syntax/map-filter.md) turns each integer into its character, and [`"".join`](../syntax/string-join-slice.md) concatenates them.

The [`.lstrip("0")`](../syntax/string-methods.md) removes the leading zero that appears whenever the product has `m + n - 1` digits rather than `m + n` — for example 12 × 12 = 144, which is 3 digits in a 4-slot array, giving `"0144"`.

**This is safe only because of the zero guard at the top.** For a genuinely zero product, `lstrip` would return `""`.
→ [map-filter](../syntax/map-filter.md) · [string-join-slice](../syntax/string-join-slice.md) · [string-methods](../syntax/string-methods.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def multiply(self, num1: str, num2: str) -> str:

        if num1 == "0" or num2 == "0":
            return "0"

        m = len(num1)
        n = len(num2)
        result = [0] * (m + n)

        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                digit_product = int(num1[i]) * int(num2[j])
                pos_low = i + j + 1
                pos_high = i + j

                total = digit_product + result[pos_low]
                result[pos_low] = total % 10
                result[pos_high] += total // 10

        return "".join(map(str, result)).lstrip("0")
```
</details>

**Trace it** — `num1 = "12"`, `num2 = "34"` (expected: 408)

`m = n = 2`, so `result = [0, 0, 0, 0]`.

| `i` | `j` | digits | product | `pos_low` | `total` | `result` after |
|---|---|---|---|---|---|---|
| 1 | 1 | 2 × 4 | 8 | 3 | 8 + 0 = 8 | `[0, 0, 0, **8**]` |
| 1 | 0 | 2 × 3 | 6 | 2 | 6 + 0 = 6 | `[0, 0, **6**, 8]` |
| 0 | 1 | 1 × 4 | 4 | 2 | 4 + **6** = 10 | `[0, **1**, **0**, 8]` |
| 0 | 0 | 1 × 3 | 3 | 1 | 3 + **1** = 4 | `[**0**, **4**, 0, 8]` |

Join → `"0408"`, `.lstrip("0")` → **"408"** ✅ (12 × 34 = 408)

Row 3 is where the mechanism shows: the column at index 2 already held 6, the new product 4 brings it to 10, so 0 stays and 1 carries into index 1. Row 4 then picks that carry up — `3 + 1 = 4` — which is exactly the `+=` accumulation being read back.

And the leading `0` at index 0 is the "one too many slots" case: 12 × 34 = 408 has 3 digits, but the array has 4. `lstrip` handles it.

**And the full example** — `num1 = "123"`, `num2 = "456"` (expected: 56088):

`result` has 6 slots. Rather than all nine pairs, here are the column totals before normalization — each cell shows which products land at each index:

| result index | contributing pairs (`i+j+1`) | products |
|---|---|---|
| 5 | (2,2) | 3×6 = 18 |
| 4 | (2,1), (1,2) | 3×5 + 2×6 = 15 + 12 = 27 |
| 3 | (2,0), (1,1), (0,2) | 3×4 + 2×5 + 1×6 = 12 + 10 + 6 = 28 |
| 2 | (1,0), (0,1) | 2×4 + 1×5 = 8 + 5 = 13 |
| 1 | (0,0) | 1×4 = 4 |

Propagating carries from the right: index 5 → 8 carry 1; index 4 → 27+1 = 28 → 8 carry 2; index 3 → 28+2 = 30 → 0 carry 3; index 2 → 13+3 = 16 → 6 carry 1; index 1 → 4+1 = 5.

Result array: `[0, 5, 6, 0, 8, 8]` → `"056088"` → **"56088"** ✅

The column-grouping view makes the `i + j + 1` rule visible — **every pair whose indices sum to the same value shares a column**, which is precisely how you'd align the partial products on paper.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(m · n)</summary>

**O(m · n)**, where m and n are the digit counts.

- The nested loops run **m × n** times — every digit of `num1` paired with every digit of `num2`.
- Each iteration does two `int()` conversions on single characters, one multiplication, one addition, one modulo, one floor division, and two array writes — all **O(1)**.
- The final join is **O(m + n)**.
- Total: **O(m · n)**.

At the limits, 200 × 200 = **40,000** digit multiplications. Instant.

**This is the same complexity as the paper method**, and for good reason — it *is* the paper method, with the partial-product rows collapsed into a single accumulator. Both do m·n digit multiplications; this version just avoids materializing n intermediate strings.

**Faster?** Asymptotically yes:

| Algorithm | Time | When it wins |
|---|---|---|
| Schoolbook (this) | **O(n²)** | Up to ~1,000 digits |
| Karatsuba | **O(n^1.585)** | Thousands of digits |
| Toom–Cook | O(n^1.465) | Tens of thousands |
| Schönhage–Strassen (FFT-based) | O(n log n log log n) | Very large numbers |

Python's own big integers use schoolbook below a threshold and switch to Karatsuba above it — which is a nice concrete example of why the asymptotically-worse algorithm is the right default at small sizes. **At n ≤ 200, schoolbook wins on constant factors.**

</details>

<details>
<summary><b>5 · Space complexity</b> — O(m + n)</summary>

**O(m + n)** — the result array holds exactly `m + n` integers, which is the maximum possible digit count of the product.

| Component | Space | Why |
|---|---|---|
| `result` | **O(m + n)** | One slot per possible output digit |
| The joined string | **O(m + n)** | Built at the end |
| Loop scalars | O(1) | Indices and temporaries |

So **O(m + n)**, which is optimal — the output itself has that many digits, so you can't do better.

**Why a list of ints rather than building a string:** Python strings are [immutable](../syntax/string-immutability.md), so accumulating into one would create a new string on every update — O(m + n) per write, and O(m·n·(m+n)) overall. **The mutable list is what keeps the writes O(1)**, and the single join at the end is the only string construction.

**Against the partial-products approach:** that one allocates n intermediate strings, each up to m + n long — **O(n · (m + n))** space, versus O(m + n) here. Same time, considerably more memory, which is the practical argument for collapsing the rows.

**Could you use fewer than m + n slots?** Only by knowing the exact output length in advance, which requires computing the product first. The `m + n` bound over-allocates by at most one slot, and `lstrip` handles that.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Since I can't convert to integers, this is grade-school long multiplication. The key is figuring out where each digit-pair product lands. If `num1[i]` has place value `m-1-i` and `num2[j]` has `n-1-j`, their product sits at place value `m+n-2-i-j`, which in a left-indexed array of length `m+n` is index `i+j+1` — with the carry going to `i+j`. So every pair has a fixed home determined by `i+j`. I accumulate all the products into one array rather than building separate partial-product rows, normalizing each column as I go: keep `total % 10` in place and add `total // 10` to the position on the left. The `+=` on the carry is essential since several pairs contribute to the same column. The array is `m+n` long because the product has at most that many digits, so I strip one possible leading zero at the end — and I handle a zero input up front, otherwise stripping would leave an empty string. O(m·n) time, O(m+n) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why does `num1[i] × num2[j]` land at `i + j + 1`?" | Place values: `(m-1-i) + (n-1-j) = m+n-2-i-j`. In an `m+n` array indexed from the left, index `k` has place value `m+n-1-k`. Solving gives `k = i+j+1`. |
| "Why `+=` for the carry instead of `=`?" | Several digit pairs and carries land on the same position. Overwriting would discard all but the last contribution. |
| "Can a slot exceed 9 mid-computation?" | Yes, and that's fine — it's normalized when the loop reaches that position as a `pos_low`. The array holds intermediate non-digit values by design. |
| "Why the zero check at the top?" | Without it, `"0" × "9999"` gives an all-zero array and `lstrip("0")` returns `""` rather than `"0"`. |
| "Why is the array `m + n` long?" | An m-digit times an n-digit number has at most m+n digits (99 × 99 = 9801) and at least m+n−1. So m+n always fits, sometimes with one leading zero. |
| "Can you do better than O(n²)?" | Karatsuba is O(n^1.585) by splitting each number in half and using three multiplications instead of four. It only pays off past about 1,000 digits — Python's own big ints switch over at a threshold like that. |
| "What about negative numbers?" | Strip and record the signs, multiply the magnitudes, then apply the sign to the result. |
| "Could you build the answer as a string directly?" | You could, but strings are immutable so each update would rebuild the whole thing — O(m·n·(m+n)). The mutable list keeps writes O(1). |

**Traps:**
- **Overwriting the carry** with `=` instead of `+=` — loses contributions from other digit pairs.
- **Getting the index offset wrong** — `i + j` instead of `i + j + 1` for the low position shifts the entire product by a factor of ten.
- **Omitting the zero check**, so a zero product returns `""`.
- Sizing the array `m + n - 1` — correct for most inputs, and off by one exactly when the product needs the extra digit (99 × 99).
- Stripping with `.strip("0")` instead of `.lstrip("0")` — would also remove **trailing** zeros, turning 400 into 4.
- Trying to normalize carries only in a final pass. Workable, but you'd need to handle multi-digit accumulations, and normalizing as you go is simpler.

**This same move shows up in:** [Plus One](66-plus-one.md) (digit-array arithmetic with carry propagation, avoiding native integer limits) · [Add Two Numbers](2-add-two-numbers.md) (the same carry logic over a linked list) · [Pow(x, n)](50-pow-x-n.md) (implementing an arithmetic primitive from a lower-level operation) · [Happy Number](202-happy-number.md) (digit-level decomposition of a number).

</details>

---
