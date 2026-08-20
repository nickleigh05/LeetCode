# 252. Meeting Rooms

**Easy** · [LeetCode](https://leetcode.com/problems/meeting-rooms/)

[📖 17. Intervals lesson](../learning/17-intervals.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 17. Intervals problems](../rmap-practice/17-intervals.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Given an array of meeting time `intervals` where `intervals[i] = [start_i, end_i]`, determine if a person could **attend all meetings** — that is, whether any two meetings overlap.

```
intervals = [[0,30],[5,10],[15,20]]   →  false    [0,30] overlaps both others
intervals = [[7,10],[2,4]]            →  true     no overlap
intervals = [[1,5],[5,9]]             →  true     touching at a point is fine
```

**Constraints:** `0 <= intervals.length <= 10⁴` · `intervals[i].length == 2` · `0 <= start_i < end_i <= 10⁶`.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "attend **all** meetings" | Feasibility, and it's a **universal** claim — every pair must be compatible. So a *single* conflict anywhere makes the answer false |
| meetings are intervals | Two meetings conflict when they overlap in time |
| input order unspecified | Arbitrary order. Sorting is the standard response |
| `[1,5]` and `[5,9]` are fine | One meeting ending exactly as another begins is not a conflict. So the test is strict: `start < prev_end` is a conflict |
| `n` can be **0** | Zero meetings trivially works. The code must not assume anything exists |
| `n <= 10⁴` | n² = 10⁸ is borderline; **O(n log n)** is the target |

The brute force is obvious: check all `n(n-1)/2` pairs for overlap. Two intervals `[a,b]` and `[c,d]` overlap when `a < d` **and** `c < b`. That's O(n²) — around 5 × 10⁷ pair checks at the limit, which is uncomfortably slow and, more to the point, unnecessary.

**Sorting by start time reduces "any pair" to "any adjacent pair."** Here's why that's valid, and it's the only real insight in the problem:

Suppose meetings are sorted by start, and consider any two that overlap — say `intervals[i]` and `intervals[j]` with `i < j`. Then `intervals[j]` starts before `intervals[i]` ends. But every meeting *between* them also starts at or after `intervals[i]`'s start and at or before `intervals[j]`'s start — so **`intervals[i]` and `intervals[i+1]` must overlap too.**

In other words: **if any overlap exists in a start-sorted list, an adjacent overlap exists.** So checking the n−1 adjacent pairs is enough to detect *any* conflict. You never miss one by skipping the non-adjacent comparisons.

That collapses O(n²) pair checks into a single O(n) sweep.

🤔 **Before you open the next section:** the check below is `intervals[i][0] < intervals[i-1][1]`. Why strict `<` rather than `<=` — and which of the three examples above depends on that choice?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Check every pair | Test all n(n−1)/2 pairs for overlap | **O(n²)** | O(1) | ⚠️ Correct, and it might squeak by at n = 10⁴ — but it's the answer that stops working one constraint bump later |
| Timeline / boolean array | Mark every minute each meeting occupies, look for a double-marking | O(n · T) | O(T) | ❌ Times reach 10⁶, so the array is huge and the marking is slow |
| Sweep line with events | `+1` at each start, `−1` at each end, sort, check whether the count ever exceeds 1 | O(n log n) | O(n) | ✅ Correct — and it's exactly what [Meeting Rooms II](253-meeting-rooms-ii.md) needs |
| **Sort by start, check adjacent pairs** | Sort, then one linear sweep | **O(n log n)** | **O(1)** | ✅ |

**The decision:** **sort by start time, then check adjacent pairs.**

**Why sort by *start*?** Because this is a **grouping/detection** problem, not a selection one. Sorting by start makes potentially-conflicting meetings adjacent, which is what licenses the single sweep. Compare [Non-overlapping Intervals](435-non-overlapping-intervals.md), which sorts by **end** because it's *choosing* which intervals to keep and wants whichever frees the timeline soonest.

That's the unit's organizing rule again:

| Problem type | Sort by |
|---|---|
| Merging, grouping, **detecting** conflicts | **start** |
| Selecting, scheduling, maximizing keeps | **end** |

**Why adjacent-only checking is sufficient**, restated as the thing to say out loud: *in a start-sorted list, the earliest possible conflict for any meeting is with its immediate predecessor.* If a meeting doesn't overlap the one just before it, it can't overlap anything earlier either — because everything earlier started sooner and (given no adjacent conflicts so far) ended before this one began. **One comparison per meeting settles it.**

**Why not the sweep line here?** It's correct and it's the right tool when you need to *count* simultaneous meetings. But for a yes/no conflict check it builds 2n events and sorts them for an answer the simpler sweep already gives — more machinery, O(n) extra space, same complexity. Mention it as the generalization; don't write it.

**Why not the timeline array?** Times reach 10⁶, so you'd allocate a million-slot array and potentially mark a million slots per meeting. It's O(n·T), which is worse in both dimensions.

**On early exit:** returning `False` at the first conflict is the natural shape, since one conflict is decisive. It doesn't improve the worst case (no conflicts means a full scan) but it's free.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
intervals.sort(key=lambda interval: interval[0])
```
**Sort by start time** — the move that makes adjacent-pair checking valid.

The [`lambda`](../syntax/lambda-functions.md) selects the start as the sort key. Plain `intervals.sort()` would give the same order here (Python sorts lists lexicographically, so ties break by end), but naming the key states the intent.

`.sort()` works in place, avoiding an O(n) copy — at the cost of mutating the caller's array.
→ [sorting-key](../syntax/sorting-key.md) · [lambda-functions](../syntax/lambda-functions.md) · [list-methods](../syntax/list-methods.md)

```python
for i in range(1, len(intervals)):
```
Start at index **1**, since each iteration compares a meeting to the one **before** it. There's nothing before index 0.

This also handles both degenerate cases with no special code: with 0 or 1 meetings, `range(1, 0)` and `range(1, 1)` are empty, the loop never runs, and the function returns `True` — which is correct, since a person with no conflicts to have can attend everything.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md)

```python
    if intervals[i][0] < intervals[i - 1][1]:
        return False
```
**The conflict test**, and both halves of it matter.

`intervals[i][0]` is this meeting's start; `intervals[i - 1][1]` is the previous meeting's end. If this one **starts before** the previous one ends, they overlap and attending both is impossible.

**Strict `<`, not `<=`** — the answer to section 1's question. `[[1,5],[5,9]]` has one meeting ending exactly as the next begins, which is *not* a conflict. Using `<=` would return `False` there, wrongly.

Note the contrast with [Merge Intervals](56-merge-intervals.md), where `<=` is correct because touching intervals are *merged*. **Same geometry, opposite comparison, because the two problems define "overlap" differently** — and that's exactly the kind of detail worth reading the statement carefully for.

One conflict is decisive, so return immediately.
→ [comparison-operators](../syntax/comparison-operators.md) · [if-return](../syntax/if-return.md) · [nested-lists](../syntax/nested-lists.md)

```python
return True
```
Every adjacent pair was clear — and by the argument in section 1, that means **no** pair conflicts anywhere.
→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def canAttendMeetings(self, intervals: List[List[int]]) -> bool:

        intervals.sort(key=lambda interval: interval[0])

        for i in range(1, len(intervals)):
            if intervals[i][0] < intervals[i - 1][1]:
                return False

        return True
```
</details>

**Trace it** — `intervals = [[0,30],[5,10],[15,20]]`

Sorted by start: `[[0,30], [5,10], [15,20]]` (already in order)

| `i` | previous | current | `cur_start < prev_end`? | result |
|---|---|---|---|---|
| 1 | `[0,30]` | `[5,10]` | **5 < 30** ✓ | **return False** |

Return **false** ✅ — caught on the first comparison, since `[0,30]` swallows everything after it.

**And a clean schedule** — `intervals = [[7,10],[2,4]]`:

Sorted by start: `[[2,4], [7,10]]`

| `i` | previous | current | `cur_start < prev_end`? | result |
|---|---|---|---|---|
| 1 | `[2,4]` | `[7,10]` | 7 < 4 ✗ | continue |

Return **true** ✅ — and note the sort was essential. **Unsorted, the comparison would have been `2 < 10` — a false conflict**, reporting `false` for a perfectly valid schedule.

**And the touching case** — `intervals = [[1,5],[5,9]]`:

| `i` | previous | current | `cur_start < prev_end`? | result |
|---|---|---|---|---|
| 1 | `[1,5]` | `[5,9]` | **5 < 5** ✗ | continue |

Return **true** ✅ — the strict `<` is what makes this work. With `<=`, `5 <= 5` would fire and wrongly report a conflict.

**And a case showing why adjacent-only is enough** — `intervals = [[1,4],[2,6],[8,9]]`:

| `i` | previous | current | test | result |
|---|---|---|---|---|
| 1 | `[1,4]` | `[2,6]` | **2 < 4** ✓ | **return False** |

The pair `[1,4]`/`[8,9]` is never compared, and doesn't need to be — the conflict surfaced between neighbours. **Any overlap in a start-sorted list guarantees an adjacent overlap**, so the sweep can't miss one.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n log n)</summary>

**O(n log n)**, dominated by the sort.

- **`intervals.sort()`** — comparison sort on n items → **O(n log n)**. The bottleneck.
- **The scan** — n − 1 iterations, each doing two array reads and one comparison → **O(n)**.
- O(n log n) + O(n) = **O(n log n)**.

At n = 10⁴ that's roughly 1.4 × 10⁵ comparisons. Instant.

**Best case is much better:** the loop returns on the first conflict found, so `[[0,30],[5,10],…]` exits after one comparison. The sort still costs O(n log n) though, so **the early exit improves the scan, not the overall bound.**

**Against brute force:** checking all pairs is **O(n²)** ≈ 5 × 10⁷ at the limit. The saving comes entirely from the sort: **paying O(n log n) once to make the pairwise check unnecessary is cheaper than the pairwise check itself.** That trade — spend on sorting to buy a linear sweep — is the defining move of this whole unit.

**Can you beat O(n log n)?** Not by comparison sorting. Times are bounded by 10⁶, so a radix sort on start values would give **O(n + k)**, but with k = 10⁶ and n = 10⁴ that's worse in practice. Not worth it here.

**If the input arrived sorted**, the whole thing would be **O(n)**.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** auxiliary — just the loop index. No result array, no auxiliary structure; the answer is a single boolean.

| Component | Space | Why |
|---|---|---|
| `i` | **O(1)** | One integer |
| Python's `.sort()` (Timsort) | **O(n)** worst case | Temporary storage for merging runs |

So: **O(1) beyond the sort**, or O(n) if you count Timsort's working memory. Say which convention you're using.

**Why this is leaner than the alternatives:**

- The **sweep-line** version builds a list of 2n events → **O(n)**.
- The **timeline array** version allocates up to 10⁶ slots → **O(T)**, far worse.
- Sorting in place and comparing neighbours needs **nothing**.

**Why no accumulator is needed:** the question is a single yes/no, and the algorithm returns the instant it knows. Nothing has to be remembered across iterations except the previous interval — which is already in the array, one index back. **When a scan can read its own history from the input, it needs no state at all.**

**Side effect worth flagging:** `.sort()` mutates the caller's array. If the input must be preserved, use `sorted(intervals, key=...)` at the cost of an O(n) copy.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Brute force checks all pairs for overlap — O(n²). But if I sort by start time, I only need to check *adjacent* pairs. The reason is that in a start-sorted list, if any two meetings overlap, then some adjacent pair overlaps too: everything between them starts within the same window. So a single linear sweep detects any conflict at all. The comparison is strict — a meeting starting exactly when the previous one ends is fine — which is the opposite of Merge Intervals, where touching intervals *do* merge. One conflict is decisive so I return immediately. O(n log n) from the sort, O(1) extra space. And I'd sort by start rather than end here because this is a detection problem, not a selection problem — selection problems like Non-overlapping Intervals want the earliest *end*."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why is checking adjacent pairs enough?" | In a start-sorted list, any overlapping pair implies an adjacent overlapping pair — every meeting between them starts in the same window. So no conflict can hide between non-adjacent meetings. |
| "Why strict `<` and not `<=`?" | Touching meetings don't conflict — `[1,5]` and `[5,9]` are both attendable. `<=` would report a false conflict. |
| "Why does [Merge Intervals](56-merge-intervals.md) use `<=` then?" | Different definition of overlap. There, touching intervals merge into one; here, touching meetings are compatible. Read the statement — the geometry is identical, the convention isn't. |
| "How many rooms would you need?" | That's [Meeting Rooms II](253-meeting-rooms-ii.md) — count the maximum number of simultaneous meetings, using a sweep line or a two-pointer walk over sorted starts and ends. |
| "Why sort by start and not end?" | Detection and grouping want conflicting intervals adjacent, which start-sorting gives. Selection problems want whichever interval frees the timeline soonest, which is end-sorting. |
| "What if the input were already sorted?" | O(n) — just the scan. |
| "Can you avoid mutating the input?" | Use `sorted(...)` instead of `.sort()`, costing an extra O(n). |
| "What about zero or one meeting?" | Both return `True` with no special case — the loop range is empty. |

**Traps:**
- **Using `<=` instead of `<`.** Reports a conflict for back-to-back meetings. The defining bug here, and it's the opposite of the right choice in [56](56-merge-intervals.md).
- **Forgetting to sort.** `[[7,10],[2,4]]` would compare `2 < 10` and wrongly return `False`.
- **Starting the loop at 0** — `intervals[-1]` silently wraps to the last element in Python, comparing the first meeting against the last. Wrong answer, no error.
- Comparing `intervals[i][1]` against `intervals[i-1][0]` — the two fields reversed.
- Checking all pairs after sorting. Correct but O(n²), and it misses the point of sorting.
- Assuming an empty input needs special handling. It doesn't.

**This same move shows up in:** [Merge Intervals](56-merge-intervals.md) (sort by start, sweep once — the same structure, but merging rather than detecting, and with `<=`) · [Insert Interval](57-insert-interval.md) (a single pass over already-sorted intervals) · [Non-overlapping Intervals](435-non-overlapping-intervals.md) (sorted by *end*, because it selects rather than detects) · [Meeting Rooms II](253-meeting-rooms-ii.md) (the same question generalized from "is there any overlap" to "how many overlap at once") · [Contains Duplicate](217-contains-duplicate.md) (sorting to turn a pairwise question into an adjacent-neighbour check).

</details>

---
