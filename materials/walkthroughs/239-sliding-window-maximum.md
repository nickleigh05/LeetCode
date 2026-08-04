# 239. Sliding Window Maximum

**Hard** · [LeetCode](https://leetcode.com/problems/sliding-window-maximum/)

[📖 03. Sliding Window lesson](../learning/03-sliding-window.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 03. Sliding Window problems](../rmap-practice/03-sliding-window.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

You're given an array `nums` and a sliding window of size `k` moving from the very left to the very right. You can only see the `k` numbers inside the window, and it moves one position to the right each step.

Return an array of the **maximum** of each window.

```
nums = [1,3,-1,-3,5,3,6,7], k = 3  →  [3,3,5,5,6,7]

window                max
[1  3  -1] -3  5  3  6  7    3
 1 [3  -1  -3] 5  3  6  7    3
 1  3 [-1  -3  5] 3  6  7    5
 1  3  -1 [-3  5  3] 6  7    5
 1  3  -1  -3 [5  3  6] 7    6
 1  3  -1  -3  5 [3  6  7]   7
```

**Constraints:** `1 <= nums.length <= 10⁵` · `-10⁴ <= nums[i] <= 10⁴` · `1 <= k <= nums.length`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "window of size **k**" | A **fixed**-size window, like [Permutation in String](567-permutation-in-string.md) — no shrink logic |
| "the **maximum** of each window" | ⚠️ An **aggregate query**, not a validity test. Every window problem so far asked *"is this valid?"*; this asks *"what's the max?"* |
| "return **an array**" | One answer per window — `n - k + 1` of them. No single running best |
| n up to 10⁵ | O(n·k) is 10¹⁰ in the worst case → dead. Target **O(n)** |
| values can be **negative** | Don't initialize a running max to 0 |

**Why this is harder than the earlier fixed-size window.** In [Permutation in String](567-permutation-in-string.md), the window's state (letter counts) updated in O(1) on a slide, because adding and removing a character each touch one counter.

A **maximum** doesn't work that way. Adding an element is easy — compare with the current max. But **removing** is the problem: if the element leaving the window *was* the maximum, the new maximum is some other element you never tracked, and you'd have to rescan all k of them. That rescan is what makes the naive solution O(n·k).

So the real question is: **what should you remember so that removals don't force a rescan?**

The insight. Consider two elements in the window, `nums[i]` and `nums[j]` with `i < j` and `nums[i] <= nums[j]`. Can `nums[i]` ever be the answer for a future window? No — any future window containing `i` also contains `j` (since `j` is further right and windows only move right), and `nums[j]` is at least as large. **`nums[i]` is permanently useless.**

So you only need to keep elements that are *strictly decreasing* from front to back. That collection is a **monotonic deque**, and its front is always the current maximum.

🤔 **Before you open the next section:** if a smaller element arrives *after* a bigger one, can the smaller one ever be a window maximum? What if it arrives *before*?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Brute force | Scan all k elements per window | O(n·k) | ❌ 10¹⁰ worst case |
| Max-heap | Push all, pop stale entries lazily | O(n log n) | ⚠️ Works, and a fine fallback — but log n and O(n) space |
| [Segment tree](../data-structures/segment-tree.md) | Range-max queries | O(n log n) | ❌ Enormous overkill |
| **Monotonic deque** | Keep only viable max candidates | **O(n)** | ✅ |

**The decision: a [monotonic decreasing deque](../data-structures/monotonic-stack.md) holding *indices*.**

The deque maintains one invariant:

> **Values at the stored indices are in strictly decreasing order from front to back, and every index is inside the current window.**

Given that, `queue[0]` is *always* the index of the current window's maximum — reading the answer is O(1).

Two maintenance rules keep the invariant true:

1. **Back (before pushing `i`):** pop while `nums[back] < nums[i]`. Those elements are smaller *and* older, so by the argument in section 1 they can never be a maximum again. This is what keeps the deque decreasing.
2. **Front (after pushing):** if `queue[0]` has slid out of the window, pop it. This is why we store **indices, not values** — you can't tell from a value whether it's still in range.

**Why a deque and not a stack or queue?** You need to remove from **both** ends: the back for the monotonic property, the front for the window boundary. `collections.deque` gives O(1) at both. A list would make `pop(0)` an O(n) shift, silently degrading the whole thing to O(n²).

**Why not the heap?** It's genuinely reasonable and worth naming: push every element, and when reading the max, discard heap entries whose index has expired. O(n log n) time, O(n) space. If the deque insight doesn't come to you in an interview, **say the heap solution out loud rather than stalling** — a working O(n log n) beats a stalled O(n).

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
from collections import deque
```

A double-ended queue with O(1) append and pop at **both** ends — the property this whole solution rests on.
→ [from-import](../syntax/from-import.md) · [deque](../data-structures/deque.md) · [deque-basics](../syntax/deque-basics.md)

```python
queue = deque()
result = []
```

`queue` holds **indices** (not values) in decreasing order of their values. `result` collects one maximum per window.
→ [list-basics](../syntax/list-basics.md)

```python
for i, num in enumerate(nums):
```

One pass. `enumerate` gives both, and we need the index for the window-boundary check.
→ [enumerate](../syntax/enumerate.md) · [for-loop](../syntax/for-loop.md)

```python
    while queue and nums[queue[-1]] < num:
        queue.pop()
```

**Maintain the monotonic property.** Pop every element at the back that's smaller than the incoming value — each is both smaller and older, so it can never be a maximum while `num` remains in the window.

`queue and ...` guards against popping from an empty deque. `queue[-1]` is the back; `.pop()` removes from the back.
→ [while-loop](../syntax/while-loop.md) · [truthy-falsy-values](../syntax/truthy-falsy-values.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
    queue.append(i)
```

Push the new index at the back. The deque is now decreasing again, with `i` as its smallest value.

```python
    if queue[0] <= i - k:
        queue.popleft()
```

**Maintain the window boundary.** The current window covers indices `[i - k + 1, i]`, so anything at or below `i - k` has expired. `.popleft()` removes from the front in O(1).

One check suffices — at most one index falls out per step, since the window advances by exactly one.
→ [if-return](../syntax/if-return.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
    if i >= k - 1:
        result.append(nums[queue[0]])
```

Record — but only once a **full** window exists. The first complete window ends at index `k - 1`; before that we're still filling up and there's no window to report.

`queue[0]` is the front, holding the index of the current maximum. O(1) to read.
→ [list-methods](../syntax/list-methods.md)

```python
return result
```

<details>
<summary>The whole thing together</summary>

```python
from collections import deque

class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:

        queue = deque()
        result = []

        for i, num in enumerate(nums):
            while queue and nums[queue[-1]] < num:
                queue.pop()
            queue.append(i)

            if queue[0] <= i - k:
                queue.popleft()

            if i >= k - 1:
                result.append(nums[queue[0]])

        return result
```

</details>

**Trace it** — `nums = [1,3,-1,-3,5,3,6,7]`, `k = 3` (deque shown as *index(value)*):

| `i` | `num` | Pop from back | Deque after | Expire front? | Record |
|---|---|---|---|---|---|
| 0 | 1 | — | `0(1)` | no | — (not full) |
| 1 | 3 | pop `0(1)` — smaller | `1(3)` | no | — |
| 2 | −1 | — (−1 < 3) | `1(3) 2(-1)` | no | **3** |
| 3 | −3 | — | `1(3) 2(-1) 3(-3)` | no | **3** |
| 4 | 5 | pop `3(-3)`, `2(-1)`, `1(3)` | `4(5)` | no | **5** |
| 5 | 3 | — | `4(5) 5(3)` | no | **5** |
| 6 | 6 | pop `5(3)`, `4(5)` | `6(6)` | no | **6** |
| 7 | 7 | pop `6(6)` | `7(7)` | no | **7** |

Result: `[3,3,5,5,6,7]` ✅

Look at `i = 4`: the arrival of `5` wiped out three stored candidates at once. Each of them was smaller *and* older, so none could ever win again — that mass eviction is the deque earning its keep.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** — and the inner `while` loop makes this the thing to justify.

The argument is about **total** work, not per-iteration work:

> **Every index is appended to the deque exactly once, and popped at most once** (from the back by the monotonic rule, or from the front by the window rule). With n indices, that's at most n pushes and n pops across the entire run — 2n deque operations total.

Each operation is O(1) on a deque. Plus n iterations of O(1) bookkeeping → **O(n)**.

The inner `while` can pop many elements in a single iteration (see `i = 4` above, which popped three) — but those pops are "paid for" by the pushes that put them there. This is the **amortized** argument again, in its cleanest form: *if each element can only be removed once, the total removal cost is bounded by the number of elements.*

**Versus the alternatives:** brute force O(n·k) → 10¹⁰; heap O(n log n) → ~1.7·10⁶; deque O(n) → 10⁵.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(k)</summary>

**O(k)** auxiliary.

The deque never holds more than `k` indices — every index inside it is within the current window, and the window has exactly `k` positions. The front-expiry check enforces that bound.

- **Worst case, O(k):** a strictly decreasing array like `[9,8,7,6,…]`. Nothing is ever popped from the back (each new value is smaller), so the deque fills to `k`.
- **Best case, O(1):** a strictly increasing array like `[1,2,3,…]`. Each new value evicts everything before it, so the deque holds a single index.

`result` is O(n − k + 1), but it's the required output and conventionally excluded from auxiliary space. Say **"O(k) auxiliary, plus O(n − k + 1) for the output"** to be precise.

**Compared to the heap:** the lazy-deletion heap holds up to n entries (expired ones linger until they surface), so **O(n)** space. The deque is better on both axes — it discards candidates eagerly the moment they're provably useless, rather than lazily when they get in the way.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Rescanning each window is O(n·k). The problem with maintaining a running max is removal — when the max slides out, you'd have to rescan. The insight is that if an element is smaller than something that came *after* it, it can never be a future window max, because every window containing it also contains the bigger, newer one. So I keep a deque of indices whose values are decreasing: before pushing, I pop smaller values off the back; then I pop the front if it's slid out of the window. The front is always the current maximum, read in O(1). Each index is pushed and popped at most once, so it's O(n) time and O(k) space. A max-heap with lazy deletion also works at O(n log n) and O(n) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why store indices instead of values?" | **The question.** The front-expiry check needs to know *where* an element came from — a value alone can't tell you whether it's still in the window. |
| "Why is the nested `while` still O(n)?" | Each index is pushed once and popped once, so total pops ≤ n across the whole run. Amortized, not per-iteration. |
| "Sliding window **minimum**?" | Flip the comparison — keep an increasing deque. Same code, `>` instead of `<`. |
| "Both min and max?" | Run two deques in parallel. Still O(n). |
| "What if `k` changes as you go?" | The deque breaks (its bound assumes fixed `k`). Switch to a heap or a segment tree. |
| "Solve it with a heap." | Push `(-num, i)`; before reading the max, `popleft` while the top's index has expired. O(n log n), O(n) space. |
| "Can you do better than O(n)?" | No — you must at minimum read all n inputs and write n−k+1 outputs. |

**Traps:**

- **Storing values instead of indices.** You then can't detect expiry. The most common wrong first attempt.
- **Using a list with `pop(0)`.** That's an O(n) shift each time, turning the solution into O(n²). Use `collections.deque`.
- **Popping the front before pushing.** Order matters — push first, then expire, so the boundary check sees the final state.
- **`queue[0] < i - k`** instead of `<=`. Off by one; the element at exactly `i - k` has already left the window.
- **Recording before a full window exists** — you'd emit `k - 1` spurious answers. Guard with `i >= k - 1`.
- **Popping the back on `<=` vs `<`.** Both work here (equal values are interchangeable as maxima); `<` keeps duplicates, which matters if you ever adapt this to count occurrences.

**This same move shows up in:** [Daily Temperatures](739-daily-temperatures.md) and [Largest Rectangle in Histogram](84-largest-rectangle-in-histogram.md) (the [monotonic stack](../data-structures/monotonic-stack.md) — same "discard the provably useless" idea, one end instead of two) · [Permutation in String](567-permutation-in-string.md) (fixed-size window with incremental state) · [Trapping Rain Water](42-trapping-rain-water.md) (running maxima maintained without rescanning).

</details>
