# 875. Koko Eating Bananas

**Medium** · [LeetCode](https://leetcode.com/problems/koko-eating-bananas/) · [Solution file (no hints)](../../problems/0500-0999/875.py)

[📖 05. Binary Search lesson](../learning/05-binary-search.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 05. Binary Search problems](../rmap-practice/05-binary-search.md)

---

Koko has `n` piles of bananas, where `piles[i]` is the size of the i-th pile, and the guards return in `h` hours.

Each hour she picks one pile and eats `k` bananas from it. **If the pile has fewer than `k`, she eats it all and does not continue eating during that hour.**

Return the **minimum** integer `k` such that she can eat all the bananas within `h` hours.

```
piles = [3,6,7,11],       h = 8   →  4
piles = [30,11,23,4,20],  h = 5   →  30
piles = [30,11,23,4,20],  h = 6   →  23
```

**Constraints:** `1 <= piles.length <= 10⁴` · `piles.length <= h <= 10⁹` · `1 <= piles[i] <= 10⁹`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

This is the problem where binary search stops being about arrays. **You binary search the answer itself.**

| The statement says | Which really means |
|---|---|
| "**minimum** integer `k`" | ⚠️ You're searching for a **number**, not an element in a collection. The search space is the range of possible speeds |
| "does **not continue** during that hour" | Each pile costs `ceil(pile / k)` hours — leftovers still burn a whole hour. **This is the formula** |
| `h >= piles.length` | At least one hour per pile, so an answer always exists (`k = max(piles)` always works) |
| `piles[i]` up to **10⁹** | The answer can be up to 10⁹ → you can't try every `k` |
| `h` up to 10⁹ | Doesn't bound the answer usefully; `max(piles)` does |
| n up to 10⁴ | Checking one candidate `k` costs O(n) — affordable if you only check ~30 of them |

**The realization.** Nothing here is sorted, and there's no array to search. But ask: what happens to the hours needed as `k` increases?

```
piles = [3,6,7,11], h = 8

k = 1  →  3 + 6 + 7 + 11 = 27 hours   too slow
k = 2  →  2 + 3 + 4 +  6 = 15 hours   too slow
k = 3  →  1 + 2 + 3 +  4 = 10 hours   too slow
k = 4  →  1 + 2 + 2 +  3 =  8 hours   ✅ fits
k = 5  →  1 + 2 + 2 +  3 =  8 hours   ✅ fits
k = 6  →  1 + 1 + 2 +  2 =  6 hours   ✅ fits
```

Hours needed **never increases** as `k` grows. So the feasibility pattern is:

```
k:        1     2     3     4     5     6   ...
feasible: ✗     ✗     ✗     ✓     ✓     ✓
                            ↑ the boundary — the answer
```

That's **monotonic** — and monotonic is the *actual* precondition for binary search. Sortedness in [704](704-binary-search.md) was just one instance of it. You're looking for the boundary between ✗ and ✓, and each test of a candidate `k` eliminates half the remaining range.

🤔 **Before you open the next section:** what's the smallest `k` worth testing, and the largest? Why is there no point trying anything above `max(piles)`?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Try every `k` from 1 upward | Stop at the first that fits | O(n · max) = 10¹³ | ❌ `max(piles)` is 10⁹ |
| Derive a formula | Compute `k` directly | — | ❌ Ceilings make it non-closed-form |
| **Binary search on `k`** | Halve the candidate range | **O(n log max)** | ✅ |

**The decision: binary search over the *answer space* `k ∈ [1, max(piles)]`.**

This is the pattern's second face, and the one that separates people who memorized binary search from people who understand it:

> **Binary search doesn't need an array. It needs a monotonic predicate.**

Here the predicate is `canFinish(k)` — "can Koko eat everything in ≤ h hours at speed k?" It's `False` for small `k` and `True` for large `k`, flipping exactly once. Binary search finds that flip point.

**The bounds:**
- **Low = 1** — she must eat at least one banana per hour.
- **High = `max(piles)`** — at that speed every pile takes exactly one hour, giving `n` hours total, and `h >= n` is guaranteed. Going faster can't help, since she can't start a second pile within an hour. **This is why `max(piles)` is the tight upper bound, not `sum(piles)`.**

**The feasibility check.** At speed `k`, a pile of size `p` takes `ceil(p / k)` hours — because leftovers waste the remainder of the hour. Summing over all piles gives the total. That ceiling is the direct encoding of "does not continue eating during that hour."

**The structural difference from [704](704-binary-search.md).** There, a match returned immediately. Here, finding a feasible `k` doesn't mean you're done — **a smaller one might also work**. So on success you *record* the candidate and keep searching left. The answer is the last feasible value seen.

That "record and continue" shape is the template for every *minimize/maximize* binary search, and it's worth internalizing separately from the "find exact value" template.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
left = 1
right = max(piles)
result = right
```

The candidate range for `k`, and `result` seeded with `max(piles)` — a speed **guaranteed** to work, so the answer is never unset. A defensive initialization that also documents the upper bound's meaning.
→ [min-max-key](../syntax/min-max-key.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
while left <= right:
    mid = (left + right) // 2
```

Same skeleton as [704](704-binary-search.md) — but `mid` is now a **candidate eating speed**, not an array index. Nothing else about the loop changes.
→ [while-loop](../syntax/while-loop.md) · [integer-division-modulo](../syntax/integer-division-modulo.md)

```python
    hours = 0
    for pile in piles:
        hours += (pile + mid - 1) // mid
```

**The feasibility check** — the only problem-specific part.

`(pile + mid - 1) // mid` is the **ceiling division** idiom: it computes `ceil(pile / mid)` using only integers. Adding `mid - 1` before flooring pushes any non-zero remainder up to the next whole number.

Check it: `pile = 7, mid = 3` → `(7 + 2) // 3 = 3`. And indeed 7 bananas at 3/hour takes 3 hours (3, 3, 1). ✅ A plain `7 // 3 = 2` would be wrong — it forgets the leftover banana still costs an hour.

*(Equivalently: `math.ceil(pile / mid)`, or `-(-pile // mid)`. The integer form avoids float precision entirely, which matters at 10⁹.)*
→ [integer-division-modulo](../syntax/integer-division-modulo.md) · [for-loop](../syntax/for-loop.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
    if hours <= h:
        result = mid
        right = mid - 1
```

**Feasible** — this speed works. But we want the *minimum*, so **record it and keep searching left** for something smaller. This is the key departure from [704](704-binary-search.md), where a match ended the search.

`<=` because finishing exactly at `h` hours counts as success.
→ [comparison-operators](../syntax/comparison-operators.md) · [if-return](../syntax/if-return.md)

```python
    else:
        left = mid + 1
```

**Too slow** — she runs out of time. This speed and everything below it are infeasible (slower is never better), so discard the entire left half.
→ [elif-else](../syntax/elif-else.md)

```python
return result
```

The smallest feasible speed found.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:

        left = 1
        right = max(piles)
        result = right

        while left <= right:
            mid = (left + right) // 2

            hours = 0
            for pile in piles:
                hours += (pile + mid - 1) // mid

            if hours <= h:
                result = mid
                right = mid - 1
            else:
                left = mid + 1

        return result
```

</details>

**Trace it** — `piles = [3,6,7,11]`, `h = 8`. Range starts at `[1, 11]`:

| `left` | `right` | `mid` | Hours at that speed | ≤ 8? | Action | `result` |
|---|---|---|---|---|---|---|
| 1 | 11 | 6 | 1+1+2+2 = 6 | ✅ | record, search left | **6** |
| 1 | 5 | 3 | 1+2+3+4 = 10 | ✗ | too slow, search right | 6 |
| 4 | 5 | 4 | 1+2+2+3 = **8** | ✅ | record, search left | **4** |
| 4 | 3 | — | — | | `left > right`, exit | **4** |

Answer: **4** ✅

Row 1 is the point of the pattern — speed 6 *works*, but returning immediately would give the wrong answer. Recording and continuing left found the genuinely minimal 4.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n log m)</summary>

**O(n · log m)**, where n = number of piles and m = `max(piles)`.

| Component | Cost |
|---|---|
| Binary search iterations | **O(log m)** — the range `[1, m]` halves each step |
| Feasibility check per iteration | **O(n)** — one pass over the piles |
| `max(piles)` once | O(n) |

O(n) + O(n · log m) = **O(n log m)**.

With the constraints: log₂(10⁹) ≈ **30** iterations × 10⁴ piles = ~3·10⁵ operations. Instant.

**Versus trying every k:** O(n · m) = 10⁴ × 10⁹ = **10¹³**. Binary search turns an impossible problem into a trivial one — and note it does so by shrinking the *number of candidates tested*, not by making each test faster.

**The general shape of answer-space binary search:**

```
O(log(range) × cost_of_one_feasibility_check)
```

Worth memorizing, because it's how you'll estimate every problem in this family. Notice the check itself is allowed to be expensive — you only run ~30 of them.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).**

