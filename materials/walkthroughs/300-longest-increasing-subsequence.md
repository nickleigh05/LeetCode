# 300. Longest Increasing Subsequence

**Medium** · [LeetCode](https://leetcode.com/problems/longest-increasing-subsequence/)

[📖 13. 1-D Dynamic Programming lesson](../learning/14-dp-1d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 13. 1-D Dynamic Programming problems](../rmap-practice/13-dp-1d.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Given an integer array `nums`, return the **length** of the longest **strictly increasing subsequence**. A subsequence is derived by deleting some or no elements **without changing the order** of the remaining ones.

```
nums = [10,9,2,5,3,7,101,18]   →  4      [2,3,7,101]
nums = [0,1,0,3,2,3]           →  4      [0,1,2,3]
nums = [7,7,7,7,7]             →  1      strictly increasing, so equal values don't extend
```

**Constraints:** `1 <= nums.length <= 2500` · `-10⁴ <= nums[i] <= 10⁴`.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**subsequence**", not substring | **Non-contiguous.** You may skip freely, so there are 2ⁿ candidates — far more than the O(n²) substrings in [Longest Palindromic Substring](5-longest-palindromic-substring.md) |
| "without changing the order" | Relative order is fixed. You're choosing *which* elements, never rearranging them |
| "**strictly** increasing" | Equal values don't extend a sequence. `[7,7,7]` has an LIS of 1 — this decides `bisect_left` vs `bisect_right` later, and it's the whole difference |
| "return the **length**" | You don't have to produce the sequence itself. That's a real simplification, and it's what makes the fast approach possible |
| `n <= 2500` | n² = 6.25 × 10⁶ — **passes**. So O(n²) is acceptable here, and O(n log n) is the stretch answer rather than a requirement |

The classic DP framing: let `dp[i]` = the length of the longest increasing subsequence **ending at index `i`**. Then

```
dp[i] = 1 + max( dp[j] for all j < i where nums[j] < nums[i] )
```

— look back at every earlier element you could have extended from, take the best. The answer is `max(dp)`. That's O(n²), it's correct, and it's the version you should be able to produce immediately.

But there's a second way to see the problem that leads somewhere much faster, and it starts from a question about **greedy**:

If you're building an increasing subsequence of some length, and you have a choice of what its last element should be, **which is better — a smaller tail or a larger one?** A smaller tail is strictly more useful, because anything that can extend a large tail can also extend a small one. So for each possible *length*, you only ever care about the **smallest tail achievable at that length**.

Keep an array of those smallest tails, one per length. That array turns out to be **sorted** — which means binary search applies.

🤔 **Before you open the next section:** if `tails[k]` is the smallest possible last element of an increasing subsequence of length `k+1`, why must `tails` be sorted in increasing order? What would a longer subsequence with a *smaller* tail imply about the shorter ones?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Every subsequence | Generate all 2ⁿ, check each | O(2ⁿ · n) | O(n) | ❌ |
| Classic DP | `dp[i] = 1 + max(dp[j])` for valid `j < i` | O(n²) | O(n) | ⚠️ Correct, passes at n = 2500, and the version to have ready. But quadratic |
| Longest common subsequence with `sorted(nums)` | LIS = LCS of the array and its sorted, deduplicated self | O(n²) | O(n²) | ❌ Same time, far worse space, and needs the dedup subtlety to be right |
| **Patience sorting / tails + binary search** | Keep the smallest tail per length; binary search each element into place | **O(n log n)** | O(n) | ✅ |

**The decision:** the **tails array with binary search** — O(n log n), and about six lines.

**Why the greedy "smallest tail" idea is valid.** For a subsequence of a given length, a smaller final element dominates a larger one: every future element that could extend the larger tail can also extend the smaller, and some can extend only the smaller. There's never a reason to prefer a bigger tail. So for each length you keep exactly one number — the minimum achievable tail — and nothing is lost.

**Why `tails` is sorted** (the question from section 1). Suppose you have an increasing subsequence of length `k+1` ending at value `v`. Chop off its last element and you have one of length `k` ending at something **strictly less than `v`**. So the smallest tail at length `k` is at most that, which is `< v` — hence `tails[k-1] < tails[k]` always. The array is sorted **as a consequence of the problem's structure**, not by construction. That's what licenses the binary search, and it's the crux of the whole approach.

**What each element does when it arrives.** Binary search for its position in `tails`:
- It's **larger than everything** → it extends the longest subsequence found so far → **append**, and the LIS length grows by one.
- It **fits somewhere in the middle** → it's a *better* (smaller) tail for that length → **overwrite** that slot. The LIS length doesn't change, but future elements now have an easier target.

**The critical warning: `tails` is not the LIS.** It has the right *length*, but its contents may not be an actual subsequence of `nums`. On `[10, 9, 2, 5, 3, 7, 101, 18]` it ends as `[2, 3, 7, 18]` — and `18` comes *after* `101` in the input, so `[2,3,7,18]` happens to be valid here, but in general the overwrites can leave a mix of values from incompatible subsequences. **Only `len(tails)` is meaningful.** Claiming the array *is* the answer is the classic overreach on this problem.

**Why `bisect_left`, not `bisect_right`.** This is where "strictly increasing" gets enforced. `bisect_left` returns the position of the first element **≥** `num`, so an equal value **overwrites** rather than appends — `[7,7,7]` correctly gives 1. Using `bisect_right` would append duplicates and solve the *non-decreasing* version instead. One function name is the entire difference between the two problems.

**Why not skip straight to O(n²)?** You can — it passes. But LIS is the canonical place where the n log n solution is expected, and the reasoning (greedy on tails + binary search) is more interesting than the DP. Mention the O(n²) as your baseline, then improve it.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
import bisect
```
The standard-library [binary search](../syntax/bisect-module.md) on a sorted list. `bisect_left(a, x)` returns the leftmost index where `x` could be inserted while keeping `a` sorted — in O(log n), without writing the loop yourself.
→ [bisect-module](../syntax/bisect-module.md) · [import-basics](../syntax/import-basics.md) · [binary-search](../algorithms/binary-search.md)

```python
tails = []
```
`tails[k]` will hold **the smallest possible last value of an increasing subsequence of length `k+1`**.

Read that definition twice — it's doing all the work, and every line below is a direct consequence of it. Two properties follow: the array stays **sorted** (proved in section 2), and its **length is the current LIS length**.
→ [list-basics](../syntax/list-basics.md)

```python
for num in nums:
```
One pass, left to right. Order matters — processing in input order is what guarantees every value in `tails` came from an earlier index than the one being placed.
→ [for-loop](../syntax/for-loop.md)

```python
    pos = bisect.bisect_left(tails, num)
```
**Binary search for where `num` belongs** — the first index whose value is **≥ `num`**.

`bisect_left` rather than `bisect_right` is what enforces **strict** increase: if `num` equals an existing tail, `bisect_left` points *at* it so `num` replaces it rather than extending past it. That's why `[7,7,7,7,7]` returns 1. Swap in `bisect_right` and you'd solve "longest non-decreasing subsequence" instead — a silent, plausible-looking wrong answer.

O(log n) per element, and this is where the whole speedup lives: the classic DP scans all earlier entries in O(n); the sortedness of `tails` replaces that scan with a search.
→ [bisect-module](../syntax/bisect-module.md) · [binary-search](../algorithms/binary-search.md)

```python
    if pos == len(tails):
        tails.append(num)
```
**`num` is larger than every tail so far**, so it extends the longest subsequence found to date. Append it — the LIS length just grew by one.
→ [if-return](../syntax/if-return.md) · [list-methods](../syntax/list-methods.md)

```python
    else:
        tails[pos] = num
```
**`num` fits inside the existing range**, meaning it's a smaller (better) tail for a subsequence of length `pos + 1`. Overwrite that slot.

The length doesn't change here, but the array gets *more useful*: a lower tail at that length means more future elements can extend it. This is the greedy improvement step, and it's why elements that don't lengthen anything still matter.
→ [elif-else](../syntax/elif-else.md) · [list-basics](../syntax/list-basics.md)

```python
return len(tails)
```
The array holds one slot per achievable length, so its length **is** the LIS length. (Its *contents* are not necessarily an actual subsequence — see section 2.)
→ [if-return](../syntax/if-return.md) · [dynamic-programming](../algorithms/dynamic-programming.md)

<details>
<summary>The whole thing together</summary>

```python
import bisect

class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:

        tails = []

        for num in nums:
            pos = bisect.bisect_left(tails, num)
            if pos == len(tails):
                tails.append(num)
            else:
                tails[pos] = num

        return len(tails)
```
</details>

**Trace it** — `nums = [10, 9, 2, 5, 3, 7, 101, 18]`

| `num` | `bisect_left(tails, num)` | action | `tails` after |
|---|---|---|---|
| 10 | 0 == len(`[]`) | append | `[10]` |
| 9 | 0 (before 10) | **overwrite** slot 0 | `[9]` |
| 2 | 0 | **overwrite** slot 0 | `[2]` |
| 5 | 1 == len(`[2]`) | append | `[2, 5]` |
| 3 | 1 (before 5) | **overwrite** slot 1 | `[2, 3]` |
| 7 | 2 == len | append | `[2, 3, 7]` |
| 101 | 3 == len | append | `[2, 3, 7, 101]` |
| 18 | 3 (before 101) | **overwrite** slot 3 | `[2, 3, 7, 18]` |

Return `len(tails)` = **4** ✅ — matching `[2,3,7,101]`.

Two rows are worth pausing on.

**Row 5 (`3`)**: it doesn't lengthen anything — the LIS is still 2 — but it lowers the length-2 tail from 5 to 3. That pays off immediately at row 6, where `7` extends it. Had `tails` still read `[2,5]`, `7` would still have appended, but the principle holds in general: **a lower tail keeps more futures open.**

**Row 8 (`18`)**: it replaces `101` at length 4. The LIS length is unchanged, but if the array continued with, say, `20`, the improved tail would allow a length-5 subsequence. This is also the row that shows why `tails` isn't the LIS itself — the final `[2,3,7,18]` is assembled from what were, at various moments, different candidate subsequences.

**And `nums = [7,7,7,7,7]`:** the first `7` appends → `[7]`. Every subsequent `7` gets `bisect_left` = 0 (pointing *at* the equal value), so it overwrites slot 0 and the array never grows. Return **1** ✅ — `bisect_left` enforcing strictness.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n log n)</summary>

**O(n log n).**

- The loop runs **n** times, once per element.
- Each iteration does one `bisect_left` over `tails`, which holds at most n entries → **O(log n)**.
- The append or overwrite is **O(1)** — appending is amortized constant, and assigning to an existing index is genuinely constant.
- n × O(log n) = **O(n log n)**.

At n = 2500 that's ~2500 × 12 ≈ 30,000 operations. Effectively instant.

**Against the classic DP:** `dp[i] = 1 + max(dp[j] for j < i with nums[j] < nums[i])` scans every earlier index for every element → **O(n²)** = 6.25 × 10⁶ here. It passes, and it's a perfectly acceptable first answer. The improvement comes entirely from **`tails` being sorted**, which lets a binary search replace the linear scan — O(n) → O(log n) per element.

**Can you beat O(n log n)?** Not by comparisons. LIS is at least as hard as sorting under a comparison model, so **Ω(n log n)** is the lower bound. (With small integer values you could use a Fenwick tree over the value range for O(n log V) — a different bound, not a better one here.)

**A Python note:** `bisect` is implemented in C, so the constant factor is much better than a hand-written binary search loop. Writing your own is fine and shows you know the mechanics; using `bisect` shows you know the library.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** — `tails` holds at most one entry per achievable length, and the LIS can be as long as the whole array (a fully sorted input), so it can reach n entries.

Nothing else is allocated: `pos` and `num` are O(1), and `bisect` operates in place without copying.

| Approach | Space | Why |
|---|---|---|
| Classic DP | **O(n)** | The `dp` array, one length per index |
| LCS with sorted copy | **O(n²)** | A full 2-D table — much worse for the same time bound |
| **Tails + binary search** | **O(n)** | One slot per achievable subsequence length |

**Why this can't collapse to O(1)** the way [Climbing Stairs](70-climbing-stairs.md) and [House Robber](198-house-robber.md) did: those recurrences read a *fixed* two cells back. Here every incoming element may binary-search across the entire history of tails, so the full array must be retained. **The rolling-variable trick needs a bounded lookback window, and this problem has none.**

**What you'd need beyond this:** to return the actual subsequence, keep a parallel array recording each element's predecessor index and which `tails` slot it landed in, then walk backwards from the final one. That's another O(n) and it's the standard extension — necessary precisely because `tails` itself is not the answer.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The straightforward DP is `dp[i]` = length of the LIS ending at i, computed by scanning all earlier smaller elements — O(n²), and it passes at n = 2500. But there's a better way. For an increasing subsequence of a given length, a smaller final element is strictly more useful, since anything that extends a larger tail also extends a smaller one. So I keep an array where `tails[k]` is the smallest achievable tail for a subsequence of length k+1. That array is necessarily sorted — chop the last element off a length-k+1 subsequence and you get a length-k one with a smaller tail — which means I can binary search it. Each element either extends the longest sequence, so I append, or improves some existing tail, so I overwrite. I use `bisect_left` specifically because the problem says *strictly* increasing: an equal value overwrites instead of appending. O(n log n) time, O(n) space. One caveat — `tails` has the right length but isn't itself the LIS; reconstructing that needs predecessor pointers."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why is `tails` sorted?" | Remove the last element from an increasing subsequence of length k+1 and you have one of length k ending at a strictly smaller value. So the minimum tail at length k is strictly less than the minimum at k+1. Sortedness is a consequence of the structure. |
| "Is `tails` the actual LIS?" | No — only its *length* is meaningful. Overwrites can leave values from different candidate subsequences mixed together. To recover the real sequence, store predecessor indices and walk back. |
| "What if it were non-decreasing?" | Swap `bisect_left` for `bisect_right`. Then an equal value appends rather than overwrites. That one change is the whole difference. |
| "Return the actual subsequence." | Track, for each element, which `tails` index it occupied and which element preceded it, then reconstruct backwards from the last appended one. O(n) extra. |
| "Write the O(n²) version." | `dp = [1]*n`; for each `i`, for each `j < i` with `nums[j] < nums[i]`, `dp[i] = max(dp[i], dp[j]+1)`; return `max(dp)`. Simpler and it passes here. |
| "Longest *decreasing* subsequence?" | Negate every value and run the same code — or reverse the comparison. |
| "Can you beat O(n log n)?" | Not with comparisons — LIS is at least as hard as sorting, so Ω(n log n) is a lower bound. A Fenwick tree over the value range gives O(n log V), a different trade rather than a better bound. |
| "Explain the patience-sorting analogy." | Deal cards into piles, each card onto the leftmost pile whose top is ≥ it. The number of piles equals the LIS length, and `tails` is exactly the list of pile tops. |

**Traps:**
- **`bisect_right` instead of `bisect_left`.** Silently solves the non-decreasing version — `[7,7,7]` returns 3 instead of 1.
- **Claiming `tails` is the LIS.** It has the right length, not necessarily the right contents.
- Comparing `pos == len(tails)` incorrectly, e.g. `pos >= len(tails) - 1`, which appends when it should overwrite.
- Sorting the input. It destroys the order the problem is entirely about.
- Confusing subsequence with substring and reaching for a sliding window.
- Forgetting that `tails` starting empty means the first element always appends — no special case needed, but worth checking rather than assuming.

**This same move shows up in:** [Binary Search](704-binary-search.md) (the search primitive this depends on) · [Longest Common Subsequence](1143-longest-common-subsequence.md) (the 2-D subsequence DP — LIS is LCS with a sorted copy, though that's the worse solution here) · [Russian Doll Envelopes](https://leetcode.com/problems/russian-doll-envelopes/) (2-D LIS: sort by one dimension, run this on the other) · [Coin Change](322-coin-change.md) (a DP where the array genuinely can't collapse to rolling variables).

</details>

---
