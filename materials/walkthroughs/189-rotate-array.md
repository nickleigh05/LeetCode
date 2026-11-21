# 189. Rotate Array

**Medium** · [LeetCode](https://leetcode.com/problems/rotate-array/) · [Solution file (no hints)](../../problems/0001-0499/189.py)

[📖 02. Two Pointers lesson](../learning/02-two-pointers.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 02. Two Pointers problems](../rmap-practice/02-two-pointers.md)

---

Given an integer array `nums`, rotate it to the **right** by `k` steps **in place**. `k` is non-negative.

```
nums = [1,2,3,4,5,6,7], k = 3  →  [5,6,7,1,2,3,4]
nums = [-1,-100,3,99],  k = 2  →  [3,99,-1,-100]
```

**Constraints:** `1 <= nums.length <= 10⁵` · `-2³¹ <= nums[i] <= 2³¹ - 1` · `0 <= k <= 10⁵`

**Follow-up:** can you do it in place with **O(1) extra space**?

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| rotate **right** by k | The last k elements move to the front, in their original order |
| **in place** | You have to change `nums` itself. Returning a new list doesn't count |
| k can be **larger than n** | Rotating by n gets you back where you started, so only `k % n` matters |
| n and k up to 10⁵ | Rotating one step at a time is O(n·k) = 10¹⁰. Too slow |
| follow-up O(1) space | No copy of the array |

**Normalise k first.** Rotating 7 elements by 10 is the same as rotating by 3. Always do `k = k % n`. Without it, `k > n` will index out of range.

**The trick: three reversals.** Look at what rotation does: `[1,2,3,4 | 5,6,7]` → `[5,6,7 | 1,2,3,4]`. The two blocks swap places, and each keeps its internal order.

1. **Reverse everything:** `[7,6,5,4,3,2,1]`. The blocks have swapped places, but each one is now backwards.
2. **Reverse the first k:** `[5,6,7, 4,3,2,1]`. The first block is the right way round.
3. **Reverse the rest:** `[5,6,7, 1,2,3,4]`. Done.

Each reversal is an in-place two-pointer swap, so you need no extra array.

🤔 **Before you open the next section:** why does reversing the whole array put each block in the right *position* but the wrong *order*?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Rotate one step k times | Move the last element to the front, repeat | O(n·k) | O(1) | ❌ 10¹⁰ at the limits |
| Extra array | `new[(i + k) % n] = nums[i]`, copy back | O(n) | O(n) | ✅ Fine, fails the follow-up |
| Slicing | `nums[:] = nums[-k:] + nums[:-k]` | O(n) | O(n) | ✅ Pythonic, fails the follow-up |
| Cyclic replacements | Follow each index's cycle, moving one value at a time | O(n) | O(1) | ⚠️ Correct, tricky cycle counting |
| **Three reversals** | Reverse all, reverse first k, reverse the rest | **O(n)** | **O(1)** | ✅ |

**The decision: three in-place reversals**, each one a [two-pointer](../learning/02-two-pointers.md) swap moving inwards.

It's O(n), O(1) extra space, and the only tricky part is the indices. Cyclic replacements also hits O(1), but you have to count cycles carefully (there are `gcd(n, k)` of them), and it's easy to get wrong under pressure.

**About the slicing one-liner.** `nums[:] = nums[-k:] + nums[:-k]` is correct and in place in the sense LeetCode checks, because slice assignment writes into the same list object. But the right-hand side builds a new list, so it's O(n) extra space. Mention it, then give the reversal version for the follow-up. Watch out for `k = 0` with that one-liner: `nums[-0:]` is the **whole** list, so you'd get the array doubled.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
n = len(nums)
k = k % n
```

**Normalise k.** A rotation by `n` is a no-op, so only the remainder matters. This also means `k < n` from here on, which keeps every index below valid.
→ [integer-division-modulo](../syntax/integer-division-modulo.md)

```python
def reverse(left, right):
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1
```

**A reusable in-place reverse** between two inclusive indices. The pointers move inwards, swapping as they go, and stop when they meet or cross.

It's nested inside the method so it can see `nums` directly. Reading a variable from the enclosing scope is fine. You only need `nonlocal` to *rebind* a name, and here you're changing the list's contents, not rebinding it.
→ [function-basics](../syntax/function-basics.md) · [closures](../syntax/closures.md) · [swap-tuple-assign](../syntax/swap-tuple-assign.md) · [while-loop](../syntax/while-loop.md)

```python
reverse(0, n - 1)
reverse(0, k - 1)
reverse(k, n - 1)
```

**The three reversals.** All, then the first `k`, then the rest.

When `k == 0`, the middle call is `reverse(0, -1)`. `left < right` is false straight away, so it does nothing. The first and third calls both reverse the whole array and cancel out, so the array comes back unchanged, which is correct.
→ [function-basics](../syntax/function-basics.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """

        n = len(nums)
        k = k % n

        def reverse(left, right):
            while left < right:
                nums[left], nums[right] = nums[right], nums[left]
                left += 1
                right -= 1

        reverse(0, n - 1)
        reverse(0, k - 1)
        reverse(k, n - 1)
```

</details>

**Trace it.** `nums = [1,2,3,4,5,6,7]`, `k = 3`:

| Step | Call | Array |
|---|---|---|
| start | — | `[1,2,3,4,5,6,7]` |
| 1 | `reverse(0, 6)` | `[7,6,5,4,3,2,1]` |
| 2 | `reverse(0, 2)` | `[5,6,7,4,3,2,1]` |
| 3 | `reverse(3, 6)` | `[5,6,7,1,2,3,4]` ✅ |

**And with k larger than n.** `nums = [1,2]`, `k = 3`: `k % 2 = 1`. Reverse all → `[2,1]`, reverse `[0..0]` → no change, reverse `[1..1]` → no change. The result is `[2,1]` ✅, the same as rotating by 1.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).** Each reversal swaps half the elements in its range:

