# 34. Find First and Last Position of Element in Sorted Array

**Medium** · [LeetCode](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/) · [Solution file (no hints)](../../problems/0001-0499/34.py)

[📖 05. Binary Search lesson](../learning/05-binary-search.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 05. Binary Search problems](../rmap-practice/05-binary-search.md)

---

Given an array of integers `nums` sorted in **non-decreasing** order, find the starting and ending position of a given `target`. If the target is not found, return `[-1, -1]`. You must write an algorithm with **O(log n)** runtime.

```
nums = [5,7,7,8,8,10], target = 8  →  [3, 4]
nums = [5,7,7,8,8,10], target = 6  →  [-1, -1]
nums = [],             target = 0  →  [-1, -1]
```

**Constraints:** `0 <= nums.length <= 10⁵` · `-10⁹ <= nums[i] <= 10⁹` · `nums` sorted non-decreasing · `-10⁹ <= target <= 10⁹`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**non-decreasing**" | ⚠️ Sorted **with duplicates allowed** — that's the whole problem. Equal values form a contiguous block |
| "**starting and ending** position" | Two boundaries of that block: the leftmost and rightmost occurrences |
| "**O(log n)**" | Rules out finding one occurrence then scanning outward — a block of 10⁵ equal values would make that O(n) |
| "`[-1,-1]` if not found" | Both searches must agree on absence |
| `nums.length` can be **0** | Empty input must return `[-1,-1]`, not crash |

**Why the obvious approach fails the complexity bar.** A plain binary search finds *some* occurrence in O(log n) — but which one is arbitrary. Expanding left and right from there to find the block's edges is O(k) where `k` is the block size, and `k` can be the entire array (`[8,8,8,…,8]`). That's O(n) worst case, violating the requirement.

**The fix: run two separate binary searches**, each biased toward a different edge.

```
nums  = [5, 7, 7, 8, 8, 10]     target = 8
index:  0  1  2  3  4  5
                    ↑  ↑
                first  last
```

- **Leftmost search:** on finding the target, don't stop — keep searching *left* for an earlier occurrence.
- **Rightmost search:** on finding the target, keep searching *right*.

Each is O(log n), so the total is still O(log n).

**The key mental shift:** with duplicates, "found it" is no longer a stopping condition. It's a *candidate* — record it and keep narrowing toward the edge you want. That's what turns an exact-match search into a boundary search.

🤔 **Before you open the next section:** if you find the target at index `mid` but want the *first* occurrence, which half of the range should you continue searching — and does `mid` stay in it?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Linear scan | Walk once, record first and last | O(n) | ❌ Violates O(log n) |
| Binary search + expand | Find any occurrence, walk outward | O(log n + k) → **O(n)** | ❌ Fails on large duplicate blocks |
| **Two biased binary searches** | One leftmost, one rightmost | **O(log n)** | ✅ |
| `bisect_left` / `bisect_right` | Standard library | O(log n) | ⚠️ Correct; write the loop in an interview |

**The decision: two binary searches, each biased toward one edge.**

The structure of each is identical except for one branch:

| | On `nums[mid] == target` | Effect |
|---|---|---|
| **Leftmost** | `right = mid - 1` (keep looking left) | converges to the first occurrence |
| **Rightmost** | `left = mid + 1` (keep looking right) | converges to the last occurrence |

In both, you **record `mid` as a candidate** before continuing, so the last recorded value when the loop ends is the edge you wanted.

**Why recording is essential.** Since you never return early on a match, the loop always runs to exhaustion. Without saving each hit, you'd finish with no idea where the target was. The recorded variable ratchets toward the correct edge — each new find is closer to the target edge than the last.

**Why not use the `left < right` / `right = mid` convention here?** You could — that's the classic `bisect_left` formulation. But it requires a post-loop check (`nums[left] == target`?) and careful handling of the empty-array and target-absent cases. The "record a candidate, use `<=` and `mid ± 1`" version:

- uses the **same convention for both searches**, so the two functions are near-identical,
- returns `-1` naturally when nothing was ever recorded,
- needs no post-loop validation.

Consistency across the two searches is worth a lot when you're writing this under time pressure.

**Why a shared helper.** The two searches differ by a single boolean, so factoring them into one parameterized function halves the code and eliminates the risk of the two drifting apart. That's a genuine design point, not just tidiness.

