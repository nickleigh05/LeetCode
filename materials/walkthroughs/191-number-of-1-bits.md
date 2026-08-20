# 191. Number of 1 Bits

**Easy** · [LeetCode](https://leetcode.com/problems/number-of-1-bits/) · [Solution file (no hints)](../../problems/0001-0499/191.py)

[📖 19. Bit Manipulation lesson](../learning/19-bit-manipulation.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 19. Bit Manipulation problems](../rmap-practice/19-bit-manipulation.md)

---

Write a function that takes an integer and returns the number of **1 bits** in its binary representation — also known as the **Hamming weight**.

```
n = 11    →  3      binary 1011  →  three 1s
n = 128   →  1      binary 10000000
n = 2147483645 → 30 binary 1111111111111111111111111111101
```

**Constraints:** `1 <= n <= 2³¹ − 1`.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| count the **1 bits** | You need to inspect the binary representation — the number's *value* is irrelevant, only its bit pattern matters |
| "**Hamming weight**" | The standard name. Worth knowing, because it's what the operation is called in hardware and in cryptography |
| `n` up to 2³¹ − 1 | At most **31 bits**, so any per-bit approach is bounded by a small constant |
| `n >= 1` | Positive only, so no two's-complement sign-bit complications |

The obvious approach: check each bit position in turn.

```python
count = 0
while n:
    count += n & 1     # is the lowest bit set?
    n >>= 1            # shift right to examine the next
return count
```

That's correct and runs **once per bit position** — up to 31 iterations regardless of how many bits are actually set. For `n = 128` (binary `10000000`) it does 8 iterations to find a single 1.

**The better approach comes from a specific identity**, and it's worth deriving rather than memorizing:

> **`n & (n - 1)` clears the lowest set bit of `n`, leaving everything else unchanged.**

Why? Consider what subtracting 1 does to a binary number. Find the lowest set bit; subtracting 1 **flips it to 0** and **turns every 0 below it into 1**. Everything above is untouched.

```
n      = 1011 1000
n - 1  = 1011 0111      ← lowest 1 became 0; the zeros below became 1s
n & (n-1) = 1011 0000   ← AND keeps only the untouched high bits
```

The AND is exact: above the lowest set bit both numbers agree, so those bits survive. At the lowest set bit, `n` has 1 and `n-1` has 0 → cleared. Below it, `n` has 0s and `n-1` has 1s → all cleared.

**So each application removes exactly one 1 bit.** Repeat until `n` is 0, and the number of repetitions *is* the number of set bits.

This is **Brian Kernighan's algorithm**, and its virtue is that it runs once per **set bit** rather than once per bit position.

🤔 **Before you open the next section:** for `n = 128` the shift-based loop takes 8 iterations. How many does `n & (n - 1)` take? And for which inputs are the two approaches equally fast?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| `bin(n).count("1")` | Convert to a string, count characters | O(log n) | O(log n) | ⚠️ Works, and it's what you'd write in real code — but it sidesteps the exercise |
| Shift and test each position | `n & 1`, then `n >>= 1` | **O(b)** = 32 | O(1) | ✅ Correct; runs once per bit *position* |
| **Brian Kernighan's trick** | `n &= n - 1` clears the lowest set bit | **O(k)**, k = set bits | **O(1)** | ✅ |
| Lookup table | Precompute counts for every byte, sum four lookups | O(1) | O(256) | ✅ The production answer for high-throughput code |
| `popcount` instruction | Hardware instruction (`__builtin_popcount`, `int.bit_count()`) | O(1) | O(1) | ✅ What real systems use |

**The decision:** **Brian Kernighan's trick** — `n &= n - 1`, counting iterations.

**Why it beats the shift loop.** Both are O(1) given a fixed 32-bit width, but the constant differs sharply:

| Input | Shift loop | Kernighan |
|---|---|---|
| `128` = `10000000` | **8** iterations | **1** iteration |
| `2³¹ − 1` (all 1s) | 31 | 31 — **identical** |
| `1` | 1 | 1 |

**Kernighan's runs once per set bit; the shift loop runs once per bit position.** They tie only when every bit is set (the answer to section 1's second question) and Kernighan's wins everywhere else — dramatically on sparse numbers.

**Why the identity is worth understanding rather than memorizing.** `n & (n - 1)` shows up constantly in bit manipulation, and knowing *why* it works lets you derive relatives:

| Expression | Effect |
|---|---|
| `n & (n - 1)` | Clears the **lowest set bit** |
| `n & -n` | **Isolates** the lowest set bit (everything else cleared) |
| `n \| (n + 1)` | Sets the **lowest clear bit** |
| `n & (n - 1) == 0` | Tests whether `n` is a **power of two** — at most one bit set |

That last one is a common interview question in its own right, and it falls straight out of this identity.

