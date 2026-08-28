# 367. Valid Perfect Square

**Easy** · [LeetCode](https://leetcode.com/problems/valid-perfect-square/) · [Solution file (no hints)](../../problems/0001-0499/367.py)

[📖 05. Binary Search lesson](../learning/05-binary-search.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 05. Binary Search problems](../rmap-practice/05-binary-search.md)

---

Given a positive integer `num`, return `true` if it is a **perfect square** — the square of some integer — or `false` otherwise. You must **not** use any built-in library function such as `sqrt`.

```
num = 16  →  true    (4² = 16)
num = 14  →  false
num = 1   →  true    (1² = 1)
```

**Constraints:** `1 <= num <= 2³¹ - 1`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**perfect square**" | Does an integer `k` exist with `k² = num`? An **exact match**, not a floor |
| "no `sqrt`" | No `math.sqrt`, no `num ** 0.5`. Multiplication and comparison only |
| `1 <= num` | Never zero, so no degenerate case (though `num = 1` is worth checking) |
| `num` up to 2³¹ − 1 | ⚠️ `mid * mid` can reach ~10¹⁸ — **overflow risk** outside Python |
| return a **boolean** | You don't need the root itself, just whether one exists |

This is [Sqrt(x)](69-sqrtx.md)'s simpler sibling. There you wanted the **floor** of the square root and had to track the best valid candidate; here you only need to know whether an **exact** hit exists — so the standard value-search binary search applies with no extra bookkeeping.

The domain and predicate:

```
k:        1    2    3    4    5
k²:       1    4    9   16   25
                        ↑
              searching for k² == 16
```

`k²` is strictly increasing, so the sequence of squares is sorted. Searching a sorted sequence for an exact value is textbook binary search — the only twist is that the "array" is **implicit**: you compute `mid * mid` on demand rather than storing squares.

**Why searching `k` and not the squares.** You binary search over candidate *roots* `[1, num]`, computing each candidate's square to compare. There's no array to index — the ordered domain is the roots themselves.

🤔 **Before you open the next section:** if `mid * mid` is less than `num`, can `mid` still be the root you're looking for?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Linear scan | Try `k = 1, 2, 3, …` until `k² >= num` | O(√num) ≈ 46341 | ⚠️ Passes, ignores the structure |
| `math.sqrt` + check | `int(sqrt(num)) ** 2 == num` | O(1) | ❌ Forbidden — and float-imprecise near 2³¹ |
| **Binary search** | Halve the root range | **O(log num)** ≈ 31 | ✅ |
| Newton's method | Iterate to the root, then verify | O(log log num) | ✅ Faster; more to justify |
| Sum of odd numbers | `1+3+5+… = k²`; subtract until ≤ 0 | O(√num) | ⚠️ Cute identity, same as linear |

**The decision: binary search over candidate roots.**

Value-search convention throughout, because an exact match is possible:

- `left <= right` (inclusive bounds)
- `left = mid + 1` / `right = mid - 1` (exclude the tested value)
- `return True` on an exact hit; `return False` when the range empties

**Why this is simpler than [Sqrt(x)](69-sqrtx.md).** There, a non-perfect input still needed an answer — the floor — so you had to remember the best valid candidate as you went. Here, a non-perfect input just means "no match found," which the loop's natural exhaustion already expresses. **No `result` variable needed.**

That contrast is worth internalizing:

| | Question | Needs a "best so far"? |
|---|---|---|
| [Sqrt(x)](69-sqrtx.md) | largest `k` with `k² <= x` | **Yes** — track the floor |
| **Valid Perfect Square** | does any `k` have `k² == num`? | **No** — exact match or bust |

**The sum-of-odd-numbers trick**, worth mentioning as a curiosity: `1 + 3 + 5 + … + (2k−1) = k²`. So repeatedly subtract successive odd numbers from `num`; if you land exactly on 0 it's a perfect square. Elegant and division-free, but O(√num) — slower than binary search, and only interesting as a demonstration that you know the identity.

**The overflow point.** `right` starts at `num`, so early `mid` values are ~10⁹ and `mid * mid` ~10¹⁸. That overflows `int32` badly and uses most of `int64`. Python is immune, but the portable form compares without multiplying:

```python
if mid > num // mid:   # instead of mid * mid > num
```

Note the solution file uses `mid = left + (right - left) // 2` — the **overflow-safe midpoint** — which is good practice even in Python, and a signal the author was thinking about it.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
left = 1
right = num
```

Candidate roots. Starting at **1** (not 0) is safe because `num >= 1`, so the root is at least 1.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
while left <= right:
```

Inclusive bounds ⇒ `<=`, so the final one-element range is still checked. Missing that would fail `num = 1`.
→ [while-loop](../syntax/while-loop.md)

```python
    mid = left + (right - left) // 2
```

**The overflow-safe midpoint.** Mathematically identical to `(left + right) // 2`, but `right - left` can't overflow even when both are near the maximum.

Unnecessary in Python, correct everywhere — a good habit to carry into languages where it matters.
→ [integer-division-modulo](../syntax/integer-division-modulo.md)

```python
    square = mid * mid
```

Compute once and reuse across the three comparisons, rather than recomputing the multiplication in each branch.
→ [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
    if square == num:
        return True
```

Exact match — `num` is a perfect square. Return immediately; nothing more to check.
→ [comparison-operators](../syntax/comparison-operators.md) · [if-return](../syntax/if-return.md)

```python
    elif square < num:
        left = mid + 1
```

`mid` is too small. Since squares increase with `mid`, the root (if any) is strictly larger.

Note there's **no `result = mid`** here — unlike [Sqrt(x)](69-sqrtx.md), a near-miss is worthless. You either hit exactly or you don't.

```python
    else:
        right = mid - 1
```

`mid` is too large; look lower.
→ [elif-else](../syntax/elif-else.md)

```python
return False
```

The range emptied without an exact match, so no integer squares to `num`.
→ [boolean-basics](../syntax/boolean-basics.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def isPerfectSquare(self, num: int) -> bool:

        left = 1
        right = num

        while left <= right:
            mid = left + (right - left) // 2
            square = mid * mid

            if square == num:
                return True
            elif square < num:
                left = mid + 1
            else:
                right = mid - 1

        return False
```

</details>

**Trace the true case** — `num = 16`:

| `left` | `right` | `mid` | `square` | vs 16 | Action |
|---|---|---|---|---|---|
| 1 | 16 | 8 | 64 | `> 16` | `right = 7` |
| 1 | 7 | 4 | 16 | **equal** | `return True` ✅ |

**Trace the false case** — `num = 14`:

| `left` | `right` | `mid` | `square` | vs 14 | Action |
|---|---|---|---|---|---|
| 1 | 14 | 7 | 49 | `> 14` | `right = 6` |
| 1 | 6 | 3 | 9 | `< 14` | `left = 4` |
| 4 | 6 | 5 | 25 | `> 14` | `right = 4` |
| 4 | 4 | 4 | 16 | `> 14` | `right = 3` |
| 4 | 3 | — | — | — | `left > right` → exit |

`return False` ✅ — 14 sits strictly between `3² = 9` and `4² = 16`.

Row 4 only executes because of the `<=` condition; with `<`, the loop would exit at `left == right == 4` without testing it. Here that happens to give the same answer, but on `num = 16` it would skip the match entirely.

**And the smallest case** — `num = 1`:

| `left` | `right` | `mid` | `square` | Action |
|---|---|---|---|---|
| 1 | 1 | 1 | 1 | `== 1` → **return True** ✅ |

Only reachable because `left <= right` permits a single-element range.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(log num)</summary>

**O(log num).**

Each iteration halves the root range `[1, num]`, so it takes `log₂ num` steps. At `num = 2³¹ - 1` that's **31 iterations**, each doing one multiplication and comparisons.

| | Iterations at num = 2³¹ |
|---|---|
| Linear / odd-sum | ~46,341 |
| **Binary search** | **31** |
| Newton's method | ~5 |

**A tighter starting bound.** Searching `[1, num]` is wasteful — no perfect square root exceeds `num // 2 + 1` for `num >= 2`. Setting `right = num // 2 + 1` saves a couple of iterations. Not asymptotically meaningful, but a legitimate refinement to mention.

**Newton's method** would converge in O(log log num) — about 5 steps — by iterating `g = (g + num//g) // 2` until it stops decreasing, then checking `g * g == num`. Faster, but binary search is the expected answer and easier to argue correct.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — four integers, independent of `num`.

Nothing is allocated. The "sorted array of squares" being searched is entirely **implicit** — each element is computed on demand as `mid * mid` rather than stored. Materializing it would need ~46,000 entries for `num = 2³¹`, and unbounded memory in general.

That's the recurring lesson of this unit:

> **Binary search needs an ordered domain and a comparison — the data need not exist in memory.**

Same as [Guess Number Higher or Lower](374-guess-number-higher-or-lower.md) (domain = numbers, comparison = an API) and [First Bad Version](278-first-bad-version.md) (domain = versions, comparison = a predicate).

**The overflow caveat, again worth raising unprompted:** `mid * mid` reaches ~10¹⁸ at the top of the range. Fine in Python; in C++/Java use 64-bit types or compare via `mid > num // mid` to avoid the multiplication entirely.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Squares increase monotonically, so the candidate roots form a sorted sequence I can binary search — even though I never build an array; I compute `mid * mid` on demand. Standard value search: `left <= right` with `mid ± 1`, returning true on an exact match and false when the range empties. Unlike Sqrt(x), I don't need to track a best-so-far candidate, because a near miss is worthless here — it's an exact match or nothing. I use the overflow-safe midpoint `left + (right - left) // 2`, and I'd note that `mid * mid` reaches about 10¹⁸ at the top of the constraint, so outside Python I'd compare `mid > num // mid` instead. O(log num), about 31 iterations, O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Can you do it faster?" | Newton's method — O(log log num). Iterate `g = (g + num//g) // 2` until stable, then verify `g*g == num`. |
| "Do it without multiplication." | The odd-number identity: `1+3+5+…+(2k−1) = k²`. Subtract successive odds; land exactly on 0 ⇒ perfect square. O(√num). |
| "How does this differ from [Sqrt(x)](69-sqrtx.md)?" | That one needs the **floor**, so it tracks the best valid candidate. This one needs an **exact match**, so the loop's natural exhaustion suffices. |
| "Overflow?" | `mid * mid` ~10¹⁸ at `num = 2³¹`. Use 64-bit, or compare `mid > num // mid`. |
| "Why not `int(math.sqrt(num)) ** 2 == num`?" | Forbidden here — and genuinely risky: float64 has 53 mantissa bits, so near 2³¹ the rounding can land one off. |
| "Perfect **cube**?" | Same structure with `mid ** 3`; overflow risk is considerably worse. |
| "Tighter bounds?" | `right = num // 2 + 1` for `num >= 2`; saves a couple of iterations. |

**Traps:**

- **Using `left < right`.** Skips the final one-element range — fails `num = 1` and any input whose root is found last.
- **Adding a `result` variable.** Unnecessary here; that's [Sqrt(x)](69-sqrtx.md)'s requirement, not this one.
- **`left = 0`.** Harmless but pointless — `num >= 1` guarantees the root is ≥ 1, and `mid = 0` would waste an iteration.
- **`mid * mid` overflow** in fixed-width languages.
- **Recomputing `mid * mid` in each branch.** Store it once; it's the loop's only real work.
- **Using `math.sqrt`.** Forbidden, and imprecise at the range's top.

**This same move shows up in:** [Sqrt(x)](69-sqrtx.md) (the floor-finding sibling that needs a best-so-far) · [Binary Search](704-binary-search.md) (the canonical value-search form) · [Guess Number Higher or Lower](374-guess-number-higher-or-lower.md) (value search over an implicit domain) · [Koko Eating Bananas](875-koko-eating-bananas.md) (searching a range of candidate answers with a feasibility predicate).

</details>

---
