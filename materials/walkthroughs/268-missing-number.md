# 268. Missing Number

**Easy** · [LeetCode](https://leetcode.com/problems/missing-number/) · [Solution file (no hints)](../../problems/0001-0499/268.py)

[📖 19. Bit Manipulation lesson](../learning/19-bit-manipulation.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 19. Bit Manipulation problems](../rmap-practice/19-bit-manipulation.md)

---

Given an array `nums` containing `n` **distinct** numbers taken from the range `[0, n]`, return the one number in that range which is **missing** from the array.

The follow-up asks for **O(n)** runtime and **O(1)** extra space.

```
nums = [3,0,1]         →  2      n = 3, so the range is [0,3]; 2 is absent
nums = [0,1]           →  2      n = 2, range [0,2]
nums = [9,6,4,2,3,5,7,0,1]  →  8
```

**Constraints:** `n == nums.length` · `1 <= n <= 10⁴` · `0 <= nums[i] <= n` · all numbers are **unique**.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| `n` numbers from the range `[0, n]` | That range holds **n + 1** values, and the array has only **n** — so exactly one is missing |
| all numbers are **distinct** | No duplicates to complicate the accounting. Each value appears at most once |
| indices run `0 .. n-1` | And the *values* run `0 .. n`. **Those two sets differ by exactly one element** — which is the missing number |
| follow-up: O(1) space | Rules out the hash set, which is the obvious first answer |
| `n <= 10⁴` | Small; the constraint that matters is space, not time |

The observation that unlocks everything is in the third row, so state it precisely:

> The array's **indices** are `0, 1, …, n-1`.
> The array's **values** are `0, 1, …, n` **minus one missing element**.

So if you pool the indices and the values together, every number from 0 to n−1 appears... **twice**, once as an index and once as a value — *except* the missing number, which appears only as an index. And `n` itself appears only as a value's would-be slot, never as an index.

That's a set where **everything is paired except one element** — which is exactly [Single Number](136-single-number.md). And the tool for "everything cancels except the unpaired one" is **XOR**.

Concretely, for `nums = [3, 0, 1]` (n = 3):

```
indices:  0, 1, 2        plus n = 3
values:   3, 0, 1
```

XOR them all: `0^1^2^3 ^ 3^0^1`. Regroup — legal, since XOR is commutative and associative:

```
(0^0) ^ (1^1) ^ (3^3) ^ 2  =  0 ^ 0 ^ 0 ^ 2  =  2 ✓
```

**The missing number is the only one without a partner.**

The one wrinkle: indices only go up to `n-1`, but the value range goes up to `n`. So `n` needs to be XORed in manually — which is exactly what seeding the accumulator with `len(nums)` does.

🤔 **Before you open the next section:** there's a completely different solution using the sum formula `n(n+1)/2`. It's arguably simpler. What's the one thing XOR gives you that the sum version doesn't?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Hash set | Add all values, then scan `0..n` for the absent one | O(n) | **O(n)** | ❌ Violates the follow-up's space constraint |
| Sort, then scan | Sort and find the first index where `nums[i] != i` | **O(n log n)** | O(1) | ❌ Violates the time constraint |
| **Gauss sum** | `n(n+1)/2 − sum(nums)` | **O(n)** | **O(1)** | ✅ Correct, and the shortest to write |
| **XOR indices with values** | Everything pairs off except the missing number | **O(n)** | **O(1)** | ✅ |
| Cyclic sort | Place each value at its own index, then scan | O(n) | O(1) | ⚠️ Correct but mutates the input, and it's more code |

**The decision:** **XOR** — though the Gauss sum is equally valid here and worth naming.

**The sum approach** is genuinely elegant: the numbers `0..n` sum to `n(n+1)/2` by Gauss's formula, so subtracting the array's actual sum leaves the missing value.

```python
return len(nums) * (len(nums) + 1) // 2 - sum(nums)
```

One line, O(n) time, O(1) space. **It satisfies every stated requirement.**

**So what does XOR give you that the sum doesn't?** — the answer to section 1's question. **Overflow safety.**

The sum of `0..n` grows quadratically. At n = 10⁴ that's about 5 × 10⁷ — fine. But at n = 10⁵ or in a 32-bit language, `n(n+1)/2` can exceed the integer range **even though the answer itself is small**. Python's arbitrary-precision integers make this a non-issue, but in Java or C++ the sum version can overflow while the XOR version cannot — **XOR never produces a value larger than the largest input**, because it's bitwise.

That's the honest distinction: both are correct here, and **XOR is the more robust of the two**. Mention both, and say why you'd prefer XOR in a fixed-width language.

**Why XOR works structurally.** Same three properties as [Single Number](136-single-number.md):

- `a ^ a = 0` — pairs annihilate.
- `a ^ 0 = a` — 0 is the identity, so the seed is safe.
- Commutative and associative — you can regroup the index-value pairs freely, which is what licenses the cancellation argument regardless of array order.

**Why the accumulator starts at `len(nums)`.** The indices supply `0 .. n-1`, but the value range extends to `n`. Seeding with `n` injects that final element so the pairing is complete. Seeding with 0 instead would leave `n` unaccounted for and the answer would be wrong by `n`.

**Why not cyclic sort?** Repeatedly swapping each value to its own index also finds the gap in O(n)/O(1), but it destroys the input and takes considerably more code for no gain.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
res = len(nums)   # accounts for index n, which has no matching nums index
```
**Seed the accumulator with `n`.**

This is the line that most people get wrong or omit. The loop below XORs indices `0 .. n-1` against the values, but the *value range* is `0 .. n` — so `n` itself would never enter the computation. Seeding with `len(nums)` injects it up front.

Think of it as XORing in the one "index" that doesn't exist: there's no `nums[n]`, so `n` is supplied by hand.

If the missing number happens to *be* `n` (as in `[0,1]` where n = 2), this seed is what carries it through to the answer — every other term cancels and the seed survives untouched.
→ [variables-assignment](../syntax/variables-assignment.md) · [list-basics](../syntax/list-basics.md)

```python
for i, num in enumerate(nums):
    res ^= i ^ num
```
**XOR in both the index and the value at each position.**

[`enumerate`](../syntax/enumerate.md) gives both at once, which is exactly the pairing the argument needs — index `i` and value `nums[i]` are two independent members of the pool being XORed.

`res ^= i ^ num` folds in two values per iteration. XOR's associativity means `res ^ (i ^ num)` equals `(res ^ i) ^ num`, so the grouping is free.

After the loop, `res` holds the XOR of **every index `0..n-1`, every value, and `n`** — in which each number `0..n` appears exactly twice except the missing one.
→ [enumerate](../syntax/enumerate.md) · [bitwise-operators](../syntax/bitwise-operators.md) · [for-loop](../syntax/for-loop.md)

```python
return res
```
Every paired number has cancelled to 0. What survives is the single unpaired value — the missing number.
→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def missingNumber(self, nums: List[int]) -> int:

        res = len(nums)   # accounts for index n, which has no matching nums index

        for i, num in enumerate(nums):
            res ^= i ^ num
        return res
```
</details>

**Trace it** — `nums = [3, 0, 1]`, so `n = 3` and the missing number should be 2.

Seed: `res = 3`.

| `i` | `num` | `i ^ num` | `res` before | `res` after |
|---|---|---|---|---|
| — | — | — | — | **3** (seed) |
| 0 | 3 | `0 ^ 3` = 3 | 3 | `3 ^ 3` = **0** |
| 1 | 0 | `1 ^ 0` = 1 | 0 | `0 ^ 1` = **1** |
| 2 | 1 | `2 ^ 1` = 3 | 1 | `1 ^ 3` = **2** |

Return **2** ✅

Seen as one flat expression, the cancellation is clearer:

```
3 ^ (0^3) ^ (1^0) ^ (2^1)
= (3^3) ^ (0^0) ^ (1^1) ^ 2      regrouped
= 0 ^ 0 ^ 0 ^ 2
= 2 ✓
```

Every number **except 2** appears exactly twice — the 3 from the seed pairs with the value 3, the index 0 pairs with the value 0, the index 1 pairs with the value 1. **Only index 2 has no matching value**, because 2 is the number that's absent.

**And the case where the missing number is `n`** — `nums = [0, 1]`, n = 2:

| `i` | `num` | `res` after |
|---|---|---|
| — | — | **2** (seed) |
| 0 | 0 | `2 ^ 0 ^ 0` = **2** |
| 1 | 1 | `2 ^ 1 ^ 1` = **2** |

Return **2** ✅

**This is the case the seed exists for.** Every index-value pair cancels itself immediately, and the seeded `n` passes straight through untouched. Without the seed the answer would have been 0 — badly wrong.

**And the larger example** — `nums = [9,6,4,2,3,5,7,0,1]`, n = 9:

Indices contribute `0..8`, the seed contributes `9`, so the pool holds `0..9` once from that side. The values contribute `{9,6,4,2,3,5,7,0,1}` — every number from 0 to 9 **except 8**. So 8 is the only value appearing an odd number of times.

Return **8** ✅

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

- One pass over the array → **n iterations**.
- Each iteration does two XORs and an assignment — **O(1)**.
- **O(n)** total.

At n = 10⁴ that's ten thousand XORs. Instant.

**This is optimal.** Every element must be read: the missing number could be any value, and skipping an element means you can't rule out the value it holds. **Ω(n)** is a lower bound.

**No early exit exists**, and none is possible — the answer isn't determined until every element has contributed. Unlike a search, there's no point at which you can stop early, so the bound is tight rather than an upper limit.

**Against the alternatives:** the hash-set version is also O(n) time but O(n) space. Sorting is **O(n log n)**, which fails the follow-up's requirement. The Gauss-sum version is O(n) — one pass to sum — and identical in complexity to this.

**Constant factor:** XOR is a single CPU instruction, and this does two per element. That's about as tight as an O(n) pass gets — meaningfully faster in practice than the hash-set version, which pays for hashing and memory traffic on every element.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — a single integer accumulator, regardless of input size. The array isn't modified and nothing is allocated.

| Approach | Space | Why |
|---|---|---|
| Hash set | **O(n)** | Every value stored |
| Sorting | O(1) in place | But O(n log n) time |
| Cyclic sort | O(1) | Mutates the input |
| Gauss sum | **O(1)** | One accumulator — but risks overflow in fixed-width languages |
| **XOR** | **O(1)** | One accumulator, no overflow risk |

**This is what the follow-up is testing.** The hash set is the natural first answer and it's O(n) space, so the constraint is what pushes you toward an algebraic identity — the same shape as [Single Number](136-single-number.md), where the space limit similarly rules out the obvious structure.

**Why one integer suffices:** the accumulator doesn't record *which* numbers have been seen, only their cumulative XOR. **A number appearing twice reverts the accumulator to its prior state**, so all the bookkeeping a set would do is absorbed into the algebra.

That's the reusable principle from this pair of problems: **when an operation is self-inverse, replace "remember what you've seen" with "accumulate and let it cancel."**

**The overflow point, restated as a space-adjacent concern:** the XOR accumulator can never exceed the largest input value, since XOR is bitwise. The sum accumulator grows to roughly n²/2. In Python both are fine; in a 32-bit language the sum can overflow at large n while XOR cannot — **which is the practical reason to prefer XOR even though both are O(1).**

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The array has n values drawn from a range of n+1 numbers, so exactly one is missing. The key observation is that the indices give me `0` through `n−1`, and the values give me `0` through `n` minus the missing one. So if I pool indices and values together, every number appears twice except the missing one — which is [Single Number](136-single-number.md), and XOR is the tool. I seed the accumulator with `n` because the indices only reach `n−1`, so `n` needs injecting by hand — and that seed is exactly what carries the answer when the missing number *is* n. Then I XOR each index and each value in; everything pairs off and the missing number survives. O(n) time, O(1) space. There's also a Gauss-sum version — `n(n+1)/2 − sum(nums)` — which is shorter, but the sum grows quadratically and can overflow in a fixed-width language, while XOR never exceeds the largest input."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why seed with `len(nums)`?" | Indices run `0..n−1` but the value range runs `0..n`, so `n` never enters via an index. Seeding injects it. Without it, `[0,1]` returns 0 instead of 2. |
| "Is there a simpler solution?" | `n(n+1)/2 − sum(nums)` — Gauss's formula minus the actual sum. Same complexity and shorter. |
| "Then why prefer XOR?" | Overflow. The sum grows like n²/2 and can exceed a 32-bit int for large n, even though the answer is small. XOR is bitwise and never exceeds the largest input. |
| "What if two numbers were missing?" | XOR everything to get `a ^ b`, isolate any set bit with `x & -x`, then partition the pool by that bit — `a` and `b` land in different groups, and XORing each group recovers both. |
| "What if there were duplicates?" | The pairing argument breaks — XOR relies on each value appearing exactly once. That's [Find the Duplicate Number](287-find-the-duplicate-number.md), which needs Floyd's cycle detection. |
| "Solve it with cyclic sort." | Swap each value to the index matching its value, then scan for the first index where `nums[i] != i`. O(n)/O(1), but it mutates the input. |
| "Does array order matter?" | No — XOR is commutative and associative, so any permutation gives the same result. |
| "What if the range were `[1, n]` instead?" | Seed differently: XOR in every value from 1 to n, or adjust the sum formula. The structure is unchanged. |

**Traps:**
- **Forgetting to seed with `n`.** The defining bug — the answer comes out wrong whenever the missing number is `n`, and `[0,1]` catches it immediately.
- Seeding with 0 and expecting the loop to handle everything.
- Using `+` instead of `^` and expecting cancellation — addition isn't self-inverse.
- Reaching for a hash set and stopping there, without noticing the space follow-up.
- Assuming the array is sorted. It isn't, and it doesn't need to be.
- In a fixed-width language, using the sum formula without considering that `n(n+1)/2` can overflow.

**This same move shows up in:** [Single Number](136-single-number.md) (the same XOR-cancellation argument — this problem is that one with indices supplying the partners) · [Sum of Two Integers](371-sum-of-two-integers.md) (XOR as arithmetic without carry) · [Find the Duplicate Number](287-find-the-duplicate-number.md) (the same range-and-array setup, but with a duplicate instead of a gap, needing a different technique) · [Contains Duplicate](217-contains-duplicate.md) (the hash-set approach the space constraint rules out here).

</details>

---
