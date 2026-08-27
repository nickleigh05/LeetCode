# 169. Majority Element

**Easy** · [LeetCode](https://leetcode.com/problems/majority-element/) · [Solution file (no hints)](../../problems/0001-0499/169.py)

[📖 01. Arrays & Hashing lesson](../learning/01-arrays-hashing.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 01. Arrays & Hashing problems](../rmap-practice/01-arrays-hashing.md)

---

Given an array `nums` of size `n`, return the **majority element** — the element that appears **more than `⌊n/2⌋` times**. You may assume the majority element **always exists**.

```
nums = [3,2,3]           →  3
nums = [2,2,1,1,1,2,2]   →  2
```

**Constraints:** `1 <= n <= 5·10⁴` · `-10⁹ <= nums[i] <= 10⁹`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "more than `⌊n/2⌋` times" | **Strictly** more than half. Not "the most common" — a genuine absolute majority |
| "you may **assume it always exists**" | ⚠️ The most important sentence. It removes the need to verify, which unlocks an algorithm that would otherwise be wrong |
| "return the element" | The value, not its index or its count |
| values up to ±10⁹ | Huge range, so no counting array indexed by value — hash or nothing |
| `n` up to 5·10⁴ | O(n²) is 2.5·10⁹ — too slow. O(n) or O(n log n) |

Two consequences of "more than half" that do all the work:

1. **There can be at most one.** Two different elements each appearing >n/2 times would need >n elements total. So you're not searching for a set of candidates — you're searching for *the* one.
2. **It survives pairwise cancellation.** If you repeatedly delete two *different* elements from the array, the majority element can never be fully eliminated — it has more copies than everything else combined. Whatever's left standing at the end must be it.

That second point is not obvious, and it's the entire trick behind the optimal solution.

🤔 **Before you open the next section:** if you paired up every element with a *different* element and threw both away, what could possibly be left over — and why must it be the majority?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Brute force | For each element, count its occurrences | O(n²) | O(1) | ❌ 2.5·10⁹ ops |
| Sort, take middle | After sorting, index `n//2` **must** be the majority | O(n log n) | O(1)\* | ⚠️ Slick one-liner, but slower than needed |
| **Hash map counting** | Count as you go, return the first to cross the threshold | **O(n)** | O(n) | ✅ Obvious, fast, easy to defend |
| **[Boyer–Moore voting](../algorithms/boyer-moore-voting.md)** | Cancel unequal pairs; the survivor is the answer | **O(n)** | **O(1)** | ✅✅ Optimal on both axes |

\* if you're allowed to sort in place.

**The decision depends on what you're optimizing.** Both O(n) options are worth knowing, and the solution file carries both.

**Hash map** — reach for this first in an interview. It's the [Arrays & Hashing](../learning/01-arrays-hashing.md) reflex: you need counts, a hash map gives counts, done. One subtlety worth exploiting: because the majority element exceeds n/2, you can **return the instant any count crosses the threshold** rather than counting everything and taking the max.

**Boyer–Moore** — the answer they're actually fishing for with "can you do O(1) space?". It's a *pairing* argument: walk the array maintaining a candidate and a counter. A matching element votes the counter up; a differing one votes it down. Hitting zero means everything so far has cancelled out perfectly, so you discard the candidate and adopt the current element.

**Why Boyer–Moore is correct** — and be ready to say this, because "it works" isn't an explanation:

> Every decrement pairs off one copy of the candidate against one non-candidate, removing one of each. The true majority has more copies than *all other elements combined*, so it can never be fully cancelled. Whatever remains when the array runs out must be it.

**Why sorting works too:** with more than half the array holding the same value, that value's block must straddle the midpoint no matter where it sits. So `sorted(nums)[n // 2]` is always the answer. Great to mention, but O(n log n) when O(n) is available.

**⚠️ The critical caveat:** Boyer–Moore is only correct *because a majority is guaranteed*. On `[1, 2, 3]` it returns 3 — meaningless, since no majority exists. If the guarantee is removed, you must add a second pass to verify the candidate actually exceeds n/2. Interviewers ask this exact follow-up constantly.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

**Approach A — hash map counting** (the one to write first)

```python
counts = {}
threshold = len(nums) // 2
```

`counts` maps value → occurrences so far. `threshold` is `⌊n/2⌋` computed once — the bar a count must **exceed** (strictly) to win.
→ [dict-basics](../syntax/dict-basics.md) · [integer-division-modulo](../syntax/integer-division-modulo.md)

```python
for num in nums:
    counts[num] = counts.get(num, 0) + 1
```

The standard count-as-you-go idiom. `.get(num, 0)` returns 0 for a value never seen, so first sightings and repeats take the same line — no `if num in counts` branch.
→ [dict-methods](../syntax/dict-methods.md) · [for-loop](../syntax/for-loop.md)

```python
    if counts[num] > threshold:
        return num
```

**The early exit, and why it belongs inside the loop.** Only the majority element can ever cross `⌊n/2⌋`, so the first value to do so is the answer — no need to finish counting or scan for a max afterward.

Note `>` not `>=`: on `n = 4`, `threshold` is 2, and an element appearing exactly twice is *not* a majority.
→ [comparison-operators](../syntax/comparison-operators.md)

<details>
<summary>Approach A together</summary>

```python
class Solution:
    def majorityElement(self, nums: List[int]) -> int:

        counts = {}
        threshold = len(nums) // 2

        for num in nums:
            counts[num] = counts.get(num, 0) + 1
            if counts[num] > threshold:
                return num
```

</details>

---

**Approach B — Boyer–Moore voting** (the O(1)-space answer)

```python
candidate = None
count = 0
```

Two variables replace the entire hash map. `candidate` is who we're currently backing; `count` is the margin by which they're ahead among everything seen so far.
→ [none-type](../syntax/none-type.md)

```python
for num in nums:
    if count == 0:
        candidate = num
```

**Zero means a clean slate.** Every element so far has been cancelled by a differing one, so the prefix contributes nothing and can be discarded entirely. Adopt the current element and start fresh.
→ [for-loop](../syntax/for-loop.md)

```python
    if num == candidate:
        count += 1
    else:
        count -= 1
```

The vote. Agreement strengthens the candidate; disagreement cancels one copy of the candidate against this element — removing **one of each** from consideration.

Note the second `if` is deliberately *not* an `elif` on the first: when `count` hits 0 we adopt `num` as candidate on the line above, and then immediately want to count that adoption as a `+1` vote. Writing it as a single `if/elif/else` chain is a common way to get this subtly wrong.
→ [elif-else](../syntax/elif-else.md)

```python
return candidate
```

The last one standing. Guaranteed correct **only** because the problem promises a majority exists.

<details>
<summary>Approach B together</summary>

```python
### Boyer Moore Voting Algorithm ###
class Solution:
    def majorityElement(self, nums: List[int]) -> int:

        candidate = None
        count = 0

        for num in nums:
            if count == 0:
                candidate = num

            if num == candidate:
                count += 1
            else:
                count -= 1

        return candidate
```

</details>

**Trace Boyer–Moore** — `nums = [2,2,1,1,1,2,2]`:

| `num` | `count` on entry | Adopt? | Vote | `candidate` | `count` after |
|---|---|---|---|---|---|
| 2 | 0 | ✅ → 2 | match | 2 | 1 |
| 2 | 1 | no | match | 2 | 2 |
| 1 | 2 | no | differ | 2 | 1 |
| 1 | 1 | no | differ | 2 | **0** |
| 1 | 0 | ✅ → 1 | match | 1 | 1 |
| 2 | 1 | no | differ | 1 | **0** |
| 2 | 0 | ✅ → 2 | match | 2 | 1 |

Return **2**. Watch the candidate flip to `1` mid-run and still lose — the extra copies of `2` at the end reclaim it. That's cancellation doing its job.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n) for both approaches.**

- **Hash map:** one pass, and each iteration does an O(1) average `get` and an O(1) average insert. Often *better* than n in practice — a majority element is dense, so the threshold is typically crossed well before the end. Worst case (all majority copies at the tail, e.g. `[1,2,3,1,1,1,1]`) it reads everything.
- **Boyer–Moore:** exactly n iterations of pure comparison and integer arithmetic. No hashing, no allocation — the fastest of the two by a constant factor, and it never degrades.

**The hash caveat:** map operations are O(1) *average*, not worst case; adversarial collisions push them toward O(n). Boyer–Moore has no such asterisk — it's O(n) unconditionally, which is a genuine point in its favour beyond just the space win.

**Sorting for comparison:** O(n log n). Fine to name as a baseline, but strictly worse on both axes than Boyer–Moore.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n) vs O(1)</summary>

