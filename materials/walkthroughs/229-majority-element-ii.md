# 229. Majority Element II

**Medium** · [LeetCode](https://leetcode.com/problems/majority-element-ii/) · [Solution file (no hints)](../../problems/0001-0499/229.py)

[📖 01. Arrays & Hashing lesson](../learning/01-arrays-hashing.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 01. Arrays & Hashing problems](../rmap-practice/01-arrays-hashing.md)

---

Given an integer array `nums` of size `n`, return **all elements that appear more than `⌊n / 3⌋` times**. Follow-up: do it in **O(n) time and O(1) space**.

```
nums = [3, 2, 3]                    →  [3]
nums = [1]                          →  [1]
nums = [1, 2]                       →  [1, 2]
nums = [1, 1, 1, 3, 3, 2, 2, 2]     →  [1, 2]
```

**Constraints:** `1 <= nums.length <= 5 * 10⁴` · `-10⁹ <= nums[i] <= 10⁹`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "more than `⌊n/3⌋` times" | Strictly more than a third. Exactly a third doesn't count |
| "all elements" | The answer is a *list*, not a single value |
| "O(1) space" | A frequency map (O(n)) is the easy answer but the follow-up rules it out |
| "more than a third" | There's a **ceiling on how many can qualify**. Three elements each above `n/3` would total more than `n`. So **at most 2** answers exist |

That last row is the whole trick. If at most 2 values can qualify, you only need to track **two candidates**, not a whole map.

The ancestor is [Majority Element](169-majority-element.md) (more than `n/2`, at most 1 answer, Boyer-Moore voting with one candidate). This is the same idea with two.

🤔 **Before you open the next section:** in the one-candidate vote, a different element *cancels* one vote. With two candidates, an element that matches neither one cancels how many votes, and from whom?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Time | Space | Verdict |
|---|---|---|---|
| Count every pair of values | O(n²) | O(1) | ❌ Too slow |
| Hash map of counts, then filter | O(n) | O(n) | ⚠️ Correct and a fine first answer, but not the O(1)-space follow-up |
| Sort and scan runs | O(n log n) | O(1) to O(n) | ⚠️ Meets neither bound cleanly |
| **Boyer-Moore voting with 2 candidates** | **O(n)** | **O(1)** | ✅ |

**The decision: extended [Boyer-Moore voting](../algorithms/boyer-moore-voting.md).** Keep two candidates, each with a counter.

- Matches candidate 1 → its count goes up. Matches candidate 2 → its count goes up.
- A free slot (count 0) → the number takes it.
- Otherwise it matches neither and no slot is free → **decrement both counts**. Three distinct values just cancelled each other out (one of each).

Why does that work? Each cancellation removes three *different* values. A value that occurs more than `n/3` times can't be fully cancelled away, because each cancellation uses at most one copy of it and there are fewer than `n/3` cancellations. So every true answer survives as a candidate.

**Survival isn't proof.** The candidates are only *possible* answers. A second pass **counts** them to confirm. That verification is mandatory here (for the `n/2` version it's only skipped when a majority is guaranteed).

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
candidate1, candidate2 = None, None
count1, count2 = 0, 0
```

Two candidate slots and their vote counters. `None` means "nobody yet".
→ [none-type](../syntax/none-type.md) · [tuple-unpacking](../syntax/tuple-unpacking.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
for num in nums:
    if num == candidate1:
        count1 += 1
    elif num == candidate2:
        count2 += 1
    elif count1 == 0:
        candidate1, count1 = num, 1
    elif count2 == 0:
        candidate2, count2 = num, 1
    else:
        count1 -= 1
        count2 -= 1
```

**The order of these branches matters.** First check whether the number already belongs to a candidate and vote for it. Only if it doesn't, look for an empty slot. Only if both slots are full, cancel one vote from each.

