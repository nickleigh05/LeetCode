# 703. Kth Largest Element in a Stream

**Easy** · [LeetCode](https://leetcode.com/problems/kth-largest-element-in-a-stream/) · [Solution file (no hints)](../../problems/0500-0999/703.py)

[📖 09. Heap / Priority Queue lesson](../learning/09-heap-priority-queue.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 09. Heap / Priority Queue problems](../rmap-practice/09-heap-priority-queue.md)

---

Design a class to find the **k-th largest element in a stream** — the k-th largest in sorted order, **not** the k-th distinct element.

- **`KthLargest(k, nums)`** — initialize with an integer `k` and a stream of initial values
- **`add(val)`** — append `val` to the stream and return the element representing the k-th largest

```
KthLargest(3, [4,5,8,2])
add(3)   →  4      stream [4,5,8,2,3] → sorted desc [8,5,4,3,2], 3rd is 4
add(5)   →  5      [8,5,5,4,3,2] → 3rd is 5
add(10)  →  5
add(9)   →  8
add(4)   →  8
```

**Constraints:** `1 <= k <= 10⁴` · up to 10⁴ calls to `add` · it's guaranteed there are at least k elements when `add` is called

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

This is the introductory problem for the unit, and the **size-k heap** idea it teaches reappears in almost every problem that follows.

| The statement says | Which really means |
|---|---|
| "in a **stream**" | ⚠️ Values arrive over time and `add` is called repeatedly — so you need **cheap incremental updates**, not a from-scratch computation each time |
| "k-th largest, **not** k-th distinct" | Duplicates count. `[5,5,5]` with k=2 gives 5 |
| "**return** after each add" | Every call must produce the answer, so the structure must always be ready |
| up to 10⁴ adds | Re-sorting per call would be 10⁴ × 10⁴ log — too slow |

**The naive approach and why it fails.** Store everything, sort on each `add`, return index `k-1`. That's O(n log n) **per call** — 10⁴ calls over a growing list is far too slow.

**The realization.** To answer "what's the k-th largest?", you don't need all n values. You only need the **k largest ones** — everything smaller is irrelevant and can be discarded forever.

And among those k, the answer is specifically the **smallest** of them:

```
stream:      [8, 5, 5, 4, 3, 2]     k = 3
keep only:   [8, 5, 5]
                     ↑ the smallest of the k largest = the 3rd largest ✅
```

So the structure needs two things: **fast access to its minimum**, and **fast insertion/removal**. That's a **min-heap**.

⚠️ **The counterintuitive part worth pausing on:** finding the k-th *largest* uses a **min**-heap. The heap holds the k biggest values, and its root — the smallest of them — is the answer.

🤔 **Before you open the next section:** if the heap already holds k values and a new one arrives, what's the cheapest way to decide whether it belongs?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | `add` cost | Space | Verdict |
|---|---|---|---|
| Store all, sort each time | O(n log n) | O(n) | ❌ Recomputes from scratch every call |
| Keep a sorted list, insert in place | O(n) per insert | O(n) | ⚠️ Better, still linear shifting |
| Max-heap of everything, pop k times | O(k log n) per query | O(n) | ⚠️ Works, but re-pops and must restore |
| **Min-heap capped at size k** | **O(log k)** | **O(k)** | ✅ |

**The decision: a [min-heap](../data-structures/heap.md) holding exactly the k largest values seen so far.**

The invariant, which is the whole solution:

> **The heap contains the k largest values seen so far, and `heap[0]` — its minimum — is the k-th largest overall.**

Maintaining it on each `add` is two steps:

1. **Push** the new value.
2. **If the heap now exceeds k, pop the minimum** — that value is no longer among the top k.

That's it. If the new value is small, it gets pushed and immediately popped back out (or displaces nothing important). If it's large, it stays and evicts the previous smallest.

**Why a *min*-heap for a *largest* question.** You need to know which of your k candidates to discard when a better one arrives — and that's always the **smallest** of them. A min-heap surfaces exactly that in O(1). A max-heap would give you the *largest*, which you never need to remove.

**Why the heap stays at size k.** Anything below the top k can never become the answer *later*, because the stream only ever adds values — the k-th largest can only move up. So discarded values are gone for good. **That's what bounds both time and memory**, and it's why this works on an unbounded stream.

**Why not a sorted list?** `bisect.insort` finds the position in O(log k) but the insertion itself shifts elements — O(k). The heap avoids the shifting because it maintains only a partial order, which is all you need.
→ [heapq-module](../syntax/heapq-module.md)

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
import heapq
```

Python has no heap class — `heapq` provides functions that treat a **plain list** as a binary min-heap. Same module as [Merge k Sorted Lists](23-merge-k-sorted-lists.md).
→ [import-basics](../syntax/import-basics.md) · [heapq-module](../syntax/heapq-module.md) · [heap](../data-structures/heap.md)

```python
def __init__(self, k: int, nums: List[int]):
    self.k = k
    self.heap = []

    for num in nums:
        heapq.heappush(self.heap, num)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)
