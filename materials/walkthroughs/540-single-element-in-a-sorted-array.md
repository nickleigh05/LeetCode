# 540. Single Element in a Sorted Array

**Medium** · [LeetCode](https://leetcode.com/problems/single-element-in-a-sorted-array/) · [Solution file (no hints)](../../problems/0500-0999/540.py)

[📖 05. Binary Search lesson](../learning/05-binary-search.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 05. Binary Search problems](../rmap-practice/05-binary-search.md)

---

You are given a **sorted** array where every element appears exactly **twice**, except one which appears **once**. Return that single element. Your solution must run in **O(log n)** time and **O(1)** space.

```
nums = [1,1,2,3,3,4,4,8,8]   →  2
nums = [3,3,7,7,10,11,11]    →  10
```

**Constraints:** `1 <= nums.length <= 10⁵` · `0 <= nums[i] <= 10⁵`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**sorted**" | ⚠️ Duplicates are **adjacent**, which is what makes the pairing structure visible |
| "every element twice, except one" | The length is always **odd** (`2k + 1`) |
| "**O(log n)** time" | Rules out XOR-everything and linear scanning, which are O(n) |
| "**O(1)** space" | Rules out a hash map or set |
| `n` up to 10⁵ | O(n) would pass the clock, but the stated bounds forbid it |

**The XOR trap.** The classic trick for "everything appears twice except one" is XOR-ing the entire array — pairs cancel, leaving the singleton. It's beautiful, O(n) time, O(1) space… and **it violates the O(log n) requirement**. Mention it as the obvious answer, then note why the problem rules it out. The constraint exists specifically to push you past it.

**The structural insight.** In a perfectly paired sorted array, pairs occupy index positions `(0,1), (2,3), (4,5), …` — each pair starts at an **even** index:

```
index:  0  1  2  3  4  5  6  7  8
value:  1  1  2  3  3  4  4  8  8
        └──┘  ↑  └──┘  └──┘  └──┘
        pair  single, and everything after it is SHIFTED
```

Before the singleton, `nums[even] == nums[even + 1]`. **After** the singleton, that pairing breaks — everything is displaced by one, so `nums[even] != nums[even + 1]`.

That gives a monotonic predicate:

```
even index i:      0      2      4      6
paired correctly: true  false  false  false
                        ↑
              the boundary — the singleton is at or before here
```

True-then-false, flipping exactly once. That's a boundary search — the same shape as [First Bad Version](278-first-bad-version.md), with "is this even index still correctly paired?" as the oracle.

🤔 **Before you open the next section:** if you check an even index `i` and find `nums[i] == nums[i+1]`, is the singleton to the left or the right of `i`?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| XOR everything | Pairs cancel; the singleton survives | O(n) | O(1) | ⚠️ Elegant, but violates O(log n) |
| Hash set toggle | Add/remove; one element remains | O(n) | **O(n)** | ❌ Violates both bounds |
| Linear scan in steps of 2 | Check each pair | O(n) | O(1) | ⚠️ Violates O(log n) |
| **Binary search on pairing parity** | Test whether even indices are still paired | **O(log n)** | **O(1)** | ✅ |

**The decision: binary search over even indices, testing the pairing invariant.**

The algorithm:

1. Keep `left` and `right` on the array, using the boundary convention (`left < right`, `right = mid`).
2. Force `mid` to be **even** — `if mid % 2 == 1: mid -= 1`.
3. If `nums[mid] == nums[mid + 1]`, the pairing still holds here, so the singleton is **after** this pair → `left = mid + 2`.
4. Otherwise the pairing is already broken, so the singleton is at `mid` or before → `right = mid`.
5. When they converge, `left` is the singleton's index.

**Why force `mid` to be even.** The entire test — "does this element pair with the next one?" — is only meaningful at the *start* of a pair. At an odd index you'd be comparing the second element of one pair with the first of the next, which tells you nothing useful. Snapping `mid` down to the nearest even index guarantees you're always asking the right question.

`mid -= 1` (rather than `+= 1`) keeps `mid` within `[left, right)`, preserving the loop's shrinking guarantee.

**Why `left = mid + 2` and not `mid + 1`.** If `nums[mid] == nums[mid+1]`, you've confirmed a **complete pair** at positions `mid` and `mid+1`. Both are eliminated, so the next candidate start is `mid + 2` — which is also even, maintaining the invariant that `left` always points at a pair boundary.

**Why `right = mid` keeps the candidate.** When the pairing is broken at `mid`, the singleton could be `mid` itself. Discarding it with `mid - 1` would overshoot. This is the same `right = mid` / `left < right` pairing as [First Bad Version](278-first-bad-version.md) and [Find Peak Element](162-find-peak-element.md).

**Why `mid + 1` is always in bounds.** Since `left < right` and `mid < right`, and the array has odd length with `right` at most `n - 1`, `mid + 1 <= right <= n - 1`. No bounds check needed.

**The alternative XOR-index trick**, worth knowing: instead of snapping `mid` to even, use `nums[mid] == nums[mid ^ 1]`. The XOR flips the last bit, so it pairs even↔odd automatically — `mid ^ 1` gives `mid+1` for even `mid` and `mid-1` for odd. Same logic, no explicit parity fix. Clever, and a nice thing to mention.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
left = 0
right = len(nums) - 1
```

The full range. `right` is the last index — and because the length is odd, it's even.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
while left < right:
```

**Boundary-search convention** — `<` pairs with `right = mid` below. Loop until one candidate remains.
→ [while-loop](../syntax/while-loop.md)

```python
    mid = (left + right) // 2
    if mid % 2 == 1:
        mid -= 1
```

**Snap `mid` down to an even index.**

The pairing test only makes sense at a pair's first element. Decrementing (rather than incrementing) keeps `mid >= left`, so the range still shrinks properly.
→ [integer-division-modulo](../syntax/integer-division-modulo.md)

```python
    if nums[mid] == nums[mid + 1]:
        left = mid + 2
```

**Pairing intact here** — so everything up to and including `mid + 1` is correctly paired, and the singleton lies strictly after. Skip the whole pair with `+ 2`, which also keeps `left` even.
→ [comparison-operators](../syntax/comparison-operators.md)

```python
    else:
        right = mid
```

**Pairing broken** — the displacement has already begun, so the singleton is at `mid` or before it. Keep `mid` as a candidate.
→ [elif-else](../syntax/elif-else.md)

```python
return nums[left]
```

The pointers converged on the singleton's index. Return the **value**, not the index — the problem asks for the element.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def singleNonDuplicate(self, nums: List[int]) -> int:

        left = 0
        right = len(nums) - 1

        while left < right:
            mid = (left + right) // 2
            if mid % 2 == 1:
                mid -= 1

            if nums[mid] == nums[mid + 1]:
                left = mid + 2
            else:
                right = mid

        return nums[left]
```

</details>

<details>
<summary>The XOR-index variant (no explicit parity fix)</summary>

```python
class Solution:
    def singleNonDuplicate(self, nums: List[int]) -> int:
        left, right = 0, len(nums) - 1

        while left < right:
            mid = (left + right) // 2
            if nums[mid] == nums[mid ^ 1]:
                left = mid + 1
            else:
                right = mid

        return nums[left]
```

`mid ^ 1` flips the lowest bit: even `mid` pairs with `mid + 1`, odd `mid` pairs with `mid - 1`. The parity handling becomes implicit, so `left = mid + 1` suffices. Same O(log n), fewer lines — see [bitwise-operators](../syntax/bitwise-operators.md).

</details>

**Trace it** — `nums = [1,1,2,3,3,4,4,8,8]` (singleton `2` at index 2):

| `left` | `right` | raw `mid` | even `mid` | `nums[mid]` vs `nums[mid+1]` | Paired? | Action |
|---|---|---|---|---|---|---|
| 0 | 8 | 4 | 4 | `nums[4]=3` vs `nums[5]=4` | ❌ | `right = 4` |
| 0 | 4 | 2 | 2 | `nums[2]=2` vs `nums[3]=3` | ❌ | `right = 2` |
| 0 | 2 | 1 | **0** | `nums[0]=1` vs `nums[1]=1` | ✅ | `left = 2` |
| 2 | 2 | — | — | — | — | exit |

`return nums[2]` = **2** ✅

Row 3 shows the parity snap doing real work: raw `mid` was 1 (odd), which would have compared `nums[1]=1` against `nums[2]=2` — a meaningless cross-pair comparison. Snapping to 0 asked the correct question and correctly concluded the first pair was intact.

**A second trace** — `nums = [3,3,7,7,10,11,11]` (singleton `10` at index 4):

| `left` | `right` | raw `mid` | even `mid` | Compare | Paired? | Action |
|---|---|---|---|---|---|---|
| 0 | 6 | 3 | **2** | `nums[2]=7` vs `nums[3]=7` | ✅ | `left = 4` |
| 4 | 6 | 5 | **4** | `nums[4]=10` vs `nums[5]=11` | ❌ | `right = 4` |
| 4 | 4 | — | — | — | — | exit |

`return nums[4]` = **10** ✅

</details>

<details>
<summary><b>4 · Time complexity</b> — O(log n)</summary>

**O(log n).**

Each iteration halves the range and does one comparison. At `n = 10⁵` that's about **17 iterations**.

**Why the O(n) approaches don't qualify** — worth saying explicitly, since the XOR solution is so tempting:

| | Time | Space | Meets the brief? |
|---|---|---|---|
| XOR everything | O(n) | O(1) | ❌ time |
| Hash set | O(n) | O(n) | ❌ both |
| Linear pair scan | O(n) | O(1) | ❌ time |
| **Binary search** | **O(log n)** | **O(1)** | ✅ |

The XOR solution is genuinely elegant and correct, and it's the right answer to the *unsorted* version of this problem ([Single Number](136-single-number.md)). Here, sortedness provides extra structure — the pairing invariant — and the problem's tighter bound exists to make you exploit it.

That's the lesson: **when a problem hands you sortedness and demands better than linear, the sortedness is the tool you're expected to use.**

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — three integers, no allocation.

Both the parity-snap and XOR-index variants are constant space; the difference is purely stylistic.

**Why O(1) rules out the hash approaches.** Toggling elements in and out of a set until one remains is O(n) space and would fail the brief even if the time bound allowed it.

**The structural point:** the array's own ordering encodes all the information needed. You're not building an index of what you've seen — you're **querying a property of the arrangement** (is this even index still correctly paired?) that sortedness makes locally checkable in O(1).

Recognizing when the input's structure can substitute for auxiliary memory is the same skill as in [First Missing Positive](41-first-missing-positive.md), where the array becomes its own hash table.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The obvious answer is XOR-ing everything, since pairs cancel — but that's O(n) and the problem asks for O(log n), so the sortedness must be doing work. The key structure is that before the singleton, every pair starts at an even index — `nums[even] == nums[even+1]`. After the singleton, everything shifts by one and that breaks. So 'is this even index still correctly paired?' is a monotonic true-then-false predicate, which I can binary search. I snap `mid` down to an even index so the comparison is always at a pair's start; if it's paired I skip the whole pair with `left = mid + 2`, otherwise the singleton is at or before `mid` so `right = mid`. When they converge, `nums[left]` is the answer. O(log n) time, O(1) space. There's also a neat variant using `nums[mid] == nums[mid ^ 1]`, which handles parity implicitly."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why not XOR everything?" | **The expected question.** It's O(n); the problem demands O(log n), so sortedness must be exploited. |
| "What if the array **weren't** sorted?" | Then XOR is optimal — O(n) time, O(1) space. That's [Single Number](136-single-number.md). |
| "Why snap `mid` to even?" | The pairing test is only meaningful at a pair's first element; at an odd index you'd compare across two different pairs. |
| "Why `left = mid + 2`?" | A confirmed intact pair eliminates two positions, and `+2` keeps `left` even. |
| "Can you avoid the parity fix?" | Yes — `nums[mid] == nums[mid ^ 1]` pairs even↔odd automatically. |
| "What if elements appeared **three** times except one?" | The pairing invariant becomes a modulo-3 index property; binary search still applies with a reworked predicate. |
| "What if there were **two** singletons?" | Monotonicity breaks — the predicate flips more than once, so binary search is invalid. You'd need O(n). |

**Traps:**

- **Not forcing `mid` even.** Comparisons then straddle pair boundaries and the logic silently breaks.
- **Snapping with `mid += 1` instead of `-= 1`.** Can push `mid` to `right`, breaking the shrink guarantee and risking an infinite loop.
- **`left = mid + 1` after a confirmed pair.** Leaves `left` odd, violating the invariant that it points at a pair start. (It *is* correct in the XOR-index variant, where parity is handled differently — don't mix the two.)
- **`right = mid - 1`.** Discards the singleton when the break is exactly at `mid`.
- **`left <= right` with `right = mid`.** Infinite loop at a one-element range.
- **Returning `left` instead of `nums[left]`.** The problem wants the value.
- **Reaching for XOR.** Right instinct, wrong problem — the bound rules it out.

**This same move shows up in:** [Single Number](136-single-number.md) (the unsorted version, where XOR *is* the answer) · [First Bad Version](278-first-bad-version.md) (the same `right = mid` boundary convention over a monotonic predicate) · [Find Peak Element](162-find-peak-element.md) (binary search on a structural property rather than values) · [First Missing Positive](41-first-missing-positive.md) (using the array's own arrangement instead of auxiliary memory).

</details>

---
