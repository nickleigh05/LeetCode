# 1834. Single-Threaded CPU

**Medium** · [LeetCode](https://leetcode.com/problems/single-threaded-cpu/) · [Solution file (no hints)](../../problems/1500-1999/1834.py)

[📖 09. Heap / Priority Queue lesson](../learning/09-heap-priority-queue.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 09. Heap problems](../rmap-practice/09-heap-priority-queue.md)

---

`tasks[i] = [enqueueTime, processingTime]`. A single-threaded CPU:

- If **idle with no available task**, it stays idle
- If **idle with available tasks**, it picks the **shortest processing time**; ties broken by **smallest index**
- Runs a task to completion without interruption, and can start the next instantly

Return the **order** in which tasks are processed.

```
tasks = [[1,2],[2,4],[3,2],[4,1]]        →  [0,2,3,1]
tasks = [[7,10],[7,12],[7,5],[7,4],[7,2]]  →  [4,3,2,0,1]
```

**Constraints:** `1 <= n <= 10⁵` · `1 <= enqueueTime, processingTime <= 10⁹`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| tasks become available at `enqueueTime` | ⚠️ Availability is time-gated — the candidate pool **grows** as the clock advances |
| picks **shortest processing time** | Selection is by a *different* key than availability |
| ties → **smallest index** | ⚠️ You must carry the **original index**, and the output is indices |
| "**idle** with no tasks" | The clock may need to **jump forward** to the next arrival |
| return the **order** | Output is a permutation of indices, not times |
| `n` up to 10⁵, times up to 10⁹ | O(n²) is too slow; and you can't simulate second-by-second — 10⁹ ticks is hopeless |

**This is [IPO](502-ipo.md)'s structure with a clock.** Two different orderings again:

- **Availability** is ordered by `enqueueTime`
- **Selection** is ordered by `processingTime` (then index)

So the same pairing applies: **sort by the availability key, sweep a monotonic pointer, and heap on the selection key.**

**The new wrinkle: idle time.** Unlike IPO, where capital only grows through your own actions, here the gate is a clock — and the CPU may have to **wait**. If no task has arrived yet, you can't just stop; you must advance the clock to the next arrival:

```
time = max(time, tasks[i].enqueueTime)
```

That single line is what distinguishes this from IPO, and forgetting it causes an infinite loop or a wrong order.

**Why you can't simulate tick by tick.** With times up to 10⁹, incrementing a clock one unit at a time is 10⁹ iterations. The clock must **jump** — either forward to the next arrival (when idle) or forward by the task's duration (when working).

🤔 **Before you open the next section:** if the CPU is idle and nothing has arrived yet, what's the earliest moment anything can happen — and how do you get there in one step?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Simulate each time unit | Advance the clock by 1 | O(maxTime) = 10⁹ | O(n) | ❌ Hopeless |
| Scan all tasks each step | Find the best available one linearly | O(n²) | O(n) | ❌ 10¹⁰ |
| **Sort by enqueue + min-heap on (proc, index)** | Unlock by time, select by duration | **O(n log n)** | O(n) | ✅ |

**The decision: sort tasks by `enqueueTime`, sweep a pointer, and maintain a min-heap keyed on `(processingTime, index)`.**

**Why the heap key is a tuple.** Python compares tuples element-wise, so `(processingTime, index)` gives exactly the required ordering:

1. shortest processing time first ✅
2. on a tie, smallest index first ✅

Both keys point the **same** direction (ascending), so a plain min-heap works with no negation and no custom comparator — a pleasant contrast with [Top K Frequent Words](692-top-k-frequent-words.md), where the keys conflicted.

**Why the original index must be captured before sorting.** Sorting by enqueue time destroys positional information, and the answer *is* a list of original indices. So build triples up front:

```python
sorted_tasks = sorted((enq, proc, i) for i, (enq, proc) in enumerate(tasks))
```

Forgetting this is the most common bug — you end up returning sorted positions rather than original indices.

**The three-case main loop:**

| Situation | Action |
|---|---|
| Heap empty **and** tasks remain unarrived | **Jump the clock** to the next arrival |
| Tasks have arrived (`enqueue <= time`) | Push them into the heap |
| Heap non-empty | Pop the best, run it, advance `time` by its duration |

**Why the pointer is monotonic.** The clock never goes backward, so once a task's `enqueueTime <= time`, it stays available. Each task is unlocked exactly once across the whole run — the same amortized O(n) argument as [IPO](502-ipo.md) and the sliding-window family.

**Why not a sorted list instead of a heap?** The available pool changes as tasks arrive, so a static sort goes stale. A heap absorbs insertions in O(log n) while keeping the minimum available in O(1).

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
import heapq

sorted_tasks = sorted((enq, proc, i) for i, (enq, proc) in enumerate(tasks))
```

**Capture the original index before sorting.**

`enumerate` supplies `i`; the triple `(enqueueTime, processingTime, index)` sorts by arrival, which is the order the pointer will sweep.
→ [enumerate](../syntax/enumerate.md) · [sorting-key](../syntax/sorting-key.md) · [generator-expressions](../syntax/generator-expressions.md)

```python
result = []
min_heap = []
time = 0
i = 0
n = len(tasks)
```

- `min_heap` — available tasks as `(processingTime, index)`
- `time` — the clock, only ever advancing
- `i` — how far into `sorted_tasks` we've unlocked; **never resets**

→ [variables-assignment](../syntax/variables-assignment.md)

```python
while i < n or min_heap:
```

**Continue while work remains** — either unarrived tasks or available ones.

Both conditions are needed: the heap can be empty while tasks are still to come (the CPU is idle), and tasks can be exhausted while the heap still holds work.
→ [while-loop](../syntax/while-loop.md) · [logical-operators](../syntax/logical-operators.md)

```python
    if not min_heap and time < sorted_tasks[i][0]:
        time = sorted_tasks[i][0]
```

**The idle jump — the line that distinguishes this from [IPO](502-ipo.md).**

Nothing is available and the next task hasn't arrived, so advance the clock straight to its arrival. One assignment instead of 10⁹ increments.

Safe to index `sorted_tasks[i]` because an empty heap plus the loop condition guarantees `i < n`.
→ [comparison-operators](../syntax/comparison-operators.md)

```python
    while i < n and sorted_tasks[i][0] <= time:
        heapq.heappush(min_heap, (sorted_tasks[i][1], sorted_tasks[i][2]))
        i += 1
```

**Unlock everything that has arrived by now.**

Push `(processingTime, index)` — the selection key. `i` only moves forward, so this inner loop runs at most `n` times **in total** across the whole algorithm.
→ [heapq-module](../syntax/heapq-module.md)

```python
    proc, idx = heapq.heappop(min_heap)
    result.append(idx)
    time += proc
```

**Run the best available task.**

The heap's root is the shortest processing time, with the smallest index breaking ties — exactly the CPU's rule.

`time += proc` jumps the clock to the completion moment; any tasks arriving during that interval will be unlocked on the next iteration.
→ [tuple-unpacking](../syntax/tuple-unpacking.md) · [list-methods](../syntax/list-methods.md)

```python
return result
```

<details>
<summary>The whole thing together</summary>

```python
import heapq

class Solution:
    def getOrder(self, tasks: List[List[int]]) -> List[int]:

        sorted_tasks = sorted((enq, proc, i) for i, (enq, proc) in enumerate(tasks))

        result = []
        min_heap = []
        time = 0
        i = 0
        n = len(tasks)

        while i < n or min_heap:
            if not min_heap and time < sorted_tasks[i][0]:
                time = sorted_tasks[i][0]

            while i < n and sorted_tasks[i][0] <= time:
                heapq.heappush(min_heap, (sorted_tasks[i][1], sorted_tasks[i][2]))
                i += 1

            proc, idx = heapq.heappop(min_heap)
            result.append(idx)
            time += proc

        return result
```

</details>

**Trace it** — `tasks = [[1,2],[2,4],[3,2],[4,1]]`:

**Sorted as `(enqueue, processing, index)`:** `[(1,2,0), (2,4,1), (3,2,2), (4,1,3)]`

| Step | `time` | Idle jump? | Unlocked | Heap `(proc, idx)` | Popped | `result` | `time` after |
|---|---|---|---|---|---|---|---|
| 1 | 0 | ✅ → 1 | `(2,0)` | `[(2,0)]` | **(2,0)** | `[0]` | 3 |
| 2 | 3 | no | `(4,1)`, `(2,2)` | `[(2,2),(4,1)]` | **(2,2)** | `[0,2]` | 5 |
| 3 | 5 | no | `(1,3)` | `[(1,3),(4,1)]` | **(1,3)** | `[0,2,3]` | 6 |
| 4 | 6 | no | — | `[(4,1)]` | **(4,1)** | `[0,2,3,1]` | 10 |

Return **`[0,2,3,1]`** ✅

Step 1 shows the idle jump: at `time = 0` nothing has arrived, so the clock leaps to 1. Step 3 shows the heap's value — task 3 arrived at time 4 with duration 1, and it beat the already-waiting task 1 (duration 4) despite arriving later.

**The all-same-arrival case** — `tasks = [[7,10],[7,12],[7,5],[7,4],[7,2]]`:

Sorted: `[(7,10,0), (7,12,1), (7,5,2), (7,4,3), (7,2,4)]`

Step 1 jumps the clock to 7, then **all five** unlock at once. The heap holds `(10,0), (12,1), (5,2), (4,3), (2,4)`, and popping repeatedly yields them by ascending processing time:

| Pop order | `(proc, idx)` | `result` |
|---|---|---|
| 1 | `(2,4)` | `[4]` |
| 2 | `(4,3)` | `[4,3]` |
| 3 | `(5,2)` | `[4,3,2]` |
| 4 | `(10,0)` | `[4,3,2,0]` |
| 5 | `(12,1)` | `[4,3,2,0,1]` |

Return **`[4,3,2,0,1]`** ✅ — purely by duration, since all arrival times tie.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n log n)</summary>

**O(n log n).**

| Phase | Cost |
|---|---|
| Sorting by enqueue time | **O(n log n)** |
| Unlocking (total across the run) | **O(n log n)** — each task pushed once |
| Selection | **O(n log n)** — each task popped once |

At `n = 10⁵`: about `3 × 10⁵ × 17` ≈ **5 × 10⁶ operations** — fast.

**The amortized point again:** the inner `while` inside the outer `while` looks quadratic, but `i` never resets, so the unlock loop executes at most `n` times **in total**. Each task is pushed exactly once and popped exactly once.

**Why the clock jumps rather than ticks.** With times up to 10⁹, a per-unit simulation is 10⁹ iterations. Both advances — `time = nextArrival` when idle, `time += proc` when working — move the clock in single steps to the only moments where anything changes. **Event-driven simulation, not time-stepped.**

That distinction is worth naming: you only ever visit the `2n` moments when a task starts or finishes, never the empty intervals between.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** — the sorted triples plus a heap that can hold every task if they all arrive before any completes.

`result` is O(n), required output.

| | Space |
|---|---|
| Sorted triples | O(n) |
| Min-heap | O(n) worst case |
| Clock, pointer | O(1) |

**The design pattern, stated generally:**

> **When availability is governed by one key and selection by another, sort on the availability key and sweep a monotonic pointer, then heap on the selection key.**

The sort handles a **static** ordering known up front; the heap handles a **dynamic** pool whose membership grows over time. Neither structure alone can do both jobs efficiently.

This is exactly [IPO](502-ipo.md)'s architecture, with one addition: **the gate here is a clock that can require waiting**, so the idle jump is needed. In IPO the gate is capital, which only changes through your own actions, so there's nothing to wait for — you simply stop.

That contrast is worth holding onto:

| | Availability gate | When nothing is available |
|---|---|---|
| [IPO](502-ipo.md) | capital (self-driven) | **stop** — it can never improve |
| **Single-Threaded CPU** | clock (external) | **jump forward** to the next arrival |

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Availability is ordered by enqueue time but selection is by processing time, so I use two structures: sort the tasks by arrival — capturing each original index first, since the answer is indices — and sweep a pointer forward, pushing arrived tasks into a min-heap keyed on `(processingTime, index)`. That tuple gives both rules at once: shortest duration first, smallest index on ties, and since both keys ascend a plain min-heap works with no negation. Each round I unlock whatever has arrived, pop the best, and advance the clock by its duration. The extra piece compared to IPO is the **idle jump**: if nothing is available yet, I set the clock straight to the next arrival rather than ticking — times go up to 10⁹, so this has to be event-driven. O(n log n), and the unlock pointer never resets so each task is pushed and popped exactly once."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why not simulate each time unit?" | Times reach 10⁹. Jump the clock to the next event — either the next arrival or the current task's completion. |
| "How are ties broken?" | The heap key is `(processingTime, index)`; tuple comparison handles the tie automatically. |
| "Why capture the index before sorting?" | Sorting destroys positions, and the output is original indices. |
| "How does this differ from [IPO](502-ipo.md)?" | Same sort-plus-heap architecture, but the gate is a **clock**, so when nothing is available you *wait* rather than stop. |
| "Why isn't the nested loop O(n²)?" | The unlock pointer only moves forward — total inner iterations ≤ n. |
| "What if the CPU had **multiple cores**?" | Add a second heap of core-free times; pop the earliest-free core, assign, push back its new free time. |
| "What if tasks could be **preempted**?" | Shortest-remaining-time-first — you'd re-heap the partially completed task with its remaining duration. |

**Traps:**

- **Forgetting the idle jump.** With an empty heap and no arrivals yet, the loop spins or pops an empty heap.
- **Losing the original index.** Returning sorted positions instead of task indices — the most common bug.
- **Heaping on `(index, processingTime)`.** Wrong key order; ties must break on index *after* duration.
- **Resetting the unlock pointer.** Turns the amortized O(n) into O(n²) and re-pushes duplicates.
- **Ticking the clock by 1.** 10⁹ iterations.
- **Using `while i < n` alone as the loop condition.** Leaves tasks stranded in the heap after the last arrival.
- **Advancing `time` before running the task.** The task starts *now* and finishes at `time + proc`.

**This same move shows up in:** [IPO](502-ipo.md) (the same sort-by-availability, heap-by-selection pairing, gated by capital instead of time) · [Maximum Subsequence Score](2542-maximum-subsequence-score.md) (sort by the constraint key, heap on the accumulated key) · [Meeting Rooms II](253-meeting-rooms-ii.md) (event-driven simulation with a heap of end times) · [Merge k Sorted Lists](23-merge-k-sorted-lists.md) (a heap surfacing the next item from a changing frontier).

</details>

---
