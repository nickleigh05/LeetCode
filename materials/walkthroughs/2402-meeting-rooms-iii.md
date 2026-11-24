# 2402. Meeting Rooms III

**Hard** · [LeetCode](https://leetcode.com/problems/meeting-rooms-iii/) · [Solution file (no hints)](../../problems/2000-2499/2402.py)

[📖 16. Intervals lesson](../learning/17-intervals.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 16. Intervals problems](../rmap-practice/16-intervals.md)

---

There are `n` rooms numbered `0..n-1`. `meetings[i] = [start, end)` are meetings with **unique start times**. They are allocated as follows:

1. Each meeting takes the **lowest-numbered free room** at its start time.
2. If no room is free, the meeting **waits** for the room that frees up **earliest**. It keeps its **duration** (`end − start`) and starts as soon as that room is free.
3. When a room frees up and several meetings are waiting, the one with the **earliest original start time** goes first.

Return the room number that **held the most meetings** (the lowest number on ties).

```
n = 2, meetings = [[0, 10], [1, 5], [2, 7], [3, 4]]   →  0
n = 3, meetings = [[1, 20], [2, 10], [3, 5], [4, 9], [6, 8]]   →  1
```

**Constraints:** `1 <= n <= 100` · `1 <= meetings.length <= 10⁵` · `0 <= start < end <= 5 * 10⁵` · all starts distinct

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "lowest-numbered **free** room" | You need the minimum over a **set of free rooms** that changes: a **min-heap of free room ids** |
| "if none free, wait for the **earliest** to finish" | You need the minimum **end time** among busy rooms: a **min-heap of `(end_time, room)`** |
| delayed meeting keeps its **duration** | New end = `earliest_end + duration` |
| earlier original start goes first | Process meetings **sorted by start**, one at a time. The queue-order rule is then automatic |
| "most meetings, lowest on ties" | Count per room, then pick with a left-to-right scan |

**A simulation with two heaps.** Sort the meetings by start. For each meeting:

1. **Release rooms** whose end time is `<= start`: move them from the busy heap to the free heap.
2. If a room is free: take the **smallest id**, schedule `[start, end)`.
3. Otherwise: pop the busy room with the **earliest end** and schedule the meeting right after it: `[old_end, old_end + duration)`.
4. Increment that room's count.

🤔 **Before you open the next section:** when a meeting has to wait, which room does it get: the lowest-numbered one, or the one that frees up first? Why does a tie in end time get resolved by room number for free?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Time | Verdict |
|---|---|---|
| Scan all `n` rooms for every meeting | O(m · n) | ⚠️ `10⁵ × 100 = 10⁷`: acceptable here, but doesn't scale |
| **Two [heaps](../data-structures/heap.md): free rooms by id, busy rooms by `(end, id)`** | **O(m log n)** | ✅ |

**The decision: two min-heaps.**

- `free`: a heap of room numbers, so `heappop` always returns the **lowest-numbered** free room.
- `busy`: a heap of `(end_time, room)`, so `heappop` returns the room that frees **earliest**, and Python's tuple comparison breaks end-time ties by **lowest room number**. That matches the rule exactly.

Sorting by start and processing in order handles rule 3 (earlier-start meetings are scheduled first, so they claim a room that frees up first).

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
meetings.sort()
free = list(range(n))
heapq.heapify(free)
busy = []
count = [0] * n
```

Sort by start time. All rooms begin free. A list `0..n-1` is already a valid min-heap, and `heapify` makes the intent explicit. `busy` holds `(end_time, room)`, and `count[r]` is how many meetings room `r` has hosted.
→ [list-methods](../syntax/list-methods.md) · [heapq-module](../syntax/heapq-module.md) · [heap](../data-structures/heap.md)

```python
for start, end in meetings:
    duration = end - start
    while busy and busy[0][0] <= start:
        _, room = heapq.heappop(busy)
        heapq.heappush(free, room)
```

For each meeting, first **release every room that has finished by `start`** (end time at or before the start). They return to the free heap, so the lowest-numbered one becomes available again.
→ [for-loop](../syntax/for-loop.md) · [tuple-unpacking](../syntax/tuple-unpacking.md) · [while-loop](../syntax/while-loop.md)

```python
    if free:
        room = heapq.heappop(free)
        heapq.heappush(busy, (end, room))
```

A free room exists: take the **lowest-numbered** one and run the meeting exactly as scheduled.
→ [if-return](../syntax/if-return.md)

```python
    else:
        earliest_end, room = heapq.heappop(busy)
        heapq.heappush(busy, (earliest_end + duration, room))
    count[room] += 1
```

**Everything is busy.** Wait for the room that frees up first (and the lowest number among ties). The meeting starts at `earliest_end`, so it finishes at `earliest_end + duration`. Push the room back with its new end time and count the meeting.

```python
best = 0
for room in range(1, n):
    if count[room] > count[best]:
        best = room
return best
```

A strict `>` scanning from the lowest room keeps the **lowest-numbered** room on ties.
→ [range-function](../syntax/range-function.md) · [comparison-operators](../syntax/comparison-operators.md)

<details>
<summary>The whole thing together</summary>

```python
import heapq


class Solution:
    def mostBooked(self, n: int, meetings: List[List[int]]) -> int:
        meetings.sort()
        free = list(range(n))
        heapq.heapify(free)
        busy = []
        count = [0] * n

        for start, end in meetings:
            duration = end - start

            while busy and busy[0][0] <= start:
                _, room = heapq.heappop(busy)
                heapq.heappush(free, room)

            if free:
                room = heapq.heappop(free)
                heapq.heappush(busy, (end, room))
            else:
                earliest_end, room = heapq.heappop(busy)
                heapq.heappush(busy, (earliest_end + duration, room))

            count[room] += 1

        best = 0
        for room in range(1, n):
            if count[room] > count[best]:
                best = room
        return best
```

</details>

**Trace it.** `n = 2`, `meetings = [[0,10],[1,5],[2,7],[3,4]]`:

| Meeting | Free rooms | Action | `busy` after | `count` |
|---|---|---|---|---|
| `[0,10]` | 0, 1 | room 0 | `(10,0)` | `[1,0]` |
| `[1,5]` | 1 | room 1 | `(5,1)`, `(10,0)` | `[1,1]` |
| `[2,7]` | none | wait for `(5,1)`: runs `[5,10)` in room 1 | `(10,0)`, `(10,1)` | `[1,2]` |
| `[3,4]` | none | earliest is `(10,0)`: runs `[10,11)` in room 0 | `(10,1)`, `(11,0)` | `[2,2]` |

Counts tie at 2 → the lowest room, **0** ✅.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(m log m + m log n)</summary>

Sorting is **O(m log m)** (`m` = meetings). Each meeting does a handful of heap operations on heaps of size at most `n`: **O(log n)**, and every room is released at most once per meeting it hosted. Total **O(m log m)**.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n):** the two heaps together hold exactly `n` rooms, plus the `count` array. (Sorting may use O(m).)

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "I process meetings in start order. I keep a min-heap of free room numbers, so I always get the lowest, and a min-heap of busy rooms keyed by `(end_time, room)`, so the room that frees first comes out, and ties go to the lowest room automatically. For each meeting I first release any room whose end time is at or before the start. If one's free I use the lowest. If none is, I take the earliest-finishing room and delay the meeting to start then, keeping its duration. I count meetings per room and return the lowest room with the maximum. O(m log m)."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why must a delayed meeting keep its duration?" | The problem says so: its new end is `old_end + (end − start)` |
| "Why does sorting by start enforce rule 3?" | Waiting meetings take rooms in the order they were scheduled, which is start order |
| "How's it different from Meeting Rooms II?" | [Meeting Rooms II](253-meeting-rooms-ii.md) asks only for the minimum rooms needed. III simulates actual allocation |
| "Why a tuple `(end, room)`?" | Python compares tuples element-wise, so equal end times fall back to the lowest room |
| "Without the `free` heap?" | Scan rooms 0..n-1 for the first free one: O(n) each, fine for `n <= 100` |

**Traps:**

- **Delaying with `end + something`** instead of `earliest_end + duration`.
- **Forgetting to release finished rooms first.** Rooms never become free.
- **Using `<` instead of `<=`** when releasing. A room ending exactly at `start` is free.
- **Choosing the wrong room on ties** in the final scan (use strict `>`).

**This same move shows up in:** [Meeting Rooms II](253-meeting-rooms-ii.md) · [Car Pooling](1094-car-pooling.md) · [Single-Threaded CPU](1834-single-threaded-cpu.md) (heaps driving a simulation).

</details>

---
