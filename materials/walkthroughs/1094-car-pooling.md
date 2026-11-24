# 1094. Car Pooling

**Medium** · [LeetCode](https://leetcode.com/problems/car-pooling/) · [Solution file (no hints)](../../problems/1000-1499/1094.py)

[📖 09. Heap / Priority Queue lesson](../learning/09-heap-priority-queue.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 09. Heap / Priority Queue problems](../rmap-practice/09-heap-priority-queue.md)

---

A car has `capacity` empty seats and only drives **east**. `trips[i] = [passengers, from, to]` means `passengers` get in at kilometre `from` and get out at kilometre `to`. Return `True` if all trips can be completed without ever exceeding the capacity.

```
trips = [[2, 1, 5], [3, 3, 7]],  capacity = 4   →  False   (at km 3 there are 5 people)
trips = [[2, 1, 5], [3, 3, 7]],  capacity = 5   →  True
```

**Constraints:** `1 <= trips.length <= 1000` · `1 <= passengers <= 100` · `0 <= from < to <= 1000` · `1 <= capacity <= 10⁵`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "only drives east" | Positions only increase. A trip is the **interval** `[from, to)` |
| "pick up at `from`, drop off at `to`" | At `to`, the passengers have already left. Intervals are half-open: the seat is free at the drop-off kilometre |
| "never exceed capacity" | You need the **peak number of people on board at any one moment** |
| `to <= 1000` | The route is short and positions are small integers. An array over positions is feasible |

This is an "overlapping intervals" question in disguise: *what's the maximum overlap?* It has two classic solutions.

**Solution A, event sorting with a heap:** sort trips by start. Keep a min-heap of `(end, passengers)` for people currently on board. Before picking up at position `from`, drop everyone whose `end <= from`. Then add the new group and check the total.

**Solution B, difference array:** at each position, record `+passengers` where they board and `-passengers` where they leave. A running sum across positions is the load at that kilometre.

Since positions are bounded by 1000, B is simpler and faster.

🤔 **Before you open the next section:** with a difference array, where do you subtract the passengers, at `to` or at `to + 1`? What does "half-open interval" tell you?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Time | Space | Verdict |
|---|---|---|---|
| For each km, add up all trips covering it | O(1001 · n) | O(1) | ⚠️ ~10⁶ operations. Fine here but wasteful |
| Sort by start + min-heap of drop-offs | O(n log n) | O(n) | ✅ General: works for huge coordinates |
| **Difference array + running sum** | **O(n + R)** (`R` = 1001) | **O(R)** | ✅ Simplest |

**The decision: a difference array** (the idea behind [line sweep](../algorithms/line-sweep.md)). Write `+p` at the boarding position and `-p` at the drop-off position, then take a running sum. Each position's running sum is the number of people in the car **there**.

The heap version is worth knowing. If coordinates were up to `10⁹`, an array wouldn't fit and you'd sort and sweep instead (the same technique as [Meeting Rooms II](253-meeting-rooms-ii.md)).

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
diff = [0] * 1002
```

One slot per kilometre `0..1000`, plus a spare. `diff[k]` will hold "the *change* in passenger count at kilometre `k`".
→ [list-basics](../syntax/list-basics.md) · [constraints-cheatsheet](../guides/constraints-cheatsheet.md)

```python
for passengers, start, end in trips:
    diff[start] += passengers
    diff[end] -= passengers
```

Board at `start`, leave at `end`. Because the drop-off is registered **at `end` itself**, the running sum already excludes those passengers when we reach `end`, which is the half-open `[from, to)` rule. `+=` and `-=` handle several trips sharing the same kilometre.
→ [for-loop](../syntax/for-loop.md) · [tuple-unpacking](../syntax/tuple-unpacking.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
load = 0
for change in diff:
    load += change
    if load > capacity:
        return False
return True
```

Sweep west to east. `load` is the running total: passengers on board right after processing this kilometre's changes. Any kilometre over capacity fails the whole trip.
→ [if-return](../syntax/if-return.md) · [comparison-operators](../syntax/comparison-operators.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def carPooling(self, trips: List[List[int]], capacity: int) -> bool:
        diff = [0] * 1002

        for passengers, start, end in trips:
            diff[start] += passengers
            diff[end] -= passengers

        load = 0
        for change in diff:
            load += change
            if load > capacity:
                return False

        return True
```

</details>

**Trace it.** `trips = [[2, 1, 5], [3, 3, 7]]`, `capacity = 4`:

| km | `diff` | running `load` | Over 4? |
|---|---|---|---|
| 0 | 0 | 0 | |
| 1 | +2 | 2 | |
| 3 | +3 | **5** | **yes, return `False`** ✅ |

With `capacity = 5` the sweep continues: km 5 gives `-2` (load 3) and km 7 gives `-3` (load 0), so it returns `True`.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n + R)</summary>

One pass over the trips (**O(n)**) and one pass over the position array (**O(R)**, `R = 1001`). Together roughly 2000 steps. The heap version is O(n log n).

</details>

<details>
<summary><b>5 · Space complexity</b> — O(R)</summary>

**O(R)** for the difference array, a fixed 1002 integers here, so effectively O(1).

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The question is the maximum number of passengers on board at any kilometre. I'll use a difference array: add the passengers at their start, subtract them at their end, then take a running sum along the route. The drop-off is subtracted at `to` itself, so passengers leave before the next pickup there. If the running total ever exceeds capacity I return False. O(n + range) time."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Positions up to 10⁹?" | Sort the events (position, ±passengers) and sweep, or use a min-heap of drop-offs keyed by `end`. O(n log n) |
| "Why subtract at `to`, not `to + 1`?" | The interval is half-open: at `to` the passengers have left, and new ones can board in their seats |
| "Same pattern elsewhere?" | [Meeting Rooms II](253-meeting-rooms-ii.md) (max overlap = rooms needed) · [Meeting Rooms III](2402-meeting-rooms-iii.md) |
| "Return the *kilometre* where it overflows?" | Return `index` instead of `False` in the sweep |
| "Heap solution?" | Sort trips by start. Pop from a `(end, passengers)` min-heap while `end <= start`, then push the new group and compare the sum |

**Traps:**

- **Subtracting at `end + 1`.** It double-counts the passengers at their drop-off kilometre, so a valid trip fails.
- **Checking capacity only at the start of each trip.** That's fine in principle, but it requires processing in sorted order. The sweep avoids the issue.
- **An array that's too small.** `to` can be 1000, so you need index 1000.
- **Assuming trips are sorted.** They aren't.

**This same move shows up in:** [Meeting Rooms II](253-meeting-rooms-ii.md) · [Meeting Rooms](252-meeting-rooms.md) · [Employee Free Time](759-employee-free-time.md) · [My Calendar II](731-my-calendar-ii.md).

</details>

---
