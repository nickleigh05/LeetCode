# 1851. Minimum Interval to Include Each Query

**Hard** · [LeetCode](https://leetcode.com/problems/minimum-interval-to-include-each-query/)

[📖 17. Intervals lesson](../learning/17-intervals.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 17. Intervals problems](../rmap-practice/17-intervals.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

You're given `intervals`, where `intervals[i] = [left_i, right_i]` describes the **inclusive** interval, and an array of `queries`. For each query, find the **size of the smallest interval containing it** — where size is `right - left + 1`. If no interval contains the query, the answer is `-1`.

Return an array of the answers, **in the original query order**.

```
intervals = [[1,4],[2,4],[3,6],[4,4]], queries = [2,3,4,5]
        →  [3,3,1,4]
           query 2: [1,4] size 4, [2,4] size 3        → 3
           query 3: [1,4] 4, [2,4] 3, [3,6] 4         → 3
           query 4: all four contain it; [4,4] size 1 → 1
           query 5: only [3,6] size 4                 → 4

intervals = [[2,3],[2,5],[1,8],[20,25]], queries = [2,19,5,22]
        →  [2,-1,4,6]
```

**Constraints:** `1 <= intervals.length, queries.length <= 10⁵` · `1 <= left_i <= right_i <= 10⁷` · `1 <= queries[j] <= 10⁷`.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| answer **each** query | q independent-looking questions — but answering them independently is O(n) each, so **O(n·q) = 10¹⁰**. Dead |
| "**smallest** interval containing it" | Minimization, and the key is `right - left + 1`, not the endpoints themselves |
| intervals are **inclusive** | Containment is `left <= query <= right`, and size includes both ends — hence the `+1` |
| `-1` if none contains it | Some queries fall in gaps |
| answers in **original query order** | You may reorder the queries for processing, but you must **restore the order** at the end. That forces you to carry indices |
| `n, q <= 10⁵` | O((n+q) log n) is the target — that shape practically names a sort plus a heap |

The queries look independent, and that's the trap: answering each by scanning all intervals is O(n·q) = 10¹⁰.

**The unlock is that you're allowed to reorder the queries.** Nothing says you must answer them in the given order — only *report* them in that order. So sort them ascending and sweep.

Why does sorting help? Because containment has a **monotone** structure. Sweep a point rightward, and consider interval `[left, right]`:

- It becomes **eligible** once the query reaches `left`, and stays eligible from then on (as far as its left endpoint is concerned).
- It becomes **dead** once the query passes `right`, and can **never** be eligible again.

So as the sweep advances, intervals enter once and leave once. **Each interval is added and removed at most one time across the entire sweep**, which is what makes the total work near-linear instead of quadratic.

Now, at any moment during the sweep you're holding a set of intervals whose `left <= query`. Among those, you need:

1. only the ones with `right >= query` (the others have expired), and
2. the **smallest** one by size.

"Give me the minimum of a live set, with insertions" is exactly a **min-heap** keyed on size.

And here's the neat part: expired intervals don't have to be hunted down. Since you only ever need the *smallest* valid one, you can pop expired entries off the top **lazily** — discard them only when they surface as the minimum.

🤔 **Before you open the next section:** the heap is ordered by *size*, but the expiry test is on *end*. Why is it still safe to discard expired intervals only when they reach the top, rather than removing them the moment they expire?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| For each query, scan all intervals | Check containment, track the min size | **O(n · q)** | O(1) | ❌ 10¹⁰ |
| Sort intervals by size, scan per query | For each query, take the first containing interval | O(n·q) | O(n) | ❌ Same bound — sorting doesn't help without a sweep |
| Segment tree / interval tree | Range-minimum over interval sizes | O((n+q) log n) | O(n) | ⚠️ Correct, and the general tool — but far more machinery than needed |
| Offline sweep + **min-heap** | Sort both, add eligible intervals, lazily discard expired | **O((n+q) log n)** | O(n) | ✅ |
| Sweep + union-find | Sort intervals by size, assign each query the first interval that covers it, using DSU to skip answered queries | O((n+q) α) | O(q) | ✅ Faster, and a genuinely clever alternative |

**The decision:** an **offline sweep with a min-heap keyed on interval size**.

**"Offline" is the concept worth naming.** An *online* algorithm must answer each query as it arrives, in order. An *offline* one gets all queries up front and may reorder them. This problem is offline, and **the entire speedup comes from exploiting that** — sorting the queries turns q independent searches into one coordinated sweep.

Recognizing "I'm allowed to reorder the queries" is the insight; everything after it is standard machinery. That's a broadly reusable move: **whenever a problem hands you all the queries at once, ask whether processing them in a different order makes them share work.**

**Why a heap and not a sorted list.** The live set changes constantly — intervals are added as the sweep advances and removed as they expire — and you need the minimum from it repeatedly. A [heap](../data-structures/heap.md) gives O(log n) insertion and O(1) access to the minimum. A sorted list would give O(1) minimum but O(n) insertion.

**Why lazy deletion is safe** — the answer to section 1's question. The heap is ordered by **size**, so an expired interval can sit anywhere inside it, and finding it would cost O(n). But you never need to: **you only ever read the top.** If the top is expired, pop it — it's expired for this query and, since queries only increase, for every future query too, so discarding it permanently is correct. If the top is valid, it's the answer, and any expired entries buried deeper are irrelevant because they're larger than the top anyway.

This is the same lazy-deletion pattern as [Network Delay Time](743-network-delay-time.md) and [Min Cost to Connect All Points](1584-min-cost-to-connect-all-points.md): **keep stale entries and discard them on the way out**, because a heap can't cheaply remove from the middle.

**Why the queries must be sorted, not just the intervals.** Both pointers move forward monotonically. If queries arrived out of order, an interval discarded as "expired" might be needed again by a smaller later query — the whole one-pass structure would collapse.

**Why not the segment tree?** It handles the online version, where queries arrive one at a time and can't be reordered. Here you have them all, so the offline sweep is simpler and has a better constant.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
import heapq
```
Python's binary min-heap, operating on a plain list. `heappush` and `heappop` maintain the invariant in O(log n), and `heap[0]` is the minimum in O(1).
→ [heapq-module](../syntax/heapq-module.md) · [heap](../data-structures/heap.md)

```python
intervals.sort()
```
**Sort intervals by start** (then by end, since Python compares lists lexicographically — the tie-break is harmless here).

Sorting by start is what lets a single forward pointer add intervals as they become eligible: once the sweep passes an interval's left endpoint, it's a candidate, and everything after it in the array starts even later.
→ [sorting-key](../syntax/sorting-key.md) · [list-methods](../syntax/list-methods.md)

```python
sorted_queries = sorted(range(len(queries)), key=lambda i: queries[i])
```
**Sort the query *indices* by their values** — this is the line that makes the offline trick work while still returning answers in the original order.

Rather than sorting the query values (which would lose track of where each answer belongs), you sort `0, 1, 2, …` using each index's query value as the key. Iterating `sorted_queries` then visits queries in ascending value while `query_index` remembers the original slot.
→ [sorting-key](../syntax/sorting-key.md) · [lambda-functions](../syntax/lambda-functions.md) · [range-function](../syntax/range-function.md)

```python
heap = []   # (size, end)
result = [0] * len(queries)
i = 0
```
- **`heap`** — live intervals as `(size, end)` tuples. **Size first**, because tuple comparison orders element-wise and the heap must be ordered by size. `end` rides along so expiry can be tested without a separate lookup.
- **`result`** — preallocated so answers can be written to arbitrary positions as they're computed out of order.
- **`i`** — the interval cursor. It only ever moves forward across the whole sweep.
→ [list-basics](../syntax/list-basics.md) · [tuple-basics](../syntax/tuple-basics.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
for query_index in sorted_queries:
    query = queries[query_index]
```
Visit queries in **ascending value**, keeping the original index for the write-back.
→ [for-loop](../syntax/for-loop.md) · [list-basics](../syntax/list-basics.md)

```python
    while i < len(intervals) and intervals[i][0] <= query:
        left, right = intervals[i]
        heapq.heappush(heap, (right - left + 1, right))
        i += 1
```
**Add every newly-eligible interval.** An interval qualifies once its `left` is at or before the current query.

`i` **never resets** — it advances monotonically across all queries, which is why the total pushes across the whole run are bounded by n rather than n per query. **That's the difference between O((n+q) log n) and O(n·q log n).**

`right - left + 1` is the inclusive size, and the `+1` matters: `[4,4]` has size 1, not 0. Getting it wrong shifts every answer.
→ [while-loop](../syntax/while-loop.md) · [tuple-unpacking](../syntax/tuple-unpacking.md) · [heapq-module](../syntax/heapq-module.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
    while heap and heap[0][1] < query:
        heapq.heappop(heap)
```
**Lazy deletion.** `heap[0][1]` is the smallest-by-size interval's **end**. If that end is before the query, the interval no longer contains it — discard it.

Popping repeatedly is necessary because several expired intervals can be stacked at the top. And discarding is **permanent**, which is safe precisely because queries are processed in ascending order: an interval too small for this query is too small for every query still to come.

Expired intervals deeper in the heap are simply left there. They cost nothing, because they'll only ever be examined if they reach the top — and if they do, this loop removes them.
→ [while-loop](../syntax/while-loop.md) · [heap](../data-structures/heap.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
    result[query_index] = heap[0][0] if heap else -1
```
**Read the answer off the top.** After the pruning loop, the heap's minimum is the smallest interval that both started early enough and hasn't ended — the smallest containing interval.

An empty heap means no interval covers this query → `-1`.

Writing to `result[query_index]` rather than appending is what restores the original ordering.
→ [ternary-expression](../syntax/ternary-expression.md) · [list-basics](../syntax/list-basics.md)

```python
return result
```
All q answers, in the order they were asked.
→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
import heapq

class Solution:
    def minInterval(self, intervals: List[List[int]], queries: List[int]) -> List[int]:

        intervals.sort()
        sorted_queries = sorted(range(len(queries)), key=lambda i: queries[i])

        heap = []   # (size, end)
        result = [0] * len(queries)
        i = 0

        for query_index in sorted_queries:
            query = queries[query_index]

            while i < len(intervals) and intervals[i][0] <= query:
                left, right = intervals[i]
                heapq.heappush(heap, (right - left + 1, right))
                i += 1

            while heap and heap[0][1] < query:
                heapq.heappop(heap)

            result[query_index] = heap[0][0] if heap else -1

        return result
```
</details>

**Trace it** — `intervals = [[1,4],[2,4],[3,6],[4,4]]`, `queries = [2,3,4,5]`

Sorted intervals: `[[1,4], [2,4], [3,6], [4,4]]`. Queries are already ascending, so `sorted_queries = [0,1,2,3]`.

| query | intervals pushed (`size, end`) | heap after pushes | expired pops | heap top | answer |
|---|---|---|---|---|---|
| **2** | `[1,4]` → (4,4)<br>`[2,4]` → (3,4) | `(3,4), (4,4)` | none (ends 4 ≥ 2) | **(3,4)** | **3** |
| **3** | `[3,6]` → (4,6) | `(3,4), (4,4), (4,6)` | none | **(3,4)** | **3** |
| **4** | `[4,4]` → **(1,4)** | `(1,4), (3,4), (4,4), (4,6)` | none (ends 4 ≥ 4) | **(1,4)** | **1** |
| **5** | none left | same | `(1,4)`: 4 < 5 ✗ pop<br>`(3,4)`: 4 < 5 ✗ pop<br>`(4,4)`: 4 < 5 ✗ pop | **(4,6)** | **4** |

Return **[3,3,1,4]** ✅

Query 4 shows why the heap is keyed on **size**: `[4,4]` has size 1 and jumps straight to the top ahead of intervals that were added earlier and are still valid.

Query 5 is lazy deletion doing its job — **three** expired entries surface in a row and are popped, revealing `(4,6)` as the only survivor. Notice they were never removed at the moment they expired; they simply waited at the top until a query needed them gone.

**And the `-1` case** — `intervals = [[2,3],[2,5],[1,8],[20,25]]`, `queries = [2,19,5,22]`:

Sorted intervals: `[[1,8], [2,3], [2,5], [20,25]]`. Query values sorted: 2, 5, 19, 22 → `sorted_queries = [0, 2, 1, 3]`.

| query (orig. index) | pushed | heap top after pruning | answer → slot |
|---|---|---|---|
| **2** (idx 0) | `[1,8]`→(8,8), `[2,3]`→(2,3), `[2,5]`→(4,5) | **(2,3)** | **2** → `result[0]` |
| **5** (idx 2) | none | pop (2,3): 3 < 5 → **(4,5)** | **4** → `result[2]` |
| **19** (idx 1) | none | pop (4,5): 5<19; pop (8,8): 8<19 → **empty** | **−1** → `result[1]` |
| **22** (idx 3) | `[20,25]`→(6,25) | **(6,25)** | **6** → `result[3]` |

Return **[2,−1,4,6]** ✅

This one shows the index bookkeeping earning its place: the queries were processed in the order 2, 5, 19, 22 — **not** the order they were asked — yet each answer landed in its original slot.

</details>

<details>
<summary><b>4 · Time complexity</b> — O((n + q) log n)</summary>

**O(n log n + q log q + (n + q) log n)** = **O((n + q) log n)** for comparable n and q.

Broken down:

- **Sorting the intervals** — **O(n log n)**.
- **Sorting the query indices** — **O(q log q)**.
- **The sweep** — the outer loop runs **q** times, and inside it:
  - Each interval is pushed **exactly once across the entire run**, because `i` never resets → **n** pushes total, at O(log n) each.
  - Each interval is popped **at most once ever**, since deletion is permanent → at most **n** pops, at O(log n) each.
  - The heap-top read is **O(1)**.

**The amortized argument is the crux.** The two inner `while` loops look like they could each run n times per query, suggesting O(n·q). They can't: across the *whole* algorithm the pushes total n and the pops total n, because both are one-way operations. **The inner loops are amortized O(1) per query.**

At the limits, (10⁵ + 10⁵) × 17 ≈ **3.4 × 10⁶** heap operations. Comfortable.

**Against brute force:** scanning every interval per query is **O(n·q)** = 10¹⁰. The saving comes entirely from processing the queries **offline**, in sorted order, so they share the sweep instead of each repeating it.

**Faster?** Yes — the **union-find** variant. Sort intervals by size ascending, and for each interval assign it to every not-yet-answered query inside its range, using a DSU to jump over already-answered queries in near-constant time. That's **O((n + q) α)** after sorting, which is effectively linear. More clever, harder to get right; worth naming as the optimal approach.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n + q)</summary>

**O(n + q)**.

| Component | Space | Why |
|---|---|---|
| `heap` | **O(n)** | Can hold every interval at once if they all overlap a single query — and lazy deletion means expired entries linger |
| `sorted_queries` | **O(q)** | One index per query |
| `result` | **O(q)** | The output |
| Sorting workspace | O(n + q) | Timsort's buffers |

**The cost of lazy deletion** is worth stating explicitly: expired intervals stay in the heap until they happen to reach the top, so the heap can be larger than the set of genuinely-live intervals. That's the trade — **O(log n) amortized time in exchange for carrying dead weight**. Eager deletion would need a different structure (a balanced tree or an indexed heap) and buy nothing asymptotically.

**Why `result` is preallocated** rather than appended to: answers are produced in *sorted query order* but must be stored in *original query order*. Preallocating `[0] * len(queries)` allows the scattered writes. Appending would produce the answers sorted by query value — a subtly wrong output that passes the simplest test cases where the queries happen to already be ascending.

**The union-find variant** uses **O(q)** for the DSU and doesn't need a heap at all, so it's leaner as well as faster — the usual trade being implementation difficulty.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Answering each query independently is O(n·q), which is 10¹⁰ — too slow. But this is an *offline* problem: I'm given all the queries up front, so I can reorder them. Sorting the queries ascending lets them share one sweep. As the sweep moves right, an interval becomes eligible when the query passes its left endpoint and dies when the query passes its right endpoint — each interval enters and leaves exactly once. I keep the live intervals in a min-heap keyed on size, so the answer is whatever's on top. Expired intervals are discarded lazily: I only prune from the top, which is safe because I only ever read the top, and because queries only increase, so an interval that's expired now is expired forever. I sort query *indices* rather than values so I can write each answer back to its original slot. O((n+q) log n) — the inner loops look quadratic but each interval is pushed and popped at most once across the entire run, so they're amortized O(1) per query."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "What makes this offline?" | All queries are known up front, so they can be reordered. An online version — queries arriving one at a time — would need a segment tree or interval tree instead. |
| "Why is lazy deletion safe?" | You only ever read the heap's top. If it's expired, pop it; since queries only increase, it's expired permanently. Expired entries buried deeper are larger than the top and never consulted. |
| "Why sort query indices instead of values?" | The answers must be returned in the original order. Sorting indices preserves the mapping so each result can be written to its original slot. |
| "Why is the heap keyed on size, not end?" | The question asks for the *smallest* containing interval. Size must be the ordering key; `end` rides along only so expiry can be tested at the top. |
| "Aren't the inner while loops O(n) per query?" | No — `i` never resets and popped intervals never return, so across the whole run there are at most n pushes and n pops. Amortized O(1) per query. |
| "Can you do better?" | Yes — sort intervals by size and use union-find to assign each interval to all unanswered queries in its range, skipping answered ones. O((n+q) α), effectively linear. |
| "What if queries arrived one at a time?" | You'd need an online structure — a segment tree over coordinates storing minimum interval size, or an interval tree. O(log n) per query. |
| "Why `right - left + 1`?" | The intervals are inclusive, so `[4,4]` has size 1. Omitting the `+1` shifts every answer by one. |

**Traps:**
- **Sorting query values instead of indices.** The answers come out in sorted order rather than the requested order — and it passes any test where the queries were already ascending.
- **Resetting `i` per query.** Destroys the amortization and makes it O(n·q).
- **Forgetting the `+1` in the size.** Every answer is off by one.
- **Ordering the heap tuple as `(end, size)`.** The heap would return the earliest-ending interval, not the smallest.
- **Pruning before pushing.** New intervals must be added first, or a valid small interval could be missed for this query.
- Trying to remove expired intervals eagerly from the middle of the heap — O(n) per removal, and unnecessary.
- Appending to `result` instead of indexing into it.

**This same move shows up in:** [Meeting Rooms II](253-meeting-rooms-ii.md) (a sweep over sorted events maintaining a live set) · [Network Delay Time](743-network-delay-time.md) (lazy deletion — keep stale heap entries and discard them on pop) · [Min Cost to Connect All Points](1584-min-cost-to-connect-all-points.md) (the same lazy-deletion pattern in Prim's) · [Merge Intervals](56-merge-intervals.md) (sorting intervals so a single forward pass suffices) · [Sliding Window Maximum](239-sliding-window-maximum.md) (maintaining the extreme of a window as elements enter and expire).

</details>

---
