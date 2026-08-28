# 1027. Longest Arithmetic Subsequence

**Medium** · [LeetCode](https://leetcode.com/problems/longest-arithmetic-subsequence/) · [Solution file (no hints)](../../problems/1000-1499/1027.py)

[📖 14. 1-D DP lesson](../learning/14-dp-1d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 13. 1-D Dynamic Programming problems](../rmap-practice/13-dp-1d.md)

---

Return the length of the longest **arithmetic subsequence** of `nums` — a subsequence whose consecutive differences are all equal.

```
nums = [3,6,9,12]         →  4      the whole array, step 3
nums = [9,4,7,2,10]       →  3      [4,7,10], step 3
nums = [20,1,15,3,10,5,8] →  4      [20,15,10,5], step −5
```

**Constraints:** `2 <= nums.length <= 1000` · `0 <= nums[i] <= 500`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**subsequence**" | ⚠️ Elements need not be adjacent — order preserved, gaps allowed |
| "`seq[i+1] - seq[i]` are all the same" | A single fixed step throughout |
| — | ⚠️ The step can be **negative or zero** — Example 3 uses −5 |
| `nums.length <= 1000` | O(n²) = 10⁶ is comfortable; O(n³) = 10⁹ is not |
| `0 <= nums[i] <= 500` | ⚠️ So differences range over **−500..500** — a small, bounded set |
| `length >= 2` | Any two elements form a valid arithmetic subsequence, so the answer is ≥ 2 |

**Why [Longest Increasing Subsequence](300-longest-increasing-subsequence.md)'s state isn't enough.** There, `dp[i]` = "longest increasing subsequence ending at `i`" suffices, because "can I extend?" depends only on a comparison. Here it doesn't:

```
nums = [1, 3, 5, 9]

ending at index 2 (value 5):  [1,3,5] with step 2 — length 3
ending at index 3 (value 9):  can I extend [1,3,5]?  9 - 5 = 4 ≠ 2  ✗
                              but [1,5,9] with step 4 — length 3 ✓
```

**The same ending index supports several different sequences, one per step.** So `dp[i]` must record a length **for each possible difference**:

> **`dp[i][d]` = length of the longest arithmetic subsequence ending at index `i` with common difference `d`.`**

**The transition is then one line.** For every pair `j < i`, the difference `d = nums[i] - nums[j]` means index `i` can extend whatever ended at `j` with that same step:

```
dp[i][d] = dp[j][d] + 1
```

⚠️ **And if `j` has no entry for `d`, treat it as 1** — the single element `nums[j]` is a length-1 sequence, so adding `nums[i]` gives 2. That default is what seeds every new step value:

```python
dp[i][d] = dp[j].get(d, 1) + 1
```

**Why a dict per index rather than a 2-D array.** Differences range over −500..500, so a `1000 × 1001` array with an offset would work — but most cells stay empty. **A dict stores only the differences actually seen**, which is at most `i` per index.

**A subtlety worth noticing: later pairs overwrite earlier ones, and that's correct.** If two different `j` values give the same `d`, the *later* `j` is closer to `i` and has had more chances to build up, so `dp[j][d]` is at least as large. Assigning rather than taking a max is therefore safe — though `max` would also be correct and is the more defensive choice.

🤔 **Before you open the next section:** the answer is at least 2 whenever the array has two elements. What should `best` be initialised to, and why not 0 or 1?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Enumerate all subsequences | Check each | O(2ⁿ) | ❌ 2¹⁰⁰⁰ |
| For each difference, scan | Fix `d`, run an LIS-style pass | O(n·D) = 10⁶ | ✅ Works; D is the difference range |
| **`dp[i][d]` with a dict per index** | Pairwise transitions | **O(n²)** | ✅ |
| 2-D array with an offset | `dp[i][d + 500]` | O(n²), O(n·D) space | ✅ Faster constant, more memory |

**The decision: a list of dicts, `dp[i][d]`.**

**The whole algorithm is four lines:**

```python
dp = [{} for _ in range(len(nums))]
best = 2
for i in range(1, len(nums)):
    for j in range(i):
        d = nums[i] - nums[j]
        dp[i][d] = dp[j].get(d, 1) + 1
        best = max(best, dp[i][d])
```

**Why `.get(d, 1)` and not `.get(d, 0)`.** The default represents "`nums[j]` alone", which is a sequence of length **1**. Adding `nums[i]` makes 2 — correct. With a default of 0 you'd get 1, undercounting every pair by one.

⚠️ **Why `best` starts at 2, not 0.** The constraints guarantee `n >= 2`, and *any* two elements form an arithmetic subsequence. Starting at 0 would still work here because the loop always runs at least once for `n >= 2` — but starting at 2 states the invariant plainly and is robust if the constraint changed.

**The alternative worth knowing — fix the difference, then scan:**

```python
for d in range(-500, 501):
    # one pass computing the longest chain with step exactly d
```

**O(n·D)** where D = 1001 differences. At n = 1000 that's 10⁶ — comparable to O(n²) here, and **better when the array is long but the value range is narrow**. The dict version is better when values are spread out. Worth naming as the trade.

**Why the dict beats a 2-D array in practice**, even though both are O(n²) time:

| | Dict per index | 2-D array with offset |
|---|---|---|
| Space | **O(n²) worst, sparse in practice** | O(n·D) = 1000 × 1001 = **10⁶ always** |
| Lookup | hash | array index (faster constant) |
| Handles unbounded values | ✅ | ❌ needs a known range |

⚠️ **The array version depends on the `0 <= nums[i] <= 500` constraint.** If values could be arbitrary integers, the offset trick collapses and the dict is the only option. **Say that** — it shows you noticed which constraint you're leaning on.

**Why not the LIS patience-sorting trick** (O(n log n))? It works because "increasing" is a *total order* you can binary-search. "Arithmetic with step d" is a different relation for each d, so there's no single ordering to search. **O(n²) is the standard bound here.**

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
dp = [{} for _ in range(len(nums))]
best = 2
```

**One dict per index**, mapping a difference to the best length ending there with that difference.

⚠️ `[{} for _ in range(n)]` — **never `[{}] * n`**, which would make every index share **one** dict, so all differences would collide across indices. A classic aliasing bug, and unlike the list version it's easy to miss because dicts print the same either way.

`best = 2` because any two elements qualify.
→ [list-comprehension](../syntax/list-comprehension.md) · [dict-basics](../syntax/dict-basics.md)

```python
for i in range(1, len(nums)):
    for j in range(i):
```

**Every pair `j < i`.** Starting `i` at 1 because index 0 has no earlier partner.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md)