Four integers — `left`, `right`, `result`, `hours` — plus the loop variable. `piles` is only read; nothing is built, sorted, or copied.

**Note what *didn't* happen: the search space was never materialized.** You're binary searching over `[1, 10⁹]` — a billion candidate speeds — while storing nothing but two bounds. Only ~30 of those candidates are ever evaluated.

That's the same trick as [Search a 2D Matrix](74-search-a-2d-matrix.md)'s virtual index, taken further: there the flat array at least corresponded to real data, whereas here **the search space is entirely conceptual**. There is no array of speeds anywhere.

This is why answer-space binary search is such a powerful pattern — the space can be astronomically large at zero memory cost, because you only ever hold its bounds.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "There's no array to search here — I'm searching for a number. The key observation is monotonicity: as the eating speed increases, the hours needed never increases, so feasibility flips from false to true exactly once. That's the real precondition for binary search, and sortedness is just a special case of it. So I binary search `k` over `[1, max(piles)]` — `max(piles)` is the tight upper bound because at that speed every pile takes exactly one hour and going faster can't help. For each candidate I sum `ceil(pile / k)` hours. Since I want the *minimum*, a feasible candidate doesn't end the search — I record it and keep looking left. O(n log m) time, O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "How did you know to binary search here?" | **The question.** Monotonic feasibility over a numeric range. Whenever "can I do it with X?" is false-then-true as X grows, you can binary search X. |
| "Why is `max(piles)` the upper bound?" | At that speed each pile takes exactly one hour → `n` hours total, and `h >= n` is guaranteed. She can't start a second pile in the same hour, so faster is wasted. |
| "Why not return immediately on a feasible `k`?" | You want the minimum — a smaller `k` may also work. Record and continue left. |
| "Explain the ceiling division." | `(p + k - 1) // k` rounds up with integer arithmetic. Leftovers still cost a full hour, per the problem statement. |
| "Maximize instead of minimize?" | Mirror it: record on success and search **right**. E.g. "split an array into k subarrays minimizing the largest sum" (LeetCode 410) or [Swim in Rising Water](778-swim-in-rising-water.md). |
| "What if `h < len(piles)`?" | Impossible — at most one pile per hour, so no answer exists. The constraints rule it out; you'd return −1. |
| "Use floats for the ceiling?" | `math.ceil(p / k)` risks precision loss at 10⁹. Integer arithmetic is exact. |

**Traps:**

- **Using `//` instead of ceiling division.** Undercounts hours and returns a speed that's too slow — the defining bug here.
- **Returning `mid` on the first feasible speed.** Gives *a* valid answer, not the minimum.
- **`left = 0`.** Speed 0 means she never eats; it also divides by zero.
- **`right = sum(piles)`.** Correct but wasteful — and it signals you haven't reasoned about the bound.
- **Trying to binary search the `piles` array.** There's nothing to find in it; the search space is the speeds.
- **`hours < h` instead of `<=`.** Finishing exactly on time is success.

**This same move shows up in:** [Binary Search](704-binary-search.md) (the loop skeleton) · [Search a 2D Matrix](74-search-a-2d-matrix.md) (searching a space you never build) · [Swim in Rising Water](778-swim-in-rising-water.md) (binary search the answer, with a graph feasibility check) · [Median of Two Sorted Arrays](4-median-of-two-sorted-arrays.md) (binary searching a partition rather than a value).

</details>