**Why not `bin(n).count("1")`?** It's the right answer in production Python and it's O(log n) — but the problem is *about* bit manipulation, and a string conversion answers a different question. Mention it, then show the bitwise version.

**What real code does:** modern CPUs have a **`POPCNT` instruction** that does this in one cycle, exposed as `int.bit_count()` in Python 3.10+, `Integer.bitCount` in Java, and `__builtin_popcount` in GCC. The lookup-table approach was the standard software fallback before that instruction was widespread. **Knowing the hardware answer exists is worth a sentence**, even though the interview wants the algorithm.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
count = 0
```
The running tally of set bits removed so far.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
while n:
```
**Loop until every bit is cleared.** Relies on `0` being [falsy](../syntax/truthy-falsy-values.md), so `while n:` reads as "while any bit remains set."

The loop must terminate: each iteration removes exactly one set bit, and there are finitely many — at most 31 given the constraints.
→ [while-loop](../syntax/while-loop.md) · [truthy-falsy-values](../syntax/truthy-falsy-values.md)

```python
    n &= n - 1   # clears the lowest set bit
```
**The whole algorithm in one line.**

`n - 1` flips the lowest set bit to 0 and turns all the zeros below it into 1s. ANDing with the original keeps only the bits **above** the lowest set bit — which is precisely "remove one 1."

Written as the in-place [augmented assignment](../syntax/bitwise-operators.md) `&=`, equivalent to `n = n & (n - 1)`.

