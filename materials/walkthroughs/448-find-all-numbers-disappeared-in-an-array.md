# 448. Find All Numbers Disappeared in an Array

**Easy** · [LeetCode](https://leetcode.com/problems/find-all-numbers-disappeared-in-an-array/) · [Solution file (no hints)](../../problems/0001-0499/448.py)

[📖 01. Arrays & Hashing lesson](../learning/01-arrays-hashing.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 01. Arrays & Hashing problems](../rmap-practice/01-arrays-hashing.md)

---

Given an array `nums` of `n` integers where `nums[i]` is in the range `[1, n]`, return all the integers in `[1, n]` that **do not appear** in `nums`.

```
nums = [4,3,2,7,8,2,3,1]  →  [5,6]
nums = [1,1]              →  [2]
```

**Constraints:** `n == nums.length` · `1 <= n <= 10⁵` · `1 <= nums[i] <= n`

**Follow-up:** can you do it without extra space and in O(n) runtime? (The returned list doesn't count as extra space.)

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| `1 <= nums[i] <= n` | ⚠️ **The entire problem.** Values and indices live in the *same* range. That's an invitation to use the array as its own lookup table |
| `n == nums.length` | There are exactly as many slots as possible values — a perfect one-to-one correspondence, if nothing repeated |
| "do not appear" | Set difference: `{1..n}` minus `{what's present}` |
| duplicates are allowed | `[1,1]` has two 1s and zero 2s. Every duplicate implies a missing value, and vice versa |
| `n` up to 10⁵ | O(n²) is 10¹⁰ — dead. Need O(n) or O(n log n) |
| follow-up: **no extra space** | The real challenge. The obvious solutions all cost O(n) memory |

The naive solutions are easy and correct: a set of what's present, then test `1..n` against it. That's O(n) time and O(n) space, and it's a perfectly good first answer.

But the follow-up is where the problem earns its keep. And the unlock is the constraint in row one:

> **Every value is a valid index (after subtracting 1). So the array can serve as its own hash table.**

You don't need a separate structure to record "I saw the value `v`" — you can record it *inside `nums` itself*, at position `v - 1`. The only question is how to mark a slot without destroying the value living there, since you still need to read it.

🤔 **Before you open the next section:** all values are guaranteed **positive**. What's a reversible way to mark a slot that leaves the original number recoverable?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Brute force | For each `v` in `1..n`, scan `nums` for it | O(n²) | O(1) | ❌ 10¹⁰ ops |
| Sort, then scan | Sort and walk looking for gaps | O(n log n) | O(1)\* | ⚠️ Correct, slower than needed |
| **Hash set** | Add everything, then test `1..n` | **O(n)** | O(n) | ✅ The obvious, defensible answer |
| Boolean array | `seen = [False] * (n+1)`, mark, then scan | O(n) | O(n) | ✅ Same idea, better constants than a set |
| **Sign marking in place** | Negate `nums[|v|-1]` to mark `v` as seen | **O(n)** | **O(1)** | ✅✅ Answers the follow-up |

**Both are worth knowing, and the solution file carries both.**

**The hash set version** is what you write first. It's the direct translation of "set difference" into code, and nobody will fault it. Say it, code it, then offer the follow-up.

**The sign-marking version** is the answer to "no extra space." The trick has three parts:

1. **Values map to indices.** Value `v` corresponds to index `v - 1`. That's a bijection between `[1..n]` and `[0..n-1]`.
2. **Signs are a free bit of storage.** Every value starts positive, so the sign bit is unused — you can flip it to mean "the value at this index+1 was seen" without allocating anything.
3. **`abs()` recovers the data.** Because negation is reversible, a marked slot still tells you its original value. You mark and read from the same array without conflict.

After one pass, the slots still holding a **positive** value are exactly the ones never marked — and their positions, plus 1, are the missing numbers.

**Why not sort?** It works — walk the sorted array tracking which value you expect next. But it's O(n log n) when O(n) is available, and it destroys the input just as thoroughly as the sign trick does, so it doesn't even win on that front.

**The honest caveat:** sign marking **mutates the input**. If the caller needs `nums` intact afterward, this is off the table (or you restore it with a final `abs()` pass). Interviewers like to probe this — say it before they ask.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

**Approach A — hash set** (write this first)

```python
seen = set()
result = []

for num in nums:
    seen.add(num)
```

Record everything present. The set deduplicates for free, which matters because `[1,1]` must not confuse the count.
→ [set-basics](../syntax/set-basics.md) · [set-operations](../syntax/set-operations.md)

```python
for i in range(1, len(nums) + 1):
    if i not in seen:
        result.append(i)
return result
```

Walk the full range `1..n` — note `len(nums) + 1` as the stop, since `range` is exclusive at the top and `n` itself must be tested. Anything absent from the set is missing.
→ [range-function](../syntax/range-function.md) · [membership-operators](../syntax/membership-operators.md)

<details>
<summary>Approach A together</summary>

```python
class Solution:
    def findDisappearedNumbers(self, nums: List[int]) -> List[int]:

        seen = set()
        result = []

        for num in nums:
            seen.add(num)

        for i in range(1, len(nums) + 1):
            if i not in seen:
                result.append(i)

        return result
```

</details>

---

**Approach B — sign marking in place** (the O(1)-space follow-up)

```python
for num in nums:
    idx = abs(num) - 1
```

**`abs()` is mandatory, not decorative.** By the time you reach a given element, an *earlier* iteration may already have negated it. The magnitude is still the original value, so `abs(num)` recovers it; `- 1` converts value → index.
→ [math-module-basics](../syntax/math-module-basics.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
    if nums[idx] > 0:
        nums[idx] = -nums[idx]
```

Mark index `idx` as "the value `idx + 1` is present" by flipping its sign.

**The `> 0` guard handles duplicates.** With `[1,1]`, the second `1` would negate index 0 a second time and flip it *back* to positive — falsely reporting `1` as missing. Only ever negate an already-positive slot, so marking is **idempotent**.
→ [comparison-operators](../syntax/comparison-operators.md)

```python
result = []
for i in range(len(nums)):
    if nums[i] > 0:
        result.append(i + 1)
return result
```

Second pass: a still-positive slot was never marked, so nothing pointed at it, so the value `i + 1` never appeared. Convert index back to value with `+ 1`.
→ [list-methods](../syntax/list-methods.md)

<details>
<summary>Approach B together</summary>

```python
### Another solution that does not use extra space, but modifies the input array. ###
class Solution:
    def findDisappearedNumbers(self, nums: List[int]) -> List[int]:

        for num in nums:
            idx = abs(num) - 1
            if nums[idx] > 0:
                nums[idx] = -nums[idx]

        result = []
        for i in range(len(nums)):
            if nums[i] > 0:
                result.append(i + 1)

        return result
```

</details>

**Trace approach B** — `nums = [4,3,2,7,8,2,3,1]` (n = 8):

| `num` read | `idx` | `nums[idx]` before | Action | `nums` after |
|---|---|---|---|---|
| 4 | 3 | 7 | negate | `[4,3,2,-7,8,2,3,1]` |
| 3 | 2 | 2 | negate | `[4,3,-2,-7,8,2,3,1]` |
| −2 | 1 | 3 | negate | `[4,-3,-2,-7,8,2,3,1]` |
| −7 | 6 | 3 | negate | `[4,-3,-2,-7,8,2,-3,1]` |
| 8 | 7 | 1 | negate | `[4,-3,-2,-7,8,2,-3,-1]` |
| 2 | 1 | −3 | already ≤ 0, skip | unchanged |
| −3 | 2 | −2 | already ≤ 0, skip | unchanged |
| −1 | 0 | 4 | negate | `[-4,-3,-2,-7,8,2,-3,-1]` |

Final scan — positive slots are indices **4** and **5**, so the answer is `[5, 6]` ✅

Watch rows 3, 4, 7, 8: the value being *read* is already negative, and `abs()` is the only reason those steps work at all.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n) for both approaches.** Two linear passes each — 2n steps, which is still O(n).

- **Hash set:** n inserts plus n membership tests, each O(1) *average*. Carries the usual hashing asterisk (adversarial collisions degrade it).
- **Sign marking:** n negations plus n sign checks, all pure integer arithmetic and array indexing. **No hashing at all**, so it's O(n) unconditionally and noticeably faster in practice — no hash computation, no cache-hostile bucket chasing.

Both are optimal in order: you must read all n elements to know what's absent, and you may have to output up to n values.

Sorting-based alternatives are O(n log n) — fine to name, strictly worse.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n) vs O(1)</summary>

The problem's follow-up says the output list doesn't count, so measure only the *auxiliary* space:

| | Auxiliary space |
|---|---|
| Hash set | **O(n)** — up to n distinct keys |
| Boolean array | **O(n)** — n+1 booleans (smaller constant, same order) |
| **Sign marking** | **O(1)** — one index variable |

Sign marking achieves O(1) by exploiting something that was free all along: **every value is positive, so the sign bit is unused storage.** One bit per element, n elements, and it's already sitting inside the array you were given.

That's the generalizable idea, and it's worth stating in exactly these terms:

> **When values are constrained to the index range, the array can be its own hash table. Look for an unused bit — a sign, a range gap, a high bit — to record "seen" without allocating.**

**The cost:** the input is destroyed. Be upfront about it. If the caller needs `nums` preserved, either use the set version or add a restoring pass:

```python
for i in range(len(nums)):
    nums[i] = abs(nums[i])
```

The related trick is **cyclic sort** — swap each value to its home index rather than marking signs. It also gets O(1) space, doesn't rely on values being positive, and generalizes better; see [First Missing Positive](41-first-missing-positive.md), which needs exactly that.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The straightforward version is a set of everything present, then walk `1` to `n` and collect what's missing — O(n) time, O(n) space. For the O(1)-space follow-up I'd use the array itself: every value is in `[1, n]`, so value `v` maps to index `v-1`. I walk the array and negate `nums[abs(v)-1]` to mark `v` as seen — `abs` because the slot may already have been negated, and I only negate positives so duplicates don't un-mark. Then any slot still positive was never pointed at, so `i+1` is missing. O(n) time, O(1) extra space — but it mutates the input, which I'd confirm is acceptable."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "O(1) space?" | **The point of the problem.** Sign marking, as above. |
| "But you destroyed the input." | Restore it with a final `abs()` pass, still O(n) / O(1). Or use the set version if mutation is forbidden outright. |
| "Find the **duplicates** instead." | [LeetCode 442](https://leetcode.com/problems/find-all-duplicates-in-an-array/) — same marking pass, but collect `abs(num)` when you find a slot *already* negative. |
| "Find the one missing and the one duplicated." | [LeetCode 645](https://leetcode.com/problems/set-mismatch/) — same pass; the already-negative hit is the duplicate, the still-positive slot is the missing value. |
| "What if values aren't bounded by `n`?" | The index mapping breaks. Fall back to a hash set — or if you need O(1) space and only the *smallest* missing positive, see [First Missing Positive](41-first-missing-positive.md). |
| "What if values could be negative or zero?" | Sign marking dies (0 has no sign, negatives are ambiguous). Use cyclic sort, or a set. |
| "Do it without mutating and without extra space." | Not possible in general — you need somewhere to record what you've seen. Say so plainly. |

**Traps:**

- **Forgetting `abs()` when computing the index.** The most common bug. Later reads see already-negated values, producing wild negative indices and silently wrong answers (Python's negative indexing won't even raise).
- **Omitting the `> 0` guard.** Duplicates negate the same slot twice, flipping it back to positive and reporting a present value as missing. `[1,1]` catches it instantly — test it.
- **Off-by-one on the range.** Values are `1..n` but indices are `0..n-1`. Every conversion needs its `-1` or `+1`, and mixing them up is easy.
- **`range(1, len(nums))` in the set version.** Stops at `n-1` and never tests `n`. It must be `len(nums) + 1`.
- **Assuming the input is sorted.** It isn't, and neither approach needs it to be.

**This same move shows up in:** [First Missing Positive](41-first-missing-positive.md) (the hard version — cyclic sort, same "array as hash table" idea) · [Find the Duplicate Number](287-find-the-duplicate-number.md) (values-as-indices, exploited as a linked list with cycle detection) · [Missing Number](268-missing-number.md) (the single-missing case, solvable with XOR or a sum formula) · [Contains Duplicate](217-contains-duplicate.md) (the set-membership baseline this builds on).

</details>

---
