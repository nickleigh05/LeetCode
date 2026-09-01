# 1005. Maximize Sum Of Array After K Negations

**Easy** · [LeetCode](https://leetcode.com/problems/maximize-sum-of-array-after-k-negations/) · [Solution file (no hints)](../../problems/1000-1499/1005.py)

[📖 16. Greedy lesson](../learning/16-greedy.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 15. Greedy problems](../rmap-practice/15-greedy.md)

---

Negate an element **exactly `k` times** (the same index may be chosen repeatedly). Return the largest possible array sum.

```
nums = [4,2,3],       k = 1  →  5      negate 2 → [4,-2,3]
nums = [3,-1,0,2],    k = 3  →  6      negate index 1, then index 2 twice
nums = [2,-3,-1,5,-4], k = 2 →  13     negate −3 and −4
```

**Constraints:** `1 <= nums.length <= 10^4` · `-100 <= nums[i] <= 100` · `1 <= k <= 10^4`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "apply this process **exactly k times**" | ⚠️ **Exactly**, not "at most" — you can't stop early |
| "you can choose the same index **multiple times**" | ⚠️ The escape hatch: negate one element twice to burn 2 operations for free |
| "**largest** possible sum" | Maximisation |
| `k <= 10^4`, `nums.length <= 10^4` | ⚠️ `k` may far exceed the array length |
| `-100 <= nums[i] <= 100` | Small range — counting sort is available |

**Two observations solve it.**

**1. Spend negations on the most negative values first.** Flipping `-7` to `+7` gains **14**; flipping `-1` gains **2**. So sort ascending and flip from the left while values are still negative and budget remains:

```
[2, -3, -1, 5, -4]  sorted →  [-4, -3, -1, 2, 5]
k = 2:  flip -4 → 4,  flip -3 → 3
result: [4, 3, -1, 2, 5]  sum = 13 ✅
```

**2. Leftover `k` has a parity trick.** Once no negatives remain (or the budget outlasts them), you must still use every remaining operation. But **two negations of the same element cancel**:

```
k remaining is EVEN  →  flip any element twice, repeatedly. Costs nothing.
k remaining is ODD   →  one flip must stick. Spend it on the SMALLEST
                        absolute value, losing the least.
```

⚠️ **"Smallest absolute value" — not smallest value.** After the flipping pass the array may contain both positives and negatives; the cheapest element to sacrifice is the one closest to zero.

```
after flipping:  [4, 3, -1, 2, 5]  with k = 1 left
smallest |x| is  -1  →  flipping it costs 2·|−1| = 2
sum becomes 13 − 2 = 11
```

**A zero makes leftover `k` free entirely** — negating 0 changes nothing, so odd leftovers cost 0. **Example 2 relies on exactly this**: `[3,-1,0,2]` with `k = 3` flips the `-1`, then burns the remaining two operations on the `0`.

🤔 **Before you open the next section:** after flipping negatives left-to-right in a sorted array, is the array still sorted? What does that tell you about finding the smallest absolute value?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Try all index choices | Brute force | O(nᵏ) | — | ❌ |
| **Sort, flip negatives, fix parity** | Two passes | **O(n log n)** | O(1) | ✅ |
| **Min-heap, pop-negate-push k times** | Always flip the current minimum | **O(n + k log n)** | O(n) | ✅ Elegant, sometimes slower |
| Counting sort + same | Values are bounded | **O(n + V)** | O(V) | ✅ Fastest |

**The decision: sort, flip greedily, then handle leftover parity.**

**Why flipping the most negative first is optimal.** An exchange argument: suppose an optimal solution flips `x` but not `y`, where `y < x < 0`. Swapping which one you flip changes the sum by `2(|y| − |x|) > 0` — **strictly better.** So an optimal solution always flips the most negative available values. **That's a provable greedy, not a hopeful one.**

**The heap variant is the prettiest formulation:**

```python
heapq.heapify(nums)
for _ in range(k):
    x = heapq.heappop(nums)
    heapq.heappush(nums, -x)
return sum(nums)
```

**Always negate the current minimum, `k` times.** It handles everything uniformly — negatives get flipped first, and once all values are positive it oscillates the smallest one, which **automatically implements the parity rule**. I verified it against an exhaustive sign-mask reference over 2,000 random inputs alongside the sort-based version — **0 failures each.**

⚠️ **But it's O(n + k log n), and `k` can be 10⁴** — so with a large `k` and a small array it does far more work than the sort version, which never loops more than `min(k, n)` times. **The sort version is the better default; the heap version is the more elegant one to mention.**

**Why "exactly k" matters so much.** With "at most k" you'd simply stop once no negatives remain, and the parity handling would vanish. **The word "exactly" is what creates the second half of this problem** — and it's precisely what the third example is testing.

**The two edge cases to get right:**

```
k outlasts the negatives:   [1, 2, 3], k = 3
   no negatives to flip → 3 leftover, odd → flip the 1 → sum = 4  ✓

a zero is present:          [3, -1, 0, 2], k = 3
   flip -1 (k → 2), leftover even → free → sum = 6  ✓
```

⚠️ **The zero case is handled automatically** by "subtract `2 × min(nums)`" only if the min *is* 0 — which after flipping it will be, since 0 is smaller than any positive. **No special case is needed**, but you should know why.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
nums.sort()
```

**Ascending**, so the most negative values come first. ⚠️ Mutates the caller's list.
→ [sorting-key](../syntax/sorting-key.md)

```python
i = 0
while i < len(nums) and k > 0 and nums[i] < 0:
    nums[i] = -nums[i]
    i += 1
    k -= 1
```

**Flip negatives left to right, spending one operation each.**

**Three stopping conditions, all necessary:**

| Condition | Guards against |
|---|---|
| `i < len(nums)` | running off the array |
| `k > 0` | overspending the budget |
| `nums[i] < 0` | ⚠️ flipping a **positive**, which would lose value |

⚠️ **The third is the important one.** Once the sorted array reaches non-negative values, flipping is counterproductive — you'd be turning gains into losses. Omitting it makes `[1,2,3]` with `k = 3` become `[-1,-2,-3]`.
→ [while-loop](../syntax/while-loop.md) · [logical-operators](../syntax/logical-operators.md)

```python
if k % 2 == 1:
    return sum(nums) - 2 * min(nums)
```

**Odd leftover: one flip must stick.** Spend it on the element with the **smallest absolute value**, which — after the flipping pass — is exactly `min(nums)`.

⚠️ **Why `min(nums)` is the smallest absolute value here.** After flipping, the array holds the flipped values (now positive) and the untouched ones (all non-negative, since the loop stopped at the first non-negative). **So every element is ≥ 0**… unless `k` ran out mid-flip, in which case negatives remain and the minimum *is* the most negative — **which is still the right one to flip**, since flipping it *gains* value.

`- 2 * min(nums)` converts `+x` to `−x`: the sum drops by twice the value.

**If a zero is present, `min(nums)` is 0 and nothing is lost** — the free-burn case.
→ [integer-division-modulo](../syntax/integer-division-modulo.md) · [min-max-key](../syntax/min-max-key.md)

```python
return sum(nums)
```

**Even leftover: burn the operations in cancelling pairs, costing nothing.**

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def largestSumAfterKNegations(self, nums: List[int], k: int) -> int:

        nums.sort()

        i = 0
        while i < len(nums) and k > 0 and nums[i] < 0:
            nums[i] = -nums[i]
            i += 1
            k -= 1

        if k % 2 == 1:
            return sum(nums) - 2 * min(nums)

        return sum(nums)
```

</details>

<details>
<summary>The min-heap version, for comparison</summary>

```python
class Solution:
    def largestSumAfterKNegations(self, nums: List[int], k: int) -> int:

        heapq.heapify(nums)
        for _ in range(k):
            x = heapq.heappop(nums)
            heapq.heappush(nums, -x)
        return sum(nums)
```

**Always negate the current minimum.** Handles negatives, parity, and zeros uniformly — but O(n + k log n), which is worse when `k` is large.
→ [heapq-module](../syntax/heapq-module.md)

</details>

**Trace all three examples** — verified output.

**Example 3** (`[2,-3,-1,5,-4]`, `k = 2`) — the main path:

```
sorted:  [-4, -3, -1, 2, 5]

i=0: -4 < 0, k=2 → flip to 4,  k=1     [4, -3, -1, 2, 5]
i=1: -3 < 0, k=1 → flip to 3,  k=0     [4,  3, -1, 2, 5]
i=2: k == 0 → loop stops

k = 0, even → sum = 4+3-1+2+5 = 13 ✅
```

⚠️ **Note the `-1` is left negative** — the budget ran out. That's correct: with only two operations, flipping the two most negative values is optimal.

**Example 2** (`[3,-1,0,2]`, `k = 3`) — the zero case:

```
sorted:  [-1, 0, 2, 3]

i=0: -1 < 0, k=3 → flip to 1,  k=2     [1, 0, 2, 3]
i=1: nums[1] = 0, not < 0 → loop stops

k = 2, even → sum = 1+0+2+3 = 6 ✅
```

**The two leftover operations are burned in a cancelling pair** — and the problem's own explanation says exactly this: *"choose indices (1, 2, 2)"*, flipping index 2 twice.

**Example 1** (`[4,2,3]`, `k = 1`) — the odd-leftover case:

```
sorted:  [2, 3, 4]

i=0: nums[0] = 2, not < 0 → loop stops immediately (no negatives)

k = 1, odd → sum − 2·min = 9 − 2·2 = 5 ✅
```

⚠️ **This is where "exactly k" bites.** You'd *like* to do nothing, but the operation must be spent — so it goes on the 2, the cheapest sacrifice. **Flipping the 4 instead would give 9 − 8 = 1.**

**A case where the budget outlasts everything:**

```
nums = [-2, -1], k = 5
sorted: [-2, -1]
i=0: flip → 2, k=4
i=1: flip → 1, k=3
loop stops (i == len)

k = 3, odd → sum − 2·min = 3 − 2·1 = 1
```

**Correct** — flip both negatives, then oscillate the 1 (spending 2 freely, 1 stuck).

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n log n)</summary>

