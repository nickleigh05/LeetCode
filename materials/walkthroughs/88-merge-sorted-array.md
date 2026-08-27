# 88. Merge Sorted Array

**Easy** · [LeetCode](https://leetcode.com/problems/merge-sorted-array/) · [Solution file (no hints)](../../problems/0001-0499/88.py)

[📖 01. Arrays & Hashing lesson](../learning/01-arrays-hashing.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 01. Arrays & Hashing problems](../rmap-practice/01-arrays-hashing.md)

---

You are given two integer arrays `nums1` and `nums2`, sorted in **non-decreasing order**, and integers `m` and `n` — the number of real elements in each. Merge `nums2` into `nums1` as one sorted array, **in-place**. `nums1` has length `m + n`, where the final `n` slots are `0` placeholders to be overwritten.

```
nums1 = [1,2,3,0,0,0], m = 3,  nums2 = [2,5,6], n = 3   →  [1,2,2,3,5,6]
nums1 = [1],           m = 1,  nums2 = [],      n = 0   →  [1]
nums1 = [0],           m = 0,  nums2 = [1],     n = 1   →  [1]
```

**Constraints:** `nums1.length == m + n` · `nums2.length == n` · `0 <= m, n <= 200` · `-10⁹ <= nums[i] <= 10⁹`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| both arrays are **sorted** | You never need to *sort* anything — only to **interleave**. That's the O(n) merge step from [merge sort](../algorithms/merge-sort.md) |
| "**in-place**", into `nums1` | Return nothing; mutate `nums1`. No building a third array and copying back |
| `nums1` has **`m + n`** slots | ⚠️ **The gift, and the whole point.** The destination is exactly the right size — the space you need has been pre-allocated for you |
| the last `n` entries are `0` | Placeholders. Not data. `m`, not `len(nums1)`, tells you where the real values end |
| `m` or `n` can be **0** | `nums2` empty ⇒ nothing to do. `nums1` empty ⇒ it's a straight copy. Both must work with no special-casing |
| values can be negative | So `0` is a legitimate *value*, not a sentinel you can test for. Never write `if nums1[i] == 0` to find the padding |

The naive plan is "merge from the front like a normal two-list merge." Try it and watch it fail: writing the merged result at `nums1[0]` **clobbers `nums1[0]`'s original value before you've used it.** On `nums1 = [1,2,3,0,0,0]` and `nums2 = [2,5,6]`, the first write is fine, but you're now overwriting live data with every subsequent step.

The fix is the entire insight:

> **The free space is at the back. So fill from the back.**

Walk both arrays from their largest elements down, writing the biggest remaining value into the highest unfilled slot. Every write lands in the padding or in a slot whose value you've already consumed — so nothing is ever destroyed.

🤔 **Before you open the next section:** if you write the merged array starting from the *last* index and work down, can a write ever land on an element you still need to read?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Concatenate + sort | `nums1[m:] = nums2; nums1.sort()` | O((m+n)log(m+n)) | O(1)–O(n)\* | ⚠️ Two lines, correct, throws away sortedness |
| Merge forward into a copy | Standard merge into a new list, then copy back | O(m+n) | **O(m+n)** | ⚠️ Correct but violates in-place |
| Merge forward in place | Merge from index 0 | — | — | ❌ **Clobbers unread data** |
| **Merge backward in place** | Two read pointers at the ends, write pointer at the back | **O(m+n)** | **O(1)** | ✅ |

\* CPython's Timsort needs O(n) auxiliary in the general case.

**The decision: three pointers, all moving backward.**

- **`p1 = m - 1`** — the last *real* element of `nums1`
- **`p2 = n - 1`** — the last element of `nums2`
- **`p = m + n - 1`** — the last slot overall, where the next-largest value goes

At each step, compare `nums1[p1]` against `nums2[p2]`, write the **larger** at `p`, and step that pointer back.

**Why backward is safe — the invariant worth stating out loud:**

> `p` is always ≥ `p1`.

The write index starts strictly ahead of the read index (`m + n - 1 >= m - 1` whenever `n >= 0`) and both decrease by one per write, so the gap never closes. `nums1[p]` is therefore always either padding or a slot already consumed. **You cannot clobber unread data.** That's not a lucky accident of the examples — it's a property you can prove, and proving it is what separates "I remember this trick" from "I understand it."

**Why not just sort?** `nums1[m:] = nums2` followed by `nums1.sort()` genuinely works and is two lines. Say it as your baseline — but it's O((m+n) log(m+n)) and *discards the sortedness you were handed*. Being given sorted inputs and paying for a sort anyway is exactly what the problem is testing you not to do. The solution file keeps it as a documented alternative, and that's the right place for it.

**Why not merge forward into a temp array?** It's the natural [merge sort](../algorithms/merge-sort.md) step and it's O(m+n) time — but it needs O(m+n) space for the temp. The backward trick is what buys the O(1), and it only exists because the destination happens to have the padding at the end.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
p1 = m - 1
p2 = n - 1
p = m + n - 1
```

Three pointers, all at the **end** of their regions. `p1` is the last real element of `nums1` (index `m-1`, *not* `len(nums1)-1` — everything past `m` is padding). `p` is the final slot of the whole array.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
while p1 >= 0 and p2 >= 0:
```

Run only while **both** arrays still have elements. The moment either is exhausted the comparison stops making sense, and the cleanup below takes over.
→ [while-loop](../syntax/while-loop.md) · [logical-operators](../syntax/logical-operators.md)

```python
    if nums1[p1] > nums2[p2]:
        nums1[p] = nums1[p1]
        p1 -= 1
    else:
        nums1[p] = nums2[p2]
        p2 -= 1
```

The merge step, running downward: whichever remaining element is **larger** claims the highest unfilled slot.

The `else` covers the tie case (`==`) by taking from `nums2`, which is fine — with equal values it makes no difference to the result. (For a *stable* merge you'd want ties to come from `nums1`, but the elements here are plain integers, so there's nothing to distinguish.)

Note the self-assignment case: when `p == p1`, `nums1[p] = nums1[p1]` writes an element onto itself. Harmless, and a sign the invariant is holding exactly at its tightest.
→ [comparison-operators](../syntax/comparison-operators.md) · [elif-else](../syntax/elif-else.md)

```python
    p -= 1
```

Outside the branch, because **every** iteration fills exactly one slot regardless of which array it came from.

```python
nums1[:p2 + 1] = nums2[:p2 + 1]
```

**The cleanup, and the line most people get wrong.** The loop ends when one array is exhausted. Two cases:

- **`nums1` ran out** (`p1 < 0`) — `nums2` still has elements `0..p2`, and they're all smaller than everything already placed. They belong at the very front of `nums1`, which is precisely where they aren't yet. **This copy is required.**
- **`nums2` ran out** (`p2 < 0`) — the remaining `nums1` elements are *already sitting in their correct positions*. Nothing to do. And conveniently, `p2 + 1 == 0`, so the slice is empty and this line is a no-op.

One line handles both cases with no `if`. That's why it's written as a slice assignment rather than a loop.
→ [list-slicing](../syntax/list-slicing.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        p1 = m - 1
        p2 = n - 1
        p = m + n - 1

        while p1 >= 0 and p2 >= 0:
            if nums1[p1] > nums2[p2]:
                nums1[p] = nums1[p1]
                p1 -= 1
            else:
                nums1[p] = nums2[p2]
                p2 -= 1
            p -= 1

        nums1[:p2 + 1] = nums2[:p2 + 1]
```

</details>

<details>
<summary>The pragmatic alternative (in the solution file too)</summary>

```python
### additional solution ###
class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        nums1[m:] = nums2
        nums1.sort()
```

Correct and two lines — but O((m+n) log(m+n)), and it ignores the sortedness you were given. Name it as a baseline, then write the merge.

</details>

**Trace it** — `nums1 = [1,2,3,0,0,0]`, `m = 3`, `nums2 = [2,5,6]`, `n = 3`:

| `p1` | `p2` | `p` | Compare | Write | `nums1` |
|---|---|---|---|---|---|
| 2 | 2 | 5 | `3 > 6`? no | `nums2[2]=6` at 5 | `[1,2,3,0,0,6]` |
| 2 | 1 | 4 | `3 > 5`? no | `nums2[1]=5` at 4 | `[1,2,3,0,5,6]` |
| 2 | 0 | 3 | `3 > 2`? **yes** | `nums1[2]=3` at 3 | `[1,2,3,3,5,6]` |
| 1 | 0 | 2 | `2 > 2`? no | `nums2[0]=2` at 2 | `[1,2,2,3,5,6]` |
| 1 | **−1** | 1 | loop ends | — | `[1,2,2,3,5,6]` |

Cleanup: `p2 = -1`, so `nums1[:0] = nums2[:0]` — an empty no-op. Final: **`[1,2,2,3,5,6]`** ✅

Notice step 3 overwrote index 3, which held a `0` placeholder, and step 4 overwrote index 2 — whose original value `3` had already been copied to index 3. The invariant held throughout.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(m + n)</summary>

**O(m + n).**

Every iteration of the `while` writes exactly one element and permanently retires one input element, so the loop runs at most m + n times. The cleanup slice copies at most n more. Total work is linear in the combined size — and it must be, since a correct answer has to write m + n values.

This is **optimal**: you cannot merge two sorted sequences in less than linear time, because every element has to be placed.

**Compare to the sort-based approach:** O((m+n) log(m+n)). The log factor is pure waste here — sorting rediscovers ordering information you were already given. That's the specific inefficiency this problem is built to make you notice.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).** Three integer pointers, nothing allocated.

The reason it's achievable is worth stating precisely: **the destination was pre-sized to `m + n`, with the slack at the end.** That's not incidental — it's the design of the problem. The classic merge step needs somewhere to write, and here the padding at the back *is* that somewhere.

Change where the slack lives and the trick changes with it:

| Free space is… | Merge direction |
|---|---|
| at the **end** (this problem) | **backward**, largest first |
| at the **front** | forward, smallest first |
| nowhere (equal-size arrays) | you need O(n) temp, or an in-place merge algorithm that's far more involved |

**The transferable lesson:** when an in-place algorithm risks overwriting data you still need, check whether processing in the *opposite direction* makes the writes land somewhere safe. It's the same reasoning behind shifting an array right by iterating from the back, and behind `memmove` handling overlapping regions.

One Python note: `nums1[:p2+1] = nums2[:p2+1]` builds a small temporary slice of `nums2`, so it's technically O(n) for an instant. Nobody counts this against you, and you can avoid it entirely with an explicit loop if an interviewer is being strict.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Both arrays are sorted, so this is just the merge step — no sorting needed. The catch is doing it in place: merging from the front would overwrite `nums1`'s live elements before I read them. But the free space is at the *back*, so I merge backward — three pointers, one at the end of each array's real data and one at the last slot, writing the larger element each time. The write pointer starts ahead of `nums1`'s read pointer and they decrease together, so it can never clobber unread data. At the end, any leftover `nums2` elements get copied to the front; leftover `nums1` elements are already in place. O(m+n) time, O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why not merge forward?" | It overwrites `nums1`'s unread elements. Backward works because the padding is at the back, so the write pointer stays ahead of the read pointer. |
| "Why is the leftover-`nums1` case a no-op?" | Those elements are already in their final positions — they were never moved. Only leftover `nums2` elements need relocating. |
| "Merge **k** sorted arrays." | [Merge k Sorted Lists](23-merge-k-sorted-lists.md) — a [min-heap](../data-structures/heap.md) of the k current heads gives O(N log k). |
| "What if `nums1` had no extra space?" | You'd need O(n) temp space, or a genuine in-place merge (block-swap / rotation based) — O(n log n) time and considerably harder. |
| "What if the free space were at the front?" | Merge **forward**, smallest first. Same invariant, mirrored. |
| "Do it without the final slice copy." | Replace it with `while p2 >= 0: nums1[p] = nums2[p2]; p2 -= 1; p -= 1`. Same cost, no temporary. |
| "Merge in descending order?" | Flip the comparison and run the pointers forward from index 0. |

**Traps:**

- **Merging forward.** The single most common wrong answer — it silently corrupts `nums1`.
- **Using `len(nums1) - 1` for `p1`.** That points at padding, not data. `m` defines the boundary.
- **Treating `0` as "empty."** Values can be negative *and* zero — `0` is real data. Only `m` tells you what's real.
- **Forgetting the leftover-`nums2` copy.** Passes `[1,2,3] + [4,5,6]` and fails `[4,5,6] + [1,2,3]`. Always test the case where `nums2` holds the smallest values.
- **Copying leftover `nums1` elements too.** Unnecessary — they're already correct — and easy to get wrong.
- **Decrementing `p` inside both branches.** Works, but duplicating it invites one branch to drift. Put it once at the bottom of the loop.

**This same move shows up in:** [Merge Two Sorted Lists](21-merge-two-sorted-lists.md) (the same merge, on linked lists, where node reuse removes the clobbering worry) · [Merge k Sorted Lists](23-merge-k-sorted-lists.md) (the k-way generalization) · [Remove Element](27-remove-element.md) (in-place writing with a pointer invariant) · [Squares of a Sorted Array](977-squares-of-a-sorted-array.md) (another "fill from the back because the largest values are at the ends" problem).

</details>

---
