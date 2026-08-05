# 238. Product of Array Except Self

**Medium** · [LeetCode](https://leetcode.com/problems/product-of-array-except-self/) · [Solution file (no hints)](../../problems/0001-0499/238.py)

[📖 01. Arrays & Hashing lesson](../learning/01-arrays-hashing.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 01. Arrays & Hashing problems](../rmap-practice/01-arrays-hashing.md)

---

Given an integer array `nums`, return an array `answer` where `answer[i]` is the product of **all elements except `nums[i]`**.

You must write an algorithm that runs in **O(n)** time and **without using the division operator**.

```
nums = [1,2,3,4]    →  [24,12,8,6]
nums = [-1,1,0,-3,3] →  [0,0,9,0,0]
```

**Constraints:** `2 <= nums.length <= 10⁵` · `-30 <= nums[i] <= 30` · every prefix/suffix product fits in a 32-bit integer · **follow-up: O(1) extra space (the output array doesn't count)**

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "product of all elements **except `nums[i]`**" | For each position, you need everything **to the left** × everything **to the right**. Split it at `i` |
| "**without division**" | The obvious trick — total product ÷ `nums[i]` — is banned. And it would break on zeros anyway |
| "must run in **O(n)**" | The nested loop (recompute the product for every `i`) is O(n²) and explicitly ruled out |
| "**O(1) extra space** follow-up" | You're expected to reuse the output array as your scratch space rather than keep two helper arrays |
| the example contains a **0** | Deliberate. Test whatever you design against zeros — and note two zeros makes *every* answer 0 |
| n ≥ 2 | No single-element edge case to worry about |

The reframe: `answer[i] = (product of everything before i) × (product of everything after i)`.

Those are the **prefix product** and the **suffix product**. And the crucial observation — the one that makes it O(n) — is that consecutive prefixes are related: the prefix at `i+1` is just the prefix at `i` times `nums[i]`. So a running variable computes all n of them in **one pass**, no recomputation.

🤔 **Before you open the next section:** you need a left-product and a right-product at every index. How many passes over the array does that actually take, and do you need to store both?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Extra space | Verdict |
|---|---|---|---|---|
| Brute force | For each `i`, multiply every other element | O(n²) | O(1) | ❌ 10¹⁰ ops; violates the stated O(n) |
| Divide the total | Total product ÷ `nums[i]` | O(n) | O(1) | ❌ Banned — **and** it breaks on zeros |
| Prefix + suffix arrays | Store all prefixes, all suffixes, multiply pairwise | O(n) | O(n) | ⚠️ Correct and the clearest first draft |
| **Two passes, running variables** | Prefixes into `answer`, then fold suffixes in | **O(n)** | **O(1)** | ✅ |

**The decision: two passes with running products, writing into the output array.**

Pass one walks left→right putting the *prefix* product at each index. Pass two walks right→left multiplying in the *suffix* product. After both, every slot holds left × right — which is the answer.

**Why not division?** Beyond being banned, it's genuinely fragile: one zero makes every other answer a division by zero (you'd special-case counting the zeros), and two zeros makes everything 0. The interviewer's ban isn't arbitrary — it's steering you away from a brittle solution toward a robust one.

**Why not keep two arrays?** Nothing's wrong with it, and it's the right thing to write first — it makes the idea obvious. But you have to *return* an n-length array anyway, so it can double as your prefix scratch space; the suffix only ever needs one running number. That's the whole O(1) follow-up. **Write the two-array version if it helps you think, then collapse it.**

This is [prefix sums](../learning/01b-prefix-sums.md) with multiplication swapped in for addition — the same "precompute cumulative work once, reuse it everywhere" idea.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
answer = [1] * len(nums)
```

The output array, and also the scratch space. Seeded with `1` because 1 is the **identity for multiplication** — it's the "empty product", so a slot that's had nothing multiplied into it yet is correct as-is.
→ [list-basics](../syntax/list-basics.md)

*(`[1] * n` is safe here even though `[[]] * n` isn't — integers are immutable, so there's no shared-reference trap.)*

```python
prefix = 1
for i in range(len(nums)):
    answer[i] = prefix
    prefix *= nums[i]
```

Pass one, left to right. Read the two lines in order — **the write comes before the update**, and that's the whole subtlety: at the moment we write, `prefix` holds the product of everything *strictly before* `i`, which excludes `nums[i]` exactly as required. Then we fold `nums[i]` in so the next index sees it.

`prefix` starts at 1 because index 0 has nothing to its left.
→ [range-function](../syntax/range-function.md) · [for-loop](../syntax/for-loop.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
suffix = 1
for i in range(len(nums) - 1, -1, -1):
    answer[i] *= suffix
    suffix *= nums[i]
```

Pass two, right to left — `range(n-1, -1, -1)` counts down from the last index to 0 (the `-1` endpoint is excluded, so index 0 *is* visited).

Same shape mirrored: `*=` multiplies the suffix product into the prefix already sitting in `answer[i]`, then `suffix` absorbs `nums[i]` for the next step left. Again the write precedes the update, so `nums[i]` is never included in its own answer.
→ [range-function](../syntax/range-function.md)

```python
return answer
```

Every slot now holds `left product × right product`.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:

        answer = [1] * len(nums)

        prefix = 1
        for i in range(len(nums)):
            answer[i] = prefix
            prefix *= nums[i]

        suffix = 1
        for i in range(len(nums) - 1, -1, -1):
            answer[i] *= suffix
            suffix *= nums[i]

        return answer
```

</details>

**Trace it** — `nums = [1, 2, 3, 4]`:

```
after pass 1 (prefix products, left→right)
  i:        0     1     2     3
  answer: [ 1     1     2     6 ]        ← product of everything LEFT of i
  prefix:   1  →  1  →  2  →  6  → 24

after pass 2 (suffix products, right→left)
  i:        3     2     1     0
  answer: [ 1×24  1×12  2×4   6×1 ]  =  [24, 12, 8, 6]
  suffix:   1  →  4  →  12 →  24
```

Check index 1: everything left is `1`, everything right is `3×4=12` → `12`. ✅

**Zeros need no special handling** — `nums = [-1,1,0,-3,3]`: only index 2 has a non-zero product on both sides, so it gets `9`; every other index has the 0 on one side or the other and lands on 0. The algorithm handles it for free, which is exactly why it beats the division approach.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

- Allocating `answer`: O(n).
- Pass one: n iterations, one write and one multiply each → O(n).
- Pass two: another O(n).

O(n) + O(n) + O(n) = **O(n)**. Two sequential passes *add* — this is linear, not quadratic.

**Versus the brute force:** O(n²) → O(n). At n = 10⁵ that's 10¹⁰ operations down to 10⁵.

There's no early exit and no best case: every index needs both a prefix and a suffix, so all 2n steps always run.

**Why it's not O(n log n) or worse:** each pass does O(1) work per element because the running variable *carries* the accumulated product forward. The brute force is slow precisely because it recomputes that accumulation from scratch at every index — the same repeated work that [prefix sums](../learning/01b-prefix-sums.md) exists to eliminate.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1) extra</summary>

**O(1) extra space** — which satisfies the follow-up.

`answer` is O(n), but the problem states the **output array doesn't count** toward the space analysis. That's a standard convention: you're measuring *auxiliary* space, the memory you use beyond what you're obliged to return.

Beyond the output there are only two integers, `prefix` and `suffix`. Constant, regardless of n.

**How the two-array version compares:** keeping a full prefix array *and* a full suffix array is O(n) auxiliary — perfectly correct, just not the follow-up answer. The collapse works because (a) the output array is already n long and can hold prefixes on the way through, and (b) a suffix product only ever needs the single running value, never the whole history.

**Say the distinction explicitly in an interview.** "O(1) auxiliary space, not counting the output array" is precise; a bare "O(1)" invites the challenge *"but you allocated an n-element array."*

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The answer at each index is everything to its left times everything to its right. Recomputing those per index is O(n²), but consecutive prefixes differ by one factor, so a running variable gets me all of them in one pass. I'll do a left-to-right pass writing prefix products into the output array, then a right-to-left pass multiplying the suffix product in. The key detail in both passes is writing *before* updating the running product, which is what excludes `nums[i]` from its own answer. O(n) time, O(1) auxiliary space. I'm avoiding division deliberately — it's banned, and it would break on zeros anyway."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "What if division *were* allowed?" | Count the zeros. None → total ÷ `nums[i]`. Exactly one → only that index gets the product of the rest, everything else is 0. Two or more → all zeros. Notice how much messier that is. |
| "What about integer overflow?" | Here the constraints guarantee it fits in 32 bits. In a fixed-width language you'd need a wider type or modular arithmetic — Python's ints are arbitrary precision, so it's a non-issue. See [modular-arithmetic](../algorithms/modular-arithmetic.md). |
| "Sums instead of products?" | Same structure, `+` for `*` and 0 as the identity instead of 1 — that's literally [prefix sums](../learning/01b-prefix-sums.md). |
| "Answer range queries — product of any subarray?" | Precompute a prefix-product array and divide... which zeros break. Segment trees handle it robustly: [segment-tree](../data-structures/segment-tree.md). |
| "Can you do it in one pass?" | Not honestly — index 0 needs the product of everything to its right, which isn't knowable until you've seen the whole array. You can interleave both passes in one loop with two pointers, but that's still 2n work. |

**Traps:**

- **Updating the running product before writing.** The single most common bug: `nums[i]` ends up included in its own answer. Write, *then* update — in both passes.
- **Initializing to 0 instead of 1.** Multiplicative identity is 1; seed with 0 and every answer is 0.
- **`range(len(nums)-1, 0, -1)`** for the backward pass — stops at index 1 and silently never fixes index 0. The endpoint must be `-1`.
- **Special-casing zeros.** Not needed. If you're writing zero-handling logic, you've drifted back toward the division solution.
- **Claiming O(1) space without the caveat** about the output array.

**This same move shows up in:** [Prefix Sums](../learning/01b-prefix-sums.md) (the additive original) · [Maximum Subarray](53-maximum-subarray.md) (a running accumulator in one pass) · [Trapping Rain Water](42-trapping-rain-water.md) (max-so-far from the left *and* the right, combined per index — structurally the same two-pass idea).

</details>

---
