# 1046. Last Stone Weight

**Easy** · [LeetCode](https://leetcode.com/problems/last-stone-weight/) · [Solution file (no hints)](../../problems/1000-1499/1046.py)

[📖 09. Heap / Priority Queue lesson](../learning/09-heap-priority-queue.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 09. Heap / Priority Queue problems](../rmap-practice/09-heap-priority-queue.md)

---

You're given an array of integers `stones` where `stones[i]` is the weight of the i-th stone.

Each turn, choose the **two heaviest** stones and smash them together. If they weigh `x` and `y` with `x <= y`:
- If `x == y`, **both are destroyed**.
- If `x != y`, the stone of weight `x` is destroyed and the other becomes weight `y - x`.

Return the weight of the last remaining stone, or `0` if none remain.

```
stones = [2,7,4,1,8,1]  →  1

  smash 8,7 → 1     stones become [2,4,1,1,1]
  smash 4,2 → 2     [2,1,1,1]
  smash 2,1 → 1     [1,1,1]
  smash 1,1 → 0     [1]
  →  1
```

**Constraints:** `1 <= stones.length <= 30` · `1 <= stones[i] <= 1000`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "the **two heaviest**" | ⚠️ You need repeated access to the **maximum** — and the set changes after every smash |
| "the other becomes `y - x`" | The result **re-enters** the pool and may be smashed again |
| "**each turn**" until ≤ 1 remains | A simulation loop, not a formula |
| "`0` if none remain" | Handle the empty case |
| n ≤ 30 | Tiny — the point is choosing the right structure, not squeezing performance |

The process is a straightforward simulation; the only question is **how to find the two largest values repeatedly** while the collection keeps changing.

That phrasing is the signal:

> **Repeatedly need the extreme element, from a set that keeps changing** → a **heap**.

Contrast the alternatives. Sorting gives you the largest, but after a smash you'd have to re-sort or insert the new stone in order — O(n) per turn. Scanning for the max twice is also O(n). A heap does both the extraction and the reinsertion in O(log n).

**The Python-specific wrinkle.** `heapq` is a **min**-heap only — there's no max-heap in the standard library. Since you need maxima, you negate:

```
stones:     [2, 7, 4, 1, 8, 1]
negated:   [-2,-7,-4,-1,-8,-1]

the min of the negated values (-8) is the max of the originals (8) ✅
```

Negate on the way in, negate on the way out. It's the standard idiom and worth having in reflex memory.

🤔 **Before you open the next section:** after smashing, when do you push something back — and what happens to the loop if you push a zero?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Per turn | Total | Verdict |
|---|---|---|---|
| Re-sort each turn | O(n log n) | O(n² log n) | ❌ Re-derives an order you mostly still have |
| Scan for the two largest | O(n) | O(n²) | ⚠️ Fine at n = 30, but wrong instinct |
| Sorted list + `bisect.insort` | O(n) for the shift | O(n²) | ⚠️ Log-time lookup, linear insertion |
| **Max-heap (negated min-heap)** | **O(log n)** | **O(n log n)** | ✅ |

**The decision: a [max-heap](../data-structures/heap.md), simulated by negating values in Python's min-heap.**

Each turn is three heap operations:
1. Pop the largest.
2. Pop the second largest.
3. If they differ, push back the difference.

**Why the heap fits so exactly.** A heap maintains only a *partial* order — enough to know the extreme, not enough to know the full ranking. That's precisely what this problem needs: you never care about the 3rd or 4th heaviest stone, only the top two. **Sorting would compute a total order you'd immediately invalidate.**

**Why negation works.** Negating reverses the ordering, so the min-heap's root is the most-negative value — which corresponds to the largest original. The two conversions are trivially cheap:

```python
heapq.heappush(heap, -value)    # in
value = -heapq.heappop(heap)    # out
```

*(For floats or objects the mirror trick gets awkward; then you'd wrap values in a class with an inverted `__lt__`, or push `(-key, item)` tuples as in [Merge k Sorted Lists](23-merge-k-sorted-lists.md).)*

**Why `heapify` rather than pushing one at a time.** `heapq.heapify(list)` rearranges an existing list into a valid heap **in place, in O(n)** — better than n individual O(log n) pushes, which total O(n log n). A small but free win, and worth knowing it exists.

**Why nothing is pushed when `x == y`.** Both stones are destroyed and the difference is 0. Pushing a 0 would be *almost* harmless — it'd sit at the bottom — but it would linger in the heap and could become the final answer on inputs where the true result should be 0 anyway. Cleaner to skip it, and it matches the problem statement exactly.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
import heapq

heap = [-s for s in stones]
heapq.heapify(heap)
```

**Negate everything, then heapify.** The comprehension flips every sign so the min-heap behaves as a max-heap; `heapify` rearranges the list into heap order **in O(n)**, in place.

Cheaper than pushing stones one at a time — a small optimization that costs nothing to write.
→ [import-basics](../syntax/import-basics.md) · [list-comprehension](../syntax/list-comprehension.md) · [heapq-module](../syntax/heapq-module.md) · [heap](../data-structures/heap.md)

```python
while len(heap) > 1:
```

Keep smashing while at least **two** stones remain. When 0 or 1 are left, the process is over.
→ [while-loop](../syntax/while-loop.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
    first = -heapq.heappop(heap)
    second = -heapq.heappop(heap)
```

**Pop the two largest**, negating on the way out to recover the real weights.

Because the heap is negated, `heappop` returns the most-negative value — the heaviest stone. And since `first` is popped before `second`, we know `first >= second`, so `first - second` is never negative. **The ordering is guaranteed by the heap, not by an explicit comparison.**
→ [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
    if first != second:
        heapq.heappush(heap, -(first - second))
```

**Push back the remainder**, negated again to preserve the max-heap encoding.

Equal stones destroy each other, so nothing is pushed — the heap shrinks by two. Unequal stones leave one behind, so it shrinks by one. **Either way the heap shrinks, which is what guarantees termination.**

Note the double negation: `-(first - second)`. Forgetting the outer minus is the classic bug here.
→ [if-return](../syntax/if-return.md)

```python
return -heap[0] if heap else 0
```

**One stone left → return it** (negated back to positive). **Empty heap → return 0**, meaning every stone was destroyed.

The ternary handles both cases in one line, and `heap` being falsy when empty makes the check natural.
→ [ternary-expression](../syntax/ternary-expression.md) · [truthy-falsy-values](../syntax/truthy-falsy-values.md)

<details>
<summary>The whole thing together</summary>

```python
import heapq

class Solution:
    def lastStoneWeight(self, stones: List[int]) -> int:

        heap = [-s for s in stones]
        heapq.heapify(heap)

        while len(heap) > 1:
            first = -heapq.heappop(heap)
            second = -heapq.heappop(heap)
            if first != second:
                heapq.heappush(heap, -(first - second))

        return -heap[0] if heap else 0
```

</details>

**Trace it** — `stones = [2,7,4,1,8,1]`:

Negated and heapified, the heap represents the multiset `{8,7,4,2,1,1}`.

| Turn | Pop `first` | Pop `second` | Equal? | Push | Remaining stones |
|---|---|---|---|---|---|
| 1 | **8** | **7** | no | `8−7 = 1` | `{4,2,1,1,1}` |
| 2 | **4** | **2** | no | `4−2 = 2` | `{2,1,1,1}` |
| 3 | **2** | **1** | no | `2−1 = 1` | `{1,1,1}` |
| 4 | **1** | **1** | **yes** | — (both destroyed) | `{1}` |

`len(heap) == 1` → loop ends → return **1** ✅

Turn 4 is the case that shrinks the heap by two: equal stones annihilate and nothing is pushed back.

**And an all-destroyed case** — `stones = [2,2]`:

| Turn | `first` | `second` | Equal? | Heap after |
|---|---|---|---|---|
| 1 | 2 | 2 | yes | empty |

`heap` is falsy → return **0** ✅

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n log n)</summary>

**O(n log n)**, where n is the number of stones.

| Step | Cost |
|---|---|
| Negate all values | O(n) |
| `heapify` | **O(n)** — not O(n log n); the bottom-up construction is linear |
| Each turn: 2 pops + ≤1 push | O(log n) |
| Number of turns | **at most n − 1** |

**Why at most n−1 turns.** Every turn removes two stones and adds back at most one, so the count strictly decreases. Starting from n, the loop can run at most n−1 times before fewer than two remain.

(n−1) × O(log n) = **O(n log n)** overall.

**Versus the alternatives:**

| Approach | Total |
|---|---|
| Re-sort each turn | O(n² log n) |
| Scan for the max twice | O(n²) |
| **Heap** | **O(n log n)** |

At n = 30 all of these are instantaneous — this problem is about **recognizing the structure**, not about performance. But the same pattern at n = 10⁵ would make the difference decisive, which is why it's worth internalizing here where it's easy.

**Note `heapify` is O(n), not O(n log n)** — a genuinely useful fact. Building a heap from an existing list is cheaper than inserting elements one at a time, because most elements are near the bottom and sift down only a short distance.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** — the heap holds every stone.

Unlike [Kth Largest Element in a Stream](703-kth-largest-element-in-a-stream.md), which capped its heap at k, this heap must hold **everything**: any stone could eventually become one of the two heaviest as larger ones are consumed. There's nothing safe to discard.

**The distinction is worth noting explicitly**, since both problems use a heap for different reasons:

| Problem | Heap size | Why |
|---|---|---|
| [703](703-kth-largest-element-in-a-stream.md) | **O(k)** | Values outside the top k are permanently irrelevant |
| **1046** | **O(n)** | Every stone can eventually surface as a maximum |

The list comprehension creates a new negated list — you *could* negate in place to save that copy, but at O(n) either way it makes no difference.

**A note on `heapify` being in place:** it rearranges the existing list rather than allocating a new structure, so the only allocation is the negated copy.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Each turn I need the two heaviest stones, and the collection changes after every smash — repeatedly needing the extreme from a changing set is exactly what a heap is for. Sorting would give a total order I'd immediately invalidate; a heap maintains just enough structure to surface the maximum, and both extraction and reinsertion are O(log n). Python's `heapq` is a min-heap only, so I negate the values on the way in and out to simulate a max-heap. Each turn pops two, and pushes back the difference unless they're equal, in which case both are destroyed. The heap shrinks every turn, so there are at most n−1 turns — O(n log n) overall. I use `heapify` rather than pushing individually, since building a heap from a list is O(n)."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "How do you get a max-heap in Python?" | **The question.** Negate on push and pop. For non-numeric items, push `(-key, item)` tuples or wrap them with an inverted `__lt__`. |
| "Why not just sort?" | Sorting computes a total order that a single smash invalidates. You'd re-sort or insert every turn — O(n) per turn versus O(log n). |
| "Why is `heapify` better than n pushes?" | It's O(n) versus O(n log n) — most elements are near the bottom and sift down only a little. |
| "**Last Stone Weight II** — minimize the final weight?" | Completely different: partition the stones into two subsets with minimal difference. That's subset-sum DP, not a heap. LeetCode 1049. |
| "What if you smashed the two **lightest**?" | Use the min-heap directly, no negation. |
| "What if n were 10⁵?" | The heap version still works at O(n log n); the scanning version would be 10¹⁰. |
| "Why at most n−1 turns?" | Each turn removes two stones and adds back at most one, so the count strictly decreases. |

**Traps:**

- **Forgetting to negate on the way out** — you'd compute with negative weights and get nonsense.
- **Forgetting to negate the pushed difference** (`heappush(heap, first - second)`) — the heap's ordering silently breaks.
- **Pushing when `first == second`.** A stray 0 lingers in the heap; harmless in most cases but it doesn't match the statement.
- **Assuming `first <= second`.** The pop order guarantees `first >= second`; getting it backwards makes the difference negative.
- **`while heap`** instead of `while len(heap) > 1` — you'd pop from a heap with one element and crash.
- **Forgetting the empty case** — `heap[0]` on an empty list raises `IndexError`.
- **Using `heap[1]`** to get the second largest. Only index 0 is guaranteed; the rest of the array isn't sorted.

**This same move shows up in:** [Kth Largest Element in a Stream](703-kth-largest-element-in-a-stream.md) (a heap for repeated extremes, capped at k) · [K Closest Points to Origin](973-k-closest-points-to-origin.md) (the negation trick for a max-heap) · [Task Scheduler](621-task-scheduler.md) (repeatedly taking the most frequent task) · [heap](../data-structures/heap.md).

</details>
