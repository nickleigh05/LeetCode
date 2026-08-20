# 34. Find First and Last Position of Element in Sorted Array

**Medium** · [LeetCode](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/) · [Solution file (no hints)](../../problems/0001-0499/34.py)

[📖 06. Binary Search lesson](../learning/06-binary-search.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 06. Binary Search problems](../rmap-practice/06-binary-search.md)

---

Given `nums` sorted in **non-decreasing** order, return the starting and ending index of `target`. If it isn't there, return `[-1, -1]`.

You must write an algorithm with **O(log n)** runtime.

```
nums = [5,7,7,8,8,10], target = 8   →  [3,4]
nums = [5,7,7,8,8,10], target = 6   →  [-1,-1]
nums = [],             target = 0   →  [-1,-1]
```

**Constraints:** `0 <= nums.length <= 10⁵` · `-10⁹ <= nums[i] <= 10⁹` · `nums` is non-decreasing · `-10⁹ <= target <= 10⁹`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "sorted in **non-decreasing** order" | Not *increasing*. **Duplicates are expected** — the whole problem exists because of them |
| "the **starting and ending** position" | A range, so there may be many matches. Plain [binary search](704-binary-search.md) returns *an* index, not the first or last |
| "**O(log n)** runtime" | Stated as a requirement, not a follow-up. Any linear step anywhere kills the solution |
| `[-1, -1]` when absent | A miss is a normal outcome, not an edge case bolted on |
| `nums.length` can be `0` | Empty array must work — `right = len(nums) - 1` starts at `-1` and the loop simply never runs |
| `0 <= nums.length <= 10⁵` | log₂(10⁵) ≈ 17 steps. A linear scan is 10⁵ — see [constraints-cheatsheet](../guides/constraints-cheatsheet.md) |

Here's the trap. Find a match with ordinary binary search, then walk left and right to the edges of the run — that *feels* O(log n). It isn't. On `nums = [8,8,8,...,8]` with `target = 8`, the run is the entire array and you walk all of it: **O(n)**. The stated requirement rules that out.

🤔 **Before you open the next section:** ordinary binary search stops the moment `nums[mid] == target`. What if a match were treated not as an answer, but as *evidence that the answer is here or further left*?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Linear scan | Walk once, record first and last match | O(n) | O(1) | ❌ Violates the stated O(log n) |
| Binary search, then expand | Find any match, then walk out to both edges | O(n) worst | O(1) | ❌ All-equal array degrades to a full scan |
| Two boundary searches | Binary search twice: once biased left, once biased right | **O(log n)** | O(1) | ✅ |
| `bisect_left` / `bisect_right` | The same two searches, from the standard library | O(log n) | O(1) | ✅ The production answer |

**The decision: run binary search twice, and don't stop on a match.**

The change from [704](704-binary-search.md) is one line of behaviour. Ordinary binary search returns as soon as `nums[mid] == target`. Here, a match is not the end of the search — it's a **candidate**. Record it, then keep shrinking in the direction of the boundary you want:

- Hunting the **first** occurrence: after a match, everything at or right of `mid` is now irrelevant. Move `right = mid - 1` and look further left.
- Hunting the **last** occurrence: move `left = mid + 1` and look further right.

Each search still halves the space every step, so each is O(log n) and two of them is O(log n). The last recorded candidate is the boundary, because the search only ever moved *toward* it.

**Why not expand outward?** It's the intuitive fix and it's the one that gets rejected. Worth saying out loud — "I could find any occurrence and expand, but with all elements equal that's O(n), and the problem asks for O(log n)" — because naming the trap you avoided is worth as much as the solution.

**The general move:** this is **binary search on a boundary** rather than on a value — finding the edge of a region where a predicate flips from false to true. Same shape as [Find Minimum in Rotated Sorted Array](153-find-minimum-in-rotated-sorted-array.md) and [Koko Eating Bananas](875-koko-eating-bananas.md); once you see it, the "first/last index of X" family is one template.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
def bound(first: bool) -> int:
```

One helper, a flag for which edge. The two searches are identical except for which way they lean after a match — writing them twice invites the copy-paste bug where you flip one line and not the other.
→ [function-basics](../syntax/function-basics.md) · [closures](../syntax/closures.md) · [boolean-basics](../syntax/boolean-basics.md)

```python
    left = 0
    right = len(nums) - 1
    found = -1
```

The standard inclusive range `[left, right]`, plus `found` — the last index where we saw the target. Seeding it to `-1` means "never seen", which is also exactly the value the problem wants returned on a miss. No special-casing needed.

On an empty array `right = -1`, the loop condition fails immediately, and `found` stays `-1`. The edge case handles itself.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
    while left <= right:
        mid = left + (right - left) // 2
```

`<=` because the range is inclusive — a single remaining element still has to be examined. `left + (right - left) // 2` is the overflow-safe midpoint; in Python integers are unbounded so `(left + right) // 2` is equally fine, but the habit costs nothing and matters in C++/Java.
→ [while-loop](../syntax/while-loop.md) · [integer-division-modulo](../syntax/integer-division-modulo.md)

```python
        if nums[mid] == target:
            found = mid
            if first:
                right = mid - 1
            else:
                left = mid + 1
```

**The line that makes this problem different from [704](704-binary-search.md).** A match doesn't return — it updates `found` and keeps going, toward the edge we're after. Since every subsequent match must be further in that direction, the *last* value written to `found` is the boundary.
→ [elif-else](../syntax/elif-else.md)

```python
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return found
```

The ordinary halving for non-matches, unchanged from plain binary search. `mid ± 1` rather than plain `mid` — `mid` has been examined, so leaving it in the range means a loop that never terminates.

```python
return [bound(True), bound(False)]
```

