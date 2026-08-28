# 1011. Capacity To Ship Packages Within D Days

**Medium** · [LeetCode](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/) · [Solution file (no hints)](../../problems/1000-1499/1011.py)

[📖 05. Binary Search lesson](../learning/05-binary-search.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 05. Binary Search problems](../rmap-practice/05-binary-search.md)

---

Packages must ship within `days` days. The `i`-th package weighs `weights[i]`. Each day you load packages **in the given order**, never exceeding the ship's capacity. Return the **least** weight capacity that gets everything shipped within `days` days.

```
weights = [1,2,3,4,5,6,7,8,9,10], days = 5  →  15
    day 1: 1,2,3,4,5   day 2: 6,7   day 3: 8   day 4: 9   day 5: 10

weights = [3,2,2,4,1,4], days = 3  →  6
weights = [1,2,3,1,1],   days = 4  →  3
```

**Constraints:** `1 <= days <= weights.length <= 5·10⁴` · `1 <= weights[i] <= 500`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**least** weight capacity" | ⚠️ You're minimizing an **answer**, not searching an array. This is *binary search on the answer* |
| "in the **given order**" | ⚠️ No reordering or bin-packing — packages ship sequentially. This is what keeps the feasibility check simple and greedy |
| "within `days` days" | A **feasibility** question: can capacity `C` finish in ≤ `days`? |
| `weights.length` up to 5·10⁴ | An O(n) feasibility check inside an O(log range) search is comfortable |
| `weights[i]` up to 500 | Total weight ≤ 2.5·10⁷, which bounds the search range |

**The reframe that solves it.** You can't directly compute the minimum capacity — but you *can* easily answer:

> **"Given capacity `C`, how many days does shipping take?"**

Simulate greedily: keep loading until the next package would overflow, then start a new day. That's O(n).

And the crucial property:

> **Feasibility is monotonic in `C`.** If capacity `C` works, then `C + 1` works too (a bigger ship never needs more days). If `C` fails, every smaller capacity fails.

```
capacity:  10   11   12   13   14   15   16   17
feasible?  no   no   no   no   no  YES  YES  YES
                                   ↑
                        the boundary — the answer
```

False-then-true, flipping once. That's precisely what binary search needs — the same structure as [First Bad Version](278-first-bad-version.md), but the domain is *candidate capacities* rather than array indices.

**Setting the search bounds** — both matter and both have reasons:

- **`left = max(weights)`** — the ship must carry the heaviest single package, or it can never ship at all. Anything smaller is infeasible by definition.
- **`right = sum(weights)`** — carrying everything in one day is always feasible (given `days >= 1`), so this is a guaranteed-valid upper bound.

🤔 **Before you open the next section:** why can't the answer ever be less than the heaviest single package — and why is the total weight always enough?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

Let `n = len(weights)`, `S = sum(weights)`, `M = max(weights)`.

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Try every capacity | Test `M, M+1, M+2, …` until feasible | O(S · n) ≈ 10¹² | ❌ Hopeless |
| Greedy/DP partition | Dynamic programming over splits | O(n² · days) | ❌ Far too slow, and unnecessary |
| **Binary search on the answer** | Halve the capacity range; O(n) feasibility check | **O(n log S)** | ✅ |

**The decision: binary search over the capacity range, with a greedy O(n) feasibility check.**

This is the canonical **"binary search on the answer"** pattern, and it's worth learning as a named technique:

> When you can't compute the optimum directly but you **can cheaply verify** whether a candidate works — and verification is **monotonic** — binary search the answer space.

The three ingredients, all present here:

1. **A bounded answer range** — `[max(weights), sum(weights)]`
2. **A feasibility predicate** — "does capacity `C` finish within `days`?"
3. **Monotonicity** — bigger capacity never hurts

**Why the feasibility check can be greedy.** Because packages must ship **in order**, there's no packing decision to make: on each day, load as much as fits, then start a new day. Loading less than possible can never help — it only pushes work into later days. So the greedy simulation gives the *exact* minimum number of days for that capacity, not an approximation.

If reordering were allowed, this would become bin packing — NP-hard — and the whole approach would collapse. The "in the given order" clause is what makes the problem tractable, and calling that out shows you understand *why* the technique applies.

**Why the boundary convention.** You want the **smallest** feasible capacity, so:

