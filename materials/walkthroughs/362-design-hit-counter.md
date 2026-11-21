# 362. Design Hit Counter

**Medium** · 🔒 Premium · [LeetCode](https://leetcode.com/problems/design-hit-counter/) · [Solution file (no hints)](../../problems/0001-0499/362.py)

[📖 03. Sliding Window lesson](../learning/03-sliding-window.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 03. Sliding Window problems](../rmap-practice/03-sliding-window.md)

---

Design a hit counter that counts the number of hits received in the **past 5 minutes** (the past **300 seconds**).

- `HitCounter()`: initialise the counter.
- `hit(timestamp)`: record a hit at `timestamp` (in seconds). Several hits can share a timestamp.
- `getHits(timestamp)`: return the number of hits in the past 300 seconds, meaning hits with times in **`(timestamp − 300, timestamp]`**.

Calls arrive in **chronological order**: `timestamp` never decreases.

```
hit(1), hit(2), hit(3)
getHits(4)    →  3
hit(300)
getHits(300)  →  4
getHits(301)  →  3      (the hit at 1 is now 300 seconds old and drops out)
```

**Constraints:** `1 <= timestamp <= 2·10⁹` · timestamps are non-decreasing · at most 300 calls in total

**Follow-up:** what if the number of hits per second could be **enormous**? Does your design scale?

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "past 300 seconds" | A **sliding time window** of width 300 |
| window `(t − 300, t]` | A hit at exactly `t − 300` is **out**. `getHits(301)` excludes the hit at 1 |
| **chronological** calls | Hits arrive in order, so the oldest hit is always at the front. That's what makes a queue work |
| several hits per timestamp | Don't key a dict on timestamp and overwrite. Count them |
| follow-up: huge hit rates | Storing every hit individually won't scale. You'll want one counter per second |

**Why a queue.** Hits come in time order and leave in time order (the oldest expire first). First in, first out is a **queue**. When asked for the count:

1. Drop hits from the **front** while they're too old (`<= t − 300`).
2. Whatever remains is the window, so return its length.

Each hit is added once and removed once, so this is efficient even though `getHits` might drop many at a time.

**The follow-up's answer: fixed buckets.** With millions of hits a second, storing each one is wasteful. Use **300 buckets**, one per second modulo 300. Each bucket remembers which second it holds and a count. That's constant memory, whatever the hit rate.

🤔 **Before you open the next section:** at `getHits(301)`, the oldest hit is at time 1. Should it be removed, and what exact comparison decides?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | `hit` | `getHits` | Space | Verdict |
|---|---|---|---|---|
| List of all hits, filter on query | O(1) | O(all hits ever) | O(all hits) | ❌ Old hits are never discarded |
| **Deque of timestamps** | O(1) | **O(1) amortised** | O(hits in window) | ✅ Simplest correct answer |
| 300 circular buckets | O(1) | O(300) = O(1) | **O(300)** | ✅ The follow-up answer |
| Sorted list + binary search | O(1) append | O(log n) | O(all hits) | ⚠️ Never frees memory |

**The decision: a [deque](../data-structures/deque.md) used as a queue**, with old hits expiring from the front.

This is a [sliding window](../learning/03-sliding-window.md) over time instead of over array indices. The right edge is "now" and moves forward on each call. The left edge moves forward by popping expired hits.

**The bucket version, ready for the follow-up** (a [circular buffer](../data-structures/circular-buffer.md)):

```python
class HitCounter:
    def __init__(self):
        self.times = [0] * 300
        self.counts = [0] * 300

    def hit(self, timestamp):
        i = timestamp % 300
        if self.times[i] != timestamp:      # bucket holds an old second → reset it
            self.times[i] = timestamp
            self.counts[i] = 0
        self.counts[i] += 1

    def getHits(self, timestamp):
        return sum(self.counts[i] for i in range(300)
                   if timestamp - self.times[i] < 300)
```

Memory is fixed at 600 integers, however many hits arrive per second. Many hits in the same second just increase one counter.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
def __init__(self):
    self.hits = deque()
```

The queue of hit timestamps, oldest at the front. `deque` gives O(1) pops from the left. A plain list's `pop(0)` is O(n).
→ [init-method](../syntax/init-method.md) · [deque-basics](../syntax/deque-basics.md)

```python
def hit(self, timestamp: int) -> None:
    self.hits.append(timestamp)
```

**Record the hit at the back.** Timestamps never decrease, so the queue stays sorted with no extra work. Repeated timestamps are just repeated entries.
→ [class-basics](../syntax/class-basics.md)

```python
def getHits(self, timestamp: int) -> int:
    while self.hits and self.hits[0] <= timestamp - 300:
        self.hits.popleft()
```

**Slide the window's left edge.** A hit at `h` is out of the window if `h <= timestamp − 300`, which is the same as `timestamp − h >= 300`. Pop from the front until the oldest hit is recent enough.

`self.hits` is checked first, so `self.hits[0]` is never read on an empty deque.
→ [while-loop](../syntax/while-loop.md) · [logical-operators](../syntax/logical-operators.md)

```python
    return len(self.hits)
```

Everything left in the deque is inside `(timestamp − 300, timestamp]`. `len` on a deque is O(1).

<details>
<summary>The whole thing together</summary>

```python
from collections import deque

class HitCounter:

    def __init__(self):
        self.hits = deque()

    def hit(self, timestamp: int) -> None:
        self.hits.append(timestamp)

    def getHits(self, timestamp: int) -> int:
        while self.hits and self.hits[0] <= timestamp - 300:
            self.hits.popleft()
        return len(self.hits)
```

</details>

**Trace it.** The example:

| Call | Deque before | Expired (`<= t − 300`) | Deque after | Returns |
|---|---|---|---|---|
| `hit(1)`, `hit(2)`, `hit(3)` | `[]` | — | `[1, 2, 3]` | — |
| `getHits(4)` | `[1, 2, 3]` | `<= −296`: none | `[1, 2, 3]` | **3** |
| `hit(300)` | `[1, 2, 3]` | — | `[1, 2, 3, 300]` | — |
| `getHits(300)` | | `<= 0`: none | `[1, 2, 3, 300]` | **4** |
| `getHits(301)` | | `<= 1`: **1** | `[2, 3, 300]` | **3** ✅ |

The hit at 1 drops out at exactly `t = 301`, because `301 − 1 = 300` is not strictly less than 300.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(1) amortised</summary>

- **`hit`:** O(1), a single append.
- **`getHits`:** O(1) **amortised**. One call might pop many hits, but each hit is popped at most once over the counter's lifetime. Spread across all calls, the total popping work is at most the number of hits.

**Bucket version:** `hit` is O(1) and `getHits` is O(300), which is constant, whatever the number of hits.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(hits in the window)</summary>

**Deque:** O(k), where k is the number of hits in the last 300 seconds. Expired hits are discarded, so memory doesn't grow forever. But at a million hits a second, that's 3·10⁸ timestamps.

**Buckets:** **O(300) = O(1)**, fixed, whatever the hit rate.

| | Space | Handles bursts? |
|---|---|---|
| **Deque** | O(hits in window) | Memory grows with the hit rate |
| Buckets | O(300) | ✅ Constant |

That's the trade-off the follow-up is asking about.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Hits arrive in time order and expire in time order, so a queue is the natural fit. `hit` appends the timestamp. `getHits` pops from the front while the oldest hit is at or before `timestamp − 300`, then returns the length. Each hit is pushed and popped once, so both are O(1) amortised. Memory is proportional to hits in the window. For the follow-up with huge hit rates, I'd switch to 300 buckets indexed by `timestamp % 300`, each storing its second and a count. That's constant memory, and `getHits` sums the buckets that are less than 300 seconds old."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Millions of hits per second?" | 300 circular buckets with `(time, count)` per slot. O(1) memory. |
| "Timestamps arrive out of order?" | The queue's sorted order breaks. Use a sorted structure, or buckets keyed by second, which don't care about order. |
| "Concurrent callers?" | Lock around updates, or use per-thread counters merged on read. Buckets with atomic increments scale best. |
| "Window size as a parameter?" | Replace 300 with `self.window`. Buckets need `window` slots. |
| "Rate limiter: allow at most N per window?" | The same deque, but in `hit`, expire old entries and reject if `len >= N`. That's the classic sliding-log rate limiter. |

**Traps:**

- **Using `<` instead of `<=` when expiring.** The window is `(t − 300, t]`, so a hit exactly 300 seconds old must go.
- **`list.pop(0)`.** O(n) per pop, which quietly makes expiry quadratic.
- **A dict of `{timestamp: count}` that never shrinks.** Memory grows forever.
- **Keying buckets on `timestamp % 300` without storing the time.** An old count from 300 seconds ago looks current.

**This same move shows up in:** [Sliding Window Maximum](239-sliding-window-maximum.md) (a deque where old entries leave from the front) · [Implement Queue using Stacks](232-implement-queue-using-stacks.md) (first in, first out as a design problem) · [Time Based Key-Value Store](981-time-based-key-value-store.md) (a class queried by timestamp) · [Online Stock Span](901-online-stock-span.md) (a stream processed one call at a time with amortised O(1)).

</details>

---
