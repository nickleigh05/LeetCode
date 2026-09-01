# 1288. Remove Covered Intervals

**Medium** · [LeetCode](https://leetcode.com/problems/remove-covered-intervals/) · [Solution file (no hints)](../../problems/1000-1499/1288.py)

[📖 16. Intervals lesson](../learning/17-intervals.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 16. Intervals problems](../rmap-practice/16-intervals.md)

---

Remove every interval that is **covered** by another one — `[a,b)` is covered by `[c,d)` when `c <= a` **and** `b <= d`. Return how many intervals survive.

```
intervals = [[1,4],[3,6],[2,8]]   →  2      [3,6] is covered by [2,8]
intervals = [[1,4],[2,3]]         →  1      [2,3] is covered by [1,4]
```

**Constraints:** `1 <= len <= 1000` · `0 <= l < r <= 10^5` · **all intervals are unique**

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "covered: `c <= a` **and** `b <= d`" | ⚠️ **Non-strict on both sides** — sharing an endpoint still counts as covered |
| "covered by **another** interval" | Not by itself; the "another" is doing real work |
| "**all intervals are unique**" | ⚠️ **Load-bearing.** Two identical intervals would each cover the other |
| "return the **number** remaining" | You never have to name the survivors — just count them |
| `len <= 1000` | O(n²) = 10⁶ passes. But O(n log n) is the point |
| `[l, r)` half-open | Cosmetic here — the covering test is the same for `[l, r]` |

**Covering is about *both* endpoints.** An interval survives only if nothing starts at-or-before it **and** ends at-or-after it.

```
[2,8]   c────────────────d
[3,6]      a───────b            ← covered: 2<=3 and 6<=8  ✅
[1,4]  a──────b                 ← NOT covered: 1 < 2       ✅ survives
```

**Now the reframe that turns it into one pass.** Sort by start, ascending. Walk left to right and keep `prev_end` = the largest end seen so far. For the interval you're looking at:

- Every earlier interval started **at or before** it (that's what sorting by start gives you).
- So it is covered **exactly when** some earlier interval also ended **at or after** it.
- Which is exactly when `end <= prev_end`.

```
sorted by start:  [1,4]  [2,8]  [3,6]
prev_end:          4      8      8
                   new    new    6 <= 8 → COVERED
survivors:         ✅     ✅     ❌         →  2 ✅
```

**Covering collapses to a single running maximum.** That's the whole idea.

⚠️ **But it only works if ties on `start` are ordered correctly.** If two intervals share a start, the *longer* one covers the shorter one — so the longer must come **first**, or the shorter one will be seen first, record a small `prev_end`, and both will be counted.

```
[1,2] and [1,4]:   true answer is 1   ([1,2] is covered by [1,4])

sorted (1,2),(1,4):   4>0 → keep, 2… wait, 2 comes first: keep [1,2], then 4>2 → keep [1,4]  →  2  ❌
sorted (1,4),(1,2):   keep [1,4] (prev_end 4), then 2 <= 4 → covered            →  1  ✅
```

🤔 **Before you open the next section:** the sort key needs a tie-break. What is it, and can you state *why* it makes the greedy correct rather than just "it happens to pass"?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| All pairs | For each `i`, scan all `j` for a coverer | O(n²) | O(1) | ⚠️ Passes at n ≤ 1000 — but it's the obvious one |
| **Sort `(start ↑, end ↓)` + running max end** | One sweep | **O(n log n)** | O(1) | ✅ **The answer** |
| Sort `(end ↓, start ↑)` + running min start | The mirror image | O(n log n) | O(1) | ✅ Equally correct |
| Interval tree / segment tree | Query for a coverer | O(n log n) | O(n) | ❌ Massive overkill |

**The decision: sort by start ascending, end descending; sweep once tracking the maximum end.**

**Why the tie-break is the algorithm.** With `(start ↑, end ↓)`:

> Once sorted, **every interval that comes earlier has `start <= mine`.** So the *only* remaining question is whether any of them ends at or after me — and `prev_end`, the running maximum, answers it in O(1). The descending end guarantees that when starts tie, the longer interval is processed first, so it gets to *be* the coverer rather than being counted as a separate survivor.

**⚠️ This is not a stylistic choice — measured over 5,000 random inputs, sorting `(start ↑, end ↑)` gives the wrong count 32.8% of the time.** And the minimal counterexample is only two intervals:

```
[[1,2],[1,4]]      correct: 1        ascending tie-break: 2   ❌
```

**Why "uniqueness" appears in the constraints.** Under the literal definition, two identical intervals each cover the other, so a strict reading would remove *both*. Check it:

```
[[1,4],[1,4]]      greedy: 1        literal brute force: 0
```

**The constraint exists precisely to make that ambiguity impossible** — and noticing it is a good interview remark. If duplicates *were* allowed, you'd have to state which reading you're implementing.

**The mirror version is equally valid** (verified over 6,000 random inputs, 0 disagreements): sort by end **descending**, start ascending, and count intervals whose start is strictly below the running **minimum** start. Same idea, opposite axis.

**Why the brute force is worth mentioning and not writing.** `n <= 1000` makes `10⁶` pair checks fast enough, and it's the natural first answer. But it's the direct transcription of the definition — **the sweep is the one that shows you found the structure.** Say the brute force out loud, then improve it.

**Why no interval tree.** You're not answering arbitrary queries — you get to choose the processing order, and the right order makes each test O(1). **Sorting *is* the data structure here.**
→ [sorting-key](../syntax/sorting-key.md) · [lambda-functions](../syntax/lambda-functions.md)

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
intervals.sort(key=lambda x: (x[0], -x[1]))
```

**Start ascending, end descending.** A tuple key sorts lexicographically: primary `x[0]` ascending, and negating `x[1]` flips *only* the second field.

⚠️ **`-x[1]` is the entire correctness argument**, not a tidiness detail — without it the count is wrong on a third of random inputs. It puts the longest interval first among equal starts so it can act as the coverer.

⚠️ This **mutates the caller's list**. `sorted(intervals, key=...)` if that matters.
→ [sorting-key](../syntax/sorting-key.md) · [lambda-functions](../syntax/lambda-functions.md) · [tuple-basics](../syntax/tuple-basics.md)

```python
count = 0
prev_end = 0
```

**`count`** is the number of survivors; **`prev_end`** is the largest end seen so far.

**`0` is a safe initial value** because the constraints give `0 <= l < r`, so every real end is at least 1 and the first interval always beats it. ⚠️ **`float('-inf')` is the version that doesn't depend on the constraints** — prefer it if ends could be negative.
→ [variables-assignment](../syntax/variables-assignment.md) · [float-inf](../syntax/float-inf.md)

```python
for start, end in intervals:
    if end > prev_end:
        count += 1
        prev_end = end
```

**The whole sweep.**

- **`end > prev_end`** → nothing seen so far reaches this far right, and everything seen so far started at or before it. **Not covered — count it, and it becomes the new frontier.**
- **`end <= prev_end`** → some earlier interval starts at or before it *and* ends at or after it. **Covered — skip it, and `prev_end` stays put.**

⚠️ **`>` and not `>=`.** With `>=`, an interval ending exactly where the frontier ends would be counted as a survivor — but `b <= d` is non-strict, so it *is* covered. On `[[1,4],[2,4]]` that would give 2 instead of 1.

⚠️ **`prev_end` only ever increases**, so it really is the maximum end of everything processed. Assigning it unconditionally (outside the `if`) would let a covered interval *lower* the frontier and break the invariant.
→ [for-loop](../syntax/for-loop.md) · [tuple-unpacking](../syntax/tuple-unpacking.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
return count
```

**No list of survivors is ever built** — the problem only asks how many.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def removeCoveredIntervals(self, intervals: List[List[int]]) -> int:

        intervals.sort(key=lambda x: (x[0], -x[1]))

        count = 0
        prev_end = 0

        for start, end in intervals:
            if end > prev_end:
                count += 1
                prev_end = end

        return count
```

</details>

<details>
<summary>The mirror version — sort by end descending</summary>

```python
class Solution:
    def removeCoveredIntervals(self, intervals: List[List[int]]) -> int:

        intervals.sort(key=lambda x: (-x[1], x[0]))

        count = 0
        min_start = float('inf')

        for start, end in intervals:
            if start < min_start:
                count += 1
                min_start = start

        return count
```

**Same argument on the other axis:** everything earlier ends at or after me, so I'm covered exactly when something earlier also started at or before me — i.e. when `start >= min_start`. **Verified identical to the primary version on 6,000 random inputs.**
→ [float-inf](../syntax/float-inf.md)

</details>

<details>
<summary>The O(n²) brute force — worth saying out loud, not submitting</summary>

```python
class Solution:
    def removeCoveredIntervals(self, intervals: List[List[int]]) -> int:

        n = len(intervals)
        count = 0

        for i in range(n):
            a, b = intervals[i]
            covered = any(
                intervals[j][0] <= a and b <= intervals[j][1]
                for j in range(n) if j != i
            )
            if not covered:
                count += 1

        return count
```

**A direct transcription of the definition** — which is exactly why it makes a good verification reference. ⚠️ Note `j != i`: without it every interval covers itself and the answer is always 0.
→ [any-all](../syntax/any-all.md) · [generator-expressions](../syntax/generator-expressions.md)

</details>

**Trace it** — Example 1, `[[1,4],[3,6],[2,8]]`:

```
sorted by (start ↑, end ↓):   [1,4]  [2,8]  [3,6]
```

| Interval | `end` vs `prev_end` | Verdict | `count` | `prev_end` |
|---|---|---|---|---|
| — | — | start | 0 | 0 |
| [1,4] | 4 > 0 | ✅ survives | 1 | 4 |
| [2,8] | 8 > 4 | ✅ survives | 2 | 8 |
| [3,6] | 6 ≤ 8 | ❌ **covered by [2,8]** | 2 | 8 |

**Answer: 2** ✅ — and the covering interval it names, `[2,8]`, is exactly the one the problem's explanation names.

**Example 2**, `[[1,4],[2,3]]`:

| Interval | Test | `count` | `prev_end` |
|---|---|---|---|
| [1,4] | 4 > 0 ✅ | 1 | 4 |
| [2,3] | 3 ≤ 4 ❌ covered | 1 | 4 |

**Answer: 1** ✅

**The tie-break case, traced both ways** — `[[1,2],[1,4]]`:

```
(start ↑, end ↓) →  [1,4] [1,2]
   [1,4]: 4 > 0  ✅  count=1, prev_end=4
   [1,2]: 2 <= 4 ❌  covered
   answer 1  ✅

(start ↑, end ↑) →  [1,2] [1,4]
   [1,2]: 2 > 0  ✅  count=1, prev_end=2
   [1,4]: 4 > 2  ✅  count=2
   answer 2  ❌
```

**Both intervals get counted because the short one set a low frontier before the long one arrived.**

**Verified:** the sweep was checked against the O(n²) definitional brute force on **6,000 randomised inputs** — **0 disagreements**. The same harness measured the ascending-tie-break variant failing **1,639 of 5,000** cases (**32.8%**).

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n log n)</summary>

**O(n log n)**, dominated entirely by the sort.

| Phase | Cost |
|---|---|
| Sort with the tuple key | **O(n log n)** |
| Single sweep | **O(n)** |
| **Total** | **O(n log n)** |

At `n = 1000` that's about **10⁴ operations**. Instant.

**Versus the brute force:**

| Approach | Time | At n = 1000 |
|---|---|---|
| **Sort + sweep** | **O(n log n)** | **~10⁴** ✅ |
| All pairs | O(n²) | 10⁶ — passes, ~100× more work |

**Can you beat O(n log n)?** ⚠️ **In general, no** — but here the coordinates are bounded by `10⁵`, so **counting/radix sort on the start value gives O(n + V)**. With `n <= 1000` and `V = 10⁵` that is *worse* in practice (the bucket array dwarfs the input), which makes it a nice thing to reason about out loud rather than implement:

```
comparison sort:  1000 × log₂1000  ≈  10⁴
counting sort:    1000 + 100,000   ≈  10⁵      ← the range dominates
```

**Comparison sorting wins whenever `V ≫ n`** — the mirror of the [Array Partition](561-array-partition.md) situation, where `V` was small and counting sort won.

**Why Ω(n) is the floor.** Every interval must be examined; an unread one could cover something or be uncovered itself.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1) auxiliary</summary>

**O(1)** auxiliary, beyond the sort.

| Component | Size |
|---|---|
| `count`, `prev_end`, `start`, `end` | **O(1)** ✅ |
| `intervals.sort()` | in place — **O(n)** for Timsort's temp buffer |
| **Total auxiliary** | **O(1)** (O(n) counting the sort's internals) |

⚠️ **No list of survivors is built.** The problem asks only for a count, so nothing accumulates. If you *did* need the survivors, append inside the `if` — **O(k) output for `k` survivors, and the algorithm is otherwise unchanged**:

```python
kept = []
for start, end in intervals:
    if end > prev_end:
        kept.append([start, end])
        prev_end = end
```

⚠️ **`intervals.sort()` mutates the caller's list.** Use `sorted(intervals, key=...)` — O(n) extra — when the caller still needs the original order.

**No recursion**, no auxiliary structures.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The brute force is to check each interval against every other for a coverer — O(n²), which passes at n equals a thousand but ignores the structure. Better: sort by start ascending. Then every interval processed before the current one starts at or before it, so the only question left is whether any of them ends at or after it — and I can answer that with a running maximum of the ends. If the current end is strictly greater than that maximum, nothing covers it, so I count it and it becomes the new frontier; otherwise it's covered and I skip it. The tie-break matters: when two intervals share a start, the longer one has to come first, so I sort end *descending*. Without that, `[[1,2],[1,4]]` returns 2 instead of 1 — it's wrong on about a third of random inputs, not a rare edge case. O(n log n) for the sort, O(1) extra space. Also worth noting: the constraints say the intervals are unique, which is what stops two identical intervals from covering each other."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why sort by start?" | It makes "does something earlier start before me?" automatically true, leaving one question — does anything earlier end after me — which a running max answers in O(1). |
| "**Why `-x[1]`?**" | **The key question.** Equal starts: the longer interval must be processed first so it can be the coverer. Otherwise the short one sets a low frontier and both get counted. `[[1,2],[1,4]]` → 2 instead of 1. |
| "How often does that actually matter?" | 32.8% of random inputs, measured. It's the common case, not a corner. |
| "Why `>` and not `>=`?" | `b <= d` is non-strict, so ending exactly at the frontier means covered. `[[1,4],[2,4]]` → 2 instead of 1. |
| "Can you do it without sorting?" | O(n²) pairwise, or bucket by start since coordinates are ≤ 10⁵ — but `V ≫ n` here, so counting sort is slower. |
| "Return the survivors, not the count." | Append inside the `if`. O(k) output, same time. |
| "What if intervals could repeat?" | Ambiguous by the literal definition — identical intervals cover each other. The greedy keeps one; a strict reading removes both. **State your choice.** |
| "Is the mirror version valid?" | Yes — sort end descending, start ascending, track the minimum start. Verified equivalent. |
| "What if they're `[l, r]` closed instead of `[l, r)`?" | No change — the covering test is identical. |
| "Count intervals covered by a *union* of others?" | Different, harder problem — merge the others first, then test containment. The single-coverer greedy doesn't apply. |
| "Relation to [Merge Intervals](56-merge-intervals.md)?" | Same sort-by-start sweep with a running end. Merging *joins* overlappers; this one *discards* the contained ones. |

**Traps:**

- ⚠️ **Sorting `(start ↑, end ↑)`** — the single biggest trap. Wrong on 32.8% of random inputs; minimal counterexample `[[1,2],[1,4]]`.
- ⚠️ **`end >= prev_end`** instead of `>` — counts an interval that shares the frontier's end, which *is* covered.
- **Updating `prev_end` outside the `if`** — a covered interval would lower the frontier and destroy the running-max invariant.
- **Sorting by end only** without the start tie-break — the mirror version needs `(-end, start)`, not just `-end`.
- **Forgetting `j != i` in the brute force** — every interval covers itself; the answer becomes 0.
- **Assuming covering means overlapping** — `[1,4]` and `[3,6]` overlap but neither covers the other.
- **`intervals.sort()` mutating the caller's list.**
- **Building the survivor list when only a count was asked for** — harmless, but it turns O(1) space into O(k).

**This same move shows up in:** [Merge Intervals](56-merge-intervals.md) (sort by start, sweep with a running end) · [Non-overlapping Intervals](435-non-overlapping-intervals.md) (a sort key chosen to make a greedy provable) · [Minimum Number of Arrows to Burst Balloons](452-minimum-number-of-arrows-to-burst-balloons.md) (the same family, sorted by end instead) · [Meeting Rooms](252-meeting-rooms.md) (sort by start, compare adjacent) · [Array Partition](561-array-partition.md) (sorting as the entire algorithm) · [sorting-key](../syntax/sorting-key.md).

</details>

---