- feasible at `mid` → `mid` is a candidate; keep it → `right = mid`
- infeasible at `mid` → `mid` is definitively too small → `left = mid + 1`
- loop while `left < right`, return `left`

Same `right = mid` / `left < right` pairing as [First Bad Version](278-first-bad-version.md) and [Find Peak Element](162-find-peak-element.md).

**Why `left = max(weights)` rather than 1.** With `left = 1`, capacities below the heaviest package are infeasible — the simulation would loop forever or need a special case, since a single package could never be loaded. Starting at `max` makes every candidate in the range at least *loadable*.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
def shipWithinDays(self, weights: List[int], days: int) -> int:
    left = max(weights)
    right = sum(weights)
```

**The answer range.**

- `left = max(weights)` — the minimum conceivable capacity; anything less can't carry the heaviest package.
- `right = sum(weights)` — everything in one day, always feasible.

Both are O(n) to compute, dominated by the search below.
→ [min-max-key](../syntax/min-max-key.md)

```python
    while left < right:
        mid = (left + right) // 2
```

Boundary-search convention — `<` pairs with `right = mid`.
→ [while-loop](../syntax/while-loop.md)

```python
        if self.daysNeeded(weights, mid) <= days:
            right = mid
        else:
            left = mid + 1
```

**The decision.**

- Feasible (`<= days`) → `mid` is a valid capacity, but maybe not the smallest. **Keep it** with `right = mid`.
- Infeasible → `mid` is too small; the answer is strictly larger. `left = mid + 1`.

Note `<=`, not `<` — finishing in exactly `days` days is success.
→ [comparison-operators](../syntax/comparison-operators.md) · [elif-else](../syntax/elif-else.md)

```python
    return left
```

Converged on the smallest feasible capacity.

---

**The feasibility check**

```python
def daysNeeded(self, weights, capacity):
    days_used = 1
    current_load = 0
```

Start on **day 1** with an empty ship. Starting at 1 (not 0) is right because shipping any non-empty list takes at least one day.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
    for w in weights:
        if current_load + w > capacity:
            days_used += 1
            current_load = 0
```

**The greedy rule.** If adding this package would overflow, close out the day and begin a new one with an empty ship.

Because order is fixed, there's no choice to make here — this simulation yields the exact minimum days for the given capacity.
→ [for-loop](../syntax/for-loop.md)

```python
        current_load += w
    return days_used
```

Load the package (onto whichever day is now current) and continue.

