# 190. Reverse Bits

**Easy** · [LeetCode](https://leetcode.com/problems/reverse-bits/) · [Solution file (no hints)](../../problems/0001-0499/190.py)

[📖 19. Bit Manipulation lesson](../learning/19-bit-manipulation.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 19. Bit Manipulation problems](../rmap-practice/19-bit-manipulation.md)

---

Reverse the bits of a given **32-bit unsigned** integer.

```
n = 0b00000010100101000001111010011100   →  0b00111001011110000010100101000000
    (43261596)                                (964176192)

n = 0b11111111111111111111111111111101   →  0b10111111111111111111111111111111
    (4294967293)                              (3221225471)
```

**Constraints:** the input is a binary string of length exactly **32**.

**Follow-up:** if this function is called many times, how would you optimize it?

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**32-bit** unsigned integer" | The width is **fixed and explicit**. That matters enormously in Python, where integers have no inherent width |
| "**reverse** the bits" | Bit at position `i` moves to position `31 - i`. A pure permutation — no arithmetic on the value |
| **unsigned** | No sign bit to worry about; all 32 positions are data |
| leading zeros are significant | `1` (binary `…0001`) reverses to `10000000000000000000000000000000`, not to `1`. **The zeros carry information** |
| follow-up: called many times | A hint that a precomputed table is the production answer |

The core operation is simple to state: **the bit at position `i` ends up at position `31 - i`.** Position 0 (the least significant) goes to position 31 (the most significant), and vice versa.

So you need two primitives:

- **Read bit `i` of `n`:** shift right by `i` to bring that bit to the bottom, then mask with 1 to discard everything above it → `(n >> i) & 1`.
- **Write a bit at position `31 - i`:** shift the bit left into place, then OR it into the result → `result | (bit << (31 - i))`.

Do that 32 times and you're done.

**The critical detail — and it's a Python-specific trap — is that the loop must run exactly 32 times, not "until `n` becomes 0."**

In C or Java, an `int` is 32 bits and its leading zeros are physically there. In Python, integers are arbitrary-precision: `n = 1` is just `1`, with no notion of 31 leading zeros. So a `while n:` loop would stop after one iteration and place that bit at the wrong position entirely.

**The fixed 32 iterations are what supply the width that Python's integers don't carry.** That's the single most important thing to get right here, and it's why the loop is `range(32)` rather than a condition on `n`.

🤔 **Before you open the next section:** the code reads bit `i` and writes it to `31 - i`. There's an alternative formulation that shifts the result left and ORs in the *lowest* bit of `n` each time, with no explicit position arithmetic. Can you see why that also reverses the order?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| String manipulation | `int(bin(n)[2:].zfill(32)[::-1], 2)` | O(1) — 32 chars | O(1) | ⚠️ Works, and it's genuinely short — but it dodges the bit manipulation the problem is about |
| **Explicit position mapping** | Read bit `i`, place it at `31 - i` | **O(1)** — 32 iterations | **O(1)** | ✅ |
| Shift-and-accumulate | Shift `result` left, OR in `n`'s lowest bit, shift `n` right | O(1) | O(1) | ✅ Equivalent, slightly terser |
| Divide-and-conquer swaps | Swap 16-bit halves, then 8-bit, 4, 2, 1 — with masks | **O(log b)** = 5 steps | O(1) | ✅ The clever version — 5 operations instead of 32 |
| Byte lookup table | Precompute reversals for all 256 bytes, combine four | O(1) | O(256) | ✅ **The answer to the follow-up** |

**The decision:** **explicit position mapping** — clear, correct, and it makes the `31 - i` relationship visible.

**Why the 32-iteration loop is non-negotiable in Python.** This is worth being emphatic about, because it's the one place this "Easy" problem actually bites. Consider `n = 1`:

- A `while n:` loop runs **once**, placing the single bit and stopping. Result: 1. **Wrong** — the answer is 2³¹.
- The `range(32)` loop runs 32 times, reading 31 zeros above the set bit and placing that bit at position 31. Result: **2147483648** ✓

**In a fixed-width language the leading zeros exist physically; in Python you must supply them by iterating a fixed number of times.** Any solution that terminates based on `n`'s value is wrong here.

**The shift-and-accumulate alternative** — the answer to section 1's question:

```python
result = 0
for _ in range(32):
    result = (result << 1) | (n & 1)
    n >>= 1
return result
```

It reverses because **the first bit extracted gets shifted left 31 more times** as the loop continues, ending up at the top; the last bit extracted is never shifted and stays at the bottom. **The reversal emerges from the accumulation order** rather than from explicit index arithmetic. Same complexity, arguably neater — but the position-mapping version makes the `i → 31 - i` mapping explicit, which is easier to defend out loud.

**The divide-and-conquer version** does it in five steps by swapping progressively smaller blocks:

```python
n = ((n & 0xFFFF0000) >> 16) | ((n & 0x0000FFFF) << 16)   # swap 16-bit halves
n = ((n & 0xFF00FF00) >> 8)  | ((n & 0x00FF00FF) << 8)    # swap bytes
n = ((n & 0xF0F0F0F0) >> 4)  | ((n & 0x0F0F0F0F) << 4)    # swap nibbles
n = ((n & 0xCCCCCCCC) >> 2)  | ((n & 0x33333333) << 2)    # swap bit pairs
n = ((n & 0xAAAAAAAA) >> 1)  | ((n & 0x55555555) << 1)    # swap adjacent bits
```

**O(log b) instead of O(b)** — 5 operations rather than 32. It's how real bit-twiddling libraries do it, and worth naming even though you wouldn't write it from memory.

**The follow-up's intended answer is the lookup table:** precompute the reversal of all 256 possible bytes once, then reverse a 32-bit number with **four table lookups** and three shifts. Amortized over many calls, that's the fastest software approach — the classic time-space trade.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
result = 0
```
The accumulator, built one bit at a time. Starting at 0 means every position is clear, so the OR operations below only ever **set** bits — never accidentally clear one.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
for i in range(32):
```
**Exactly 32 iterations — one per bit position, regardless of `n`'s value.**

This is the line that supplies the fixed width Python's integers lack. A `while n:` loop would stop early on any input with leading zeros and misplace every bit.

`i` runs 0 through 31, indexing bit positions from the least significant end.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md)