```

Seed the heap with the initial values, applying the **same push-then-trim rule** used by `add`.

Reusing the identical logic is deliberate: the invariant is established during construction and then simply maintained. (Calling `self.add(num)` in the loop would be equivalent — the duplication here is just for clarity.)

Note `nums` may be shorter than k initially; the trim simply never fires until the heap fills.
→ [class-basics](../syntax/class-basics.md) · [init-method](../syntax/init-method.md) · [for-loop](../syntax/for-loop.md)

```python
def add(self, val: int) -> int:
    heapq.heappush(self.heap, val)
```

**Push unconditionally.** You could compare against `heap[0]` first and skip small values, but pushing then trimming is simpler and the same complexity — the heap self-corrects.

`heappush` is O(log k): the value bubbles up until the heap property is restored.

```python
    if len(self.heap) > self.k:
        heapq.heappop(self.heap)
```

**Trim back to k.** `heappop` removes the **smallest** element — the one that just fell out of the top k.

If `val` was small, this pops `val` itself and nothing changes. If `val` was large, this evicts the old k-th largest. Either way the invariant is restored, with no branching needed to distinguish the cases.
→ [comparison-operators](../syntax/comparison-operators.md) · [if-return](../syntax/if-return.md)

```python
    return self.heap[0]
```

**O(1) read.** In a min-heap the root — index 0 — is always the minimum, and by the invariant that's the k-th largest overall.

No search, no scan. The work was done during insertion.

<details>
<summary>The whole thing together</summary>

```python
import heapq

class KthLargest:

    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.heap = []

        for num in nums:
            heapq.heappush(self.heap, num)
            if len(self.heap) > self.k:
                heapq.heappop(self.heap)

    def add(self, val: int) -> int:
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)
        return self.heap[0]
