# 1962. Remove Stones to Minimize the Total

**Medium** · [LeetCode](https://leetcode.com/problems/remove-stones-to-minimize-the-total/) · [Solution file (no hints)](../../problems/1500-1999/1962.py)

[📖 09. Heap / Priority Queue lesson](../learning/09-heap-priority-queue.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 09. Heap problems](../rmap-practice/09-heap-priority-queue.md)

---

Given `piles` where `piles[i]` is a stone count, apply this operation **exactly `k` times**: choose any pile and remove `floor(piles[i] / 2)` stones from it. The same pile may be chosen repeatedly. Return the **minimum possible total** remaining.

```
piles = [5,4,9], k = 2  →  12   (9→5 gives [5,4,5]; 5→3 gives [3,4,5])
piles = [4,3,6,7], k = 3  →  12
```

**Constraints:** `1 <= piles.length <= 10⁵` · `1 <= piles[i] <= 10⁴` · `1 <= k <= 10⁵`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| remove `floor(pile / 2)` | ⚠️ The pile is **halved** (rounding up what remains): `9 → 9 − 4 = 5` |
| "**minimize** the total" | Each operation should remove as many stones as possible |
| "**exactly `k`** times" | You must use all operations — though halving a pile of 1 removes 0, so extra operations are harmless |
| same pile **repeatedly** | A pile can be halved over and over |
| `n`, `k` up to 10⁵ | O(k · n) = 10¹⁰ is far too slow; you need O(k log n) |

**The greedy insight, and it's worth proving rather than assuming:**

> **Always halve the largest pile.**

Why? Halving a pile of size `p` removes `floor(p/2)` stones — an amount that **increases monotonically with `p`**. So at every step, the largest pile yields the biggest immediate reduction.

But greedy choices need more than "biggest now" — they need to not sabotage the future. Here they don't, because the piles are **independent**: halving one never changes what any other pile would yield. There's no interaction to trade off, so taking the maximum reduction at each step is optimal by a straightforward exchange argument.

**What that demands of the data structure.** You need, repeatedly:

1. the **maximum** element, and
2. to **replace** it with a smaller value, keeping the structure valid

That's precisely a **max-heap**: O(1) peek, O(log n) pop, O(log n) push.

```
[5,4,9]  k=2

step 1: max is 9 → remove 4 → becomes 5      piles [5,4,5]
step 2: max is 5 → remove 2 → becomes 3      piles [3,4,5]
                                              total = 12 ✅
```

🤔 **Before you open the next section:** if halving a pile removes `floor(p/2)` stones, which pile gives the biggest reduction — and does that choice ever hurt a later step?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Scan for the max each round | Linear search, halve it | O(k · n) | O(1) | ❌ 10¹⁰ operations |
| Re-sort each round | Sort, halve the last | O(k · n log n) | O(n) | ❌ Worse still |
| **Max-heap** | Pop the max, push the half back | **O(n + k log n)** | O(n) | ✅ |
| Counting / bucket by value | Values ≤ 10⁴, so bucket them | O(n + k + maxval) | O(maxval) | ✅ Viable alternative |

**The decision: a max-heap.**

Each of the `k` operations is: pop the largest, compute the remainder, push it back. Both operations are O(log n), so the total is **O(k log n)** after an O(n) build.

**The Python wrinkle: `heapq` is a *min*-heap.** There's no max-heap in the standard library, so the idiomatic workaround is to **negate every value**:

```python
heap = [-p for p in piles]      # negate on the way in
heapq.heapify(heap)             # O(n)

largest = -heapq.heappop(heap)  # negate on the way out
```

The most negative number is the smallest, so it sits at the min-heap's root — and negating it back gives the true maximum. Every push must be negated too. **Forgetting one negation is the classic bug here**, and it produces a plausible-looking wrong answer rather than a crash.

**Why `heapify` rather than repeated `heappush`.** Building a heap from an existing list is **O(n)** via `heapify`, versus O(n log n) for `n` separate pushes. At `n = 10⁵` that's a real difference, and it's free — one function call.

**Why the remaining count is `p − p//2`, i.e. `ceil(p/2)`.** The problem says you *remove* `floor(p/2)`, so what stays is `p − floor(p/2)`. For odd `p` that's the larger half: `9 → 9 − 4 = 5`. Writing `p // 2` for the remainder would remove too much on odd piles.

**The bucket alternative**, worth naming: since `piles[i] <= 10⁴`, you can keep a count array indexed by pile size and sweep downward from the maximum. That's O(n + k + maxval) with no log factor — faster in theory, but the heap is clearer and 10⁵ · log(10⁵) ≈ 1.7 × 10⁶ operations is already trivial.

**Why extra operations are harmless.** If every pile reaches 1, halving removes `1 // 2 = 0` stones. So even when `k` exceeds what's useful, the loop stays correct — no guard needed for "nothing left to remove."

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
import heapq

max_heap = [-p for p in piles]
heapq.heapify(max_heap)
```

**Negate everything to simulate a max-heap**, then build in **O(n)**.

`heapify` rearranges the list in place — no extra allocation beyond the negated copy.
→ [heapq-module](../syntax/heapq-module.md) · [list-comprehension](../syntax/list-comprehension.md)

```python
for _ in range(k):
    largest = -heapq.heappop(max_heap)
```

**Pop the maximum**, negating on the way out to recover the true value.

`heappop` returns the smallest stored value — which, after negation, is the largest real pile.
→ [range-function](../syntax/range-function.md)

```python
    remaining = largest - largest // 2
    heapq.heappush(max_heap, -remaining)
```

**Halve the pile and push it back.**

`largest - largest // 2` is the count that **stays** — equivalently `ceil(largest / 2)`. For `9`: `9 - 4 = 5` ✅. Using `largest // 2` directly would remove the wrong half on odd piles.

Negate again on the way in to preserve the max-heap simulation.
→ [integer-division-modulo](../syntax/integer-division-modulo.md) · [heapq-module](../syntax/heapq-module.md)

```python
return -sum(max_heap)
```

**Sum and flip the sign.**

The heap holds negated values, so their sum is the negative of the true total. One negation at the end is cheaper and cleaner than negating each element first.
→ [any-all](../syntax/any-all.md)

<details>
<summary>The whole thing together</summary>

```python
import heapq

class Solution:
    def minStoneSum(self, piles: List[int], k: int) -> int:

        max_heap = [-p for p in piles]
        heapq.heapify(max_heap)

        for _ in range(k):
            largest = -heapq.heappop(max_heap)
            remaining = largest - largest // 2
            heapq.heappush(max_heap, -remaining)

        return -sum(max_heap)
```

</details>

<details>
<summary>The bucket-counting alternative (no log factor)</summary>

```python
class Solution:
    def minStoneSum(self, piles: List[int], k: int) -> int:
        MAX = 10 ** 4
        count = [0] * (MAX + 1)
        for p in piles:
            count[p] += 1

        total = sum(piles)
        value = MAX
        while k > 0 and value > 1:
            if count[value] == 0:
                value -= 1
                continue
            take = min(count[value], k)
            removed = value // 2
            total -= removed * take
            count[value] -= take
            count[value - removed] += take
            k -= take

        return total
```

Exploits `piles[i] <= 10⁴` to sweep values downward instead of using a heap. O(n + k + maxval), no logarithm — but noticeably more code and it only works because the value range is bounded.

</details>

**Trace it** — `piles = [5,4,9]`, `k = 2`:

| Step | Heap (as real values) | Pop max | Remove `//2` | Remaining | Heap after |
|---|---|---|---|---|---|
| start | `[9,5,4]` | — | — | — | — |
| 1 | | **9** | 4 | `9 − 4 = 5` | `[5,5,4]` |
| 2 | | **5** | 2 | `5 − 2 = 3` | `[5,4,3]` |

Total = `5 + 4 + 3` = **12** ✅

Internally the heap stores `[-9,-5,-4]` → `[-5,-5,-4]` → `[-5,-4,-3]`, and `-sum([-5,-4,-3])` = 12.

**A second trace** — `piles = [4,3,6,7]`, `k = 3`:

| Step | Pop max | Removed | Remaining | Piles after |
|---|---|---|---|---|
| 1 | **7** | 3 | 4 | `[4,3,6,4]` |
| 2 | **6** | 3 | 3 | `[4,3,3,4]` |
| 3 | **4** | 2 | 2 | `[2,3,3,4]` |

Total = `2 + 3 + 3 + 4` = **12** ✅

Step 3 shows why re-pushing matters: after two operations the maximum has changed twice, and the heap surfaces the current maximum each time without any re-scanning.

**The odd-pile detail** — at step 1, pile 7 removes `7 // 2 = 3` and keeps **4**, not 3. Using `7 // 2` as the remainder would have kept 3 and over-removed.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n + k log n)</summary>

