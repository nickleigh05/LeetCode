# 973. K Closest Points to Origin

**Medium** · [LeetCode](https://leetcode.com/problems/k-closest-points-to-origin/)

[📖 10. Heap / Priority Queue lesson](../learning/10-heap-priority-queue.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 10. Heap / Priority Queue problems](../rmap-practice/10-heap-priority-queue.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Given an array of `points` where `points[i] = [xᵢ, yᵢ]` on the X-Y plane, and an integer `k`, return the **k closest points to the origin** `(0, 0)`.

The distance is the Euclidean distance, `√(x² + y²)`. You may return the answer **in any order**, and it is guaranteed to be **unique** (except for the order).

```
points = [[1,3],[-2,2]], k = 1        →  [[-2,2]]
points = [[3,3],[5,-1],[-2,4]], k = 2 →  [[3,3],[-2,4]]
```

**Constraints:** `1 <= k <= points.length <= 10⁴` · `-10⁴ <= xᵢ, yᵢ <= 10⁴`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**k closest**" | A top-k selection — exactly [problem 703](703-kth-largest-element-in-a-stream.md)'s shape, but returning all k rather than the boundary |
| "**in any order**" | ⚠️ No sorting of the output needed. You need the *set*, not the ranking |
| Euclidean distance `√(x²+y²)` | ⚠️ **The square root is unnecessary** — see below |
| answer is **unique** | No tie-breaking rules to worry about |
| n up to 10⁴ | O(n log n) sorting passes, but O(n log k) is better when k ≪ n |

**The first simplification: skip the square root.**

`√` is **monotonic** — if `a < b` then `√a < √b`. So comparing `√(x₁²+y₁²)` against `√(x₂²+y₂²)` gives exactly the same ordering as comparing `x₁²+y₁²` against `x₂²+y₂²`.

Since you only ever *compare* distances and never report them, the square root is pure overhead — and worse, it introduces floating-point imprecision into what can be exact integer arithmetic. **Use squared distances.**

That's a genuinely reusable instinct: *when a monotonic transformation sits between you and a comparison, drop it.*

**The second decision: which structure.** Sorting all n points by distance and taking the first k is O(n log n) and perfectly correct. But you don't need the full ranking — only the *membership* of the top k, and the problem explicitly says order doesn't matter.

So the same reasoning as [703](703-kth-largest-element-in-a-stream.md) applies: **keep a heap of size k, evicting the worst candidate as better ones arrive.**

⚠️ And the same counterintuitive twist: finding the k **closest** uses a **max**-heap — because the element you need to evict is the *farthest* one currently held.

🤔 **Before you open the next section:** the heap holds your k best candidates so far. When a new point arrives and the heap is full, which stored point do you need instant access to?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Sort by distance, take k | `points.sort(key=...)` | O(n log n) | O(n) | ⚠️ Correct and one line — mention it |
| Min-heap of all n, pop k | Heapify everything, extract k | O(n + k log n) | O(n) | ⚠️ Good; O(n) space |
| **Max-heap capped at k** | Evict the farthest when full | **O(n log k)** | **O(k)** | ✅ |
| [Quickselect](../algorithms/quickselect.md) | Partition around the k-th | **O(n) average** | O(1) | ✅ Optimal average case; O(n²) worst |

**The decision: a max-heap capped at size k, holding the k closest points seen so far.**

The rule per point, identical in shape to [703](703-kth-largest-element-in-a-stream.md):
1. Push it.
2. If the heap exceeds k, **pop the farthest** — it's no longer a contender.

**Why a *max*-heap for the *closest* points.** The heap holds your current best k. When a new point arrives and the heap is full, you must discard whichever stored point is **worst** — the farthest. A max-heap surfaces that in O(1); a min-heap would give you the closest, which you never want to remove.

> **The heap type is always the opposite of what you're selecting for**, because you need fast access to the element you'll *evict*. Top-k largest → min-heap ([703](703-kth-largest-element-in-a-stream.md)). Top-k smallest → **max**-heap (here).

**Python's negation trick** again: push `-dist` so the min-heap's root is the largest actual distance.

**Why push `(-dist, x, y)` tuples.** The heap orders by the first element. Carrying `x` and `y` along means you can reconstruct the points at the end without a separate lookup — the same "payload in the tuple" idea as [Merge k Sorted Lists](23-merge-k-sorted-lists.md). *(Here the coordinates are ints, so ties on distance fall through to comparing them harmlessly — no unorderable-object risk.)*

**Why not just sort?** It's O(n log n) versus O(n log k), and it computes a full ranking you discard. When k ≪ n the heap wins — at n = 10⁴, k = 10 that's log 10 ≈ 3 versus log 10⁴ ≈ 13 per element. **Say the sort answer first, then offer the heap as the improvement.**

**Quickselect is the theoretically best answer** — O(n) average by partitioning around the k-th element without fully sorting. Worth naming; its O(n²) worst case and greater complexity make the heap the safer interview choice.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
import heapq

heap = []
```

A plain list managed by `heapq` as a min-heap — negation will make it behave as a max-heap.
→ [import-basics](../syntax/import-basics.md) · [heapq-module](../syntax/heapq-module.md) · [heap](../data-structures/heap.md)

```python
for x, y in points:
    dist = x * x + y * y
```

**Squared distance — no `math.sqrt`.** Since `√` is monotonic, squaring preserves the ordering, and skipping it keeps the arithmetic in exact integers with no floating-point error.

`for x, y in points` unpacks each `[x, y]` pair directly in the loop header.
→ [tuple-unpacking](../syntax/tuple-unpacking.md) · [for-loop](../syntax/for-loop.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
    heapq.heappush(heap, (-dist, x, y))
```

**Push the negated distance with the coordinates attached.**

- `-dist` makes the min-heap surface the **largest** true distance at its root — the eviction candidate.
- `x, y` ride along so the final answer needs no extra bookkeeping.
→ [tuple-basics](../syntax/tuple-basics.md)

```python
    if len(heap) > k:
        heapq.heappop(heap)
```

**Trim to k.** `heappop` removes the root, which — because of the negation — is the **farthest** point currently held.

If the new point was far, this pops the point just pushed and nothing changes. If it was close, it evicts the previous worst. **One rule, both cases**, exactly as in [703](703-kth-largest-element-in-a-stream.md).
→ [comparison-operators](../syntax/comparison-operators.md) · [if-return](../syntax/if-return.md)

```python
return [[x, y] for _, x, y in heap]
```

**Read out the survivors.** After the loop the heap holds exactly the k closest points.

The comprehension unpacks each tuple, discarding the negated distance with `_` (the conventional name for a value you don't use) and rebuilding the `[x, y]` pairs.

**No sorting needed** — the problem accepts any order, so the heap's internal arrangement is fine as-is.
→ [list-comprehension](../syntax/list-comprehension.md)

<details>
<summary>The whole thing together</summary>

```python
import heapq

class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:

        heap = []

        for x, y in points:
            dist = x * x + y * y
            heapq.heappush(heap, (-dist, x, y))
            if len(heap) > k:
                heapq.heappop(heap)

        return [[x, y] for _, x, y in heap]
```

</details>

**Trace it** — `points = [[3,3],[5,-1],[-2,4]]`, `k = 2`:

| Point | `dist` = x²+y² | Pushed | Heap size | Popped (farthest) | Heap holds |
|---|---|---|---|---|---|
| `[3,3]` | 9+9 = **18** | `(-18,3,3)` | 1 | — | `{18}` |
| `[5,-1]` | 25+1 = **26** | `(-26,5,-1)` | 2 | — | `{18, 26}` |
| `[-2,4]` | 4+16 = **20** | `(-20,-2,4)` | **3 > 2** | **26** (the farthest) | `{18, 20}` |

Result: `[[3,3], [-2,4]]` ✅

Row 3 is the eviction doing its job: `[5,-1]` at distance 26 was the worst of the three, and the max-heap surfaced it immediately for removal.

**And a case where the new point is the one discarded** — adding `[9,9]` (dist 162): it's pushed, the heap hits size 3, and the max-heap's root is now 162 — so `[9,9]` is popped straight back out. The heap absorbs it with no effect.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n log k)</summary>

**O(n log k)**, where n is the number of points.

| Step | Cost |
|---|---|
| Compute one squared distance | O(1) |
| `heappush` | O(log k) — the heap never exceeds k+1 |
| `heappop` (when over) | O(log k) |
| Over all n points | **O(n log k)** |
| Build the result | O(k) |

**Versus sorting: O(n log n).** The gap matters most when **k ≪ n**:

| n | k | Sort: n log n | Heap: n log k |
|---|---|---|---|
| 10⁴ | 10⁴ | ~1.3·10⁵ | ~1.3·10⁵ — identical |
| 10⁴ | 100 | ~1.3·10⁵ | ~6.6·10⁴ |
| 10⁴ | **10** | ~1.3·10⁵ | **~3.3·10⁴** |

When `k` approaches `n` the heap loses its advantage entirely — worth saying, because it shows you understand *when* the optimization applies rather than reaching for it reflexively.

**Quickselect is O(n) average** — better still, by partitioning around the k-th element and recursing into only one side. Its O(n²) worst case (bad pivots) and fiddlier implementation make the heap the safer choice under interview pressure.

**Skipping `sqrt` doesn't change the complexity**, but it removes n floating-point operations and all rounding concerns.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(k)</summary>

**O(k)** auxiliary — the heap never exceeds k+1 elements, and the output is the required k points.

**Compare across the approaches:**

| Approach | Time | Auxiliary space |
|---|---|---|
| Sort | O(n log n) | O(n) — Python's sort |
| Min-heap of all n | O(n + k log n) | **O(n)** |
| **Max-heap of k** | **O(n log k)** | **O(k)** |
| Quickselect | O(n) avg | O(1) in place |

**The size-k heap wins decisively on space**, and that's often the more important axis. With n = 10⁶ streaming points and k = 10, the capped heap holds **ten** entries while every other approach needs all million in memory.

**The streaming property is the real payoff.** This algorithm never needs the full array — it processes points one at a time and keeps only the current best k. That makes it viable on data that doesn't fit in memory, exactly like [Kth Largest Element in a Stream](703-kth-largest-element-in-a-stream.md).

Quickselect, by contrast, **requires random access to the whole array** to partition it — O(1) extra space but O(n) resident. Different trade, worth naming: *the heap streams; Quickselect doesn't.*

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Two things first: the square root is unnecessary, because it's monotonic and I only compare distances — so I use squared distances and keep everything in exact integers. Then, since I need the k closest and the order doesn't matter, I don't need a full sort. I keep a max-heap capped at size k holding the closest points so far; each new point is pushed, and if the heap exceeds k I pop the farthest, which is the one that can no longer be in the answer. It's a *max*-heap even though I want the *closest* points, because the element I need instant access to is the one I'll evict. Python's heapq is a min-heap so I negate the distance, and I carry the coordinates in the tuple so I can read the answer straight out. O(n log k) time and O(k) space — better than sorting's O(n log n) and O(n) when k is much smaller than n."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why skip the square root?" | **The question.** `√` is monotonic, so it preserves the ordering — and dropping it keeps the arithmetic exact. |
| "Why a **max**-heap for the *closest* points?" | You need O(1) access to the point you'll **evict**, which is the farthest. The heap type is always the opposite of what you're selecting for. |
| "Can you do better than O(n log k)?" | Quickselect: O(n) average by partitioning around the k-th element. O(n²) worst case, and it needs the whole array in memory. |
| "When is sorting just as good?" | When k is close to n — then log k ≈ log n and the heap's advantage vanishes. |
| "What if the points streamed in?" | The heap handles it natively — only k are ever held. Quickselect can't; it needs random access to everything. |
| "Distance from an arbitrary point, not the origin?" | Same code with `(x−px)² + (y−py)²`. |
| "What if there were ties at the boundary?" | The problem guarantees uniqueness. Otherwise you'd need a stated rule, or return any valid set — **ask**. |

**Traps:**

- **Using `math.sqrt`.** Unnecessary, slower, and it introduces floating-point comparison risk.
- **Using a min-heap.** You'd have O(1) access to the closest point — which you never want to remove — making evictions O(k).
- **Pushing bare distances** without the coordinates, then having to map distances back to points (and failing on duplicates).
- **Letting the heap grow to n** — correct, but forfeits the O(k) space that's the whole point.
- **Sorting the result.** Unnecessary work; the problem accepts any order.
- **Forgetting to negate**, so you'd be keeping the k *farthest* points.

**This same move shows up in:** [Kth Largest Element in a Stream](703-kth-largest-element-in-a-stream.md) (the size-k heap, with the type flipped) · [Kth Largest Element in an Array](215-kth-largest-element-in-an-array.md) (where Quickselect is the headline answer) · [Last Stone Weight](1046-last-stone-weight.md) (the negation trick) · [Merge k Sorted Lists](23-merge-k-sorted-lists.md) (payload carried in heap tuples).

</details>

---
