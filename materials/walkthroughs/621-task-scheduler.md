# 621. Task Scheduler

**Medium** · [LeetCode](https://leetcode.com/problems/task-scheduler/)

[📖 10. Heap / Priority Queue lesson](../learning/10-heap-priority-queue.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 10. Heap / Priority Queue problems](../rmap-practice/10-heap-priority-queue.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

You're given an array of CPU `tasks`, each labelled with a letter, and a **cooldown** integer `n`. Each task takes **one unit of time**, and the CPU can complete one task or stay **idle** in each unit.

There must be **at least `n` units of time between any two identical tasks**.

Return the **minimum** number of time units needed to complete all tasks.

```
tasks = ["A","A","A","B","B","B"], n = 2  →  8

  A → B → idle → A → B → idle → A → B
  the two A's are always ≥ 2 units apart ✅

tasks = ["A","C","A","B","D","B"], n = 1  →  6      (no idling needed)
tasks = ["A","A","A","B","B","B"], n = 0  →  6      (no cooldown)
```

**Constraints:** `1 <= tasks.length <= 10⁴` · tasks are **uppercase English letters** (so ≤ 26 distinct) · `0 <= n <= 100`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "at least `n` units between **identical** tasks" | ⚠️ Only same-letter tasks conflict. Different tasks can run back to back |
| "**minimum** time" | Minimize idling — which means keeping the CPU busy whenever possible |
| CPU can stay **idle** | Idle slots count toward the total, so they're the thing to avoid |
| **uppercase letters only** | ≤ 26 distinct task types — a bounded alphabet, which shapes the complexity |
| task labels are interchangeable | Only the **counts** matter, never which specific letter |

**The first realization: only counts matter.** `["A","A","B"]` and `["X","X","Y"]` are the same problem. So begin by counting frequencies — the actual letters are irrelevant.

**The second: the most frequent task is the bottleneck.** In the first example, `A` appears 3 times with cooldown 2, so the A's alone force a skeleton:

```
A _ _ A _ _ A          the gaps MUST be at least 2 wide
```

Everything else has to fit into those gaps — or the gaps stay idle.

**So the greedy rule is: always schedule the most frequent remaining task.** Intuitively, the task with the most copies left is the one most likely to cause idling later, so you want to start burning it down as early as possible. Leaving it until the end guarantees stalls.

**And the structural need:** you must repeatedly find the **maximum remaining count**, from a set whose counts keep changing as tasks are scheduled. That's a **max-heap** — the same signal as [Last Stone Weight](1046-last-stone-weight.md).

**The extra complication over a plain heap:** a task that's just run isn't available again for `n` units. So it can't go straight back into the heap — it has to **wait** somewhere until its cooldown expires. That's a second structure: a queue of cooling-down tasks, ordered by when they become ready.

🤔 **Before you open the next section:** if a task has just been executed at time `t`, at what time does it become eligible again — and what makes a queue the right place to park it?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Verdict |
|---|---|---|
| Try all orderings | Brute-force permutations | ❌ Factorial |
| Round-robin the distinct tasks | Cycle through types | ⚠️ Works sometimes; fails when one task dominates |
| **Math formula** | Compute idle slots directly from the max count | ✅ **O(n)**, no simulation — see below |
| **Max-heap + cooldown queue** | Greedily schedule the most frequent available task | ✅ Simulates the schedule explicitly |

**The decision: a max-heap of remaining counts, plus a queue of cooling-down tasks.**

Two structures, each doing one job:

| Structure | Holds | Answers |
|---|---|---|
| **Max-heap** | counts of **available** tasks | "which task should I run now?" |
| **Queue** | `(count, ready_time)` for **cooling** tasks | "which task becomes available next?" |

Each time unit:
1. **Run** the highest-count available task (pop the heap). If copies remain, park it in the queue with `ready_time = time + n`.
2. **Release** any task whose cooldown has just expired — push it back onto the heap.
3. If the heap is empty but the queue isn't, the CPU **idles** — time still advances.

**Why a queue and not another heap.** Tasks enter the cooldown queue in increasing order of `ready_time` (since `time` only advances), so the queue is **already sorted** — the front is always the next to become ready. A FIFO queue suffices; a heap would be unnecessary machinery. **That's the same "the input arrives in order, so no sorting needed" observation as [Time Based Key-Value Store](981-time-based-key-value-store.md).**

**Why greedy works.** Scheduling the most frequent task first is optimal because that task constrains the schedule the most — it needs the most gaps. Deferring it only compresses its remaining copies into fewer slots, forcing more idling. (The formal argument is an exchange argument; the intuition is enough for an interview.)

**The formula alternative is worth knowing**, and some interviewers prefer it:

```python
counts = Counter(tasks).values()
max_count = max(counts)
n_max = sum(1 for c in counts if c == max_count)
return max(len(tasks), (max_count - 1) * (n + 1) + n_max)
```

The most frequent task creates `max_count - 1` gaps of width `n + 1`, plus a final block for the tasks tied at the maximum. And it can never be fewer than `len(tasks)`. **O(n), no simulation** — but it requires trusting the derivation, whereas the heap simulation is self-evidently correct.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
import heapq
from collections import Counter, deque

counts = Counter(tasks)
max_heap = [-count for count in counts.values()]
heapq.heapify(max_heap)
```

**Count, then heapify the negated counts.** `Counter` tallies the frequencies; the labels are discarded via `.values()` because only counts matter.

Negation simulates a max-heap in Python's min-heap, as in [Last Stone Weight](1046-last-stone-weight.md). `heapify` builds it in O(26).
→ [counter](../syntax/counter.md) · [from-import](../syntax/from-import.md) · [list-comprehension](../syntax/list-comprehension.md) · [heapq-module](../syntax/heapq-module.md)

```python
time = 0
queue = deque()
```

`time` is the clock — the answer. `queue` holds `(remaining_count, ready_time)` for tasks in cooldown.
→ [deque](../data-structures/deque.md) · [deque-basics](../syntax/deque-basics.md)

```python
while max_heap or queue:
    time += 1
```

**Advance one time unit per iteration.** Continue while any task is either available (heap) or cooling (queue).

Incrementing **first** means `time` is 1-based — the first task runs at time 1, which makes the cooldown arithmetic below read naturally.
→ [while-loop](../syntax/while-loop.md) · [logical-operators](../syntax/logical-operators.md) · [truthy-falsy-values](../syntax/truthy-falsy-values.md)

```python
    if max_heap:
        count = 1 + heapq.heappop(max_heap)   # counts are negative, +1 uses one occurrence
        if count:
            queue.append((count, time + n))
```

**Run the most frequent available task.**

`1 + heappop(...)` looks odd but is exactly right: the stored value is **negative**, so adding 1 moves it *toward zero* — consuming one occurrence. A count of `-3` becomes `-2`.

`if count:` is a truthiness check — `0` is falsy, so a fully-consumed task isn't re-queued. Any non-zero (negative) count means copies remain, so it goes into cooldown until `time + n`.

**If the heap is empty**, this block is skipped entirely — the CPU idles, but `time` still advanced. That's how idle units get counted with no special handling.
→ [arithmetic-operators](../syntax/arithmetic-operators.md) · [tuple-basics](../syntax/tuple-basics.md)

```python
    if queue and queue[0][1] == time:
        heapq.heappush(max_heap, queue.popleft()[0])
```

**Release a cooled-down task.** The front of the queue has the earliest `ready_time`; when it equals the current time, that task is available again.

`queue[0][1]` reads the front entry's ready time; `popleft()[0]` removes it and takes its count.

Only **one** task can become ready per time unit, because each was queued at a distinct time — so a single `if` suffices, not a `while`.
→ [if-return](../syntax/if-return.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
return time
```

The clock when everything is done — including every idle unit.

<details>
<summary>The whole thing together</summary>

```python
import heapq
from collections import Counter, deque

class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:

        counts = Counter(tasks)
        max_heap = [-count for count in counts.values()]
        heapq.heapify(max_heap)

        time = 0
        queue = deque()

        while max_heap or queue:
            time += 1

            if max_heap:
                count = 1 + heapq.heappop(max_heap)   # counts are negative, +1 uses one occurrence
                if count:
                    queue.append((count, time + n))

            if queue and queue[0][1] == time:
                heapq.heappush(max_heap, queue.popleft()[0])

        return time
```

</details>

**Trace it** — `tasks = ["A","A","A","B","B","B"]`, `n = 2`. Counts: A=3, B=3 → heap `{-3, -3}`.

| `time` | Heap before | Run | Queued as | Released | Schedule |
|---|---|---|---|---|---|
| 1 | `{-3,-3}` | A (−3→−2) | (−2, ready 3) | — | `A` |
| 2 | `{-3}` | B (−3→−2) | (−2, ready 4) | — | `A B` |
| 3 | `{}` | **idle** | — | A returns | `A B _` |
| 4 | `{-2}` | A (−2→−1) | (−1, ready 6) | B returns | `A B _ A` |
| 5 | `{-2}` | B (−2→−1) | (−1, ready 7) | — | `A B _ A B` |
| 6 | `{}` | **idle** | — | A returns | `A B _ A B _` |
| 7 | `{-1}` | A (−1→0) | not requeued | B returns | `… A` |
| 8 | `{-1}` | B (−1→0) | not requeued | — | `A B _ A B _ A B` |

Heap and queue both empty → return **8** ✅

Times 3 and 6 are the idle units: the heap was empty because both A and B were cooling, so `time` advanced with nothing scheduled — exactly the behaviour the `if max_heap:` guard produces.

**And the no-idle case** — `["A","C","A","B","D","B"]`, `n = 1`: with four distinct tasks there's always something available, the heap never empties, and the answer is just `len(tasks) = 6` ✅

</details>

<details>
<summary><b>4 · Time complexity</b> — O(total time)</summary>

**O(T)** where T is the returned answer, with each step costing O(log 26) = **O(1)**.

| Step | Cost |
|---|---|
| `Counter(tasks)` | O(len(tasks)) |
| `heapify` | O(26) = O(1) |
| Each loop iteration | one pop + one push, both O(log 26) = **O(1)** |
| Iterations | T (the total time, including idles) |

**Why log 26 is a constant:** tasks are uppercase letters, so the heap holds **at most 26** entries regardless of how many tasks there are. Its depth is bounded by log₂ 26 ≈ 5.

Since T ≤ `len(tasks)` × (n+1) in the worst case, and idles are bounded, this is effectively **O(len(tasks) + T)** — linear in the schedule length.

**The formula approach is strictly better: O(len(tasks))**, with no simulation at all. It computes the answer arithmetically rather than stepping through every time unit — a genuine improvement when the schedule is long and mostly idle (e.g. one task type with a huge `n`).

**Worth naming the trade:** the simulation is *obviously* correct and produces the actual schedule if you need it; the formula is faster but requires trusting a derivation. **Mention the formula, write whichever you can defend.**

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — bounded by the 26-letter alphabet.

| Structure | Size |
|---|---|
| `Counter` | ≤ 26 entries |
| `max_heap` | ≤ 26 |
| `queue` | ≤ 26 (a task is in exactly one of the two at any moment) |

All bounded by the number of **distinct task types**, which the constraints cap at 26 — independent of `len(tasks)`. Ten thousand tasks still use at most 26 slots.

**Justify it, don't just assert it:** *"O(1), bounded by the 26 uppercase letters."* A bare "O(1)" invites the challenge. Same discipline as [Valid Anagram](242-valid-anagram.md) and [Longest Repeating Character Replacement](424-longest-repeating-character-replacement.md) — **always check the alphabet constraint before claiming a space bound.**

**Note a task is never in both structures.** It's either available (heap) or cooling (queue), so their combined size is at most 26 — not 52.

**In the general case** with an unbounded alphabet, this would be **O(d)** for d distinct task types. The 26-letter constraint is what collapses it to constant.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Only the counts matter — the labels are interchangeable. The greedy insight is to always run the most frequent remaining task, because that's the one most likely to force idling later. So I need repeated access to the maximum remaining count from a changing set, which is a max-heap. The complication is cooldown: a task just executed isn't available for n units, so it can't go straight back into the heap. I park it in a queue with its ready time, and since time only advances, tasks enter that queue already in ready-time order — so a plain FIFO queue works, no second heap needed. Each time unit I run the best available task and release any that has cooled down; if the heap is empty the CPU idles but the clock still advances, which counts idle time automatically. Everything is bounded by 26 letters, so it's O(1) space and effectively linear time. There's also a closed-form formula that skips the simulation entirely."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Solve it without simulating." | **The formula:** `max(len(tasks), (max_count − 1) × (n + 1) + count_of_tasks_tied_at_max)`. The most frequent task creates `max_count−1` gaps of width `n+1`. |
| "Why is greedy optimal?" | The most frequent task constrains the schedule most; deferring it compresses its copies into fewer remaining slots, forcing more idling. |
| "Why a queue and not a second heap?" | Tasks enter cooldown in increasing ready-time order because time only advances — so it's already sorted. |
| "Return the actual **schedule**?" | Track labels alongside counts in the heap tuples and append each executed label to a list. |
| "What if cooldowns differed per task?" | The queue is no longer sorted by ready time — you'd need a **min-heap** keyed on ready time. |
| "What if the alphabet were unbounded?" | Space becomes O(d) for d distinct types, and heap operations O(log d). The algorithm is unchanged. |
| "n = 0?" | No cooldown, so nothing ever queues and the answer is `len(tasks)`. The code handles it — `time + 0` releases immediately. |

**Traps:**

- **`count = heappop(max_heap) - 1`.** Counts are stored **negative**, so consuming one means **adding** 1. Getting the sign backwards makes counts diverge.
- **Pushing a zero count back** into the queue — use the truthiness check so exhausted tasks disappear.
- **Forgetting the negation** anywhere in the round trip.
- **Using `while` for the release step.** Only one task can become ready per time unit, since each was queued at a distinct time.
- **Not advancing `time` when idling.** The `if max_heap:` guard must be *inside* the loop, after `time += 1`, so idle units are still counted.
- **Round-robin scheduling.** Seems reasonable, fails when one task dominates.

**This same move shows up in:** [Last Stone Weight](1046-last-stone-weight.md) (a max-heap for repeated extremes, with negation) · [Design Twitter](355-design-twitter.md) (heap plus a second structure) · [Time Based Key-Value Store](981-time-based-key-value-store.md) (input arriving pre-sorted, so no sorting is needed) · [heap](../data-structures/heap.md).

</details>

---