```python
        d = nums[i] - nums[j]
```

**The step implied by this pair.** ⚠️ Can be **negative** (Example 3's −5) or **zero** (repeated values, giving a constant sequence). Both are valid, and using `abs()` here would be wrong.

```python
        dp[i][d] = dp[j].get(d, 1) + 1
```

**The transition, and the line the problem turns on.**

| Part | Meaning |
|---|---|
| `dp[j].get(d, 1)` | longest run ending at `j` with step `d`; **default 1** = just `nums[j]` |
| `+ 1` | append `nums[i]` |
| `dp[i][d] =` | record it for index `i` |

**Assignment rather than `max` is safe** because a later `j` with the same `d` always has a value at least as large — it sits closer to `i` with more room to have grown. `max(dp[i].get(d, 0), ...)` would also be correct and is more defensive.
→ [dict-methods](../syntax/dict-methods.md)

```python
        best = max(best, dp[i][d])
```

**Track the global maximum** — the answer can end at any index with any step, so it must be sampled at every update rather than read off the last entry.
→ [min-max-key](../syntax/min-max-key.md)

```python
return best
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def longestArithSeqLength(self, nums: List[int]) -> int:

        dp = [{} for _ in range(len(nums))]
        best = 2

        for i in range(1, len(nums)):
            for j in range(i):
                d = nums[i] - nums[j]
                dp[i][d] = dp[j].get(d, 1) + 1
                best = max(best, dp[i][d])

        return best
```

</details>

**Trace it** — `nums = [9,4,7,2,10]`, expected **3**. Verified output:

| `i` (value) | `j` (value) | `d` | `dp[j].get(d,1)` | `dp[i][d]` | `best` |
|---|---|---|---|---|---|
| 1 (4) | 0 (9) | −5 | 1 | 2 | 2 |
| 2 (7) | 0 (9) | −2 | 1 | 2 | 2 |
| 2 (7) | 1 (4) | **3** | 1 | **2** | 2 |
| 3 (2) | 0 (9) | −7 | 1 | 2 | 2 |
| 3 (2) | 1 (4) | −2 | 1 | 2 | 2 |
| 3 (2) | 2 (7) | −5 | 1 | 2 | 2 |
| 4 (10) | 0 (9) | 1 | 1 | 2 | 2 |
| 4 (10) | 1 (4) | 6 | 1 | 2 | 2 |
| 4 (10) | 2 (7) | **3** | **2** ⚠️ | **3** | **3** |
| 4 (10) | 3 (2) | 8 | 1 | 2 | 3 |

**Answer: 3** ✅ — the subsequence `[4, 7, 10]`.

**The ⚠️ row is the only place the DP does real work.** Every other row falls back to the default of 1 and produces a length-2 pair. Here, `dp[2]` already knows that a step of 3 reaches index 2 with length 2 (from the earlier `4 → 7` row), so appending 10 extends it to **3**.

**Trace the chain across the two bold rows:**

```
i=2, j=1:  7 − 4 = 3   →  dp[2][3] = 2      the pair [4,7]
i=4, j=2:  10 − 7 = 3  →  dp[4][3] = dp[2][3] + 1 = 3   →  [4,7,10] ✅
```

**Note that index 0 (value 9) is skipped entirely** in the winning chain — that's what "subsequence" buys you. The elements 4, 7, 10 sit at indices 1, 2, 4, with index 3 (value 2) jumped over.

**Example 3** (`[20,1,15,3,10,5,8]`) finds `[20,15,10,5]` with `d = −5`, at indices 0, 2, 4, 5 — **the negative step is essential**, and taking `abs(d)` would break it.

**A zero-step case:** `nums = [7,7,7]` gives `d = 0` throughout, so `dp[2][0] = 3` — a constant sequence is arithmetic, with difference 0.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n²)</summary>

