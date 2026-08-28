# 658. Find K Closest Elements

**Medium** · [LeetCode](https://leetcode.com/problems/find-k-closest-elements/) · [Solution file (no hints)](../../problems/0500-0999/658.py)

[📖 05. Binary Search lesson](../learning/05-binary-search.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 05. Binary Search problems](../rmap-practice/05-binary-search.md)

---

Given a **sorted** array `arr`, and integers `k` and `x`, return the `k` closest integers to `x`, sorted ascending. An integer `a` is closer than `b` if `|a − x| < |b − x|`, or if they tie and `a < b`.

```
arr = [1,2,3,4,5],   k = 4, x = 3   →  [1,2,3,4]
arr = [1,1,2,3,4,5], k = 4, x = -1  →  [1,1,2,3]
```

**Constraints:** `1 <= k <= arr.length` · `1 <= arr.length <= 10⁴` · `arr` sorted ascending · `-10⁴ <= arr[i], x <= 10⁴`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**sorted** array" | Enables binary search — and something stronger, below |
| "**k closest**" | Not one element, a **group** of `k` |
| result "sorted ascending" | ⚠️ Combined with sortedness, this implies the answer is a **contiguous window** of `arr` |
| ties broken by "`a < b`" | Prefer the **smaller** value — which biases the window leftward |
| `x` may be outside `arr`'s range | `x = -1` with `arr` starting at 1 — the window then clamps to an edge |
| `arr.length` up to 10⁴ | O(n log n) sorting would pass, but O(log n) is achievable |

**The insight that reframes everything:** because `arr` is sorted, the `k` closest elements are always **contiguous**.

Why? Suppose your answer set skipped some element `m` sitting between two chosen elements `a` and `b`. Since `a < m < b`, `m` is closer to `x` than at least one of `a` or `b` (whichever is on the far side of `x`). So swapping it in improves the set — meaning any optimal set has no gaps.

So the problem is not "pick `k` elements" — it's:

> **Find the starting index of the best length-`k` window.**

That collapses a selection problem into a **single-value search** over `n − k + 1` candidate start positions.

```
arr = [1,2,3,4,5],  k = 4,  x = 3

start 0: [1,2,3,4]   ← best
start 1: [2,3,4,5]
```

🤔 **Before you open the next section:** if you're comparing two candidate windows that differ only at their two ends, which single comparison tells you which one is better?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Sort by distance | `sorted(arr, key=lambda a: abs(a-x))[:k]`, then re-sort | O(n log n) | ⚠️ Correct, ignores sortedness |
| Max-heap of size `k` | Push/pop by distance | O(n log k) | ⚠️ Correct, still linear-ish |
| Find `x`, expand two pointers | Locate `x`, grow outward `k` times | O(log n + k) | ✅ Intuitive, more edge cases |
| **Binary search the window start** | Search over start positions | **O(log(n−k) + k)** | ✅ Tightest, fewest branches |

**The decision: binary search over candidate window **start** positions.**

Search `left = 0` to `right = n - k` — the last valid start for a length-`k` window. At each step compare the two elements that distinguish window `[mid, mid+k-1]` from window `[mid+1, mid+k]`:

```
window at mid:    arr[mid] ... arr[mid+k-1]
window at mid+1:           ... arr[mid+k-1] arr[mid+k]
                  ↑                          ↑
              only difference           only difference
```

The comparison:

```python
if x - arr[mid] > arr[mid + k] - x:
    left = mid + 1      # the right window is better
else:
    right = mid         # the left window is at least as good
```

**Why this comparison is exactly right.** `x - arr[mid]` is how far `x` is from the element you'd *drop* by shifting right; `arr[mid+k] - x` is how far it is from the element you'd *gain*. If the dropped element is farther away, shifting right improves the window.

**Why no `abs()` is needed.** It looks like a distance comparison that ought to use absolute values, but it doesn't:

- If `x < arr[mid]`, then `x - arr[mid]` is negative while `arr[mid+k] - x` is positive (since `arr[mid+k] > arr[mid] > x`), so the condition is correctly false — don't shift right.
- If `x > arr[mid+k]`, both are positive and the comparison is a genuine distance test.
- In between, both sides behave correctly by the same reasoning.

The signed form handles all three cases, which is why the code has no branching on where `x` falls. That's elegant but genuinely subtle — worth tracing once to convince yourself.

**Why `>` and not `>=` handles ties correctly.** On a tie (`x - arr[mid] == arr[mid+k] - x`), the condition is false, so `right = mid` — keeping the **left** window. The problem's tie-break prefers smaller values, so the leftward bias is exactly what's specified. Using `>=` would break the tie the wrong way.

**Why `right = mid` and `left < right`.** The standard boundary convention: `mid` remains a candidate when the left window wins, so it must be kept. Same pairing as [First Bad Version](278-first-bad-version.md).

**Why not the expand-from-`x` approach?** It's a fine O(log n + k) solution — binary search for `x`'s insertion point, then extend two pointers outward `k` times, taking the closer side each step. But it needs careful bounds handling when the window hits either end of the array. The window-start search has no such edge cases: `[0, n-k]` is always a valid range, and clamping happens automatically.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
left = 0
right = len(arr) - k
```

**The range of valid window starts.** A window of length `k` starting at `n - k` ends exactly at `n - 1`, so that's the last legal start.

Note this is *not* the array's index range — it's the range of *answers*, which is what makes this a compact search.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
while left < right:
    mid = (left + right) // 2
```

Boundary-search convention. Because `left < right`, we have `mid < right <= n - k`, so `mid + k <= n - 1` — **`arr[mid + k]` is always in bounds**, with no guard needed.
→ [while-loop](../syntax/while-loop.md)

```python
    if x - arr[mid] > arr[mid + k] - x:
        left = mid + 1
```

**The window-shift decision.**

`arr[mid]` is the element lost by shifting right; `arr[mid + k]` is the element gained. If the lost one is farther from `x`, the shift is an improvement — so discard `mid` as a start.
→ [comparison-operators](../syntax/comparison-operators.md)

```python
    else:
        right = mid
```

The current window is at least as good, so **keep `mid`** as a candidate. This branch also absorbs ties, which correctly biases toward the smaller (leftward) window.
→ [elif-else](../syntax/elif-else.md)

```python
return arr[left:left + k]
```

Slice out the winning window. It's already ascending because `arr` is sorted — no re-sorting needed.
→ [list-slicing](../syntax/list-slicing.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def findClosestElements(self, arr: List[int], k: int, x: int) -> List[int]:

        left = 0
        right = len(arr) - k

        while left < right:
            mid = (left + right) // 2

            if x - arr[mid] > arr[mid + k] - x:
                left = mid + 1
            else:
                right = mid

        return arr[left:left + k]
```

</details>

**Trace it** — `arr = [1,2,3,4,5]`, `k = 4`, `x = 3`. Start range: `[0, 1]`.

| `left` | `right` | `mid` | `x - arr[mid]` | `arr[mid+k] - x` | Shift right? | Action |
|---|---|---|---|---|---|---|
| 0 | 1 | 0 | `3 - 1 = 2` | `arr[4] - 3 = 2` | `2 > 2`? **no** | `right = 0` |
| 0 | 0 | — | — | — | — | exit |

`return arr[0:4]` = **`[1,2,3,4]`** ✅

The tie at the first step is instructive: distances were equal, the condition was false, and the **left** window was kept — matching the "prefer smaller values" tie-break. With `>=` it would have shifted right and returned `[2,3,4,5]`, which is wrong.

**A second trace** — `arr = [1,1,2,3,4,5]`, `k = 4`, `x = -1`. Start range: `[0, 2]`.

| `left` | `right` | `mid` | `x - arr[mid]` | `arr[mid+k] - x` | Shift? | Action |
|---|---|---|---|---|---|---|
| 0 | 2 | 1 | `-1 - 1 = -2` | `arr[5] - (-1) = 6` | `-2 > 6`? no | `right = 1` |
| 0 | 1 | 0 | `-1 - 1 = -2` | `arr[4] - (-1) = 5` | `-2 > 5`? no | `right = 0` |
| 0 | 0 | — | — | — | — | exit |

`return arr[0:4]` = **`[1,1,2,3]`** ✅

Here `x` sits entirely to the **left** of the array. The signed comparison produced negative values on the left side and positive on the right, so the condition was never true and the window clamped to the start — exactly correct, with no special-case code.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(log(n−k) + k)</summary>

**O(log(n − k) + k).**

- The binary search runs over `n − k + 1` candidate starts → **O(log(n − k))** iterations, each O(1).
- The final slice copies `k` elements → **O(k)**.

At `n = 10⁴`, the search is ~14 iterations; the slice dominates only when `k` is large.

**Compare:**

| | Time |
|---|---|
| Sort by distance | O(n log n) |
| Heap of size `k` | O(n log k) |
| Expand from `x` | O(log n + k) |
| **Window-start search** | **O(log(n−k) + k)** |

The sort-based one-liner is genuinely tempting — `sorted(arr, key=lambda a: (abs(a-x), a))[:k]` then re-sort — and it's correct. But it's O(n log n) and throws away the sortedness you were handed, which is the same critique as in [Squares of a Sorted Array](977-squares-of-a-sorted-array.md).

**Is the O(k) slice avoidable?** Not if you must return the elements — that's output cost. If you only needed the *start index*, it would be pure O(log(n−k)).

</details>

<details>
<summary><b>5 · Space complexity</b> — O(k)</summary>

**O(k)** for the returned slice — required output, not overhead.

**O(1) auxiliary** — three integers, no allocation during the search.

Compare with the alternatives: sorting by distance needs O(n) for the sorted copy; a heap needs O(k). The window search needs nothing beyond its pointers, because it never examines candidate elements individually — it only compares the two that distinguish adjacent windows.

**The idea worth extracting:**

> **When the answer is a contiguous window, search for its *position* rather than selecting its *elements*.** That converts a selection problem into a single-value search, and collapses both time and space.

The same reframing turns [Squares of a Sorted Array](977-squares-of-a-sorted-array.md) into a merge and [Maximum Average Subarray I](643-maximum-average-subarray-i.md) into a slide — in each case, exploiting structure to avoid touching every candidate.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Because the array is sorted, the `k` closest elements must be contiguous — if the answer skipped a middle element, swapping it in for an endpoint would strictly improve the set. So the real question is where the length-`k` window starts, and I binary search over start positions from 0 to `n − k`. Comparing window `mid` against window `mid+1`, they differ only at two elements: `arr[mid]`, which I'd drop, and `arr[mid+k]`, which I'd gain. If the dropped one is farther from `x`, shifting right is better. I use the signed comparison `x - arr[mid] > arr[mid+k] - x`, which handles `x` being left of, inside, or right of the array without any absolute values or special cases. Using strict `>` means ties keep the left window, matching the tie-break rule that prefers smaller values. O(log(n−k)) for the search plus O(k) to slice the result."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why must the answer be contiguous?" | **The key insight.** Skipping a middle element means it's closer to `x` than an endpoint, so swapping improves the set. |
| "Why no `abs()`?" | The signed comparison is correct in all three positions of `x` — trace `x` left of, inside, and right of the array. |
| "Why `>` and not `>=`?" | Ties must favor the smaller value, so the false branch keeps the left window. `>=` breaks ties the wrong way. |
| "What if `arr` weren't sorted?" | Contiguity is lost. Use a max-heap of size `k` by distance — O(n log k) — then sort the result. |
| "Solve it by expanding from `x`." | Binary search `x`'s insertion point, then extend two pointers outward `k` times taking the closer side. O(log n + k), but more boundary cases. |
| "What if `k` equals `n`?" | The range is `[0, 0]`, the loop never runs, and the whole array is returned. |
| "Return the **k farthest** elements?" | No longer contiguous in general — the answer would come from both ends, so this technique doesn't apply. |

**Traps:**

- **Setting `right = len(arr) - 1`.** That allows starts whose window overruns the array. It must be `len(arr) - k`.
- **Using `abs()` in the comparison.** Not wrong per se, but it obscures why the signed form works and invites inconsistent handling of the out-of-range cases.
- **Using `>=`.** Breaks ties toward the larger values, contradicting the spec.
- **`left <= right` with `right = mid`.** Infinite loop at a one-element range.
- **Sorting by distance then slicing.** Correct, but O(n log n) and it discards the sortedness; also needs a second sort to restore ascending order.
- **Special-casing `x` outside the array.** Unnecessary — the signed comparison clamps the window automatically.

**This same move shows up in:** [Squares of a Sorted Array](977-squares-of-a-sorted-array.md) (exploiting sortedness rather than re-sorting) · [First Bad Version](278-first-bad-version.md) (the `right = mid` boundary convention) · [Find Peak Element](162-find-peak-element.md) (binary searching a *position* using a local comparison) · [Maximum Average Subarray I](643-maximum-average-subarray-i.md) (the best fixed-size window, found by sliding instead of searching).

</details>

---
