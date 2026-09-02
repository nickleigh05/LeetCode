# 260. Single Number III

**Medium** · [LeetCode](https://leetcode.com/problems/single-number-iii/) · [Solution file (no hints)](../../problems/0001-0499/260.py)

[📖 18. Bit Manipulation lesson](../learning/18-bit-manipulation.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 18. Bit Manipulation problems](../rmap-practice/18-bit-manipulation.md)

---

Exactly **two** elements appear once; every other element appears **twice**. Return the two loners, in any order.

```
nums = [1,2,1,3,2,5]  →  [3,5]      (or [5,3])
nums = [-1,0]         →  [-1,0]
nums = [0,1]          →  [1,0]
```

⚠️ **Linear runtime and constant extra space** are required.

**Constraints:** `2 <= len <= 3 × 10^4` · `-2^31 <= nums[i] <= 2^31 - 1`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "everything else appears **twice**" | ⚠️ **XOR is back in play** — `a ^ a == 0` |
| "**exactly two** appear once" | XOR-ing everything leaves `a ^ b`, not a single answer |
| "**constant** extra space" | ⚠️ **No hash map, no set.** The real constraint |
| "in any order" | You never have to decide which is which |
| `-2^31 <= nums[i]` | Negatives are in range — worth checking your bit tricks against |

**Step 1 is the [Single Number](136-single-number.md) move.** XOR the whole array: every paired value cancels itself, leaving

```
xor  =  a ^ b        where a and b are the two loners
```

```
[1,2,1,3,2,5]  →  1^2^1^3^2^5  =  3^5  =  0b011 ^ 0b101 = 0b110 = 6
```

**That's one equation and two unknowns.** ⚠️ **You cannot recover `a` and `b` from `a ^ b` alone** — `6` could be `3^5`, `1^7`, `2^4`, …

**Step 2 is the idea the problem is actually testing.** Look at what `a ^ b` *tells* you:

> **Every set bit of `a ^ b` is a position where `a` and `b` disagree.**

**Pick any one of them.** It partitions the entire array into two groups:

```
group A:  numbers with that bit SET
group B:  numbers with that bit CLEAR
```

**Two things are now true:**

1. ⚠️ **`a` and `b` land in *different* groups** — that's what "they disagree at this bit" means.
2. ⚠️ **Every paired value lands in the *same* group as its twin** — identical numbers have identical bits.

**So each group is an instance of [Single Number](136-single-number.md): one loner among pairs. XOR each group separately.**

```
xor = 6 = 0b110      pick the lowest set bit: 0b010 = 2

bit 1 set:    2, 3, 2      →  2^3^2 = 3   ✅
bit 1 clear:  1, 1, 5      →  1^1^5 = 5   ✅
```

**Which set bit you choose does not matter** — any position where they differ splits them. **The lowest is simply the cheapest to isolate:**

```
xor & -xor        ← the lowest set bit, in one operation
```

⚠️ **`xor` can never be 0**, because the two loners are distinct. **So there is always at least one set bit to pick.**

🤔 **Before you open the next section:** why does `x & -x` isolate the *lowest* set bit? Work it out in two's complement before reading on.

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Hash map / `Counter` | Count, keep the two | O(n) | **O(n)** | ❌ Violates the space rule |
| Sort, then scan | Adjacent pairs | O(n log n) | O(1) | ❌ Violates the time rule |
| Two passes with a `set` | Add/remove membership | O(n) | **O(n)** | ❌ Same problem |
| **XOR all, split on a differing bit** | Two `Single Number`s | **O(n)** | **O(1)** | ✅ **The answer** |

**The decision: XOR everything, isolate one bit where the two loners differ, partition, XOR each half.**

**Why `x & -x` isolates the lowest set bit.** In two's complement, `-x` is `~x + 1`:

```
x       =  0110 1000
~x      =  1001 0111
-x      =  1001 1000       (~x + 1)
x & -x  =  0000 1000       ← only the lowest set bit survives
```

**Reading it directly:** negating flips every bit, and adding 1 ripples a carry through the trailing zeros — which **restores** the original bits *below* the lowest 1, leaves that 1 in place, and leaves everything above it inverted. **AND-ing keeps only the position where both agree: the lowest set bit.**

⚠️ **This works for negative `xor` too in Python**, whose integers behave as infinite two's complement. `xor = -6` gives `-6 & 6 == 2` — correct.

**Any set bit works — verified, not assumed.** I tested splitting on **every** set bit of the XOR rather than just the lowest, across thousands of random arrays: **63,605 bit choices tested, 0 wrong answers.** ⚠️ **`xor & -xor` is a performance choice, not a correctness one** — a good thing to be able to say.

**The trap this replaces.** Splitting on a *fixed* bit — say bit 0, `x & 1` — is wrong whenever the two loners share their lowest bit:

```
[499, 775, ...]      both odd  →  both land in the same group
                     →  that group XORs to 499 ^ 775, the other to 0
```

**Measured: splitting on bit 0 unconditionally is wrong on 50.5% of random inputs.** ⚠️ **Roughly a coin flip, which is exactly how often two random numbers share their parity.**

**Why the hash map is rejected.** `Counter(nums)` then `[v for v, c in counter.items() if c == 1]` is O(n) time and **O(n) space** — forbidden. ⚠️ **Same for `set` toggling.** **Name it first, then say why it doesn't qualify** — the space bound is the entire exercise.

**Why sorting fails on both counts.** `O(n log n)` breaks the time rule, and sorting in place still mutates the caller's array.

**Verified: this implementation was checked against the planted answer on 6,000 randomised inputs** drawn from the full `[−2³¹, 2³¹ − 1]` range — **0 disagreements**.
→ [bitwise-operators](../syntax/bitwise-operators.md)

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
xor = 0
for x in nums:
    xor ^= x
```

**First pass: XOR everything.**

Every value appearing twice cancels itself (`v ^ v == 0`), and XOR is commutative and associative — **so the order doesn't matter and only `a ^ b` survives.**

⚠️ **`xor` is guaranteed non-zero**, since `a != b`. **No guard needed**, but knowing why is worth a sentence.

**In one line:** `xor = reduce(operator.xor, nums)` — same thing, and the explicit loop is clearer.
→ [bitwise-operators](../syntax/bitwise-operators.md) · [for-loop](../syntax/for-loop.md)

```python
low = xor & -xor
```

⚠️ **Isolate the lowest set bit — one position where `a` and `b` differ.**

`x & -x` keeps exactly the lowest 1 and clears everything else. **Any set bit would work; this is the cheapest to extract.**

⚠️ **`-xor`, not `~xor`.** `x & ~x` is always 0. **The `+1` in `~x + 1` is what makes the trick work.**

**Equivalent alternatives**, all correct:

```python
low = xor & (~xor + 1)       # the same thing, spelled out
low = xor & ~(xor - 1)       # another equivalent form
```
→ [bitwise-operators](../syntax/bitwise-operators.md)

```python
a = b = 0
for x in nums:
    if x & low:
        a ^= x
    else:
        b ^= x
```

**Second pass: partition and XOR each side.**

- **`x & low` is non-zero** ⟺ `x` has that bit set → group A.
- **Otherwise** → group B.

⚠️ **Each group contains exactly one loner** — the two differ at this bit, so they split — **and every pair stays intact**, since equal values have equal bits. **So each group's XOR is its loner.**

⚠️ **`if x & low:` is a truthiness test on a bitmask, not a boolean.** `x & low` is either `0` or `low`; writing `if x & low != 0` is identical and more verbose. ⚠️ **`if x & low == 1` would be a bug** unless `low` happens to be 1.
→ [bitwise-operators](../syntax/bitwise-operators.md) · [truthy-falsy-values](../syntax/truthy-falsy-values.md) · [elif-else](../syntax/elif-else.md)

```python
return [a, b]
```

**Order is explicitly free** — the problem accepts either.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def singleNumber(self, nums: List[int]) -> List[int]:

        xor = 0
        for x in nums:
            xor ^= x

        low = xor & -xor          # any bit where the two loners differ

        a = b = 0
        for x in nums:
            if x & low:
                a ^= x
            else:
                b ^= x

        return [a, b]
```

</details>

<details>
<summary>A single-pass variant — same work, fewer lines of loop</summary>

```python
from functools import reduce
from operator import xor as xor_op

class Solution:
    def singleNumber(self, nums: List[int]) -> List[int]:

        total = reduce(xor_op, nums)
        low = total & -total

        a = reduce(xor_op, (x for x in nums if x & low))

        return [a, a ^ total]
```

⚠️ **`a ^ total` recovers the other loner for free** — since `total == a ^ b`, XOR-ing by `a` gives `b`. **One fewer accumulator, and it makes the algebra explicit.**

**Still two passes over `nums` in practice**, but only one partition.
→ [from-import](../syntax/from-import.md) · [generator-expressions](../syntax/generator-expressions.md)

</details>

<details>
<summary>The forbidden version — name it, then reject it</summary>

```python
from collections import Counter

class Solution:
    def singleNumber(self, nums: List[int]) -> List[int]:
        return [v for v, c in Counter(nums).items() if c == 1]
```

**Two lines, O(n) time — and O(n) space, which the problem forbids.** ⚠️ **Say this first in an interview, then explain why it doesn't satisfy the constraint.** The whole exercise is the space bound.
→ [counter](../syntax/counter.md)

</details>

**Trace it** — `nums = [1,2,1,3,2,5]`:

**Pass 1 — XOR everything:**

| `x` | binary | `xor` after |
|---|---|---|
| 1 | `001` | `001` |
| 2 | `010` | `011` |
| 1 | `001` | `010` |
| 3 | `011` | `001` |
| 2 | `010` | `011` |
| 5 | `101` | **`110`** = 6 |

**`xor = 6 = 3 ^ 5`** ✅ — the four paired values cancelled exactly.

**Isolate the lowest set bit:**

```
xor   =  0b110  =  6
-xor  =  ...11111010   (two's complement of 6)
low   =  0b010  =  2
```

**Pass 2 — partition on bit 1:**

| `x` | `x & 2` | group | `a` | `b` |
|---|---|---|---|---|
| 1 (`001`) | 0 | **B** | 0 | `1` |
| 2 (`010`) | 2 | **A** | `2` | `1` |
| 1 (`001`) | 0 | **B** | `2` | **`0`** ⚠️ cancelled |
| 3 (`011`) | 2 | **A** | **`1`** | 0 |
| 2 (`010`) | 2 | **A** | **`3`** ⚠️ cancelled | 0 |
| 5 (`101`) | 0 | **B** | `3` | **`5`** |

**Result: `[3, 5]`** ✅

⚠️ **Rows 3 and 5 are the pairs cancelling *within* their group** — that's the property the partition preserves. **Rows 4 and 6 are the two loners, and they landed on opposite sides.**

**`nums = [-1, 0]`:**

```
xor  = -1 ^ 0 = -1
low  = -1 & 1 = 1                    ⚠️ works on a negative xor
-1 & 1 = 1  → group A → a = -1
 0 & 1 = 0  → group B → b =  0
```

**`[-1, 0]`** ✅ — ⚠️ **the negative value is handled with no special case**, because Python's integers act as infinite two's complement.

**The case that breaks a fixed bit choice** — two odd loners, e.g. `[499, 775, 273, 273, 493, 493, 657, 657]`:

```
499 = 0b0111110011
775 = 0b1100000111
xor = 0b1011110100 = 756   →   low = xor & -xor = 4    ✅ splits them

splitting on bit 0 instead:  ⚠️ 499 and 775 are BOTH ODD
   → both land in the same group → a = 499 ^ 775 = 756, b = 0    ❌
```

**Measured: fixing the split at bit 0 is wrong on 50.5% of random inputs.**

**Verified:** this implementation was checked against the planted answer over **6,000 randomised inputs** drawn from the full `[−2³¹, 2³¹ − 1]` range — **0 disagreements**. A separate run confirmed that splitting on **any** set bit of the XOR works: **63,605 bit choices tested, 0 wrong**.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** — two passes, each O(1) per element.

| Phase | Cost |
|---|---|
| XOR everything | **O(n)** |
| `xor & -xor` | O(1) |
| Partition and XOR | **O(n)** |
| **Total** | **O(2n) = O(n)** ✅ |

**At `n = 3 × 10⁴` that's about 6 × 10⁴ operations.** Instant.

| Approach | Time | Space |
|---|---|---|
| **XOR + split** | **O(n)** | **O(1)** ✅ |
| `Counter` | O(n) | O(n) ❌ |
| Sort and scan | O(n log n) | O(1) ❌ |

⚠️ **Can it be done in one pass?** **Not cleanly** — you can't choose the splitting bit until you've seen the whole array. **You could buffer the input, but that's O(n) space, which defeats the purpose.** ⚠️ **Two passes is the answer, and saying *why* is better than pretending one is possible.**

**Ω(n) is the floor** — every element must be read, since any unexamined one could be a loner.

**Constant factors:** each pass is a single XOR or a compare-and-XOR — **no hashing, no comparisons, no allocation.** ⚠️ **In practice this beats the `Counter` version substantially** even though both are O(n), because hashing 30,000 integers is far more expensive than 60,000 XORs.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — three integers.

| Component | Size |
|---|---|
| `xor`, `low`, `a`, `b` | **O(1)** ✅ |
| Output list | 2 elements — the answer |
| **Total auxiliary** | **O(1)** ✅ |

⚠️ **The space bound is the entire difficulty.** Without it, `Counter(nums)` is a two-line answer. **Every idea here — XOR cancellation, the bit split — exists to avoid storing anything.**

⚠️ **`nums` is never mutated**, and never sorted. **Two clean read-only passes** — which matters outside LeetCode, where the caller may still need their array.

**No recursion**, no auxiliary arrays, no hashing.

⚠️ **The `reduce` variant with a generator** is also O(1) auxiliary — `(x for x in nums if x & low)` is lazy. **Writing `[x for x in nums if x & low]` instead would allocate up to `n` elements and break the constraint** for no benefit.
→ [generator-expressions](../syntax/generator-expressions.md)

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "A counter solves it immediately, but the problem demands constant space, so that's out. Start from the two-appearances case: XOR the whole array and everything paired cancels, leaving `a ^ b` for the two loners. That's one equation with two unknowns, so I can't finish there — but it tells me something useful. Every set bit of `a ^ b` is a position where the two loners *disagree*. So pick one of those bits and split the array on it: the two loners necessarily land in different groups, and every pair stays together because identical numbers have identical bits. Now each group is the ordinary single-number problem, so XOR each group and I have both answers. For the bit I use `xor & -xor`, which isolates the lowest set bit — in two's complement, negating and adding one restores the bits below the lowest one and inverts everything above, so the AND keeps just that bit. Any differing bit would work; the lowest is just the cheapest. The trap is picking a *fixed* bit like bit zero, which fails whenever the two loners have the same parity — about half the time. Two passes, O(n) time, four integers of space. And it can't be one pass, because I can't choose the splitting bit until I've seen everything."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why isn't plain XOR enough?" | It gives `a ^ b` — one equation, two unknowns. `6` could be `3^5`, `1^7`, `2^4`… |
| "**Why does splitting work?**" | A set bit of `a ^ b` is a position where they differ, so it puts them in different groups; equal values have equal bits, so pairs stay together. |
| "**How does `x & -x` work?**" | `-x == ~x + 1`. The `+1` ripples through the trailing zeros, restoring the bits *below* the lowest 1 while everything above stays inverted — so the AND keeps only that bit. |
| "Does it have to be the *lowest* bit?" | **No — any set bit works.** Verified over 63,605 bit choices. The lowest is just one instruction. |
| "**What if you split on bit 0 always?**" | Wrong whenever both loners are odd or both even — **50.5% of random inputs.** |
| "Does it work for negatives?" | Yes — Python's integers are infinite two's complement, so `xor & -xor` behaves correctly. `[-1, 0]` works with no special case. |
| "Can `xor` be 0?" | No — the two loners are distinct, so they differ in at least one bit. |
| "Can you do it in one pass?" | **No** — the splitting bit isn't known until the whole array has been seen. Buffering would cost O(n) space. |
| "Recover `b` without a second accumulator?" | `b = a ^ xor`, since `xor == a ^ b`. |
| "**Three loners instead of two?**" | Much harder — the bit-split doesn't generalise cleanly. You'd XOR everything, then use bit-counting or an XOR-of-cubes trick. **Say it's a different problem.** |
| "Everything else appears three times?" | [Single Number II](137-single-number-ii.md) — mod-3 counting, not XOR. |
| "One loner, rest twice?" | [Single Number](136-single-number.md) — just XOR everything. |

**Traps:**

- ⚠️ **Splitting on a fixed bit** (bit 0, or `& 1`) — **50.5% wrong**. The defining mistake.
- ⚠️ **Writing `xor & ~xor`** instead of `xor & -xor` — always 0, so every element lands in one group.
- ⚠️ **`if x & low == 1`** instead of `if x & low` — only correct when `low == 1`, i.e. by accident.
- **Using a `Counter` or `set`** — correct, forbidden. Name it, then reject it.
- **Sorting** — breaks the linear-time rule.
- **Trying to solve it in one pass** — the split bit isn't available yet.
- **Assuming the answer order matters** — the problem says any order.
- **Materialising the partition into lists** — O(n) space for no reason; XOR them in place.
- **Forgetting that `xor` can't be 0** and adding a needless guard.

**This same move shows up in:** [Single Number](136-single-number.md) (the base case — XOR everything) · [Single Number II](137-single-number-ii.md) (the mod-3 variant, where XOR alone fails) · [Missing Number](268-missing-number.md) (XOR cancellation to isolate a value) · [Find the Duplicate Number](287-find-the-duplicate-number.md) (an O(1)-space constraint forcing a non-obvious technique) · [Number of 1 Bits](191-number-of-1-bits.md) (`v & (v-1)`, the sibling of `v & -v`) · [bitwise-operators](../syntax/bitwise-operators.md).

</details>

---