Two searches, two boundaries. If the target is absent, both return `-1` and the answer is `[-1, -1]` with no extra check.
→ [multiple-return-values](../syntax/multiple-return-values.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:

        def bound(first: bool) -> int:

            left = 0
            right = len(nums) - 1
            found = -1

            while left <= right:

                mid = left + (right - left) // 2

                if nums[mid] == target:
                    found = mid
                    if first:
                        right = mid - 1
                    else:
                        left = mid + 1
                elif nums[mid] < target:
                    left = mid + 1
                else:
                    right = mid - 1

            return found

        return [bound(True), bound(False)]
```

</details>

**Trace the first-occurrence search** — `nums = [5,7,7,8,8,10]`, `target = 8`:

| `left` | `right` | `mid` | `nums[mid]` | `found` | Action |
|---|---|---|---|---|---|
| 0 | 5 | 2 | 7 | −1 | `7 < 8` → `left = 3` |
| 3 | 5 | 4 | 8 | **4** | match → search left, `right = 3` |
| 3 | 3 | 3 | 8 | **3** | match → search left, `right = 2` |
| 3 | 2 | — | — | 3 | `left > right`, return **3** |

**And the last-occurrence search:**

| `left` | `right` | `mid` | `nums[mid]` | `found` | Action |
|---|---|---|---|---|---|
| 0 | 5 | 2 | 7 | −1 | `7 < 8` → `left = 3` |
| 3 | 5 | 4 | 8 | **4** | match → search right, `left = 5` |
| 5 | 5 | 5 | 10 | 4 | `10 > 8` → `right = 4` |
| 5 | 4 | — | — | 4 | `left > right`, return **4** |

Answer: `[3, 4]`. ✅

**A miss** — `target = 6`: no `nums[mid]` ever equals 6, `found` is never assigned, both searches return `-1` → `[-1, -1]`. ✅

</details>

<details>
<summary><b>4 · Time complexity</b> — O(log n)</summary>

**O(log n).**

- Each search halves `[left, right]` every iteration — including on a match, because `right = mid - 1` or `left = mid + 1` shrinks the range rather than leaving it alone. **This is the crux:** a match that didn't shrink the range would loop forever.
- One search is therefore O(log n) — about 17 iterations at n = 10⁵.
- Two searches: 2 · O(log n) = **O(log n)**. Constant factors don't change the class.

**Compare to the expand-outward version:** identical on random data, but O(n) on `[8,8,8,…,8]` — 10⁵ steps instead of 34. That's the input an interviewer reaches for.

**Best case O(1):** unreachable, and worth knowing why. Even if `mid` hits the target on the first probe, the search keeps going to prove there's nothing further out. It's always the full log n.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).**

Three integers per search, and the two searches run one after the other rather than nested — so the peak is constant regardless of `n`. Nothing is allocated; `nums` is only read.

**The recursive version is O(log n) space,** because each halving adds a stack frame and the depth is the number of halvings. Same time, worse space, for no gain — the iterative form is strictly better here, and the reason is the same one covered in [Recursion](../learning/05-recursion.md): call-stack depth *is* memory.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Plain binary search finds *an* occurrence, but with duplicates I need the two edges of the run. Finding one match and expanding outward is O(n) when the whole array is the target, and the problem demands O(log n) — so instead I'll run binary search twice and change what a match means. Rather than returning on `nums[mid] == target`, I record `mid` as a candidate and keep searching *left* for the first occurrence, or *right* for the last. Every step still halves the range, so each search is O(log n). If the target never appears, my candidate stays at its `-1` seed, which is the answer the problem wants anyway. O(log n) time, O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "How would you write this in production?" | [`bisect_left`](../syntax/bisect-module.md) and `bisect_right`. `lo = bisect_left(nums, target)`; if `lo == len(nums)` or `nums[lo] != target` return `[-1, -1]`; else `[lo, bisect_right(nums, target) - 1]`. Same complexity, no boundary bugs — reach for it *after* showing you can write the loop. |
| "Count the occurrences?" | `last - first + 1`, or straight from the library: `bisect_right(nums, t) - bisect_left(nums, t)` — which is 0 for an absent target, no branch needed. |
| "Do it in a single pass?" | Find the first occurrence, then binary search for the last *within* `[first, n-1]`. Fewer steps, same O(log n). Not worth the complexity. |
| "What if the array were rotated?" | Locate the pivot first, then boundary-search the correct half. See [Search in Rotated Sorted Array](33-search-in-rotated-sorted-array.md). |
| "Insert position if it's missing?" | That's `bisect_left`'s return value with no equality check — the classic "search insert position" variant. |

**Traps:**

- **Returning on a match.** The habit from [704](704-binary-search.md), and it gives you a random index inside the run.
- **Expanding outward from a match.** Correct, and O(n) on the all-equal input.
- **Not shrinking the range on a match.** Setting `right = mid` instead of `mid - 1` in the first-occurrence branch is an infinite loop when `left == right == mid`.
- **Mixing up the directions.** First occurrence searches *left* after a match — it's easy to write it backwards. Trace `[8,8]` by hand: first should give 0, last should give 1.
- **Special-casing the empty array.** Unnecessary. `right = -1` makes the loop body unreachable and `found` is already `-1`.

**This same move shows up in:** [Binary Search](704-binary-search.md) (the base loop this modifies) · [Find Minimum in Rotated Sorted Array](153-find-minimum-in-rotated-sorted-array.md) (binary search for a boundary, not a value) · [Koko Eating Bananas](875-koko-eating-bananas.md) (first value in a range that satisfies a predicate) · [Time Based Key-Value Store](981-time-based-key-value-store.md) (last entry at or before a timestamp — `bisect_right` in disguise).

</details>

---