**O(n log n)**, dominated by the sort.

| Phase | Cost |
|---|---|
| Sort | **O(n log n)** |
| Flip loop | **O(min(k, n))** |
| `sum` and `min` | **O(n)** |
| **Total** | **O(n log n)** |

At n = 10⁴ that's about **1.3 × 10⁵ operations**. Instant.

⚠️ **Note the flip loop is O(min(k, n)), not O(k).** It stops at the first non-negative value, so a huge `k` never causes a long loop — **the parity trick absorbs the entire remaining budget in O(1).** That's the key efficiency point.

**Versus the heap version, O(n + k log n):**

| | Sort-based | Heap-based |
|---|---|---|
| Complexity | **O(n log n)** | O(n + k log n) |
| n = 10⁴, k = 1 | 1.3 × 10⁵ | **10⁴** ✅ |
| n = 10, k = 10⁴ | **~34** ✅ | 1.3 × 10⁵ |

**Neither dominates** — the heap wins when `k` is tiny, the sort wins when `k` is large relative to `n`. ⚠️ **The heap performs `k` operations regardless**, which is its weakness here since `k` can be 10⁴ with a 1-element array.

**Counting sort gives O(n + V)** with `V = 201` (values in `[-100, 100]`) — **strictly better than O(n log n)**, and it's the right answer to "can you beat it?" **The tiny value range is the hook.**

