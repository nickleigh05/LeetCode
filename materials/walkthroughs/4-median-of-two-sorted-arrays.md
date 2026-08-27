# 4. Median of Two Sorted Arrays

**Hard** · [LeetCode](https://leetcode.com/problems/median-of-two-sorted-arrays/)

[📖 05. Binary Search lesson](../learning/05-binary-search.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 05. Binary Search problems](../rmap-practice/05-binary-search.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Given two sorted arrays `nums1` and `nums2` of sizes `m` and `n`, return the **median** of the two sorted arrays combined.

The overall run time complexity should be **O(log(m+n))**.

```
nums1 = [1,3], nums2 = [2]     →  2.0      (merged: [1,2,3])
nums1 = [1,2], nums2 = [3,4]   →  2.5      (merged: [1,2,3,4] → (2+3)/2)
```

**Constraints:** `0 <= m, n <= 1000` · `1 <= m + n <= 2000` · both arrays sorted ascending

> **Try it yourself first.** This is a genuinely hard problem — the sections below build up slowly.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**median**" | The middle of the combined data. Odd total → the single middle element; even → the average of the two middle ones |
| "two **sorted** arrays" | Both ordered — the structure you must exploit |
| "**O(log(m+n))**" | ⚠️ Rules out merging, which is O(m+n). And log of a *sum* means you binary search one of them |
| either array can be **empty** | `m` or `n` can be 0 — the code must survive that |

**Start from what the median actually is.** Forget medians as "the middle value" and think of it as a **partition**:

> Split the combined data into a **left half** and a **right half** of equal size, such that *every element on the left is ≤ every element on the right*. The median lives at that boundary.

```
merged:  [1, 2, 3, 4, 5, 6]
                  |
          left    |    right       ← 3 elements each
        [1,2,3]   |   [4,5,6]
              ↑   ↑
        max of left, min of right  →  median = (3+4)/2
```

Now the leap: **you never have to merge to find that boundary.** If you decide to take `i` elements from A's front, then to fill a half of size `half` you must take exactly `half - i` from B. **Choosing `i` determines the entire partition.** So there's really only one unknown.

And the partition is *correct* precisely when the two "cross" conditions hold:

```
A:  ... a_left  |  a_right ...
B:  ... b_left  |  b_right ...

valid  ⟺  a_left <= b_right   AND   b_left <= a_right
```

Within each array, left ≤ right is automatic (they're sorted). Only the cross-comparisons can fail.

🤔 **Before you open the next section:** if `a_left > b_right`, you took too many elements from A. Should `i` go up or down — and does that suggest a search strategy?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Merge fully, take the middle | Build the combined array | O(m+n) | ❌ Violates the bound (but write it first if stuck!) |
| Merge halfway | Stop at the midpoint | O(m+n) | ❌ Same order |
| Find the k-th element recursively | Discard k/2 at a time | O(log(m+n)) | ⚠️ Correct, notoriously fiddly |
| **Binary search the partition** | Search `i` in the **smaller** array | **O(log(min(m,n)))** | ✅ Even better than required |

**The decision: binary search over the partition point `i` in the smaller array.**

Three ideas stack up:

**1. Search the smaller array.** Swap so `A` is shorter. This bounds the search by `log(min(m,n))` — *better* than the required `log(m+n)` — and, more practically, it guarantees the derived index into `B` stays in range.

**2. `i` determines `j`.** With `half = (m+n) // 2` elements needed on the left, taking `i+1` from A forces `j+1 = half - (i+1)` from B, so:

```
j = half - i - 2
```

*(The `-2` is because `i` and `j` are the **indices of the last elements** in each left part, so the counts are `i+1` and `j+1`.)*

**3. The cross-conditions are monotonic.** Increase `i` and `a_left` rises while `b_right` falls — so `a_left > b_right` means you overshot and must move **left**. That monotonicity is what licenses binary search, exactly as in [Koko](875-koko-eating-bananas.md).

**The infinity sentinels.** When a partition takes nothing from an array (or everything), there's no neighbour to compare. Using `-inf` for a missing left and `+inf` for a missing right makes those comparisons *automatically pass* — an empty left side can't be too big, an empty right side can't be too small. **This is what removes every edge case**, including empty arrays, and it's worth calling out as a deliberate technique rather than a hack.

**If you freeze in an interview:** say *"the O(m+n) merge is straightforward — let me write that first, then optimize."* A correct linear solution vastly beats a broken logarithmic one on a Hard.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
A, B = nums1, nums2
if len(A) > len(B):
    A, B = B, A
```

Ensure **`A` is the shorter array**. This bounds the search at `log(min(m,n))` and keeps the derived `j` within `B`'s range.

Python's tuple assignment swaps without a temporary.
→ [swap-tuple-assign](../syntax/swap-tuple-assign.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
total = len(A) + len(B)
half = total // 2
```

`half` is how many elements belong on the **left** side. For an odd total this floors, putting the extra element on the *right* — which is why the odd case later reads the minimum of the right side.
→ [integer-division-modulo](../syntax/integer-division-modulo.md)

```python
left = 0
right = len(A) - 1

while True:
    i = (left + right) // 2
    j = half - i - 2
```

Binary search over `i`, the index of A's **last left-side element**. `j` is the same for B, derived so the two left parts total `half`.

`while True` because the exit is the *validity check* inside, not a boundary condition. The search always terminates — a valid partition provably exists.

Note `i` can legitimately be `-1` (take nothing from A), which Python's floor division produces naturally when `right` goes negative.
→ [while-loop](../syntax/while-loop.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
    a_left = A[i] if i >= 0 else float("-inf")
    a_right = A[i + 1] if (i + 1) < len(A) else float("inf")
    b_left = B[j] if j >= 0 else float("-inf")
    b_right = B[j + 1] if (j + 1) < len(B) else float("inf")
```

**The four boundary values — and the sentinels that kill every edge case.**

- `a_left` / `b_left`: the largest element on each array's left side.
- `a_right` / `b_right`: the smallest on each right side.

When a side is empty, the sentinel makes its comparisons vacuously true:
- **`-inf` for a missing left** — nothing on an empty left can be too large.
- **`+inf` for a missing right** — nothing on an empty right can be too small.

This is why empty input arrays, and partitions taking all-or-nothing from A, need no special handling at all.
→ [ternary-expression](../syntax/ternary-expression.md) · [float-inf](../syntax/float-inf.md) · [int-float-basics](../syntax/int-float-basics.md)

```python
    if a_left <= b_right and b_left <= a_right:
```

**The validity test.** Both cross-conditions must hold. Within an array left ≤ right is guaranteed by sortedness, so only these two can fail.
→ [logical-operators](../syntax/logical-operators.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
        if total % 2:
            return min(a_right, b_right)
        return (max(a_left, b_left) + min(a_right, b_right)) / 2
```

**Odd total** — `half` floored, so the right side has one extra element and the median is the smallest thing on the right.

**Even total** — the median averages the largest on the left and the smallest on the right. `/` gives a float, as required.
→ [min-max-key](../syntax/min-max-key.md)

```python
    elif a_left > b_right:
        right = i - 1
```

**Too many from A** — A's left side reaches past B's right side. Shrink `i`.

```python
    else:
        left = i + 1
```

**Too few from A** (so `b_left > a_right`). Take more.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:

        A, B = nums1, nums2
        if len(A) > len(B):
            A, B = B, A

        total = len(A) + len(B)
        half = total // 2

        left = 0
        right = len(A) - 1

        while True:
            i = (left + right) // 2
            j = half - i - 2

            a_left = A[i] if i >= 0 else float("-inf")
            a_right = A[i + 1] if (i + 1) < len(A) else float("inf")
            b_left = B[j] if j >= 0 else float("-inf")
            b_right = B[j + 1] if (j + 1) < len(B) else float("inf")

            if a_left <= b_right and b_left <= a_right:
                if total % 2:
                    return min(a_right, b_right)
                return (max(a_left, b_left) + min(a_right, b_right)) / 2
            elif a_left > b_right:
                right = i - 1
            else:
                left = i + 1
```

</details>

**Trace it** — `nums1 = [1,3]`, `nums2 = [2]`. A is longer, so swap: **`A = [2]`, `B = [1,3]`**. `total = 3`, `half = 1`.

| `left` | `right` | `i` | `j` | `a_left` | `a_right` | `b_left` | `b_right` | Valid? | Action |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | −1 | 2 | +inf | −inf | 1 | `2 <= 1`? **no** | `a_left > b_right` → `right = -1` |
| 0 | −1 | −1 | 0 | −inf | 2 | 1 | 3 | `-inf<=3` ✓ `1<=2` ✓ | **valid** |

Odd total → `min(a_right, b_right) = min(2, 3) = **2**` ✅ (merged `[1,2,3]`, median 2).

Notice the final partition takes **nothing** from A and one element from B — handled entirely by the `-inf` sentinel.

**Second example** — `A = [1,2]`, `B = [3,4]`, `total = 4`, `half = 2`:

| `left` | `right` | `i` | `j` | `a_left` | `a_right` | `b_left` | `b_right` | Valid? |
|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 0 | 0 | 1 | 2 | 3 | 4 | `1<=4` ✓ but `3<=2` ✗ → `left = 1` |
| 1 | 1 | 1 | −1 | 2 | +inf | −inf | 3 | ✓ ✓ **valid** |

Even → `(max(2, −inf) + min(inf, 3)) / 2 = (2+3)/2 = **2.5**` ✅

</details>

<details>
<summary><b>4 · Time complexity</b> — O(log(min(m, n)))</summary>

**O(log(min(m, n)))** — strictly better than the required O(log(m+n)).

The search runs over A's partition points, and A is the **shorter** array. Each iteration does O(1) work: compute `j`, read four values, compare. The range halves every step.

At m = n = 1000 that's about **10 iterations**.

**Why it beats the requirement.** `log(min(m,n)) <= log(m+n)` always, and dramatically so when the arrays are lopsided: with m = 1 and n = 1,000,000, this does **1** iteration while `log(m+n)` would allow 20. Searching the smaller array is free to do and strictly better.

**Versus merging:** O(m+n) = 2000 operations here versus ~10. The bound is what makes this a Hard — the merge is trivial to write and simply too slow.

**Why binary search applies at all:** the cross-conditions are monotonic in `i`. As `i` grows, `a_left` increases and `b_right` decreases, so `a_left > b_right` flips from false to true exactly once. Same underlying justification as [Koko Eating Bananas](875-koko-eating-bananas.md) — **a monotonic predicate, not a sorted array, is the real precondition.**

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).**

A handful of integers and four boundary values. **Nothing is merged, copied, or allocated** — the arrays are only indexed.

That's the striking part of this solution. The obvious approach materializes an `(m+n)`-element merged array to read one or two values out of the middle. This one computes those same values directly from four index lookups.

**The pattern completes the unit's arc:**

| Problem | What was never built |
|---|---|
| [74](74-search-a-2d-matrix.md) | The flattened matrix |
| [875](875-koko-eating-bananas.md) | The array of candidate speeds |
| **4** | **The merged array** |

Each searches a structure that exists only as *arithmetic*. Once you see that binary search needs nothing but "a range, and a rule for halving it", the search space stops needing to be real.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Merging is O(m+n) and I need logarithmic, so I won't merge at all. I reframe the median as a *partition*: split the combined data into equal-size left and right halves where everything on the left is ≤ everything on the right. The key insight is that choosing how many elements to take from A completely determines how many come from B — so there's one unknown. I binary search that partition point in the **smaller** array. A partition is valid when both cross-conditions hold: A's last-left ≤ B's first-right, and B's last-left ≤ A's first-right. If A's left overshoots, I took too many and search left; otherwise right. I use ±infinity for missing boundary elements, which makes empty sides and empty arrays fall out with no special cases. O(log(min(m,n))) time, O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why binary search the **smaller** array?" | Better bound — `log(min(m,n))` — and it keeps the derived `j` in range. Free to do. |
| "What are the infinities for?" | Partitions can take nothing or everything from an array, leaving no neighbour to compare. `±inf` makes those comparisons vacuously true, removing every edge case. |
| "Why is the partition condition only two comparisons?" | Within each array, left ≤ right is guaranteed by sortedness. Only the cross-pairs can be violated. |
| "Generalize to the **k-th** smallest element." | Same partition idea with `half` replaced by `k`. Or the recursive "discard k/2 from one array" approach — also O(log(m+n)). |
| "**Three** sorted arrays?" | The partition argument doesn't extend cleanly. Use a heap-based merge, or binary search on the *value* and count elements ≤ it — O((m+n+p) log(range)). |
| "How would you test it?" | Empty arrays, single elements, no overlap (`[1,2]` and `[3,4]`), full overlap, one array much longer, and odd vs. even totals. Then compare against a brute-force merge on random inputs. |
| "I'm stuck — is a merge acceptable?" | Write it, state it's O(m+n), then optimize. A working linear solution beats a broken logarithmic one. |

**Traps:**

- **Getting `j` wrong.** It's `half - i - 2` because `i` and `j` are *indices* (counts are `i+1`, `j+1`). Verify it on a concrete example rather than trusting the algebra.
- **Forgetting to swap** so A is smaller — `j` can then index outside `B`.
- **Omitting the sentinels** and writing explicit boundary cases instead. Correct but far more code and far more bugs.
- **`half = (total + 1) // 2`** — a valid alternative convention, but then the odd case reads `max` of the *left* side. Pick one and stay consistent.
- **Integer division for the even-case average.** `//` truncates; `(2+3)//2 = 2`, not 2.5.
- **`while left <= right`** — the exit here is the validity check, not the boundary; the loop is `while True` deliberately.

**This same move shows up in:** [Koko Eating Bananas](875-koko-eating-bananas.md) (binary search on a monotonic predicate, not an array) · [Search a 2D Matrix](74-search-a-2d-matrix.md) (searching a structure never materialized) · [Binary Search](704-binary-search.md) (the skeleton underneath) · [Merge k Sorted Lists](23-merge-k-sorted-lists.md) (when you *do* need the merged data).

</details>

---
