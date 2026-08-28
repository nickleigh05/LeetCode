# 526. Beautiful Arrangement

**Medium** · [LeetCode](https://leetcode.com/problems/beautiful-arrangement/) · [Solution file (no hints)](../../problems/0500-0999/526.py)

[📖 10. Backtracking lesson](../learning/10-backtracking.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 10. Backtracking problems](../rmap-practice/10-backtracking.md)

---

A permutation `perm` of `1..n` (**1-indexed**) is **beautiful** if for every position `i`, either `perm[i]` is divisible by `i`, **or** `i` is divisible by `perm[i]`. Return **how many** beautiful arrangements exist.

```
n = 1  →  1
n = 2  →  2      [1,2]: 1|1 and 2|2   ·   [2,1]: 1|2 and 1|2
n = 3  →  3
```

**Constraints:** `1 <= n <= 15`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "a **permutation** of 1..n" | The [Permutations](46-permutations.md) skeleton: `used` array, no `start` index |
| "**either** divisible **or** divides" | A **symmetric** test — check both directions, not one |
| "return the **number** of" | ⚠️ **Count**, don't collect. No `path` list, no `res` — just an integer |
| `n <= 15` | 15! = 1.3 × 10¹². ⚠️ Brute force is **impossible**; the constraint is a warning |
| 1-indexed | Positions run `1..n`, same range as the values |

**Why this isn't just "generate permutations and filter".** 15! is 1.3 trillion. Filtering after the fact is not merely slow — it will never finish. The check has to happen **during** construction, killing branches at the moment they become invalid.

That's the whole idea, and it's the same one as [N-Queens](51-n-queens.md): a constraint that can be tested on a *partial* assignment turns an impossible enumeration into an easy one.

```
n = 3, trying to place at position 2:

perm = [1, ?, ?]
  ? = 2 → 2 % 2 == 0 ✓  keep going
  ? = 3 → 3 % 2 = 1 and 2 % 3 = 2 ✗  prune here, don't explore below
```

Pruning at position 2 discards the whole subtree beneath it. At n=15 that's what turns 10¹² into ~10⁵.

**Count, don't collect.** Every Unit 10 problem so far built a `res` list. Here the return type is `int`, which simplifies the code in a way worth noticing:

```python
if pos > n:
    return 1          # this arrangement is one valid arrangement
...
total += backtrack(pos + 1)     # sum what the children found
```

No `path`, no `path[:]` copy, no result list. The recursion **returns counts and adds them up**. That's a shape you'll reuse constantly in DP.

**The asymmetry that unlocks the optimisation.** Positions are not equally constrained. At n=15:

| Position | Numbers that can go there | Count |
|---|---|---|
| 1 | 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15 | **15** |
| 2 | 1,2,4,6,8,10,12,14 | 8 |
| 7 | 1,7,14 | 3 |
| **11** | **1,11** | **2** |
| **13** | **1,13** | **2** |

Position 1 accepts **everything** (every number is divisible by 1). Positions 11 and 13 accept **two numbers each**. Filling position 1 first means branching 15 ways before learning anything.

🤔 **Before you open the next section:** if you had to place queens on a board where one row had 15 legal squares and another had 2, which would you fill first? Does the same reasoning apply to positions here?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Generate all n!, filter | Plain permutations, test each | O(n·n!) | ❌ 1.3 × 10¹² at n=15. Impossible |
| **Backtracking with the divisibility check** | Prune the instant a position fails | **≈ O(n!) worst, tiny in practice** | ✅ |
| **…placing high positions first** | Most-constrained-first ordering | same bound, **~11× faster** | ✅ ← |
| **Bitmask DP** | `dp[mask]` — position is implied by popcount | **O(n·2ⁿ)** | ✅ Best guarantee |
| Precompute candidate lists | `valid[pos]` built once up front | same, smaller constant | ✅ Good with any of the above |

**The decision: backtracking with the check applied at every placement.** Then know the two upgrades.

**The core structure is [Permutations](46-permutations.md) with two edits:**

| | [Permutations](46-permutations.md) | **Beautiful Arrangement** |
|---|---|---|
| Tracks | `used` array | **`used` array** — same |
| Loop | all indices | **all values `1..n`** |
| Filter | none | **`num % pos == 0 or pos % num == 0`** |
| Base case | `len(path) == n` → append | **`pos > n` → return 1** |
| Accumulates | a result list | **an integer count** |

**Upgrade 1 — fill the most constrained positions first.** Instead of `pos = 1, 2, …, n`, go `pos = n, n-1, …, 1`.

High positions have few valid numbers (11 and 13 accept only two each), so the tree branches narrowly at the top and failures surface immediately. Position 1 — which accepts anything — is left for last, where it costs nothing.

Measured node counts, verified:

| n | answer | forward (1→n) | backward (n→1) | ratio |
|---|---|---|---|---|
| 8 | 132 | 1,138 | **486** | 2.3× |
| 12 | 4,010 | 58,612 | **15,437** | 3.8× |
| 15 | 24,679 | 747,961 | **102,376** | **7.3×** |

In wall-clock at n=15: **0.220s → 0.019s, about 11×.** And notice the ratio *grows* with n — this is the general "most-constrained-variable-first" heuristic, and it's the single most transferable idea in constraint search.

**Upgrade 2 — bitmask DP.** The state doesn't need the position at all:

```python
@lru_cache(maxsize=None)
def dp(mask):
    pos = bin(mask).count("1") + 1          # position is implied!
    if pos > n:
        return 1
    return sum(dp(mask | (1 << (num - 1)))
               for num in range(1, n + 1)
               if not mask & (1 << (num - 1))
               and (num % pos == 0 or pos % num == 0))
```

**The insight: `pos` is redundant.** If `mask` says which numbers are placed, then the number placed is `popcount(mask)`, so the next position is `popcount(mask) + 1`. Keying on `(pos, mask)` stores the same information twice.

That gives **O(n·2ⁿ)** — at n=15, 32,768 states (only **19,393** reachable) in **0.021s**, and unlike the backtracking it has a bound that doesn't depend on how the divisibility happens to fall.

**Which to write?** Backtracking with the backward ordering is the expected answer and is fast enough. **Mention the bitmask DP when asked for a bound**, and mention the ordering heuristic unprompted — it's the part that shows judgement.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
used = [False] * (n + 1)
```

⚠️ **`n + 1`, not `n`.** Values are `1..n`, so indexing by value directly needs a slot for `n`. Index 0 goes unused — deliberately, to keep `used[num]` readable rather than `used[num - 1]`.
→ [list-basics](../syntax/list-basics.md)

```python
def backtrack(pos):
    if pos > n:
        return 1
```

**Base case: every position filled → this is one valid arrangement.**

Returning **1** rather than appending to a list is the counting shape. Each leaf contributes 1, and the sums propagate up.
→ [recursion-basics](../syntax/recursion-basics.md) · [if-return](../syntax/if-return.md)

```python
    total = 0
    for num in range(1, n + 1):
        if used[num]:
            continue
```

Loop over **values** `1..n`, skipping ones already placed. `range(1, n + 1)` because both bounds are 1-based.
→ [range-function](../syntax/range-function.md) · [for-loop](../syntax/for-loop.md)

```python
        if num % pos != 0 and pos % num != 0:
            continue
```

**The beauty test**, negated so it reads as a skip.

The condition is "beautiful **if** `num % pos == 0` **or** `pos % num == 0`", so it's *not* beautiful when **both** fail — De Morgan turns the `or` into an `and`. Getting this backwards is easy; check it against `pos=2, num=3`: `3 % 2 = 1 ≠ 0` and `2 % 3 = 2 ≠ 0`, so skip. ✓

No division-by-zero risk: `num >= 1` and `pos >= 1` always.
→ [integer-division-modulo](../syntax/integer-division-modulo.md) · [logical-operators](../syntax/logical-operators.md) · [break-continue](../syntax/break-continue.md)

```python
        used[num] = True
        total += backtrack(pos + 1)
        used[num] = False
```

**Choose, explore, un-choose** — with the explore step **accumulating** instead of discarding its return value.

`total += backtrack(...)` is the line that makes this a counting problem. Compare [Permutations](46-permutations.md), where the recursive call's value is ignored because results are collected in a shared list.

Only **one** thing to undo here (`used[num]`), since there's no `path` to pop.
→ [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
    return total

return backtrack(1)
```

Start at **position 1**.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def countArrangement(self, n: int) -> int:

        used = [False] * (n + 1)

        def backtrack(pos):
            if pos > n:
                return 1

            total = 0
            for num in range(1, n + 1):
                if used[num]:
                    continue
                if num % pos != 0 and pos % num != 0:
                    continue

                used[num] = True
                total += backtrack(pos + 1)
                used[num] = False

            return total

        return backtrack(1)
```

</details>

**Trace it** — `n = 3`, the complete search. Verified output, every branch shown:

| Depth | Position | Number | Test | Outcome |
|---|---|---|---|---|
| 0 | 1 | 1 | 1 % 1 = 0 ✓ | place |
| 1 | 2 | 2 | 2 % 2 = 0 ✓ | place |
| 2 | 3 | 3 | 3 % 3 = 0 ✓ | place |
| 3 | — | — | `pos 4 > 3` | **count 1** ✅ |
| 1 | 2 | 3 | 3%2=1, 2%3=2 | ✗ **skip** |
| 0 | 1 | 2 | 2 % 1 = 0 ✓ | place |
| 1 | 2 | 1 | 2 % 1 = 0 ✓ | place |
| 2 | 3 | 3 | 3 % 3 = 0 ✓ | place |
| 3 | — | — | `pos 4 > 3` | **count 1** ✅ |
| 1 | 2 | 3 | 3%2=1, 2%3=2 | ✗ **skip** |
| 0 | 1 | 3 | 3 % 1 = 0 ✓ | place |
| 1 | 2 | 1 | 2 % 1 = 0 ✓ | place |
| 2 | 3 | 2 | 2%3=2, 3%2=1 | ✗ **skip** |
| 1 | 2 | 2 | 2 % 2 = 0 ✓ | place |
| 2 | 3 | 1 | 3 % 1 = 0 ✓ | place |
| 3 | — | — | `pos 4 > 3` | **count 1** ✅ |

**Total = 3** ✅ — the arrangements `[1,2,3]`, `[2,1,3]`, `[3,2,1]`.

**Position 1 never rejects anything** — all three rows at depth 0 place successfully, because every integer is divisible by 1. That's the wasted branching the backward ordering fixes: at n=15, position 1 fans out 15 ways before a single constraint has been tested.

**The `✗ skip` rows are the pruning.** Each one discards a subtree without recursing. Only three of them here; at n=15 they cut 10¹² down to about 10⁵ nodes.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n!) worst case, ~O(n·2ⁿ) in practice</summary>

**Backtracking: O(n!) as a bound**, but wildly pessimistic — the divisibility constraint does most of the work.

The honest framing:

> "The bound is O(n!) since it's a permutation search, but the constraint prunes so aggressively that the real node count is nowhere near it — about 750,000 at n=15 against 1.3 trillion permutations. Roughly six million times smaller."

**Measured:**

| n | n! | nodes (forward) | nodes (backward) |
|---|---|---|---|
| 8 | 40,320 | 1,138 | **486** |
| 12 | 479,001,600 | 58,612 | **15,437** |
| 15 | **1.3 × 10¹²** | 747,961 | **102,376** |

At n=15 the backward ordering visits **~10⁷ times fewer nodes than there are permutations**.

**Why the constraint prunes so well:** a position `pos` accepts only its divisors and multiples within `1..n` — roughly `n/pos + d(pos)` numbers, which is small for large `pos`. The product of the branching factors is nothing like n!.

**Bitmask DP: O(n·2ⁿ)** — a real guarantee.

- **2ⁿ states** = 32,768 at n=15 (only **19,393** actually reachable)
- **O(n)** work per state
- ≈ **500,000 operations**, independent of how the divisibility falls

**Practically all three are instant at n=15** (0.220s / 0.019s / 0.021s). The value of knowing the DP is being able to state a bound that doesn't rely on "the pruning works out".

**⚠️ Why filtering doesn't work here** — and this is the point of the `n <= 15` constraint. Generating 15! permutations at a billion per second takes **~22 minutes**. The constraint isn't saying "exponential is fine", it's saying "**prune, or don't bother**".

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n) auxiliary</summary>

**O(n) auxiliary** for the backtracking version.

| Component | Size |
|---|---|
| **Recursion depth** | exactly n — one frame per position → **O(n)** |
| `used` | n + 1 booleans → **O(n)** |
| Output | a single integer → **O(1)** |

**The output is O(1)** — one of the few problems in this unit where nothing accumulates. Counting instead of collecting eliminates the O(n·n!) result list that dominates [Permutations](46-permutations.md) and [Permutations II](47-permutations-ii.md):

| Problem | Auxiliary | Output |
|---|---|---|
| [Permutations](46-permutations.md) | O(n) | **O(n·n!)** |
| [Permutations II](47-permutations-ii.md) | O(n) | O(n·P) |
| **Beautiful Arrangement** | **O(n)** | **O(1)** ← |

**Bitmask DP costs O(2ⁿ)** for the memo — 19,393 entries at n=15. Same trade as [Partition to K Equal Sum Subsets](698-partition-to-k-equal-sum-subsets.md): a guaranteed time bound purchased with exponential memory.

**Precomputing candidate lists** (`valid[pos] = [numbers that fit]`) costs O(n²) space up front but removes the inner scan-and-test. Worth it if `countArrangement` is called repeatedly; unnecessary for a single call.

**⚠️ `used` is sized `n + 1`**, not `n` — values are 1-indexed. Sizing it `n` gives an `IndexError` on the very last value.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "It's a permutation search, so `used` array, no `start` index — but with two differences from plain Permutations. First, I'm counting rather than collecting, so the base case returns 1 and each frame sums what its children return; there's no path list at all. Second, and this is what makes it feasible, I test the divisibility condition at the moment I place a number, not at the end — 15! is 1.3 trillion, so filtering after the fact never finishes, whereas pruning brings it to about 750,000 nodes. The refinement I'd add is ordering: position 1 accepts every number while positions 11 and 13 accept only two, so I fill the **high** positions first. Most-constrained-first is worth about 11× at n=15. If they want a hard bound rather than 'the pruning works out', it's bitmask DP over which numbers are used — and the position doesn't need to be in the state, since it's just popcount plus one. That's O(n·2ⁿ)."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why not generate and filter?" | 15! = 1.3 × 10¹² — roughly 22 minutes at a billion/sec. Pruning during construction gives ~750K nodes. |
| "Which position should you fill first?" | **The question.** The most constrained one — high positions, which accept only their divisors and multiples. ~11× at n=15, and the ratio grows with n. |
| "Why is the position not part of the DP state?" | It's `popcount(mask) + 1` — implied by the mask. Keying on both stores the same fact twice. |
| "Write the condition." | `num % pos == 0 or pos % num == 0`. As a skip: `and` both `!= 0`. Sanity-check with `pos=2, num=3`. |
| "Why `used` of size n+1?" | Values are 1..n and indexing by value keeps it readable. Index 0 is intentionally unused. |
| "Precompute the candidates?" | `valid[pos]` built once, O(n²) space — removes the inner test. Worth it for repeated calls. |
| "Is there a closed form?" | None known — the counts are irregular. For n=1..15: 1, 2, 3, 8, 10, 36, 41, 132, 250, 700, 750, 4010, 4237, 10680, 24679. Note 11 → 750 is barely more than 10 → 700, because 11 is prime and position 11 accepts only two numbers. |
| "What if you needed to **list** them?" | Add a `path`, append `path[:]` at the base case — but the output becomes the bottleneck (24,679 lists at n=15). |
| "Same idea in another problem?" | [N-Queens](51-n-queens.md) — identical shape: assign one row/position at a time, test the constraint against a partial assignment, prune. |

**Traps:**

- **Filtering after generating.** Not slow — *non-terminating* at n=15. The defining mistake.
- **Getting the negated condition wrong.** `if num % pos != 0 or pos % num != 0: continue` skips almost everything (De Morgan: the `or` must become `and`). Test with `pos=1`.
- **`used = [False] * n`** — off by one; values run to `n`, so it needs `n + 1` slots.
- **Looping `range(n)`** instead of `range(1, n + 1)` — introduces a 0 and drops `n`; `0 % pos` is 0, so a zero silently passes the test.
- **Building a `path` you never use** — harmless but pointless when only the count is wanted.
- **Forgetting `used[num] = False`** — the [Permutations](46-permutations.md) trap; here it silently undercounts rather than crashing.
- **Filling position 1 first without thinking about it** — correct, ~11× slower, and the thing an interviewer is most likely to probe.

**This same move shows up in:** [Permutations](46-permutations.md) (the skeleton, with no constraint) · [N-Queens](51-n-queens.md) and [N-Queens II](52-n-queens-ii.md) (constrained assignment with pruning; N-Queens II also counts rather than collects) · [Partition to K Equal Sum Subsets](698-partition-to-k-equal-sum-subsets.md) (the same bitmask-DP-as-guarantee alternative) · [backtracking](../algorithms/backtracking.md) · [dynamic-programming](../algorithms/dynamic-programming.md).

</details>

---