**The library equivalent**, worth naming: `bisect_left(nums, target)` gives the first index where the target could be inserted, and `bisect_right(nums, target) - 1` gives the last occurrence. Guard with a membership check. Fine to mention; write the loop.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
def searchRange(self, nums: List[int], target: int) -> List[int]:
    first = self.findBound(nums, target, True)
    if first == -1:
        return [-1, -1]
    last = self.findBound(nums, target, False)
    return [first, last]
```

Two calls to one helper. The **early exit** when `first == -1` is a small but real optimization — if the target isn't present at all, the second search is guaranteed to fail too, so skip it.
→ [function-basics](../syntax/function-basics.md)

---

**The shared helper**

```python
def findBound(self, nums, target, findFirst):
    left = 0
    right = len(nums) - 1
    bound = -1
```

`bound` starts at `-1`, which doubles as the "never found" answer — so the not-found case needs no special handling.

For an empty array, `right = -1`, the loop never runs, and `-1` is returned correctly.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
    while left <= right:
        mid = left + (right - left) // 2
```

Inclusive bounds ⇒ `<=`. Overflow-safe midpoint, as in [Valid Perfect Square](367-valid-perfect-square.md).
→ [while-loop](../syntax/while-loop.md) · [integer-division-modulo](../syntax/integer-division-modulo.md)

```python
        if nums[mid] == target:
            bound = mid
            if findFirst:
                right = mid - 1
            else:
                left = mid + 1
```

**The heart of it — and the only place the two searches differ.**

Record `mid` as the best candidate so far, then **keep searching** toward the desired edge:

- `findFirst` ⇒ narrow to the **left half**, hunting for an earlier occurrence
- otherwise ⇒ narrow to the **right half**, hunting for a later one

Crucially, we do **not** return here. With duplicates, a match is a candidate, not an answer.
→ [if-return](../syntax/if-return.md) · [boolean-basics](../syntax/boolean-basics.md)

```python
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
```

Ordinary binary-search narrowing when `mid` isn't the target.
→ [elif-else](../syntax/elif-else.md)

```python
    return bound
```

The last recorded candidate — which, by the biasing above, is the first or last occurrence.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:

        first = self.findBound(nums, target, True)
        if first == -1:
            return [-1, -1]

        last = self.findBound(nums, target, False)
        return [first, last]

    def findBound(self, nums: List[int], target: int, findFirst: bool) -> int:

        left = 0
        right = len(nums) - 1
        bound = -1

        while left <= right:
            mid = left + (right - left) // 2

            if nums[mid] == target:
                bound = mid
                if findFirst:
                    right = mid - 1
                else:
                    left = mid + 1
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

        return bound
