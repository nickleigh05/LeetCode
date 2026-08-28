# 2542. Maximum Subsequence Score

**Medium** · [LeetCode](https://leetcode.com/problems/maximum-subsequence-score/) · [Solution file (no hints)](../../problems/2500-2999/2542.py)

[📖 09. Heap / Priority Queue lesson](../learning/09-heap-priority-queue.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 09. Heap problems](../rmap-practice/09-heap-priority-queue.md)

---

Given equal-length arrays `nums1` and `nums2` and an integer `k`, choose **`k` indices**. The score is:

> **(sum of the chosen `nums1` values) × (minimum of the chosen `nums2` values)**

Return the maximum possible score.

```
nums1 = [1,3,3,2], nums2 = [2,1,3,4], k = 3  →  12
    choose indices 0, 2, 3 → (1+3+2) × min(2,3,4) = 6 × 2 = 12

nums1 = [4,2,3,1,1], nums2 = [7,5,10,9,6], k = 1  →  30
```

**Constraints:** `n == nums1.length == nums2.length` · `1 <= n <= 10⁵` · `0 <= nums1[i], nums2[j] <= 10⁵` · `1 <= k <= n`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| score = **sum × min** | ⚠️ Two competing objectives — maximize a sum *and* a minimum, over the same choice |
| **min** of the `nums2` values | One element caps the whole product; adding a small `nums2` can ruin a large sum |
| choose exactly `k` indices | A fixed-size selection |
| a **subsequence of indices** | Order is irrelevant — it's a subset |
| `n` up to 10⁵ | O(n²) is 10¹⁰; and C(n,k) subsets is astronomically worse |

**Why this is hard to attack directly.** The two factors pull against each other. Adding an index increases the sum (good) but may lower the minimum (bad), and you can't evaluate either in isolation.

**The unlocking idea — fix the minimum:**

> Suppose you **decide in advance** which element supplies the minimum `nums2` value. Then every other chosen index must have `nums2 >= that value`, and among those you simply want the `k−1` largest `nums1` values.

With the minimum pinned, the second factor is a constant and the problem collapses to "maximize a sum" — which is easy.

**Making that efficient.** Sort the pairs by `nums2` **descending**. Then sweep: when you reach position `i`, every element seen so far has `nums2 >= nums2[i]`, so if you pick `i` as the minimum, all previous elements are eligible partners.

```
sorted by nums2 desc:   (nums2=4, nums1=2)
                        (nums2=3, nums1=3)
                        (nums2=2, nums1=1)   ← if this is the min,
                        (nums2=1, nums1=3)      the three above are eligible
```

So at each position you want: **the sum of the `k` largest `nums1` values among everything seen so far**, times the current `nums2`.

Maintaining "the `k` largest so far" while streaming is exactly the **size-`k` min-heap** pattern — and keeping a running sum alongside it makes each step O(log k).

🤔 **Before you open the next section:** if you sort by `nums2` descending and treat each position as the minimum, what do you know about every element that came before it?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Try every subset | Evaluate all C(n,k) choices | exponential | — | ❌ Hopeless |
| Fix each min, sort the rest | For each `i`, sort eligible `nums1` and take top `k−1` | O(n² log n) | O(n) | ❌ 10¹⁰+ |
| **Sort by `nums2` desc + size-`k` min-heap** | Sweep, maintaining the `k` best `nums1` | **O(n log n)** | O(k) | ✅ |

**The decision: sort pairs by `nums2` descending, then sweep with a size-`k` min-heap of `nums1` values plus a running sum.**

The algorithm:

1. Pair up and sort by `nums2` **descending**
2. Walk the sorted list, pushing each `nums1` into a min-heap and adding it to a running total
3. When the heap exceeds `k`, pop the **smallest** `nums1` and subtract it from the total
4. Once the heap holds exactly `k`, the candidate score is `total × current nums2` — track the best

**Why descending order is essential.** It guarantees the sweep invariant:

> At position `i`, every element already in the heap has `nums2 >= nums2[i]`.

So `nums2[i]` is safely the minimum of any selection drawn from the heap plus `i` itself. Sorting ascending would break this — earlier elements would have *smaller* `nums2`, and the current value wouldn't be the minimum.

**Why a *min*-heap when maximizing.** The heap holds the `k` largest `nums1` values seen so far, and you need to evict the **weakest** member when a better one arrives. A min-heap surfaces exactly that. Same inversion as [Kth Largest Element](215-kth-largest-element-in-an-array.md) — **the heap type is the opposite of what you're selecting.**

**Why the running sum matters.** Recomputing `sum(heap)` at each position would be O(k) per step → O(n·k) overall. Maintaining `total` incrementally — `+= value` on push, `-= popped` on pop — keeps each step O(log k).

**Why the current element is always included.** After pushing `nums1[i]` and trimming to size `k`, the heap contains the `k` largest values from positions `0..i`. That set might exclude `i` itself if its `nums1` is small — but that's fine: those `k` elements all have `nums2 >= nums2[i]`, so `nums2[i]` is a **valid lower bound** on their minimum. The score computed is therefore achievable or conservative, and the true optimum is captured when the sweep reaches the position that actually supplies the minimum.

That subtlety is worth stating precisely, because it's the step people find hardest to justify.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
import heapq

pairs = sorted(zip(nums2, nums1), reverse=True)
```

**Pair as `(nums2, nums1)` and sort descending by `nums2`.**

Putting `nums2` first makes it the sort key. `reverse=True` gives descending order, which establishes the sweep invariant: everything seen so far has a `nums2` at least as large as the current one.
→ [zip-function](../syntax/zip-function.md) · [sorting-key](../syntax/sorting-key.md)

```python
min_heap = []
total = 0
best = 0
```

- `min_heap` — the `k` largest `nums1` values seen so far
- `total` — their running sum, maintained incrementally
- `best` — the maximum score found

→ [heapq-module](../syntax/heapq-module.md)

```python
for n2, n1 in pairs:
    heapq.heappush(min_heap, n1)
    total += n1
```

**Add the current element** to both the heap and the running sum.
→ [tuple-unpacking](../syntax/tuple-unpacking.md)

```python
    if len(min_heap) > k:
        total -= heapq.heappop(min_heap)
```

**Evict the smallest `nums1` when over capacity.**

A min-heap's root is the smallest — precisely the weakest member of the current top-`k`. Subtracting it keeps `total` consistent with the heap's contents.
→ [if-return](../syntax/if-return.md)

```python
    if len(min_heap) == k:
        best = max(best, total * n2)
```

**Score this configuration.**

`total` is the sum of the `k` largest `nums1` among everything seen; `n2` is the current (smallest so far) `nums2`, which lower-bounds the minimum of any selection from the heap.

The guard ensures we only score once `k` elements are available.
→ [min-max-key](../syntax/min-max-key.md)

```python
return best
```

<details>
<summary>The whole thing together</summary>

```python
import heapq

class Solution:
    def maxScore(self, nums1: List[int], nums2: List[int], k: int) -> int:

        pairs = sorted(zip(nums2, nums1), reverse=True)

        min_heap = []
        total = 0
        best = 0

        for n2, n1 in pairs:
            heapq.heappush(min_heap, n1)
            total += n1

            if len(min_heap) > k:
                total -= heapq.heappop(min_heap)

            if len(min_heap) == k:
                best = max(best, total * n2)

        return best
```

</details>

**Trace it** — `nums1 = [1,3,3,2]`, `nums2 = [2,1,3,4]`, `k = 3`:

**Paired and sorted by `nums2` descending:** `[(4,2), (3,3), (2,1), (1,3)]`

| Step | `(n2, n1)` | Heap after push | Over `k`? | `total` | Size == 3? | Score | `best` |
|---|---|---|---|---|---|---|---|
| 1 | `(4, 2)` | `[2]` | no | 2 | no | — | 0 |
| 2 | `(3, 3)` | `[2,3]` | no | 5 | no | — | 0 |
| 3 | `(2, 1)` | `[1,2,3]` | no | 6 | ✅ | `6 × 2 = 12` | **12** ⭐ |
| 4 | `(1, 3)` | `[1,2,3,3]` → pop 1 | ✅ | `9 − 1 = 8` | ✅ | `8 × 1 = 8` | 12 |

Return **12** ✅

Step 3 is the winning configuration: `nums1` values `{2, 3, 1}` sum to 6, and every one of them has `nums2 >= 2`, so the minimum is 2 → `6 × 2 = 12`. That matches the expected answer's indices 0, 2, 3.

Step 4 shows the eviction working: adding a fourth element forced out the smallest `nums1` (1), and `total` was decremented in lockstep — but the lower `n2` of 1 made the score worse anyway.

**The `k = 1` example** — `nums1 = [4,2,3,1,1]`, `nums2 = [7,5,10,9,6]`, `k = 1`:

Sorted by `nums2` desc: `[(10,3), (9,1), (7,4), (6,1), (5,2)]`

| Step | `(n2, n1)` | Heap (size 1 after trim) | `total` | Score |
|---|---|---|---|---|
| 1 | `(10, 3)` | `[3]` | 3 | `3 × 10 = 30` ⭐ |
| 2 | `(9, 1)` | `[3]` (pop 1) | 3 | `3 × 9 = 27` |
| 3 | `(7, 4)` | `[4]` (pop 3) | 4 | `4 × 7 = 28` |
| 4 | `(6, 1)` | `[4]` (pop 1) | 4 | `4 × 6 = 24` |
| 5 | `(5, 2)` | `[4]` (pop 2) | 4 | `4 × 5 = 20` |

Return **30** ✅

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n log n)</summary>

**O(n log n)**, dominated by the sort.

| Phase | Cost |
|---|---|
| Pair and sort by `nums2` | **O(n log n)** |
| Sweep: one push + at most one pop per element | **O(n log k)** |
| Scoring | O(1) per position |

Since `k <= n`, the total is **O(n log n)**.

At `n = 10⁵`: roughly `10⁵ × 17 × 2` ≈ **3.4 × 10⁶ operations** — fast.

**Compare:**

| | Time at n = 10⁵ |
|---|---|
| All subsets | C(n,k) — astronomically infeasible ❌ |
| Fix each min, re-sort | O(n² log n) ❌ |
| **Sort + size-k heap** | **3.4 × 10⁶** ✅ |

**Why the running sum matters for the bound.** Calling `sum(min_heap)` at each position would add O(k) per step → **O(n · k)** = 10¹⁰ in the worst case. Maintaining `total` incrementally is what keeps the sweep at O(n log k).

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** for the sorted pairs, **O(k)** for the heap.

| | Space |
|---|---|
| Sorted pairs | O(n) |
| Min-heap | **O(k)** |
| Running total, best | O(1) |

The sort's O(n) dominates, but the heap being O(k) is what makes this scale — you never hold more than `k` candidates.

**The two ideas this problem combines**, both from earlier in the unit:

1. **Sort by the constraint key, sweep monotonically** — as in [IPO](502-ipo.md) and [Single-Threaded CPU](1834-single-threaded-cpu.md). Sorting by `nums2` descending makes the current element's `nums2` a valid minimum for everything already seen.
2. **Size-`k` min-heap for the top `k`** — as in [Kth Largest Element](215-kth-largest-element-in-an-array.md) and [Find the Kth Largest Integer](1985-find-the-kth-largest-integer-in-the-array.md). The min-heap's root is the eviction candidate.

Stated generally:

> **When a score multiplies an aggregate by a minimum, fix the minimum by sorting on that key, then optimize the aggregate greedily over the eligible prefix.**

The same reframing solves problems where the score involves a max instead (sort ascending), or where the aggregate is a product rather than a sum.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The score multiplies a sum by a minimum, and those pull against each other — adding an index raises the sum but might lower the min. The unlock is to **fix which element supplies the minimum**. If I sort the pairs by `nums2` descending and sweep, then at any position everything seen so far has `nums2` at least as large as the current value — so the current `nums2` is a valid minimum for any selection drawn from what I've seen. With the minimum pinned, I just want the `k` largest `nums1` values among those, which is the classic size-`k` min-heap: push each value, and if the heap exceeds `k`, pop the smallest. I keep a running sum alongside so scoring is O(1) rather than O(k). At each position where the heap holds `k` elements, the candidate score is `total × current nums2`, and I track the maximum. O(n log n) dominated by the sort, O(n) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why sort by `nums2` **descending**?" | **The key step.** It guarantees everything already seen has `nums2 >= current`, so the current value validly bounds the minimum. |
| "Why a *min*-heap when maximizing?" | The heap holds the `k` largest `nums1`; you evict the weakest, and a min-heap's root is exactly that. |
| "Why keep a running sum?" | `sum(heap)` per step is O(k) → O(n·k) overall. Incremental updates keep it O(log k) per step. |
| "What if the score used **max** instead of min?" | Sort **ascending** by `nums2` — mirror the same argument. |
| "What if `nums1` could be **negative**?" | Taking the `k` largest may no longer be optimal for the product, since a smaller sum times a larger min could win. The greedy needs re-examination. |
| "Does the current element have to be in the heap?" | No — the `k` in the heap all have `nums2 >= current`, so the current value is a valid (possibly conservative) minimum. The true optimum is caught at the position that actually supplies it. |
| "Can you avoid the sort?" | Not really — the whole approach depends on processing in `nums2` order. |

**Traps:**

- **Sorting ascending.** The invariant inverts and the current `nums2` is no longer a valid minimum.
- **Using a max-heap.** You'd evict the largest `nums1` — exactly what you want to keep.
- **Recomputing `sum(heap)` each step.** O(n·k) instead of O(n log k).
- **Forgetting to decrement `total` on eviction.** The sum drifts out of sync with the heap and every later score is wrong.
- **Scoring before the heap reaches size `k`.** You'd multiply an incomplete sum, producing spuriously low (or with fewer than `k` picks, invalid) candidates.
- **Pairing as `(nums1, nums2)`.** Sorts by the wrong key entirely.

**This same move shows up in:** [IPO](502-ipo.md) (sort by the constraint key, heap on the selection key) · [Single-Threaded CPU](1834-single-threaded-cpu.md) (the same architecture, gated by a clock) · [Kth Largest Element in an Array](215-kth-largest-element-in-an-array.md) (the size-`k` min-heap in isolation) · [Find the Kth Largest Integer in the Array](1985-find-the-kth-largest-integer-in-the-array.md) (size-`k` selection with a custom key).

</details>

---
