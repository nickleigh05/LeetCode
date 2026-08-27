# 75. Sort Colors

**Medium** · [LeetCode](https://leetcode.com/problems/sort-colors/) · [Solution file (no hints)](../../problems/0001-0499/75.py)

[📖 02. Two Pointers lesson](../learning/02-two-pointers.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 02. Two Pointers problems](../rmap-practice/02-two-pointers.md)

---

Given an array `nums` with `n` objects colored red, white, or blue — represented as `0`, `1`, and `2` — sort them **in-place** so that objects of the same color are adjacent, in the order red, white, blue. You must **not** use the library sort.

```
nums = [2,0,2,1,1,0]  →  [0,0,1,1,2,2]
nums = [2,0,1]        →  [0,1,2]
```

**Constraints:** `n == nums.length` · `1 <= n <= 300` · `nums[i]` is `0`, `1`, or `2`

**Follow-up:** can you solve it in **one pass** with O(1) extra space?

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| only **three** values | ⚠️ The unlock. With a tiny fixed value set, comparison sorting is overkill — you can *partition* instead |
| "**in-place**" | O(1) extra space; mutate `nums` |
| "don't use the library sort" | The point is the mechanism, not the result |
| follow-up: **one pass** | Counting sort (two passes) is the easy answer; one pass needs the three-way partition |
| `n` up to 300 | Tiny — so this is purely about technique, not performance |

The naive-but-valid answer is **counting sort**: count how many 0s, 1s, and 2s there are, then overwrite the array with that many of each. Two passes, O(n) time, O(1) space (three counters). Perfectly correct, and worth saying first.

But the follow-up asks for **one pass**, and that's the real problem. It's the classic **Dutch national flag** problem, posed by Dijkstra: partition an array into three regions using a single scan.

The idea: maintain three boundaries so the array is always divided into four zones:

```
[ 0 0 0 | 1 1 1 | ? ? ? ? | 2 2 2 ]
         ↑       ↑        ↑
        low     mid     high
```

- `nums[0 .. low-1]` — confirmed **0s**
- `nums[low .. mid-1]` — confirmed **1s**
- `nums[mid .. high]` — **unknown**, still to examine
- `nums[high+1 .. n-1]` — confirmed **2s**

`mid` scans forward. The unknown region shrinks from both ends until it's empty, and then the array is sorted.

🤔 **Before you open the next section:** if you find a `2` at position `mid` and swap it to the far end, can you safely advance `mid` afterward — and what about when you find a `0`?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Passes | Time | Space | Verdict |
|---|---|---|---|---|---|
| `nums.sort()` | Library sort | — | O(n log n) | O(1) | ❌ Explicitly forbidden |
| Counting sort | Count each value, then rewrite | **2** | O(n) | O(1) | ✅ Simple, correct, but two passes |
| Bubble/insertion | Compare-swap neighbours | many | O(n²) | O(1) | ❌ Quadratic |
| **Dutch national flag** | Three pointers, three-way partition | **1** | **O(n)** | **O(1)** | ✅✅ Answers the follow-up |

**The decision: the three-way partition (Dutch national flag).**

Three pointers, and each has a distinct meaning:

- **`low`** — the boundary where the next `0` goes. Everything left of it is `0`.
- **`mid`** — the current element under inspection.
- **`high`** — the boundary where the next `2` goes. Everything right of it is `2`.

At each step, look at `nums[mid]` and do one of three things:

| `nums[mid]` | Action | Advance |
|---|---|---|
| `0` | swap with `nums[low]` | `low += 1`, `mid += 1` |
| `1` | leave it — it's already in the right zone | `mid += 1` |
| `2` | swap with `nums[high]` | `high -= 1` **only** |

**The critical asymmetry — why `mid` advances on a `0` but not on a `2`:**

- Swapping with `low`: the element coming back from `nums[low]` is from the region **already scanned**, so it must be a `1` (0s were moved left, 2s moved right). It's already correctly placed, so `mid` can safely move on.
- Swapping with `high`: the element coming back from `nums[high]` is from the **unexamined** region. You have no idea what it is — it could be another `2`. So `mid` must **stay** and re-inspect it.

Getting this backwards is the defining bug of this problem, and understanding *why* is what makes it stick.

**Why the loop condition is `mid <= high`:** `high` points at an element that is still **unknown**, not yet confirmed as a `2`. Using `mid < high` leaves the final element unexamined, breaking inputs like `[2, 0]`.

**Why counting sort is still worth mentioning:** it's simpler, equally O(n)/O(1), and generalizes to any small fixed value set. The only thing it doesn't do is answer the one-pass follow-up. Name it, then show the partition.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
low, mid, high = 0, 0, len(nums) - 1
```

Three boundaries. `low` and `mid` both start at 0 (nothing confirmed yet, scanning from the front); `high` starts at the last index (nothing confirmed as `2` yet).
→ [multiple-return-values](../syntax/multiple-return-values.md)

```python
while mid <= high:
```

**`<=`, not `<`.** `nums[high]` is still unknown territory — it hasn't been inspected. Stopping at `mid < high` skips the last element and fails on `[2, 0]`.

The loop ends when `mid` passes `high`, meaning the unknown region is empty.
→ [while-loop](../syntax/while-loop.md)

```python
    if nums[mid] == 0:
        nums[low], nums[mid] = nums[mid], nums[low]
        low += 1
        mid += 1
```

**A `0` belongs in the left region.** Swap it to `low` and advance both pointers.

Safe to advance `mid` because whatever came back from `nums[low]` is from the already-scanned zone — necessarily a `1` (or the same `0`, when `low == mid`). Either way it's correctly placed.
→ [swap-tuple-assign](../syntax/swap-tuple-assign.md)

```python
    elif nums[mid] == 1:
        mid += 1
```

**A `1` is already home.** The middle region is exactly where 1s belong, so just move on. No swap, no boundary change.

```python
    else:
        nums[mid], nums[high] = nums[high], nums[mid]
        high -= 1
```

**A `2` belongs in the right region.** Swap it to `high` and shrink that boundary.

**`mid` does not advance** — this is the line that matters. The element swapped in from `nums[high]` has never been examined. It could be a `0`, a `1`, or another `2`, and the next loop iteration must inspect it.
→ [elif-else](../syntax/elif-else.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        low, mid, high = 0, 0, len(nums) - 1

        while mid <= high:
            if nums[mid] == 0:
                nums[low], nums[mid] = nums[mid], nums[low]
                low += 1
                mid += 1
            elif nums[mid] == 1:
                mid += 1
            else:
                nums[mid], nums[high] = nums[high], nums[mid]
                high -= 1
```

</details>

**Trace it** — `nums = [2, 0, 2, 1, 1, 0]`:

| `low` | `mid` | `high` | `nums` | `nums[mid]` | Action |
|---|---|---|---|---|---|
| 0 | 0 | 5 | `[2,0,2,1,1,0]` | **2** | swap mid↔high, `high→4` (mid stays!) |
| 0 | 0 | 4 | `[0,0,2,1,1,2]` | **0** | swap mid↔low, `low→1`, `mid→1` |
| 1 | 1 | 4 | `[0,0,2,1,1,2]` | **0** | swap mid↔low (self), `low→2`, `mid→2` |
| 2 | 2 | 4 | `[0,0,2,1,1,2]` | **2** | swap mid↔high, `high→3` (mid stays!) |
| 2 | 2 | 3 | `[0,0,1,1,2,2]` | **1** | `mid→3` |
| 2 | 3 | 3 | `[0,0,1,1,2,2]` | **1** | `mid→4` |
| 2 | 4 | 3 | — | — | `mid > high` → **stop** |

Result `[0,0,1,1,2,2]` ✅

Rows 1 and 4 are the crucial ones: `mid` held still after each `2`-swap, and in row 2 the newly-arrived `0` was correctly re-inspected. Had `mid` advanced, that `0` would have been stranded in the middle region.

Row 7 shows why `mid <= high` matters — the loop only stopped once `mid` genuinely passed `high`.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n), one pass.**

