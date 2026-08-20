# 435. Non-overlapping Intervals

**Medium** · [LeetCode](https://leetcode.com/problems/non-overlapping-intervals/)

[📖 17. Intervals lesson](../learning/17-intervals.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 17. Intervals problems](../rmap-practice/17-intervals.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Given an array of `intervals`, return the **minimum number of intervals you need to remove** so that the rest are non-overlapping.

```
intervals = [[1,2],[2,3],[3,4],[1,3]]   →  1
        remove [1,3] and the rest don't overlap

intervals = [[1,2],[1,2],[1,2]]         →  2
        keep one, remove the other two

intervals = [[1,2],[2,3]]               →  0
        touching at a point is NOT overlapping here
```

**Constraints:** `1 <= intervals.length <= 10⁵` · `intervals[i].length == 2` · `-5 × 10⁴ <= start_i < end_i <= 5 × 10⁴`.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**minimum** number to remove" | Minimizing removals is the same as **maximizing keeps**. Flip it — the maximization is the version with a known greedy |
| "so the rest are **non-overlapping**" | You're selecting a mutually compatible subset. This is the **activity selection problem**, one of the classic greedy results |
| `[1,2]` and `[2,3]` are fine | Touching at a point does **not** count as overlapping here. So the test is `start >= prev_end`, using `>=` |
| input order unspecified | Arbitrary order, so sorting is coming — the only question is *by what* |
| `n <= 10⁵` | n² = 10¹⁰ is dead. **O(n log n)**, which again points at a sort |

**Reframe it first.** "Remove the fewest" is awkward to reason about directly. But every interval is either kept or removed, so:

```
removals = n − (maximum number of mutually non-overlapping intervals you can keep)
```

Maximizing keeps is the standard framing, and it has a clean greedy answer. (The code below counts removals directly, but the *justification* runs through the maximization.)

**Now, which interval should you keep first?** Three candidate rules:

- **Earliest start?** No. One interval could start at 0 and run to 1000, blocking everything.
- **Shortest?** Tempting, and wrong. A short interval in the middle can conflict with two intervals that don't conflict with each other, costing you a keep.
- **Earliest end?** **Yes.** Among all intervals, the one that finishes soonest leaves the **maximum possible room** for everything after it.

That's the activity-selection greedy, and the intuition is worth stating plainly: **when choosing which meeting to attend, the one that ends soonest frees your calendar earliest.** Nothing about its start or length matters — only when it releases the timeline.

So: sort by **end**, then sweep left to right keeping any interval that starts at or after the last kept interval's end. Everything else must be removed.

🤔 **Before you open the next section:** [Merge Intervals](56-merge-intervals.md) sorts by **start** and this one sorts by **end**. What's different about the two problems that flips the choice?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Try every subset | Check all 2ⁿ subsets for compatibility | **O(2ⁿ · n)** | O(n) | ❌ |
| DP after sorting | `dp[i]` = most keeps ending at `i`, scanning back for compatible predecessors | O(n²) | O(n) | ⚠️ Correct — it's weighted interval scheduling — but unnecessary when all weights are equal |
| Sort by **start**, greedily keep | Keep the earliest-starting compatible interval | O(n log n) | O(1) | ❌ **Wrong.** A long early interval blocks many short later ones |
| Sort by **length**, keep shortest | Prefer short intervals | O(n log n) | O(1) | ❌ Also wrong — a short middle interval can block two compatible neighbours |
| **Sort by end, greedily keep** | Keep any interval starting at/after the last kept end | **O(n log n)** | **O(1)** | ✅ |

**The decision:** **sort by end time, then one greedy pass** — the activity selection algorithm.

**Why earliest-end is provably optimal.** This deserves a real argument, since it's the whole problem. Use an **exchange argument**:

Let `G` be the interval with the earliest end, and let `OPT` be any optimal solution that does *not* include `G`. Let `f` be the first interval in `OPT` by end time. Since `G` ends no later than `f`, swapping `f` for `G` in `OPT` keeps everything compatible — `G` finishes at or before `f` did, so it can't conflict with anything that came after `f`. The swapped solution has the **same size** and includes `G`.

So there's always an optimal solution containing the earliest-ending interval. Take it, discard everything it conflicts with, and repeat on the remainder. **Greedy is safe at every step.**

**Why sorting by start fails**, concretely: `[[1,100],[2,3],[4,5]]`. Sorted by start, the greedy takes `[1,100]` first and then nothing else fits — 1 keep, 2 removals. Sorting by end takes `[2,3]` and `[4,5]` — 2 keeps, 1 removal. **One long interval poisons the start-sorted greedy.**

**Why sorting by length fails:** `[[1,4],[3,6],[5,8]]`. Shortest-first picks `[3,6]` (length 3), which blocks both others — 1 keep. Earliest-end picks `[1,4]` then `[5,8]` — 2 keeps.

**Why sort by *end* here but by *start* in [Merge Intervals](56-merge-intervals.md)?** — the answer to section 1's question. The two problems want different things:

| Problem type | Sort by | Why |
|---|---|---|
| **Grouping / merging** ([56](56-merge-intervals.md), [57](57-insert-interval.md), [252](252-meeting-rooms.md)) | **start** | You need overlapping intervals to be *adjacent* so one pass can collect them |
| **Selection / scheduling** (this, activity selection) | **end** | You need whichever interval *frees the timeline soonest*, to leave maximum room |

**That table is the single most useful thing to carry out of this unit.**

**Why not the O(n²) DP?** It solves a strictly harder problem — weighted interval scheduling, where intervals have values and you maximize total value. That genuinely needs DP. Here every interval is worth the same, and equal weights are exactly the condition under which the greedy becomes optimal.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
intervals.sort(key=lambda interval: interval[1])
```
**Sort by end time** — `interval[1]`, not `interval[0]`. This one index is the entire algorithm; sorting by start gives a wrong answer, not a slower one.

The [`lambda`](../syntax/lambda-functions.md) extracts the end as the sort key. `.sort()` works in place, avoiding an O(n) copy.
→ [sorting-key](../syntax/sorting-key.md) · [lambda-functions](../syntax/lambda-functions.md) · [list-methods](../syntax/list-methods.md)

```python
removed = 0
prev_end = float("-inf")
```
- **`removed`** — the running count of intervals discarded.
- **`prev_end`** — when the last *kept* interval finished. Everything kept from here must start at or after it.

Seeding with [`float("-inf")`](../syntax/float-inf.md) means the first interval is always compatible, since any start exceeds negative infinity. That's cleaner than special-casing the first iteration — and it matters because starts can be negative (down to −5 × 10⁴), so seeding with `0` would be a genuine bug rather than a stylistic one.
→ [float-inf](../syntax/float-inf.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
for start, end in intervals:
```
One pass in end-sorted order. [Tuple unpacking](../syntax/tuple-unpacking.md) names the two components directly, which keeps the comparison below readable.
→ [for-loop](../syntax/for-loop.md) · [tuple-unpacking](../syntax/tuple-unpacking.md)

```python
    if start >= prev_end:
        prev_end = end
```
**Keep it.** This interval starts at or after the last kept one finished, so they don't overlap — and because the list is end-sorted, this is the earliest-ending interval among everything still compatible. The greedy says take it.

`>=` and not `>`, because touching at a point isn't an overlap in this problem: `[1,2]` and `[2,3]` may both be kept.

Updating `prev_end = end` advances the frontier. Note there's no `max` here — unlike [Merge Intervals](56-merge-intervals.md) — because the end-sorted order guarantees `end >= prev_end` already.
→ [comparison-operators](../syntax/comparison-operators.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
    else:
        removed += 1
```
**Remove it.** It overlaps the interval already kept, and since that one ends **no later** than this one (end-sorted order), keeping this instead could never help — it would block at least as much of the future.

So `prev_end` is deliberately **left unchanged**: the kept interval remains the frontier, and the removed one is simply discarded. **That's the greedy choice, and it's never revisited.**
→ [elif-else](../syntax/elif-else.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
return removed
```
The count of intervals discarded, which by construction is the minimum.
→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:

        intervals.sort(key=lambda interval: interval[1])
        removed = 0
        prev_end = float("-inf")

        for start, end in intervals:
            if start >= prev_end:
                prev_end = end
            else:
                removed += 1

        return removed
```
</details>

**Trace it** — `intervals = [[1,2],[2,3],[3,4],[1,3]]`

Sorted by end: `[[1,2], [1,3], [2,3], [3,4]]` (ends 2, 3, 3, 4)

| interval | `start >= prev_end`? | action | `prev_end` after | `removed` |
|---|---|---|---|---|
| `[1,2]` | 1 ≥ −∞ ✓ | **keep** | **2** | 0 |
| `[1,3]` | 1 ≥ 2 ✗ | **remove** | 2 | **1** |
| `[2,3]` | 2 ≥ 2 ✓ | **keep** | **3** | 1 |
| `[3,4]` | 3 ≥ 3 ✓ | **keep** | **4** | 1 |

Return **1** ✅ — `[1,3]` is the one removed.

Two rows are instructive. **`[1,3]`** is removed even though it comes before `[2,3]` in start order — it overlaps the already-kept `[1,2]`, and since it ends *later*, keeping it instead would have blocked `[2,3]` as well. **Row 3** shows the `>=`: `[2,3]` starts exactly where `[1,2]` ends, and that's compatible here.

**And the start-sort counterexample** — `intervals = [[1,100],[2,3],[4,5]]`:

Sorted by **end**: `[[2,3], [4,5], [1,100]]`

| interval | `start >= prev_end`? | action | `prev_end` | `removed` |
|---|---|---|---|---|
| `[2,3]` | 2 ≥ −∞ ✓ | keep | 3 | 0 |
| `[4,5]` | 4 ≥ 3 ✓ | keep | 5 | 0 |
| `[1,100]` | 1 ≥ 5 ✗ | **remove** | 5 | **1** |

Return **1** ✅ — two keeps.

Now the same input sorted by **start**: `[[1,100], [2,3], [4,5]]`. The greedy would keep `[1,100]` first (frontier → 100), then remove both `[2,3]` and `[4,5]` — returning **2**. **Wrong**, and it's exactly the failure mode the end-sort avoids: one long interval consumed the whole timeline.

**And the duplicates case** — `intervals = [[1,2],[1,2],[1,2]]`: sorted order is unchanged. The first is kept (`prev_end` → 2), then the second and third both fail `1 >= 2` and are removed. Return **2** ✅.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n log n)</summary>

**O(n log n)**, dominated by the sort.

- **`intervals.sort()`** — comparison sort on n items → **O(n log n)**. The bottleneck.
- **The greedy scan** — one iteration per interval, each doing a comparison and one assignment → **O(n)**.
- O(n log n) + O(n) = **O(n log n)**.

At n = 10⁵ that's roughly 10⁵ × 17 ≈ 1.7 × 10⁶ comparisons. Fast.

**As with [Merge Intervals](56-merge-intervals.md), the interesting work is linear and the sorting is what costs.** That's characteristic of this whole unit: interval problems are usually "sort, then sweep," and the sweep is almost always O(n).

**Against the alternatives:** the subset enumeration is O(2ⁿ). The DP is **O(n²)** — for each interval, scan backwards for the best compatible predecessor. That DP is *necessary* if intervals carry weights (weighted interval scheduling, solvable in O(n log n) with binary search over predecessors), but here all weights are equal and the greedy wins outright.

**Can you beat O(n log n)?** Not by comparison sorting. Coordinates are bounded by ±5 × 10⁴, so a counting or radix sort on the end values would give **O(n + k)** — linear for these constraints. Worth naming; not worth writing.

**If the input arrived already sorted by end**, the whole thing would be **O(n)**.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** auxiliary — two variables, `removed` and `prev_end`. No result list is built, because the answer is a single count rather than the intervals themselves.

| Component | Space | Why |
|---|---|---|
| `removed`, `prev_end` | **O(1)** | Two scalars |
| Python's `.sort()` (Timsort) | **O(n)** worst case | Temporary storage for merging runs |

So: **O(1) beyond the sort**, or O(n) if you count Timsort's working memory. Stating the convention is what matters.

**Why this is leaner than [Merge Intervals](56-merge-intervals.md)**, which is O(n): that problem must *return the merged intervals*, so an output list of up to n entries is unavoidable. Here the question asks only "how many," so nothing accumulates. **When a problem asks for a count rather than the objects, the space usually collapses to O(1)** — the same reason [Palindromic Substrings](647-palindromic-substrings.md) is O(1) while [Longest Palindromic Substring](5-longest-palindromic-substring.md) builds strings.

**If you needed the kept intervals**, you'd append them in the `if` branch — O(n) output, same time.

**A side effect worth flagging:** `.sort()` mutates the caller's array. Use `sorted(intervals, key=...)` if the input must be preserved, at the cost of an O(n) copy.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Minimizing removals is the same as maximizing how many I keep, which is the classic activity-selection problem. The greedy is to always keep the interval that **ends earliest**, because that leaves the most room for everything after it. I can justify it with an exchange argument: if some optimal solution doesn't include the earliest-ending interval, I can swap it in for that solution's first interval without breaking compatibility, and the size doesn't change — so an optimal solution containing it always exists. So I sort by end time and sweep, keeping any interval that starts at or after the last kept one's end and counting the rest as removals. The comparison is `>=` because touching at a point isn't an overlap here. O(n log n) from the sort, O(1) extra space. And note this is why interval problems split into two families: sort by *start* when you're merging or grouping, sort by *end* when you're selecting or scheduling."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why sort by end and not start?" | Sorting by start fails on `[[1,100],[2,3],[4,5]]` — the greedy takes the long interval and blocks everything. Earliest-end always frees the timeline soonest. |
| "Prove the greedy is optimal." | Exchange argument: given any optimal solution excluding the earliest-ending interval `G`, swap `G` in for that solution's first interval. `G` ends no later, so compatibility is preserved and the size is unchanged. |
| "Why not keep the shortest interval?" | `[[1,4],[3,6],[5,8]]` — shortest-first picks `[3,6]`, blocking both others for 1 keep; earliest-end gets 2. |
| "Why `>=` and not `>`?" | This problem states that intervals touching at a point don't overlap, so `[1,2]` and `[2,3]` can both be kept. |
| "What if intervals had weights?" | Then greedy fails and you need weighted interval scheduling: sort by end, and `dp[i] = max(dp[i-1], weight[i] + dp[predecessor])`, with the predecessor found by binary search. O(n log n). |
| "Return the kept intervals, not the count." | Append in the `if` branch. O(n) output space, same time. |
| "What if you wanted the minimum removals to make them *all* overlap at a point?" | Different problem entirely — that's about finding the point covered by the most intervals, which is [Meeting Rooms II](253-meeting-rooms-ii.md)'s machinery. |
| "Can you beat O(n log n)?" | Not with comparison sorting. Coordinates are bounded, so counting/radix sort on ends gives O(n + k). |

**Traps:**
- **Sorting by start instead of end.** The defining error — it produces a plausible wrong answer rather than a crash.
- **Using `>` instead of `>=`.** Counts touching intervals as overlapping and over-removes.
- **Seeding `prev_end = 0`.** Starts can be negative here (down to −5 × 10⁴), so a `0` seed wrongly rejects early intervals. `float("-inf")` is required, not stylistic.
- Updating `prev_end` in the `else` branch. The removed interval must not become the frontier — that's the greedy choice being thrown away.
- Adding a `max` when updating `prev_end`. Harmless but pointless: end-sorted order already guarantees the new end is larger.
- Reaching for DP by reflex. Correct but O(n²), and it solves a harder problem than the one asked.

**This same move shows up in:** [Merge Intervals](56-merge-intervals.md) (sorted by *start*, because grouping needs overlapping intervals adjacent — the contrast that defines this unit) · [Meeting Rooms](252-meeting-rooms.md) (sorted intervals scanned once for any conflict) · [Meeting Rooms II](253-meeting-rooms-ii.md) (counting simultaneous overlaps rather than selecting a compatible subset) · [Hand of Straights](846-hand-of-straights.md) (processing in sorted order so each greedy decision is forced) · [Jump Game](55-jump-game.md) (a greedy justified by an exchange argument, with O(1) state).

</details>

---
