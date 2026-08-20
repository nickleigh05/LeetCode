# 295. Find Median from Data Stream

**Hard** · [LeetCode](https://leetcode.com/problems/find-median-from-data-stream/) · [Solution file (no hints)](../../problems/0001-0499/295.py)

[📖 10. Heap / Priority Queue lesson](../learning/10-heap-priority-queue.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 10. Heap / Priority Queue problems](../rmap-practice/10-heap-priority-queue.md)

---

The **median** is the middle value in an ordered list. If the list has an even number of elements, it's the **average of the two middle values**.

Implement a class that supports:

- **`addNum(num)`** — add an integer from the data stream
- **`findMedian()`** — return the median of all elements added so far

```
addNum(1)
addNum(2)
findMedian()  →  1.5      ([1,2] → (1+2)/2)
addNum(3)
findMedian()  →  2.0      ([1,2,3] → 2)
```

**Constraints:** `-10⁵ <= num <= 10⁵` · up to **5·10⁴** calls · `findMedian` is only called after at least one `addNum`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "from a **data stream**" | Values arrive over time; both operations are called repeatedly, so updates must be **incremental** |
| "**median**" | ⚠️ Not a top-k question — you need the *middle*, which depends on the whole distribution |
| even count → average of two | Two different answers depending on parity |
| up to 5·10⁴ calls | Sorting on each `findMedian` would be 5·10⁴ × O(n log n) — far too slow |
| returns a **float** | `2.0`, not `2` — use true division |

**Why the earlier heap technique doesn't transfer.** In [Kth Largest in a Stream](703-kth-largest-element-in-a-stream.md) you could **discard** everything below the top k, because the k-th largest only ever rises. Here you can't discard anything — a new value can shift the median in either direction, so **every number stays relevant forever**.

**The reframe.** Think of the sorted data as split into two halves:

```
sorted:   1   3   5  |  7   9   11
          └ lower ┘     └ upper ┘

median = average of the largest of the lower half (5)
                 and the smallest of the upper half (7)
```

The median depends **only on the boundary between the halves** — the largest of the small half and the smallest of the large half. Everything else is irrelevant to the answer.

And "largest of a set" and "smallest of a set" are exactly what heaps give in O(1):

| Half | Structure | Its root is |
|---|---|---|
| Lower | **max**-heap | the largest of the small values ← just below the median |
| Upper | **min**-heap | the smallest of the large values ← just above the median |

**Keep the two halves balanced** (sizes differing by at most 1) and the median is always one or both of those roots — an O(1) read.

🤔 **Before you open the next section:** two invariants must hold after every insert. One is about sizes. What's the other, about the *values*?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | `addNum` | `findMedian` | Verdict |
|---|---|---|---|
| Store all, sort on query | O(1) | **O(n log n)** | ❌ Re-sorts constantly |
| Keep a sorted list, insert in place | **O(n)** shifting | O(1) | ⚠️ Better; still linear inserts |
| Balanced BST with subtree sizes | O(log n) | O(log n) | ✅ Works; far more machinery |
| **Two heaps** | **O(log n)** | **O(1)** | ✅ |

**The decision: a max-heap for the lower half and a min-heap for the upper half, kept balanced.**

Two invariants must hold after every `addNum`:

| Invariant | Why |
|---|---|
| **1. Ordering** — every value in `small` ≤ every value in `large` | Otherwise the roots aren't the true middle values |
| **2. Balance** — the sizes differ by at most 1 | Otherwise the boundary isn't the median |

Given both, reading the median is trivial:
- **Unequal sizes** → the median is the root of the **larger** heap (it holds the extra element).
- **Equal sizes** → the median is the **average of both roots**.

**The insertion procedure** is three steps, each restoring one property:

1. **Push** onto `small` (either heap works as the default — you fix it next).
2. **Fix ordering:** if `small`'s max exceeds `large`'s min, move that value across.
3. **Fix balance:** if one heap is more than one larger, move its root to the other.

Do them in that order and both invariants are always restored. Doing balance before ordering can leave a value on the wrong side.

**Why two heaps rather than one sorted structure.** A sorted list gives O(1) median but O(n) insertion because of the shifting. Heaps maintain only a **partial** order — enough to know each half's boundary, which is all the median needs — so insertion is O(log n). **You're deliberately not computing information you don't need**, the same instinct as [Top K Frequent Elements](347-top-k-frequent-elements.md) avoiding a full sort.

**Python's negation trick** again for the max-heap: `small` stores negated values, so `-small[0]` is its true maximum.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
def __init__(self):
    self.small = []   # max-heap (negated values), lower half
    self.large = []   # min-heap, upper half
```

Two heaps for the two halves. `small` stores **negated** values so Python's min-heap behaves as a max-heap — the comments earn their place here, because the negation is invisible otherwise.
→ [class-basics](../syntax/class-basics.md) · [init-method](../syntax/init-method.md) · [heap](../data-structures/heap.md)

```python
def addNum(self, num: int) -> None:
    heapq.heappush(self.small, -num)
```

**Step 1 — push onto `small`** (negated). Which heap you pick as the default doesn't matter; the next two steps repair whatever is wrong.
→ [heapq-module](../syntax/heapq-module.md) · [import-basics](../syntax/import-basics.md)

```python
    if self.small and self.large and (-self.small[0] > self.large[0]):
        val = -heapq.heappop(self.small)
        heapq.heappush(self.large, val)
```

**Step 2 — fix the ordering invariant.** `-self.small[0]` is `small`'s true maximum; `self.large[0]` is `large`'s minimum. If the max of the lower half exceeds the min of the upper half, the value is on the wrong side — move it across.

Note the double negation: pop gives a negated value, so `-heapq.heappop(...)` recovers the real number before pushing it into the non-negated heap.

The `self.small and self.large` guard avoids indexing an empty heap.
→ [logical-operators](../syntax/logical-operators.md) · [truthy-falsy-values](../syntax/truthy-falsy-values.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
    if len(self.small) > len(self.large) + 1:
        val = -heapq.heappop(self.small)
        heapq.heappush(self.large, val)
    elif len(self.large) > len(self.small) + 1:
        val = heapq.heappop(self.large)
        heapq.heappush(self.small, -val)
```

**Step 3 — fix the balance invariant.** If either heap is more than one bigger, move its root to the other side.

Only one transfer is ever needed, because sizes change by at most one per insert — so `if`/`elif` suffices, not a loop.

Watch the negations: moving *out* of `small` un-negates; moving *into* `small` negates.
→ [elif-else](../syntax/elif-else.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
def findMedian(self) -> float:
    if len(self.small) > len(self.large):
        return -self.small[0]
    elif len(self.large) > len(self.small):
        return self.large[0]
    else:
        return (-self.small[0] + self.large[0]) / 2.0
```

**O(1) read**, three cases:

- **`small` bigger** — it holds the extra element, so its max *is* the median.
- **`large` bigger** — its min is the median.
- **Equal** — an even count, so average the two boundary values.

`/ 2.0` forces true division, returning a float as required (`/` in Python 3 already does this; the `.0` makes the intent explicit).
→ [if-return](../syntax/if-return.md) · [int-float-basics](../syntax/int-float-basics.md)

<details>
<summary>The whole thing together</summary>

```python
import heapq

class MedianFinder:

    def __init__(self):
        self.small = []   # max-heap (negated values), lower half
        self.large = []   # min-heap, upper half

    def addNum(self, num: int) -> None:
        heapq.heappush(self.small, -num)

        if self.small and self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)

        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        elif len(self.large) > len(self.small) + 1:
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return -self.small[0]
        elif len(self.large) > len(self.small):
            return self.large[0]
        else:
            return (-self.small[0] + self.large[0]) / 2.0
```

</details>

**Trace it** — `addNum(1)`, `addNum(2)`, `findMedian()`, `addNum(3)`, `findMedian()`:

*(`small` shown as true values, not negated.)*

| Call | Step | `small` (lower) | `large` (upper) |
|---|---|---|---|
| `addNum(1)` | push 1 | `{1}` | `{}` |
| | ordering: `large` empty, skip | `{1}` | `{}` |
| | balance: 1 vs 0, ok | `{1}` | `{}` |
| `addNum(2)` | push 2 | `{1,2}` | `{}` |
| | ordering: `large` empty, skip | `{1,2}` | `{}` |
| | **balance:** 2 > 0+1 → move max (2) | `{1}` | `{2}` |
| `findMedian()` | equal sizes | | → `(1 + 2)/2 = ` **1.5** ✅ |
| `addNum(3)` | push 3 | `{1,3}` | `{2}` |
| | **ordering:** max(small)=3 > min(large)=2 → move 3 across | `{1}` | `{2,3}` |
| | **balance:** 2 > 1+1? no | `{1}` | `{2,3}` |
| `findMedian()` | `large` bigger | | → `large[0] = ` **2** ✅ |

The `addNum(3)` step shows both fixes in sequence: 3 was pushed into the wrong half, the ordering check moved it, and the balance check then confirmed the sizes were already fine. Sorted, the data is `[1, 2, 3]` — median **2** ✅

</details>

<details>
<summary><b>4 · Time complexity</b> — O(log n) add, O(1) find</summary>

| Operation | Cost |
|---|---|
| **`addNum`** | **O(log n)** |
| **`findMedian`** | **O(1)** |

**`addNum`** does at most three heap operations — one push, plus up to two transfers (each a pop and a push). Each is O(log n) on a heap of at most n elements, and three is a constant, so **O(log n)**.

**`findMedian`** reads `heap[0]` on one or both heaps — index 0, no search. **O(1)**.

**Versus the alternatives, over 5·10⁴ calls:**

| Approach | `addNum` | `findMedian` | Total |
|---|---|---|---|
| Sort on query | O(1) | O(n log n) | ~4·10⁹ |
| Sorted list | O(n) | O(1) | ~1.3·10⁹ |
| **Two heaps** | **O(log n)** | **O(1)** | **~8·10⁵** |

**The asymmetry is deliberate:** all the work happens on insert so queries are free. That's the right shape when queries are frequent — the same do-work-on-write trade as [Min Stack](155-min-stack.md) and [Kth Largest in a Stream](703-kth-largest-element-in-a-stream.md).

**Why not O(1) inserts too?** The median genuinely depends on the whole distribution, so each new value may shift the boundary. The heaps make that shift O(log n) instead of O(n).

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** — every number added is stored, split across the two heaps.

**Nothing can be discarded**, and this is the sharp contrast with the rest of the unit:

| Problem | Structure size | Why |
|---|---|---|
| [703](703-kth-largest-element-in-a-stream.md), [973](973-k-closest-points-to-origin.md), [215](215-kth-largest-element-in-an-array.md) | **O(k)** | Values outside the top k are permanently irrelevant |
| **295** | **O(n)** | Any value can influence the median as more data arrives |

A small value discarded early could become the median once enough large values arrive. **The median depends on the whole distribution; top-k depends only on a boundary.** That's why the size-k trick doesn't transfer, and it's worth saying explicitly.

**Balanced heaps mean each holds about n/2** — same total, but the balance is what keeps the median at the boundary.

**If memory were the constraint**, you'd give up exactness: reservoir sampling or a t-digest gives an *approximate* median in sublinear space. That's the real answer for a genuinely unbounded stream, and naming it shows you know exact medians can't be done in O(1) space.
→ [reservoir-sampling](../algorithms/reservoir-sampling.md)

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Unlike the top-k problems, I can't discard anything — a value that looks unimportant now could become the median later, because the median depends on the whole distribution. The key reframe is that the median depends only on the *boundary* between the lower and upper halves of the data. So I keep a max-heap for the lower half and a min-heap for the upper half: their roots are the two values adjacent to the median, both readable in O(1). Each insert maintains two invariants — every value in the lower half is ≤ every value in the upper half, and the sizes differ by at most one. I push, then fix ordering if the boundary values are out of order, then fix balance if one side got too big. The median is the root of the larger heap, or the average of both roots when they're equal. O(log n) insert, O(1) query, O(n) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why can't you cap the heaps at some size?" | **The question.** Any value can become the median later — unlike top-k, where anything outside the top k is permanently irrelevant. |
| "What if 99% of values are in [0, 100]?" | Use **counting**: a frequency array over the range, then scan to the middle. O(1) insert, O(range) query — a big win for bounded values. |
| "What if all values fit in a small range generally?" | Same idea, or bucket them. Worth asking about the data distribution. |
| "Handle memory limits on an infinite stream?" | Give up exactness — reservoir sampling or t-digest for an approximate median in sublinear space. |
| "Find the k-th percentile instead of the median?" | Same two heaps, balanced at a k:(100−k) ratio instead of 50:50. |
| "Support **removing** numbers?" | Heaps can't delete arbitrary elements efficiently. Use lazy deletion with a "to remove" counter, or switch to a balanced BST / `SortedList`. |
| "Why not a balanced BST?" | It works — O(log n) both ways — but it's much more code, and augmenting nodes with subtree sizes is needed to find the middle. |

**Traps:**

- **Getting the heap types backwards.** The **lower** half needs a **max**-heap (its largest is at the boundary) and the **upper** half a **min**-heap. Swapping them puts the wrong values at the roots.
- **Balancing before fixing the ordering.** You could move a value to the wrong side and break invariant 1.
- **Negation errors.** `small` stores negated values — negate on push, un-negate on pop and on read.
- **Allowing a size difference of 2 or more.** The roots would no longer straddle the median.
- **Integer division** for the even case — `//` gives 1 instead of 1.5.
- **Indexing an empty heap** in the ordering check without the `and` guard.

**This same move shows up in:** [Kth Largest Element in a Stream](703-kth-largest-element-in-a-stream.md) (a heap on a stream, where discarding *is* allowed) · [Last Stone Weight](1046-last-stone-weight.md) (the negation trick) · [Min Stack](155-min-stack.md) (work on insert so queries are O(1)) · [heap](../data-structures/heap.md).

</details>

---
