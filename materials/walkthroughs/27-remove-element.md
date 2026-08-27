# 27. Remove Element

**Easy** · [LeetCode](https://leetcode.com/problems/remove-element/) · [Solution file (no hints)](../../problems/0001-0499/27.py)

[📖 01. Arrays & Hashing lesson](../learning/01-arrays-hashing.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 01. Arrays & Hashing problems](../rmap-practice/01-arrays-hashing.md)

---

Given an integer array `nums` and an integer `val`, remove **all occurrences** of `val` in-place. Return `k`, the number of remaining elements — the first `k` slots of `nums` must hold them (in any order), and what lies beyond `k` doesn't matter.

```
nums = [3,2,2,3], val = 3           →  k = 2,  nums = [2,2,_,_]
nums = [0,1,2,2,3,0,4,2], val = 2   →  k = 5,  nums = [0,1,3,0,4,_,_,_]
```

**Constraints:** `0 <= nums.length <= 100` · `0 <= nums[i] <= 50` · `0 <= val <= 100`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "remove **all occurrences**" | Not just the first. Every match goes |
| "**in-place**" | O(1) extra space — overwrite `nums`, don't build and copy back |
| "return `k`" | The count of survivors. LeetCode reads `nums[0..k-1]` |
| "**in any order**" | ⚠️ Notably *weaker* than [problem 26](26-remove-duplicates-from-sorted-array.md), which demanded relative order. This permits a second, cheaper trick |
| "beyond `k` doesn't matter" | No deleting, shifting, or blanking required — just make the front right |
| `nums.length` can be **0** | Empty input must return 0 without crashing |
| nothing about sortedness | Input is arbitrary — but you don't care, since the test is against `val`, not against neighbours |

This is [Remove Duplicates](26-remove-duplicates-from-sorted-array.md) with a **simpler** keep-test. There the question was "does this differ from the last thing I kept?" — a question about the array's history. Here it's "does this differ from `val`?" — a question about one element in isolation, needing no memory or context at all.

But look again at "in any order." That permission is doing real work, and it's the difference between the two solutions below.

🤔 **Before you open the next section:** if order doesn't matter and you find a `val` at the front, is there anything cheaper you could do than shifting everything left — or than scanning forward?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| `.remove()` in a loop | Repeatedly call `nums.remove(val)` | O(n²) | O(1) | ❌ Each removal shifts the tail |
| List comprehension | `nums = [x for x in nums if x != val]` | O(n) | O(n) | ❌ Rebinds a local name — the caller's array is untouched |
| **Two pointers (read + write)** | Read scans; write index places keepers at the front | **O(n)** | **O(1)** | ✅ Order-preserving, always n reads |
| Swap-from-the-end | On a match, overwrite it with the last element and shrink | **O(n)** | **O(1)** | ✅ Fewer writes when matches are rare |

**The decision: two pointers — read index `i`, write index `k`.** Same skeleton as problem 26, and the one to write by default.

- **`i` (read)** — visits every element once, asking "keeper?"
- **`k` (write)** — the boundary of the finished region. `nums[0..k-1]` holds the survivors; `k` is where the next one goes.

Safe for exactly the same reason: **`k <= i` always**, because `k` advances at most once per iteration while `i` advances every iteration. You can never overwrite something you haven't already read.

**The alternative worth knowing — swap-from-the-end.** Because order is free, you can handle a match by *stealing the last element*:

```python
k = len(nums)
i = 0
while i < k:
    if nums[i] == val:
        nums[i] = nums[k - 1]   # steal from the back
        k -= 1                  # shrink the live region
    else:
        i += 1                  # only advance on a keeper
```

Don't advance `i` after a steal — the element you just pulled in is unexamined and might itself be `val`.

**When does that win?** When matches are **rare**. The two-pointer version performs a write for every *keeper* (n writes when nothing matches); the swap version performs a write for every *match* (0 writes when nothing matches). If `val` appears twice in a million-element array, one does ~10⁶ writes and the other does 2.

**When does it lose?** When matches are common, and — more importantly — it **scrambles the order**. Problem 26 could not have used it. Reach for it only when the problem hands you "in any order," and say that's why.

**Why not the list comprehension?** In Python, `nums = [...]` rebinds the local parameter name; the caller's list object is unchanged, so LeetCode sees nothing. `nums[:] = [...]` *does* mutate in place — but it builds the full temporary list first, so it's O(n) space and fails the in-place requirement in spirit.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
k = 0
```

**Start at 0 — and note the contrast with problem 26, which started at 1.** There, `nums[0]` was guaranteed a keeper (the first element of a sorted array can't duplicate anything before it). Here `nums[0]` might well *be* `val`, so nothing is pre-committed and the output region starts empty.

The starting value follows from *how many elements you already know belong in the answer*. Reason it out each time rather than memorizing a number.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
for i in range(len(nums)):
```

From 0 — every element needs testing, including the first. (Problem 26 could skip index 0; this one can't.)
→ [range-function](../syntax/range-function.md)

```python
    if nums[i] != val:
```

**The keep-test, in its simplest possible form.** No neighbour comparison, no set lookup, no state — just "is this element something other than the thing we're deleting?"

This is why the problem is easier than it looks: the predicate is *context-free*. Everything else is the same in-place-filter machinery you already know.
→ [comparison-operators](../syntax/comparison-operators.md)

```python
        nums[k] = nums[i]
        k += 1
```

Commit the keeper at the boundary, then advance the boundary. When `k == i` (no match seen yet) this is a self-assignment — wasteful in theory, harmless in practice, and not worth guarding against.
→ [list-basics](../syntax/list-basics.md)

```python
return k
```

The count of survivors, which is also the index one past the last one.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:

        k = 0

        for i in range(len(nums)):
            if nums[i] != val:
                nums[k] = nums[i]
                k += 1

        return k
```

</details>

**Trace it** — `nums = [0,1,2,2,3,0,4,2]`, `val = 2`:

| `i` | `nums[i]` | Keep? | Action | `k` | `nums` front |
|---|---|---|---|---|---|
| 0 | 0 | ✅ | write at 0 | 1 | `[0]` |
| 1 | 1 | ✅ | write at 1 | 2 | `[0,1]` |
| 2 | 2 | ❌ | skip | 2 | `[0,1]` |
| 3 | 2 | ❌ | skip | 2 | `[0,1]` |
| 4 | 3 | ✅ | write at 2 | 3 | `[0,1,3]` |
| 5 | 0 | ✅ | write at 3 | 4 | `[0,1,3,0]` |
| 6 | 4 | ✅ | write at 4 | **5** | `[0,1,3,0,4]` |
| 7 | 2 | ❌ | skip | 5 | `[0,1,3,0,4]` |

Return **5**. Watch `k` fall behind `i` at the first match and stay behind — that gap is exactly the number of elements removed so far.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

Exactly n iterations, each doing one comparison and at most one assignment. No nesting, no shifting, no early exit — the cost is the same whether every element matches or none do.

**Contrast with the naive approach:** `nums.remove(val)` is O(n) on its own (it scans to find the value, then shifts the tail left). Calling it once per occurrence gives **O(n²)**. With n ≤ 100 here that's harmless, but the habit isn't — the same instinct on a 10⁵-element array is a timeout.

**The swap-from-the-end variant is also O(n)**, but with a different write profile: n writes for the two-pointer version in the no-match case versus 0 for the swap version. Same complexity class, meaningfully different constants when matches are sparse.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).** Two integers, `i` and `k`, regardless of input size.

Both the list comprehension and a filtered copy are O(n) and fail the in-place requirement — and the comprehension has the extra Python gotcha of not mutating the caller's list at all:

```python
nums = [x for x in nums if x != val]   # ❌ rebinds the local name only
nums[:] = [x for x in nums if x != val] # ⚠️ mutates, but O(n) temp space
```

The first is a *correctness* bug in this context, not just an efficiency one — it's worth understanding the difference between rebinding a name and mutating an object, because it bites people well beyond LeetCode. See [list-slicing](../syntax/list-slicing.md).

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "In-place filter, so two pointers: a read index over every element and a write index marking the end of the kept region. If the element isn't `val`, I write it at `k` and advance `k`. The write pointer can't overtake the read pointer, so it's safe to overwrite as I go. O(n) time, O(1) space, return `k`. Since the problem says order doesn't matter, there's also a swap-from-the-end variant that overwrites each match with the last live element — same complexity but far fewer writes when `val` is rare."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Can you minimize the number of **writes**?" | **The follow-up this problem exists for.** Swap-from-the-end: on a match, copy `nums[k-1]` over it and shrink `k`, without advancing `i`. Writes ∝ matches, not ∝ keepers. |
| "What if order **must** be preserved?" | Then the swap trick is out — use the two-pointer version, which is naturally stable. |
| "Remove duplicates instead." | [Remove Duplicates from Sorted Array](26-remove-duplicates-from-sorted-array.md) — same skeleton, keep-test becomes `nums[i] != nums[k-1]`. |
| "Remove all values in a **set**?" | `if nums[i] not in remove_set` — O(1) average per test, still O(n) overall. |
| "Move all `val`s to the end instead of discarding them." | [Move Zeroes](283-move-zeroes.md) — same write pass, then fill `nums[k:]` with `val`. |
| "Actually shrink the list." | `del nums[k:]` afterward. |
| "Why doesn't the list comprehension work?" | `nums = [...]` rebinds a local name; the caller's object is untouched. `nums[:] = [...]` mutates but costs O(n) space. |

**Traps:**

- **Advancing `i` after a swap-from-the-end.** The stolen element is unexamined and may itself be `val`. This is *the* bug in the swap variant — use `while` with a manual increment, not `for`.
- **Reassigning `nums` instead of mutating it.** Returns the right `k` while leaving the caller's array untouched. Passes a naive local test, fails the judge.
- **`.remove()` in a loop.** O(n²), and it raises `ValueError` once no occurrences remain.
- **Starting `k = 1`** by pattern-matching off problem 26. There, index 0 was a guaranteed keeper; here it isn't. Derive the initial value, don't copy it.
- **Mutating while iterating.** `for x in nums: nums.remove(x)` skips elements — the classic Python trap.

**This same move shows up in:** [Remove Duplicates from Sorted Array](26-remove-duplicates-from-sorted-array.md) (identical skeleton, richer predicate) · [Move Zeroes](283-move-zeroes.md) (write pass plus a fill pass) · [Sort Colors](75-sort-colors.md) (three-way in-place partition — the Dutch national flag) · [Merge Sorted Array](88-merge-sorted-array.md) (in-place writing from the back).

</details>

---