Every iteration shrinks the unknown region `[mid, high]` by exactly one, either by advancing `mid` or retreating `high`. The region starts with `n` elements, so there are at most `n` iterations, each doing O(1) work.

**Note the subtlety:** on a `2`-swap, `mid` doesn't move — but `high` does, so the unknown region still shrinks. That's what guarantees termination despite `mid` occasionally stalling. Being able to point at the decreasing quantity is the clean way to argue this.

**Compare:**

| | Passes | Time |
|---|---|---|
| Counting sort | 2 | O(n) |
| **Dutch flag** | **1** | O(n) |
| Library sort | — | O(n log n) |

Both linear options beat a comparison sort, because with only three distinct values you're **partitioning**, not comparing — the same reason [counting sort](../algorithms/counting-sort.md) escapes the `n log n` lower bound.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).** Three integer pointers, regardless of `n`.

Counting sort is also O(1) here — three counters — but only because the value set is fixed at three. In general, counting sort is O(k) for `k` distinct values, so it degrades if the alphabet grows. The three-way partition stays O(1) no matter what, since it never stores counts at all.

| | Space | Passes | Generalizes to k values? |
|---|---|---|---|
| Counting sort | O(k) | 2 | ✅ easily |
| **Dutch flag** | **O(1)** | **1** | ⚠️ only to 3 regions |

