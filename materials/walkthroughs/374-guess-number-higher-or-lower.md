# 374. Guess Number Higher or Lower

**Easy** · [LeetCode](https://leetcode.com/problems/guess-number-higher-or-lower/) · [Solution file (no hints)](../../problems/0001-0499/374.py)

[📖 05. Binary Search lesson](../learning/05-binary-search.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 05. Binary Search problems](../rmap-practice/05-binary-search.md)

---

I pick a number from `1` to `n`. You guess. I tell you whether my number is higher or lower. Use the API `guess(num)` which returns:

- **`-1`** — my number is **lower** than your guess
- **`1`** — my number is **higher** than your guess
- **`0`** — correct

Return the number I picked.

```
n = 10, pick = 6  →  6
n = 1,  pick = 1  →  1
n = 2,  pick = 1  →  1
```

**Constraints:** `1 <= n <= 2³¹ - 1` · `1 <= pick <= n`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "higher or lower" feedback | ⚠️ Each guess eliminates an entire **direction** — the signature of binary search |
| numbers `1` to `n` | An ordered domain, even though no array exists |
| `guess` returns −1 / 1 / 0 | A **three-way** comparison, so a plain value-search binary search applies |
| `n` up to 2³¹ − 1 | ~2·10⁹. Linear guessing is hopeless; `log₂` ≈ **31 guesses** |
| `1 <= pick <= n` | The target always exists — no "not found" case |

This is the number-guessing game everyone plays as a child, and the optimal strategy is the reason binary search feels intuitive once you've seen it: **always guess the middle**, because that's the guess whose worst case is smallest.

**Why the middle is optimal.** Guessing at position `k` splits the remaining range into two parts of size `k-1` and `n-k`. The adversary picks whichever side is larger, so your worst case is `max(k-1, n-k)` — minimized exactly when `k` is the midpoint. Any other guess leaves a bigger worst-case remainder.

**The one thing to get right: the sign convention.** The API's return value is described from *my* number's perspective, not your guess's:

- `guess(mid) == -1` → **my number is lower** → search **left** → `right = mid - 1`
- `guess(mid) == 1` → **my number is higher** → search **right** → `left = mid + 1`

It's easy to invert these, because "returns −1" instinctively reads as "your guess is too low." It means the opposite. Read the spec twice.

🤔 **Before you open the next section:** if the API told you your guess was too high, which half of the remaining range can you discard?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Guesses | Verdict |
|---|---|---|---|
| Linear | Try 1, 2, 3, … | O(n) ≈ 2·10⁹ | ❌ Hopeless |
| Random guessing | Guess uniformly at random | O(n) expected | ❌ Worse than linear in practice |
| **Binary search** | Always guess the midpoint | **O(log n)** ≈ 31 | ✅ Provably optimal |
| Ternary search | Two probes per round, split in thirds | O(log n) but more calls | ❌ Strictly worse — see below |

**The decision: binary search with the standard value-search convention.**

Because the API gives a **three-way** answer (lower / higher / equal), this is a *value* search, not a boundary search — so it uses the `left <= right` and `mid ± 1` convention, exactly like [Search Insert Position](35-search-insert-position.md), and unlike [First Bad Version](278-first-bad-version.md).

The pairing rule again:

| | Convention |
|---|---|
| Three-way compare, exact match possible | `left <= right`, `right = mid - 1`, `left = mid + 1` |
| Two-way predicate, finding a boundary | `left < right`, `right = mid` |

Here you can *confirm* a match with `guess(mid) == 0`, so `mid` is definitively resolved each round and can be excluded from both branches. That's what makes `mid ± 1` correct.

**Why ternary search is worse**, despite intuitively "narrowing faster": splitting into thirds costs **two** probes per round to eliminate two-thirds, giving `2·log₃ n` ≈ `1.26·log₂ n` probes — about 26% more than binary search's `log₂ n`. When the *probe* is the expensive operation, halving with one probe wins. Worth being able to say why, since it's a natural "can we do better?" question.

**Why O(log n) is optimal.** Each guess returns one of three outcomes, so it yields at most `log₂ 3` ≈ 1.58 bits. Distinguishing `n` possibilities needs `log₂ n` bits, giving a lower bound of `log₃ n` guesses. Binary search achieves `log₂ n`, within a constant factor of that bound — and no strategy does asymptotically better.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
left = 1
right = n
```

The candidate range, **1-indexed** because the numbers start at 1. Both bounds are inclusive.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
while left <= right:
```

`<=` because both bounds are inclusive — when `left == right` there's still one unchecked candidate, and here that candidate is guaranteed to be the answer.
→ [while-loop](../syntax/while-loop.md)

```python
    mid = (left + right) // 2
```

The midpoint — the guess that minimizes the worst-case remaining range.

⚠️ With `n` up to 2³¹ − 1, `left + right` **overflows `int32`** in C++/Java. Python's arbitrary-precision integers make it safe here, but the portable form is `left + (right - left) // 2`.
→ [integer-division-modulo](../syntax/integer-division-modulo.md)

```python
    result = guess(mid)
```

**Call the API once and store it.** The value is needed for up to three comparisons; calling `guess()` repeatedly would triple the cost of the very operation you're minimizing.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
    if result == 0:
        return mid
```

Exact match — done.
→ [if-return](../syntax/if-return.md)

```python
    elif result == -1:
        right = mid - 1
```

**`-1` means my number is LOWER than your guess** — so the guess was too high. Discard `mid` and everything above it.

This is the line to double-check against the spec; inverting it produces a search that confidently converges on the wrong answer.

```python
    else:
        left = mid + 1
```

`result == 1` means my number is **higher** — the guess was too low. Discard `mid` and everything below it.
→ [elif-else](../syntax/elif-else.md)

The loop needs no fallback return: `1 <= pick <= n` guarantees the target is in range, so `guess` must eventually return 0.

<details>
<summary>The whole thing together</summary>

```python
# The guess API is already defined for you.
# @param num, your guess
# @return -1 if num is higher than the picked number
#          1 if num is lower than the picked number
#          otherwise return 0
# def guess(num: int) -> int:

class Solution:
    def guessNumber(self, n: int) -> int:

        left = 1
        right = n

        while left <= right:
            mid = (left + right) // 2
            result = guess(mid)

            if result == 0:
                return mid
            elif result == -1:
                right = mid - 1
            else:
                left = mid + 1
```

</details>

**Trace it** — `n = 10`, the picked number is **6**:

| `left` | `right` | `mid` | `guess(mid)` | Meaning | Action |
|---|---|---|---|---|---|
| 1 | 10 | 5 | `1` | pick is **higher** than 5 | `left = 6` |
| 6 | 10 | 8 | `-1` | pick is **lower** than 8 | `right = 7` |
| 6 | 7 | 6 | `0` | **match** | `return 6` ✅ |

**3 guesses** for a range of 10 — versus up to 10 for a linear scan.

**A second trace** — `n = 10`, pick = **1** (worst case for a low target):

| `left` | `right` | `mid` | `guess` | Action |
|---|---|---|---|---|
| 1 | 10 | 5 | `-1` (lower) | `right = 4` |
| 1 | 4 | 2 | `-1` (lower) | `right = 1` |
| 1 | 1 | 1 | `0` | `return 1` ✅ |

Note the final row only executes because the condition is `left <= right`. With `<`, the loop would exit at `left == right == 1` without ever guessing 1, and the function would fall off the end returning `None`.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(log n)</summary>

**O(log n) API calls.**

Each guess halves the range: `n` → `n/2` → `n/4` → … → 1. That's `log₂ n` halvings.

At `n = 2³¹ - 1` ≈ 2.1·10⁹, that's **31 guesses**.

| n | Guesses |
|---|---|
| 10 | 4 |
| 100 | 7 |
| 10⁶ | 20 |
| 2³¹ | **31** |

**Why this is optimal**, in the form worth saying aloud:

> Each guess returns one of three outcomes, so it conveys at most `log₂ 3` ≈ 1.58 bits. Identifying one of `n` numbers requires `log₂ n` bits, so at least `log₃ n` guesses are necessary. Binary search uses `log₂ n`, which is within a constant factor — asymptotically optimal.

**Why not ternary search then?** Splitting into thirds needs **two** probes per round to eliminate two-thirds, costing `2·log₃ n ≈ 1.26·log₂ n` probes — measurably *more* than binary search. Halving with a single probe is the efficient trade.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — four integers (`left`, `right`, `mid`, `result`), regardless of `n`.

Crucially, nothing is materialized. With `n` up to 2·10⁹, building an array of candidates would need ~8 GB; the algorithm instead searches an **implicit** ordered domain defined only by its bounds and a comparison function.

That's the same structural point as [First Bad Version](278-first-bad-version.md):

> **Binary search requires an ordered domain and a way to compare — not stored data.**

Which is exactly why the technique generalizes to "binary search on the answer," where the domain is a range of candidate answers and the comparison is a feasibility test — see [Koko Eating Bananas](875-koko-eating-bananas.md) and [Split Array Largest Sum](410-split-array-largest-sum.md).

An iterative loop keeps it O(1); a recursive formulation would add O(log n) stack frames for no benefit.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Each guess tells me a direction, so I can discard half the range every time — binary search over `[1, n]`. I guess the midpoint, which is optimal because it minimizes the worst-case remaining range. The API gives a three-way answer including an exact match, so this is a value search: `left <= right` with `mid ± 1` on each side. The one thing to be careful about is the sign convention — `-1` means *my number is lower than your guess*, so the guess was too high and I move `right` down. I also store the API result rather than calling it multiple times, since API calls are the cost being minimized. O(log n) guesses — about 31 at the maximum `n` — and O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Can you do better than O(log n)?" | No. Each guess yields ≤ `log₂ 3` bits, and identifying one of `n` numbers needs `log₂ n` bits — a `log₃ n` lower bound. |
| "What about ternary search?" | Worse. Two probes to eliminate two-thirds costs ~1.26× binary search's probes. |
| "What if the range were unbounded?" | Exponential search: probe 1, 2, 4, 8, … until you overshoot, then binary search the last interval. Still O(log n). |
| "What if `guess` sometimes **lied**?" | A different problem — noisy binary search. You'd repeat queries and take a majority, or use Rényi–Ulam techniques. |
| "Overflow?" | `n` can be 2³¹ − 1, so `left + right` overflows `int32` outside Python. Use `left + (right - left) // 2`. |
| "Why `left <= right` here but `left < right` in First Bad Version?" | Three-way compare resolves `mid` exactly, so it can be excluded with `mid ± 1`, which pairs with `<=`. Boundary search keeps `mid` via `right = mid`, which requires `<`. |
| "Minimize guesses when wrong answers cost money?" | That's the "guess number higher or lower II" variant — [LeetCode 375](https://leetcode.com/problems/guess-number-higher-or-lower-ii/) — a minimax DP, not binary search. |

**Traps:**

- **Inverting the sign convention.** `-1` means *the pick is lower*, i.e. your guess was too high. Reading it backwards gives a clean-looking wrong answer.
- **Using `left < right`.** Skips the final single candidate and can return `None`.
- **Calling `guess(mid)` more than once per iteration.** Triples the cost of the metric you're optimizing.
- **`left = 0`.** The domain starts at 1.
- **`left + right` overflow** in fixed-width languages, given `n` reaches `int32` max.
- **Using `right = mid`** with `<=`. Wrong convention pairing — infinite loop.

**This same move shows up in:** [Search Insert Position](35-search-insert-position.md) (same value-search convention over a real array) · [First Bad Version](278-first-bad-version.md) (the boundary-search convention, for contrast) · [Binary Search](704-binary-search.md) (the canonical form) · [Koko Eating Bananas](875-koko-eating-bananas.md) (binary search over an implicit domain of candidate answers).

</details>

---