Since `capacity >= max(weights)` throughout the search, every individual package always fits after a reset — no infinite loop is possible.
→ [arithmetic-operators](../syntax/arithmetic-operators.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def shipWithinDays(self, weights: List[int], days: int) -> int:

        left = max(weights)
        right = sum(weights)

        while left < right:
            mid = (left + right) // 2

            if self.daysNeeded(weights, mid) <= days:
                right = mid
            else:
                left = mid + 1

        return left

    def daysNeeded(self, weights: List[int], capacity: int) -> int:

        days_used = 1
        current_load = 0

        for w in weights:
            if current_load + w > capacity:
                days_used += 1
                current_load = 0
            current_load += w

        return days_used
```

</details>

**Trace it** — `weights = [1,2,3,4,5,6,7,8,9,10]`, `days = 5`. Range: `left = 10`, `right = 55`.

| `left` | `right` | `mid` | Days needed at `mid` | ≤ 5? | Action |
|---|---|---|---|---|---|
| 10 | 55 | 32 | 2 | ✅ | `right = 32` |
| 10 | 32 | 21 | 3 | ✅ | `right = 21` |
| 10 | 21 | 15 | **5** | ✅ | `right = 15` ⭐ |
| 10 | 15 | 12 | 6 | ❌ | `left = 13` |
| 13 | 15 | 14 | 6 | ❌ | `left = 15` |
| 15 | 15 | — | — | — | exit |

`return 15` ✅

**Verifying `daysNeeded([1..10], 15) = 5`:**

| Day | Packages loaded | Load |
|---|---|---|
| 1 | 1,2,3,4,5 | 15 |
| 2 | 6,7 | 13 |
| 3 | 8 | 8 |
| 4 | 9 | 9 |
| 5 | 10 | 10 |

Exactly 5 days ✅ — and the starred row shows `right = mid` **keeping 15** in the range, which is what let it be returned. Using `right = mid - 1` there would have narrowed to `[10,14]` and returned 15's neighbor — wrong.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n log S)</summary>

**O(n · log S)**, where `S = sum(weights)`.

- The binary search runs over `[max(weights), sum(weights)]`, a range of size ≤ `S`, so **O(log S)** iterations.
- Each iteration runs an **O(n)** feasibility simulation.

At the constraints: `n = 5·10⁴`, `S ≤ 5·10⁴ × 500 = 2.5·10⁷`, so `log₂ S ≈ 25`. Total ≈ `5·10⁴ × 25` = **1.25·10⁶ operations** — instant.

**The general shape of "binary search on the answer":**

> **O(log(answer range)) × O(cost of one feasibility check)**

That formula is worth memorizing, because it makes the cost of these problems easy to estimate. Here the check is O(n); in other problems it might be O(n log n) or O(1).

**Compare to brute force:** testing every capacity from `M` upward is O(S · n) ≈ 10¹² — the log factor is doing enormous work.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).** A handful of integers across both functions; the simulation reuses two accumulators and allocates nothing.

`max()` and `sum()` are single passes with no auxiliary storage.

**The conceptual point:** the "array" being binary searched — the sequence of capacities `[M, M+1, …, S]` — is **never materialized**. It's an implicit ordered domain, exactly as in [Guess Number Higher or Lower](374-guess-number-higher-or-lower.md) and [Sqrt(x)](69-sqrtx.md). Building it would need 2.5·10⁷ entries; instead you compute feasibility on demand.

That's the recurring theme across this unit:

> **Binary search needs an ordered domain and a monotonic test. The domain can be array indices, version numbers, or — as here — the set of candidate answers itself.**

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "I can't compute the minimum capacity directly, but I *can* cheaply check whether a given capacity works: simulate greedily, loading packages in order until the next one would overflow, then start a new day. That's O(n) and it's exact, because the packages must ship in order — there's no packing choice, so greedy is optimal. Feasibility is monotonic: a bigger ship never needs more days. So I binary search the capacity range, from `max(weights)` — the ship must carry the heaviest package — up to `sum(weights)`, which always works in one day. When a capacity is feasible I keep it as a candidate with `right = mid`; when it isn't I move `left = mid + 1`. That converges on the smallest feasible capacity. O(n log S) time, O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why can the feasibility check be greedy?" | **The key question.** Order is fixed, so there's no packing decision — loading less than possible only defers work. Greedy gives the exact minimum days. |
| "What if packages could be **reordered**?" | It becomes bin packing — NP-hard. The "in order" constraint is what makes this tractable. |
| "Why `left = max(weights)`?" | Any smaller capacity can't carry the heaviest package, so it's infeasible by definition. |
| "Why `right = sum(weights)`?" | One day carrying everything is always feasible, so it's a guaranteed upper bound. |
| "This looks like [Koko Eating Bananas](875-koko-eating-bananas.md)." | Identical technique — different domain (speed vs capacity) and predicate (hours vs days). |
| "And [Split Array Largest Sum](410-split-array-largest-sum.md)?" | **The same problem** with different wording: minimize the largest subarray sum over `k` splits. |
| "Return the actual day-by-day split?" | Re-run the simulation at the final capacity, recording the boundaries. |

**Traps:**

- **`right = mid - 1`.** Discards a feasible candidate that might be the minimum. *The* bug in answer-space search.
- **`left <= right` with `right = mid`.** Infinite loop once the range reaches one element.
- **Starting `left = 1`.** Capacities below `max(weights)` are unshippable, and the simulation would misbehave.
- **`days_used = 0`.** Off by one — shipping anything takes at least one day.
- **Using `<` instead of `<=`** when comparing to `days`. Finishing in exactly `days` days is success.
- **Resetting `current_load = w` instead of `0` then adding.** Both work if written carefully, but mixing them drops a package.
- **Reaching for DP.** Correct but far slower, and it misses the point of the problem.

**This same move shows up in:** [Koko Eating Bananas](875-koko-eating-bananas.md) (the same answer-space search — eating speed instead of ship capacity) · [Split Array Largest Sum](410-split-array-largest-sum.md) (the same problem in different clothing) · [First Bad Version](278-first-bad-version.md) (the boundary-search convention this relies on) · [Sqrt(x)](69-sqrtx.md) (searching an implicit range of candidate answers).

</details>

---
