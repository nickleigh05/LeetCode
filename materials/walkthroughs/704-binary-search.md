# 704. Binary Search

**Easy** · [LeetCode](https://leetcode.com/problems/binary-search/) · [Solution file (no hints)](../../problems/0500-0999/704.py)

[📖 05. Binary Search lesson](../learning/05-binary-search.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 05. Binary Search problems](../rmap-practice/05-binary-search.md)

---

Given an array `nums` sorted in **ascending order** with **distinct** values, and a `target`, return the index of `target` if it exists, otherwise `-1`.

You must write an algorithm with **O(log n)** runtime complexity.

```
nums = [-1,0,3,5,9,12], target = 9   →  4
nums = [-1,0,3,5,9,12], target = 2   →  -1
```

**Constraints:** `1 <= nums.length <= 10⁴` · `-10⁴ < nums[i], target < 10⁴` · all values **distinct**, sorted ascending

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

This is the **template problem** for the entire unit. Everything that follows is a variation on the machinery you build here, so it's worth learning precisely rather than approximately.

| The statement says | Which really means |
|---|---|
| "sorted in **ascending order**" | ⚠️ The precondition. Sortedness means one comparison tells you which *side* the target must be on |
| "**distinct** values" | No duplicates, so no "find the first/last occurrence" complications |
| "**O(log n)** runtime" | Explicitly rules out the linear scan. Halving is the only way to get log n |
| "return the **index**" | Not a boolean — you need the position |
| "`-1` if absent" | A defined not-found result |

The core idea in one sentence: **maintain a range that must contain the target if it exists anywhere, and shrink it by half every step.**

Look at the middle element:
- Equal to the target → found it.
- **Less** than the target → everything from the middle leftward is also less (it's sorted), so the target can only be to the **right**. Discard the left half *and* the middle.
- **Greater** → symmetrically, discard the right half and the middle.

Each comparison eliminates half the remaining candidates, which is why n → log₂ n. At n = 10⁴, that's at most **14 comparisons**.

🤔 **Before you open the next section:** the tricky part isn't the idea, it's the boundaries. When the range has shrunk to a single element, has it been checked yet? And when the target is absent, what makes the loop stop?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Linear scan | Check every element | O(n) | ❌ Violates the stated O(log n) |
| Hash map of value→index | Build a dict, look up | O(n) build, O(1) query | ❌ O(n) to build, O(n) space — and it throws away the sortedness |
| `bisect` module | Python's built-in binary search | O(log n) | ⚠️ Correct and idiomatic, but the point is to write it |
| **Binary search** | Halve the range each comparison | **O(log n)** | ✅ |

**The decision: classic binary search on an inclusive range `[left, right]`.**

The whole problem is getting three details right — and they're the details that decide whether *every* problem in this unit works:

**1. The loop condition: `while left <= right`.**

With an **inclusive** range, `left == right` still describes one unchecked element. Stopping at `<` would skip it, and single-element arrays would fail. The loop ends when `left > right`, i.e. the range is genuinely empty.

**2. The midpoint: `mid = (left + right) // 2`.**

Floor division, so `mid` biases toward `left`. That matters for termination in the two-element case.

*(In languages with fixed-width ints, `left + right` can overflow, so the idiom is `left + (right - left) // 2`. Python's ints are arbitrary-precision, so it's a non-issue here — but it's a classic interview question and worth being able to explain.)*

**3. The updates: `mid + 1` and `mid - 1`, never plain `mid`.**

You just *checked* `mid` and it wasn't the target, so it must be excluded. Writing `left = mid` creates an infinite loop the moment the range is two elements — `mid` floors to `left`, so `left` never advances.

**These three together are the invariant:** *if the target exists, it is inside `[left, right]`*. Every update preserves that, which is why the search is correct rather than merely plausible.

**Why not `bisect`?** [`bisect_left`](../syntax/bisect-module.md) is the right production answer and worth mentioning. But binary search is asked precisely to see whether you can write the boundaries correctly — famously, most programmers can't on the first try.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
left = 0
right = len(nums) - 1
```

The initial range: the **entire array**, inclusive at both ends. `len(nums) - 1` — not `len(nums)` — because `right` is a valid index we intend to check.

This choice of an inclusive range is what dictates the `<=` and the `±1` below. Mixing conventions is the number one source of binary-search bugs.
→ [variables-assignment](../syntax/variables-assignment.md) · [list-basics](../syntax/list-basics.md)

```python
while left <= right:
```

Continue while the range still holds at least one unchecked element. **`<=`, not `<`** — when `left == right` there's exactly one element left and it hasn't been examined yet.

Test it mentally on `nums = [5]`, `target = 5`: `left = right = 0`. With `<` the loop never runs and you'd return `-1`.
→ [while-loop](../syntax/while-loop.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
    mid = (left + right) // 2
```

The midpoint, floored. For `left=0, right=1` this gives `mid=0` — biased left, which combined with `left = mid + 1` guarantees progress.
→ [integer-division-modulo](../syntax/integer-division-modulo.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
    if nums[mid] == target:
        return mid
```

Found. Since values are distinct, there's exactly one match and no need to keep looking.
→ [if-return](../syntax/if-return.md)

```python
    elif nums[mid] < target:
        left = mid + 1
```

The middle is **too small**. Because the array is sorted, everything at or left of `mid` is also too small — so discard all of it. `mid + 1` excludes the already-checked midpoint.
→ [elif-else](../syntax/elif-else.md)

```python
    else:
        right = mid - 1
```

The middle is **too large**. Discard `mid` and everything to its right.

```python
return -1
```

The loop exited, meaning `left > right` — the range is empty. Every element was eliminated, so the target isn't present.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def search(self, nums: List[int], target: int) -> int:

        left = 0
        right = len(nums) - 1

        while left <= right:
            mid = (left + right) // 2

            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1
```

</details>

**Trace it** — `nums = [-1,0,3,5,9,12]`, `target = 9`:

| `left` | `right` | `mid` | `nums[mid]` | vs 9 | Action |
|---|---|---|---|---|---|
| 0 | 5 | 2 | 3 | too small | `left = 3` |
| 3 | 5 | 4 | **9** | **match** | `return 4` ✅ |

**And a miss** — `target = 2`:

| `left` | `right` | `mid` | `nums[mid]` | vs 2 | Action |
|---|---|---|---|---|---|
| 0 | 5 | 2 | 3 | too big | `right = 1` |
| 0 | 1 | 0 | −1 | too small | `left = 1` |
| 1 | 1 | 1 | 0 | too small | `left = 2` |
| 2 | 1 | — | — | `left > right` | exit → `return -1` ✅ |

Row 3 is the one to study: the range narrowed to a single element, `<=` let it be checked, and then `left` overtook `right` to end the loop. All three boundary rules doing their job.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(log n)</summary>

**O(log n).**

Each iteration eliminates **half** the remaining range. Starting at n elements: n → n/2 → n/4 → … → 1. The number of halvings to reach 1 is log₂ n.

| n | Comparisons (worst case) |
|---|---|
| 10 | 4 |
| 1,000 | 10 |
| **10,000** | **14** |
| 1,000,000 | 20 |
| 1,000,000,000 | 30 |

That table is the reason binary search matters: a **billion** elements in 30 comparisons. The growth is so slow that the difference between a thousand and a billion is only 20 extra steps.

**Best case O(1):** the target is at the initial midpoint.

**The precondition is the cost.** If the array weren't sorted, you'd pay O(n log n) to sort it first — at which point a single lookup is worse than an O(n) scan. Binary search pays off when you search a sorted structure **repeatedly**, or when it arrives sorted for free. That's the trade to state out loud.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).**

Three integers — `left`, `right`, `mid`. The array is only read; nothing is copied or built.

**The recursive version is O(log n) space**, because each recursive call adds a stack frame and the depth is the number of halvings:

```python
def search(nums, target, left, right):
    if left > right:
        return -1
    mid = (left + right) // 2
    ...
```

It reads well, but the iterative version is strictly better here — same time, less space, no risk of hitting Python's recursion limit. This is one of the cases where iteration genuinely wins.
→ [recursion-limit](../syntax/recursion-limit.md)

**Note this is the second O(1)-space technique in the roadmap that gets its speed from *structure* rather than *memory*** — like [Two Sum II](167-two-sum-ii-input-array-is-sorted.md)'s two pointers. Sortedness is doing the work a hash map would otherwise do with O(n) space. Contrast with [Two Sum](1-two-sum.md), where an unsorted array forced the memory trade.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The array is sorted, so comparing the target to the middle element tells me which half it must be in — and I discard the other half entirely. I keep an inclusive range `[left, right]` with the invariant that the target, if present, is inside it. The loop runs while `left <= right`, because when they're equal there's still one unchecked element. On each step I compare and move past the midpoint with `mid + 1` or `mid - 1`, never plain `mid`, which would loop forever on a two-element range. Each step halves the space, so O(log n) time and O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why `<=` and not `<`?" | With an inclusive range, `left == right` is one unchecked element. `<` fails on single-element arrays. |
| "Why `mid + 1` rather than `mid`?" | `mid` was just checked and rejected. Keeping it means no progress — `[1,2]` with `left = mid` loops forever. |
| "What if there were **duplicates**?" | Standard binary search returns *an* index, not the first. For the leftmost occurrence, don't return on a match — set `right = mid - 1` and record the index, continuing left. See [`bisect_left`](../syntax/bisect-module.md). |
| "What about integer overflow?" | Not in Python (arbitrary-precision ints), but in C/Java `left + right` can overflow — use `left + (right - left) // 2`. Famously a real bug in Java's standard library for years. |
| "Find the **insertion point** for a missing target." | It's `left` when the loop exits — that's exactly `bisect_left`. LeetCode 35. |
| "Descending order?" | Flip the two comparisons. The structure is identical. |
| "Write it recursively." | Same logic, but O(log n) stack space. Iterative is better here. |

**Traps:**

- **`while left < right`** — skips the final element.
- **`left = mid` or `right = mid`** — infinite loop on a two-element range, because floor division keeps `mid == left`.
- **`right = len(nums)`** — that's an exclusive bound paired with inclusive logic. If you use exclusive `[left, right)`, you must *also* switch to `while left < right` and `right = mid`. **Pick one convention and keep it.**
- **Forgetting the array must be sorted.** Binary search on unsorted data returns plausible-looking garbage.
- **Using `/` instead of `//`** — a float index raises `TypeError`.
- **Returning `left` instead of `-1`** on a miss — `left` is the insertion point, a different question.

**This same move shows up in:** [Search a 2D Matrix](74-search-a-2d-matrix.md) (this exact loop over a flattened index space) · [Koko Eating Bananas](875-koko-eating-bananas.md) (binary search on the *answer* rather than an array) · [Find Minimum in Rotated Sorted Array](153-find-minimum-in-rotated-sorted-array.md) (halving with a modified comparison) · [Two Sum II](167-two-sum-ii-input-array-is-sorted.md) (the other way sortedness buys O(1) space).

</details>

---
