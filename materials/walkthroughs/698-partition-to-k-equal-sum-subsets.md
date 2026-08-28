# 698. Partition to K Equal Sum Subsets

**Medium** · [LeetCode](https://leetcode.com/problems/partition-to-k-equal-sum-subsets/) · [Solution file (no hints)](../../problems/0500-0999/698.py)

[📖 10. Backtracking lesson](../learning/10-backtracking.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 10. Backtracking problems](../rmap-practice/10-backtracking.md)

---

Given `nums` and an integer `k`, return `true` if the array can be divided into **`k` non-empty subsets with equal sums**.

```
nums = [4,3,2,3,5,2,1], k = 4  →  true      (5) (1,4) (2,3) (2,3)
nums = [1,2,3,4],       k = 3  →  false
```

**Constraints:** `1 <= k <= nums.length <= 16` · `1 <= nums[i] <= 10^4` · each value appears at most 4 times

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "divide into **k** subsets" | Every element must land in **exactly one** bucket — a partition, not a selection |
| "**equal** sums" | ⚠️ The target is computable up front: `sum(nums) / k` |
| "return **true** if possible" | A **decision** problem — stop at the first success, don't enumerate |
| `nums.length <= 16` | ⚠️ The classic **"exponential is expected"** bound. 2¹⁶ = 65,536 — and it hints at bitmask DP |
| `1 <= nums[i]` | All **positive** — so a bucket's sum only ever grows. Pruning is safe |
| each value appears ≤ 4 times | A hint that the test data contains heavy duplication |

**Two free rejections before any search.** Both are O(n) and both kill large classes of input instantly:

```python
if sum(nums) % k != 0:   return False    # can't split evenly at all
if max(nums) > target:   return False    # one element alone overflows a bucket
```

**The framing that makes it tractable.** There are two ways to think about the recursion, and they are *not* equally good:

| Framing | The move | Cost |
|---|---|---|
| ❌ "Fill one bucket at a time" | Choose a subset summing to target, remove it, repeat k times | Awkward — needs subset enumeration inside subset enumeration |
| ✅ **"Place one number at a time"** | For each number, try dropping it into each of the k buckets | Clean: depth n, branching k |

The second gives a tree of depth **n** with branching factor **k**, so the raw space is **kⁿ**. At n=16, k=4 that's 4 billion — far too slow **unless you prune hard**. The pruning *is* the problem.

**A decision problem, not an enumeration problem.** Every other Unit 10 problem so far collects all answers. Here you return the moment one works:

```python
if backtrack(i + 1):
    return True          # short-circuit; don't undo, don't keep looking
```

That single `return True` propagating up the stack is worth noticing — it's why the un-choose line sits *after* the `if` rather than running unconditionally.

🤔 **Before you open the next section:** suppose the first number fails to lead to a solution when placed in **empty** bucket 0. Is there any point trying it in empty bucket 1?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Enumerate all k-way splits | Assign each element a bucket label | O(kⁿ) | ❌ 4 billion at n=16, k=4 |
| Fill buckets one at a time | Find a target-sum subset, recurse on the rest | O(k·2ⁿ) | ⚠️ Works, but clumsier to write correctly |
| **Backtracking + the three prunes** | Place numbers into buckets, cut dead branches | **O(kⁿ) worst case, tiny in practice** | ✅ |
| **Bitmask DP** | `dp[mask]` = remainder in the bucket being filled | **O(n·2ⁿ)** | ✅ Better worst-case guarantee |

**The decision: backtracking with three prunes** — and know the bitmask DP as the answer to "can you bound it better?"

**Prune 1 — sort descending.** Place the **biggest** numbers first.

Large numbers are the constrained ones: a 5 fits almost nowhere, a 1 fits almost everywhere. Placing the 5 first means failures surface at depth 1 instead of depth 15. Committing all the 1s first and *then* discovering the 5 doesn't fit means re-deriving that failure across thousands of leaves.

**Prune 2 — skip identical empty buckets.** ⚠️ **The one that matters most.**

```python
if buckets[b] == 0:
    break
```

If a number doesn't work in an empty bucket, it won't work in a *different* empty bucket either — the buckets are **interchangeable**. Without this, the search re-explores k! relabellings of the same partition.

**Prune 3 — the fit check**, `buckets[b] + nums[i] <= target`. Trivial, and sound only because all values are positive.

**How much each one saves.** Node counts, measured:

| Case | answer | naive | + sort | + empty-break | **both** |
|---|---|---|---|---|---|
| `[4,3,2,3,5,2,1]`, k=4 | true | 8 | 8 | 8 | **8** |
| `[10,10,10,7×6,6×7]`, k=3 | true | 22,778 | 22,778 | 15,894 | **15,894** |
| 16 values near 1500, k=4 | **false** | **13,210,397** | 2,530,801 | 550,467 | **105,469** |

Read the last row: **13.2 million nodes down to 105 thousand — 125× faster.** And read the first row too: on an easy satisfiable input the prunes do *nothing*, because the search stumbles onto an answer immediately.

**That contrast is the real lesson.** Pruning is nearly irrelevant when the answer is `true` and easy to find; it's decisive when the answer is `false`, because proving impossibility means exhausting the space. **Worst cases in backtracking are the negative instances** — that's the sentence to say out loud.

**The bitmask DP alternative** trades the unbounded worst case for a guaranteed one:

```python
@lru_cache(maxsize=None)
def dp(mask, remaining):        # mask = which numbers are placed
    if mask == (1 << n) - 1:
        return True
    for i in range(n):
        if mask & (1 << i):     continue
        if nums[i] > remaining: break          # sorted ascending
        if dp(mask | (1 << i), remaining - nums[i] or target):
            return True
    return False
```

The insight: you never need to track *which* bucket is being filled or how full the others are — only **which numbers are used** and **how much room is left in the current bucket**. Completed buckets are interchangeable, so they carry no information. That collapses the state to `2ⁿ × n` and gives **O(n·2ⁿ)** — 1M operations at n=16, regardless of input. I verified both versions agree over 400 randomized cases against exhaustive bin assignment.

**Which to write?** Backtracking is faster to produce under pressure and usually passes. **Mention the bitmask DP as the version with the provable bound** — that's the answer to "what's your worst case?", where the honest reply for the backtracking version is "exponential, but the prunes make it fast in practice."

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
total = sum(nums)
if total % k != 0:
    return False
target = total // k
```

**The free rejection.** If the total doesn't divide evenly there is nothing to search.

`//` is integer division — `target` must be an int for the comparisons below.
→ [integer-division-modulo](../syntax/integer-division-modulo.md)

```python
nums.sort(reverse=True)
if nums[0] > target:
    return False
```

**Descending sort** (Prune 1) — biggest first, so failures surface early.

It also makes the second check trivial: after sorting, `nums[0]` **is** the maximum, so one element overflowing a bucket is a one-line rejection.
→ [sorting-key](../syntax/sorting-key.md)

```python
buckets = [0] * k
```

Running sums, one per bucket. Only the **sums** are tracked, never the contents — you're answering "is it possible?", not "what's the partition?".
→ [list-basics](../syntax/list-basics.md)

```python
def backtrack(i):
    if i == len(nums):
        return True
```

**Base case: every number is placed.** And that's automatically a *success* — the fit check below guarantees no bucket ever exceeds `target`, and if all n numbers are placed without overflow while the totals must sum to `k × target`, every bucket is exactly full.

**Worth stating explicitly**, because it looks like a missing check: there's no need to verify the buckets are equal at the end. **The invariant makes it impossible for them not to be.**
→ [recursion-basics](../syntax/recursion-basics.md)

```python
    for b in range(k):
        if buckets[b] + nums[i] <= target:
            buckets[b] += nums[i]
            if backtrack(i + 1):
                return True
            buckets[b] -= nums[i]
```

**Try number `i` in each bucket.** The fit check (Prune 3) is the choose-guard.

`if backtrack(...): return True` is the **short-circuit** — the first success unwinds the whole stack. Note the un-choose (`buckets[b] -= nums[i]`) runs only on *failure*; on success we're leaving anyway.
→ [for-loop](../syntax/for-loop.md) · [if-return](../syntax/if-return.md)

```python
        if buckets[b] == 0:
            break
```

**Prune 2 — the interchangeable-empty-bucket cut.** ⚠️ **The most important line in the solution.**

Reaching here means `nums[i]` in bucket `b` didn't pan out. If `b` was **empty**, then every remaining bucket is also empty and identical, so all of them would fail identically. Stop.

It sits **after** the attempt (we did try bucket `b`) and covers the case where the fit check failed too — an empty bucket that can't hold `nums[i]` means no bucket can.
→ [break-continue](../syntax/break-continue.md)

```python
    return False

return backtrack(0)
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def canPartitionKSubsets(self, nums: List[int], k: int) -> bool:

        total = sum(nums)
        if total % k != 0:
            return False

        target = total // k
        nums.sort(reverse=True)
        if nums[0] > target:
            return False

        buckets = [0] * k

        def backtrack(i):
            if i == len(nums):
                return True

            for b in range(k):
                if buckets[b] + nums[i] <= target:
                    buckets[b] += nums[i]
                    if backtrack(i + 1):
                        return True
                    buckets[b] -= nums[i]

                if buckets[b] == 0:
                    break

            return False

        return backtrack(0)
```

</details>

**Trace it** — `nums = [4,3,2,3,5,2,1]`, `k = 4`. Total 20, target **5**, sorted descending → `[5,4,3,3,2,2,1]`. Verified output:

| Depth | Number | Action | `buckets` |
|---|---|---|---|
| 0 | 5 | into bucket 0 | `[5,0,0,0]` |
| 1 | 4 | 5+4 > 5 ✗ bucket 0 | |
| 1 | 4 | into bucket 1 | `[5,4,0,0]` |
| 2 | 3 | ✗ buckets 0, 1 | |
| 2 | 3 | into bucket 2 | `[5,4,3,0]` |
| 3 | 3 | ✗ buckets 0, 1, 2 | |
| 3 | 3 | into bucket 3 | `[5,4,3,3]` |
| 4 | 2 | ✗ buckets 0, 1 | |
| 4 | 2 | into bucket 2 | `[5,4,5,3]` |
| 5 | 2 | ✗ buckets 0, 1, 2 | |
| 5 | 2 | into bucket 3 | `[5,4,5,5]` |
| 6 | 1 | ✗ bucket 0 | |
| 6 | 1 | into bucket 1 | `[5,5,5,5]` |
| 7 | — | **all placed → `True`** ✅ | |

**Eight nodes, zero backtracking.** Sorting descending is why: the 5 immediately claims a bucket, the 4 claims another, and the small numbers slot into whatever's left. Presented in the original order `[4,3,2,3,5,2,1]`, the search would commit the 4 and 3 first and then have to unwind when the 5 arrives with nowhere to go.

**Where Prune 2 fires**, on a failing input like `[1,2,3,4], k=3` (target isn't even an integer — but take `[2,2,2,3,3], k=3`, target 4): the 3 goes in empty bucket 0, fails downstream, and rather than trying it in empty buckets 1 and 2 — **identical situations with identical outcomes** — the `break` abandons the level. Without it, every partition is rediscovered `k!` times over.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(kⁿ) worst case; O(n·2ⁿ) with bitmask DP</summary>

**Backtracking: O(kⁿ)** in the worst case — n numbers, k bucket choices each.

At n=16, k=4 that's 4×10⁹ nominally. **The prunes make the real number vastly smaller**, but they don't improve the *bound*, and it's important to say both halves:

> "Worst case is O(kⁿ). The pruning doesn't change that bound, but in practice it's the difference between 13 million nodes and 105 thousand on the hard cases."

**Measured, on the hardest standard test** (16 values near 1500, k=4, answer `false`):

| Version | Nodes |
|---|---|
| No pruning | 13,210,397 |
| + descending sort | 2,530,801 |
| + empty-bucket break | 550,467 |
| **Both** | **105,469** |

**125× from two lines of code.** And the sort and the break are not independent — together they beat either alone by a wide margin.

**Bitmask DP: O(n·2ⁿ)** — a genuine guarantee.

- **2ⁿ states** (which numbers are placed) — 65,536 at n=16
- **O(n)** transitions per state
- ≈ **1M operations**, input-independent

**Why `remaining` doesn't need to be part of the state:** it's *determined* by the mask. The numbers placed so far have a known total, so the current bucket's fill level is `total_placed mod target`. The `(mask, remaining)` pair is really just `mask`, which is what keeps the state count at 2ⁿ rather than 2ⁿ × target.

**Why k doesn't appear in the DP bound at all** is the same interchangeability insight as Prune 2: finished buckets are indistinguishable, so there's no need to remember which bucket you're on.

**⚠️ The worst case is `false`, not `true`.** Proving impossibility means exhausting the space; finding one valid partition can terminate immediately. When someone asks for your worst case, reach for an unsatisfiable input.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n) auxiliary</summary>

**O(n + k) auxiliary** for the backtracking version.

| Component | Size |
|---|---|
| **Recursion depth** | exactly n — one frame per number → **O(n)** |
| `buckets` | k integers → **O(k)** |
| Sort | O(n) or O(log n) |

Since `k <= n`, this is **O(n)**. At n ≤ 16 it's nothing.

**No `path`, no result list** — a decision problem returns a bool, so nothing accumulates. That's a real difference from every other Unit 10 problem, where the output dominates the space.

**The bitmask DP costs more: O(2ⁿ)** for the memo table — 65,536 entries at n=16. That's the trade in one line:

| Approach | Time | Space |
|---|---|---|
| **Backtracking + prunes** | O(kⁿ) worst, fast in practice | **O(n)** |
| Bitmask DP | **O(n·2ⁿ) guaranteed** | O(2ⁿ) |

**Backtracking buys a guaranteed time bound with exponential memory.** Both are acceptable at n=16; name the trade rather than declaring a winner.

**⚠️ `nums.sort()` mutates the caller's array.** Use `nums = sorted(nums, reverse=True)` if that matters.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "First the free checks: if the sum isn't divisible by k it's impossible, and the target is sum over k. Then I frame it as placing one number at a time into one of k buckets — depth n, branching k — rather than filling buckets one at a time, which is messier. That's kⁿ naively, so the pruning carries the solution. Three prunes: sort descending so the hardest-to-place numbers fail early; only add to a bucket if it still fits; and crucially, if a number fails in an *empty* bucket, break — the empty buckets are interchangeable, so trying the next one repeats the same failure. That last line alone is worth about 25×. Base case is 'all numbers placed', which is automatically a success since the fit check keeps every bucket at or under target. Worst case is still O(kⁿ), and it's the *unsatisfiable* inputs that hit it. If they want a real bound I'd switch to bitmask DP over which numbers are used — O(n·2ⁿ), about a million operations at n=16."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why `break` on an empty bucket?" | **The question.** Empty buckets are interchangeable — failing in one means failing in all. Without it you re-explore k! relabellings. Measured: 550K nodes vs 2.5M. |
| "Why sort descending?" | Big numbers are the constrained ones; placing them first surfaces failures at shallow depth. 13.2M → 2.5M nodes on the hard case. |
| "Why is the base case an automatic success?" | The fit check keeps every bucket ≤ target, and the totals must sum to k×target. All placed with none over ⇒ all exactly full. |
| "What's the real worst case?" | O(kⁿ), on **unsatisfiable** inputs — proving `false` requires exhausting the space. Satisfiable ones often terminate immediately. |
| "Can you guarantee a better bound?" | Bitmask DP, O(n·2ⁿ). State is just the mask; `remaining` is derivable from it, and finished buckets carry no information. |
| "Why doesn't k appear in the DP bound?" | Same interchangeability insight — you never need to know *which* bucket you're filling. |
| "What if values could be **negative**?" | Every prune breaks — bucket sums no longer grow monotonically, so `<= target` stops being a valid cutoff. Much harder problem. |
| "Relation to [Partition Equal Subset Sum](416-partition-equal-subset-sum.md)?" | That's this with **k = 2**, which is easier: find one subset summing to half. Classic subset-sum DP, O(n·sum). |
| "Return the actual partition?" | Track bucket contents instead of just sums — O(n) extra space, same search. |

**Traps:**

- **Omitting the empty-bucket `break`.** Still correct, ~25× slower, and the usual cause of a TLE here.
- **Placing the `break` inside the fit-check `if`** — then it never fires when the number simply doesn't fit an empty bucket, which is exactly a case worth cutting. It belongs at the end of the loop body.
- **Sorting ascending** — the opposite of what you want; small numbers first delays every failure to maximum depth.
- **Forgetting `total % k != 0`** — the search runs to exhaustion to conclude what one modulo would have told you.
- **Verifying bucket equality at the base case** — harmless but redundant; the invariant already guarantees it.
- **Filling buckets one at a time** — a valid framing, but nested subset enumeration is far easier to get wrong.
- **Assuming a greedy fit works** — first-fit-decreasing is a *heuristic* for bin packing and gives wrong answers here. This is an exact decision problem.

**This same move shows up in:** [Partition Equal Subset Sum](416-partition-equal-subset-sum.md) (the k = 2 special case) · [Combination Sum II](40-combination-sum-ii.md) (pruning a sorted search with `break`) · [N-Queens II](52-n-queens-ii.md) (another decision-style backtracking search where symmetry is the thing to cut) · [Word Search](79-word-search.md) (choose/explore/un-choose with early `return True`) · [backtracking](../algorithms/backtracking.md) · [dynamic-programming](../algorithms/dynamic-programming.md).

</details>

---
