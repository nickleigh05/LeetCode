# 371. Sum of Two Integers

**Medium** · [LeetCode](https://leetcode.com/problems/sum-of-two-integers/)

[📖 19. Bit Manipulation lesson](../learning/19-bit-manipulation.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 19. Bit Manipulation problems](../rmap-practice/19-bit-manipulation.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Given two integers `a` and `b`, return their **sum** — without using the operators `+` and `-`.

```
a = 1, b = 2     →  3
a = 2, b = 3     →  5
a = -1, b = 1    →  0
```

**Constraints:** `-1000 <= a, b <= 1000`.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| add **without `+` or `-`** | You must rebuild addition from more primitive operations — which means **bitwise** |
| integers, possibly **negative** | Negative numbers are represented in **two's complement**, and that representation is what makes the bit tricks work uniformly |
| `-1000 <= a, b <= 1000` | Small values, but the sign handling is where the difficulty lives |
| (implied) fixed-width semantics | The problem assumes 32-bit integers. **Python's arbitrary-precision integers break that assumption**, which is the real challenge here |

Think about how addition works at the bit level, one column at a time:

| `a` bit | `b` bit | sum bit | carry out |
|---|---|---|---|
| 0 | 0 | 0 | 0 |
| 0 | 1 | **1** | 0 |
| 1 | 0 | **1** | 0 |
| 1 | 1 | 0 | **1** |

Look at the "sum bit" column: it's 1 exactly when the inputs **differ**. That's **XOR**.

Look at the "carry out" column: it's 1 exactly when **both** inputs are 1. That's **AND** — and the carry belongs in the *next* column up, so shift it left by one.

```
a ^ b          →  the sum, ignoring all carries
(a & b) << 1   →  the carries, positioned where they need to be added
```

Neither alone is the answer, but together they *are* the answer — just not yet combined. So **add them**... which is the operation you're trying to implement. Recursion, but productive recursion:

```
sum(a, b) = sum(a ^ b, (a & b) << 1)
```

Each round folds the carries into the sum and produces a new, **smaller** set of carries. Since carries shift left every round, they eventually shift off the top and vanish. **When the carry is 0, the XOR alone is the answer.**

This is precisely how a hardware **ripple-carry adder** works — you're implementing the circuit.

**Now the Python-specific complication**, which is most of the code below. In C, integers are 32 bits: carries shift off the end and disappear, and negative numbers are two's-complement bit patterns that add correctly with no special handling. In Python, integers are **arbitrary-precision**, so:

- Carries never shift off the top — they keep growing, and the loop **never terminates** for negative inputs.
- A negative Python integer conceptually has **infinitely many leading 1s**, so the bit pattern doesn't match a 32-bit two's-complement value.

The fix is to **simulate fixed width with a mask**, then convert the result back to a signed Python integer at the end.

🤔 **Before you open the next section:** the final step is `a = ~(a ^ mask)` when `a` exceeds `0x7FFFFFFF`. What is that expression doing, and why is `0x7FFFFFFF` the threshold?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| `sum([a, b])` or `math.fsum` | Use a built-in that hides the `+` | O(1) | O(1) | ❌ A loophole, not a solution — it's still addition |
| Repeated increment | Increment `a` and decrement `b` in a loop | O(b) | O(1) | ❌ And incrementing needs `+` anyway |
| **XOR for sum, AND-shift for carry** | Rebuild the ripple-carry adder | **O(1)** — ≤32 rounds | **O(1)** | ✅ |
| Recursion on the same identity | `getSum(a ^ b, (a & b) << 1)` | O(1) | O(1) stack | ✅ Same idea, recursive form |

**The decision:** the **XOR/AND-shift loop**, with masking to simulate 32-bit width.

**Why this decomposition is *the* answer.** Addition at the bit level is exactly two things: a **sum without carry** and a **carry**. XOR computes the first, AND-then-shift computes the second. There's no cleverness to find — **the truth table hands you the two operators**, and the only insight needed is realizing that combining them is itself an addition, so you iterate until there's nothing left to combine.

**Why it terminates.** Each round, the carry is shifted left by one. So the carry's lowest set bit moves strictly upward every iteration, and after at most 32 rounds it has been shifted out of the 32-bit window entirely. **The loop is bounded by the bit width**, which is what makes it O(1).

**The masking, explained properly** — this is the part that makes the Python version look so much more complicated than the C version:

- **`mask = 0xFFFFFFFF`** is 32 ones. ANDing with it keeps only the low 32 bits, **discarding anything that shifted above** — exactly what a hardware register does automatically.
- **`while b & mask:`** tests whether any carry remains *within* the 32-bit window. Without the mask, a negative number's infinite leading 1s would keep the condition true forever.

**The final conversion** — the answer to section 1's question:

After the loop, `a` holds a 32-bit pattern as a *non-negative* Python integer, somewhere in `0 .. 0xFFFFFFFF`. But in 32-bit two's complement, patterns above `0x7FFFFFFF` (which is 2³¹ − 1, the largest positive) represent **negative** numbers. So:

```python
if a > 0x7FFFFFFF:
    a = ~(a ^ mask)
```

`a ^ mask` flips all 32 bits (that's the one's complement within the window), and `~` negates-and-subtracts-one in Python's infinite-precision world. Together they reinterpret the pattern as the negative value it stands for. **`0x7FFFFFFF` is the threshold because it's the boundary between "positive in 32-bit two's complement" and "negative."**

**Why not the recursive form?** `return b == 0 and a or self.getSum(a ^ b, (a & b) << 1)` is the same identity and equally valid — it just needs the same masking, and the iterative version makes the bounded-rounds argument more visible.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
mask = 0xFFFFFFFF   # keep results within 32 bits
```
**A 32-bit window**, since Python integers have no inherent width.

`0xFFFFFFFF` is 32 consecutive 1s. ANDing any value with it keeps the low 32 bits and discards everything above — **simulating the overflow behaviour a hardware register gives you for free.**

Every line below exists to work within this window.
→ [bitwise-operators](../syntax/bitwise-operators.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
while b & mask:
```
**Loop while a carry remains inside the window.**

`b` holds the pending carry. Once it's zero (within 32 bits), `a` alone is the answer.

The `& mask` is essential and not decorative: for negative Python integers, `b` conceptually has infinitely many leading 1s, so a bare `while b:` would **never terminate**. Masking asks the right question — *"is there a carry in the bits we actually care about?"*
→ [while-loop](../syntax/while-loop.md) · [bitwise-operators](../syntax/bitwise-operators.md)

```python
    carry = (a & b) << 1
```
**Compute the carry.** A carry is generated at every position where **both** `a` and `b` have a 1 — that's the AND — and it applies to the **next column up**, hence the left shift.

Computing it *before* `a` is overwritten on the next line is essential; both operations need the original values.
→ [bitwise-operators](../syntax/bitwise-operators.md)

```python
    a = (a ^ b) & mask
```
**The sum without carries**, masked back into the window.

XOR sets a bit wherever exactly one of `a`, `b` has one — which is the correct sum bit whenever no carry is involved. The `& mask` discards anything that has drifted above bit 31.
→ [bitwise-operators](../syntax/bitwise-operators.md)

```python
    b = carry & mask
```
**The carry becomes the new addend.** Next round adds it into the running sum, potentially generating further carries — each one shifted a position higher.

The mask drops carries that have shifted past bit 31, which is exactly the overflow a 32-bit register would discard. **This is what guarantees termination**: carries can only move up, and there are only 32 places to go.
→ [bitwise-operators](../syntax/bitwise-operators.md)

```python
if a > 0x7FFFFFFF:   # reinterpret as a negative 32-bit signed number
    a = ~(a ^ mask)
```
**Convert the 32-bit pattern back to a signed Python integer.**

After the loop, `a` is a non-negative Python integer holding a 32-bit pattern. In two's complement, patterns above `0x7FFFFFFF` = 2³¹ − 1 represent negatives — bit 31 is the sign bit.

The conversion: `a ^ mask` flips all 32 bits (one's complement within the window), and `~x` in Python computes `-x - 1`. Composed, they map the unsigned pattern to the signed value it denotes.

**Worked example:** the 32-bit pattern for −1 is `0xFFFFFFFF`. Then `a ^ mask` = 0, and `~0` = **−1** ✓
→ [bitwise-operators](../syntax/bitwise-operators.md) · [if-return](../syntax/if-return.md)

```python
return a
```
→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def getSum(self, a: int, b: int) -> int:

        mask = 0xFFFFFFFF   # keep results within 32 bits

        while b & mask:
            carry = (a & b) << 1
            a = (a ^ b) & mask
            b = carry & mask

        if a > 0x7FFFFFFF:   # reinterpret as a negative 32-bit signed number
            a = ~(a ^ mask)

        return a
```
</details>

**Trace it** — `a = 3`, `b = 5` (binary `011` and `101`, expected 8)

| round | `a` | `b` | `a & b` | `carry = (a&b)<<1` | `a ^ b` | new `a` | new `b` |
|---|---|---|---|---|---|---|---|
| 1 | `011` (3) | `101` (5) | `001` | `010` (2) | `110` (6) | **6** | **2** |
| 2 | `110` (6) | `010` (2) | `010` | `100` (4) | `100` (4) | **4** | **4** |
| 3 | `100` (4) | `100` (4) | `100` | `1000` (8) | `000` (0) | **0** | **8** |
| 4 | `0000` (0) | `1000` (8) | `0000` | `0` | `1000` (8) | **8** | **0** |
| — | `b` is 0 → loop exits; `8 <= 0x7FFFFFFF` so no conversion | | | | | | |

Return **8** ✅

Watch the carry climb: `010` → `100` → `1000`, one position left each round. **That upward march is why the loop is bounded** — after at most 32 rounds the carry exits the window.

Round 3 is the interesting one: the XOR produces **0**, so the entire value now lives in the carry. Round 4 then folds it back in with nothing to carry, and the loop ends.

**And a negative case** — `a = -1`, `b = 1` (expected 0):

In 32-bit two's complement, `-1` is `0xFFFFFFFF`.

| round | `a` | `b` | `a & b` | `carry` | `a ^ b` | new `a` | new `b` |
|---|---|---|---|---|---|---|---|
| 1 | `0xFFFFFFFF` | `1` | `1` | `2` | `0xFFFFFFFE` | **0xFFFFFFFE** | **2** |
| 2 | `0xFFFFFFFE` | `2` | `2` | `4` | `0xFFFFFFFC` | **0xFFFFFFFC** | **4** |
| … | carries keep climbing | | | | | | |
| 32 | `0x80000000` | `0x80000000` | `0x80000000` | `0x100000000` | `0` | **0** | `0x100000000 & mask` = **0** |

The final carry `0x100000000` is bit 32 — **outside the window** — so `& mask` clears it to 0 and the loop exits with `a = 0`.

Return **0** ✅

**This is exactly where the mask earns its place.** Without it, `b` would become `0x100000000` and keep growing forever, since Python would happily represent bit 32, bit 33, and beyond. **The mask supplies the overflow that a 32-bit register does automatically.**

**And a case needing the sign conversion** — `a = -2`, `b = 1` (expected −1):

The loop resolves to `a = 0xFFFFFFFF`. Since `0xFFFFFFFF > 0x7FFFFFFF`, the conversion fires: `a ^ mask` = `0xFFFFFFFF ^ 0xFFFFFFFF` = **0**, then `~0` = **−1** ✅

</details>

<details>
<summary><b>4 · Time complexity</b> — O(1)</summary>

**O(1)** — at most **32 iterations**, bounded by the bit width.

- Each round shifts the carry **left by one**, so its lowest set bit moves strictly upward.
- After at most 32 rounds the carry has been shifted entirely out of the 32-bit window and masked to 0.
- Each round does a handful of O(1) bitwise operations.
- **O(1)** total, or **O(b)** for a b-bit width if you prefer to state the dependency.

**In practice it's usually far fewer than 32 rounds** — the loop ends as soon as the carry is zero. For `3 + 5` it took 4 rounds; for two numbers with no overlapping set bits (say `4 + 2` = `100` + `010`), the very first XOR is the answer and the carry is 0 immediately, so it's **one round**.

**Worst case** is inputs whose carries ripple all the way up — like `-1 + 1`, which took the full 32 in the trace above. **That's the ripple-carry adder's worst case too**, and it's why real hardware uses carry-lookahead adders that compute all carries in parallel rather than propagating them.

**Faster?** Not with this decomposition — the carry genuinely must propagate. Hardware solves it with lookahead circuits; in software you'd just use `+`, which compiles to a single instruction. **The exercise is about understanding the mechanism, not about speed.**

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — three integers (`mask`, `carry`, and the rebound `a`/`b`), regardless of input.

| Component | Space | Why |
|---|---|---|
| `mask` | O(1) | A constant |
| `carry` | O(1) | One integer per round, reused |
| `a`, `b` | O(1) | Rebound each round; Python integers here are bounded by 33 bits |

No arrays, no recursion, no allocation that grows.

**The recursive formulation** would be O(1) space too in any practical sense — at most 32 stack frames — but the iterative version makes the bounded-rounds argument visible and avoids the stack entirely.

**The Python-versus-C comparison is the real content here.** In C this function is:

```c
int getSum(int a, int b) {
    while (b) {
        int carry = (a & b) << 1;
        a = a ^ b;
        b = carry;
    }
    return a;
}
```

**No mask, no sign conversion, no `0x7FFFFFFF` check.** The `int` type is 32 bits, so carries shift off the end automatically and negative values are already two's-complement patterns that add correctly.

**Every extra line in the Python version exists to simulate what a fixed-width register does for free.** That's worth saying explicitly in an interview — it shows you understand *why* the code looks complicated, rather than having memorized an incantation. The algorithm is four lines; the other four are language compensation.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Addition at the bit level is two things: the sum ignoring carries, and the carries themselves. Looking at the truth table, the sum bit is 1 when the inputs differ — that's XOR — and a carry is generated when both are 1, applying to the next column up — that's `(a & b) << 1`. Neither is the full answer, but adding them together is, so I iterate: XOR becomes the new sum, the shifted AND becomes the new carry, and I repeat until no carry remains. It terminates because the carry shifts left each round, so after at most 32 rounds it's out of the window. That's a ripple-carry adder. The complication is Python: integers are arbitrary-precision, so carries never fall off the end and negative numbers have conceptually infinite leading ones — a naive loop wouldn't terminate. So I mask with `0xFFFFFFFF` to simulate a 32-bit register, and at the end, if the result exceeds `0x7FFFFFFF` it's a negative two's-complement pattern, so I convert it back with `~(a ^ mask)`. In C this would be four lines with no masking at all."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why XOR for the sum and AND for the carry?" | Straight from the truth table: the sum bit is 1 when the inputs differ (XOR), and a carry occurs when both are 1 (AND), applying one column up (shift left). |
| "Why does the loop terminate?" | The carry shifts left every round, so its lowest set bit rises. After at most 32 rounds it's shifted past bit 31 and the mask clears it. |
| "Why is the mask needed in Python but not C?" | C's `int` is 32 bits, so carries fall off the end and negatives are already two's-complement patterns. Python's integers are unbounded, so a negative has infinite leading 1s and the loop would never end. |
| "What does `~(a ^ mask)` do?" | `a ^ mask` flips all 32 bits, and `~x` is `-x - 1`. Together they reinterpret an unsigned 32-bit pattern as its signed value. For `0xFFFFFFFF`: flip to 0, then `~0` = −1. |
| "Why `0x7FFFFFFF` as the threshold?" | It's 2³¹ − 1, the largest positive 32-bit signed value. Anything above it has bit 31 set, which is the sign bit. |
| "Implement subtraction the same way." | `a - b` is `a + (-b)`, and `-b` in two's complement is `~b + 1` — so negate with `~`, then add 1 using this same routine. |
| "Implement multiplication?" | Shift-and-add: for each set bit `i` in `b`, add `a << i` to the result, using this function for the addition. |
| "Why do real CPUs not ripple?" | Ripple-carry is O(b) gate delays. Hardware uses carry-lookahead adders that compute all carries in parallel for O(log b) depth. |

**Traps:**
- **`while b:` instead of `while b & mask:`** — infinite loop on any negative input, since Python's negatives never run out of 1 bits.
- **Overwriting `a` before computing the carry** — both operations need the original values, so `carry` must be computed first.
- **Omitting the sign conversion** — negative results come back as large positive numbers like 4294967295 instead of −1.
- Forgetting to mask `a` or `b` inside the loop, letting values grow past 32 bits.
- Shifting the AND right instead of left — the carry goes to a *higher* column.
- Using `+` anywhere, including in `~b + 1` for negation, which defeats the exercise.

**This same move shows up in:** [Single Number](136-single-number.md) (XOR's algebraic properties doing the work) · [Missing Number](268-missing-number.md) (XOR cancellation) · [Reverse Bits](190-reverse-bits.md) (masking to simulate fixed width in Python) · [Pow(x, n)](50-pow-x-n.md) (rebuilding an arithmetic primitive from a lower-level operation).

</details>

---