**The transferable idea:** the three-way partition is the core of **3-way quicksort**, which is what makes quicksort efficient on arrays with many duplicate keys. Standard 2-way partitioning degrades to O(n²) when most elements equal the pivot; partitioning into `< pivot`, `== pivot`, `> pivot` handles duplicates in one pass. Recognizing this problem as "the partition step of quicksort, standalone" is what makes it memorable.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "With only three values I don't need a comparison sort — I can partition. The simple answer is counting sort: count 0s, 1s, and 2s, then overwrite. Two passes, O(n) time, O(1) space. For the one-pass follow-up it's the Dutch national flag partition: three pointers, `low` for where the next 0 goes, `high` for where the next 2 goes, and `mid` scanning. On a 0 I swap with `low` and advance both; on a 1 I just advance `mid`; on a 2 I swap with `high` and **don't** advance `mid` — because the element coming back from `high` hasn't been examined yet, whereas the one coming back from `low` is already-scanned and must be a 1. The loop runs while `mid <= high`, since `high` is still unknown territory. O(n) one pass, O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "One pass, O(1) space?" | **The stated follow-up.** Dutch national flag, as above. |
| "Why doesn't `mid` advance on a 2?" | **The key question.** The element from `high` is unexamined; the one from `low` is already-scanned and known to be a 1. |
| "Why `mid <= high` and not `<`?" | `nums[high]` is still unknown. `[2,0]` fails with `<`. |
| "Sort `k` colors instead of 3." | Counting sort — O(n + k) time, O(k) space. The three-way partition doesn't generalize cleanly beyond three regions. |
| "Where else does this appear?" | The partition step of **3-way quicksort**, which handles duplicate-heavy arrays in O(n log n) instead of degrading to O(n²). |
| "What if you could only swap adjacent elements?" | Then it's bubble-sort-like — O(n²) lower bound, since each swap fixes at most one inversion. |
| "Is it stable?" | No — swapping across the array reorders equal elements. Counting sort can be made stable; this can't. |

**Traps:**

- **Advancing `mid` after a `2`-swap.** *The* bug. The unexamined element from `high` gets skipped, stranding 0s and 2s in the middle. Trace `[2,0]` to see it immediately.
- **Using `mid < high`.** Leaves the last element uninspected. `[2,0]` again.
- **Advancing `low` without advancing `mid`** on a `0`. Since `low <= mid` always, this desynchronizes the boundaries and can loop forever.
- **Calling `nums.sort()`.** Explicitly forbidden, and it dodges the entire exercise.
- **Returning the array.** The signature returns `None` — mutate in place.
- **Trying to handle 1s with a swap.** They're already in the correct region; swapping them does nothing but risk breaking an invariant.

**This same move shows up in:** [Move Zeroes](283-move-zeroes.md) (two-region in-place partition, order preserved) · [Remove Element](27-remove-element.md) (the "swap with the far end" trick when order is free) · [Merge Sorted Array](88-merge-sorted-array.md) (pointer invariants that make in-place writing safe) · [H-Index](274-h-index.md) (counting sort exploiting a small bounded value range).

</details>

---
