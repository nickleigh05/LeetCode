# 283. Move Zeroes

**Easy** · [LeetCode](https://leetcode.com/problems/move-zeroes/) · [Solution file (no hints)](../../problems/0001-0499/283.py)

[📖 02. Two Pointers lesson](../learning/02-two-pointers.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 02. Two Pointers problems](../rmap-practice/02-two-pointers.md)

---

Given an integer array `nums`, move all `0`s to the **end** while maintaining the **relative order** of the non-zero elements. Do this **in-place** without making a copy.

```
nums = [0,1,0,3,12]  →  [1,3,12,0,0]
nums = [0]           →  [0]
```

**Constraints:** `1 <= nums.length <= 10⁴` · `-2³¹ <= nums[i] <= 2³¹ - 1`

**Follow-up:** minimize the total number of operations.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "maintain **relative order**" | ⚠️ **Stability required.** This is the constraint that rules out the cheap swap-with-the-end trick from [Remove Element](27-remove-element.md) |
| "move `0`s to the **end**" | Not delete — they stay in the array, just relocated |
| "**in-place**, without a copy" | O(1) extra space |
| "minimize **operations**" (follow-up) | A hint that there's a version doing fewer writes than the obvious one |
| `n` up to 10⁴ | Small; any O(n) approach is comfortable |
| values can be negative | `0` is a specific value, not "falsy-ish" — but note `-0 == 0` isn't a concern for ints |

The reframe that makes it easy: don't think about *moving zeroes*. Think about **compacting the non-zeroes to the front** — the zeroes then end up at the back automatically, because they're whatever's left over.

That turns it into the same in-place filter you already know from [Remove Element](27-remove-element.md), with `nums[i] != 0` as the keep-test — plus one extra step to fill the tail.

The order requirement is what forces the *stable* version. Compare:

| | Order preserved? | Writes |
|---|---|---|
| Compact + fill | ✅ | one per element |
| Swap with the end | ❌ | one per zero |

Here you must take the first.

🤔 **Before you open the next section:** if you slid every non-zero element to the front in order, what must be sitting in all the remaining slots?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Build a new list | Non-zeroes, then pad with zeroes, copy back | O(n) | **O(n)** | ❌ Violates in-place |
| `.remove(0)` + append | Delete each zero, append at the end | O(n²) | O(1) | ❌ Each removal shifts the tail |
| Bubble zeroes backward | Repeatedly swap adjacent pairs | O(n²) | O(1) | ❌ Quadratic |
| **Two passes: compact, then fill** | Write non-zeroes to the front, zero out the rest | **O(n)** | **O(1)** | ✅ Clearest |
| **One pass: swap on non-zero** | Swap each non-zero into the write slot | **O(n)** | **O(1)** | ✅ Fewer writes |

**Both good options are in the solution file, and the difference between them is the follow-up.**

**The swap version (primary).** Keep `lastNonZeroFoundAt` — the index where the next non-zero belongs. Scan with `cur`; whenever `nums[cur]` is non-zero, **swap** it into the write slot and advance.

Why does swapping do the right thing? Everything between the write index and `cur` is guaranteed to be zeroes (they're the elements the scan passed over without writing). So swapping sends the non-zero forward *and* pushes a zero backward into the vacated slot — both halves of the job in one operation, with order preserved.

**The two-pass version.** Copy non-zeroes forward (overwriting, not swapping), then fill everything from the write index onward with `0`. Slightly easier to reason about, and it's the same skeleton as [Remove Element](27-remove-element.md) with a fill step appended.

**Which minimizes operations?** The swap version, in most cases:

| | Writes when there are `z` zeroes and `k` non-zeroes |
|---|---|
| Two-pass | `k` copies + `z` fills = **n** |
| Swap | `k` swaps (2 writes each, but only when `cur != write`) |

If the array has no zeroes at all, the swap version's condition `cur == lastNonZeroFoundAt` means every "swap" is a self-swap — Python still performs the writes, but a language with an explicit guard would skip them entirely. The genuinely minimal version adds `if cur != lastNonZeroFoundAt` before swapping.

**Why swap-with-the-end is wrong here.** In [Remove Element](27-remove-element.md), order was explicitly free, so you could overwrite a match with the last element. Here order is required, and that trick scrambles it. Same family of problems, opposite answer — driven entirely by one line of the statement.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

**Approach A — one pass with swaps** (the primary)

```python
lastNonZeroFoundAt = 0
```

The write boundary: `nums[0 .. lastNonZeroFoundAt-1]` holds the non-zeroes found so far, in order. Starting at 0 because nothing is placed yet.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
for cur in range(len(nums)):
    if nums[cur] != 0:
```

Scan every element; act only on non-zeroes. Zeroes are simply passed over — they'll be handled implicitly by the swaps.
→ [for-loop](../syntax/for-loop.md)

```python
        nums[lastNonZeroFoundAt], nums[cur] = nums[cur], nums[lastNonZeroFoundAt]
        lastNonZeroFoundAt += 1
```

**The swap, and why it preserves order.** Everything strictly between `lastNonZeroFoundAt` and `cur` is a zero (the scan skipped them). So this swap:

- moves the non-zero **forward** into the write slot, and
- moves a **zero backward** into the slot `cur` just vacated.

Non-zeroes are written in the order encountered, so relative order holds. When `lastNonZeroFoundAt == cur` (no zeroes seen yet), it's a self-swap — harmless.
→ [swap-tuple-assign](../syntax/swap-tuple-assign.md)

<details>
<summary>Approach A together</summary>

```python
class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        lastNonZeroFoundAt = 0

        for cur in range(len(nums)):
            if nums[cur] != 0:
                nums[lastNonZeroFoundAt], nums[cur] = nums[cur], nums[lastNonZeroFoundAt]
                lastNonZeroFoundAt += 1
```

</details>

---

**Approach B — two passes: compact then fill**

```python
write_idx = 0
for read_idx in range(len(nums)):
    if nums[read_idx] != 0:
        nums[write_idx] = nums[read_idx]
        write_idx += 1
```

Pass 1 — identical to [Remove Element](27-remove-element.md): copy every keeper to the front. Safe because `write_idx <= read_idx` always.

```python
for i in range(write_idx, len(nums)):
    nums[i] = 0
```

Pass 2 — everything from `write_idx` onward is leftover garbage (duplicated values from the compaction), so overwrite it all with zeroes. The count is automatically right: `n - write_idx` equals the number of zeroes removed.
→ [range-function](../syntax/range-function.md)

<details>
<summary>Approach B together</summary>

```python
### Two passes and overwrite ###
class Solution:
    def moveZeroes(self, nums: List[int]) -> None:

        write_idx = 0
        for read_idx in range(len(nums)):
            if nums[read_idx] != 0:
                nums[write_idx] = nums[read_idx]
                write_idx += 1

        for i in range(write_idx, len(nums)):
            nums[i] = 0
```

</details>

**Trace approach A** — `nums = [0, 1, 0, 3, 12]`:

| `cur` | `nums[cur]` | Non-zero? | `write` before | Swap | `nums` after | `write` after |
|---|---|---|---|---|---|---|
| 0 | 0 | no | 0 | — | `[0,1,0,3,12]` | 0 |
| 1 | 1 | ✅ | 0 | idx 0 ↔ 1 | `[1,0,0,3,12]` | 1 |
| 2 | 0 | no | 1 | — | `[1,0,0,3,12]` | 1 |
| 3 | 3 | ✅ | 1 | idx 1 ↔ 3 | `[1,3,0,0,12]` | 2 |
| 4 | 12 | ✅ | 2 | idx 2 ↔ 4 | `[1,3,12,0,0]` | 3 |

Result `[1,3,12,0,0]` ✅ — and notice `1`, `3`, `12` appear in their original relative order, which is the whole requirement.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** for both approaches.

- **Approach A:** one pass, n iterations, each O(1).
- **Approach B:** two passes — n for the compaction and at most n for the fill — so 2n, still O(n).

**On the "minimize operations" follow-up:** both are O(n) *time*, but they differ in **writes**, which is what the follow-up is really asking about.

| Array | Approach A writes | Approach B writes |
|---|---|---|
| No zeroes, `[1,2,3]` | 3 self-swaps (6 writes, or 0 with a guard) | 3 copies + 0 fills = 3 |
| All zeroes, `[0,0,0]` | 0 | 0 copies + 3 fills = 3 |
| Mixed, `[0,1,0,3,12]` | 3 swaps = 6 writes | 3 copies + 2 fills = 5 |

The genuinely minimal version guards the self-swap:

```python
if cur != lastNonZeroFoundAt:
    nums[lastNonZeroFoundAt], nums[cur] = nums[cur], nums[lastNonZeroFoundAt]
```

Now a zero-free array does **no writes at all**. That's the answer the follow-up is fishing for — say it even if you don't code it.

**Compare to the naive `.remove(0)` loop:** O(n²), because each removal shifts the tail. At n = 10⁴ that's 10⁸ — slow, and needless.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).** One or two integer indices; the tuple swap is a constant-size transient.

The problem explicitly forbids a copy, which rules out the natural Python one-liners:

```python
nums = [x for x in nums if x != 0] + [0] * nums.count(0)   # ❌ rebinds; caller unaffected
nums[:] = [x for x in nums if x != 0] + [0] * nums.count(0) # ⚠️ mutates, but O(n) temp
```

The second genuinely modifies the caller's list, but builds the whole replacement first — O(n) space, failing the brief. It's the same rebind-vs-mutate distinction that matters in [Remove Element](27-remove-element.md), and worth understanding once properly.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Rather than moving zeroes, I'll compact the non-zeroes to the front — the zeroes end up at the back for free. I keep a write index for where the next non-zero belongs, and scan with a read index. When I hit a non-zero I swap it into the write slot and advance. Everything between the two indices is guaranteed to be zeroes, so the swap simultaneously pushes a zero backward — and since I write non-zeroes in the order I meet them, relative order is preserved. O(n) time, O(1) space. To minimize writes I'd guard the swap with `cur != write`, so a zero-free array does no writes at all."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Minimize the number of operations." | Guard the self-swap with `if cur != write`. Zero-free input then costs zero writes. |
| "What if order **didn't** matter?" | Swap each zero with the last live element and shrink a boundary — writes proportional to the number of zeroes. Exactly [Remove Element](27-remove-element.md). |
| "Move zeroes to the **front** instead." | Mirror it: scan from the right with a write index starting at `n-1`. |
| "Move all instances of `val`, not just 0." | Same code, `nums[cur] != val`. |
| "Why is the swap version stable?" | Non-zeroes are written in encounter order, and the swap only ever exchanges a non-zero with a zero from the skipped region. |
| "Group by a predicate into three regions?" | That's the Dutch national flag — [Sort Colors](75-sort-colors.md). |
| "Can you do it in one pass with no swaps?" | Yes, if you accept the fill: copy forward, then zero the tail. That's Approach B — one pass plus a fill. |

**Traps:**

- **Swapping with the last element.** Fast, but destroys relative order — the one thing this problem requires. It's the correct move in [Remove Element](27-remove-element.md) and wrong here; read the statement.
- **Forgetting the fill in Approach B.** The tail keeps duplicated leftovers, e.g. `[1,3,12,3,12]`.
- **`nums.remove(0)` in a loop.** O(n²), and mutating while iterating skips elements.
- **Rebinding `nums`.** The caller's array is unchanged; the judge reports failure.
- **Advancing the write index on zeroes.** It must only advance when something is written, or the boundary loses meaning.
- **Returning the array.** The signature returns `None`.

**This same move shows up in:** [Remove Element](27-remove-element.md) (the same read/write compaction, with order explicitly free) · [Remove Duplicates from Sorted Array](26-remove-duplicates-from-sorted-array.md) (same skeleton, neighbour-based predicate) · [Sort Colors](75-sort-colors.md) (three-region in-place partition) · [Merge Sorted Array](88-merge-sorted-array.md) (in-place writing with a pointer invariant).

</details>

---