```

</details>

**Trace it** — `KthLargest(3, [4,5,8,2])`, then the example calls:

**Construction** (k = 3):

| Push | Heap after push | Over k? | Heap after trim |
|---|---|---|---|
| 4 | `[4]` | no | `[4]` |
| 5 | `[4,5]` | no | `[4,5]` |
| 8 | `[4,5,8]` | no | `[4,5,8]` |
| 2 | `[2,4,8,5]` | **yes** → pop 2 | `[4,5,8]` |

The 2 was pushed and immediately discarded — it's not among the top 3.

**The `add` calls:**

| Call | After push | Popped | Heap (the top 3) | Returns `heap[0]` |
|---|---|---|---|---|
| `add(3)` | `[3,4,8,5]` | 3 | `{4,5,8}` | **4** ✅ |
| `add(5)` | — | 4 | `{5,5,8}` | **5** ✅ |
| `add(10)` | — | 5 | `{5,8,10}` | **5** ✅ |
| `add(9)` | — | 5 | `{8,9,10}` | **8** ✅ |
| `add(4)` | — | 4 | `{8,9,10}` | **8** ✅ |

Watch `add(5)`: it evicted the 4, and the answer rose from 4 to 5. And `add(4)` pushed a value that was immediately popped back out — the heap absorbed it with no effect, exactly as it should.

*(Heap contents are shown as sets; the internal array order is an implementation detail — only `heap[0]` is guaranteed to be the minimum.)*

</details>

<details>
<summary><b>4 · Time complexity</b> — O(log k) per add</summary>

**O(log k)** per `add`, **O(n log k)** for construction with n initial values.

| Operation | Cost |
|---|---|
| `heappush` | O(log k) — bubble up through the heap's depth |
| `heappop` | O(log k) — move the last element to the root and sift down |
| `heap[0]` | **O(1)** — the root is just index 0 |

The heap has at most k elements, so its depth is log₂ k — **that's why the cost is log k rather than log n.**

**Versus the alternatives, at 10⁴ adds:**

| Approach | Per add | Total |
|---|---|---|
| Sort every time | O(n log n) | ~10⁹ |
| Sorted list insert | O(k) | ~10⁸ |
| **Size-k heap** | **O(log k)** | **~1.3·10⁵** |

**The stream property is what makes this the right structure.** A one-shot "find the k-th largest of a fixed array" could use [Quickselect](../algorithms/quickselect.md) at O(n) average. But with values arriving continuously, you need cheap *incremental* updates, and the heap gives them.

**The key asymmetry:** the answer is O(1) to read because the maintenance happens on insertion. That's the same do-work-on-write trade as [Min Stack](155-min-stack.md).

</details>

<details>
<summary><b>5 · Space complexity</b> — O(k)</summary>

**O(k)** — and this is arguably more important than the time bound.

The heap **never exceeds k elements**, no matter how many values the stream delivers. Ten million `add` calls with k = 3 still uses three slots.

**Why discarding is safe.** Once a value falls out of the top k, it can never return — the stream only *adds*, so the k-th largest can only increase. A discarded value is permanently irrelevant.

⚠️ **That reasoning would break if values could be removed** from the stream. Then you'd need all n values, since deleting a large one could promote a previously-discarded small one. Worth stating — it's the natural follow-up.

**Versus storing everything: O(n)**, unbounded as the stream continues. For a genuinely infinite stream that's not merely slow, it's *impossible* — which is why bounded-memory streaming algorithms matter.

**The general pattern this introduces:**

> **To track the top k of a stream, keep a min-heap of size k. To track the bottom k, keep a max-heap of size k.**

The heap type is always the *opposite* of what you're looking for, because you need fast access to the element you'll **evict**. That idea drives [K Closest Points](973-k-closest-points-to-origin.md) and [Kth Largest Element in an Array](215-kth-largest-element-in-an-array.md) too.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Re-sorting on every add is O(n log n) per call and far too slow. The key realization is that to answer 'what's the k-th largest?', I only need to retain the k largest values — everything smaller is permanently irrelevant, because a stream only adds and the k-th largest can only rise. And among those k, the answer is the *smallest*, so I keep a min-heap capped at size k. Each add pushes the new value and pops the minimum if the heap exceeds k, which either discards the new value or evicts the old k-th largest. Reading the answer is `heap[0]`, O(1). O(log k) per add and O(k) space, regardless of how long the stream runs. It's a min-heap even though the question asks for the largest, because I need fast access to the element I'll evict."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why a **min**-heap for the k-th *largest*?" | **The question.** The heap holds the k largest; its root is the smallest of them, which is both the answer *and* the element to evict when a better one arrives. |
| "What if values could be **removed** from the stream?" | The discard logic breaks — a deleted large value could promote something you threw away. You'd need all n values, e.g. a balanced BST or a sorted structure. |
| "One-shot on a fixed array instead of a stream?" | [Quickselect](../algorithms/quickselect.md) at O(n) average beats O(n log k). See [Kth Largest Element in an Array](215-kth-largest-element-in-an-array.md). |
| "k-th **smallest** in a stream?" | Mirror it: a **max**-heap of size k, with the root being the answer. In Python, negate the values. |
| "The **median** of a stream?" | Not a top-k question — you need *two* heaps balanced against each other. See [Find Median from Data Stream](295-find-median-from-data-stream.md). |
| "Can you skip the push when `val` is small?" | Yes — `if len(heap) < k or val > heap[0]`. Same complexity, avoids some churn. The unconditional version is simpler. |
| "What if k > the stream length?" | The heap just holds everything and `heap[0]` is the minimum. The constraints guarantee at least k elements at `add` time. |

**Traps:**

- **Using a max-heap.** You'd have O(1) access to the largest, which you never need to remove — the evictions become O(k).
- **Sorting on every call.** Correct, far too slow, and it ignores that the answer changes incrementally.
- **Letting the heap grow past k.** Still correct (the k-th largest is no longer at index 0 though), but you lose both the O(log k) and the O(k) bounds.
- **Returning `heap[-1]` or scanning for a maximum.** In a min-heap only index 0 is guaranteed — the rest of the array is *not* sorted.
- **Trimming before pushing** — you'd drop a value that might belong in the top k.
- **Assuming distinct values.** Duplicates count; `[5,5]` with k=2 gives 5.

**This same move shows up in:** [K Closest Points to Origin](973-k-closest-points-to-origin.md) (a size-k heap, with the type flipped) · [Kth Largest Element in an Array](215-kth-largest-element-in-an-array.md) (the one-shot version, where Quickselect wins) · [Merge k Sorted Lists](23-merge-k-sorted-lists.md) (a heap holding only the current candidates) · [Find Median from Data Stream](295-find-median-from-data-stream.md) (two heaps instead of one).

</details>

---
