# 560. Subarray Sum Equals K

**Medium** · [LeetCode](https://leetcode.com/problems/subarray-sum-equals-k/) · [Solution file (no hints)](../../problems/0500-0999/560.py)

[📖 01. Arrays & Hashing lesson](../learning/01-arrays-hashing.md) · [📖 Prefix sums](../learning/01b-prefix-sums.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 01. Arrays & Hashing problems](../rmap-practice/01-arrays-hashing.md)

---

Given an array of integers `nums` and an integer `k`, return the **total number of subarrays** whose sum equals `k`. A subarray is a contiguous, non-empty sequence.

```
nums = [1,1,1],   k = 2  →  2      ([1,1] at 0-1 and at 1-2)
nums = [1,2,3],   k = 3  →  2      ([1,2] and [3])
nums = [1,-1,0],  k = 0  →  3      ([1,-1], [0], [1,-1,0])
```

**Constraints:** `1 <= nums.length <= 2·10⁴` · `-1000 <= nums[i] <= 1000` · `-10⁷ <= k <= 10⁷`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**subarray**" | **Contiguous.** Not a subsequence — you can't skip elements. So a subarray is fully described by its two endpoints |
| "**total number**" | Count them all. You cannot stop at the first, and you cannot double-count |
| `nums[i]` can be **negative** | ⚠️ **The single most important constraint.** It kills sliding window, and most wrong answers to this problem ignore it |
| `k` can be negative or zero | Your logic must not assume sums grow |
| `n` up to 2·10⁴ | O(n²) is 4·10⁸ — borderline-to-dead in Python. Aim for O(n) |
| non-empty subarrays | The empty subarray (sum 0) must not be counted — but, subtly, an *empty prefix* still needs representing |

**Why negatives break sliding window** — internalize this, because it's the trap:

A sliding window works when growing the window *monotonically* increases the sum and shrinking it decreases it. That lets you say "sum too big ⇒ shrink from the left." With negative numbers, extending the window can *decrease* the sum, so "too big" gives you no information about which direction to move. The whole basis for the technique is gone. If every value were positive, [Minimum Size Subarray Sum](209-minimum-size-subarray-sum.md) style windowing would work fine — here it does not.

So: contiguous ranges, arbitrary signs, need a count. That points straight at **prefix sums**.

The reframe that solves it — and it's worth deriving rather than memorizing:

> `sum(i..j)` = `prefix[j+1] - prefix[i]`
>
> We want `sum(i..j) == k`, i.e. `prefix[j+1] - prefix[i] == k`
>
> Rearrange: **`prefix[i] == prefix[j+1] - k`**

So standing at position `j` with running sum `curr`, the number of subarrays ending here equals **the number of earlier prefix sums equal to `curr - k`**. That's a counting question about things you've already seen — which is the [Two Sum](1-two-sum.md) move, and it means a hash map.

🤔 **Before you open the next section:** if you're at index `j` with running sum `curr`, what would an earlier prefix sum have to equal for the chunk between it and `j` to total exactly `k`?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Brute force | Every `(i, j)` pair, sum it | O(n³) | O(1) | ❌ Hopeless |
| Brute force + running sum | Every start `i`, extend `j` accumulating | O(n²) | O(1) | ⚠️ Correct; 4·10⁸ ops — too slow in Python |
| Prefix array + pair search | Build prefixes, then find pairs differing by `k` | O(n²) | O(n) | ❌ No better |
| Sliding window | Grow/shrink to hit `k` | — | — | ❌ **Wrong** — negatives break monotonicity |
| **Prefix sum + hash map** | Count earlier prefixes equal to `curr - k` | **O(n)** | O(n) | ✅ |

**The decision: a running prefix sum plus a [hash map](../data-structures/hashmap.md) of prefix-sum frequencies.**

The structure is exactly [Two Sum](1-two-sum.md), lifted from elements to prefix sums:

| | Two Sum | This problem |
|---|---|---|
| Walking over | elements | running prefix sums |
| Looking for | `target - num` | `curr - k` |
| Map stores | value → index | prefix sum → **how many times seen** |
| Returns | one pair | a **count** of pairs |

The one real difference: you need **counts**, not indices. Several different starting points can produce the same prefix sum, and *each one* is a distinct valid subarray. Storing only the most recent index would silently undercount.

**The `{0: 1}` initialization is essential.** It says: *before processing anything, the empty prefix with sum 0 has been seen once.* That's what lets a subarray starting at index 0 be counted — when `curr == k`, we look up `curr - k == 0` and find that seeded 1.

Drop it and you undercount every subarray that begins at the start of the array. On `nums = [1,1,1], k = 2` you'd get 1 instead of 2. It's the same sentinel idea as the leading zero in [Range Sum Query](303-range-sum-query-immutable.md) — *"the sum of nothing is zero, and nothing is a legitimate prefix."*

**Why order matters inside the loop.** Look up `curr - k` **before** recording `curr`. Otherwise, when `k == 0`, the current prefix would match itself and you'd count the empty subarray. Getting this ordering right is the same discipline as checking-before-inserting in [Contains Duplicate](217-contains-duplicate.md).

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
count = 0
curr_sum = 0
prefix_sums = {0: 1}
```

Three pieces of state:

- `count` — the running answer.
- `curr_sum` — the prefix sum up to and including the current element. Note we never build the whole prefix *array*; a single scalar is enough, since we only ever need the current value.
- `prefix_sums` — maps a prefix sum → **how many times it has occurred**. Seeded with `{0: 1}` for the empty prefix, as above.

→ [dict-basics](../syntax/dict-basics.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
for num in nums:
    curr_sum += num
```

Extend the prefix by one element. After this line, `curr_sum` is the sum of everything from index 0 through the current position.
→ [for-loop](../syntax/for-loop.md)

```python
    if (curr_sum - k) in prefix_sums:
        count += prefix_sums[curr_sum - k]
```

**The heart of it.** Every earlier position whose prefix sum was `curr_sum - k` marks the start of a subarray ending here that sums to exactly `k`.

`count += prefix_sums[...]` — add the **frequency**, not 1. If three earlier prefixes shared that value, three distinct subarrays end at this position. Writing `count += 1` here is the classic undercount bug.
→ [membership-operators](../syntax/membership-operators.md) · [dict-methods](../syntax/dict-methods.md)

```python
    prefix_sums[curr_sum] = prefix_sums.get(curr_sum, 0) + 1
```

Record the current prefix sum for future positions to find. **After** the lookup — which is what prevents a zero-length match when `k == 0`.

`.get(curr_sum, 0)` handles first-sighting and repeat in one line.
→ [dict-methods](../syntax/dict-methods.md)

```python
return count
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:

        count = 0
        curr_sum = 0
        prefix_sums = {0: 1}

        for num in nums:
            curr_sum += num

            if (curr_sum - k) in prefix_sums:
                count += prefix_sums[curr_sum - k]

            prefix_sums[curr_sum] = prefix_sums.get(curr_sum, 0) + 1

        return count
```

</details>

**Trace it** — `nums = [1, 1, 1]`, `k = 2`:

| `num` | `curr_sum` | look for `curr_sum - k` | found? | `count` | map after |
|---|---|---|---|---|---|
| — | 0 | — | — | 0 | `{0: 1}` |
| 1 | 1 | −1 | no | 0 | `{0:1, 1:1}` |
| 1 | 2 | 0 | **yes ×1** | **1** | `{0:1, 1:1, 2:1}` |
| 1 | 3 | 1 | **yes ×1** | **2** | `{0:1, 1:1, 2:1, 3:1}` |

Answer **2** ✅ — the subarrays `[1,1]` at indices 0–1 and 1–2.

**A trace that shows why counts matter** — `nums = [1, -1, 0]`, `k = 0`:

| `num` | `curr_sum` | look for `0` | found | `count` | map after |
|---|---|---|---|---|---|
| — | 0 | — | — | 0 | `{0: 1}` |
| 1 | 1 | 1 | no | 0 | `{0:1, 1:1}` |
| −1 | 0 | 0 | **×1** | 1 | `{0:2, 1:1}` |
| 0 | 0 | 0 | **×2** | **3** | `{0:3, 1:1}` |

Answer **3** ✅ — `[1,-1]`, `[0]`, and `[1,-1,0]`. On the last row the lookup returns **2**, not 1, and that's the whole reason the map stores frequencies. `count += 1` would have returned 2 and looked plausible.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

One pass, and each iteration does a fixed amount of work: one addition, one membership test, one lookup, one insert — all O(1) average on a hash map.

There's no nested loop and no early exit; the cost is n regardless of the input's shape.

**Compare to the O(n²) brute force:** at n = 2·10⁴ that's 4·10⁸ operations. In C++ that might scrape through; in Python it's a timeout. The hash map converts "search all earlier positions" into "look it up," which is the same trade as [Two Sum](1-two-sum.md) — and the same reason both problems exist.

**The usual asterisk:** hash operations are O(1) *average*. Adversarial collisions could degrade it toward O(n²), but Python's dict randomizes hashing for strings and uses well-behaved integer hashing, so this is theoretical here.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n).**

The map holds one entry per **distinct** prefix sum. Worst case every prefix is unique — e.g. all-positive input, where sums strictly increase — giving n + 1 entries.

Best case is O(1): on `[0, 0, 0, …]` every prefix is 0, so the map holds a single key with a large count.

**Can you do better?** Not in general. The prefix sums you might need to match against are unbounded in variety, so you have to remember them. The O(n²) brute force is O(1) space — that's the trade, and it's the standard one:

| | Time | Space |
|---|---|---|
| Brute force | O(n²) | O(1) |
| **Prefix + hash map** | **O(n)** | O(n) |

**The special case worth knowing:** if all values were guaranteed **positive**, prefix sums would be strictly increasing, and you could use a sliding window in **O(n) time and O(1) space** — strictly better. The negatives are what force the hash map. Spotting that the sign constraint dictates the technique is exactly the reasoning this problem is testing.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Values can be negative, so a sliding window won't work — growing the window doesn't monotonically increase the sum, so there's no rule for when to shrink. Instead I'll use prefix sums: `sum(i..j) = prefix[j+1] - prefix[i]`, so a subarray ending at `j` sums to `k` exactly when some earlier prefix equals `curr - k`. I keep a running sum and a hash map from prefix sum to **how many times** I've seen it, adding that frequency to the count each step. I seed the map with `{0: 1}` for the empty prefix so subarrays starting at index 0 are counted, and I look up before inserting so a zero-length match can't occur when `k = 0`. O(n) time, O(n) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "What if all numbers are **positive**?" | Sliding window works — O(n) time, **O(1) space**. Strictly better. The negatives are what force the map. |
| "Return the **longest** such subarray instead." | Store prefix sum → **first** index seen (don't overwrite), then track `j - first_index`. Same as [Contiguous Array](525-contiguous-array.md). |
| "Return the actual subarrays." | Store prefix sum → list of indices. Space can blow up to O(n²) in the worst case. |
| "Why `{0: 1}`?" | It represents the empty prefix. Without it, any subarray starting at index 0 is missed — `[1,1,1], k=2` returns 1 instead of 2. |
| "Why look up before inserting?" | With `k = 0`, inserting first lets `curr` match itself, counting an empty subarray. |
| "Count subarrays **divisible by k**." | [LeetCode 974](https://leetcode.com/problems/subarray-sums-divisible-by-k/) — same skeleton, key on `curr % k` (careful with Python's sign handling on negatives). |
| "2-D version — submatrices summing to target?" | [LeetCode 1074](https://leetcode.com/problems/matrix-sum-queries/) — fix a pair of rows, collapse columns to 1-D, run this algorithm. O(rows² · cols). |
| "Subarray with sum **at most** k?" | Different problem — needs sorting/BIT over prefix sums, or a window if all values are positive. |

**Traps:**

- **`count += 1` instead of `count += frequency`.** Undercounts whenever a prefix sum repeats. The `[1,-1,0]` trace above is the minimal case that exposes it.
- **Omitting `{0: 1}`.** Misses every subarray anchored at index 0.
- **Inserting before looking up.** Counts spurious empty subarrays when `k = 0`.
- **Reaching for a sliding window.** The instinctive move for "contiguous subarray," and *wrong here* because of negatives. Check the sign constraint before choosing the technique.
- **Building the full prefix array.** Not wrong, just unnecessary — a single scalar suffices, since you only ever query the map, never the array.
- **Confusing subarray with subsequence.** Subarrays are contiguous; subsequences aren't. Counting subsequences summing to `k` is a completely different (and much harder) DP problem.

**This same move shows up in:** [Two Sum](1-two-sum.md) (the same "look for the complement in a hash map" structure) · [Contiguous Array](525-contiguous-array.md) (prefix sums over ±1, storing first index instead of counts) · [Range Sum Query - Immutable](303-range-sum-query-immutable.md) (the prefix-sum identity in its simplest form) · [Product of Array Except Self](238-product-of-array-except-self.md) (prefix accumulation from both directions).

</details>

---