**O(n + k log n).**

| Phase | Cost |
|---|---|
| Negate and `heapify` | **O(n)** |
| `k` iterations of pop + push | **O(k log n)** |
| Final `sum` | O(n) |

At `n = k = 10⁵`: `10⁵ + 10⁵ × 17` ≈ **1.8 × 10⁶ operations** — instant.

**Compare:**

| | Time at n = k = 10⁵ |
|---|---|
| Scan for max each round | O(k·n) = **10¹⁰** ❌ |
| Re-sort each round | O(k·n log n) — worse ❌ |
| **Max-heap** | **1.8 × 10⁶** ✅ |
| Bucket counting | O(n + k + 10⁴) ≈ 2 × 10⁵ ✅ |

**Why `heapify` beats repeated pushes.** Building via `n` calls to `heappush` is O(n log n); `heapify` is **O(n)**, because the standard bottom-up construction does O(1) amortized work per element. Free improvement, one line.

**An optimization worth mentioning:** once the maximum pile is 1, no further operation removes anything, so you could `break` early. It doesn't change the worst case but avoids pointless work when `k` is large relative to the stone count.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** for the negated heap — one entry per pile.

`heapify` works **in place** on that list, so no additional allocation occurs during the operations.

**Could you avoid the copy?** Yes, by negating `piles` in place and heapifying it directly — but that mutates the caller's input, which is usually worth avoiding unless asked.

