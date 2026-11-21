# 1235. Maximum Profit in Job Scheduling

**Hard** · [LeetCode](https://leetcode.com/problems/maximum-profit-in-job-scheduling/) · [Solution file (no hints)](../../problems/1000-1499/1235.py)

[📖 13. 1-D Dynamic Programming lesson](../learning/14-dp-1d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 13. 1-D Dynamic Programming problems](../rmap-practice/13-dp-1d.md)

---

There are `n` jobs. Job `i` runs from `startTime[i]` to `endTime[i]` and earns `profit[i]`. Choose a set of jobs with **no overlapping time ranges** that earns the **maximum total profit**.

A job ending at time `X` doesn't overlap a job starting at time `X`. **Touching is allowed.**

```
startTime = [1,2,3,3], endTime = [3,4,5,6], profit = [50,10,40,70]
→ 120      (jobs 1–3 and 3–6: 50 + 70)

startTime = [1,2,3,4,6], endTime = [3,5,10,6,9], profit = [20,20,100,70,60]
→ 150      (1–3, 4–6, 6–9: 20 + 70 + 60)

startTime = [1,1,1], endTime = [2,3,4], profit = [5,6,4]
→ 6
```

**Constraints:** `1 <= n <= 5·10⁴` · `1 <= startTime[i] < endTime[i] <= 10⁹` · `1 <= profit[i] <= 10⁴`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| choose **non-overlapping** jobs | An interval-scheduling problem, but **weighted**, which changes everything |
| **maximum profit** | An optimisation with take-or-skip choices, which points to **DP** |
| touching is allowed | A job can start exactly when the previous one ends: `end <= start` |
| times up to 10⁹ | You can't make a DP array indexed by time. Index by **job** instead |
| n up to 5·10⁴ | O(n²) is 2.5·10⁹. Too slow. You need O(n log n) |

**Why greedy fails.** For the **unweighted** version (maximise the *number* of jobs), "always take the job that ends earliest" is optimal. With profits, it breaks: one long, high-paying job can beat several short ones. In example 2, the earliest-ending choice gives `1–3, 4–6, 6–9` = 150, which happens to be optimal here. But with `[1–2: $1], [1–10: $100]`, earliest-ending takes the $1 job and blocks the $100 one.

**The DP: sort by end time, then take or skip.** Process jobs in order of when they **end**. For each job, either:

- **Skip it**: the best profit stays what it was before this job.
- **Take it**: earn its profit plus the best profit from jobs that **ended at or before its start**.

```
best(through job i) = max( best(through job i−1),
                           profit[i] + best(through the last job ending <= start[i]) )
```

**"The last job ending at or before `start`" is a binary search.** The jobs are sorted by end time, so the end times are a sorted list. `bisect_right(ends, start) - 1` finds the last job whose end is `<= start`. That's what turns O(n²) into O(n log n).

🤔 **Before you open the next section:** if the sorted end times are `[3, 4, 5, 6]` and a job starts at 3, which earlier jobs can it follow, and what does `bisect_right` return?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Try every subset | Check compatibility, sum profits | O(2ⁿ · n) | O(n) | ❌ |
| Greedy by earliest end | Unweighted interval scheduling | O(n log n) | O(1) | ❌ Wrong with weights |
| DP, scan back for compatibility | `dp[i]` = max(skip, take + the best compatible `dp[j]`) via a linear scan | O(n²) | O(n) | ⚠️ 2.5·10⁹ at the limit |
| **DP + binary search** | Sort by end; find the compatible predecessor with `bisect` | **O(n log n)** | O(n) | ✅ |

**The decision: [dynamic programming](../algorithms/dynamic-programming.md) over jobs sorted by end time, with [binary search](../algorithms/binary-search.md)** to find the compatible predecessor.

This is the classic **weighted interval scheduling** problem. It has the same shape as [House Robber](198-house-robber.md): take this one and jump back past the conflicts, or skip it. The only difference is that "past the conflicts" is found by binary search instead of always being `i − 2`.

**A compact representation.** Instead of a `dp` array aligned with the jobs, keep two parallel lists that only grow when the best profit **improves**:

- `ends[k]`: an end time.
- `best[k]`: the best profit achievable by that time.

Both start with a sentinel `(0, 0)`: by time 0, the best profit is 0. Because `best` only grows when it improves, `best[-1]` is always the overall best so far, and both lists stay sorted. Binary searching `ends` gives the best profit available by any time.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
jobs = sorted(zip(startTime, endTime, profit), key=lambda job: job[1])
```

**Bundle and sort by end time.** `zip` pairs up the three lists into `(start, end, profit)` tuples. Sorting by `job[1]` (the end) is what makes the DP valid. Every job that could come before the current one has already been processed.
→ [zip-function](../syntax/zip-function.md) · [sorting-key](../syntax/sorting-key.md) · [lambda-functions](../syntax/lambda-functions.md)

```python
ends = [0]
best = [0]
```

**The sentinel.** "By time 0, profit 0." It means every job has *some* predecessor to search for, even if that's "nothing before it," so the binary search never returns −1.
→ [list-basics](../syntax/list-basics.md)

```python
for start, end, gain in jobs:
    i = bisect.bisect_right(ends, start) - 1
    take = best[i] + gain
```

**The "take" option.** `bisect_right(ends, start)` gives the position just past the last end time `<= start`. Subtract 1 to land on it. `best[i]` is then the most profit achievable before this job can begin. Add this job's profit.

`bisect_right` rather than `bisect_left` matters: a job ending **exactly** at `start` is compatible (touching is allowed), and `bisect_right` includes it.
→ [bisect-module](../syntax/bisect-module.md) · [tuple-unpacking](../syntax/tuple-unpacking.md)

```python
    if take > best[-1]:
        ends.append(end)
        best.append(take)
```

**Compare with the "skip" option.** Skipping keeps `best[-1]`, the best so far. If taking this job beats that, record a new entry: by time `end`, you can have `take`.

If it doesn't beat it, record nothing. The previous entry already says "you can have `best[-1]` by an earlier time," which is just as good for any later job. Only recording improvements keeps `best` strictly increasing.
→ [list-methods](../syntax/list-methods.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
return best[-1]
```

The last entry is the best profit after considering every job.

<details>
<summary>The whole thing together</summary>

```python
import bisect

class Solution:
    def jobScheduling(self, startTime: List[int], endTime: List[int], profit: List[int]) -> int:
        jobs = sorted(zip(startTime, endTime, profit), key=lambda job: job[1])

        ends = [0]
        best = [0]

        for start, end, gain in jobs:
            i = bisect.bisect_right(ends, start) - 1
            take = best[i] + gain
            if take > best[-1]:
                ends.append(end)
                best.append(take)

        return best[-1]
```

</details>

**Trace it.** Example 1, with jobs sorted by end: `(1,3,50)`, `(2,4,10)`, `(3,5,40)`, `(3,6,70)`:

| Job (s, e, p) | Search `ends` for last ≤ s | `best[i]` | `take` | `best[-1]` | Record? | `ends` / `best` after |
|---|---|---|---|---|---|---|
| — | | | | | | `[0]` / `[0]` |
| (1, 3, 50) | ≤ 1 → end 0 | 0 | 50 | 0 | ✅ | `[0, 3]` / `[0, 50]` |
| (2, 4, 10) | ≤ 2 → end 0 | 0 | 10 | 50 | ❌ | unchanged |
| (3, 5, 40) | ≤ 3 → end **3** | 50 | 90 | 50 | ✅ | `[0, 3, 5]` / `[0, 50, 90]` |
| (3, 6, 70) | ≤ 3 → end **3** | 50 | **120** | 90 | ✅ | `[0, 3, 5, 6]` / `[0, 50, 90, 120]` |

Answer **120** ✅. Both the third and fourth jobs could follow the first one, because it ends at exactly 3 when they start. That's `bisect_right` including the equal end time.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n log n)</summary>

**O(n log n).**

- Sorting the jobs: O(n log n).
- For each job, one binary search on `ends` (at most n + 1 long): O(log n), so O(n log n) in total.
- Appends are O(1).

**Compare with the O(n²) scan:** at n = 5·10⁴, that's about 2.5·10⁹ against about 8·10⁵ operations.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n).** The sorted `jobs` list, plus `ends` and `best`, which hold at most n + 1 entries each.

You can't avoid storing the sorted jobs. Time values up to 10⁹ rule out any array indexed by time, which is why the DP is indexed by job.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "This is weighted interval scheduling. Greedy by earliest end fails once jobs have different profits, so it's DP. I sort jobs by end time. For each job, I either skip it and keep the best so far, or take it and add its profit to the best I could have by its start time. The jobs are sorted by end, so I find that with `bisect_right` on the end times. Right rather than left, because a job ending exactly at the start is compatible. I keep parallel lists of end times and best profits, only appending when the best improves, so both stay sorted. O(n log n) time, O(n) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why not greedy?" | Earliest-end greedy maximises job **count**, not profit. One expensive long job can beat many cheap short ones. |
| "Why sort by end, not start?" | So that every job that could precede the current one has already been processed. |
| "Why `bisect_right`?" | A job ending exactly at `start` is allowed. `bisect_left` would exclude it. |
| "Return the chosen jobs?" | Keep a parent pointer with each `best` entry (which job was taken, and which entry it extended), then walk back from the last one. |
| "Sort by start instead?" | Also works top-down: `dp[i] = max(dp[i+1], profit[i] + dp[next compatible])`, where "next compatible" is a `bisect_left` on start times. |

**Traps:**

- **Greedy.** It gives wrong answers on weighted inputs.
- **`bisect_left` on end times.** It excludes jobs that end exactly at `start`, which undercounts.
- **A DP array indexed by time.** Times go up to 10⁹.
- **O(n²) predecessor scans.** Correct, but they time out at 5·10⁴.
- **Forgetting the `(0, 0)` sentinel.** The first job's search returns −1, and `best[-1]` silently reads the *last* element.

**This same move shows up in:** [House Robber](198-house-robber.md) (take-or-skip DP, where "skip the neighbours" is fixed at i − 2) · [Non-overlapping Intervals](435-non-overlapping-intervals.md) (the unweighted version, where greedy does work) · [Longest Increasing Subsequence](300-longest-increasing-subsequence.md) (DP with binary search over a sorted helper list) · [Meeting Rooms II](253-meeting-rooms-ii.md) (sorting intervals by time to make the sweep easy).

</details>

---
