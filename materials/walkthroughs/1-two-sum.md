# 1. Two Sum

**Easy** · [LeetCode](https://leetcode.com/problems/two-sum/) · [Solution file (no hints)](../../problems/0001-0499/1.py)

[📖 01. Arrays & Hashing lesson](../learning/01-arrays-hashing.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 01. Arrays & Hashing problems](../rmap-practice/01-arrays-hashing.md)

---

Given an array of integers `nums` and an integer `target`, return the **indices** of the two numbers that add up to `target`. Exactly one valid answer exists, and you may not use the same element twice.

```
nums = [2, 7, 11, 15], target = 9   →  [0, 1]     (2 + 7)
nums = [3, 2, 4],      target = 6   →  [1, 2]     (2 + 4)
nums = [3, 3],         target = 6   →  [0, 1]
```

**Constraints:** `2 <= nums.length <= 10⁴` · `-10⁹ <= nums[i], target <= 10⁹` · exactly one valid answer · **follow-up: can you do it in less than O(n²)?**

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "return the **indices**" | Not the values — **positions**. A structure that only stores values (a set) can't answer this; you need value → index |
| "two numbers that **add up to target**" | For any number `x`, its partner is forced: `target - x`. This is a **complement lookup**, not a search for an unknown |
| "**exactly one** valid answer" | No tie-breaking, no collecting results. You can return the instant you find it |
| "not the same element twice" | `nums[i] + nums[i]` is illegal — the two indices must differ |
| "`[3, 3]` → `[0, 1]`" | **Duplicate values are legal.** Whatever you build must not collapse them into one |
| "less than O(n²)?" | The problem is *telling you* the nested loop is the wrong answer |
| nothing about sortedness | Unsorted — but note you're asked for indices, so sorting would **destroy the answer** unless you track originals |

The reframe that cracks it: don't hunt for *a pair*. Walk the array once and, at each number, ask a question with a single definite answer — **"have I already seen `target - num`?"**

🤔 **Before you open the next section:** you need to look up a value and get back *where it was*. Which structure does that in O(1), and how does it differ from the one [Contains Duplicate](217-contains-duplicate.md) used?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Brute force | Every pair `(i, j)`, check the sum | O(n²) | O(1) | ❌ The follow-up explicitly rules it out |
| Sort + two pointers | Sort, then converge from both ends | O(n log n) | O(n) | ⚠️ Sorting scrambles the indices — you'd have to pair each value with its original position first |
| Hash **set** | Store seen values, test for the complement | O(n) | O(n) | ❌ Tells you the partner *exists*, not **where**. Wrong shape for this output |
| Hash **map** | Store value → index; look up the complement | O(n) | O(n) | ✅ |

**The decision: a [hash map](../data-structures/hashmap.md) from value → index.**

This is the direct upgrade from [Contains Duplicate](217-contains-duplicate.md), and the difference is exactly the lesson: **a set answers "does it exist?", a map answers "where / how many?"** Two Sum wants a position, so it must be a map.

**Why not sort + two pointers?** It's the right tool for the sorted variant ([Two Sum II](167-two-sum-ii-input-array-is-sorted.md), where it gives O(1) space). Here the array is unsorted and the answer *is* the indices, so sorting throws away the very thing you're returning. You can rescue it by sorting `(value, index)` pairs — but that's more work and more code for a worse complexity.

**The general move:** you're repeatedly *searching* for a value you may have already seen. That smell always points at a hash structure — see the pattern table in [how-to-approach-a-problem](../guides/how-to-approach-a-problem.md).

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
hashmap = {}
```

The memory: **value → the index it appeared at**. Note the direction — the value is the key, because the value is what you'll be searching *by*.
→ [dict-basics](../syntax/dict-basics.md)

```python
for i, num in enumerate(nums):
```

One pass, and `enumerate` hands you the index and the value together. You need both: the value to compute the complement, the index to build the answer.
→ [enumerate](../syntax/enumerate.md) · [for-loop](../syntax/for-loop.md) · [tuple-unpacking](../syntax/tuple-unpacking.md)

```python
    diff = target - num
```

The complement — the *exact* number that would complete the pair with `num`. This line is the whole idea: the second number was never unknown, it's fully determined by the first.
→ [arithmetic-operators](../syntax/arithmetic-operators.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
    if diff in hashmap:
        return [hashmap[diff], i]
```

The lookup. If the complement was recorded earlier, we're done — `hashmap[diff]` is *where* it was, `i` is where we are now. Since `diff` was stored on a previous iteration, its index is strictly smaller, so the pair comes out in ascending order for free.
→ [membership-operators](../syntax/membership-operators.md) · [if-return](../syntax/if-return.md)

```python
    hashmap[num] = i
```

Record the current number **after** the check. That ordering is what makes "you may not use the same element twice" impossible to violate: at check time the map holds only *earlier* elements, so `num` can never match itself. Move this line above the `if` and `target = 6` with `nums = [3, ...]` would happily return `[0, 0]`.

It also explains why duplicates are safe. A later `3` overwrites the earlier one's index, but only *after* every earlier lookup has already had its chance — and since exactly one answer exists, the overwrite can't cost you the solution.
→ [dict-basics](../syntax/dict-basics.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:

        hashmap = {}

        for i, num in enumerate(nums):
            diff = target - num
            if diff in hashmap:
                return [hashmap[diff], i]
            hashmap[num] = i
```

</details>

**Trace it** — `nums = [2, 7, 11, 15]`, `target = 9`:

| `i` | `num` | `diff` | Map before | In it? | Action |
|---|---|---|---|---|---|
| 0 | 2 | 7 | `{}` | no | store `2 → 0` |
| 1 | 7 | 2 | `{2: 0}` | **yes** | `return [0, 1]` |

Note there's no `return` after the loop — the problem guarantees a solution exists, so the loop always exits early. In production code you'd return `[]` or raise.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

- One pass → at most n iterations.
- Per iteration: one subtraction, one hash lookup, one insert — all **O(1) average**.
- n × O(1) = **O(n)**.

**Compare to the brute force:** O(n²) → O(n). At n = 10⁴ that's 10⁸ operations down to 10⁴ — the difference between "too slow" and instant.

**Best case:** the answer is the first two elements and you return on iteration two.

**The honest asterisk:** hash operations are O(1) *average*. Worst case, with everything colliding into one bucket, each degrades to O(n) and the whole thing to O(n²) — the same caveat as every hash-based solution.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n).**

The map is the only thing that grows, and in the worst case — the answer lives at the very end — it holds nearly all n entries before you find it.

This is the [arrays & hashing](../learning/01-arrays-hashing.md) trade again: **O(n) memory bought you a factor of n in time.**

**Where it can be avoided:** if the array were sorted, two pointers would solve it in O(1) extra space — no memory needed, because the sorted order itself tells you which way to move. That's [Two Sum II](167-two-sum-ii-input-array-is-sorted.md), and it's a neat demonstration that *structure in the input* can substitute for memory.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The brute force checks every pair — O(n²). But the second number isn't really unknown: for any `num`, the partner has to be `target - num`. So the repeated work is *searching* for that complement, and I'll trade memory for lookup speed with a hash map from value to index. One pass; at each element I check whether the complement was already stored, and store the current one afterward — which also guarantees I never reuse an element. O(n) time, O(n) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "What if the array is sorted?" | Two pointers from both ends — move left in when the sum is too small, right in when too big. O(n) time, **O(1) space**. See [Two Sum II](167-two-sum-ii-input-array-is-sorted.md). |
| "What if there are multiple answers?" | Don't return early; collect all pairs. You'd store a *list* of indices per value, since duplicates now matter. |
| "What about three numbers summing to target?" | Sort, fix one element, and two-pointer the rest — O(n²). That's [3Sum](15-3sum.md). |
| "What if no answer exists?" | Fall out of the loop and return `[]`. The guarantee here is a convenience of the problem, not a property of the algorithm. |
| "Can you do it in one pass?" | This *is* one pass. The common two-pass version builds the whole map first, then scans — same complexity, but it needs an `i != j` guard the one-pass version gets for free. |

**Traps:**

- **Storing before checking.** The #1 bug — an element pairs with itself and you return `[i, i]`.
- **Reaching for a set** because Contains Duplicate used one. A set can't tell you *where*.
- **Sorting the array** without preserving original indices — you'll return positions into the sorted array, which are not the answer.
- **Returning the values instead of the indices.** Re-read the output spec; this trips people up under pressure.
- **Assuming duplicates break it.** They don't — but be able to explain *why* (the check happens before the overwrite).

**This same move shows up in:** [Contains Duplicate](217-contains-duplicate.md) (the set version, when position doesn't matter) · [Two Sum II](167-two-sum-ii-input-array-is-sorted.md) (sorted → two pointers, O(1) space) · [3Sum](15-3sum.md) (fix one, two-sum the rest) · [Longest Consecutive Sequence](128-longest-consecutive-sequence.md) (asking "have I seen this value?" to find run starts).

</details>
