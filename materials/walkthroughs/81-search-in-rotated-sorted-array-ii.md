# 81. Search in Rotated Sorted Array II

**Medium** · [LeetCode](https://leetcode.com/problems/search-in-rotated-sorted-array-ii/) · [Solution file (no hints)](../../problems/0001-0499/81.py)

[📖 05. Binary Search lesson](../learning/05-binary-search.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 05. Binary Search problems](../rmap-practice/05-binary-search.md)

---

An array sorted in non-decreasing order has been **rotated** at an unknown pivot, and it **may contain duplicates**. Return `True` if `target` is in `nums`, otherwise `False`. Minimise the number of operations.

```
nums = [2, 5, 6, 0, 0, 1, 2],  target = 0   →  True
nums = [2, 5, 6, 0, 0, 1, 2],  target = 3   →  False
nums = [1, 0, 1, 1, 1],        target = 0   →  True
```

**Constraints:** `1 <= nums.length <= 5000` · `-10⁴ <= nums[i], target <= 10⁴` · `nums` is a rotated non-decreasing array

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "rotated" | Two sorted runs back to back. At any midpoint, **at least one half is sorted** |
| "non-decreasing", **duplicates allowed** | This is the change from [Search in Rotated Sorted Array](33-search-in-rotated-sorted-array.md). Equal values can hide which half is sorted |
| returns a **bool** | No index needed. Just "is it there?" |
| "minimise operations" | Use binary search, not a linear scan |

**The whole difficulty is one case.** In the no-duplicates version you decide which half is sorted by comparing `nums[lo] <= nums[mid]`. With duplicates, `nums[lo] == nums[mid] == nums[hi]` can't tell you anything:

```
[1, 1, 1, 0, 1]   ← pivot is right of mid
[1, 0, 1, 1, 1]   ← pivot is left of mid
```

Both have `lo`, `mid`, `hi` all equal to 1. You can't tell which side the drop is on. The only safe move is to **shrink the window by one from each end**, because those ends can't be the target (`mid` was already checked and they equal `mid`).

🤔 **Before you open the next section:** if `nums[lo] == nums[mid] == nums[hi]` and `mid` isn't the target, why is it safe to discard both `lo` and `hi`?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Time | Space | Verdict |
|---|---|---|---|
| Linear scan (`target in nums`) | O(n) | O(1) | ⚠️ Correct, and what the worst case degrades to anyway. Not what the question wants |
| Find the pivot, then binary search the right side | O(log n) typical | O(1) | ⚠️ Finding the pivot with duplicates has the same ambiguity |
| **Modified [binary search](../algorithms/binary-search.md)** | **O(log n) typical, O(n) worst** | **O(1)** | ✅ |

**The decision: one binary search that works out which half is sorted at each step**, plus a duplicate-shrinking branch.

At each `mid`:

1. `nums[mid] == target` → found.
2. If `lo`, `mid`, `hi` are all equal → ambiguous, shrink both ends.
3. Else if `nums[lo] <= nums[mid]` → the **left half is sorted**. If the target is inside `[nums[lo], nums[mid])`, go left, otherwise go right.
4. Else the **right half is sorted**. If the target is inside `(nums[mid], nums[hi]]`, go right, otherwise go left.

**The honest worst case is O(n).** An array of all 1s with a single 0 hides the pivot, and the shrink step removes only two elements per iteration. That's inherent: no algorithm can beat O(n) here, so say so out loud.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
lo, hi = 0, len(nums) - 1

while lo <= hi:
    mid = (lo + hi) // 2
    if nums[mid] == target:
        return True
```

A standard inclusive binary search. Seeing the target at `mid` ends it immediately.
→ [while-loop](../syntax/while-loop.md) · [integer-division-modulo](../syntax/integer-division-modulo.md) · [binary-search](../algorithms/binary-search.md)

```python
    if nums[lo] == nums[mid] == nums[hi]:
        lo += 1
        hi -= 1
```

**The duplicate case.** All three equal means we can't tell which half is sorted. `mid` is known not to be the target, and `lo` and `hi` equal `mid`'s value, so neither of them is the target either. Drop both and look again.
→ [chained-comparisons](../syntax/chained-comparisons.md)

```python
    elif nums[lo] <= nums[mid]:
        if nums[lo] <= target < nums[mid]:
            hi = mid - 1
        else:
            lo = mid + 1
```

**Left half `[lo..mid]` is sorted.** If the target's value lies in that range, search left. Otherwise it can only be in the right half. The `<=` on the left bound and `<` on the right are deliberate: `mid` itself was already tested.
→ [elif-else](../syntax/elif-else.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
    else:
        if nums[mid] < target <= nums[hi]:
            lo = mid + 1
        else:
            hi = mid - 1

return False
```

**Right half `[mid..hi]` is sorted.** Mirror image: if the target is in `(nums[mid], nums[hi]]`, go right, otherwise left. If the loop ends, the target was never found.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def search(self, nums: List[int], target: int) -> bool:
        lo, hi = 0, len(nums) - 1

        while lo <= hi:
            mid = (lo + hi) // 2

            if nums[mid] == target:
                return True

            if nums[lo] == nums[mid] == nums[hi]:
                lo += 1
                hi -= 1
            elif nums[lo] <= nums[mid]:
                if nums[lo] <= target < nums[mid]:
                    hi = mid - 1
                else:
                    lo = mid + 1
            else:
                if nums[mid] < target <= nums[hi]:
                    lo = mid + 1
                else:
                    hi = mid - 1

        return False
```

</details>

**Trace it.** `nums = [1, 0, 1, 1, 1]`, `target = 0`:

| `lo` | `hi` | `mid` | `nums[mid]` | Case | Move |
|---|---|---|---|---|---|
| 0 | 4 | 2 | 1 | `1 == 1 == 1`, ambiguous | `lo = 1`, `hi = 3` |
| 1 | 3 | 2 | 1 | `nums[lo]=0 <= 1`, left half sorted. Is `0 <= 0 < 1`? yes | `hi = 1` |
| 1 | 1 | 1 | 0 | equals target | **`True`** ✅ |

</details>

<details>
<summary><b>4 · Time complexity</b> — O(log n) typical, O(n) worst case</summary>

Without duplicates, each step halves the window: **O(log n)**.

With duplicates, the shrink branch removes only two elements. An array like `[1, 1, 1, 1, 0, 1, 1]` can force it to run about `n / 2` times: **O(n) worst case**. That's unavoidable, because a hidden single different value can sit anywhere.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).** Three integer variables and no recursion.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "A rotated array always has one sorted half at any midpoint, so I binary search by working out which half is sorted and checking whether the target lies in it. The duplicates break one step: if `lo`, `mid` and `hi` are all equal I can't tell which half is sorted. But none of the three can be the target, because `mid` already failed, so I shrink both ends by one and try again. That makes it O(log n) typically, but O(n) in the worst case, which is unavoidable since a lone different value can hide anywhere."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "How does this differ from Rotated Array I?" | [Search in Rotated Sorted Array](33-search-in-rotated-sorted-array.md) has distinct values, so `nums[lo] <= nums[mid]` always identifies the sorted half. Only the equal-ends case is new here |
| "Why can't you do better than O(n)?" | With all-equal values and one odd element, any algorithm must look at every position to find it |
| "Find the minimum?" | [Find Minimum in Rotated Sorted Array](153-find-minimum-in-rotated-sorted-array.md). The duplicates version shrinks `hi` by one on ties |
| "Return the index?" | Return `mid` on a match. With duplicates the index you find may not be the first occurrence |

**Traps:**

- **Using `<` where `<=` is needed** in `nums[lo] <= nums[mid]`. When `lo == mid` the left half is a single element and is "sorted".
- **Using `<=` on both ends of the range check.** `mid` was already compared, so one end must be strict.
- **Shrinking only one end** in the equal case. It works but only removes one element per step.
- **Skipping the equal-case check.** An input like `[1, 0, 1, 1, 1]` then goes the wrong way and returns `False`.

**This same move shows up in:** [Search in Rotated Sorted Array](33-search-in-rotated-sorted-array.md) · [Find Minimum in Rotated Sorted Array](153-find-minimum-in-rotated-sorted-array.md) · [Find Peak Element](162-find-peak-element.md) (decide a direction from local structure).

</details>

---
