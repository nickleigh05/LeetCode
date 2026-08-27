# 26. Remove Duplicates from Sorted Array

**Easy** · [LeetCode](https://leetcode.com/problems/remove-duplicates-from-sorted-array/) · [Solution file (no hints)](../../problems/0001-0499/26.py)

[📖 01. Arrays & Hashing lesson](../learning/01-arrays-hashing.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 01. Arrays & Hashing problems](../rmap-practice/01-arrays-hashing.md)

---

Given an integer array `nums` **sorted in non-decreasing order**, remove the duplicates **in-place** so each unique element appears only once, preserving the relative order. Return `k`, the number of unique elements — the first `k` slots of `nums` must hold them, and what lies beyond `k` doesn't matter.

```
nums = [1,1,2]          →  k = 2,  nums = [1,2,_]
nums = [0,0,1,1,1,2,2,3,3,4]  →  k = 5,  nums = [0,1,2,3,4,_,_,_,_,_]
```

**Constraints:** `1 <= nums.length <= 3·10⁴` · `-100 <= nums[i] <= 100` · `nums` is sorted ascending

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**sorted** in non-decreasing order" | ⚠️ The gift. Equal values are **adjacent**, so detecting a duplicate is a comparison with your neighbour — no set, no map, no memory of the past |
| "**in-place**" | O(1) extra space. You may overwrite `nums` freely, but you may not build a second array and copy it back |
| "return `k`" | The *count*, not the array. LeetCode reads `nums[0..k-1]` and ignores the rest |
| "beyond `k` doesn't matter" | **Liberating.** You don't have to delete, shift, or blank anything — just make the front correct |
| "preserving relative order" | Free, since the array is already sorted |
| `nums.length >= 1` | Never empty, so `nums[0]` is always safe — and always a keeper |

The reframe that makes this easy: stop thinking "delete the duplicates." Think **"rebuild the array from the front, keeping only what I want."** You're not removing — you're *writing*, and you happen to be writing into the same array you're reading from.

That works only because the write pointer can never outrun the read pointer: you write at most one element per element read, so `k <= i` always. You never clobber something you haven't looked at yet.

🤔 **Before you open the next section:** if you're walking the array once and copying keepers to the front, what's the single question you must ask about each element to decide whether it's a keeper?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Hash set | Track seen values, build a filtered list | O(n) | O(n) | ❌ Violates in-place; also ignores the sorted gift |
| `list(dict.fromkeys(nums))` | Dedupe via insertion-ordered dict | O(n) | O(n) | ❌ Same problem, plus it's a rebuild not an edit |
| Delete in place with `.pop()` | Remove duplicates as you find them | O(n²) | O(1) | ❌ Each `pop` shifts everything after it |
| **Two pointers (read + write)** | Read scans; write index places keepers at the front | **O(n)** | **O(1)** | ✅ |

**The decision: two pointers — a fast *read* index and a slow *write* index.**

This is the **[two pointers](../learning/02-two-pointers.md) "slow/fast" or "read/write" pattern**, and it's the canonical answer to *"filter an array in place."* Once you see it here you'll see it in [Remove Element](27-remove-element.md), [Move Zeroes](283-move-zeroes.md), and [Sort Colors](75-sort-colors.md) — same skeleton, different keep-condition.

The two pointers have genuinely different jobs, and naming them that way prevents most bugs:

- **`i` (read)** — marches across every element exactly once, asking "is this a keeper?"
- **`k` (write)** — the boundary of the finished region. `nums[0..k-1]` is the answer so far; `k` is where the next keeper goes.

**Why the sortedness is load-bearing:** the only thing that makes "is this a duplicate?" answerable in O(1) with no memory is that equal values are adjacent. Compare against the **last thing you kept** — `nums[k-1]` — and if it differs, this value is new. On an *unsorted* array this logic collapses and you genuinely need a hash set, which costs O(n) space.

**Why not `pop()`?** Removing from the middle of a Python list is O(n) because everything after it shifts left. Do that once per duplicate and you're at O(n²) — plus mutating a list while iterating it is a reliable way to skip elements.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
if not nums:
    return 0
```

Constraints promise at least one element, so this is defensive rather than required — but it makes the function safe standalone, and it's one line.
→ [truthy-falsy-values](../syntax/truthy-falsy-values.md)

```python
k = 1
```

**Start at 1, and understand why.** `nums[0]` is unconditionally a keeper — the first element of a sorted array can't be a duplicate of anything before it. So slot 0 is already correct and the next keeper belongs at index 1.

Starting at 0 instead would be wrong: `nums[k-1]` would read `nums[-1]`, the *last* element of the array, and Python won't even error — it'll silently compare against the wrong thing.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
for i in range(1, len(nums)):
```

Read from index 1 for the same reason — element 0 is already handled.
→ [range-function](../syntax/range-function.md)

```python
    if nums[i] != nums[k - 1]:
```

**The keep-test, and the heart of the solution.** `nums[k-1]` is the **last value we committed to the output**. If the current element differs from it, it's a value we haven't kept yet.

Why compare against `nums[k-1]` and not `nums[i-1]`? On this problem both happen to work, because we keep every distinct value and the read/write regions stay in lockstep. But `nums[k-1]` is the more robust framing — it asks *"does this differ from the last thing I decided to keep?"*, which stays correct if the keep-rule ever gets more complicated (as in [the "at most twice" variant](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/)). Comparing to `nums[i-1]` asks about the raw input instead, which is a coincidence of this problem rather than the principle.
→ [comparison-operators](../syntax/comparison-operators.md)

```python
        nums[k] = nums[i]
        k += 1
```

Commit it: write the keeper at the boundary, then advance the boundary.

This is safe because **`k <= i` always** — the write index never overtakes the read index, since we advance `k` at most once per loop iteration while `i` advances every iteration. When `k == i` the write is a harmless self-assignment.
→ [list-basics](../syntax/list-basics.md)

```python
return k
```

`k` finished as both the count of unique elements and the index one past the last one — the same number, which is exactly what makes this pattern tidy.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:

        if not nums:
            return 0

        k = 1

        for i in range(1, len(nums)):
            if nums[i] != nums[k - 1]:
                nums[k] = nums[i]
                k += 1

        return k
```

</details>

**Trace it** — `nums = [0,0,1,1,1,2,2,3,3,4]`:

| `i` | `nums[i]` | `nums[k-1]` | New? | Action | `k` | `nums` front |
|---|---|---|---|---|---|---|
| 1 | 0 | 0 | no | skip | 1 | `[0]` |
| 2 | 1 | 0 | ✅ | write at 1 | 2 | `[0,1]` |
| 3 | 1 | 1 | no | skip | 2 | `[0,1]` |
| 4 | 1 | 1 | no | skip | 2 | `[0,1]` |
| 5 | 2 | 1 | ✅ | write at 2 | 3 | `[0,1,2]` |
| 6 | 2 | 2 | no | skip | 3 | `[0,1,2]` |
| 7 | 3 | 2 | ✅ | write at 3 | 4 | `[0,1,2,3]` |
| 8 | 3 | 3 | no | skip | 4 | `[0,1,2,3]` |
| 9 | 4 | 3 | ✅ | write at 4 | **5** | `[0,1,2,3,4]` |

Return **5**. The tail is now `[2,2,3,3,4]` — leftover garbage, and that's explicitly fine.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

One pass, n − 1 iterations. Each does one comparison and at most one assignment — all O(1). No nested loop, no shifting, no hashing.

It's also **exactly n − 1 iterations every time** — there's no early exit and no best case. An array of all-identical values does the same number of comparisons as an all-distinct one; it just performs fewer writes.

Worth contrasting with the naive in-place attempt: deleting a duplicate with `nums.pop(i)` costs O(n) because the remaining elements shift left, so a half-duplicate array lands at **O(n²)** — roughly 4.5·10⁸ operations at n = 3·10⁴. Overwriting instead of deleting is the entire optimization.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).** Two integers, `i` and `k`. Nothing allocated regardless of input size.

This is the requirement the problem is really testing. Every "easy" alternative — a set, a filtered list comprehension, `dict.fromkeys` — is O(n) space and technically fails the brief even though it returns the right number.

The insight worth carrying forward:

> **You don't need extra space to filter a sequence in place, as long as the write pointer never overtakes the read pointer.**

That invariant (`k <= i`) is what makes reading and writing the same array safe. Every problem in the read/write family leans on it, and stating it out loud is what convinces an interviewer you understand *why* it's safe rather than having memorized the shape.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The array is sorted, so duplicates are adjacent — I don't need a set to detect them, just a comparison with the last value I kept. I'll use two pointers: a read index scanning every element, and a write index marking the end of the deduplicated region. If the current element differs from `nums[k-1]`, it's new, so I write it at `k` and advance. The write pointer never overtakes the read pointer, so overwriting in place is safe. O(n) time, O(1) space, and I return `k` as both the count and the boundary."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Allow each element **at most twice**." | [LeetCode 80](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/) — start `k = 2` and compare `nums[i] != nums[k-2]`. Same skeleton, one index changed. |
| "At most `m` times?" | Generalize: `k = m`, compare against `nums[k-m]`. The pattern scales cleanly. |
| "What if it **isn't** sorted?" | Adjacency is gone, so you need memory: a hash set of seen values, same read/write loop. O(n) time but now **O(n) space** — the sortedness was buying the O(1). |
| "Remove a *specific* value instead." | [Remove Element](27-remove-element.md) — identical structure, keep-test becomes `nums[i] != val`. |
| "Actually shrink the list." | `del nums[k:]` afterward. O(1) amortized in CPython for a tail deletion, and now `len(nums) == k`. |
| "Why not compare `nums[i]` to `nums[i-1]`?" | Works here, but it asks about the *input* rather than the *output*. Comparing to `nums[k-1]` is the version that survives generalization. |
| "Return the unique elements themselves." | `return nums[:k]` — but that's O(k) space and no longer in-place. |

**Traps:**

- **Initializing `k = 0`.** Then `nums[k-1]` is `nums[-1]` — Python's negative indexing silently reads the *last* element instead of raising. A genuinely nasty bug because it produces plausible-looking wrong answers.
- **Using `nums.pop()` or `del` inside the loop.** O(n²), and mutating a list while iterating skips elements.
- **Returning the array instead of `k`.** The signature asks for an `int`.
- **Worrying about the tail.** Beginners often try to blank or truncate everything past `k`. The problem explicitly doesn't care, and doing it is wasted work.
- **Reaching for a set out of habit.** It's the right reflex on *unsorted* input — but here it throws away the one property that makes O(1) space possible. Notice the word "sorted" and let it change your plan.

**This same move shows up in:** [Remove Element](27-remove-element.md) (same read/write skeleton, different predicate) · [Move Zeroes](283-move-zeroes.md) (write pointer plus a final fill) · [Sort Colors](75-sort-colors.md) (three pointers partitioning in place) · [Merge Sorted Array](88-merge-sorted-array.md) (in-place writing, but from the back to avoid clobbering).

</details>

---