There's no need to *check* whether a bit is set or to track *which* one was removed — the operation removes the lowest one that exists, and the loop condition handles termination. **The identity does the work that an explicit bit test would otherwise do.**
→ [bitwise-operators](../syntax/bitwise-operators.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
    count += 1
```
One bit removed, one added to the tally. Since each iteration clears **exactly one** set bit, the iteration count equals the set-bit count.
→ [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
return count
```
`n` has reached 0, so every set bit has been counted.
→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def hammingWeight(self, n: int) -> int:

        count = 0
        while n:
            n &= n - 1   # clears the lowest set bit
            count += 1
        return count
```
</details>

**Trace it** — `n = 11` (binary `1011`, expected answer 3)

| iteration | `n` | binary | `n - 1` | binary | `n & (n-1)` | binary | `count` |
|---|---|---|---|---|---|---|---|
| 1 | 11 | `1011` | 10 | `1010` | **10** | `1010` | 1 |
| 2 | 10 | `1010` | 9 | `1001` | **8** | `1000` | 2 |
| 3 | 8 | `1000` | 7 | `0111` | **0** | `0000` | 3 |
| — | 0 | — | loop exits | | | | |

Return **3** ✅

Watch the bits disappear from the right: `1011` → `1010` → `1000` → `0000`. **Each step removes exactly one 1**, always the lowest remaining, and never disturbs the higher bits.

Iteration 3 is the clearest illustration of the identity: `1000 - 1 = 0111` — the single set bit flipped to 0 and every zero below became 1 — so the AND wipes everything.

**And the sparse case** — `n = 128` (binary `10000000`):

| iteration | `n` | binary | `n - 1` binary | result | `count` |
|---|---|---|---|---|---|
| 1 | 128 | `10000000` | `01111111` | **0** | 1 |

Return **1** ✅ in a **single** iteration.

The shift-based loop would take **8** iterations here, shifting through seven zeros before finishing. **This is where Kernighan's wins**: the work scales with the number of 1s, not with the magnitude of the number.

**And the dense case** — `n = 15` (binary `1111`):

| iteration | `n` binary | result binary | `count` |
|---|---|---|---|
| 1 | `1111` | `1110` | 1 |
| 2 | `1110` | `1100` | 2 |
| 3 | `1100` | `1000` | 3 |
| 4 | `1000` | `0000` | 4 |

Return **4** ✅ — and here both approaches take 4 iterations, since every bit position is also a set bit. **All-ones input is the only case where the two are equally fast.**

</details>

<details>
<summary><b>4 · Time complexity</b> — O(k), where k is the number of set bits</summary>

**O(k)** — one iteration per set bit — which given the constraints is **O(1)**, since k ≤ 31.

- Each iteration removes exactly one set bit and does O(1) work: a subtraction, an AND, and an increment.
- The loop runs exactly **k** times, where k is the Hamming weight.
- With `n < 2³¹`, **k ≤ 31**, so this is a bounded constant.

**Best case: 1 iteration** (a single set bit, like 128 or any power of two). **Worst case: 31 iterations** (all bits set).

**Against the shift loop:** that one is **O(b)** where b is the bit *width* — 31 iterations regardless of the input's sparsity. Both are O(1) under fixed width, but the constants differ by up to 31×.

**The distinction is worth stating precisely:** *"the shift approach is O(number of bit positions), Kernighan's is O(number of set bits) — they tie only when every bit is set."* That's a more informative answer than calling both O(1), and it's the reason the trick exists.

**Faster still?** Yes:
- A **lookup table** over bytes gives O(1) with four lookups regardless of the pattern.
- The **`POPCNT` instruction** does it in a single CPU cycle — that's what `int.bit_count()` compiles to in Python 3.10+.

Neither is what an interview is asking for, but knowing where the ceiling is completes the picture.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — one integer counter. The input is modified in place (a local copy in Python, since integers are immutable and `n` is rebound), and nothing is allocated.

| Approach | Space | Why |
|---|---|---|
| `bin(n).count("1")` | **O(log n)** | Builds a string of ~32 characters |
| Shift-and-test loop | **O(1)** | One counter |
| **Kernighan's** | **O(1)** | One counter |
| Byte lookup table | **O(256)** | Precomputed, but constant and shared |

**The string version's O(log n) is the interesting comparison** — it's easy to overlook that `bin(n)` allocates. For a single call that's irrelevant, but in a tight loop over millions of integers the allocation dominates, which is precisely why the bitwise version matters in real code.

**Nothing here needs to grow.** The algorithm never records *which* bits were set, only how many — so a single counter suffices. **That's the same compression as [Single Number](136-single-number.md)**: the operation's structure means you don't need to remember what you've seen, only accumulate.

**A note on Python specifics:** `n &= n - 1` rebinds the local name rather than mutating the caller's value, since Python integers are immutable. So the caller's variable is unaffected — no side effect to flag, unlike the in-place array mutations elsewhere in this roadmap.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The straightforward approach checks each bit position — AND with 1, shift right, repeat — which is 31 iterations regardless of the input. Better is Brian Kernighan's trick: `n & (n - 1)` clears the lowest set bit. It works because subtracting 1 flips the lowest set bit to 0 and turns all the zeros below it into 1s, so ANDing with the original keeps only the bits above it. Each application removes exactly one 1, so I loop until n is zero and count the iterations. That's O(number of set bits) rather than O(number of bit positions) — for 128, which is a single bit, it's one iteration instead of eight. They only tie when every bit is set. O(1) space. In production I'd just use `int.bit_count()`, which maps to the CPU's POPCNT instruction."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why does `n & (n - 1)` clear the lowest set bit?" | Subtracting 1 flips the lowest set bit to 0 and sets every bit below it to 1. ANDing keeps only the bits above — the lowest 1 is gone and nothing else changed. |
| "How do you *isolate* the lowest set bit instead?" | `n & -n`. In two's complement, `-n` is `~n + 1`, which agrees with `n` only at the lowest set bit. |
| "Test whether a number is a power of two." | `n > 0 and n & (n - 1) == 0` — a power of two has exactly one set bit, so clearing it leaves 0. Falls straight out of the same identity. |
| "How much faster is this than shifting?" | Up to 31×, when only one bit is set. Identical when all bits are set. It scales with the answer, not the input width. |
| "What's the fastest possible?" | The `POPCNT` CPU instruction — one cycle. Exposed as `int.bit_count()` (Python 3.10+), `Integer.bitCount` (Java), `__builtin_popcount` (GCC). Before that was widespread, a 256-entry byte lookup table was standard. |
| "What if `n` could be negative?" | In Python, negative integers have conceptually infinite leading 1s, so the loop wouldn't terminate. Mask first: `n & 0xFFFFFFFF`. Fixed-width languages handle it naturally. |
| "Count the bits for every number from 0 to n." | That's [Counting Bits](338-counting-bits.md) — calling this per number is O(n log n), but a DP recurrence gets it to O(n). |
| "Why not `bin(n).count('1')`?" | It's what I'd write in real code, but it allocates a string — O(log n) space — and the question is about bit manipulation. |

**Traps:**
- **`n & (n - 1)` versus `n & -n`** — the first *clears* the lowest set bit, the second *isolates* it. Confusing them is easy and produces an infinite loop here.
- **Writing `n = n & 1` instead of `n &= n - 1`** — collapses `n` to 0 or 1 immediately.
- Forgetting to decrement or reassign `n` at all — infinite loop.
- Using `while n > 0` with a potentially negative input in Python — it terminates, but silently returns the wrong count. Mask instead.
- Counting bit *positions* rather than set bits and reporting 32.
- Assuming Python integers are 32 bits. They're arbitrary-precision, which matters for negatives and for [Reverse Bits](190-reverse-bits.md).

**This same move shows up in:** [Counting Bits](338-counting-bits.md) (the same counting problem across a range, solved by a DP recurrence instead) · [Single Number](136-single-number.md) (a bitwise identity replacing explicit bookkeeping) · [Sum of Two Integers](371-sum-of-two-integers.md) (building arithmetic from bit operations) · [Reverse Bits](190-reverse-bits.md) (per-bit extraction with shifts and masks).

</details>

---