| | Space |
|---|---|
| **Max-heap** | **O(n)** |
| Bucket counting | O(maxval) = 10⁴ — constant w.r.t. `n` |

Interestingly the bucket version is O(1) in terms of `n`, since its array is sized by the *value range* rather than the input length. With `n = 10⁵` and `maxval = 10⁴` it actually uses **less** memory — a nice illustration that "which is smaller" depends on the constraints, not on the asymptotic label alone.

**The reusable idea:**

> **A heap is the right structure whenever you repeatedly need the extreme element *and* the collection keeps changing.** Sorting handles a static collection; a heap handles a live one.

That's what separates this from a sort-once problem: every operation modifies a value and the maximum shifts, so the ordering must be maintained dynamically.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Halving a pile removes `floor(p/2)` stones, which grows with `p`, so the greedy choice is always to halve the current largest pile. That's safe because the piles are independent — halving one never affects what another would yield — so there's no future cost to taking the biggest reduction now. I need repeated access to the maximum with updates in between, which is a max-heap. Python's `heapq` is a min-heap, so I negate every value going in and coming out. I use `heapify` for an O(n) build rather than n pushes. The one arithmetic detail is that the pile **keeps** `p − p//2`, which is the larger half for odd piles — using `p//2` would over-remove. O(n + k log n) time, O(n) space. Since values are capped at 10⁴ there's also a bucket-counting version that drops the log factor."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why is the greedy correct?" | `floor(p/2)` increases with `p`, and piles are independent — halving one never changes another's yield, so the max always gives the best reduction with no future cost. |
| "Python has no max-heap." | Negate on push and pop. Or use `heapq._heapify_max` (private, avoid), or wrap values in a comparator class. |
| "Why `heapify` and not `n` pushes?" | `heapify` is O(n); pushes are O(n log n). |
| "Can you drop the log factor?" | Yes — bucket by value, since `piles[i] <= 10⁴`. O(n + k + maxval). |
| "What if `k` exceeds what's useful?" | Halving a pile of 1 removes 0, so extra operations are harmless. You could `break` when the max is 1. |
| "What if removal were `ceil(p/2)`?" | Then the remainder is `p // 2`. Same structure, different arithmetic — read the statement carefully. |
| "Remove a **fixed** number per operation instead?" | The greedy changes: every pile yields the same reduction, so it doesn't matter which you pick — no heap needed. |

**Traps:**

- **Forgetting a negation.** Omitting it on the push turns the max-heap back into a min-heap and you'd halve the *smallest* pile — wrong answer, no error.
- **Using `largest // 2` as the remainder.** That's what's *removed*, not what stays. Odd piles come out one too small.
- **Building with repeated `heappush`.** O(n log n) instead of O(n).
- **Re-scanning for the maximum each round.** O(k·n) = 10¹⁰.
- **Forgetting to negate the final sum.** Returns a negative number.
- **Assuming a min-heap works if you "just reverse at the end."** The greedy needs the maximum *at every step*, not a final ordering.

**This same move shows up in:** [Last Stone Weight](1046-last-stone-weight.md) (the same max-heap-by-negation pattern, repeatedly combining the two largest) · [Kth Largest Element in an Array](215-kth-largest-element-in-an-array.md) (heap selection) · [Task Scheduler](621-task-scheduler.md) (greedily taking the most frequent item via a max-heap) · [Remove Stones… ](https://leetcode.com/problems/remove-stones-to-minimize-the-total/) and [IPO](502-ipo.md) (greedy choices driven by a heap).

</details>

---
