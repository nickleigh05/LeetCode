# 69. Sqrt(x)

**Easy** · [LeetCode](https://leetcode.com/problems/sqrtx/) · [Solution file (no hints)](../../problems/0001-0499/69.py)

[📖 05. Binary Search lesson](../learning/05-binary-search.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 05. Binary Search problems](../rmap-practice/05-binary-search.md)

---

Given a non-negative integer `x`, return the square root of `x` **rounded down** to the nearest integer. You must **not** use any built-in exponent function or operator.

```
x = 4   →  2
x = 8   →  2    (2.828… truncated to 2)
x = 0   →  0
```

**Constraints:** `0 <= x <= 2³¹ - 1`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**rounded down**" | ⚠️ You want the largest integer `k` with `k² <= x` — a **boundary**, not an exact match |
| "no built-in exponent function" | No `math.sqrt`, no `x ** 0.5`, no `pow`. Multiplication is fine |
| `0 <= x <= 2³¹ - 1` | `x = 0` must work. And `mid * mid` can reach ~4·10¹⁸ — **overflow territory** outside Python |
| non-negative | No imaginary-number edge cases |

**Why this is a search problem at all.** There's no array — but there's an ordered domain (the integers `0…x`) and a **monotonic predicate**:

```
k:        0    1    2    3    4    5   ...
k² <= 8: true true true false false false
                      ↑
              the boundary — answer is 2
```

`k²` increases monotonically with `k`, so `k² <= x` is true for a prefix and false thereafter. That's exactly the precondition binary search needs — the same structure as [First Bad Version](278-first-bad-version.md), with `k*k <= x` playing the role of the oracle.

This is the first genuine **"binary search on the answer"** problem in the unit: you're not searching *data*, you're searching a **range of candidate answers** and testing each for feasibility. [Koko Eating Bananas](875-koko-eating-bananas.md), [Capacity To Ship Packages](1011-capacity-to-ship-packages-within-d-days.md), and [Split Array Largest Sum](410-split-array-largest-sum.md) are all the same shape with harder predicates.

**Why `right = x` is a safe upper bound.** For `x >= 1`, `√x <= x`. (It's loose — `x/2 + 1` would be tighter — but correctness first; the extra iterations cost nothing at O(log x).)

🤔 **Before you open the next section:** when `mid * mid < x`, `mid` is too small to be the answer — but could it still be the *best answer found so far*?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Linear scan | Try `k = 0, 1, 2, …` until `k² > x` | O(√x) ≈ 46341 | ⚠️ Passes, but ignores the structure |
| `math.sqrt` / `x ** 0.5` | Built-in | O(1) | ❌ Explicitly forbidden — and float precision fails near 2³¹ |
| **Binary search** | Halve the candidate range | **O(log x)** ≈ 31 | ✅ |
| **Newton's method** | Iterate `g = (g + x/g) / 2` | **O(log log x)** | ✅✅ Faster; converges quadratically |

**The decision: binary search on the answer.** The solution file also carries Newton's method as the sophisticated alternative.

**The binary search structure.** Because you want the *largest* `k` with `k² <= x`, and the loop uses the value-search convention (`left <= right`, `mid ± 1`), you need to **remember the best valid candidate** as you go:

```python
if mid * mid == x:   return mid       # exact hit
elif mid * mid < x:  result = mid; left = mid + 1    # valid, but try bigger
else:                right = mid - 1                 # too big, discard
```

The `result = mid` line is what makes this a floor-finding search rather than an exact search. Every time `mid` passes the test, it's a candidate answer — record it, then probe higher for something better. When the range empties, `result` holds the largest passing value.

**The alternative convention** avoids the extra variable by using boundary search (`left < right`, `right = mid`), but then you must be careful about which side keeps `mid`. Both are correct; the "track the best" version is easier to reason about under pressure and is what the solution file uses.

**Newton's method**, for the follow-up. To solve `f(g) = g² − x = 0`, iterate:

```
g ← (g + x/g) / 2
```

Each step roughly **doubles the number of correct digits** (quadratic convergence), so it converges in O(log log x) iterations — around 5–6 for 32-bit inputs versus 31 for binary search. Starting from `g = x // 2` and iterating while `g * g > x` lands on the floor of the square root directly.

It's genuinely faster and worth knowing, but binary search is the expected answer and is much easier to prove correct on a whiteboard. Lead with binary search, mention Newton.

**The overflow caveat.** `mid * mid` with `x` near 2³¹ means `mid` can be ~46341 and `mid²` ~2.1·10⁹ — fine for `int32`? Only just. But if you set `right = x` and compute `mid * mid` early on, `mid` can be ~10⁹ and `mid²` ~10¹⁸, which **overflows `int32` and even flirts with `int64`**. Python is immune, but in C++/Java you'd compare `mid > x / mid` instead of `mid * mid > x`.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
left = 0
right = x
tmp = 0
```

The candidate range `[0, x]`. Starting at 0 handles `x = 0` correctly.

(`tmp` is unused in the final logic — `result` is what carries the answer. Harmless, but it could be removed.)
→ [variables-assignment](../syntax/variables-assignment.md)

```python
while left <= right:
    mid = (left + right) // 2
```

Standard value-search convention with inclusive bounds.
→ [while-loop](../syntax/while-loop.md) · [integer-division-modulo](../syntax/integer-division-modulo.md)

```python
    if mid * mid == x:
        return mid
```

A perfect square — the exact answer, so return immediately.
→ [comparison-operators](../syntax/comparison-operators.md) · [if-return](../syntax/if-return.md)

```python
    elif mid * mid < x:
        result = mid
        left = mid + 1
```

**The key two lines.** `mid² < x` means `mid` is a **valid** answer (its square doesn't exceed `x`) but possibly not the largest one.

So: **record it** as the best so far, then search higher for something better. Without `result = mid`, you'd lose track of the best passing candidate and have nothing to return when the loop ends.

```python
    else:
        right = mid - 1
```

`mid² > x` — too big. `mid` is not a valid answer, so discard it and everything above.
→ [elif-else](../syntax/elif-else.md)

```python
return result
```

The loop exhausted the range; `result` holds the largest `mid` whose square was ≤ `x` — the floor of the square root.

⚠️ Note `result` is only assigned inside the `elif`. For `x = 0`: `left = right = 0`, `mid = 0`, and `0 * 0 == 0` triggers the **first** branch, returning 0. For `x = 1`: `mid = 0` initially gives `0 < 1` → `result = 0`, then `mid = 1` gives `1 == 1` → returns 1. So every input either hits the exact-match branch or assigns `result` first — but initializing `result = 0` alongside the other variables would make that safety explicit rather than incidental.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def mySqrt(self, x: int) -> int:

        left = 0
        right = x
        tmp = 0

        while left <= right:
            mid = (left + right) // 2

            if mid * mid == x:
                return mid
            elif mid * mid < x:
                result = mid
                left = mid + 1
            else:
                right = mid - 1

        return result
```

</details>

<details>
<summary>Newton's method (also in the solution file)</summary>

```python
### Newtons Method ###
class Solution:
    def mySqrt(self, x: int) -> int:
        if x < 2:
            return x

        guess = x // 2
        while guess * guess > x:
            # The Newton formula: (guess + x/guess) / 2
            guess = (guess + x // guess) // 2

        return guess
```

Converges quadratically — each iteration roughly doubles the correct digits — so it finishes in ~5 steps where binary search takes 31. The `x < 2` guard handles 0 and 1, where `x // 2` would be 0 and cause a division by zero.

</details>

**Trace it** — `x = 8`:

| `left` | `right` | `mid` | `mid²` | vs 8 | Action | `result` |
|---|---|---|---|---|---|---|
| 0 | 8 | 4 | 16 | `> 8` | `right = 3` | — |
| 0 | 3 | 1 | 1 | `< 8` | `result = 1`, `left = 2` | **1** |
| 2 | 3 | 2 | 4 | `< 8` | `result = 2`, `left = 3` | **2** |
| 3 | 3 | 3 | 9 | `> 8` | `right = 2` | 2 |
| 3 | 2 | — | — | — | `left > right` → exit | 2 |

`return result` = **2** ✅ (since `2² = 4 <= 8 < 9 = 3²`)

Rows 2 and 3 show `result` being updated each time a larger valid candidate is found — that ratcheting is what produces the floor.

**And the perfect-square case** — `x = 4`:

| `left` | `right` | `mid` | `mid²` | Action |
|---|---|---|---|---|
| 0 | 4 | 2 | 4 | `== 4` → **return 2** ✅ |

One iteration, via the exact-match branch.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(log x)</summary>

**O(log x)** for binary search.

The range `[0, x]` halves each iteration, so it takes `log₂ x` steps. At `x = 2³¹ - 1` that's **31 iterations**, each doing one multiplication and a comparison.

| | Iterations at x = 2³¹ |
|---|---|
| Linear scan | ~46,341 (that's √x) |
| **Binary search** | **31** |
| **Newton's method** | **~5** |

**Newton's method is O(log log x)** because it converges *quadratically*: the number of correct digits roughly doubles each step. Going from 1 correct digit to 10 takes about 4 iterations, not 10.

That's a genuinely different growth class, and it's why Newton (or a hardware instruction derived from it) is what real math libraries use. But binary search is the expected interview answer — it's easier to justify and impossible to get subtly wrong in the convergence argument.

**Is O(log x) optimal for binary search here?** You can tighten the constant by setting `right = x // 2 + 1` (since `√x <= x/2 + 1` for `x >= 2`), saving a couple of iterations. Not asymptotically meaningful, but a fair micro-optimization to mention.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — a handful of integers for both approaches.

Nothing is allocated, and nothing scales with `x`. This is a pure arithmetic search over an implicit domain.

**The overflow consideration is the real "space" issue here**, and it's worth raising unprompted:

With `right = x` and `x` near 2³¹, the first `mid` is ~10⁹ and `mid * mid` is ~10¹⁸. That:

- **overflows `int32`** immediately,
- fits in `int64` (max ~9.2·10¹⁸) but with little headroom.

Python's arbitrary-precision integers make this a non-issue, which is exactly why it's easy to forget. The portable fix is to avoid the multiplication entirely:

```python
if mid > x // mid:   # instead of mid * mid > x
```

Comparing via division keeps both operands within range. Mentioning this shows you're thinking beyond the Python sandbox.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "I want the largest integer `k` with `k² <= x`. Since `k²` grows monotonically, the predicate `k² <= x` is true for a prefix and false after — so I can binary search the answer range `[0, x]`. When `mid² < x`, `mid` is valid but maybe not the largest, so I record it and search higher; when `mid² > x` I discard it and everything above; an exact match returns immediately. Tracking the best valid candidate is what makes this a floor search rather than an exact search. O(log x), about 31 iterations at the maximum. Newton's method converges quadratically and would take about five iterations instead, but binary search is easier to prove correct. One caveat outside Python: `mid * mid` can overflow, so I'd compare `mid > x // mid` instead."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Can you do better than O(log x)?" | Newton's method — O(log log x) via quadratic convergence. Start at `x // 2`, iterate `g = (g + x//g) // 2`. |
| "What about **overflow**?" | `mid * mid` reaches ~10¹⁸ at `x = 2³¹`. Use `mid > x // mid`, or 64-bit types. |
| "Compute it to `k` decimal places?" | Binary search on floats with an epsilon tolerance, or Newton with a float guess. Watch the termination condition — use `abs(g*g - x) < eps`, not equality. |
| "Cube root instead?" | Same structure, predicate becomes `mid³ <= x`. Overflow risk is worse. |
| "Why is `right = x` valid?" | For `x >= 1`, `√x <= x`. Loose but correct; `x // 2 + 1` is tighter for `x >= 2`. |
| "Why track `result` instead of returning `right`?" | You *can* return `right` after this loop — it converges to the floor too. Tracking the best candidate is more obviously correct and survives convention changes. |
| "Is `x ** 0.5` really wrong?" | It's forbidden here, and it's also genuinely unsafe near 2³¹ — float64 has 53 bits of mantissa, so rounding can put you one off. `int(math.sqrt(x))` needs a correction check. |

**Traps:**

- **Forgetting `result = mid`.** Without it there's nothing to return when the range empties on a non-perfect square.
- **Returning `left`.** After this loop `left` is one *past* the answer. `right` and `result` both hold the floor.
- **Not handling `x = 0`.** With `left = right = 0` the exact-match branch catches it — but Newton's method needs an explicit `x < 2` guard to avoid dividing by zero.
- **`mid * mid` overflow** in fixed-width languages. Compare with division instead.
- **Using `math.sqrt`.** Forbidden, and imprecise at the top of the range.
- **`right = x // 2` without the `+ 1`.** Breaks for `x = 1`, where the answer is 1 but the range becomes `[0, 0]`.

**This same move shows up in:** [Valid Perfect Square](367-valid-perfect-square.md) (the same search, returning a boolean instead of the floor) · [First Bad Version](278-first-bad-version.md) (boundary search over a monotonic predicate) · [Koko Eating Bananas](875-koko-eating-bananas.md) (binary search on the answer with a costlier feasibility test) · [Split Array Largest Sum](410-split-array-largest-sum.md) (the Hard version of answer-space search).

</details>

---