**O(n²)**.

| Component | Cost |
|---|---|
| Outer loop | **n** iterations |
| Inner loop at `i` | **i** pairs → O(n) |
| Work per pair | **O(1)** — one subtraction, one dict get, one dict set |
| **Total** | **O(n²)** |

At n = 1000 that's `1000²/2 = 500,000` pairs. Fast.

**Every pair is examined exactly once**, and each contributes one dict operation. Dict access is O(1) average, so the constant is small — though hashing makes it larger than array indexing.

**Versus the fix-the-difference approach**, O(n·D) where D = 1001 possible differences: at n = 1000 that's 10⁶ — **twice this**, but it scales differently:

| | Dict DP | Fix the difference |
|---|---|---|
| Complexity | **O(n²)** | **O(n·D)** |
| n = 1000, D = 1001 | 5 × 10⁵ | 10⁶ |
| n = 10⁵, D = 1001 | ⚠️ 5 × 10⁹ | ✅ 10⁸ |
| Unbounded values | ✅ works | ❌ D is infinite |

**Which wins depends on whether n or D is larger** — a good thing to state rather than declaring one universally better.

**Why there's no O(n log n) trick**, unlike [Longest Increasing Subsequence](300-longest-increasing-subsequence.md): patience sorting works because "increasing" is a single total order that binary search can navigate. Here each difference defines its own independent chain relation, so there's nothing to binary-search over. **O(n²) is the expected bound.**

**Versus brute force:** 2¹⁰⁰⁰ subsequences. The DP works because the answer decomposes by (ending index, difference) — a state space of size O(n²) rather than 2ⁿ.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n²) worst case</summary>

**O(n²)** in the worst case.

| Component | Size |
|---|---|
| `dp[i]` | up to `i` distinct differences → **O(n)** per index |
| Total across all indices | **O(n²)** |

At n = 1000 that's up to 500,000 dict entries — **a few tens of megabytes in Python**, which is the real cost of this solution.

**When is it actually O(n²)?** When every pair produces a distinct difference — e.g. values spread widely apart. ⚠️ **But here `0 <= nums[i] <= 500`, so there are only 1001 possible differences**, capping each `dp[i]` at 1001 entries:

```
worst case in general:  O(n²)          = 10⁶ entries
worst case here:        O(n · 1001)    = 10⁶ entries
```

