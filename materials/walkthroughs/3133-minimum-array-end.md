# 3133. Minimum Array End

**Medium** · [LeetCode](https://leetcode.com/problems/minimum-array-end/) · [Solution file (no hints)](../../problems/3000-3499/3133.py)

[📖 18. Bit Manipulation lesson](../learning/18-bit-manipulation.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 18. Bit Manipulation problems](../rmap-practice/18-bit-manipulation.md)

---

Given two integers `n` and `x`, build a **strictly increasing** array `nums` of `n` positive integers whose **bitwise AND is exactly `x`**. Return the **minimum possible value of `nums[n - 1]`**.

```
n = 3, x = 4   →  6      nums = [4, 5, 6]     4 & 5 & 6 = 4
n = 2, x = 7   →  15     nums = [7, 15]       7 & 15 = 7
```

**Constraints:** `1 <= n, x <= 10⁸`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| AND of the array equals `x` | Every element must have **all of `x`'s 1-bits set** (otherwise the AND loses a bit). Extra 1-bits are fine so long as the AND ends up exactly `x`: some element must clear each non-`x` bit |
| strictly increasing | Elements are distinct and ascending |
| "minimise the last element" | Pick the **`n` smallest** numbers that contain `x`'s bits. The last one is the n-th |
| `n, x` up to `10⁸` | You can't enumerate. Compute the n-th such number directly |

**Reframe:** the allowed numbers are exactly those `y` with `y & x == x` (every 1-bit of `x` set). Their AND is `x` as long as you include `x` itself (the smallest one), because AND-ing `x` with supersets of `x` gives `x`. So the problem is: **find the n-th smallest number that has all of `x`'s bits set** (the first is `x`).

**How are those numbers ordered?** The bits of `x` are fixed at 1. The free positions are the **0-bits of `x`**. Treat the free positions as the digits of a counter: the k-th number is `x` with the binary representation of `k` written, bit by bit, into the zero positions of `x`, lowest free position first.

We want index `n − 1` (zero-based), so write `n − 1` into the free bit positions of `x`.

🤔 **Before you open the next section:** for `x = 4` (`100`) and `n = 3`, `n − 1 = 2 = 10₂`. Where do those two bits go, and what number results?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Time | Verdict |
|---|---|---|
| Count up from `x`, keep numbers with `y & x == x`, take the n-th | O(n · gap) | ❌ `n` is up to 10⁸ and the gaps grow |
| **Deposit the bits of `n − 1` into the zero bits of `x`** | **O(log(x) + log(n))** | ✅ |

**The decision: [bit manipulation](../learning/18-bit-manipulation.md), "bit deposit".** Scan the bit positions of the result from the lowest up. At each position:

- If `x` has a **1** there, the bit is forced to 1 already: skip it.
- If `x` has a **0** there, it's a free slot: put the **lowest unused bit of `n − 1`** there, then consume it (`remaining >>= 1`).

Stop when every bit of `n − 1` has been placed. The result is the n-th smallest number containing `x`.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
result = x
remaining = n - 1
bit = 1
```

`result` starts as `x`, the first (index 0) valid number. `remaining` is the zero-based index we still have to write into free positions. `bit` is the single-bit mask for the position being examined, starting at bit 0.
→ [variables-assignment](../syntax/variables-assignment.md) · [bitwise-operators](../syntax/bitwise-operators.md)

```python
while remaining > 0:
```

Keep going until every bit of `n − 1` has been deposited.
→ [while-loop](../syntax/while-loop.md)

```python
    if (x & bit) == 0:
        if remaining & 1:
            result |= bit
        remaining >>= 1
```

At a position where `x` has a **0** (a free slot): look at the lowest bit of `remaining`. If it's 1, set that bit in `result` (`|=`). **Either way, consume the bit** (`>>= 1`) because this free slot has now been "used". If `x` has a **1** here, the bit is already set in `result` and this branch is skipped entirely, so `remaining` doesn't advance.
→ [bitwise-operators](../syntax/bitwise-operators.md) · [truthy-falsy-values](../syntax/truthy-falsy-values.md)

```python
    bit <<= 1

return result
```

Move to the next bit position. When `remaining` hits 0 there's nothing more to place and `result` is the answer.
→ [arithmetic-operators](../syntax/arithmetic-operators.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def minEnd(self, n: int, x: int) -> int:
        result = x
        remaining = n - 1
        bit = 1

        while remaining > 0:
            if (x & bit) == 0:
                if remaining & 1:
                    result |= bit
                remaining >>= 1
            bit <<= 1

        return result
```

</details>

**Trace it.** `n = 3`, `x = 4` (`100`), so `remaining = 2` (`10`):

| `bit` | `x & bit` | Free? | `remaining & 1` | `result` | `remaining` after |
|---|---|---|---|---|---|
| 1 (bit 0) | 0 | yes | 0 | `100` = 4 | `1` |
| 2 (bit 1) | 0 | yes | 1 | `110` = 6 | `0` |

`remaining == 0`, so stop: **6** ✅. The array `[4, 5, 6]`. Bit 2 is `x`'s own 1-bit and would be skipped.

`n = 2`, `x = 7` (`111`): `remaining = 1`. Bits 0-2 are all 1s in `x`, so they're skipped. At bit 3 (free): `remaining & 1 = 1` → set it: `1111` = **15** ✅.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(log x + log n)</summary>

The loop walks bit positions up to about `log₂(x) + log₂(n)`, depositing one bit of `n − 1` per free slot: **O(log x + log n)**, at most about 60 iterations.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1):** a few integers.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "For the AND to be `x`, every element must contain all of `x`'s one-bits, and including `x` itself guarantees the AND is exactly `x`. So I want the n-th smallest number that is a bit-superset of `x`. Those numbers are ordered like a counter running through the zero-bits of `x`: the index `n − 1`, written in binary, gets deposited into the free positions of `x`, lowest first. I loop over bit positions, and at each zero bit of `x` I take the lowest bit of the remaining index. O(log) time, O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why is the AND exactly `x`?" | `x` itself is in the array. AND-ing it with supersets of `x` can't add bits and can't remove `x`'s bits |
| "Why does `n − 1` map to the zero bits in order?" | The numbers containing `x` ordered by value correspond to counting in binary on the free positions, since higher free bits outweigh lower ones |
| "Alternative?" | `result = x | (deposit(n-1, ~x))`: a software version of the `PDEP` CPU instruction |
| "What if `x` is 0?" | Not allowed (`x >= 1`), but the answer would be `n − 1` |
| "Related?" | [Number of 1 Bits](191-number-of-1-bits.md) · [Single Number](136-single-number.md) · [Bitwise AND of Numbers Range](201-bitwise-and-of-numbers-range.md) |

**Traps:**

- **Shifting `remaining` at positions where `x` has a 1.** Only free positions consume a bit.
- **Starting `remaining` at `n` instead of `n − 1`.** Off by one: index 0 is `x` itself.
- **Forgetting `result |= bit`** and building the result with `+`, which can double-count.
- **Counting from `x + 1` upward.** Numbers that lack `x`'s bits break the AND.

**This same move shows up in:** [Bitwise AND of Numbers Range](201-bitwise-and-of-numbers-range.md) · [Counting Bits](338-counting-bits.md) · [Sum of All Subset XOR Totals](1863-sum-of-all-subset-xor-totals.md).

</details>

---
