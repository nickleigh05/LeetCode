# 50. Pow(x, n)

**Medium** · [LeetCode](https://leetcode.com/problems/powx-n/) · [Solution file (no hints)](../../problems/0001-0499/50.py)

[📖 17. Math & Geometry lesson](../learning/19-math-geometry.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 17. Math & Geometry problems](../rmap-practice/17-math-geometry.md)

---

Implement `pow(x, n)`, which calculates `x` raised to the power `n` (that is, `xⁿ`).

```
x = 2.00000,  n = 10   →  1024.00000
x = 2.10000,  n = 3    →  9.26100
x = 2.00000,  n = -2   →  0.25000     2⁻² = 1/2² = 1/4
```

**Constraints:** `-100.0 < x < 100.0` · `-2³¹ <= n <= 2³¹ − 1` · `n` is an integer · either `x` is not zero or `n > 0` · `-10⁴ <= xⁿ <= 10⁴`.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| compute `xⁿ` | The naive loop multiplies `x` by itself n times — **O(n)** |
| `n` up to **2³¹ − 1** | About 2.1 billion iterations. **O(n) will time out**, and that's the whole reason this isn't Easy |
| `n` can be **negative** | `x⁻ⁿ = 1/xⁿ`. Needs explicit handling, and the boundary is a trap (see below) |
| `x` is a **float** | Floating-point, so exact equality is unreliable and tiny precision drift is expected |
| `xⁿ` bounded by 10⁴ | The answer stays small even though n is huge — because `x` near 1, or fractional, keeps it in range |

The naive approach is `result = 1; for _ in range(n): result *= x`. Correct, and at n = 2³¹ it's 2.1 billion multiplications. Too slow.

**The speedup comes from a single algebraic identity:**

```
x⁸ = (x⁴)²  =  ((x²)²)²
```

Rather than multiplying by `x` eight times, **square three times**. Each squaring doubles the exponent, so reaching exponent n takes only about **log₂ n** steps — 31 instead of 2.1 billion.

For odd exponents there's a leftover factor:

```
x⁹ = x · x⁸ = x · (x⁴)²
```

So the recurrence is:

```
xⁿ  =  (x²)^(n/2)            if n is even
    =  x · (x²)^(n/2)        if n is odd, with integer division
```

Both cases halve the exponent, which is what guarantees the logarithmic depth.

**Negative exponents** are handled by the identity `x⁻ⁿ = (1/x)ⁿ` — invert the base, flip the sign of the exponent, and proceed as normal.

And there's a **genuine trap** in that flip. The constraint says `n >= -2³¹`, and in a fixed-width 32-bit signed integer, `-(-2³¹)` **overflows** — because `+2³¹` isn't representable. Python's arbitrary-precision integers make this a non-issue, but in Java or C++ you'd need to widen to a `long` first. **That's exactly why the constraint is stated so precisely**, and noticing it is worth saying out loud even in a language where it doesn't bite.

🤔 **Before you open the next section:** the odd case returns `x * self.myPow(x * x, n // 2)`. For `n = 5`, that's `x * myPow(x², 2)` = `x · x⁴` = `x⁵` ✓. Check it for `n = 7` — does the integer division lose anything?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Multiply n times | `result *= x` in a loop | **O(n)** | O(1) | ❌ 2.1 billion iterations at the limit |
| Built-in `x ** n` | Let the language do it | O(log n) | O(1) | ❌ Sidesteps the exercise entirely |
| `exp(n · log x)` | Use logarithms | O(1) | O(1) | ❌ Precision loss, and breaks for negative `x` |
| **Recursive fast exponentiation** | Square the base, halve the exponent | **O(log n)** | O(log n) stack | ✅ |
| Iterative (binary exponentiation) | Same identity, driven by the bits of n | **O(log n)** | **O(1)** | ✅ Strictly better space; worth naming |

**The decision:** **recursive [fast exponentiation](../algorithms/fast-exponentiation.md)** — the identity written directly.

**Why halving beats decrementing.** The naive loop reduces the exponent by **1** per step, needing n steps. Squaring reduces it by a **factor of 2**, needing log₂ n steps. At n = 2³¹ that's the difference between 2.1 × 10⁹ and **31** operations — a factor of 70 million.

**This is the same structural idea as binary search**: don't step through the space, halve it. Once you notice that `xⁿ` can be built from `x^(n/2)` with one extra multiplication, the logarithmic bound is forced.

**Why the odd case works** — the answer to section 1's question. For `n = 7`, integer division gives `7 // 2 = 3`, so the call is `x · myPow(x², 3)` = `x · (x²)³` = `x · x⁶` = `x⁷` ✓. **The integer division discards exactly the factor that the leading `x *` puts back**, which is why the pairing is exact rather than approximate.

**Why not the logarithm trick?** `exp(n · ln x)` is O(1) and mathematically valid for positive `x`, but it introduces floating-point error at every step and is undefined for negative bases. The problem wants integer-exponent exponentiation, not a numerical approximation.

**Why mention the iterative version?** The recursion is O(log n) **stack space**, and the iterative form removes it:

```python
result = 1
while n:
    if n % 2:
        result *= x
    x *= x
    n //= 2
return result
```

That's **binary exponentiation** — it reads the bits of `n` from the least significant end, squaring `x` at each bit position and multiplying into the result wherever a bit is set. Same O(log n) time, **O(1) space**. It's the version you'd use in production; the recursive one is easier to derive under pressure and maps directly onto the identity.

**The connection worth naming:** this exact technique powers modular exponentiation in RSA, and [matrix exponentiation](../algorithms/matrix-exponentiation.md) for computing Fibonacci in O(log n) — the operation changes, the halving structure doesn't.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
if n == 0:
    return 1
```
**The base case.** Anything to the power 0 is 1, including `0⁰` by convention (and the constraints exclude the ambiguous case where `x = 0` and `n <= 0`).

This is also what terminates the recursion: each call halves `n`, so it strictly decreases toward 0.
→ [if-return](../syntax/if-return.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
if n < 0:
    x, n = 1 / x, -n
```
**Negative exponents, via `x⁻ⁿ = (1/x)ⁿ`.** Invert the base and flip the exponent's sign, then everything below runs on a positive exponent.

Doing both assignments with a [tuple assignment](../syntax/swap-tuple-assign.md) evaluates the right-hand side first, so `1 / x` uses the original `x` — writing them as two separate statements in the wrong order would compute `1 / x` after `x` had changed.

**The overflow note:** `-n` when `n = -2³¹` produces `+2³¹`, which doesn't fit in a signed 32-bit integer. Python's integers are unbounded so this is fine, but in Java or C++ you'd promote to `long` before negating. The constraint `n >= -2³¹` is stated precisely to surface this.

This check runs only once at the top level — every recursive call receives a positive `n`, so it never fires again.
→ [swap-tuple-assign](../syntax/swap-tuple-assign.md) · [int-float-basics](../syntax/int-float-basics.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
if n % 2 == 0:
    return self.myPow(x * x, n // 2)
```
**The even case: `xⁿ = (x²)^(n/2)`.**

Square the base and halve the exponent — a single recursive call, no leftover factor. This is where the halving happens, and it's why the depth is log₂ n rather than n.

`n // 2` is [floor division](../syntax/integer-division-modulo.md), keeping the exponent an integer.
→ [integer-division-modulo](../syntax/integer-division-modulo.md) · [recursion-basics](../syntax/recursion-basics.md) · [fast-exponentiation](../algorithms/fast-exponentiation.md)

```python
else:
    return x * self.myPow(x * x, n // 2)
```
**The odd case: `xⁿ = x · (x²)^(n//2)`.**

With `n` odd, halving loses a factor of `x` — `n // 2` rounds down — so one explicit `x *` puts it back.

Verify on `n = 5`: `x · myPow(x², 2)` = `x · (x²)²` = `x · x⁴` = `x⁵` ✓. And `n = 7`: `x · (x²)³` = `x · x⁶` = `x⁷` ✓.

**The exponent still halves in this branch**, which is what keeps the recursion logarithmic — the extra multiplication is O(1) work, not an extra level.
→ [elif-else](../syntax/elif-else.md) · [recursion-basics](../syntax/recursion-basics.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def myPow(self, x: float, n: int) -> float:

        if n == 0:
            return 1
        if n < 0:
            x, n = 1 / x, -n

        if n % 2 == 0:
            return self.myPow(x * x, n // 2)
        else:
            return x * self.myPow(x * x, n // 2)
```
</details>

**Trace it** — `x = 2`, `n = 10`

| call | `n` | parity | action | result |
|---|---|---|---|---|
| `myPow(2, 10)` | 10 | even | `myPow(4, 5)` | ← 1024 |
| `myPow(4, 5)` | 5 | **odd** | `4 * myPow(16, 2)` | ← 4 × 256 = **1024** |
| `myPow(16, 2)` | 2 | even | `myPow(256, 1)` | ← 256 |
| `myPow(256, 1)` | 1 | **odd** | `256 * myPow(65536, 0)` | ← 256 × 1 = **256** |
| `myPow(65536, 0)` | 0 | — | base case | **1** |

Return **1024** ✅ — and note it took **5 calls** rather than 10 multiplications. At n = 2³¹ the same structure would take 32 calls instead of 2.1 billion.

Watch the base grow: 2 → 4 → 16 → 256 → 65536. Each squaring doubles the exponent it represents (2¹ → 2² → 2⁴ → 2⁸ → 2¹⁶), and the odd steps are where the accumulated factors get multiplied in.

**And a negative exponent** — `x = 2`, `n = -2`:

| call | `n` | action | result |
|---|---|---|---|
| `myPow(2, -2)` | −2 | `n < 0` → `x = 0.5`, `n = 2`; then even → `myPow(0.25, 1)` | ← 0.25 |
| `myPow(0.25, 1)` | 1 | odd → `0.25 * myPow(0.0625, 0)` | ← **0.25** |
| `myPow(0.0625, 0)` | 0 | base case | **1** |

Return **0.25** ✅ — which is 1/4, as expected for 2⁻².

The sign flip happens **once**, at the top. Every subsequent call sees a positive exponent, so the `n < 0` branch never fires again.

**And an odd-heavy case** — `x = 3`, `n = 5`:

| call | `n` | parity | expression |
|---|---|---|---|
| `myPow(3, 5)` | 5 | odd | `3 * myPow(9, 2)` = 3 × 81 = **243** |
| `myPow(9, 2)` | 2 | even | `myPow(81, 1)` = **81** |
| `myPow(81, 1)` | 1 | odd | `81 * myPow(6561, 0)` = **81** |
| `myPow(6561, 0)` | 0 | — | **1** |

Return **243** ✅ = 3⁵.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(log n)</summary>

**O(log n)**, where n is the absolute value of the exponent.

- Each recursive call performs `n // 2`, so the exponent **halves every level** → the recursion depth is **⌊log₂ n⌋ + 1**.
- Each level does O(1) work: one squaring, one division, one comparison, and at most one extra multiplication.
- Total: **O(log n)**.

At n = 2³¹ that's **31 levels** versus 2.1 billion multiplications for the naive loop — the improvement is roughly 70-million-fold.

**Why halving is the whole game:** the naive approach subtracts 1 from the exponent per step; this divides it by 2. Any algorithm that reduces its input by a constant *factor* rather than a constant *amount* lands at logarithmic depth — the same reason [binary search](704-binary-search.md) is O(log n).

**A note on the multiplication cost.** This analysis assumes each multiplication is O(1), which holds for fixed-width floats. For **arbitrary-precision** numbers (like modular exponentiation on 2048-bit RSA keys) each multiplication costs more, and the total becomes O(log n × M(b)) for b-bit numbers. The halving structure is identical; only the per-operation cost changes.

**Faster?** Not asymptotically. You need at least log₂ n multiplications to reach exponent n by squaring, since each operation at most doubles the exponent. There are marginal wins from **addition-chain exponentiation** (finding the shortest sequence of multiplications for a specific n), but that's an NP-hard optimization for a constant-factor gain.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(log n)</summary>

**O(log n)** — the recursion stack, one frame per halving.

At n = 2³¹ that's **31 frames**, comfortably within Python's default [recursion limit](../syntax/recursion-limit.md) of 1000. So unlike [Longest Increasing Path in a Matrix](329-longest-increasing-path-in-a-matrix.md), depth isn't a practical concern here — the logarithm keeps it tiny no matter how large `n` gets.

| Version | Space | Why |
|---|---|---|
| Naive loop | **O(1)** | One accumulator — but O(n) time |
| **Recursive fast exponentiation** | **O(log n)** | One stack frame per halving |
| Iterative binary exponentiation | **O(1)** | Two variables, no stack |

**The iterative version eliminates the stack entirely:**

```python
result = 1
while n:
    if n % 2:
        result *= x
    x *= x
    n //= 2
return result
```

It's the same identity read from the other direction: **the bits of `n` from least significant upward**. At each bit position, `x` holds `x^(2^k)`; whenever the bit is set, that factor multiplies into `result`. Since `n = Σ 2^k` over its set bits, `xⁿ = Π x^(2^k)` over those same bits.

**O(1) space, same O(log n) time** — strictly better, and it's the form used in real cryptographic libraries. The recursive version is easier to derive from the identity on the spot; **write the recursion, mention the iterative form.**

**On floating-point precision:** repeated squaring compounds rounding error, and at 31 levels the drift is real but small. The problem's tolerance (10⁻⁵) accommodates it. This is also why the `exp(n · log x)` approach is rejected — it introduces error at a single, much larger step.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Multiplying x by itself n times is O(n), and with n up to 2³¹ that's 2.1 billion operations — too slow. The fix is the identity `xⁿ = (x²)^(n/2)`: squaring the base and halving the exponent, so I reach exponent n in about log₂ n steps instead of n. When n is odd, integer division drops a factor of x, so I multiply one back in explicitly — for n = 7 that's `x · (x²)³ = x · x⁶`. Negative exponents use `x⁻ⁿ = (1/x)ⁿ`, inverting the base and flipping the sign once at the top. One thing worth flagging: negating n when n is −2³¹ overflows a signed 32-bit int, since +2³¹ isn't representable — Python's fine, but in Java I'd widen to a long first, and the constraints are stated to surface exactly that. O(log n) time, O(log n) stack — and I could make it O(1) space with the iterative binary-exponentiation form that walks the bits of n."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Make it O(1) space." | Iterative binary exponentiation: while `n`, multiply `result` by `x` when the low bit is set, square `x`, halve `n`. Same time, no stack. |
| "What's the overflow concern?" | `-(-2³¹)` is `+2³¹`, which doesn't fit in a signed 32-bit int. Python is immune, but Java/C++ need a `long` before negating. |
| "Why does the odd case work?" | `n // 2` rounds down, discarding exactly one factor of `x`, which the leading `x *` restores. For n = 7: `x · (x²)³ = x · x⁶ = x⁷`. |
| "Why not use logarithms?" | `exp(n · ln x)` is O(1) but loses precision and is undefined for negative `x`. This problem needs exact integer-exponent semantics. |
| "How does this relate to binary search?" | Both reduce the problem by a constant *factor* per step rather than a constant amount, which is what produces the logarithmic bound. |
| "What about modular exponentiation?" | Identical structure with `% mod` after each multiplication — that's the core of RSA. The halving is what makes 2048-bit exponents feasible. |
| "Can you compute Fibonacci this way?" | Yes — [matrix exponentiation](../algorithms/matrix-exponentiation.md). Raise `[[1,1],[1,0]]` to the n-th power by the same repeated squaring, giving O(log n) Fibonacci. |
| "What about precision?" | Repeated squaring compounds floating-point error over ~31 levels. It's within the problem's 10⁻⁵ tolerance, and it's a reason to prefer this over the logarithm approach, which errs more. |

**Traps:**
- **Forgetting the negative-exponent case** — returns a huge number instead of a fraction.
- **Flipping the sign before inverting the base**, or writing the two assignments in the wrong order without a tuple assignment.
- **Recomputing the recursive call twice** — `myPow(x, n//2) * myPow(x, n//2)` looks equivalent but doubles the work at every level, restoring **O(n)**. Compute once (or pass `x * x`) so each level makes exactly one call.
- Using `n / 2` instead of `n // 2` — float division makes the exponent non-integer and the recursion never terminates cleanly.
- Missing the `n == 0` base case, so the recursion runs forever.
- Assuming `x` is positive. It can be negative, and the sign must come out right — which it does automatically, since squaring and the odd-case multiplication preserve it correctly.

**This same move shows up in:** [Binary Search](704-binary-search.md) (halving the problem each step for a logarithmic bound) · [Sum of Two Integers](371-sum-of-two-integers.md) (bit-level decomposition of an arithmetic operation) · [Counting Bits](338-counting-bits.md) (exploiting the binary structure of a number) · [Merge k Sorted Lists](23-merge-k-sorted-lists.md) (divide-and-conquer halving to turn linear work into logarithmic depth).

</details>

---