- `reverse(0, n-1)` does n/2 swaps.
- `reverse(0, k-1)` and `reverse(k, n-1)` together do another n/2.

So about n swaps in total, with each element moved at most twice. The `% n` makes the cost independent of k, even when k is 10⁵ and n is 2.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).** Just two indices inside `reverse`, and no copy of the array. This is the version that answers the follow-up.

| | Time | Extra space |
|---|---|---|
| Extra array / slicing | O(n) | O(n) |
| **Three reversals** | O(n) | **O(1)** |
| Cyclic replacements | O(n) | O(1) |

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "First I reduce k mod n, since rotating by n changes nothing. Rotation swaps two blocks while keeping each block's order. Reversing the whole array swaps the blocks but flips each one, so I then reverse the first k elements and the remaining n − k to put them back in order. Each reversal is an in-place two-pointer swap, so it's O(n) time and O(1) extra space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Rotate left instead?" | Reverse the first k, reverse the rest, then reverse all. Or rotate right by `n - k`. |
| "Why `k % n`?" | k can exceed n. Without it, `reverse(0, k - 1)` indexes past the end. |
| "Another O(1)-space way?" | Cyclic replacements: move each element to `(i + k) % n`, following each cycle. There are `gcd(n, k)` cycles. |
| "Rotate a linked list?" | [Rotate List](61-rotate-list.md): close the list into a ring, then break it at `n - k % n`. |
| "Rotate a matrix?" | [Rotate Image](48-rotate-image.md) uses the same "two simple flips make a rotation" idea: transpose, then reverse each row. |

**Traps:**

- **Forgetting `k % n`.** `k = 10, n = 7` crashes or gives the wrong answer.
- **`nums = nums[-k:] + nums[:-k]`.** That rebinds the local name, so the caller's list is never changed. Use `nums[:] = ...`.
- **`nums[-k:]` with `k = 0`.** `-0` is `0`, so that slice is the whole list.
- **Off-by-one on the reversal bounds.** The ranges are `[0, k-1]` and `[k, n-1]`, inclusive.
- **Rotating one step at a time.** O(n·k) is far too slow.

**This same move shows up in:** [Next Permutation](31-next-permutation.md) (an in-place suffix reversal as its final step) · [Rotate List](61-rotate-list.md) (the same rotation on a linked list) · [Reverse String](344-reverse-string.md) (the two-pointer reverse on its own) · [Rotate Image](48-rotate-image.md) (a rotation built from two simpler flips).

</details>

---