**They coincide at n = 1000** — the constraint is chosen so neither bound dominates.

**The 2-D array alternative** uses O(n·D) = 1000 × 1001 = 10⁶ **always**, allocated up front:

| | Space | Constant factor |
|---|---|---|
| Dicts | O(n²) worst, **sparse in practice** | heavier per entry (hashing) |
| 2-D array | **O(n·D) always** | lighter per entry |

**Dicts win when the data is sparse; the array wins on constant factor when it's dense.** At these constraints either is fine.

**Can it be reduced?** Not meaningfully — you genuinely need a length per (index, difference) pair, and both dimensions are needed. **This is a case where O(n²) space is inherent to the state**, unlike the 1-D DPs in this unit that reduce to O(n) or O(1).

**No recursion** — iterative, so no stack concern.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Unlike Longest Increasing Subsequence, the ending index alone isn't a sufficient state here — the same index can end many different arithmetic sequences, one for each step size. So the state is (ending index, common difference), and I keep a dict per index mapping a difference to the best length ending there with that step. For every pair j < i, the difference is `nums[i] - nums[j]`, and index i extends whatever ended at j with that same difference: `dp[i][d] = dp[j].get(d, 1) + 1`. The default of 1 matters — it represents `nums[j]` on its own, so a fresh pair correctly gets length 2. Differences can be negative or zero, so no absolute values. O(n²) time and O(n²) space in the worst case. There's no O(n log n) trick like patience sorting for LIS, because that relies on a single total order and here every difference defines its own chain. If n were much larger but the value range stayed small, I'd flip it around and iterate over the 1001 possible differences instead, which is O(n·D)."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why isn't the index alone enough state?" | **The question.** One index can end several sequences with different steps — `[1,3,5]` step 2 and `[1,5,9]` step 4 both matter. The difference must be part of the state. |
| "Why `.get(d, 1)` and not `.get(d, 0)`?" | The default means "`nums[j]` alone", a length-1 sequence. Adding `nums[i]` gives 2. A default of 0 undercounts every pair. |
| "Can the difference be negative or zero?" | Yes — Example 3 uses −5, and repeated values give 0. Never take `abs()`. |
| "Why not O(n log n) like [LIS](300-longest-increasing-subsequence.md)?" | Patience sorting needs one total order to binary-search. Each difference defines a separate relation, so there's nothing to search. |
| "Dict or 2-D array?" | Both O(n²) time. Array is O(n·D) space always with a better constant but needs a bounded value range; dicts are sparse and handle unbounded values. |
| "n = 10⁵ with the same value range?" | Flip the loops — iterate over the 1001 differences, one O(n) pass each. O(n·D) = 10⁸ beats O(n²) = 10¹⁰. |
| "Return the actual subsequence?" | Store a predecessor index alongside each length and walk back from the best (index, difference). |
| "Longest **geometric** subsequence?" | Same shape with ratios instead of differences — ⚠️ but watch zeros and use exact fractions, since float ratios collide. |
| "Why is `best` initialised to 2?" | Any two elements form an arithmetic subsequence, and `n >= 2` is guaranteed. |

**Traps:**

- **`[{}] * n`** — every index shares one dict, so differences collide across indices. **Silent and hard to spot.**
- **Using `abs(nums[i] - nums[j])`** — merges steps of +5 and −5, giving wrong answers on Example 3.
- **Defaulting to 0 instead of 1** — every length comes out one short.
- **Only tracking `dp[i]` as a single number** — the LIS state, insufficient here.
- **Forgetting that `d = 0` is valid** — `[7,7,7]` is a length-3 arithmetic subsequence.
- **Returning `dp[n-1]`'s max** — the best sequence can end anywhere, not necessarily at the last index.
- **Initialising `best = 0`** — works only because the loop always runs; 2 states the invariant.
- **Requiring contiguity** — it's a subsequence, so gaps are allowed.

**This same move shows up in:** [Longest Increasing Subsequence](300-longest-increasing-subsequence.md) (the same "best ending at i" shape, with a simpler state) · [Two Sum](1-two-sum.md) (a dict keyed on a computed difference) · [dynamic-programming](../algorithms/dynamic-programming.md) · [hashmap](../data-structures/hashmap.md).

</details>

---
