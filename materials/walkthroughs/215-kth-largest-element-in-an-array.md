# 215. Kth Largest Element in an Array

**Medium** · [LeetCode](https://leetcode.com/problems/kth-largest-element-in-an-array/) · [Solution file (no hints)](../../problems/0001-0499/215.py)

[📖 09. Heap / Priority Queue lesson](../learning/09-heap-priority-queue.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 09. Heap / Priority Queue problems](../rmap-practice/09-heap-priority-queue.md)

---

Given an integer array `nums` and an integer `k`, return the **k-th largest element** in the array.

Note this is the k-th largest in **sorted order**, not the k-th distinct element.

```
nums = [3,2,1,5,6,4],     k = 2  →  5
nums = [3,2,3,1,2,4,5,5,6], k = 4  →  4
```

**Constraints:** `1 <= k <= nums.length <= 10⁵` · `-10⁴ <= nums[i] <= 10⁴` · **follow-up: can you solve it without sorting?**

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "k-th largest" | The same selection question as [problem 703](703-kth-largest-element-in-a-stream.md) — but on a **fixed array**, not a stream |
| "**not** the k-th distinct" | Duplicates count. In `[3,2,3,1,2,4,5,5,6]` with k=4, the answer is 4 |
| "**without sorting**" follow-up | ⚠️ The problem is pointing past the one-liner. Sorting is O(n log n); better exists |
| n up to 10⁵ | Sorting is fine at ~1.7·10⁶ ops — but the follow-up wants the improvement |

**Start with the one-liner**, because it's the honest baseline: `sorted(nums)[-k]`. O(n log n), correct, and worth saying out loud.

**Why you can do better.** Sorting produces a **total order** — it tells you the rank of *every* element. You asked for **one** rank. Almost all of that work is discarded.

Two ways to avoid it:

**1. The size-k heap** — exactly [problem 703](703-kth-largest-element-in-a-stream.md)'s technique. Keep the k largest values in a min-heap; its root is the k-th largest. O(n log k) time, O(k) space.

**2. Quickselect** — partition around a pivot as in quicksort, but recurse into **only the side containing the k-th element**. O(n) *average*.

⚠️ **The key difference from [703](703-kth-largest-element-in-a-stream.md):** this array is **fixed and fully available**. That unlocks Quickselect, which needs random access to the whole array — impossible on a stream. Same question, different constraint, different optimal answer.

🤔 **Before you open the next section:** if a partition step tells you the pivot landed at index `p`, and you want the element at index `t`, why do you only ever need to recurse into one half?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Time | Space | Verdict |
|---|---|---|---|
| Sort, index `[-k]` | O(n log n) | O(n) | ⚠️ The honest baseline — say it first |
| Max-heap of all n, pop k times | O(n + k log n) | O(n) | ⚠️ Good; O(n) space |
| **Min-heap capped at k** | **O(n log k)** | **O(k)** | ✅ |
| **Quickselect** | **O(n) average**, O(n²) worst | O(1) | ✅ The follow-up's answer |

**The decision (as written): a min-heap capped at size k** — the [703](703-kth-largest-element-in-a-stream.md) technique, applied in one pass.

Push each number; whenever the heap exceeds k, pop the minimum. The heap ends holding the k largest values, and its root is the k-th largest.

**The invariant is identical to [703](703-kth-largest-element-in-a-stream.md):** *the heap holds the k largest values seen so far, and `heap[0]` is the k-th largest.* Same counterintuitive point — **a min-heap answers a "largest" question**, because the element you evict is always the smallest of your current best k.

**Quickselect is the better answer to the stated follow-up**, and worth being able to describe:

```python
import random

def quickselect(nums, k):
    target = len(nums) - k          # the k-th largest is at this index once sorted
    left, right = 0, len(nums) - 1
    while True:
        pivot = partition(nums, left, right)   # pivot lands in its final position
        if pivot == target:  return nums[pivot]
        if pivot < target:   left = pivot + 1
        else:                right = pivot - 1
```

**Why it's O(n) average.** Quicksort recurses into *both* halves — T(n) = 2T(n/2) + O(n) = O(n log n). Quickselect recurses into **one**: T(n) = T(n/2) + O(n), and n + n/2 + n/4 + … **converges to 2n**. Discarding half the search space each round, exactly like binary search — but on unsorted data, using partitioning instead of comparison.

**Why the heap is often the safer interview choice.** Quickselect's O(n²) worst case (adversarial pivots) needs random pivot selection to avoid, and the partition logic is easy to get subtly wrong under pressure. **Say Quickselect is optimal, write whichever you can get right.**
→ [quickselect](../algorithms/quickselect.md)

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
import heapq

heap = []
```

A plain list managed as a min-heap by `heapq`.
→ [import-basics](../syntax/import-basics.md) · [heapq-module](../syntax/heapq-module.md) · [heap](../data-structures/heap.md)

```python
for num in nums:
    heapq.heappush(heap, num)
```

**Push every number.** No pre-filtering — the trim below handles rejection automatically, and skipping the comparison keeps the loop simple.

`heappush` is O(log k), since the heap is capped just below.
→ [for-loop](../syntax/for-loop.md)

```python
    if len(heap) > k:
        heapq.heappop(heap)
```

**Trim back to k.** `heappop` removes the **smallest** element — the one that has just dropped out of the top k.

If `num` was small, this pops `num` itself and nothing changes. If it was large, it evicts the previous k-th largest. **One rule covers both cases**, no branching.
→ [comparison-operators](../syntax/comparison-operators.md) · [if-return](../syntax/if-return.md)

```python
return heap[0]
```

**O(1) read.** After the loop the heap holds exactly the k largest values, and a min-heap's root is the smallest of them — which is the k-th largest overall.

Only index 0 is guaranteed to be the minimum; the rest of the heap array is **not** sorted.

<details>
<summary>The whole thing together</summary>

```python
import heapq

class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:

        heap = []

        for num in nums:
            heapq.heappush(heap, num)
            if len(heap) > k:
                heapq.heappop(heap)

        return heap[0]
```

</details>

**Trace it** — `nums = [3,2,1,5,6,4]`, `k = 2`:

| `num` | Heap after push | Size > 2? | Popped | Heap holds |
|---|---|---|---|---|
| 3 | `{3}` | no | — | `{3}` |
| 2 | `{2,3}` | no | — | `{2,3}` |
| 1 | `{1,2,3}` | yes | **1** | `{2,3}` |
| 5 | `{2,3,5}` | yes | **2** | `{3,5}` |
| 6 | `{3,5,6}` | yes | **3** | `{5,6}` |
| 4 | `{4,5,6}` | yes | **4** | `{5,6}` |

Return `heap[0]` = **5** ✅ — the 2nd largest in `[3,2,1,5,6,4]`.

Watch the last row: 4 was pushed and immediately popped, because it isn't among the top 2. And the heap never held more than 3 elements despite processing 6.

**The duplicates case** — `nums = [3,2,3,1,2,4,5,5,6]`, `k = 4`. The top four values in sorted order are `6, 5, 5, 4`, so the answer is **4** — the two 5s are counted separately, exactly as "not the k-th distinct" requires.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n log k)</summary>

**O(n log k)** for the heap solution.

Each of the n numbers costs one `heappush` and possibly one `heappop`, each O(log k) since the heap never exceeds k+1 elements.

**Comparing all four approaches at n = 10⁵:**

| Approach | Complexity | Roughly |
|---|---|---|
| Sort | O(n log n) | 1.7·10⁶ |
| **Heap, k = 10** | O(n log k) | **3.3·10⁵** |
| Heap, k = n | O(n log n) | 1.7·10⁶ — no better than sorting |
| **Quickselect** | **O(n) average** | **~2·10⁵** |

**Note the heap's advantage vanishes when k ≈ n.** log k becomes log n and you've just done a more complicated sort. The heap is the right tool specifically when **k ≪ n** — worth saying, since it shows you know when *not* to reach for it.

**Why Quickselect averages O(n):** each partition discards roughly half the remaining elements, so the work is n + n/2 + n/4 + … which converges to **2n**. Its O(n²) worst case comes from consistently terrible pivots, avoided in practice by choosing pivots at random.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(k)</summary>

**O(k)** for the heap — it never exceeds k+1 elements.

| Approach | Auxiliary space |
|---|---|
| Sort | **O(n)** (Python's Timsort) |
| Max-heap of all n | **O(n)** |
| **Min-heap of k** | **O(k)** |
| **Quickselect** | **O(1)** — partitions in place |

**Quickselect wins on space** by rearranging the input array in place. ⚠️ But that means it **mutates the input** — a genuine API concern worth raising. If the caller needs the array preserved, you'd copy it first, and the O(1) advantage evaporates.

**The heap's space profile is what makes it the streaming answer.** It never needs the whole array resident — process elements one at a time, keep only the best k. That's why the identical technique works in [Kth Largest Element in a Stream](703-kth-largest-element-in-a-stream.md), where Quickselect is simply impossible.

**The trade, stated plainly:**

> **Quickselect is faster and uses less space, but needs the whole array in memory and destroys it. The heap is slightly slower but streams and doesn't mutate.**

Which one is "better" genuinely depends on the constraints — that's the answer an interviewer wants, not a blanket preference.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The one-liner is `sorted(nums)[-k]` at O(n log n), but that computes the rank of every element when I only need one. Two better options. A min-heap capped at size k: push each number, pop the minimum whenever the heap exceeds k, and the root ends up being the k-th largest — O(n log k) time, O(k) space, and it's a *min*-heap because the element I evict is always the smallest of my current best k. Or Quickselect, which partitions around a pivot like quicksort but recurses into only the side containing the target index — O(n) average, because n + n/2 + n/4 converges to 2n. Quickselect is optimal here since the array is fixed and fully available, though it mutates the input and has an O(n²) worst case without random pivots."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Solve it without sorting." | **The stated follow-up.** Size-k heap at O(n log k), or Quickselect at O(n) average. |
| "Why is Quickselect O(n) and quicksort O(n log n)?" | Quicksort recurses into both halves; Quickselect into one. The series n + n/2 + n/4 + … converges to 2n. |
| "Why a **min**-heap for the k-th *largest*?" | The heap holds the k largest; its root is the smallest of them, which is both the answer and the eviction candidate. |
| "How does this differ from [703](703-kth-largest-element-in-a-stream.md)?" | There the data streams, so Quickselect is impossible and the heap is the only option. Here the array is fixed. |
| "Quickselect's worst case?" | O(n²) with adversarial pivots. Choose pivots at random, or use median-of-medians for a guaranteed O(n) at a worse constant. |
| "k-th **smallest** instead?" | Flip: a max-heap of size k, or Quickselect targeting index `k-1`. |
| "Which would you actually ship?" | Depends: Quickselect if the array is in memory and mutation is fine; the heap if data streams or the input must be preserved. |

**Traps:**

- **Using a max-heap of size k.** You'd evict the *largest*, which is exactly what you want to keep.
- **Returning `heap[-1]`** or scanning the heap array for a value. Only index 0 is guaranteed to be the minimum.
- **Letting the heap grow to n** — still correct if you then pop k times, but you've given up the O(k) space.
- **Confusing k-th largest with k-th distinct.** Duplicates count.
- **Off-by-one in Quickselect's target index.** The k-th largest sits at index `len(nums) - k` in ascending order.
- **Not mentioning Quickselect at all.** The follow-up is explicitly asking for it.

**This same move shows up in:** [Kth Largest Element in a Stream](703-kth-largest-element-in-a-stream.md) (the same heap, where streaming rules out Quickselect) · [K Closest Points to Origin](973-k-closest-points-to-origin.md) (a size-k heap with the type flipped) · [quickselect](../algorithms/quickselect.md) and [quicksort](../algorithms/quicksort.md) (the partitioning reference pages) · [Top K Frequent Elements](347-top-k-frequent-elements.md) (a top-k question solved by bucket sort instead).

</details>

---
