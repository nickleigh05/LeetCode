# 31. Next Permutation

**Medium** · [LeetCode](https://leetcode.com/problems/next-permutation/) · [Solution file (no hints)](../../problems/0001-0499/31.py)

[📖 02. Two Pointers lesson](../learning/02-two-pointers.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 02. Two Pointers problems](../rmap-practice/02-two-pointers.md)

---

The **next permutation** of an array is the next arrangement of its numbers in **lexicographic (dictionary) order**. If the array is already the largest arrangement, wrap around to the smallest one, which is sorted ascending.

Rearrange `nums` into its next permutation **in place**, using only constant extra memory.

```
nums = [1,2,3]  →  [1,3,2]
nums = [3,2,1]  →  [1,2,3]      (largest, so wrap to smallest)
nums = [1,1,5]  →  [1,5,1]
nums = [1,3,2]  →  [2,1,3]
```

**Constraints:** `1 <= nums.length <= 100` · `0 <= nums[i] <= 100`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**next**" in lexicographic order | The *smallest* arrangement that's *strictly bigger*. Not just any bigger one |
| largest → smallest | A descending array wraps to ascending |
| **in place**, constant memory | You can't generate all permutations or build a new list |
| duplicates allowed (`[1,1,5]`) | Comparisons must handle equal values, which means `>=` and `<=`, not `>` and `<` |

**Think of it like counting.** Going from 1299 to 1300, the digits on the right are "maxed out" (99), so you increase the first digit you *can* (2 → 3) and reset everything after it to the smallest possible (00). The next permutation works the same way.

**Step 1: find what's maxed out.** Read from the right. A **descending** suffix is already the largest arrangement of those numbers. Nothing inside it can be rearranged to make a bigger number. So find the first position `i`, from the right, where `nums[i] < nums[i + 1]`. That's the rightmost number that can still be increased. It's called the **pivot**.

**Step 2: increase it by as little as possible.** Swap the pivot with the **smallest number in the suffix that's bigger than it**. The suffix is descending, so scanning from the right end, the first number bigger than the pivot is that one.

**Step 3: reset the suffix to its smallest arrangement.** After the swap, the suffix is *still descending* (the swap didn't break its order). Its smallest arrangement is ascending, and reversing a descending list makes it ascending. So **reverse** it.

**The wrap-around case comes free.** If the whole array is descending, there's no pivot (`i` falls to −1). Skip the swap and reverse everything, which gives the smallest arrangement.

🤔 **Before you open the next section:** in `[1, 5, 8, 4, 7, 6, 5, 3, 1]`, where is the pivot, what does it swap with, and what does the suffix look like afterwards?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Generate all permutations | Sort them, find the current one, take the next | O(n! · n) | O(n!) | ❌ Hopeless, and not in place |
| `itertools.permutations` | Same idea with a library | O(n!) | — | ❌ Same problem |
| **Pivot, swap, reverse** | Find pivot from the right, swap with next-larger, reverse suffix | **O(n)** | **O(1)** | ✅ |

**The decision: the classic three-step algorithm**, using [two pointers](../learning/02-two-pointers.md) for the reverse.

Each step is a linear scan or a two-pointer reverse, and nothing beyond a few indices is stored. It's an old algorithm (it goes back to 14th-century India), and C++'s `std::next_permutation` uses it.

**Why the swap keeps the suffix descending.** The swapped-in value `nums[j]` was the smallest suffix value bigger than the pivot. Everything to its left in the suffix is ≥ it, and everything to its right is ≤ the pivot. Putting the pivot into slot `j` keeps that order, so the suffix is still descending and a reverse is all you need. A full sort would also work, at O(n log n).

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
n = len(nums)

i = n - 2
while i >= 0 and nums[i] >= nums[i + 1]:
    i -= 1
```

**Find the pivot.** Start at the second-to-last position and move left while the pair is non-increasing. The loop stops at the first `i` where `nums[i] < nums[i + 1]`, which is the rightmost number that can grow. If the whole array is descending, `i` ends at −1.

`>=` (not `>`) matters for duplicates. With `[1, 5, 5]`, the pair `5, 5` can't be made bigger, so you keep moving left.
→ [while-loop](../syntax/while-loop.md) · [logical-operators](../syntax/logical-operators.md)

```python
if i >= 0:
    j = n - 1
    while nums[j] <= nums[i]:
        j -= 1
    temp = nums[i]
    nums[i] = nums[j]
    nums[j] = temp
```

**Swap with the next-larger value.** Only if a pivot exists. Scan from the right end of the descending suffix for the first value **strictly greater** than the pivot. That's the smallest increase available. The loop always stops, because `nums[i + 1] > nums[i]` is guaranteed.

The swap uses a temporary. Python's `nums[i], nums[j] = nums[j], nums[i]` does the same in one line.
→ [swap-tuple-assign](../syntax/swap-tuple-assign.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
left = i + 1
right = n - 1
while left < right:
    temp = nums[left]
    nums[left] = nums[right]
    nums[right] = temp
    left += 1
    right -= 1
```

**Reverse the suffix** with two pointers moving inwards. This turns the descending suffix into an ascending one, its smallest arrangement.

When there was no pivot, `i = -1`, so `left = 0` and the whole array is reversed. That's the wrap-around from largest to smallest, with no special case needed.
→ [while-loop](../syntax/while-loop.md) · [swap-without-temp](../syntax/swap-without-temp.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def nextPermutation(self, nums: list[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """

        n = len(nums)

        i = n - 2
        while i >= 0 and nums[i] >= nums[i + 1]:
            i -= 1

        if i >= 0:
            j = n - 1
            while nums[j] <= nums[i]:
                j -= 1
            temp = nums[i]
            nums[i] = nums[j]
            nums[j] = temp

        left = i + 1
        right = n - 1
        while left < right:
            temp = nums[left]
            nums[left] = nums[right]
            nums[right] = temp
            left += 1
            right -= 1
```

</details>

**Trace it.** `nums = [1, 5, 8, 4, 7, 6, 5, 3, 1]`:

| Step | What happens | Array |
|---|---|---|
| find pivot | from the right, `1 ≤ 3 ≤ 5 ≤ 6 ≤ 7` all descend; `4 < 7` stops at **i = 3** (value 4) | `[1, 5, 8, (4), 7, 6, 5, 3, 1]` |
| find j | from the right: 1, 3 are ≤ 4; **5** at j = 6 is the first > 4 | |
| swap | 4 ↔ 5 | `[1, 5, 8, 5, 7, 6, 4, 3, 1]` |
| reverse suffix | indices 4–8: `7 6 4 3 1` → `1 3 4 6 7` | `[1, 5, 8, 5, 1, 3, 4, 6, 7]` |

The result is the next arrangement after `158476531` ✅.

**The wrap case.** `[3, 2, 1]`: the pivot scan gives `i = -1`, the swap is skipped, and the whole array is reversed → `[1, 2, 3]` ✅.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).** Three linear steps, each at most one pass:

- The pivot scan moves left at most n times.
- The `j` scan moves left at most n times.
- The reverse swaps at most n/2 pairs.

Total O(n), with no sorting.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).** Only the indices `i`, `j`, `left`, `right` and a temp. The array is changed in place, as the problem requires.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Like incrementing a number, I want to change the rightmost position that can grow and make everything after it as small as possible. Scanning from the right, a descending suffix is already maxed out, so the pivot is the first `i` with `nums[i] < nums[i+1]`. I swap it with the smallest suffix value larger than it, which is the first larger value from the right since the suffix is descending. The suffix is still descending afterwards, so I reverse it to make it ascending. If there's no pivot, the array is the largest arrangement, and reversing it all wraps to the smallest. O(n) time, O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Previous permutation?" | Mirror every comparison: find the first `nums[i] > nums[i+1]` from the right, swap with the largest suffix value **smaller** than it, then reverse the suffix. |
| "Why reverse instead of sort?" | The suffix is guaranteed descending after the swap, so reversing gives ascending in O(n), against O(n log n) for a sort. |
| "Why `>=` in the pivot scan?" | Equal neighbours can't be made bigger. With `>`, `[1, 5, 5]` would pick the wrong pivot. |
| "k-th permutation of 1..n?" | A different technique: the factorial number system picks each digit directly (LeetCode 60). |
| "All permutations?" | Backtracking, as in [Permutations](46-permutations.md). Or call this function n! − 1 times starting from the sorted array. |

**Traps:**

- **Scanning for the pivot from the left.** The pivot is the **rightmost** position that can grow.
- **Swapping with the largest suffix value.** That overshoots. You need the *smallest* value bigger than the pivot.
- **Strict comparisons with duplicates.** `[1, 1, 5]` and `[1, 5, 1]` both go wrong with `>` or `<` in the scans.
- **Special-casing the descending array.** Not needed. `i = -1` makes the reverse start at 0.
- **Sorting the suffix.** Correct, but O(n log n) when a reverse suffices.

**This same move shows up in:** [Permutations](46-permutations.md) (generating every arrangement instead of the next one) · [Rotate Array](189-rotate-array.md) (in-place reversal as the key move) · [Reverse String](344-reverse-string.md) (the two-pointer reverse on its own) · [Monotone Increasing Digits](738-monotone-increasing-digits.md) (another "find where the order breaks, then fix the suffix" digit problem).

</details>

---
