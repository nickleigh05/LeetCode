# 57. Insert Interval

**Medium** · [LeetCode](https://leetcode.com/problems/insert-interval/)

[📖 16. Intervals lesson](../learning/17-intervals.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 16. Intervals problems](../rmap-practice/16-intervals.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

You're given an array of **non-overlapping** intervals `intervals`, **sorted in ascending order by start**, and a `newInterval`. Insert it so the result is still sorted and non-overlapping, **merging** where necessary. Return the resulting array.

```
intervals = [[1,3],[6,9]],                newInterval = [2,5]
        →  [[1,5],[6,9]]                  [2,5] merges with [1,3]

intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]
        →  [[1,2],[3,10],[12,16]]         [4,8] swallows three intervals at once

intervals = [],  newInterval = [5,7]      →  [[5,7]]
```

**Constraints:** `0 <= intervals.length <= 10⁴` · `intervals[i].length == 2` · `0 <= start_i <= end_i <= 10⁵` · `intervals` is sorted by `start_i` and non-overlapping.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| the input is **already sorted** | The expensive part of [Merge Intervals](56-merge-intervals.md) is done for you. **That's the whole gift** — it's what makes O(n) possible instead of O(n log n) |
| the input is **already non-overlapping** | You don't have to merge the existing intervals with each other, only with the new one |
| "insert… merging where necessary" | The new interval can overlap **zero, one, or many** consecutive existing intervals — example 2 swallows three |
| result must stay sorted | Position matters. The new interval goes exactly where its start belongs |
| `n` can be **0** | An empty input is legal, so the code must not assume anything exists |

Here's the observation that gives the algorithm its shape. Because the existing intervals are sorted **and** non-overlapping, they fall into exactly **three consecutive blocks** relative to the new interval:

```
[ before ][ overlapping ][ after ]
```

1. **Before** — intervals that end **strictly before** the new one starts. They're untouched; copy them.
2. **Overlapping** — intervals that touch the new one. **These are contiguous** — they can't be scattered, because sortedness means once you pass the overlapping region you never return to it. Absorb them all into one expanded interval.
3. **After** — intervals that start **strictly after** the new one ends. Untouched; copy them.

The key structural fact is that **the overlapping block is a contiguous run**. That's what lets you handle the whole problem with three sequential `while` loops sharing one index, rather than a search or a merge pass.

And notice what *isn't* needed: no sorting, no binary search (though it's possible), no comparing existing intervals against each other. **The sortedness of the input has done all the organizing already.**

🤔 **Before you open the next section:** phase 1 stops when an interval's end is `>=` the new interval's start, and phase 2 stops when an interval's start is `>` the new interval's end. Why are those the right boundaries — and what does "touching at a single point" do to each?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Append and re-run [Merge Intervals](56-merge-intervals.md) | Add the new interval, sort, merge | O(n log n) | O(n) | ⚠️ Correct, and a perfectly good fallback answer — but it throws away the sortedness you were handed |
| Insert at the right position, then merge | Binary search for the slot, insert, merge neighbours | O(n) | O(n) | ⚠️ The search is O(log n) but the list insertion is O(n), so nothing is gained |
| **Three-phase linear scan** | Copy before, absorb overlapping, copy after | **O(n)** | O(n) | ✅ |
| Binary search both boundaries | Find the first and last overlapping index, splice | O(n) | O(n) | ✅ Same bound — the copying dominates — but worth naming |

**The decision:** the **three-phase linear scan**.

**Why not just reuse [Merge Intervals](56-merge-intervals.md)?** You can, and it's correct. But it re-sorts data that arrives sorted, which is exactly the work the problem removed for you. **When a problem hands you a precondition, the expected solution exploits it** — here that turns O(n log n) into O(n). Saying "I could append and re-merge for O(n log n), but the input is already sorted so I can do it in one linear pass" is the ideal framing: acknowledge the fallback, then beat it.

**Why the three phases are genuinely separate.** Each has a different job and a different stopping condition:

| Phase | Condition to continue | What it does |
|---|---|---|
| 1 · Before | `intervals[i].end < new.start` | Copy verbatim |
| 2 · Overlapping | `intervals[i].start <= new.end` | Expand the new interval |
| 3 · After | anything remaining | Copy verbatim |

They share a single index `i` that only ever moves forward, which is why the whole thing is one pass despite being three loops.

**Why the boundary conditions are what they are** — the answer to section 1's question:

- **Phase 1 uses `end < start`** (strict). An interval ending exactly *at* the new interval's start **touches** it, and touching counts as overlapping — so it must fall into phase 2, not phase 1. Using `<=` would copy it verbatim and fail to merge.
- **Phase 2 uses `start <= end`** (inclusive). An interval starting exactly at the new interval's end also touches, so it belongs in the merge. Using `<` would leave `[1,3]` and `[3,5]` unmerged.

**Both boundaries are chosen so that "touching" lands in phase 2.** That symmetry is the thing to remember, and it's where most implementations get it wrong.

**Why binary search doesn't help asymptotically.** You could find both boundaries in O(log n), but you still have to *copy* the before-block and the after-block into the result, which is O(n). The scan is already linear, so the search buys nothing — though it's a legitimate answer if the question becomes "many insertions into a persistent structure."

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
result = []
i = 0
n = len(intervals)
```
`result` accumulates the output. `i` is a **single cursor shared by all three phases** — each loop picks up exactly where the previous one stopped, which is what keeps this to one pass.

Caching `n` avoids recomputing `len()` in three loop conditions.
→ [list-basics](../syntax/list-basics.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
while i < n and intervals[i][1] < newInterval[0]:
    result.append(intervals[i])
    i += 1
```
**Phase 1 — copy everything that ends before the new interval begins.**

The test `intervals[i][1] < newInterval[0]` is **strict**: this interval's end is *before* the new one's start, so there's no contact at all and it passes through untouched.

If it were `<=`, an interval ending exactly at the new start (like `[1,3]` against a new `[3,5]`) would be copied verbatim instead of merged — wrong, since touching counts as overlapping.

The `i < n` guard comes first so [`and`](../syntax/logical-operators.md) short-circuits before indexing out of range — and it's what makes the empty-input case work with no special handling.
→ [while-loop](../syntax/while-loop.md) · [logical-operators](../syntax/logical-operators.md) · [list-methods](../syntax/list-methods.md)

```python
while i < n and intervals[i][0] <= newInterval[1]:
    newInterval = [
        min(newInterval[0], intervals[i][0]),
        max(newInterval[1], intervals[i][1]),
    ]
    i += 1
```
**Phase 2 — absorb every overlapping interval into the new one.**

The condition `intervals[i][0] <= newInterval[1]` is **inclusive**, so an interval starting exactly where the new one ends still merges.

Two things to notice about the merge itself:

- **`min` on the start.** Only the *first* overlapping interval can start before the new one — phase 1 guaranteed everything earlier ended before `newInterval[0]`. So the `min` matters on exactly one iteration, but writing it unconditionally is simpler than special-casing.
- **`max` on the end.** Essential and not just defensive. An existing interval can be entirely *contained* in the new one — in example 2, `[6,7]` sits inside `[4,8]` — and assigning the end directly would shrink the merged range.

Note that `newInterval` is **reassigned** rather than mutated. That avoids modifying the caller's list, and it means the loop condition reads the freshly expanded bounds on each iteration — which is what lets one long new interval swallow a whole run of existing ones.
→ [while-loop](../syntax/while-loop.md) · [min-max-key](../syntax/min-max-key.md) · [nested-lists](../syntax/nested-lists.md)

```python
result.append(newInterval)
```
**Place the merged interval**, after phase 2 has finished expanding it and before phase 3 copies the rest. Its position in `result` is automatically correct: everything before it ends earlier, everything after starts later.

This line runs unconditionally — even when nothing overlapped, in which case the new interval is inserted unchanged between the two blocks.
→ [list-methods](../syntax/list-methods.md)

```python
while i < n:
    result.append(intervals[i])
    i += 1
```
**Phase 3 — copy the remainder.** Every interval left starts strictly after the merged interval ends (that's why phase 2 stopped), so none of them need any adjustment.

No condition beyond `i < n` is needed; the previous loop's exit already established that these are all clear.
→ [while-loop](../syntax/while-loop.md) · [list-methods](../syntax/list-methods.md)

```python
return result
```
Sorted, non-overlapping, with the new interval merged into place.
→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:

        result = []
        i = 0
        n = len(intervals)

        while i < n and intervals[i][1] < newInterval[0]:
            result.append(intervals[i])
            i += 1

        while i < n and intervals[i][0] <= newInterval[1]:
            newInterval = [
                min(newInterval[0], intervals[i][0]),
                max(newInterval[1], intervals[i][1]),
            ]
            i += 1
        result.append(newInterval)

        while i < n:
            result.append(intervals[i])
            i += 1

        return result
```
</details>

**Trace it** — `intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]]`, `newInterval = [4,8]`

**Phase 1** — copy while `end < 4`:

| `i` | interval | `end < 4`? | action |
|---|---|---|---|
| 0 | `[1,2]` | 2 < 4 ✓ | copy → `result = [[1,2]]`, `i = 1` |
| 1 | `[3,5]` | 5 < 4 ✗ | **stop** |

**Phase 2** — absorb while `start <= newInterval.end`:

| `i` | interval | `start <= new_end`? | new interval becomes |
|---|---|---|---|
| 1 | `[3,5]` | 3 ≤ **8** ✓ | `[min(4,3), max(8,5)]` = **`[3,8]`** |
| 2 | `[6,7]` | 6 ≤ **8** ✓ | `[min(3,6), max(8,7)]` = **`[3,8]`** ← contained |
| 3 | `[8,10]` | 8 ≤ **8** ✓ | `[min(3,8), max(8,10)]` = **`[3,10]`** |
| 4 | `[12,16]` | 12 ≤ **10** ✗ | **stop** |

Append `[3,10]` → `result = [[1,2], [3,10]]`

**Phase 3** — copy the rest:

| `i` | interval | action |
|---|---|---|
| 4 | `[12,16]` | copy → `result = [[1,2], [3,10], [12,16]]` |

Return **[[1,2],[3,10],[12,16]]** ✅

Three rows repay attention. **`[3,5]`** starts before the new interval — the only one that can — so `min` pulls the start back to 3. **`[6,7]`** is entirely inside, so both `min` and `max` leave the bounds unchanged; without the `max` the end would have collapsed to 7. And **`[8,10]`** touches at exactly the boundary, `8 <= 8`, which the inclusive comparison catches — with `<` it would have been left out and the answer would wrongly be `[[1,2],[3,8],[8,10],[12,16]]`.

**And the no-overlap case** — `intervals = [[1,2],[7,9]]`, `newInterval = [4,5]`:

| phase | what happens | `result` |
|---|---|---|
| 1 | `[1,2]`: 2 < 4 ✓ copy. `[7,9]`: 9 < 4 ✗ stop | `[[1,2]]` |
| 2 | `[7,9]`: 7 ≤ 5 ✗ — **loop body never runs** | — |
| — | append `[4,5]` unchanged | `[[1,2], [4,5]]` |
| 3 | copy `[7,9]` | `[[1,2], [4,5], [7,9]]` |

Return **[[1,2],[4,5],[7,9]]** ✅ — a pure insertion with no merging, handled by the same code with phase 2 simply doing nothing.

**And the empty case** — `intervals = []`, `newInterval = [5,7]`: all three loops fail their `i < n` guard immediately, and the append in the middle produces **[[5,7]]** ✅.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

- The three `while` loops share a **single cursor `i` that only moves forward**, so across all three phases the total number of iterations is exactly **n**.
- Each iteration does O(1) work — a comparison, plus either an append (amortized O(1)) or a `min`/`max` pair.
- **O(n)** total.

At n = 10⁴ that's ten thousand operations. Instant.

**The structural point:** three loops does *not* mean three passes. They're sequential segments of one traversal, which is why the bound is O(n) and not O(3n)-as-something-worse. Being explicit about the shared cursor is what makes the analysis obvious.

**Against the alternative:** appending and re-running [Merge Intervals](56-merge-intervals.md) is **O(n log n)** — correct, but it pays for a sort the problem already did. **The whole point of this problem is that a precondition can lower the complexity class**, and recognizing that is what's being tested.

**Can you beat O(n)?** Not while returning a full array — constructing an output of size ~n is Ω(n) on its own. Binary search could locate the two boundaries in O(log n), but the copying still dominates. It would only pay off with a persistent or tree-based structure supporting sublinear splices, which is well outside the problem.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** for the output; **O(1)** auxiliary.

| Component | Space | Why |
|---|---|---|
| `result` | **O(n)** | Up to n + 1 intervals — but it's the *return value*, not scratch space |
| `newInterval` reassignment | O(1) | A fresh 2-element list each merge, and only one is alive at a time |
| `i`, `n` | O(1) | Two integers |

So the honest statement is **O(n) including the output, O(1) auxiliary** — and saying which convention you mean is what matters.

**Note that no sorting space is involved**, unlike [Merge Intervals](56-merge-intervals.md), where Timsort needs O(n) working memory. Skipping the sort saves both time *and* space.

**Could it be done in place?** In principle you could shift elements within the input array to overwrite the merged region, giving O(1) extra space. But the shifting is O(n) anyway, the index bookkeeping is error-prone, and it mutates the caller's data. **The trade isn't worth it** — building a fresh result is clearer for the same asymptotic cost.

**One deliberate choice worth noting:** phase 2 *reassigns* `newInterval` to a new list rather than mutating it. That leaves the caller's `newInterval` argument untouched, which is good hygiene — and it costs nothing, since only one such list exists at a time.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The input is already sorted and non-overlapping, and that's the whole gift — I could just append the new interval and re-run the merge algorithm for O(n log n), but exploiting the precondition gets me O(n). Since the intervals are sorted and disjoint, they split into three consecutive blocks relative to the new interval: those entirely before it, those overlapping it, and those entirely after. Crucially the overlapping ones are *contiguous* — sortedness means once I pass that region I never come back. So it's three sequential while loops sharing one forward-moving cursor: copy the before-block, absorb the overlapping block by taking min of starts and max of ends, append the expanded interval, then copy the rest. The boundary conditions are chosen so that intervals merely *touching* the new one land in the merge phase — strict `<` when skipping ahead, inclusive `<=` when absorbing. O(n) time, O(1) auxiliary."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why not append and re-run merge intervals?" | It works, but it's O(n log n) — re-sorting data that arrived sorted. Exploiting the precondition gives O(n). |
| "Why is the overlapping block contiguous?" | The intervals are sorted by start and disjoint. Once you reach one that starts after the new interval's end, every later one starts even later, so the overlap region can't resume. |
| "Why `<` in phase 1 but `<=` in phase 2?" | Both are set so that *touching* counts as overlapping. Phase 1 skips only intervals ending strictly before the new start; phase 2 absorbs any starting at or before the new end. |
| "Why `max` when expanding the end?" | An existing interval can be entirely contained in the new one — `[6,7]` inside `[4,8]` in example 2. Assigning directly would shrink the merged range. |
| "Why is `min` on the start needed at all?" | Only the first overlapping interval can start before the new one; everything earlier ended before it. So `min` matters on exactly one iteration — but applying it unconditionally is simpler than special-casing. |
| "Would binary search help?" | It finds the boundaries in O(log n), but copying the untouched blocks is still O(n), so the bound is unchanged. It'd only pay off with a structure supporting sublinear splices. |
| "What if the input weren't sorted?" | Then it's [Merge Intervals](56-merge-intervals.md) — sort first, O(n log n). |
| "What about inserting many intervals?" | Doing this repeatedly is O(kn). Better to collect all k, concatenate, sort once, and merge — O((n+k) log(n+k)). |

**Traps:**
- **Using `<=` in phase 1** instead of `<`. Intervals that touch the new start get copied verbatim instead of merged.
- **Using `<` in phase 2** instead of `<=`. Intervals touching the new end get left out — example 2's `[8,10]` catches this.
- **Assigning the end instead of taking `max`.** Breaks on containment.
- Forgetting the `i < n` guard in the first two loops — index errors, and the empty-input case fails.
- Appending `newInterval` inside phase 2 rather than after it — you'd emit partially-merged copies.
- Restarting `i` at 0 for a later phase, or using separate cursors. The single forward cursor is what makes it one pass.
- Mutating `newInterval` in place, which alters the caller's argument as a side effect.

**This same move shows up in:** [Merge Intervals](56-merge-intervals.md) (the same merge logic, but it must sort first — this problem is that one with the sort already done) · [Non-overlapping Intervals](435-non-overlapping-intervals.md) (sorted intervals scanned once, with a greedy decision per interval) · [Merge Two Sorted Lists](21-merge-two-sorted-lists.md) (exploiting sortedness to merge in linear time instead of sorting) · [Meeting Rooms](252-meeting-rooms.md) (sorted intervals, checking adjacent pairs in one pass).

</details>

---