```

</details>

**Trace the leftmost search** — `nums = [5,7,7,8,8,10]`, `target = 8`, `findFirst = True`:

| `left` | `right` | `mid` | `nums[mid]` | Action | `bound` |
|---|---|---|---|---|---|
| 0 | 5 | 2 | 7 | `7 < 8` → `left = 3` | −1 |
| 3 | 5 | 4 | **8** | record; go **left** → `right = 3` | **4** |
| 3 | 3 | 3 | **8** | record; go **left** → `right = 2` | **3** ⭐ |
| 3 | 2 | — | — | `left > right` → exit | 3 |

Returns **3** ✅ — the starred row shows `bound` ratcheting from 4 down to 3 as an earlier occurrence was found.

**Trace the rightmost search** — same input, `findFirst = False`:

| `left` | `right` | `mid` | `nums[mid]` | Action | `bound` |
|---|---|---|---|---|---|
| 0 | 5 | 2 | 7 | `7 < 8` → `left = 3` | −1 |
| 3 | 5 | 4 | **8** | record; go **right** → `left = 5` | **4** ⭐ |
| 5 | 5 | 5 | 10 | `10 > 8` → `right = 4` | 4 |
| 5 | 4 | — | — | exit | 4 |

Returns **4** ✅

Final answer **`[3, 4]`** ✅

**And the not-found case** — `target = 6`:

| `left` | `right` | `mid` | `nums[mid]` | Action |
|---|---|---|---|---|
| 0 | 5 | 2 | 7 | `7 > 6` → `right = 1` |
| 0 | 1 | 0 | 5 | `5 < 6` → `left = 1` |
| 1 | 1 | 1 | 7 | `7 > 6` → `right = 0` |
| 1 | 0 | — | — | exit |

`bound` was never set → returns `-1` → **`[-1, -1]`** ✅, and the second search is skipped entirely.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(log n)</summary>

**O(log n).**

Each `findBound` call halves the range every iteration, so each is O(log n). Two calls give `2 · log n` = **O(log n)**.

At `n = 10⁵` that's about **17 iterations per search**, 34 total.

**Why the naive "find then expand" fails.** Finding one occurrence is O(log n), but walking outward to the block's edges costs O(k) where `k` is the number of duplicates. On `[8] * 10⁵` with `target = 8`, that's 10⁵ steps — **O(n)**, violating the stated bound. The whole point of the two biased searches is that they reach the edges *without* traversing the block.

**Why the early exit matters in practice.** When the target is absent, only one search runs — halving the work on the common miss case. It doesn't change the asymptotics, but it's free and shows attention to detail.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — a few integers per call, and the two calls happen sequentially rather than nested, so nothing accumulates.

The output list is O(1) — exactly two elements, regardless of how many duplicates exist. That's worth noticing: you're returning the *bounds* of the block, not the block itself, so a run of 10⁵ equal values costs nothing extra to report.

An iterative loop keeps the stack flat; a recursive binary search would add O(log n) frames for no benefit.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The array can contain duplicates, so equal values form a contiguous block and I need both its edges. A plain binary search finds an arbitrary occurrence, and expanding outward from it would be O(k) — up to O(n) if the whole array is the target — so that fails the O(log n) requirement. Instead I run **two** binary searches. Both are standard, except that when I hit the target I don't return: I record the index as a candidate and keep narrowing toward the edge I want — left for the first occurrence, right for the last. The last recorded candidate is the answer, and if nothing was ever recorded I return −1, which handles both the not-found and empty-array cases. I factor the two into one helper with a boolean flag so they can't drift apart, and I skip the second search if the first found nothing. O(log n) time, O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why not find one occurrence and expand?" | **The key question.** O(k) expansion is O(n) when the array is all duplicates. Two biased searches avoid touching the block. |
| "**Count** the occurrences instead." | `last - first + 1`, or `bisect_right - bisect_left`. Same searches. |
| "Use the standard library." | `bisect_left(nums, target)` and `bisect_right(nums, target) - 1`, guarded by a presence check. |
| "Handle the empty array." | Falls out: `right = -1`, the loop never runs, `bound` stays `-1`. |
| "Do it with one search?" | Find `bisect_left(target)` and `bisect_left(target + 1) - 1` — still two searches, but expressible with one helper for integer inputs. |
| "Why `<=` and `mid ± 1` rather than `right = mid`?" | Both work. This convention keeps the two searches identical apart from one branch and needs no post-loop validation. |
| "Search a rotated sorted array with duplicates?" | Much harder — worst case degrades to O(n), since duplicates can destroy the pivot-detection logic. |

**Traps:**

- **Returning immediately on a match.** With duplicates that gives an arbitrary index, not an edge. This is *the* bug.
- **Forgetting to record `bound` before narrowing.** The loop runs to exhaustion, so without recording you lose the answer entirely.
- **Biasing both searches the same way.** Both then return the same edge; the second flag must actually flip the branch.
- **Not handling the empty array.** `right = len(nums) - 1 = -1` handles it — but only if you don't index `nums` before the loop.
- **Expanding linearly from a found index.** Correct but O(n) on duplicate-heavy input.
- **Mixing conventions between the two helpers.** Keep them one function with a flag.

**This same move shows up in:** [Search Insert Position](35-search-insert-position.md) (the same value-search convention, returning `left` on a miss) · [First Bad Version](278-first-bad-version.md) (boundary search via the `right = mid` convention, for contrast) · [Find Minimum in Rotated Sorted Array](153-find-minimum-in-rotated-sorted-array.md) (boundary search on a transformed predicate) · [Single Element in a Sorted Array](540-single-element-in-a-sorted-array.md) (binary search over a pairing invariant rather than values).

</details>

---
