# 88. Merge Sorted Array

**Easy** · [LeetCode](https://leetcode.com/problems/merge-sorted-array/) · [Solution file (no hints)](../../problems/0001-0499/88.py)

[📖 02. Two Pointers lesson](../learning/02-two-pointers.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 02. Two Pointers problems](../rmap-practice/02-two-pointers.md)

---

You're given two sorted arrays `nums1` and `nums2`, plus `m` and `n` — the number of *real* elements in each. `nums1` has length `m + n`: the first `m` slots hold its values, and the last `n` are padding zeros you should ignore.

Merge them into one sorted array **stored in `nums1`**. Nothing is returned.

```
nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3   →  [1,2,2,3,5,6]
nums1 = [1],           m = 1, nums2 = [],      n = 0   →  [1]
nums1 = [0],           m = 0, nums2 = [1],     n = 1   →  [1]
```

**Constraints:** `nums1.length == m + n` · `nums2.length == n` · `0 <= m, n <= 200` · `1 <= m + n <= 200` · `-10⁹ <= nums1[i], nums2[j] <= 10⁹` · **follow-up: can you do it in O(m + n)?**

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| both arrays are **sorted** | The merge step of merge sort. You never need to compare more than the two current fronts |
| "stored **inside `nums1`**" | In-place. The interviewer is watching whether you allocate a second array |
| "`nums1` has a length of `m + n`" | **The output buffer is already the right size.** That's not a detail, it's the entire hint |
| "the last `n` elements are set to 0 and **should be ignored**" | Those slots are free real estate — writable space nobody will miss |
| "should not be returned" | Mutate the argument. Returning a new list silently fails the judge |
| `0 <= m, n` | Either array can be empty. `m = 0` and `n = 0` both have to work |
| "O(m + n)?" | Sorting afterwards is O((m+n) log(m+n)) — the follow-up is telling you that's not the answer |

The trap is that the obvious direction doesn't work. Merging **forwards** into `nums1[0]` overwrites `nums1[0]` — a value you haven't read yet. You'd be destroying your own input as you go.

🤔 **Before you open the next section:** the free space is all at the *back*. Which end of the output would you have to fill first for that to be useful, and which element do you know goes there?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Concatenate + sort | `nums1[m:] = nums2`, then `nums1.sort()` | O((m+n) log(m+n)) | O(m+n) | ⚠️ Two lines, and it works — but it throws away the sortedness you were handed |
| Copy, then merge forward | Copy `nums1[:m]` to a buffer, merge the buffer and `nums2` into `nums1` | O(m+n) | **O(m)** | ⚠️ Right complexity, but the copy is the thing the problem is asking you to avoid |
| Merge forward, in place | Write to `nums1[0]`, `nums1[1]`… | O(m+n) | O(1) | ❌ **Broken.** Each write clobbers an unread value; you'd need to shift the rest right, making it O(m·n) |
| **Merge backward, in place** | Fill from `nums1[m+n-1]` down, taking the larger of the two tails | O(m+n) | **O(1)** | ✅ |

**The decision: [two pointers](../learning/02-two-pointers.md) walking *backwards*, writing into the padding.**

The insight is a one-word change — *backwards* — and it converts a broken approach into an optimal one. Filling from the back works because **the cell you're about to write is always one you've already read, or padding.** The write pointer starts at `m + n - 1` and the read pointers start at `m - 1` and `n - 1`, so the writer is never behind either reader. It cannot catch up and clobber them.

**Why not concatenate + sort?** Say it out loud as your baseline — it's honest, it's two lines, and in production you'd probably ship it. Then note it ignores the precondition: the inputs arrive sorted, and re-sorting pays log-factor for information you already have. Interviewers ask this problem specifically to see whether you notice.

**The general move:** whenever in-place writing would destroy data you still need, check whether the *other direction* is safe. Same trick as shifting an array right, or copying overlapping memory regions.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
p1 = m - 1
p2 = n - 1
p = m + n - 1
```

Three pointers, all at the back. `p1` and `p2` read the last real element of each array; `p` is the write cursor, sitting on the final slot of `nums1`. Note `p >= p1` always — that gap is exactly the number of `nums2` elements still to be placed, and it's why the writer can't overtake the reader.
→ [variables-assignment](../syntax/variables-assignment.md) · [list-basics](../syntax/list-basics.md)

```python
while p1 >= 0 and p2 >= 0:
```

Run while **both** arrays still have something to offer. The moment one runs dry the comparison is meaningless, so the loop stops and the tail is handled separately.
→ [while-loop](../syntax/while-loop.md) · [logical-operators](../syntax/logical-operators.md)

```python
    if nums1[p1] > nums2[p2]:
        nums1[p] = nums1[p1]
        p1 -= 1
    else:
        nums1[p] = nums2[p2]
        p2 -= 1
    p -= 1
```

Take the **larger** of the two candidates and put it at the back. Going backwards means the largest remaining element is the next one placed — the mirror image of a forward merge, which takes the smaller each time.

The `else` branch catching ties (`nums1[p1] == nums2[p2]`) is fine either way: both values are equal, so either can go first and the result is identical.
→ [comparison-operators](../syntax/comparison-operators.md) · [elif-else](../syntax/elif-else.md)

```python
nums1[:p2 + 1] = nums2[:p2 + 1]
```

The leftover tail, and the line people forget. Two cases when the loop ends:

- **`p1 < 0`** — `nums1` ran out, and `nums2` still has `p2 + 1` elements. They're the smallest values in the merge, and they belong at the very front of `nums1`. Copy them there.
- **`p2 < 0`** — `nums2` ran out. Everything left in `nums1` is *already sitting in the right place*, because it never moved. Nothing to do — and this line does nothing, since `nums2[:0]` is empty.

One slice assignment covers both cases with no `if`.
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

**Trace it** — `nums1 = [1,2,3,0,0,0]`, `m = 3`, `nums2 = [2,5,6]`, `n = 3`:

| `p1` | `p2` | `p` | Compare | Write | `nums1` after |
|---|---|---|---|---|---|
| 2 | 2 | 5 | `3 > 6`? no | `nums2[2] = 6` | `[1,2,3,0,0,6]` |
| 2 | 1 | 4 | `3 > 5`? no | `nums2[1] = 5` | `[1,2,3,0,5,6]` |
| 2 | 0 | 3 | `3 > 2`? yes | `nums1[2] = 3` | `[1,2,3,3,5,6]` |
| 1 | 0 | 2 | `2 > 2`? no | `nums2[0] = 2` | `[1,2,2,3,5,6]` |
| 1 | −1 | 1 | loop ends (`p2 < 0`) | — | — |

Tail: `nums1[:0] = nums2[:0]` — a no-op. The `[1,2]` at the front never needed to move. Final: `[1,2,2,3,5,6]`. ✅

**And the other tail** — `nums1 = [0]`, `m = 0`, `nums2 = [1]`, `n = 1`: the loop never runs (`p1 = -1`), so the tail line does the work — `nums1[:1] = nums2[:1]` → `[1]`. ✅

</details>

<details>
<summary><b>4 · Time complexity</b> — O(m + n)</summary>

**O(m + n).**

- Every iteration of the loop places exactly one element and decrements `p` — so the loop body runs at most `m + n` times.
- Each iteration is one comparison, one write, two decrements: **O(1)**.
- The tail slice copies at most `n` elements: O(n).

Total **O(m + n)** — linear in the output size, which is the floor. You cannot merge two sorted arrays faster than the time it takes to write the answer.

**Compare to concatenate + sort:** O((m+n) log(m+n)). At the constraint ceiling of 200 that difference is invisible; the point isn't the runtime, it's whether you recognised that the inputs being sorted is information worth using.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1) extra.**

Three integer pointers. No buffer, no copy, no new list — the output is written into storage the caller already allocated.

This is the payoff of going backwards. The forward-merge version needs `O(m)` to stash `nums1`'s values before overwriting them; reversing direction makes that copy unnecessary, because the space you write into is space that is already logically empty.

**The one asterisk:** `nums1[:p2 + 1] = nums2[:p2 + 1]` builds a temporary slice of up to `n` elements in CPython, so a pedant would call it O(n). Write the tail as an explicit `while p2 >= 0` loop if you want a strictly O(1) answer — and say so, because noticing it is a point in your favour.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Both arrays are sorted, so this is the merge step of merge sort — but it has to be in place. Merging forward doesn't work: writing to `nums1[0]` destroys a value I haven't read. The free space is all at the end, though, so I'll merge *backwards* — three pointers, two reading the tails of each array, one writing at `m + n - 1`, taking the larger each time. The write pointer starts ahead of both readers and stays ahead, so it never clobbers unread data. When one array runs out, if it was `nums1` I copy `nums2`'s remaining head to the front; if it was `nums2` the rest is already in place. O(m + n) time, O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why not just sort?" | It works — O((m+n) log(m+n)) — but it discards the precondition. Merging uses the sortedness and hits the linear lower bound. |
| "What if `nums1` had no spare room?" | Then you need O(m) or O(n) extra space, or a new output array — in-place is only possible *because* the buffer was oversized. |
| "Merge `k` sorted arrays?" | A min-heap of the `k` current fronts → O(N log k). That's [Merge k Sorted Lists](23-merge-k-sorted-lists.md). |
| "Same thing on linked lists?" | Easier — splice nodes with a dummy head, no shifting at all. See [Merge Two Sorted Lists](21-merge-two-sorted-lists.md). |
| "Keep it stable?" | It already is, as long as ties take from `nums2` — which the `else` branch does. Flip to `>=` and equal elements swap relative order. |
| "What if `nums2` is much smaller than `nums1`?" | Still O(m + n) here. A galloping / exponential search per element gets you O(n log m), which wins when `n ≪ m`. |

**Traps:**

- **Merging forwards.** The single defining mistake of this problem. It looks natural and it corrupts the array.
- **Forgetting the leftover `nums2` tail.** `nums1 = [0], m = 0, nums2 = [1], n = 1` fails instantly without it — the loop body never runs.
- **"Forgetting" the leftover `nums1` tail.** There's nothing to forget; those elements are already home. Copying them anyway is harmless but shows you haven't reasoned it through.
- **Using `len(nums1)` instead of `m`.** `len(nums1)` is `m + n` — it counts the padding zeros as data.
- **Returning `nums1`.** The signature says `-> None`. Mutate.

**This same move shows up in:** [Merge Two Sorted Lists](21-merge-two-sorted-lists.md) (the same merge, on nodes) · [Merge k Sorted Lists](23-merge-k-sorted-lists.md) (the k-way generalisation) · [Sorting](../learning/06b-sorting.md) (merge sort's combine step, which this *is*) · [Remove Nth Node From End of List](19-remove-nth-node-from-end-of-list.md) (another problem solved by attacking from the back).

</details>

---
