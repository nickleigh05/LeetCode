# 343. Integer Break

**Medium** · [LeetCode](https://leetcode.com/problems/integer-break/) · [Solution file (no hints)](../../problems/0001-0499/343.py)

[📖 14. 1-D DP lesson](../learning/14-dp-1d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 13. 1-D Dynamic Programming problems](../rmap-practice/13-dp-1d.md)

---

Break `n` into a sum of **at least two** positive integers and **maximise their product**.

```
n = 2   →  1       2 = 1 + 1,  product 1
n = 10  →  36      10 = 3 + 3 + 4,  product 36
```

**Constraints:** `2 <= n <= 58`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "break it into… **k >= 2**" | ⚠️ **At least two parts** — you may not keep `n` whole |
| "maximise the **product**" | Multiplicative objective, unlike the additive DPs around it |
| "**positive** integers" | Parts are ≥ 1; a part of 0 would zero the product |
| `n <= 58` | ⚠️ Tiny. O(n²) = 3,364 — the bound is generous, hinting the difficulty is conceptual |
| `n >= 2` | So a valid break always exists |

**The `k >= 2` requirement is the whole subtlety**, and it's why `n = 2` gives 1 rather than 2. You *must* split, even when splitting hurts:

```
n = 2:   only option is 1 + 1  →  1        (2 alone is not allowed)
n = 3:   1+1+1 = 1,  1+2 = 2   →  2        (3 alone is not allowed)
n = 4:   2+2 = 4,  1+3 = 3     →  4        (here splitting is free — 2+2 = 4 = 4)
```

**From n = 4 onwards splitting never hurts**, which is why the awkwardness is confined to n = 2 and 3.

**The recurrence, and the trap inside it.** Split off a first part `j`, leaving `i - j`. But now there's a choice about the remainder:

```
option A:  leave i - j whole      →  j × (i - j)
option B:  break i - j further    →  j × dp[i - j]
```

⚠️ **Both must be considered.** `dp[i-j]` is the best product from breaking the remainder into **two or more** parts — so it never represents leaving it whole. If you only wrote `j * dp[i-j]`, you'd force every remainder to be split, and lose answers like `10 = 3 + 7` where 7 stays whole… except 7 shouldn't stay whole. The clearer failing case:

```
n = 4:   j = 2, remainder 2
  option A:  2 × 2       = 4  ✅
  option B:  2 × dp[2]   = 2 × 1 = 2

dp[2] = 1 because 2 must itself be split into 1+1.
Only option A finds the correct answer.
```

So the recurrence is:

```
dp[i] = max over j in 1..i-1 of  max( j × (i - j),  j × dp[i - j] )
```

**The mathematical shortcut worth knowing.** The optimal break uses **as many 3s as possible**:

```
n = 10  →  3 + 3 + 4     = 36
n = 11  →  3 + 3 + 3 + 2 = 54
n = 12  →  3 + 3 + 3 + 3 = 81
```

Why 3s? Because for a fixed sum, splitting into equal parts of size `e ≈ 2.718` maximises the product, and 3 is the nearest integer that beats 2. Concretely: `6 = 3+3 → 9` but `6 = 2+2+2 → 8`. **Never use a part of 1** (it wastes sum), and **never more than two 2s** (since `2+2+2 = 6` loses to `3+3 = 9`).

🤔 **Before you open the next section:** if `dp[i]` means "best product from breaking `i` into two or more parts", what is `dp[3]`? And is that the number you want to multiply by when 3 appears as a *part* of a larger break?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Enumerate all partitions | Recursive brute force | exponential | ❌ Unnecessary |
| **Bottom-up DP** | `dp[i]` over `i = 2..n` | **O(n²)** | ✅ |
| Memoised recursion | Top-down | O(n²) | ✅ Equivalent |
| **Math: use as many 3s as possible** | Closed form | **O(1)** | ✅ Fastest, needs proof |

**The decision: bottom-up DP.** Know the 3s formula as the O(1) follow-up.

**The DP, with both options at every split:**

```python
dp = [0] * (n + 1)
dp[1] = 1
for i in range(2, n + 1):
    for j in range(1, i):
        dp[i] = max(dp[i], j * (i - j), j * dp[i - j])
```

⚠️ **`dp[1] = 1` is a convenience, not a truth.** By the problem's own rule, 1 cannot be broken into two positive parts at all — `dp[1]` is undefined. Setting it to 1 makes it the multiplicative identity, so `j * dp[1]` degrades gracefully to `j`. It works because option A (`j * (i - j)`) already covers the "leave it whole" case correctly.

**The three-argument `max` is the readable way to write it:**

```python
max(dp[i],           # best found so far
    j * (i - j),     # leave the remainder whole
    j * dp[i - j])   # break the remainder further
```

**The mathematical solution**, and why it's true:

```python
if n == 2: return 1
if n == 3: return 2
q, r = divmod(n, 3)
if r == 0: return 3 ** q            # n = 3+3+…+3
if r == 1: return 3 ** (q-1) * 4    # ⚠️ 4 = 2+2, NOT 3+1
return 3 ** q * 2                   # r == 2
```

⚠️ **The `r == 1` case is the one to get right.** A leftover 1 is useless — `3 × 1 = 3` is worse than `2 × 2 = 4`. So you trade one 3 and the 1 for two 2s:

```
n = 10:  q=3, r=1
  naive:  3 × 3 × 3 × 1 = 27   ✗
  correct: 3 × 3 × 4     = 36  ✅   (took a 3 back, made 3+1 into 4)
```

I verified DP, the formula, and a brute-force partition enumerator agree for every `n` from 2 to 24, and DP against the formula through n = 58.

| | DP | 3s formula |
|---|---|---|
| Time | O(n²) = 3,364 | **O(1)** |
| Space | O(n) | **O(1)** |
| Requires | nothing | ⚠️ a proof you can state |
| Generalises | ✅ variants, constraints on parts | ❌ brittle |

**Write the DP; mention the formula.** Leading with the formula looks like recall rather than reasoning — but being *able* to justify it (parts of 3 beat parts of 2, never use 1) is a strong finish.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
dp = [0] * (n + 1)
dp[1] = 1
```

**`dp[i]` = the largest product obtainable by breaking `i` into two or more parts.**

⚠️ `dp[1] = 1` is a deliberate convenience — 1 can't actually be broken. Treating it as the multiplicative identity makes `j * dp[1]` collapse to `j`, and the "leave it whole" option handles the real case anyway.

`dp[0]` stays 0 and is never read, since `j` never reaches `i`.
→ [list-basics](../syntax/list-basics.md)

```python
for i in range(2, n + 1):
```

**Build up from 2**, since `dp[0]` and `dp[1]` are seeded and every larger value depends only on smaller ones.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md)

```python
    for j in range(1, i):
```

**Try every first part `j` from 1 to `i-1`.**

⚠️ **`range(1, i)` excludes `i` itself** — that's the `k >= 2` rule in code. Allowing `j = i` would mean "leave `n` whole", which the problem forbids and which would make `dp[n] = n` for every n.
→ [range-function](../syntax/range-function.md)

```python
        dp[i] = max(dp[i], j * (i - j), j * dp[i - j])
```

**The two ways to handle the remainder, plus the running best.**

| Term | Meaning |
|---|---|
| `dp[i]` | best found so far for this `i` |
| `j * (i - j)` | split into exactly two parts — **leave the remainder whole** |
| `j * dp[i - j]` | split off `j`, then **break the remainder further** |

⚠️ **Omitting `j * (i - j)` breaks it.** Since `dp[i-j]` always assumes the remainder is itself split, you'd never consider two-part breaks. `n = 4` would give 2 instead of 4.
→ [min-max-key](../syntax/min-max-key.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
return dp[n]
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def integerBreak(self, n: int) -> int:

        dp = [0] * (n + 1)
        dp[1] = 1

        for i in range(2, n + 1):
            for j in range(1, i):
                dp[i] = max(dp[i], j * (i - j), j * dp[i - j])

        return dp[n]
```

</details>

<details>
<summary>The O(1) mathematical version, for comparison</summary>

```python
class Solution:
    def integerBreak(self, n: int) -> int:

        if n == 2:
            return 1
        if n == 3:
            return 2

        q, r = divmod(n, 3)
        if r == 0:
            return 3 ** q
        if r == 1:
            return 3 ** (q - 1) * 4      # trade a 3 and the 1 for 2+2
        return 3 ** q * 2
```

→ [integer-division-modulo](../syntax/integer-division-modulo.md) · [multiple-return-values](../syntax/multiple-return-values.md)

</details>

**Trace it** — building `dp` up to `n = 10`. Verified output:

| `i` | best split found | `dp[i]` |
|---|---|---|
| 2 | 1 + 1 | **1** |
| 3 | 1 + 2 | **2** |
| 4 | 2 + 2 | **4** |
| 5 | 2 + 3 | **6** |
| 6 | 3 + 3 | **9** |
| 7 | 3 + 4 | **12** |
| 8 | 3 + 3 + 2 | **18** |
| 9 | 3 + 3 + 3 | **27** |
| 10 | 3 + 3 + 4 | **36** ✅ |

**Look at `dp[4] = 4`** — it comes from `j = 2` via `j * (i - j) = 2 × 2 = 4`. The other option gives `2 × dp[2] = 2 × 1 = 2`. **This row alone proves both terms are needed**; drop the two-part option and `dp[4]` becomes 2, corrupting everything above it.

**`dp[7] = 12`** is where the "break further" option starts earning its keep. At `j = 3`, remainder 4: `3 × dp[4] = 3 × 4 = 12`, versus leaving it whole at `3 × 4 = 12` — a tie here, because `dp[4] = 4 = 4`. By `dp[8]` they diverge: `j = 3`, remainder 5 gives `3 × dp[5] = 3 × 6 = 18` beating `3 × 5 = 15`.

**The 3s pattern is visible in the table** — from `dp[6]` onward every optimum is 3s plus a small remainder:

```
6  = 3+3            9  = 3³ ... no, 3+3 → 9
9  = 3+3+3          27
10 = 3+3+4          36     ← r = 1, so a 3 and the 1 became a 4
11 = 3+3+3+2        54     ← r = 2, one 2 left over
12 = 3+3+3+3        81
```

**Checking the formula against `n = 10`:** `q, r = 3, 1`, so `3^(3-1) × 4 = 9 × 4 = 36` ✅ — and the naive `3³ × 1 = 27` would be wrong, which is exactly the case the `r == 1` branch exists for.

**At the constraint limit `n = 58`:** `q, r = 19, 1`, so `3^18 × 4 = 1,549,681,956`. The DP produces the same value.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n²)</summary>

