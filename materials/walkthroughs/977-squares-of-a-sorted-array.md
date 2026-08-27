# 977. Squares of a Sorted Array

**Easy** · [LeetCode](https://leetcode.com/problems/squares-of-a-sorted-array/) · [Solution file (no hints)](../../problems/0500-0999/977.py)

[📖 02. Two Pointers lesson](../learning/02-two-pointers.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 02. Two Pointers problems](../rmap-practice/02-two-pointers.md)

---

Given an integer array `nums` sorted in **non-decreasing order**, return an array of the **squares** of each number, also sorted in non-decreasing order.

```
nums = [-4,-1,0,3,10]   →  [0,1,9,16,100]
nums = [-7,-3,2,3,11]   →  [4,9,9,49,121]
```

**Constraints:** `1 <= nums.length <= 10⁴` · `-10⁴ <= nums[i] <= 10⁴` · `nums` is sorted non-decreasing

**Follow-up:** an O(n) solution exists — can you find it?

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| input is **sorted** | Free structure — and the whole point is that squaring *partially* destroys it |
| values can be **negative** | ⚠️ The crux. `(-4)² = 16 > 3² = 9`, so squaring reverses the order of the negative half |
| output must be **sorted** | You must restore order — the question is whether you re-sort or exploit what's left |
| follow-up says **O(n) exists** | An explicit nudge away from the obvious sort-based answer |
| `n` up to 10⁴ | Both O(n log n) and O(n) pass comfortably; the follow-up is about insight, not speed |

**What squaring actually does to a sorted array** — picture it:

```
nums:     [-4, -1,  0,  3, 10]      sorted ascending
squares:  [16,  1,  0,  9, 100]     NOT sorted
           └────┬────┘  └──┬──┘
        decreasing      increasing
```

The negatives, squared, come out in **decreasing** order. The non-negatives, squared, stay **increasing**. So the result isn't unsorted chaos — it's **two sorted runs pointed in opposite directions**, meeting at the value closest to zero.

That's exactly a merge problem. And there's a second observation that makes it even simpler:

> **The largest square is always at one of the two ends** — either the most negative number or the most positive one. Never in the middle.

So instead of finding where the runs meet and merging outward, you can start at both ends and repeatedly take the bigger square, filling the result **from the back**.

🤔 **Before you open the next section:** if the biggest square is always at one end or the other, and you fill the answer from its last slot backward, what do you need to compare at each step?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Square then sort | `sorted(x*x for x in nums)` | O(n log n) | O(n) | ⚠️ Correct, one line — but ignores the sortedness |
| Find the pivot, merge outward | Locate the zero-crossing, merge the two runs | O(n) | O(n) | ✅ Correct, but the pivot search is fiddly |
| **Two pointers, fill from the back** | Compare `|left|` vs `|right|`, write the larger at the end | **O(n)** | O(n) | ✅ |
| Two pointers, fill from the front | Would need the *smallest* square each step | O(n) | O(n) | ⚠️ Harder — the minimum is in the middle, not at an end |

**The decision: two pointers at the ends, writing the result backward.**

- `left = 0`, `right = n - 1` — the two candidates for the largest square
- `pos = n - 1` — where the next-largest value goes
- Compare `abs(nums[left])` against `abs(nums[right])`, square the winner, write it at `pos`, and step that pointer inward

**Why fill backward and not forward?** Because the **largest** element is easy to find (it's at one end) and the **smallest** is hard (it's wherever the array crosses zero, which you'd have to search for). Producing the answer largest-first lets you always pick between exactly two candidates. Trying to build it smallest-first means finding the zero-crossing pivot before you start.

This is the same reasoning as [Merge Sorted Array](88-merge-sorted-array.md) — *"fill from the end, because that's where the easy-to-identify elements go."*

**Why compare absolute values?** Squaring is monotonic in magnitude: `|a| > |b|` ⟺ `a² > b²`. So comparing `abs` tells you which square is larger without computing either. (You could compare `nums[left]**2 > nums[right]**2` directly — same result, marginally more arithmetic.)

**Why not just sort?** `sorted(x*x for x in nums)` is genuinely fine, one line, and passes. Say it as your baseline — but the follow-up explicitly asks for O(n), and the sorted input is being handed to you for a reason. Paying `log n` to re-derive order you were given is the inefficiency this problem is built around.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
left = 0
right = len(nums) - 1
pos = len(nums) - 1
result = [0] * len(nums)
```

Three indices and a pre-sized output.

- `left` / `right` — the two candidates for the largest remaining square
- `pos` — the write position, starting at the **last** slot and moving backward
- `result` — preallocated to length `n`, so we can write to any index directly

Preallocating (rather than appending and reversing) is what lets us fill back-to-front naturally.
→ [list-basics](../syntax/list-basics.md)

```python
while left <= right:
```

`<=`, not `<` — when the two pointers land on the same element, that element still needs to be placed. Using `<` drops the final value and leaves a `0` in the result.
→ [while-loop](../syntax/while-loop.md)

```python
    if abs(nums[left]) > abs(nums[right]):
        result[pos] = nums[left] ** 2
        left += 1
    else:
        result[pos] = nums[right] ** 2
        right -= 1
```

**The core comparison.** Whichever end has the larger *magnitude* produces the larger square, so it claims the highest unfilled slot.

The `else` handles ties (`abs` equal, as in `[-3, 3]`) by taking from the right — arbitrary but fine, since the squares are identical.

Each branch advances **only its own pointer**, shrinking the live range by exactly one element per iteration.
→ [math-module-basics](../syntax/math-module-basics.md) · [arithmetic-operators](../syntax/arithmetic-operators.md) · [elif-else](../syntax/elif-else.md)

```python
    pos -= 1
```

Outside the branch — every iteration fills exactly one slot regardless of which side won.

```python
return result
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:

        left = 0
        right = len(nums) - 1
        pos = len(nums) - 1
        result = [0] * len(nums)

        while left <= right:
            if abs(nums[left]) > abs(nums[right]):
                result[pos] = nums[left] ** 2
                left += 1
            else:
                result[pos] = nums[right] ** 2
                right -= 1
            pos -= 1

        return result
```

</details>

**Trace it** — `nums = [-4, -1, 0, 3, 10]`:

| `left` | `right` | `abs(L)` vs `abs(R)` | Winner | `pos` | `result` |
|---|---|---|---|---|---|
| 0 | 4 | 4 vs **10** | right → 100 | 4 | `[_,_,_,_,100]` |
| 0 | 3 | **4** vs 3 | left → 16 | 3 | `[_,_,_,16,100]` |
| 1 | 3 | 1 vs **3** | right → 9 | 2 | `[_,_,9,16,100]` |
| 1 | 2 | **1** vs 0 | left → 1 | 1 | `[_,1,9,16,100]` |
| 2 | 2 | 0 vs 0 | right → 0 | 0 | `[0,1,9,16,100]` |
| 3 | 2 | `left > right` → stop | — | — | — |

Result `[0,1,9,16,100]` ✅

The last row is why the condition must be `<=`: with `<`, the loop would exit before placing `nums[2] = 0`, leaving `result[0]` as the initial `0` — which happens to be correct *here*, but would be wrong on `[-4,-1,5,3,10]`-style inputs where the middle element isn't zero. Test with a non-zero middle to catch it.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

Each iteration retires exactly one element (either `left` advances or `right` retreats), and the range starts with `n` elements — so the loop runs exactly `n` times, each doing O(1) work.

No sorting, no nested loops, no searching for a pivot.

**Compare to the sort-based version:** O(n log n). Both pass at n = 10⁴, but the two-pointer version is what the follow-up wants, and the reasoning behind it — *"squaring produces two sorted runs, so merge them"* — is the transferable idea.

This is **optimal**: you must produce n outputs, so Ω(n) is a floor.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** for the result array — and it's **unavoidable**, since the problem asks you to *return* a new array of n squares.

**O(1) auxiliary**, if you count only what's used beyond the required output: three integer indices.

**Could you square in place?** If mutating the input were allowed, you could write squares into `nums` itself — but not with this algorithm, because filling from the back would overwrite `nums[right]` before you read it. (Contrast [Merge Sorted Array](88-merge-sorted-array.md), where the padding at the end makes exactly that safe.) You'd need to square everything first, then run an in-place merge of the two runs — considerably more work for no asymptotic gain.

| | Time | Space |
|---|---|---|
| Square + sort | O(n log n) | O(n) |
| **Two pointers** | **O(n)** | O(n) (output only) |

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Squaring breaks the sort because negatives flip — `(-4)²` beats `3²`. But it doesn't produce chaos: the squared negatives are decreasing and the squared non-negatives are increasing, so it's two sorted runs meeting near zero. That means the largest square is always at one of the two ends. So I use two pointers at the ends, compare absolute values, and write the larger square into the result from the **back** forward. Filling backward is the trick — the maximum is easy to find at an end, whereas the minimum is somewhere in the middle. O(n) time, O(n) for the output. The one-line `sorted(x*x for x in nums)` also works but is O(n log n) and throws away the sortedness."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why fill from the back?" | **The key question.** The largest square is always at an end; the smallest is at the zero-crossing, which you'd have to search for. |
| "Why compare `abs` instead of squaring?" | Squaring is monotonic in magnitude, so `|a| > |b| ⟺ a² > b²`. Avoids two multiplications per comparison. |
| "What if the array were all non-negative?" | Already sorted after squaring — just map and return. O(n), no pointers needed. |
| "What if it were unsorted?" | The structure is gone; you'd have to sort. O(n log n) is then optimal. |
| "Cubes instead of squares?" | Cubing **preserves** sign and order, so the array stays sorted. Just map it. |
| "Can you do it in place?" | Not with this algorithm — backward filling would clobber unread values. You'd square first, then merge the two runs in place. |
| "What about overflow?" | Not in Python. In C++/Java, `10⁴² = 10⁸` fits comfortably in `int32`. |

**Traps:**

- **Using `while left < right`.** Drops the final element — the one where the pointers meet. Test an odd-length array with a non-zero middle.
- **Filling from the front.** You'd need the *smallest* square each step, which isn't at either end. It leads to a much messier pivot search.
- **Forgetting `abs`** and comparing raw values. `-4 > 3` is false, so you'd pick wrongly on exactly the inputs that matter.
- **Appending to an empty list.** You'd build it in descending order and need a final reverse — correct but an extra pass. Preallocate and index.
- **Decrementing `pos` inside both branches.** Works, but duplicating it invites drift. Put it once at the bottom.
- **Assuming a zero exists.** `[-5,-3,-1]` has no zero-crossing element; the algorithm handles it without caring.

**This same move shows up in:** [Merge Sorted Array](88-merge-sorted-array.md) (fill from the back for exactly the same reason) · [Two Sum II](167-two-sum-ii-input-array-is-sorted.md) (converging pointers on a sorted array) · [Valid Palindrome](125-valid-palindrome.md) (converging pointers, comparing ends) · [Sort Colors](75-sort-colors.md) (partitioning with pointers from both ends).

</details>

---
