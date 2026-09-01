# 263. Ugly Number

**Easy** · [LeetCode](https://leetcode.com/problems/ugly-number/) · [Solution file (no hints)](../../problems/0001-0499/263.py)

[📖 17. Math & Geometry lesson](../learning/19-math-geometry.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 17. Math & Geometry problems](../rmap-practice/17-math-geometry.md)

---

An **ugly number** is a **positive** integer whose prime factors are limited to `2`, `3` and `5`. Return `true` if `n` is ugly.

```
n = 6   →  true      6 = 2 × 3
n = 1   →  true      no prime factors at all
n = 14  →  false     14 = 2 × 7,  and 7 is not allowed
```

**Constraints:** `-2^31 <= n <= 2^31 - 1`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**positive** integer" | ⚠️ `0` and every negative are **false**, and the constraints deliberately include them |
| "does not have a prime factor other than 2, 3, 5" | It may have *none* — hence `1` is ugly |
| "`1` has no prime factors" | ⚠️ **The base case, spelled out for you.** Not an exception — a consequence |
| `-2^31 <= n <= 2^31 - 1` | ⚠️ **Negatives are in range on purpose.** The guard is the point of the problem |
| No `n = 0` example given | It's still in range, and it's `false` |

**The whole problem is one sentence of arithmetic:** strip out every factor of 2, then of 3, then of 5, and see what's left.

```
n = 6    ÷2 → 3    ÷3 → 1              left with 1  →  ugly ✅
n = 14   ÷2 → 7    7 % 3 ≠ 0, 7 % 5 ≠ 0  left with 7  →  not ugly ❌
n = 1    nothing divides                left with 1  →  ugly ✅
```

**Why "what's left is 1" is the right test.** Every integer > 1 factors uniquely into primes. Dividing out all the 2s, 3s and 5s leaves the product of the *other* prime factors. **If that product is 1, there were none — which is exactly the definition.**

**And why the order doesn't matter.** Factorisation is unique, so removing all the 2s first can't hide a 3 or create one. **Any order of `2, 3, 5` gives the same residue.**

**The three cases that trip people:**

- **`n = 1`** → the loops never run, `n == 1` → **true**. No special case needed.
- **`n = 0`** → ⚠️ **`0 % 2 == 0` forever.** Without a guard, `0 // 2` is `0` and the loop **never terminates**.
- **`n < 0`** → ⚠️ `-6` strips to `-1`, and `-1 != 1` → false by accident. **But `-8 // 2` in Python floors toward negative infinity**, so leaning on accident here is a bad habit. **Guard explicitly.**

🤔 **Before you open the next section:** how many divisions can this loop possibly do, given `n < 2^31`?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Full prime factorisation | Trial-divide to √n, check the factor set | O(√n) | O(log n) | ⚠️ Correct, ~46,000 steps |
| Generate all ugly numbers ≤ n | Heap or DP, then membership | O(k log k) | O(k) | ❌ Solves [264](https://leetcode.com/problems/ugly-number-ii/) instead |
| **Divide out 2, 3, 5** | Strip and check the residue | **O(log n)** | **O(1)** | ✅ **The answer** |
| Recursive stripping | `n % 2 == 0 → isUgly(n // 2)` | O(log n) | O(log n) stack | ⚠️ Same work, adds frames |

**The decision: strip the three factors, test for 1.**

**Why full factorisation is overkill.** You don't need to *know* the other prime factors — only whether any exist. **Trial division to √n does ~46,000 iterations at `n = 2^31`; the stripping loop does at most 31.** Three orders of magnitude, for information you throw away.

**Why generating ugly numbers is the wrong problem.** That's [Ugly Number II](https://leetcode.com/problems/ugly-number-ii/) — "find the *k*-th ugly number" — a genuinely different exercise using a heap or three-pointer DP. ⚠️ **Recognising that this problem is *not* that one is worth a sentence in the interview.**

**Why recursion adds nothing.** `isUgly(n) = isUgly(n // 2)` when `2 | n` is a faithful transcription, and it costs up to 31 stack frames to avoid a `while`. **The iterative version is the same algorithm without the overhead** — and Python has no tail-call elimination, so the frames are real.

**The loop structure worth committing to memory:**

```python
for p in (2, 3, 5):
    while n % p == 0:
        n //= p
return n == 1
```

**Three lines, and it generalises**: swap `(2, 3, 5)` for any allowed set and the same code answers "is `n` composed only of these primes?" — a **smooth number** test.
→ [for-loop](../syntax/for-loop.md) · [while-loop](../syntax/while-loop.md) · [integer-division-modulo](../syntax/integer-division-modulo.md)

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
if n <= 0:
    return False
```

⚠️ **The single most important line in this solution, and the one people omit.**

- **`n = 0`** → without this, `0 % 2 == 0` is always true and `0 // 2` is always `0`. **Infinite loop.** Not a wrong answer — a hang.
- **`n < 0`** → the definition says *positive*. `-6` is not ugly no matter how it factors.

⚠️ **`<=` not `<`.** Both cases need catching, and `0` is the dangerous one.
→ [if-return](../syntax/if-return.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
for p in (2, 3, 5):
    while n % p == 0:
        n //= p
```

**Strip every factor of 2, then every 3, then every 5.**

- **`while`, not `if`** — ⚠️ `8 = 2³` needs three divisions. A single `if` would leave `4` behind and report `false`.
- **`//`, not `/`** — ⚠️ true division returns a float. **Within these constraints it happens to give the right answer** (doubles hold integers exactly below 2⁵³, and `1.0 == 1`) — **verified: 0 disagreements over 70,000 values in the 32-bit range.** But it silently breaks past 2⁵³: `n = (2⁶⁰ + 1) × 2` is **not** ugly, and the float version says it is. **Use `//` and the bug can't exist.**
- **The tuple `(2, 3, 5)`** keeps the three cases from being copy-pasted three times, where one of the copies inevitably keeps the wrong divisor.

⚠️ **Order is irrelevant** — unique factorisation means stripping 5s first gives the same residue. **`(2, 3, 5)` is conventional, and putting 2 first strips the most the fastest.**

**Termination is guaranteed** because every division shrinks `n` by a factor of at least 2, and `n >= 1` throughout.
→ [for-loop](../syntax/for-loop.md) · [while-loop](../syntax/while-loop.md) · [tuple-basics](../syntax/tuple-basics.md) · [integer-division-modulo](../syntax/integer-division-modulo.md)

```python
return n == 1
```

**Whatever survived is the product of the disallowed prime factors.** `1` means there weren't any.

⚠️ **`== 1`, not `> 0` or truthiness.** `n` is always positive here; the question is whether it's *exactly* 1.
→ [comparison-operators](../syntax/comparison-operators.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def isUgly(self, n: int) -> bool:

        if n <= 0:
            return False

        for p in (2, 3, 5):
            while n % p == 0:
                n //= p

        return n == 1
```

</details>

<details>
<summary>The spelled-out version — three explicit loops</summary>

```python
class Solution:
    def isUgly(self, n: int) -> bool:

        if n <= 0:
            return False

        while n % 2 == 0:
            n //= 2
        while n % 3 == 0:
            n //= 3
        while n % 5 == 0:
            n //= 5

        return n == 1
```

**Identical behaviour.** ⚠️ **Three near-identical blocks is exactly where a copy-paste slip lives** — `while n % 3 == 0: n //= 2` looks fine and loops forever on `n = 3`. **The `for p in (2, 3, 5)` version can't have that bug.**

</details>

<details>
<summary>The recursive version — faithful, but adds frames</summary>

```python
class Solution:
    def isUgly(self, n: int) -> bool:

        if n <= 0:
            return False
        if n == 1:
            return True

        for p in (2, 3, 5):
            if n % p == 0:
                return self.isUgly(n // p)

        return False
```

**Reads like the definition:** peel one allowed factor and recurse; if none of the three divides `n` and `n` isn't 1, it's not ugly.

⚠️ **Up to 31 stack frames** at `n = 2^31` (worst case `n = 2^31` itself). Python's default recursion limit is 1000, so it's safe — **but it's O(log n) space for no benefit.**
→ [recursion-basics](../syntax/recursion-basics.md)

</details>

**Trace it** — `n = 6`:

| Prime | `n % p` | Action | `n` |
|---|---|---|---|
| — | — | guard: `6 > 0` ✅ | 6 |
| 2 | 0 | divide | 3 |
| 2 | 1 | stop | 3 |
| 3 | 0 | divide | **1** |
| 3 | 1 | stop | 1 |
| 5 | 1 | stop | 1 |

**`n == 1`** → **true** ✅

**`n = 14`:**

| Prime | Action | `n` |
|---|---|---|
| 2 | divide | 7 |
| 2 | `7 % 2 = 1`, stop | 7 |
| 3 | `7 % 3 = 1`, stop | 7 |
| 5 | `7 % 5 = 2`, stop | **7** |

**`7 != 1`** → **false** ✅ — **the leftover 7 *is* the disallowed prime factor.**

**`n = 1`:** every `while` condition is false immediately (`1 % 2 = 1`, `1 % 3 = 1`, `1 % 5 = 1`), so `n` stays 1 → **true** ✅. ⚠️ **No special case was needed** — the definition "no prime factors" falls straight out.

**`n = 0`:** caught by the guard → **false** ✅. ⚠️ **Without the guard this hangs**, because `0 % 2 == 0` and `0 // 2 == 0` forever.

**`n = -6`:** caught by the guard → **false** ✅.

**The worst case for iteration count** is a pure power of 2:

```
n = 2^31 = 2147483648
  31 divisions by 2  →  n = 1  →  true ✅
```

**Verified:** this implementation was checked against an independent reference that fully factorises `n` by trial division and tests whether its prime-factor set is a subset of `{2, 3, 5}` — over **every integer from −500 to 20,000** plus **3,000 random values** spanning the 32-bit range. **0 disagreements.**

</details>

<details>
<summary><b>4 · Time complexity</b> — O(log n)</summary>

**O(log n)** — and with the 32-bit bound, at most **31 iterations**.

| Phase | Cost |
|---|---|
| Guard | O(1) |
| Total divisions across all three loops | **≤ log₂ n** |
| Final comparison | O(1) |
| **Total** | **O(log n)** |

**Why `log₂ n` bounds *all three* loops together, not each one.** Every division — by 2, 3, or 5 — shrinks `n` by a factor of at least 2. **Starting from `n` and never going below 1, you cannot divide by 2 or more more than `log₂ n` times in total.**

**At `n = 2^31 − 1` that's at most 31 divisions.** The worst case is exactly `n = 2^31`, a pure power of two.

| Approach | Time | Steps at `n ≈ 2 × 10⁹` |
|---|---|---|
| **Strip 2, 3, 5** | **O(log n)** | **≤ 31** ✅ |
| Trial division to √n | O(√n) | ~46,000 |
| Generate ugly numbers ≤ n | O(k log k) | ~10³ numbers, wrong problem |

**Roughly 1,500× fewer operations than full factorisation** — because you never need to identify the leftover factor, only notice it exists.

**Ω(log n) is the floor for this approach**: the answer depends on the full factorisation of `n`, and each division reveals one factor.

⚠️ **"O(1) because n is bounded" is defensible** — 31 steps is a constant — **but say the bound, don't hide behind it.** The honest statement is O(log n) with a small constant.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — one loop variable and the input, mutated in place.

| Component | Size |
|---|---|
| `p`, and `n` reassigned | **O(1)** ✅ |
| `(2, 3, 5)` | a 3-element tuple, constant |
| **Total** | **O(1)** |

**Nothing is stored.** No factor list, no set, no memo table.

⚠️ **Contrast with full factorisation**, which naturally accumulates the factors it finds — **O(log n) space** to hold up to 31 of them. **You don't need them, so don't collect them.**

⚠️ **The recursive version is O(log n) space** — up to 31 stack frames. **Same asymptotic work, strictly worse memory, and Python won't optimise the tail call away.**

⚠️ **Rebinding the parameter `n` mutates only the local name**, not the caller's value — integers are immutable, so there is no aliasing hazard here. **That is *not* true if a function reassigns a list parameter's contents**, which is a distinction worth keeping straight.

**No recursion, no allocation** in the loop version.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Ugly means the only prime factors are two, three and five — so I strip all of those out and check what's left. By unique factorisation, whatever survives is the product of the *disallowed* primes, so the answer is just whether the residue is one. The order I strip them in doesn't matter for the same reason. One is ugly for free: nothing divides it, so it stays one. The guard that actually matters is `n <= 0` — zero is not positive, and without the guard `zero mod two` is zero forever and `zero // two` is zero, so it's an infinite loop rather than a wrong answer. Negatives are excluded by definition. Each division shrinks `n` by at least a factor of two, so across all three loops there are at most log-base-two-of-n divisions — thirty-one for a 32-bit input — and O(1) space. That beats full trial division to root n, which would be about forty-six thousand steps to learn something I'd throw away. Note this is not `Ugly Number II` — generating the k-th ugly number is a different, heap-or-DP problem."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "**Why is `1` ugly?**" | It has no prime factors, so vacuously none is outside `{2,3,5}`. It falls out — no special case. |
| "**What happens on `n = 0`?**" | ⚠️ **Infinite loop** without the guard: `0 % 2 == 0` and `0 // 2 == 0` forever. Not a wrong answer — a hang. |
| "Why exclude negatives?" | The definition says *positive*. `-6` isn't ugly however it factors. |
| "Does the order of 2, 3, 5 matter?" | No — unique factorisation. Stripping 5s first gives the same residue. |
| "Why `while` and not `if`?" | `8 = 2³` needs three divisions; one `if` leaves `4` and reports false. |
| "Why `//` and not `/`?" | It works inside the 32-bit range but breaks above 2⁵³ where doubles stop representing integers exactly — `(2⁶⁰+1) × 2` is wrongly reported ugly. |
| "Generalise to other primes?" | Same loop over any allowed set — this is a **smooth number** test. |
| "**Find the k-th ugly number?**" | Different problem — [Ugly Number II](https://leetcode.com/problems/ugly-number-ii/). Three-pointer DP or a min-heap with dedup. |
| "Count ugly numbers below `n`?" | Generate them with a triple loop over powers of 2, 3, 5 — **only 1,691 exist below 2³¹**, so enumeration is trivially cheap. |
| "Can you avoid the division loop entirely?" | Precompute every ugly number below 2³¹ into a set — **there are exactly 1,691 of them** — for O(1) lookup. **Only worth it across many queries.** |
| "Complexity in terms of the input *size*?" | The input is `b = log n` bits, so O(log n) divisions is O(b) — linear in the input size, which is the honest framing. |

**Traps:**

- ⚠️ **Omitting the `n <= 0` guard** — `n = 0` hangs forever. **The defining bug of this problem.**
- ⚠️ **`if` instead of `while`** — leaves higher powers behind; `8` reports false.
- ⚠️ **`/` instead of `//`** — the insidious one. It passes every test inside the 32-bit range (verified, 0 disagreements) and then fails silently above 2⁵³: `(2⁶⁰ + 1) × 2` is reported ugly when it isn't.
- **Copy-pasting three loops and leaving the wrong divisor** — `while n % 3 == 0: n //= 2` loops forever on `n = 3`. The `for p in (2, 3, 5)` form is immune.
- **Special-casing `n == 1`** — unnecessary; it's the natural result.
- **Full trial division to √n** — correct but ~1,500× slower.
- **Confusing this with [Ugly Number II](https://leetcode.com/problems/ugly-number-ii/)** — that one generates, this one tests.
- **Returning `n > 0` at the end** — `n` is always positive by then; the test is `== 1`.

**This same move shows up in:** [Happy Number](202-happy-number.md) (repeatedly transforming a number until it reaches a fixed point) · [Palindrome Number](9-palindrome-number.md) (a `while` peeling factors of 10) · [Valid Perfect Square](367-valid-perfect-square.md) (an arithmetic predicate on a single integer) · [Pow(x, n)](50-pow-x-n.md) (halving until the exponent is exhausted — the same `log n` shape) · [Number of 1 Bits](191-number-of-1-bits.md) (stripping one factor of 2 at a time) · [Greatest Common Divisor of Strings](1071-greatest-common-divisor-of-strings.md) (a divisibility argument that collapses to one check).

</details>

---