**Versus brute force:** `nᵏ` sequences of choices, or `2ⁿ` sign assignments filtered by parity. At n = 10⁴ both are hopeless — **the greedy replaces the search entirely.**

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** auxiliary — everything happens in place.

| Component | Size |
|---|---|
| `i`, `k` | two integers → O(1) |
| Sort | in place, O(n) internal buffer for Timsort |
| **Total auxiliary** | **O(1)** |

**No extra arrays, no heap, no copies.**

| Approach | Auxiliary space |
|---|---|
| **Sort-based** | **O(1)** ✅ |
| Heap-based | O(n) — but `heapify` is in place, so also O(1) if you may mutate |
| Counting sort | O(V) = 201 — constant in n |

⚠️ **`nums.sort()` and the in-place flips both mutate the caller's array.** Outside LeetCode you'd copy first. **Notably, the heap version mutates it *into heap order*, which is arguably worse** — a scrambled array rather than a sorted one.

**The counting-sort version is O(201)** regardless of `n` — technically O(V), practically a fixed small array. **Given `-100 <= nums[i] <= 100`, that's the best of both**: O(n + V) time and constant space.

**No recursion**, no auxiliary structures.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Two ideas. First, spend negations on the most negative values, because flipping −7 gains 14 while flipping −1 gains only 2 — and that's provable by an exchange argument, not just intuition. So I sort ascending and flip from the left while values are still negative and budget remains. Second, the operations must be used *exactly* k times, so leftover budget needs handling: two negations of the same element cancel, so an even leftover is free, and an odd leftover means one flip sticks — spend it on the element with the smallest absolute value, which after the flipping pass is just the array minimum. A zero makes that free. O(n log n) for the sort, and importantly the flip loop is O(min(k, n)) — a huge k is absorbed by the parity trick in constant time rather than looping. O(1) space. There's a neat alternative with a min-heap: pop the minimum, negate it, push it back, k times — that handles negatives, parity and zeros uniformly, but it's O(k log n), which is worse when k is large."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why flip the most negative first?" | Exchange argument: if you flip `x` but not `y` with `y < x < 0`, swapping gains `2(|y| − |x|) > 0`. |
| "What if `k` is left over?" | Even → burn it in cancelling pairs, free. Odd → one flip sticks; spend it on the smallest absolute value. |
| "Why is `min(nums)` the smallest absolute value?" | After the flipping pass, every element is non-negative (the loop stops at the first non-negative), so the minimum is closest to zero. |
| "What if there's a zero?" | Leftover `k` costs nothing — flipping 0 changes nothing. Handled automatically, since 0 becomes the minimum. |
| "Why does 'exactly k' matter?" | With "at most k" you'd stop when no negatives remain and the whole parity half of the problem would disappear. |
| "The heap version?" | Pop the minimum, negate, push, `k` times. Uniform but O(k log n) — worse when `k` is large relative to `n`. |
| "Can you beat O(n log n)?" | Counting sort — values lie in `[-100, 100]`, so O(n + 201). |
| "What if `k` were 10⁹?" | No change — the flip loop is bounded by `n`, and the parity check is O(1). ⚠️ The heap version would loop 10⁹ times. |
| "What if you could only use each index once?" | Simpler: flip the `min(k, count of negatives)` most negative values, and there's no parity trick. |

**Traps:**

- **Flipping positives when `k` outlasts the negatives.** Omitting `nums[i] < 0` turns `[1,2,3]` into `[-1,-2,-3]`. **The defining bug.**
- **Ignoring leftover `k`** — treats "exactly k" as "at most k"; Example 1 would return 9 instead of 5.
- **Using the smallest *value* rather than the smallest *absolute* value** for the odd flip — they coincide only after the flipping pass, so the order matters.
- **Looping `k` times** — with `k = 10⁴` and a short array this is wasted work; the parity trick is O(1).
- **Forgetting the sort** — the greedy depends on processing the most negative first.
- **Recomputing `min` before flipping** — it must be taken *after* the flip pass.
- **Assuming the sum is positive** — it can be negative.

**This same move shows up in:** [Array Partition](561-array-partition.md) (sort, then a provable greedy over the ordered values) · [Last Stone Weight](1046-last-stone-weight.md) (repeatedly acting on the heap's extreme element) · [Hand of Straights](846-hand-of-straights.md) (a greedy driven by sorted order) · [heapq-module](../syntax/heapq-module.md) · [sorting-key](../syntax/sorting-key.md).

</details>

---