This is the whole reason to know both.

| | Time | Space |
|---|---|---|
| Hash map | O(n) | **O(n)** — up to n distinct keys, e.g. `[1,2,3,4,5,5,5,5,5]` |
| Sort, take middle | O(n log n) | O(1) in place |
| **Boyer–Moore** | **O(n)** | **O(1)** — two variables, regardless of n |

Boyer–Moore is **optimal on both axes simultaneously**, which is rare enough to be worth remembering as a specific fact rather than a general technique.

The hash map's memory is doing real work — it tracks counts for *every* distinct value. But re-read the question: you were never asked for counts. You were asked for one value. Boyer–Moore's insight is that the majority property is strong enough to be tracked with a single counter, because **you don't need to know how many times anything appeared — only who survives cancellation.**

That's the general lesson: when a problem guarantees something unusually strong, look for a way to exploit the guarantee rather than computing the full picture and reading the answer off it.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Straightforward version: hash map of counts, and since the majority element exceeds n/2 I can return the moment any count crosses that threshold — O(n) time, O(n) space. But I can do it in O(1) space with Boyer–Moore voting: keep a candidate and a counter, increment on a match, decrement on a mismatch, and adopt a new candidate whenever the counter hits zero. Each decrement cancels one copy of the candidate against one non-candidate, and the majority element has more copies than everything else combined, so it can't be fully cancelled — the survivor is the answer. That's O(n) time, O(1) space. It relies on the guarantee that a majority exists; without it I'd need a verification pass."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Do it in O(1) space." | **The expected follow-up.** Boyer–Moore, as above. |
| "What if a majority *isn't* guaranteed?" | Boyer–Moore becomes a candidate-*finder*, not an answer. Add a second pass counting that candidate; return it only if the count exceeds n/2, else `-1`. Still O(n) / O(1). |
| "Find all elements appearing more than `n/3` times." | [LeetCode 229](https://leetcode.com/problems/majority-element-ii/) — generalized Boyer–Moore with **two** candidates and two counters (there can be at most two such elements). Verification is mandatory there. |
| "More than `n/k` times?" | Same generalization with k−1 candidates — the *Misra–Gries* summary. At most k−1 elements can qualify. |
| "The array is sorted." | Return `nums[n // 2]` directly. O(1) time, no scan at all. |
| "It's a stream too large for memory." | Boyer–Moore is already a streaming algorithm — O(1) space, single pass, no random access. That's exactly what it's for. |
| "Prove Boyer–Moore is correct." | Pairing argument: each decrement removes one candidate copy and one non-candidate. The majority has >n/2 copies, so it out-survives every possible pairing. |

**Traps:**

- **Using `>=` instead of `>`.** "More than ⌊n/2⌋" is strict. On `[1,1,2,2]`, `threshold` is 2 and a count of exactly 2 must not win.
- **Trusting Boyer–Moore without the guarantee.** On `[1,2,3]` it happily returns 3. Correct only because the problem promises a majority — say this unprompted.
- **Making the second check an `elif`.** After adopting a new candidate at `count == 0`, you must still count that element as a vote. Chaining the conditions skips it and breaks the algorithm.
- **`max(counts, key=counts.get)`** returns the *most frequent* element, which is not the same thing as a majority. It happens to be right here because a majority is guaranteed — but it answers a different question, and drops the early exit.
- **Building the whole count map before checking.** Correct, but throws away the early return that makes the hash approach fast in practice.

**This same move shows up in:** [Contains Duplicate](217-contains-duplicate.md) (hash map as the default counting reflex) · [Top K Frequent Elements](347-top-k-frequent-elements.md) (when you genuinely *do* need all the counts) · [Find the Duplicate Number](287-find-the-duplicate-number.md) (another O(1)-space trick that exploits a guarantee in the problem statement).

</details>

---