```python
    bit = (n >> i) & 1
```
**Extract bit `i` of `n`.** Two steps in one expression:

- **`n >> i`** — [right shift](../syntax/bitwise-operators.md) by `i`, moving bit `i` down to position 0. Everything below it falls off the end.
- **`& 1`** — mask with `0b1`, keeping only that lowest bit and discarding all the higher ones.

The result is always **0 or 1**, which is what makes the placement below straightforward.

This is the standard "read bit `i`" idiom, and it's worth recognizing on sight — it appears throughout bit manipulation.
→ [bitwise-operators](../syntax/bitwise-operators.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
    result = result | (bit << (31 - i))
```
**Place that bit at the mirrored position.**

- **`bit << (31 - i)`** — [left shift](../syntax/bitwise-operators.md) the extracted bit into position `31 - i`. For `i = 0` that's position 31; for `i = 31`, position 0. **This is the reversal, stated directly.**
- **`result | …`** — OR it into the accumulator, setting that position without disturbing any other.

OR is the right operator precisely because it's additive on bits: setting a position that's already 0 turns it on, and no other position changes. Using `+` would happen to work here (each position is written once, so there's never a carry), but OR expresses the intent and is safe even if positions were revisited.

Note that when `bit` is 0, the shift produces 0 and the OR is a no-op — **zeros need no special handling**, they simply leave the position clear.
→ [bitwise-operators](../syntax/bitwise-operators.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
return result
```
All 32 positions have been mirrored.
→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def reverseBits(self, n: int) -> int:

        result = 0

        for i in range(32):
            bit = (n >> i) & 1
            result = result | (bit << (31 - i))
        return result
```
</details>

**Trace it** — a small example, `n = 5` treated as 32 bits

`5` is `…000101`, so bit 0 = 1, bit 1 = 0, bit 2 = 1, and bits 3–31 are all 0.

| `i` | `(n >> i) & 1` | target position `31 - i` | contribution | `result` so far |
|---|---|---|---|---|
| 0 | **1** | 31 | 2³¹ = 2147483648 | **2147483648** |
| 1 | 0 | 30 | 0 | 2147483648 |
| 2 | **1** | 29 | 2²⁹ = 536870912 | **2684354560** |
| 3–31 | 0 | … | 0 | 2684354560 |

Return **2684354560** ✅ — which in binary is `10100000000000000000000000000000`.

Reading it back: the input's bit pattern `101` (at the bottom) became `101` at the **top**, with 29 zeros trailing. **The three significant bits mirrored to the far end, and the 29 leading zeros became 29 trailing zeros** — which is exactly what reversing a 32-bit word means.

**And the crucial edge case** — `n = 1`:

| `i` | bit | target | `result` |
|---|---|---|---|
| 0 | **1** | 31 | **2147483648** |
| 1–31 | 0 | … | unchanged |

Return **2147483648** ✅ = 2³¹.

**Now compare what `while n:` would have done:** it reads bit 0, places it, then `n` is 0 and the loop stops — after **one** iteration. Depending on how it was written it'd return 1 or misplace the bit entirely. **The 31 leading zeros in `n` are invisible to Python, and only the fixed iteration count accounts for them.**

**And the first given example** — `n = 43261596` (`00000010100101000001111010011100`):

Reversing the 32-character string gives `00111001011110000010100101000000` = **964176192** ✅. The leading `000000` of the input becomes the trailing `000000` of the output — again, the zeros are carrying real positional information.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(1)</summary>

**O(1)** — exactly **32 iterations**, always, regardless of the input.

- The loop runs a fixed 32 times.
- Each iteration does two shifts, an AND, an OR, and an assignment — all **O(1)**.
- **32 × O(1) = O(1)**.

Calling it O(1) is honest here because the bit width is fixed by the problem, not by the input. If you generalized to `b`-bit integers it would be **O(b)**, and stating it that way shows you know where the constant comes from.

**No best or worst case** — the loop can't exit early and doesn't want to. Every position must be examined, including the zeros, because **a zero at position `i` means a zero at position `31 - i`**, which is information the output needs.

**Against the alternatives:**

| Approach | Operations | Note |
|---|---|---|
| This loop | **32** iterations | Straightforward |
| Divide-and-conquer masks | **5** steps | O(log b) — swap halves, bytes, nibbles, pairs, bits |
| Byte lookup table | **4** lookups + 3 shifts | The follow-up's answer; O(1) with a 256-entry table |
| Hardware `RBIT` (ARM) | 1 instruction | Not available on x86 |

**The follow-up — "called many times"** — is asking for the lookup table. Precompute all 256 byte reversals once, then each call is four lookups. Amortized across many invocations, the precomputation cost vanishes and each call becomes ~4 operations instead of 32. **That's a clean time-space trade and the expected answer.**

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — two integers, `result` and `bit`, plus the loop index. Nothing is allocated.

| Approach | Space | Why |
|---|---|---|
| String reversal | **O(1)**, ~32 chars | Bounded, but it does allocate a string |
| **Bit loop** | **O(1)** | Two integers |
| Divide-and-conquer | **O(1)** | Constant masks, no storage |
| Byte lookup table | **O(256)** | Precomputed once, shared across all calls |

**The lookup table's O(256) is the follow-up's trade**, and worth framing correctly: it's constant space in asymptotic terms, but it's a real 256-entry allocation exchanged for an 8× speedup per call. **That trade only pays off if the function is called repeatedly** — which is precisely the condition the follow-up specifies.

**A Python-specific note worth making:** because Python integers are arbitrary-precision, `result` never overflows — it just grows to hold whatever value it needs. In C or Java you'd need an **unsigned** 32-bit type, and using a signed `int` would make the result negative whenever bit 31 ends up set. **The problem says "unsigned" for exactly that reason**, and it's a portability detail worth mentioning even though Python sidesteps it.

**The input isn't modified** in this formulation — `n` is only read, never shifted in place. The shift-and-accumulate variant does consume `n`, which is fine since it's a local rebinding, but this version leaves it intact.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Reversing means the bit at position `i` moves to position `31 - i`. So I loop over all 32 positions, extract bit `i` with `(n >> i) & 1`, and OR it into the result shifted left by `31 - i`. The critical detail in Python is that the loop must run exactly 32 times rather than until `n` becomes zero — Python integers are arbitrary-precision, so the leading zeros that a C `int` would physically have simply don't exist. For input 1, a `while n:` loop would run once and give the wrong answer; the fixed 32 iterations are what supply the width. O(1) time and space, since the width is fixed. For the follow-up about repeated calls, I'd precompute a 256-entry table of byte reversals and do four lookups per call — or use the divide-and-conquer mask approach, which swaps 16-bit halves, then bytes, nibbles, pairs, and adjacent bits in five steps instead of 32."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "How would you optimize for many calls?" | Precompute the reversal of all 256 bytes into a table, then reverse a 32-bit word with four lookups and three shifts. The table cost amortizes to nothing. |
| "Why must the loop run 32 times?" | Python integers have no fixed width, so leading zeros don't exist. A value-based loop condition would stop early and misplace bits — `n = 1` would fail. |
| "Can you do it in fewer operations?" | Divide and conquer: swap the two 16-bit halves, then bytes within halves, nibbles, bit pairs, and finally adjacent bits — 5 masked steps, O(log b). |
| "What's the alternative loop formulation?" | Shift `result` left by one and OR in `n`'s lowest bit, then shift `n` right — repeated 32 times. The first bit extracted gets shifted left 31 more times, so it lands on top. |
| "What changes in Java or C?" | You need an unsigned 32-bit type. With a signed `int`, a set bit 31 makes the result negative — which is why the problem specifies "unsigned." |
| "Why OR rather than add?" | Both work here since each position is written once, but OR expresses "set this bit" and is safe even if a position were touched twice. |
| "Does `bit` being 0 need handling?" | No — shifting 0 gives 0, and ORing 0 changes nothing. Zeros leave their position clear automatically. |
| "What about a 64-bit version?" | Change 32 to 64 and `31 - i` to `63 - i`. The lookup table still works with eight lookups instead of four. |

**Traps:**
- **Using `while n:` instead of a fixed 32 iterations.** The defining bug in Python — any input with leading zeros comes out wrong.
- **`31 - i` written as `32 - i`** — shifts every bit one position too far and overflows past the 32-bit range.
- Forgetting the `& 1` mask after shifting — you'd OR in all the higher bits, not just the one.
- Using `+=` in a formulation where a position could be written twice — OR is the safe choice.
- Assuming Python will keep the result within 32 bits. It won't; the arithmetic must be correct by construction.
- Returning a negative number in a fixed-width language by using a signed type.

**This same move shows up in:** [Number of 1 Bits](191-number-of-1-bits.md) (per-bit extraction with shifts and masks) · [Counting Bits](338-counting-bits.md) (shifting to relate a number to a smaller one) · [Sum of Two Integers](371-sum-of-two-integers.md) (building an operation from shifts and bitwise logic) · [Rotate Image](48-rotate-image.md) (a positional permutation — `(i,j) → (j, n-1-i)` there, `i → 31-i` here).

</details>

---
