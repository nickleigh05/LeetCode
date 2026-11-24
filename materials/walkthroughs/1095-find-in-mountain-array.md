# 1095. Find in Mountain Array

**Hard** · [LeetCode](https://leetcode.com/problems/find-in-mountain-array/) · [Solution file (no hints)](../../problems/1000-1499/1095.py)

[📖 05. Binary Search lesson](../learning/05-binary-search.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 05. Binary Search problems](../rmap-practice/05-binary-search.md)

---

A **mountain array** strictly increases up to a single peak, then strictly decreases. You get a `MountainArray` object you can't read directly. It has only `get(index)` and `length()`. Return the **minimum index** whose value equals `target`, or `-1`. You may call `get` **at most 100 times**.

```
mountainArr = [1, 2, 3, 4, 5, 3, 1],  target = 3   →  2     (3 appears at 2 and 5, return the smaller)
mountainArr = [0, 1, 2, 4, 2, 1],     target = 3   →  -1
```

**Constraints:** `3 <= length <= 10⁴` · `0 <= target, mountainArr.get(i) <= 10⁹`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "mountain array" | Strictly up then strictly down. One peak, no plateaus |
| "at most **100** `get` calls" | With `n = 10⁴`, a scan (10⁴ calls) is impossible. 100 calls is about `3 × log₂ n`. This is **screaming binary search**, three times |
| "**minimum** index" | The value can appear on both slopes. Search the **ascending** slope first, because it has the smaller indices |
| can't index directly | Every probe costs a call. Don't read the same position twice if you can avoid it |
| "strictly" | Adjacent elements are never equal, so comparing `a[mid]` with `a[mid+1]` always gives a clear direction |

**The reframe.** The whole array isn't sorted, but it is made of **two sorted halves** that meet at the peak. So:

1. Binary search for the **peak** (comparing `mid` with `mid + 1` tells you which slope you're on).
2. Binary search the **ascending** part `[0..peak]` for the target.
3. If not found, binary search the **descending** part `[peak+1..n-1]`, with the comparisons flipped.

Each search costs about `log₂(10⁴) ≈ 14` steps. The peak search makes two `get` calls per step, so the total is about 28 + 14 + 14 = 56 calls, well under 100.

🤔 **Before you open the next section:** if `a[mid] < a[mid + 1]`, are you on the up slope or the down slope? Does the peak lie to the left or the right of `mid`?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | `get` calls | Verdict |
|---|---|---|
| Linear scan | up to `n` (10⁴) | ❌ Breaks the 100-call limit |
| Copy the whole array, then search | `n` | ❌ Same problem |
| **Peak search + 2 binary searches** | about `2·log n + log n + log n` ≈ 60 | ✅ |

**The decision: three [binary searches](../algorithms/binary-search.md).**

- **Find the peak.** `lo, hi = 0, n-1`. While `lo < hi`: if `get(mid) < get(mid+1)` we're still climbing, so the peak is to the right (`lo = mid + 1`). Otherwise `mid` could be the peak, so `hi = mid`. This is the same "go toward the bigger neighbour" idea as [Find Peak Element](162-find-peak-element.md).
- **Search the up slope** with an ordinary ascending binary search.
- **Search the down slope** with a *descending* binary search (the comparison reverses).

Search the up slope **first**: any match there has a smaller index than any match on the down slope, so you can return immediately without comparing.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
n = mountainArr.length()
lo, hi = 0, n - 1
while lo < hi:
    mid = (lo + hi) // 2
    if mountainArr.get(mid) < mountainArr.get(mid + 1):
        lo = mid + 1
    else:
        hi = mid
peak = lo
```

**Phase 1, find the peak.** If `mid` is lower than its right neighbour, the peak is strictly right of `mid`. If not, `mid` could itself be the peak, so keep it (`hi = mid`, not `mid - 1`). The loop ends with `lo == hi`, the peak index. Two `get` calls per step, about 28 total.
→ [while-loop](../syntax/while-loop.md) · [integer-division-modulo](../syntax/integer-division-modulo.md) · [binary-search](../algorithms/binary-search.md)

```python
lo, hi = 0, peak
while lo <= hi:
    mid = (lo + hi) // 2
    value = mountainArr.get(mid)
    if value == target:
        return mid
    if value < target:
        lo = mid + 1
    else:
        hi = mid - 1
```

**Phase 2, ascending search on `[0..peak]`.** A textbook binary search. If we find the target here, it's the smallest index possible, so return at once. `get` is stored in `value` so each probe costs exactly one call.
→ [if-return](../syntax/if-return.md) · [comparison-operators](../syntax/comparison-operators.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
lo, hi = peak + 1, n - 1
while lo <= hi:
    mid = (lo + hi) // 2
    value = mountainArr.get(mid)
    if value == target:
        return mid
    if value > target:
        lo = mid + 1
    else:
        hi = mid - 1

return -1
```

**Phase 3, descending search on `[peak+1..n-1]`.** The values shrink as the index grows, so the directions swap: if `value > target` we need something smaller, so move **right**. Reaching here means the up slope had no match. If this also fails, the answer is `-1`.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def findInMountainArray(self, target: int, mountainArr: 'MountainArray') -> int:
        n = mountainArr.length()

        lo, hi = 0, n - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if mountainArr.get(mid) < mountainArr.get(mid + 1):
                lo = mid + 1
            else:
                hi = mid
        peak = lo

        lo, hi = 0, peak
        while lo <= hi:
            mid = (lo + hi) // 2
            value = mountainArr.get(mid)
            if value == target:
                return mid
            if value < target:
                lo = mid + 1
            else:
                hi = mid - 1

        lo, hi = peak + 1, n - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            value = mountainArr.get(mid)
            if value == target:
                return mid
            if value > target:
                lo = mid + 1
            else:
                hi = mid - 1

        return -1
```

</details>

**Trace it.** `[1, 2, 3, 4, 5, 3, 1]`, `target = 3`:

| Phase | `lo` | `hi` | `mid` | Reads | Move |
|---|---|---|---|---|---|
| peak | 0 | 6 | 3 | `4 < 5` | `lo = 4` |
| peak | 4 | 6 | 5 | `3 < 1`? no | `hi = 5` |
| peak | 4 | 5 | 4 | `5 < 3`? no | `hi = 4`, **peak = 4** |
| up | 0 | 4 | 2 | `3 == 3` | **return 2** ✅ |

The `3` at index 5 is never needed. Searching the up slope first gives the minimum index for free.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(log n)</summary>

Three binary searches, each O(log n): **O(log n)** overall.

In `get` calls: the peak search uses about `2 · log₂ n ≈ 28`, and each slope search uses about `log₂ n ≈ 14`. Total ≈ **56**, comfortably inside 100.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).** A few integers. We never copy the array, which we couldn't do within the call limit anyway.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The 100-call limit rules out a scan, so this has to be binary search, and since the array isn't globally sorted I do it in three steps. First I binary search for the peak by comparing `mid` with `mid + 1`: if it's still rising the peak is to the right, otherwise `mid` is a candidate. Then I binary search the ascending slope for the target, and I do that first because any match there has a smaller index than one on the descending side. If it isn't there, I binary search the descending slope with the comparison flipped. About `4 log n` calls, O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Can you cut the `get` calls?" | Cache values you've read in a dict so a repeated probe is free. Also use `lo < hi` peak search, which already avoids edge cases |
| "Can the peak search be one call per step?" | Compare `get(mid)` against a cached `get(mid + 1)` from the last round. Not needed within the limit |
| "What if values weren't strictly increasing?" | Plateaus break the peak search (see [Search in Rotated Sorted Array II](81-search-in-rotated-sorted-array-ii.md) for the same issue) |
| "Why search the up slope first?" | It holds the smaller indices, so a hit there is automatically the minimum |
| "Related problems?" | [Find Peak Element](162-find-peak-element.md) · [Search in Rotated Sorted Array](33-search-in-rotated-sorted-array.md) |

**Traps:**

- **Using `hi = mid - 1` in the peak search.** You may skip over the peak itself.
- **Not flipping the comparison on the descending slope.** Both signs swap.
- **Searching the down slope first** and returning a larger index than necessary.
- **Calling `get(mid)` several times per iteration** instead of storing it. It eats your 100-call budget.
- **Including the peak in both slope ranges.** Harmless for correctness, but wasteful.

**This same move shows up in:** [Find Peak Element](162-find-peak-element.md) · [Binary Search](704-binary-search.md) · [Find Minimum in Rotated Sorted Array](153-find-minimum-in-rotated-sorted-array.md).

</details>

---