**O(n²)** for the DP.

| Component | Cost |
|---|---|
| Outer loop | **n** iterations |
| Inner loop at `i` | **i − 1** splits → O(n) |
| **Total** | **O(n²)** |

At n = 58 that's about `58²/2 ≈ 1,700` operations. Trivial — **the constraint is small because the problem is conceptual, not computational.**

**The mathematical version is O(1)** — a `divmod` and one exponentiation. (Strictly, `3 ** q` on a bignum isn't O(1), but at n ≤ 58 the result fits in a machine word.)

| Approach | Operations at n = 58 |
|---|---|
| DP | ~1,700 |
| **Formula** | **~3** |

**Both are instant**, so this is not a performance decision — it's about which you can justify. The DP needs no proof; the formula needs you to explain why 3s win.

**Why not enumerate partitions:** 58 has **715,220** partitions — enumerable, but already 400× the DP's work, and the count grows roughly like `e^(c√n)`, so it explodes well before any interesting n. The DP's O(n²) works because overlapping subproblems collapse that space entirely.

**The symmetry optimisation:** `j` and `i - j` give the same two-part product, so the inner loop could stop at `i // 2`. Halves the work, same O(n²), and not worth the extra thought at this size.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** for the DP array.

| Component | Size |
|---|---|
| `dp` | n + 1 integers → **O(n)** |
| **Total** | **O(n)** |

At n = 58 that's 59 entries.

**⚠️ This can't reduce to O(1)** like [Tribonacci](1137-n-th-tribonacci-number.md): computing `dp[i]` reads `dp[i-1]` through `dp[1]` — **every earlier entry**. The look-back is unbounded, so the whole table must be retained:

| | Look-back | Space |
|---|---|---|
| [Tribonacci](1137-n-th-tribonacci-number.md) | fixed 3 | **O(1)** |
| **Integer Break** | all previous | **O(n)** |

**The mathematical version is O(1)** — no table at all. **That's its real advantage over the DP**, more than the speed.

**A note on integer size:** `3^19` ≈ 1.16 × 10⁹, so the answer at n = 58 fits comfortably in 32 bits — which is presumably why the constraint stops at 58. **In Python the values are arbitrary precision anyway**, but in C++ you'd want to check: `n = 60` gives `3^20` ≈ 3.5 × 10⁹, which overflows a signed 32-bit int.

**No recursion** — iterative, so no stack concern.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "`dp[i]` is the largest product from breaking i into at least two parts. For each i I try every first part j, and there are two cases for what's left: either leave the remainder whole, giving `j × (i - j)`, or break it further, giving `j × dp[i-j]`. Both are needed, because `dp[i-j]` always assumes the remainder is split — without the first term, n = 4 would give 2 instead of 4. The `k >= 2` rule shows up as the inner loop stopping at `i-1`, never letting j equal i. O(n²) time, O(n) space. There's also a closed form: the optimum is as many 3s as possible, because for a fixed sum, equal parts near e maximise the product and 3 is the best integer — 3+3 gives 9 while 2+2+2 gives 8. The one subtlety is a remainder of 1, where you take back a 3 and use 2+2 instead, since 3×1 = 3 loses to 2×2 = 4. That's O(1), but I'd write the DP first since it needs no proof."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why both `j*(i-j)` and `j*dp[i-j]`?" | **The question.** `dp[i-j]` assumes the remainder is itself split, so the two-part case needs its own term. Without it `dp[4]` = 2 instead of 4. |
| "Why is `dp[2] = 1` and not 2?" | `k >= 2` forces a split, and 2 = 1+1 gives product 1. |
| "Why does `dp[1] = 1` work?" | It's a convenience — 1 can't be split. As the multiplicative identity it makes `j * dp[1] = j`, and the whole-remainder term covers the real case. |
| "What's the O(1) solution?" | Use as many 3s as possible. Remainder 0 → `3^q`; remainder 1 → `3^(q-1) × 4`; remainder 2 → `3^q × 2`. |
| "**Why 3s?**" | For a fixed sum, equal parts of size ≈ e ≈ 2.718 maximise the product; 3 is the nearest integer that beats 2. Concretely `3+3 = 9 > 2+2+2 = 8`. |
| "Why is remainder 1 special?" | A part of 1 wastes sum — `3 × 1 = 3` loses to `2 × 2 = 4`. So trade one 3 and the 1 for two 2s. |
| "Why never use a part of 1?" | Multiplying by 1 leaves the product unchanged while consuming sum that could have grown another part. |
| "Reduce the space?" | Not for the DP — the look-back is unbounded. The formula is O(1). |
| "What if parts had to be **distinct**?" | Different problem: greedily use 2, 3, 4, … and fold the leftover into the largest part. |
| "What if `k` were fixed?" | Split as evenly as possible — parts of `n//k` and `n//k + 1`. |

**Traps:**

- **Only writing `j * dp[i-j]`.** Misses two-part breaks; `dp[4]` = 2 instead of 4. **The defining bug.**
- **Allowing `j = i`** — that's "leave n whole", forbidden by `k >= 2`, and it makes `dp[n] = n`.
- **Returning `n` for small n** — `n = 2` must give 1, not 2.
- **In the formula, using `3^q × 1` when `r == 1`** — gives 27 instead of 36 for n = 10.
- **Forgetting the `n == 2` and `n == 3` guards** in the formula version — `divmod(3,3)` gives q=1, r=0 → `3^1 = 3`, but the answer is 2.
- **Setting `dp[1] = 0`** — then `j * dp[1] = 0`, which is harmless only because the whole-remainder term saves you. Fragile.
- **Trying to enumerate partitions** — 58 has over 700 billion of them.

**This same move shows up in:** [Perfect Squares](279-perfect-squares.md) (the same "try every last piece" 1-D DP, minimising a count) · [Coin Change](322-coin-change.md) (unbounded 1-D DP over a target) · [Word Break](139-word-break.md) (splitting with an unbounded look-back) · [Palindrome Partitioning II](132-palindrome-partitioning-ii.md) (optimal splitting of a 1-D object) · [dynamic-programming](../algorithms/dynamic-programming.md).

</details>

---
