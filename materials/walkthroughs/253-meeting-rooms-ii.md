# 253. Meeting Rooms II

**Medium** · [LeetCode](https://leetcode.com/problems/meeting-rooms-ii/)

[📖 16. Intervals lesson](../learning/17-intervals.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 16. Intervals problems](../rmap-practice/16-intervals.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Given an array of meeting time `intervals`, return the **minimum number of conference rooms** required to hold all of them.

```
intervals = [[0,30],[5,10],[15,20]]   →  2
        [0,30] runs the whole time; [5,10] and [15,20] can share the second room

intervals = [[7,10],[2,4]]            →  1     they don't overlap
intervals = [[1,5],[5,9]]             →  1     touching at a point needs no second room
```

**Constraints:** `1 <= intervals.length <= 10⁴` · `0 <= start_i < end_i <= 10⁶`.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**minimum** number of rooms" | Optimization — but as you'll see, the answer is forced rather than chosen |
| meetings need separate rooms when they overlap | Rooms are a resource consumed by *simultaneity*. Meetings that don't overlap can share |
| `[1,5]` and `[5,9]` need one room | Touching at a point isn't simultaneous. The boundary convention matters again |
| input order unspecified | Sorting is coming |
| `n <= 10⁴` | O(n log n) is the target |

[Meeting Rooms](252-meeting-rooms.md) asked *"is there any overlap?"* This asks *"how many overlap at the busiest moment?"* — a count instead of a boolean, and that changes the tool.

The reframing that dissolves the problem:

> **The answer is the maximum number of meetings in progress at any single instant.**

Not a scheduling puzzle, not an assignment problem — just a **peak concurrency** measurement. If three meetings are ever running simultaneously you need three rooms, and if that's the worst moment, three rooms suffice for the whole day.

That's worth pausing on, because it's not obvious that the maximum is *achievable*. It is: process meetings in time order and always reuse a free room when one exists. You never need more rooms than the peak, because whenever you open a new room, that's precisely a moment when all existing rooms are busy — so the count of concurrent meetings equals the number of rooms in use. **The peak isn't just a lower bound; it's the answer.**

**So how do you find the peak?** Stop thinking about meetings as objects and think about **events on a timeline**:

- A meeting **starting** is `+1` room in use.
- A meeting **ending** is `−1`.

Sort all 2n events by time, sweep through them keeping a running count, and record the maximum. **The intervals stop mattering entirely** — only their endpoints do, and the pairing between a start and its own end is irrelevant, because rooms are interchangeable.

That last point is the real insight: **you never track which meeting is in which room.** You only count.

🤔 **Before you open the next section:** if a meeting ends at time 5 and another starts at time 5, should the sweep process the end or the start first — and what does each choice compute?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Simulate room assignment | Keep a list of rooms, place each meeting in a free one | O(n²) | O(n) | ⚠️ Correct but needless — you'd scan the room list per meeting, and you don't need the assignment |
| Timeline array | `+1` at each start minute, `−1` at each end, prefix-sum it | O(n + T) | O(T) | ❌ Times reach 10⁶, so T dominates |
| **Two sorted arrays, two pointers** | Sort starts and ends separately, walk both | **O(n log n)** | O(n) | ✅ |
| Min-heap of end times | Sort by start; for each meeting, pop ends that have passed, push this end; heap size is the room count | O(n log n) | O(n) | ✅ Equivalent, and it *does* model rooms explicitly |
| Sweep line with `(time, delta)` events | Build 2n events, sort, running sum | O(n log n) | O(n) | ✅ The most general version |

**The decision:** **sort starts and ends into two separate arrays, then walk them with two pointers.**

**Why separating starts from ends is legitimate.** It looks like vandalism — you're destroying the pairing between each meeting's start and its own end. But **rooms are interchangeable**, so it doesn't matter *which* meeting frees a room, only that one was freed. All the algorithm needs is the chronological sequence of "+1" and "−1" moments, and splitting the arrays gives exactly that, sorted, for free.

**Why this beats simulating rooms.** Tracking assignments means, per meeting, finding a room whose last meeting has ended — O(n) per meeting unless you keep the rooms in a heap. And the assignment is information the question never asked for. **Counting is strictly less work than scheduling.**

**The tie-breaking question** — the answer to section 1's. When a meeting ends at exactly the same time another starts, processing the **end first** frees the room for reuse, giving 1 room for `[[1,5],[5,9]]`. Processing the **start first** would give 2. The problem's convention is that touching meetings can share, so **ends must win ties.**

In the code below, that's enforced by the comparison `starts[start_ptr] < ends[end_ptr]`: a start only claims a room if it happens **strictly before** the earliest pending end. On a tie the condition is false, so the `else` branch fires and the room is released first. **One character — `<` rather than `<=` — encodes the entire tie-break rule.**

(This is the same boundary convention as [252](252-meeting-rooms.md), and the opposite of [Merge Intervals](56-merge-intervals.md). The geometry is identical across all three; only the definition of "overlap" changes.)

**Why mention the heap version?** Sort by start, keep a min-heap of end times, and for each meeting pop every end that's ≤ its start before pushing its own. The heap's size *is* the number of rooms in use, and its maximum is the answer. Same complexity, and it has the advantage of **actually modelling rooms** — so if a follow-up asks "which meeting goes where," the heap version extends naturally while the two-pointer version doesn't. Worth naming for exactly that reason.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
starts = sorted(interval[0] for interval in intervals)
ends = sorted(interval[1] for interval in intervals)
```
**Split the intervals into two independent sorted timelines** — every start time, and every end time.

This is the step that discards the pairing, and it's safe precisely because rooms are interchangeable: the sweep only needs to know *when* something starts and *when* something ends, never which belongs to which.

[Generator expressions](../syntax/generator-expressions.md) rather than list comprehensions, so `sorted()` consumes the values without materializing an intermediate list first.
→ [generator-expressions](../syntax/generator-expressions.md) · [sorting-key](../syntax/sorting-key.md) · [list-basics](../syntax/list-basics.md)

```python
start_ptr = 0
end_ptr = 0
rooms = 0
max_rooms = 0
```
Four pieces of state:

- **`start_ptr` / `end_ptr`** — independent cursors into the two timelines.
- **`rooms`** — how many meetings are in progress right now. This rises and falls.
- **`max_rooms`** — the peak, which never falls. **That separation is essential** — the answer is the maximum concurrency, not the final one.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
while start_ptr < len(starts):
```
**Loop until every meeting has started** — not until both arrays are exhausted.

That's deliberate: once all meetings have begun, the remaining ends can only *decrease* `rooms`, so they can't affect the peak. Draining them would be wasted work.

It also guarantees `end_ptr` never runs past the array: each iteration advances exactly one pointer, and `end_ptr` can only advance when some start is still pending — so `end_ptr` stays strictly behind `start_ptr`, hence within bounds. **No explicit guard on `end_ptr` is needed.**
→ [while-loop](../syntax/while-loop.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
    if starts[start_ptr] < ends[end_ptr]:
        rooms += 1
        start_ptr += 1
        max_rooms = max(max_rooms, rooms)
```
**A meeting starts before the earliest pending one ends** — so no room is free and a new one must open.

Increment `rooms`, advance the start cursor, and update the peak. The peak is recorded **only here**, because `rooms` can only reach a new maximum immediately after an increment.

**Strict `<`** is the tie-break: if a start and an end coincide, this is false and the `else` branch releases the room first, letting it be reused. That's what makes `[[1,5],[5,9]]` answer 1.
→ [comparison-operators](../syntax/comparison-operators.md) · [min-max-key](../syntax/min-max-key.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
    else:
        rooms -= 1
        end_ptr += 1
```
**A meeting ends at or before the next one starts** — a room frees up.

Decrement `rooms` and advance the end cursor. No `max` update here, since releasing a room can never raise the peak.

Note the loop makes exactly one pointer move per iteration, which is what keeps the whole sweep linear.
→ [elif-else](../syntax/elif-else.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
return max_rooms
```
The greatest number of simultaneous meetings — and therefore the minimum number of rooms.
→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:

        starts = sorted(interval[0] for interval in intervals)
        ends = sorted(interval[1] for interval in intervals)

        start_ptr = 0
        end_ptr = 0
        rooms = 0
        max_rooms = 0

        while start_ptr < len(starts):
            if starts[start_ptr] < ends[end_ptr]:
                rooms += 1
                start_ptr += 1
                max_rooms = max(max_rooms, rooms)
            else:
                rooms -= 1
                end_ptr += 1

        return max_rooms
```
</details>

**Trace it** — `intervals = [[0,30],[5,10],[15,20]]`

`starts = [0, 5, 15]`, `ends = [10, 20, 30]`

| step | `starts[sp]` | `ends[ep]` | `start < end`? | action | `rooms` | `max_rooms` |
|---|---|---|---|---|---|---|
| 1 | **0** | 10 | 0 < 10 ✓ | start → open a room | **1** | **1** |
| 2 | **5** | 10 | 5 < 10 ✓ | start → open a room | **2** | **2** |
| 3 | **15** | 10 | 15 < 10 ✗ | end → free a room | 1 | 2 |
| 4 | **15** | 20 | 15 < 20 ✓ | start → open a room | **2** | 2 |
| — | `start_ptr = 3` | — | loop ends | — | — | — |

Return **2** ✅

Step 3 is the mechanism in miniature: the meeting ending at 10 (`[5,10]`) releases its room *before* the meeting starting at 15 claims one — so step 4 **reuses** that room rather than opening a third. The algorithm never knows or cares that `[15,20]` inherited `[5,10]`'s room; it just counts.

And notice the loop stopped with `ends` only partly consumed. The two remaining ends would take `rooms` down to 0, but the peak was already recorded — draining them would change nothing.

**And the tie case** — `intervals = [[1,5],[5,9]]`:

`starts = [1, 5]`, `ends = [5, 9]`

| step | `starts[sp]` | `ends[ep]` | `start < end`? | action | `rooms` | `max_rooms` |
|---|---|---|---|---|---|---|
| 1 | 1 | 5 | 1 < 5 ✓ | start | **1** | **1** |
| 2 | **5** | **5** | **5 < 5 ✗** | **end → free a room** | 0 | 1 |
| 3 | 5 | 9 | 5 < 9 ✓ | start (reusing) | 1 | 1 |

Return **1** ✅

Step 2 is where the strict `<` earns its keep. With `<=`, the start would have claimed a room while the other was still counted as occupied, giving `rooms = 2` and a wrong answer of **2**. **The tie-break is one character, and it decides the result.**

**And a three-deep case** — `intervals = [[1,10],[2,7],[3,19],[8,12],[10,20],[11,30]]`:

`starts = [1,2,3,8,10,11]`, `ends = [7,10,12,19,20,30]`

| step | start | end | action | `rooms` | `max_rooms` |
|---|---|---|---|---|---|
| 1 | 1 | 7 | start | 1 | 1 |
| 2 | 2 | 7 | start | 2 | 2 |
| 3 | 3 | 7 | start | **3** | **3** |
| 4 | 8 | 7 | end | 2 | 3 |
| 5 | 8 | 10 | start | 3 | 3 |
| 6 | 10 | 10 | **end** (tie) | 2 | 3 |
| 7 | 10 | 12 | start | 3 | 3 |
| 8 | 11 | 12 | start | **4** | **4** |

Return **4** ✅ — the peak occurs at time 11, with `[3,19]`, `[8,12]`, `[10,20]`, and `[11,30]` all running.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n log n)</summary>

**O(n log n)**, dominated by the two sorts.

- **Building and sorting `starts`** — extracting n values and sorting → **O(n log n)**.
- **Building and sorting `ends`** — same → **O(n log n)**.
- **The two-pointer sweep** — each iteration advances exactly one of the two pointers, and together they advance at most **2n** times → **O(n)**.
- Total: **O(n log n)**.

At n = 10⁴ that's roughly 2 × 1.4 × 10⁵ comparisons. Instant.

**As everywhere in this unit, the sweep is linear and the sort is the cost.** Two sorts rather than one doesn't change the class — it's a constant factor.

**Against the alternatives:**
- Simulating room assignment naively is **O(n²)** — scanning the room list per meeting.
- The heap version is also **O(n log n)**: one sort by start, plus n pushes and up to n pops at O(log n) each. **Same bound**, so the choice between them is about what else you need — the heap models rooms explicitly, the two-pointer version just counts.
- The timeline array is **O(n + T)** with T = 10⁶, worse in both time and space.

**Can you beat O(n log n)?** Not with comparison sorting. Times are bounded by 10⁶, so a counting sort on the endpoints would give **O(n + T)** — but with T = 10⁶ ≫ n = 10⁴ that's a loss here. Only worth it if the time range were small relative to n.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** — two arrays of n integers each.

| Component | Space | Why |
|---|---|---|
| `starts`, `ends` | **O(n)** | n values apiece |
| Sorting workspace | **O(n)** | Timsort's temporary buffers |
| Four scalars | O(1) | The pointers and counters |

**Why this can't be O(1)** like [Meeting Rooms](252-meeting-rooms.md): that problem sorted the input in place and compared neighbours, needing nothing extra. Here you need the starts and ends in **two independently sorted orders**, which can't be represented by one in-place arrangement of the original array. **The moment you split the intervals into separate timelines, you've paid O(n).**

**The heap variant is also O(n)** — the heap can hold every meeting's end time if they all overlap. So both good solutions land in the same place.

**A note on the sweep-line generalization:** building explicit `(time, ±1)` event tuples and sorting them is O(n) space too, and it's what you'd reach for if events carried more information — weights, types, identifiers. For this problem the two-array split is the leaner form of the same idea.

**What you'd need beyond this:** to report *which meeting is in which room*, use the heap version and store `(end_time, room_id)` — the popped entry tells you which room just freed up. The counting version discards that by design.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The key reframing is that the answer is just the maximum number of meetings running simultaneously — I never need to decide *which* room each meeting goes in, only count how many are needed at the busiest instant. And that peak is achievable, because whenever I open a new room it's exactly a moment when every existing room is busy. So I stop thinking about intervals and think about events: a start is +1, an end is −1. I sort all starts and all ends into two separate arrays — which is legal because rooms are interchangeable, so it doesn't matter which meeting frees a room — then walk both with two pointers, keeping a running count and its maximum. The tie-break matters: when a meeting ends exactly as another starts, the end must be processed first so the room gets reused, and that's encoded by a strict `<` in the comparison. O(n log n) from the sorts, O(n) space. A min-heap of end times is an equivalent alternative, and I'd prefer it if I also needed the actual room assignments."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why is the peak concurrency the answer?" | It's a lower bound because those meetings genuinely coexist. And it's achievable, because you only ever open a new room when all existing ones are busy — so rooms in use always equals meetings in progress. |
| "Why can you separate starts from ends?" | Rooms are interchangeable. The sweep only needs the chronological sequence of +1 and −1 moments; which meeting caused which is irrelevant. |
| "What breaks with `<=` instead of `<`?" | Touching meetings would each claim a room — `[[1,5],[5,9]]` would return 2 instead of 1. Ends must win ties so the room is released before being reclaimed. |
| "Solve it with a heap." | Sort by start. For each meeting, pop all end times ≤ its start, then push its own end. The heap size is the rooms in use; track the max. Same O(n log n), and it models rooms explicitly. |
| "Which meeting goes in which room?" | Use the heap version with `(end_time, room_id)` entries — popping tells you which room freed up. The counting version deliberately discards this. |
| "Why not simulate room assignment directly?" | You'd scan the room list per meeting — O(n²) — to compute information the question never asked for. |
| "What if you only needed to know whether one room suffices?" | That's [Meeting Rooms](252-meeting-rooms.md) — sort by start and check adjacent pairs, O(1) space. |
| "What if times were small integers?" | A counting sort or difference array over the time range would give O(n + T), which wins when T is small relative to n. Here T = 10⁶ ≫ n, so it loses. |

**Traps:**
- **`<=` instead of `<`** in the comparison — breaks the tie-break and over-counts rooms.
- **Returning `rooms` instead of `max_rooms`.** The running count falls back toward 0; only the peak is the answer.
- **Looping until both arrays are exhausted.** Harmless for correctness but pointless — after the last start, only decrements remain. It also risks an index error on `starts[start_ptr]` if written carelessly.
- **Guarding `end_ptr` unnecessarily**, or failing to notice it can't overrun. It stays behind `start_ptr` by construction.
- Sorting the intervals as pairs and trying to sweep them directly — you need the two timelines *independently* sorted.
- Updating `max_rooms` in the `else` branch. Releasing a room can never set a new peak.

**This same move shows up in:** [Meeting Rooms](252-meeting-rooms.md) (the same input asking whether the peak exceeds 1) · [Merge Intervals](56-merge-intervals.md) (sweeping sorted intervals, tracking a running frontier) · [Task Scheduler](621-task-scheduler.md) (counting resource contention over time rather than simulating a schedule) · [Kth Largest Element in a Stream](703-kth-largest-element-in-a-stream.md) (a heap maintaining a live set as items enter and leave) · [Minimum Interval to Include Each Query](1851-minimum-interval-to-include-each-query.md) (a sweep over sorted events with a heap holding what's currently active).

</details>

---