If you checked for an empty slot *first*, a number equal to `candidate2` could be placed into slot 1, giving you the same value as both candidates.
→ [for-loop](../syntax/for-loop.md) · [elif-else](../syntax/elif-else.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
result = []
for candidate in (candidate1, candidate2):
    if candidate is not None and nums.count(candidate) > len(nums) // 3:
        result.append(candidate)
return result
```

**The verification pass.** The loop leaves two *possible* answers. Count each in the real array and keep only those above `n // 3`. The `is not None` guard handles inputs where a slot was never filled, for example `[1]`.
→ [list-methods](../syntax/list-methods.md) · [integer-division-modulo](../syntax/integer-division-modulo.md) · [identity-operators](../syntax/identity-operators.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def majorityElement(self, nums: List[int]) -> List[int]:
        candidate1, candidate2 = None, None
        count1, count2 = 0, 0

        for num in nums:
            if num == candidate1:
                count1 += 1
            elif num == candidate2:
                count2 += 1
            elif count1 == 0:
                candidate1, count1 = num, 1
            elif count2 == 0:
                candidate2, count2 = num, 1
            else:
                count1 -= 1
                count2 -= 1

        result = []
        for candidate in (candidate1, candidate2):
            if candidate is not None and nums.count(candidate) > len(nums) // 3:
                result.append(candidate)
        return result
```

</details>

**Trace it.** `nums = [1, 1, 1, 3, 3, 2, 2, 2]`, `n // 3 = 2`:

| `num` | Action | `(cand1, count1)` | `(cand2, count2)` |
|---|---|---|---|
| 1 | slot 1 empty, take it | (1, 1) | (None, 0) |
| 1 | matches cand1 | (1, 2) | (None, 0) |
| 1 | matches cand1 | (1, 3) | (None, 0) |
| 3 | slot 2 empty, take it | (1, 3) | (3, 1) |
| 3 | matches cand2 | (1, 3) | (3, 2) |
| 2 | no match, no free slot: cancel | (1, 2) | (3, 1) |
| 2 | cancel | (1, 1) | (3, 0) |
| 2 | slot 2 free, take it | (1, 1) | (2, 1) |

Candidates are 1 and 2. Verify: `1` appears 3 times (> 2 ✅), `2` appears 3 times (> 2 ✅). Result `[1, 2]`. Note that `3` was a candidate for a while and got voted out.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).** One pass for voting and one pass per candidate for `.count` (two scans at most). That is about `3n` steps, which is still O(n).

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1).** Two candidates and two counters, regardless of `n`. The result list holds at most 2 values. The hash-map solution would use O(n).

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "More than a third means at most two elements can qualify, since three of them would exceed n. So I'll run Boyer-Moore voting with two candidates and two counters. A matching number votes for its candidate. Otherwise it takes a free slot. Otherwise it cancels one vote from each candidate, because three distinct values just eliminated each other. A true majority-over-a-third can't be fully cancelled, so it survives, but survivors are only candidates, so I count them in a second pass. O(n) time and O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "More than `n/k` times?" | Keep `k - 1` candidates, with the same cancel rule (the Misra-Gries algorithm). O(n·k) time, O(k) space |
| "Why is verification needed?" | Surviving the cancellations doesn't mean exceeding `n/3`. `[1, 2, 3]` ends with candidates `1` and `2`, but each appears once, which is not more than `3 // 3 = 1`. Both are wrong answers until the count says otherwise |
| "Simpler solution?" | A `Counter`, then filter. O(n) time, O(n) space. Offer it first, then upgrade |
| "The `n/2` version?" | [Majority Element](169-majority-element.md): one candidate |
| "Why is the order of the `if`s important?" | Match a candidate first, otherwise one value could end up in both slots |

**Traps:**

- **Checking for a free slot before checking for a match.** The same value gets stored twice.
- **Skipping the verification pass.** The candidates may be wrong.
- **Using `0` as the initial candidate.** `0` can be a real value in the input. Use `None`.
- **Counting `> n / 3` with float division** instead of `// 3`. They agree for `>`, but be deliberate.

**This same move shows up in:** [Majority Element](169-majority-element.md) (one candidate) · [Top K Frequent Elements](347-top-k-frequent-elements.md) (frequency when you want the top k, not a threshold) · [Single Number III](260-single-number-iii.md) (another "narrow it down to two" problem).

</details>

---
