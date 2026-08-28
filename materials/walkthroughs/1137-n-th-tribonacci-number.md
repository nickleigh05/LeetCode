# 1137. N-th Tribonacci Number

**Easy** · [LeetCode](https://leetcode.com/problems/n-th-tribonacci-number/) · [Solution file (no hints)](../../problems/1000-1499/1137.py)

[📖 14. 1-D DP lesson](../learning/14-dp-1d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 13. 1-D Dynamic Programming problems](../rmap-practice/13-dp-1d.md)

---

`T₀ = 0`, `T₁ = 1`, `T₂ = 1`, and `Tₙ₊₃ = Tₙ + Tₙ₊₁ + Tₙ₊₂`. Return `Tₙ`.

```
n = 4   →  4          T₃ = 0+1+1 = 2,  T₄ = 1+1+2 = 4
n = 25  →  1389537
```

**Constraints:** `0 <= n <= 37` · the answer fits in a signed 32-bit integer

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| `Tₙ₊₃ = Tₙ + Tₙ₊₁ + Tₙ₊₂` | ⚠️ The recurrence is **given**. No modelling required |
| three base cases | `T₀ = 0`, `T₁ = 1`, `T₂ = 1` — all three needed |
| `0 <= n` | ⚠️ `n = 0` is legal and returns **0**, not 1 |
| `n <= 37` | Small — and the bound exists because `T₃₈` would overflow 32 bits |
| "the answer fits in a 32-bit integer" | A hint about *why* 37, irrelevant in Python |

**This is [Climbing Stairs](70-climbing-stairs.md) with a window of three instead of two.** Same shape, same technique, one more variable to carry:

```
Fibonacci  (2-term):  F(n) = F(n-1) + F(n-2)          → keep 2 values
Tribonacci (3-term):  T(n) = T(n-1) + T(n-2) + T(n-3) → keep 3 values
```

The only real decisions are **how many base cases you need** and **whether you store the whole sequence or just a sliding window**.

**Three base cases, not two.** A recurrence looking back three steps needs three seeds — with only `T₀` and `T₁` defined, `T₃ = T₀ + T₁ + T₂` has nothing to stand on. And note they aren't uniform: `T₀ = 0` but `T₁ = T₂ = 1`.

```
n:   0  1  2  3  4  5   6   7   8    9    10
T:   0  1  1  2  4  7  13  24  44   81   149
     └──┬──┘  └─ each is the sum of the three before it
      seeds
```

**Why the naive recursion is catastrophic.** Writing `return trib(n-1) + trib(n-2) + trib(n-3)` branches three ways at every level, so the call tree is roughly **3ⁿ**:

| n | Naive calls (≈) | Iterative steps |
|---|---|---|
| 10 | ~10³ | 10 |
| 25 | ~10¹¹ | 25 |
| **37** | **~10¹⁷** | **37** |

At n = 37 that's beyond astronomical — and every one of those calls recomputes a value already known. **The whole point of DP is that each `Tᵢ` should be computed once.**

🤔 **Before you open the next section:** to compute `T₃₇` you need `T₃₆`, `T₃₅`, `T₃₄`. Once you have `T₃₇`, is `T₃₄` ever needed again?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Naive recursion | Branch three ways | O(3ⁿ) | O(n) | ❌ 10¹⁷ at n=37 |
| Memoised recursion | Cache each value | O(n) | O(n) + stack | ✅ Correct, unnecessary overhead |
| Bottom-up array | Fill `dp[0..n]` | O(n) | **O(n)** | ✅ Clear, wasteful |
| **Three rolling variables** | Keep only the window | **O(n)** | **O(1)** | ✅ ← |
| Matrix exponentiation | 3×3 matrix power | O(log n) | O(1) | ⚠️ Overkill at n≤37 |

**The decision: three rolling variables.**

**The observation that removes the array.** After computing `T₃₇` from `T₃₆, T₃₅, T₃₄`, nothing will ever ask for `T₃₄` again — the recurrence only reaches back three places. So storing all 38 values is pure waste:

```
dp array:          [0, 1, 1, 2, 4, 7, 13, ...]   ← keeps everything, needs nothing old
rolling window:    (t0, t1, t2) sliding forward   ← O(1) space
```

**This is the standard "rolling variables" optimisation**, and it's exactly the step from [Climbing Stairs](70-climbing-stairs.md)'s array to its two-variable form. **Any DP whose transition looks back a fixed number of positions can drop to O(1) space.**

**The shift, written two ways.** Nick's solution file has both, and the second is worth internalising:

```python
# explicit temporary
t3 = t0 + t1 + t2
t0 = t1
t1 = t2
t2 = t3

# simultaneous assignment — same thing, no temporary
t0, t1, t2 = t1, t2, t0 + t1 + t2
```

⚠️ **The one-liner works because Python evaluates the entire right-hand side *before* assigning any of it.** The tuple `(t1, t2, t0+t1+t2)` is built from the *old* values, then unpacked. In a language without simultaneous assignment, writing these as four sequential statements without a temporary would corrupt the window — `t0 = t1` would destroy `t0` before the sum uses it.
→ [swap-tuple-assign](../syntax/swap-tuple-assign.md) · [tuple-unpacking](../syntax/tuple-unpacking.md)

**Why not `functools.cache`?** It works and is one line:

```python
@cache
def trib(n): return 0 if n == 0 else 1 if n <= 2 else trib(n-1) + trib(n-2) + trib(n-3)
```

O(n) time, but O(n) space **and** n stack frames. At n = 37 that's fine; the iterative version is strictly better and shows you understand what the memo is doing.
→ [functools-cache](../syntax/functools-cache.md)

**Matrix exponentiation** gets O(log n) by raising a 3×3 companion matrix to the nth power. **Genuinely useful when n is 10¹⁸** — worth naming as the answer to "what if n were enormous?", but absurd at n ≤ 37.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
if n == 0:
    return 0
if n <= 2:
    return 1
```

**The base cases, guarded before the loop.**

⚠️ `n == 0` must be checked **first and separately** — `T₀ = 0` while `T₁ = T₂ = 1`. Collapsing all three into `if n <= 2: return 1` returns 1 for `n = 0`, which is wrong.

These guards also protect the loop below, which assumes `n >= 3`.
→ [if-return](../syntax/if-return.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
t0, t1, t2 = 0, 1, 1
```

**Seed the window** with `T₀, T₁, T₂`. Multiple assignment on one line keeps the three seeds visually together.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
for i in range(3, n + 1):
    t0, t1, t2 = t1, t2, t0 + t1 + t2
```

**Slide the window forward.**

`range(3, n + 1)` starts at 3 because `T₀..T₂` are already known, and `n + 1` is inclusive of `n` — off by one either way and you return the wrong term.

⚠️ **The simultaneous assignment is doing real work.** The right-hand side is fully evaluated first, so `t0 + t1 + t2` uses the *old* values while `t0` and `t1` simultaneously take on the shifted ones. Writing it as separate statements top-to-bottom without a temporary would break it.

`i` is never used in the body — it's just a repeat counter. (`_` would be idiomatic; `i` is fine and matches the file.)
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md)

```python
return t2
```

**`t2` always holds the most recent term.** After the final iteration that's `Tₙ`.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def tribonacci(self, n: int) -> int:

        if n == 0:
            return 0
        if n <= 2:
            return 1

        t0, t1, t2 = 0, 1, 1
        for i in range(3, n + 1):
            t0, t1, t2 = t1, t2, t0 + t1 + t2

        return t2
```

</details>

<details>
<summary>The explicit-temporary version, if the one-liner feels opaque</summary>

```python
class Solution:
    def tribonacci(self, n: int) -> int:

        if n == 0:
            return 0
        if n <= 2:
            return 1

        t0 = 0
        t1 = 1
        t2 = 1

        for i in range(3, n + 1):
            t3 = t0 + t1 + t2
            t0 = t1
            t1 = t2
            t2 = t3

        return t2
```

Identical behaviour. **Write whichever you can produce correctly under pressure** — the shift order matters only in this version, where `t3` must be computed before anything is overwritten.

</details>

**Trace it** — `n = 6`:

| `i` | `t0` | `t1` | `t2` | new `t2` = t0+t1+t2 |
|---|---|---|---|---|
| — | 0 | 1 | 1 | *(seeds T₀,T₁,T₂)* |
| 3 | 1 | 1 | **2** | 0+1+1 = 2 |
| 4 | 1 | 2 | **4** | 1+1+2 = 4 |
| 5 | 2 | 4 | **7** | 1+2+4 = 7 |
| 6 | 4 | 7 | **13** | 2+4+7 = 13 |

**`T₆ = 13`** ✅

**Read the columns downward** and you see the window sliding: `t2`'s values `1, 2, 4, 7, 13` are the sequence itself, while `t0` and `t1` are the same numbers lagging by two and one. **Three variables tracking one sequence at three offsets.**

**Check `n = 4` against the problem statement:** the row `i = 4` gives `t2 = 4` ✅ — matching `T₃ = 0+1+1 = 2` then `T₄ = 1+1+2 = 4`.

**And the edge cases:**

| `n` | Path taken | Result |
|---|---|---|
| 0 | first guard | **0** ✅ |
| 1 | second guard | **1** ✅ |
| 2 | second guard | **1** ✅ |
| 3 | loop runs once | **2** ✅ |

**`n = 3` is the smallest input that reaches the loop** — `range(3, 4)` is a single iteration. Worth checking by hand, since it's where an off-by-one in the range would first show.

**Verified:** this implementation matches a memoised reference for every `n` from 0 to 37, and `T₂₅ = 1389537` as the problem states.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** — one loop iteration per term, each doing constant work.

At n = 37 that's **35 iterations**. Instantaneous.

**Versus the naive recursion, O(3ⁿ):**

| n | Naive (≈ calls) | Iterative |
|---|---|---|
| 10 | ~10³ | 10 |
| 25 | ~10¹¹ | 25 |
| **37** | **~10¹⁷** | **37** |

**At n = 37 that's roughly 10¹⁶ times more work.** Every branch recomputes values already known — `T₃₄` alone would be recalculated millions of times.

**Memoisation collapses it to O(n)** by computing each value once, which is exactly what the iterative loop does — just without the call overhead or the stack.

⚠️ **A caveat about O(n) here.** Strictly, Tribonacci numbers grow exponentially (roughly 1.84ⁿ), so they have O(n) digits and additions on them are not O(1) in general. At n ≤ 37 every value fits in a machine word, so O(n) is honest. **For huge n you'd say O(n²) bit operations** — a detail worth knowing but not worth leading with.

**Matrix exponentiation gives O(log n)** by squaring a 3×3 companion matrix. At n = 37 that's ~6 matrix multiplies versus 35 additions — **slower in practice** due to the constant factor. It only pays off around n > 10⁶, and matters when the recurrence must be evaluated modulo something for astronomically large n.
→ [matrix-exponentiation](../algorithms/matrix-exponentiation.md)

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — three integers, regardless of `n`.

| Component | Size |
|---|---|
| `t0`, `t1`, `t2` | three integers → **O(1)** |
| Array / memo | **none** → O(1) |
| Recursion | **none** → O(1) |

**This is the payoff of the rolling window.** The comparison across approaches:

| Approach | Space |
|---|---|
| Bottom-up `dp` array | O(n) — 38 values, 35 never re-read |
| `@cache` recursion | O(n) memo **+ O(n) stack frames** |
| **Rolling variables** | **O(1)** ✅ |

**The array version keeps every value it computes, but the recurrence only ever looks back three places** — so at any moment, all but three entries are dead. Dropping them is free.

**The general rule worth carrying forward:** a DP whose transition depends on a **fixed window** of previous states can always be reduced to O(1) space by rotating that many variables. Same for [Climbing Stairs](70-climbing-stairs.md) (2), [House Robber](198-house-robber.md) (2), and [Min Cost Climbing Stairs](746-min-cost-climbing-stairs.md) (2).

⚠️ **The trade-off:** you lose the ability to answer "what was `T₁₀`?" afterwards. If a caller needed the whole sequence, the array would be the right choice — **O(1) space is only free because a single value is wanted.**

**No recursion means no stack-depth question** — though at n ≤ 37 even the recursive version would be safe.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "It's Fibonacci with a three-term window. The recurrence is given, so the work is in the implementation, not the modelling. Naive recursion branches three ways and is about 3ⁿ — roughly 10¹⁷ calls at n = 37 — because it recomputes the same values endlessly. Since each term only depends on the previous three, I don't need an array at all: I keep three rolling variables and slide them forward, which is O(n) time and O(1) space. I use simultaneous assignment so the sum is computed from the old values before any of them are overwritten. The base cases need care — there are three of them, and n = 0 returns 0 while n = 1 and n = 2 both return 1, so the zero case has to be checked separately. If n were astronomically large I'd mention matrix exponentiation for O(log n), though at n ≤ 37 that's slower in practice."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why not recursion?" | O(3ⁿ) — ~10¹⁷ calls at n=37, recomputing the same values. Memoisation fixes the time but still costs O(n) space and n stack frames. |
| "Why three variables and not an array?" | The recurrence looks back exactly three places, so older values are dead. O(1) instead of O(n). |
| "Why does the one-line assignment work?" | Python evaluates the whole right-hand side first, so the sum uses the old values. Sequential assignments without a temporary would corrupt the window. |
| "Why is `n = 0` handled separately?" | `T₀ = 0` but `T₁ = T₂ = 1`. A single `if n <= 2: return 1` returns 1 for n=0. |
| "Why does the constraint stop at 37?" | `T₃₇` is the largest term fitting in a signed 32-bit int. Irrelevant in Python; relevant in C++/Java. |
| "What if n were 10¹⁸?" | Matrix exponentiation — raise the 3×3 companion matrix to the nth power by squaring. O(log n), usually modulo something. |
| "What if the caller wanted the whole sequence?" | Keep the array. O(1) space is only worthwhile when a single value is wanted. |
| "Generalise to k terms?" | Keep a deque of the last k values; each step appends their sum and pops the oldest. O(n·k) time, O(k) space. |
| "Closed form?" | Like Binet's formula for Fibonacci, it exists via the roots of `x³ = x² + x + 1` — but it's irrational and numerically unstable. Don't. |

**Traps:**

- **Returning 1 for `n = 0`.** Collapsing the base cases into one check. **The defining bug here.**
- **Only two base cases** — `T₃` then has nothing to build on.
- **`range(3, n)` instead of `range(3, n + 1)`** — returns `Tₙ₋₁`. Check against `n = 3` → 2.
- **Shifting in the wrong order** in the explicit-temporary version — compute the sum *before* overwriting anything.
- **Returning `t0` or `t1`** — `t2` is the newest term.
- **Naive recursion** — correct, and non-terminating in practice at n = 37.
- **Seeding `t0, t1, t2 = 1, 1, 1`** — copying Fibonacci's seeds; `T₀` is 0.

**This same move shows up in:** [Climbing Stairs](70-climbing-stairs.md) (the two-term version — the same rolling-variable trick) · [Min Cost Climbing Stairs](746-min-cost-climbing-stairs.md) and [House Robber](198-house-robber.md) (fixed-window DP reduced to O(1) space) · [dynamic-programming](../algorithms/dynamic-programming.md) · [matrix-exponentiation](../algorithms/matrix-exponentiation.md).

</details>

---
