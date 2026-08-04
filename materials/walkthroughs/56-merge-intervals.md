# 56. Merge Intervals

**Medium** · [LeetCode](https://leetcode.com/problems/merge-intervals/) · [Solution file (no hints)](../../problems/0001-0499/56.py)

[📖 16. Intervals lesson](../learning/17-intervals.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 16. Intervals problems](../rmap-practice/16-intervals.md)

---

Given an array of `intervals` where `intervals[i] = [start_i, end_i]`, **merge all overlapping intervals** and return an array of the non-overlapping intervals that cover all the input intervals.

```
intervals = [[1,3],[2,6],[8,10],[15,18]]   →  [[1,6],[8,10],[15,18]]
        [1,3] and [2,6] overlap → [1,6]

intervals = [[1,4],[4,5]]                  →  [[1,5]]
        touching at a single point counts as overlapping

intervals = [[1,4],[2,3]]                  →  [[1,4]]
        [2,3] is entirely swallowed by [1,4]
```

**Constraints:** `1 <= intervals.length <= 10⁴` · `intervals[i].length == 2` · `0 <= start_i <= end_i <= 10⁴`.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| intervals `[start, end]` | Each is a pair, and the pair is meaningless unless you know how it relates to the others' positions |
| "**merge all overlapping**" | Overlapping is **transitive through chains**: if A overlaps B and B overlaps C, all three collapse into one — even if A and C don't touch |
| input order is **unspecified** | The intervals arrive in arbitrary order. That's the obstacle, and sorting is the obvious response |
| `[1,4]` and `[4,5]` merge | Touching endpoints count as overlapping. So the test is `<=`, not `<` — an off-by-one that decides several test cases |
| `n <= 10⁴` | n² = 10⁸ is borderline; **O(n log n) is the target**, and the log factor practically announces a sort |

Two intervals `[a, b]` and `[c, d]` overlap when `a <= d` **and** `c <= b`. That's a two-sided condition, and checking it for every pair is O(n²) — plus the chaining problem, since merging two intervals can create a new one that now overlaps something you already passed.

**Sorting by start time collapses both difficulties at once.** Once the intervals are in ascending order of start, walk them left to right maintaining a "current merged interval." For each new interval:

- Its start is **≥** the current merged interval's start (guaranteed by the sort).
- So the two-sided overlap test reduces to a **one-sided** one: they overlap iff `interval.start <= merged.end`.

Half the condition became free.

And the chaining problem disappears too. **If a new interval doesn't overlap the current merged one, it can't overlap anything earlier either** — because everything earlier started even sooner and the merged interval already absorbed the largest end among them. So you can close the current group permanently and start a new one, never looking back.

That's the answer to the question in the file's original prompt: sorting by start guarantees that anything overlapping the current group is **immediately next**, so one pass suffices.

🤔 **Before you open the next section:** when you merge a new interval into the current one, the new end is `max(merged.end, interval.end)` rather than just `interval.end`. Which input makes that distinction matter?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Compare every pair, merge, repeat | Merge any overlapping pair and restart until stable | **O(n³)** | O(n) | ❌ Restarting after each merge is brutal |
| Compare every pair once | Check all pairs, union overlapping groups | O(n²) | O(n) | ❌ 10⁸, and chaining makes it fiddly |
| Sweep line / event points | Emit `+1` at each start and `−1` at each end, sort events, merge where the count returns to 0 | O(n log n) | O(n) | ✅ Correct, and the right tool when you need *counts* of overlaps |
| **Sort by start, then one pass** | Sort, then extend or start a new group | **O(n log n)** | O(n) | ✅ |

**The decision:** **sort by start time, then a single linear merge pass.**

**Why sorting by *start* here**, when [Non-overlapping Intervals](435-non-overlapping-intervals.md) sorts by *end*? Because the two problems want different things. Here you're **grouping** — you need overlapping intervals adjacent to each other, and sorting by start guarantees that. There, you're **choosing** which intervals to keep, and the greedy needs the one that frees up the timeline soonest, which is the earliest *end*.

That's the distinction worth carrying through this whole unit: **sort by start to merge or group; sort by end to select or schedule.** Getting it backwards is the single most common interval-problem error.

**Why one pass is enough after sorting.** The invariant is that `merged[-1]` holds the current group, and its end is the maximum end seen in that group. When a new interval arrives:

- If it starts at or before that end, it belongs to the group — extend the end.
- If it starts after, the group is **finished forever**. Every remaining interval starts even later, so nothing can reach back to it.

**That "finished forever" guarantee is what makes the algorithm greedy** — a decision to close a group is never revisited.

**Why the sweep line is worth naming.** Treating each interval as a `+1` event at its start and a `−1` at its end, sorting the events, and tracking a running count gives the same answer: a merged interval spans from where the count rises above 0 to where it returns to 0. Same complexity, more machinery — but it's the approach that generalizes when you need "how many intervals overlap at the busiest moment," which is exactly [Meeting Rooms II](253-meeting-rooms-ii.md).

**Why `<=` and not `<`.** `[1,4]` and `[4,5]` are specified to merge. Using `<` would leave them separate. The problem defines touching as overlapping, so the boundary case is a stated requirement rather than a judgment call.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
intervals.sort(key=lambda interval: interval[0])
```
**Sort by start time** — the move that makes everything else linear.

The [`lambda`](../syntax/lambda-functions.md) extracts the first element as the sort key. Python sorts tuples and lists lexicographically by default, so plain `intervals.sort()` would give the same *order* here (ties broken by end), but the explicit key states the intent.

`.sort()` rather than `sorted()` sorts **in place**, avoiding an extra O(n) copy — acceptable because the problem doesn't require preserving the input.
→ [sorting-key](../syntax/sorting-key.md) · [lambda-functions](../syntax/lambda-functions.md) · [list-methods](../syntax/list-methods.md)

```python
merged = []
```
The output, built incrementally. Its **last element is always the group currently being extended**, which is why no separate "current interval" variable is needed.
→ [list-basics](../syntax/list-basics.md)

```python
for interval in intervals:
    if len(merged) == 0:
        merged.append(interval)
```
The first interval starts the first group unconditionally — there's nothing yet to compare it against.

This could be hoisted out of the loop (`merged = [intervals[0]]`, then iterate from index 1), which avoids re-checking emptiness n times. Same complexity; the in-loop version keeps the code in one shape.
→ [for-loop](../syntax/for-loop.md) · [list-methods](../syntax/list-methods.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
    else:
        last_interval = merged[-1]
```
Grab the current group. `merged[-1]` is Python's [negative index](../syntax/list-slicing.md) for the last element — and critically, this is a **reference**, not a copy, so mutating it below updates the list directly.
→ [list-slicing](../syntax/list-slicing.md) · [elif-else](../syntax/elif-else.md)

```python
        if interval[0] <= last_interval[1]:
            last_interval[1] = max(last_interval[1], interval[1])
```
**The overlap test and the merge**, and both details matter.

`interval[0] <= last_interval[1]` — the new interval starts at or before the group ends, so they overlap. This is the **one-sided** test the sort bought you: the other half (`last_interval[0] <= interval[1]`) is automatic, since sorting guarantees `last_interval[0] <= interval[0] <= interval[1]`.

`max(last_interval[1], interval[1])` — **and this is the answer to section 1's question.** The new interval might be entirely *inside* the current group: `[[1,4],[2,3]]`. Writing `last_interval[1] = interval[1]` would shrink the group's end from 4 to 3, losing coverage. The `max` is what makes containment work.

The mutation modifies the list in `merged` directly, since `last_interval` is a reference.
→ [comparison-operators](../syntax/comparison-operators.md) · [min-max-key](../syntax/min-max-key.md) · [nested-lists](../syntax/nested-lists.md)

```python
        else:
            merged.append(interval)
```
**No overlap → close the group and open a new one.** And this decision is permanent: everything still to come starts at or after this interval's start, so nothing can reach back to the group just closed.
→ [list-methods](../syntax/list-methods.md)

```python
return merged
```
Every interval has been absorbed into some group, and the groups are non-overlapping and in ascending order.
→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:

        intervals.sort(key=lambda interval: interval[0])
        merged = []

        for interval in intervals:
            if len(merged) == 0:
                merged.append(interval)
            else:
                last_interval = merged[-1]
                if interval[0] <= last_interval[1]:
                    last_interval[1] = max(last_interval[1], interval[1])
                else:
                    merged.append(interval)
        return merged
```
</details>

**Trace it** — `intervals = [[1,3],[2,6],[8,10],[15,18]]` (already sorted by start)

| interval | `merged[-1]` | `start <= last_end`? | action | `merged` after |
|---|---|---|---|---|
| `[1,3]` | — | list empty | append | `[[1,3]]` |
| `[2,6]` | `[1,3]` | 2 ≤ 3 ✓ | extend end to `max(3, 6)` = **6** | `[[1,6]]` |
| `[8,10]` | `[1,6]` | 8 ≤ 6 ✗ | append (new group) | `[[1,6], [8,10]]` |
| `[15,18]` | `[8,10]` | 15 ≤ 10 ✗ | append | `[[1,6], [8,10], [15,18]]` |

Return **[[1,6],[8,10],[15,18]]** ✅

**And the containment case** — `intervals = [[1,4],[2,3]]`:

| interval | `merged[-1]` | overlap? | action | `merged` after |
|---|---|---|---|---|
| `[1,4]` | — | empty | append | `[[1,4]]` |
| `[2,3]` | `[1,4]` | 2 ≤ 4 ✓ | extend end to `max(4, **3**)` = **4** | `[[1,4]]` |

Return **[[1,4]]** ✅ — and here the `max` earns its place. `[2,3]` sits entirely inside `[1,4]`, so the group's end must **stay** at 4. Assigning `interval[1]` directly would produce `[[1,3]]`, silently dropping coverage of the range 3–4.

**And the touching case** — `intervals = [[1,4],[4,5]]`:

| interval | overlap test | action | `merged` after |
|---|---|---|---|
| `[1,4]` | — | append | `[[1,4]]` |
| `[4,5]` | **4 ≤ 4** ✓ | extend to `max(4,5)` = 5 | `[[1,5]]` |

Return **[[1,5]]** ✅ — the `<=` is what merges them. With `<`, the answer would wrongly be `[[1,4],[4,5]]`.

**And unsorted input** — `intervals = [[8,10],[1,3],[15,18],[2,6]]`. The sort rearranges it to `[[1,3],[2,6],[8,10],[15,18]]` and the trace proceeds exactly as the first table. **Without the sort, `[1,3]` would be compared against `[8,10]`, found non-overlapping, and appended as a separate group — and the `[2,6]` that should have merged with it would arrive far too late.**

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n log n)</summary>

**O(n log n)**, dominated by the sort.

- **`intervals.sort()`** — comparison sort on n items → **O(n log n)**. This is the bottleneck.
- **The merge pass** — one iteration per interval, each doing a comparison, a `max`, and either a mutation or an append (amortized O(1)) → **O(n)**.
- O(n log n) + O(n) = **O(n log n)**.

At n = 10⁴ that's roughly 10⁴ × 14 ≈ 1.4 × 10⁵ comparisons. Instant.

**The point worth making explicitly:** the *merging* is linear — it's the **sorting that costs**. That's a useful thing to say, because it tells you where any further optimization would have to come from.

**Can you beat it?** Only by avoiding the comparison sort. Since coordinates are bounded by 10⁴, a **counting sort** on start values would give **O(n + k)** with k = 10⁴, making the whole algorithm linear. Worth mentioning as a constraint-specific trick; not worth writing, since the general solution is what's being tested.

**If the input were already sorted**, the whole thing is **O(n)** — which is exactly the situation in [Insert Interval](57-insert-interval.md), and why that problem is linear.

**Against the alternatives:** the pairwise approach is O(n²) at best, and O(n³) if you restart after each merge to handle chaining. Sorting eliminates chaining entirely, which is the real saving.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** for the output, plus the sort's own working space.

| Component | Space | Why |
|---|---|---|
| `merged` | **O(n)** | Up to n intervals if none overlap — but it's the *output*, not auxiliary |
| Python's `.sort()` (Timsort) | **O(n)** worst case | Timsort needs temporary storage for merging runs; often much less in practice |
| `last_interval` | O(1) | A reference, not a copy |

So the honest answer is **O(n)**, with the caveat that the output dominates and is unavoidable.

**Excluding the output**, the extra space is just the sort's — **O(n)** for Timsort, or O(log n) if you assume an in-place sort like heapsort or introsort. Some interviewers count the output, some don't; **stating which convention you're using is what matters.**

**Why `.sort()` and not `sorted()`:** sorting in place avoids an additional O(n) copy of the input. It does mutate the caller's array, which is fine here — but worth flagging as a side effect if the input needed preserving.

**A subtlety about mutation:** `last_interval[1] = ...` modifies an interval object *from the input array*, since `merged` holds references rather than copies. That's efficient and correct for this problem, but it means the input is altered beyond just being reordered. If that mattered, you'd append `list(interval)` instead.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The difficulty is that overlap chains — A can overlap B and B overlap C without A touching C — and the input is in arbitrary order, so a pairwise check is O(n²) and would need repeated passes. Sorting by start time fixes both. Once sorted, the two-sided overlap test becomes one-sided: the new interval starts at or after the current group's start by construction, so they overlap exactly when its start is ≤ the group's end. And if it *doesn't* overlap, nothing later can either, since everything remaining starts even later — so I close the group permanently and open a new one. When merging I take `max` of the two ends, because the new interval might be entirely contained in the current group. And the comparison is `<=`, not `<`, because touching endpoints count as overlapping. O(n log n), dominated by the sort — the merge itself is linear."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why sort by start rather than end?" | Because this is a *grouping* problem — sorting by start makes overlapping intervals adjacent. Sorting by end is for *selection* problems like [435](435-non-overlapping-intervals.md), where you want whichever interval frees the timeline soonest. |
| "Why `max` when extending the end?" | The new interval may be contained in the current group. `[[1,4],[2,3]]` → assigning the new end directly would shrink the group to `[1,3]` and lose coverage. |
| "Why `<=` instead of `<`?" | The problem specifies that touching intervals merge — `[1,4]` and `[4,5]` become `[1,5]`. |
| "What if the input were already sorted?" | The whole algorithm becomes O(n). That's exactly the setup in [Insert Interval](57-insert-interval.md). |
| "Can you beat O(n log n)?" | Not with comparison sorting. But coordinates are ≤ 10⁴, so a counting sort would make it O(n + k) — linear for these constraints. |
| "Solve it with a sweep line." | Emit `+1` at each start and `−1` at each end, sort the events, and track a running count: a merged interval runs from where the count rises above 0 to where it returns to 0. Same complexity, and it's what you need if the question becomes "how many overlap at once" — see [Meeting Rooms II](253-meeting-rooms-ii.md). |
| "What about intervals with equal starts?" | Handled automatically — the second one's start equals the first's, which satisfies `<=`, so they merge. Tie-break order doesn't matter. |
| "Does this mutate the input?" | Yes — it sorts in place and mutates interval objects when extending ends. Append copies if the caller's data must be preserved. |

**Traps:**
- **Assigning `last_interval[1] = interval[1]`** instead of taking the `max`. Breaks on containment, and it's the most common bug here.
- **Using `<` instead of `<=`** — fails to merge touching intervals.
- **Forgetting to sort.** The whole one-pass argument collapses; unsorted input produces wrong groupings.
- Comparing against `merged[0]` or a fixed variable instead of `merged[-1]` — you must always test against the *current* group.
- Building a new interval object on merge rather than mutating — correct, just less efficient, and easy to get wrong by forgetting to write it back.
- Handling chaining explicitly with a second pass. Unnecessary — sorting already removed the problem.

**This same move shows up in:** [Insert Interval](57-insert-interval.md) (the same merge logic, on input that's already sorted — so no sort needed) · [Non-overlapping Intervals](435-non-overlapping-intervals.md) (intervals sorted by *end* because it's a selection problem, not a grouping one) · [Meeting Rooms](252-meeting-rooms.md) (sort by start, then check adjacent pairs for any overlap) · [Partition Labels](763-partition-labels.md) (this exact algorithm in disguise — each letter's first and last occurrence forms an interval, and the parts are the merged groups).

</details>

---
