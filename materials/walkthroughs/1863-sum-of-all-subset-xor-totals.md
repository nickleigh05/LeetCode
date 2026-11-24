# 1863. Sum of All Subset XOR Totals

**Easy** · [LeetCode](https://leetcode.com/problems/sum-of-all-subset-xor-totals/) · [Solution file (no hints)](../../problems/1500-1999/1863.py)

[📖 10. Backtracking lesson](../learning/10-backtracking.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 10. Backtracking problems](../rmap-practice/10-backtracking.md)

---

The **XOR total** of an array is the XOR of all its elements (`0` for an empty array). Given `nums`, return the **sum of the XOR totals of every subset** of `nums`. Subsets that differ by position count separately, even if their values match.

```
nums = [1, 3]        →  6     subsets: {} → 0, {1} → 1, {3} → 3, {1,3} → 2        total 6
nums = [5, 1, 6]     →  28
nums = [3, 4, 5, 6, 7, 8]  →  480
```

**Constraints:** `1 <= nums.length <= 12` · `1 <= nums[i] <= 20`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "every subset" | `2ⁿ` subsets: the signature of **backtracking** (include / exclude each element) |
| `n <= 12` | `2¹² = 4096` subsets. Enumerating them all is cheap, and the problem expects you to |
| XOR total per subset, then sum | Carry a running XOR down the recursion, and add it at each leaf |
| "Easy" with a clever twist available | There's an O(n) closed form hiding behind the enumeration |

**The straightforward solution** is the standard subset recursion: for each index, either skip the element or XOR it into the running value. At the end of the array add the running value to the total.

**The pattern behind it.** Look at one bit position. If **no** element has that bit set, no subset has it in its XOR. If at least one element has it set, then **exactly half of all subsets** have it set in their XOR (the subsets split evenly between odd and even counts of the elements containing that bit). Each such bit contributes `2ⁿ⁻¹ × bit_value`. Summing over bits, this is `(OR of all elements) × 2ⁿ⁻¹`.

🤔 **Before you open the next section:** for `nums = [1, 3]`, compute `OR` of the elements and `2^(n-1)`, and compare with the answer 6.

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Time | Space | Verdict |
|---|---|---|---|
| Backtracking: include / skip each element | O(2ⁿ) | O(n) stack | ✅ The expected "show the pattern" answer. Fine for `n <= 12` |
| Iterate all bitmasks `0 .. 2ⁿ-1` | O(n · 2ⁿ) | O(1) | ✅ Same idea, no recursion |
| **Bit-counting observation: `OR` of all × 2ⁿ⁻¹** | **O(n)** | **O(1)** | ✅ The follow-up an interviewer hopes you find |

**The decision: state the [backtracking](../algorithms/backtracking.md) solution as the baseline, then give the O(n) formula** (which is what the code below does).

Why the formula works: fix a bit `b` and let `k >= 1` elements have it set. A subset's XOR has bit `b` set exactly when it picks an **odd** number of those `k` elements. Half of the ways to choose from `k` elements have odd size, and the other `n - k` elements are free, so the count is `2ᵏ⁻¹ · 2ⁿ⁻ᵏ = 2ⁿ⁻¹`. Each of those subsets adds `2ᵇ` to the sum. A bit that no element has contributes nothing, and the `OR` is precisely the mask of bits that *some* element has.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
bits = 0
for num in nums:
    bits |= num
```

Accumulate the bitwise **OR** of every element. After the loop, `bits` has a 1 exactly in the positions where at least one element has a 1: the set of bits that can ever appear in any subset's XOR.
→ [bitwise-operators](../syntax/bitwise-operators.md) · [for-loop](../syntax/for-loop.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
return bits << (len(nums) - 1)
```

Each of those bits appears in exactly `2ⁿ⁻¹` subset XORs. Multiplying by `2ⁿ⁻¹` is a left shift by `n - 1`. Because it's one shift on the combined mask, it adds up every bit's contribution at once.
→ [bitwise-operators](../syntax/bitwise-operators.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def subsetXORSum(self, nums: List[int]) -> int:
        bits = 0

        for num in nums:
            bits |= num

        return bits << (len(nums) - 1)
```

</details>

**Alternative: the backtracking baseline** (what to write first if you don't see the formula):

```python
def subsetXORSum(self, nums: List[int]) -> int:
    def dfs(i, current):
        if i == len(nums):
            return current
        return dfs(i + 1, current ^ nums[i]) + dfs(i + 1, current)

    return dfs(0, 0)
```

At each index two branches: **take** the element (XOR it in) or **skip** it. The leaves return the subset's XOR and the sum bubbles back up.
→ [backtracking](../algorithms/backtracking.md) · [recursion-basics](../syntax/recursion-basics.md)

**Trace it.** `nums = [5, 1, 6]`:

| Step | Value |
|---|---|
| `bits` after 5 | `101` = 5 |
| `bits` after 1 | `101 \| 001` = `101` = 5 |
| `bits` after 6 | `101 \| 110` = `111` = 7 |
| shift by `n - 1 = 2` | `7 << 2 = 28` ✅ |

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)**: one pass to OR the elements, one shift. The backtracking baseline is **O(2ⁿ)** (4096 leaves for `n = 12`, instant here but exponential in general).

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** for the formula. The recursive baseline uses O(n) stack.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "With n up to 12 I can enumerate all 2ⁿ subsets with include-or-skip recursion, carrying the running XOR, and sum the leaves. That's the baseline. But looking at one bit at a time: if no element has the bit, it never shows up. If any element has it, exactly half of all subsets have it set in their XOR. So each present bit contributes 2ⁿ⁻¹ times its value, and the sum is the OR of all elements shifted left by n−1. That's O(n) time and O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why exactly half?" | Pick any element that has the bit. Pairing each subset with the same subset toggled on that element flips the bit's parity, so the subsets split evenly |
| "Does this need `nums` to be distinct?" | No. Duplicate values are still separate elements, and the argument counts positions |
| "Related subsets problems?" | [Subsets](78-subsets.md) and [Subsets II](90-subsets-ii.md): the same include/skip recursion |
| "What about XOR of **all** subset XORs (not the sum)?" | A different question: it's 0 when `n >= 2`, because each bit appears in an even number of subsets |
| "Large `n`?" | Only the formula works: the OR and the shift, with the answer reduced modulo a prime if asked |

**Traps:**

- **Using `+` or `*` instead of `|`** when accumulating the mask.
- **Shifting by `n` instead of `n - 1`.** Half of the `2ⁿ` subsets, not all.
- **Counting the empty subset as nothing.** It contributes `0`, which is harmless, but a recursive version must still reach it.
- **Believing the formula needs sorted or unique input.** It doesn't.

**This same move shows up in:** [Subsets](78-subsets.md) (the enumeration) · [Single Number](136-single-number.md) (XOR properties) · [Hamming Distance](461-hamming-distance.md) (reasoning bit by bit).

</details>

---
