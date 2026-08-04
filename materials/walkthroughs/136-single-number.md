# 136. Single Number

**Easy** · [LeetCode](https://leetcode.com/problems/single-number/) · [Solution file (no hints)](../../problems/0001-0499/136.py)

[📖 18. Bit Manipulation lesson](../learning/18-bit-manipulation.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 18. Bit Manipulation problems](../rmap-practice/18-bit-manipulation.md)

---

Given a **non-empty** array of integers `nums`, every element appears **twice** except for one. Find that single one.

You must implement a solution with **linear runtime complexity** and use only **constant extra space**.

```
nums = [2,2,1]        →  1
nums = [4,1,2,1,2]    →  4
nums = [1]            →  1
```

**Constraints:** `1 <= nums.length <= 3 × 10⁴` · `-3 × 10⁴ <= nums[i] <= 3 × 10⁴` · each element appears twice except one, which appears once.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| every element appears **twice** except one | A very strong guarantee. Not "at most twice," not "some appear more" — **exactly** twice, which is what makes the trick work |
| "**linear** runtime" | O(n), so no sorting (O(n log n)) and no nested scanning |
| "**constant** extra space" | **This is the real constraint.** A hash set solves it in O(n) time trivially — but that's O(n) space, and it's explicitly ruled out |
| the array is non-empty | No empty-input edge case |
| values can be **negative** | Any solution must handle negatives correctly — worth checking against whatever trick you pick |

The two obvious solutions each satisfy exactly one requirement and fail the other. A **hash set** gives O(n) time but O(n) space. **Sorting** gives O(1) space (in place) but O(n log n) time. The problem demands both, which is a strong hint that some **algebraic property** is meant to do the work rather than a data structure.

So: what operation makes a pair of identical values disappear, costs nothing to store, and doesn't care about order?

**XOR.** Its three relevant properties:

```
a ^ a = 0          anything XORed with itself is zero
a ^ 0 = a          zero is the identity
a ^ b = b ^ a      commutative, and it's also associative
```

Put those together. XOR every element of the array into a running total. Because XOR is commutative and associative, **you can mentally reorder the operations however you like** — so group each pair together:

```
4 ^ 1 ^ 2 ^ 1 ^ 2
= 4 ^ (1 ^ 1) ^ (2 ^ 2)      regroup — allowed, since order doesn't matter
= 4 ^ 0 ^ 0
= 4
```

**Every pair annihilates itself to 0, and the lone value survives.** The array's actual order is irrelevant, which is why a single pass with no bookkeeping works.

🤔 **Before you open the next section:** the accumulator starts at `0`. Why is that the right starting value specifically — what would happen if it started at 1, and what does the choice have to do with `a ^ 0 = a`?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Nested scan | For each element, count its occurrences | O(n²) | O(1) | ❌ 9 × 10⁸ at the limit |
| Hash set | Add on first sight, remove on second; one element remains | O(n) | **O(n)** | ❌ Violates the space constraint |
| Sort, then scan pairs | Sort and compare adjacent elements | **O(n log n)** | O(1) | ❌ Violates the time constraint |
| Math: `2 × sum(set) − sum(nums)` | Each pair counted twice minus once leaves the single | O(n) | **O(n)** | ❌ The set is O(n) space |
| **XOR everything** | Pairs cancel; the loner survives | **O(n)** | **O(1)** | ✅ |

**The decision:** **XOR the whole array into a single accumulator.**

**Why XOR is uniquely suited here.** The problem needs an operation that is:

1. **Self-inverse** (`a ^ a = 0`) — so duplicates vanish without being tracked.
2. **Commutative and associative** — so the array order doesn't matter and no sorting is needed.
3. **Constant-space** — a single integer accumulator.

XOR is the only common operation with all three. Addition is commutative and associative but *not* self-inverse (`a + a = 2a`, not 0). Multiplication has the same problem. **XOR's self-inverse property is exactly the "cancel out a pair" behaviour the problem describes**, which is why the fit feels so exact — you're not adapting a tool, you're using the one that matches.

**Why `0` is the correct starting value** — the answer to section 1's question. XOR's identity element is 0, since `a ^ 0 = a`. Starting the accumulator at 0 means the first element passes through unchanged, so the accumulator is always exactly "the XOR of everything seen so far." Starting at 1 would leave a stray `^ 1` corrupting every bit position where 1 has a bit — the answer would come out wrong by exactly 1 in the lowest bit.

**Why negatives are fine.** Python's integers are arbitrary-precision with two's-complement semantics for bitwise ops, so `(-5) ^ (-5) == 0` just as it does for positives. The cancellation is purely bitwise and doesn't care about sign — worth verifying rather than assuming, since some bit tricks *do* break on negatives.

**Why the sum-based math trick fails the constraint.** `2 × sum(set(nums)) − sum(nums)` is genuinely clever and correct — but building the set costs O(n) space, which is the very thing being ruled out. It's worth mentioning as an alternative *if* the space constraint were lifted.

**The generalization worth knowing:** if every element appeared **three** times except one, XOR would no longer work (three copies leave one behind, not zero). That variant needs bit-counting modulo 3 — same spirit, different mechanism.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
res = 0
```
**The accumulator, seeded with XOR's identity element.**

`0` is correct and not arbitrary: since `a ^ 0 = a`, the first element enters unchanged, and the invariant *"`res` is the XOR of every element processed so far"* holds from the very first iteration.

It's also the correct answer for a hypothetical empty array — the XOR of nothing is 0 — which is a nice consistency check that the seed is the right one.
→ [variables-assignment](../syntax/variables-assignment.md) · [bitwise-operators](../syntax/bitwise-operators.md)

```python
for num in nums:
    res ^= num
```
**The entire algorithm.** XOR each element into the accumulator.

`res ^= num` is the in-place form of `res = res ^ num`. No conditionals, no lookups, no memory of which values have been seen — **the cancellation is automatic**, because a value XORed in twice reverts the accumulator to what it was before.

Iterating values rather than indices is enough here, since position is irrelevant. And because XOR is commutative and associative, **this loop would produce the same answer for any permutation of the input** — a useful property to state, as it explains why no sorting or grouping is needed.
→ [for-loop](../syntax/for-loop.md) · [bitwise-operators](../syntax/bitwise-operators.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
return res
```
Every paired value has cancelled to 0, so what remains is the single unpaired element XORed with 0 — which is itself.
→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def singleNumber(self, nums: List[int]) -> int:

        res = 0
        for num in nums:
            res ^= num
        return res
```
</details>

**Trace it** — `nums = [4, 1, 2, 1, 2]`

Showing the accumulator in binary makes the cancellation visible:

| step | `num` | `num` in binary | `res` before | `res` after | binary |
|---|---|---|---|---|---|
| — | — | — | — | **0** | `000` |
| 1 | 4 | `100` | 0 | **4** | `100` |
| 2 | 1 | `001` | 4 | **5** | `101` |
| 3 | 2 | `010` | 5 | **7** | `111` |
| 4 | 1 | `001` | 7 | **6** | `110` ← the 1 cancels out |
| 5 | 2 | `010` | 6 | **4** | `100` ← the 2 cancels out |

Return **4** ✅

Steps 2 and 4 are the mechanism: bringing in `1` set the lowest bit, and bringing in `1` again cleared it. Same for `2` at steps 3 and 5. **The accumulator wanders during the pass and lands back on exactly the unpaired value** — the intermediate values (5, 7, 6) are meaningless on their own.

**And a reordered version** — `nums = [1, 1, 2, 2, 4]`:

| `num` | `res` after |
|---|---|
| 1 | 1 |
| 1 | **0** ← pair cancels immediately |
| 2 | 2 |
| 2 | **0** ← pair cancels immediately |
| 4 | **4** |

Return **4** ✅ — same answer, and here the pairs cancel adjacently instead of at a distance. **Commutativity means both orderings are equivalent**, which is the property that lets the loop ignore structure entirely.

**And with negatives** — `nums = [-3, 5, -3]`:

| `num` | `res` after |
|---|---|
| −3 | −3 |
| 5 | −3 ^ 5 = **−8** |
| −3 | −8 ^ −3 = **5** |

Return **5** ✅ — the two-complement bit patterns cancel exactly as positives do.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

- One pass over the array → **n iterations**.
- Each iteration is a single XOR and an assignment — **O(1)** machine operations.
- **O(n)** total.

At n = 3 × 10⁴ that's thirty thousand XORs. Instant.

**This is optimal.** Every element must be examined: the single number could be anywhere, and skipping even one element means you might skip *it*. So **Ω(n)** is a hard lower bound, and O(n) meets it.

**No best/worst case distinction** — the loop always runs exactly n times with no early exit, so the bound is tight rather than an upper limit. Unlike, say, [Jump Game](55-jump-game.md), there's nothing to bail out of: you can't know the answer until every pair has had its chance to cancel.

**Against the alternatives:** the nested-scan version is **O(n²)** ≈ 9 × 10⁸. Sorting is **O(n log n)** — fast enough in practice but explicitly outside the stated requirement. The hash-set version matches O(n) time but loses on space.

**Constant factor:** XOR is a single CPU instruction, so this is about as fast as an O(n) pass gets — considerably faster in practice than the hash-set version, which pays for hashing and memory traffic on every element.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — a single integer accumulator, regardless of input size. Nothing is allocated; the input isn't modified.

| Approach | Space | Why |
|---|---|---|
| Hash set | **O(n)** | Up to n/2 entries before cancellation |
| `2 × sum(set) − sum(nums)` | **O(n)** | Building the set |
| Sorting | O(1) in place | But O(n log n) time |
| **XOR accumulator** | **O(1)** | One integer |

**This is the constraint the problem is really testing**, and it's why the hash set — the answer most people give first — doesn't qualify. Stating that explicitly is worth doing: *"a set gives O(n) time but O(n) space; the constraint rules it out, which points at an algebraic identity rather than a data structure."*

**Why one integer suffices:** the accumulator doesn't need to remember *which* values have been seen, only their cumulative XOR. **All the bookkeeping a hash set would do is absorbed into the algebra** — a pair's second occurrence undoes its first automatically, with no record that either happened.

That's the general lesson from this problem: **when an operation is self-inverse, you can replace "track what you've seen" with "accumulate and let it cancel."** The same idea drives [Missing Number](268-missing-number.md), where XORing indices against values cancels everything except the gap.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The obvious solution is a hash set — add on first sight, remove on second, and one element is left. That's O(n) time but O(n) space, and the constraint says constant space, which tells me a data structure isn't the intended answer. XOR is: it's self-inverse, so `a ^ a = 0`, and it's commutative and associative, so the order doesn't matter. XORing the whole array means every pair cancels itself out and only the unpaired value survives. I start the accumulator at 0 because that's XOR's identity — `a ^ 0 = a` — so the first element passes through unchanged. It works for negatives too, since the cancellation is purely bitwise. O(n) time, which is optimal since every element must be examined, and O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why does XOR work here?" | Three properties: `a ^ a = 0` makes pairs vanish, `a ^ 0 = a` makes 0 the right seed, and commutativity/associativity means the array order is irrelevant. |
| "Why start at 0?" | It's XOR's identity element. Starting anywhere else leaves that value permanently mixed into the result. |
| "What if every element appeared three times except one?" | XOR breaks — three copies leave one behind. You'd count set bits at each position modulo 3, or use two accumulators tracking "seen once" and "seen twice." |
| "What if **two** elements appeared once?" | XOR everything to get `a ^ b`. Isolate any set bit of that (`x & -x` gives the lowest), then partition the array by that bit — `a` and `b` land in different groups, and XORing each group separately recovers both. |
| "Can you do it without bit manipulation?" | `2 × sum(set(nums)) − sum(nums)` works, since each distinct value is counted twice and each occurrence once. But the set costs O(n) space. |
| "Does it work with negative numbers?" | Yes — XOR operates on two's-complement bit patterns, and identical patterns cancel regardless of sign. |
| "What if the array were empty?" | It returns 0, which is arguably the right answer (the XOR of nothing). The constraints guarantee non-empty anyway. |
| "Why is a hash set worse if both are O(n) time?" | Space, and constant factors — XOR is one CPU instruction per element, while hashing involves computing a hash and touching memory. |

**Traps:**
- **Initializing the accumulator to `nums[0]` and starting the loop at index 1.** Correct, but only by accident — and it breaks on an empty array. Seeding with 0 is cleaner and always right.
- **Initializing to 1** or any non-zero value — corrupts every bit that value occupies.
- Using `+` instead of `^`, hoping pairs cancel. Addition isn't self-inverse; `a + a = 2a`.
- Reaching for a hash set and stopping there, without noticing the space constraint.
- Assuming the array is sorted or that pairs are adjacent — neither is guaranteed, and neither matters.
- Trying to track which values have been seen. The whole point is that the algebra removes that need.

**This same move shows up in:** [Missing Number](268-missing-number.md) (XOR indices against values so everything cancels except the gap) · [Sum of Two Integers](371-sum-of-two-integers.md) (XOR as addition-without-carry) · [Number of 1 Bits](191-number-of-1-bits.md) (a bitwise identity replacing an explicit loop over bits) · [Contains Duplicate](217-contains-duplicate.md) (the hash-set approach this problem's constraint deliberately rules out).

</details>

---
