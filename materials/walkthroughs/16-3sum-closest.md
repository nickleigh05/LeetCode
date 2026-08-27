# 16. 3Sum Closest

**Medium** · [LeetCode](https://leetcode.com/problems/3sum-closest/) · [Solution file (no hints)](../../problems/0001-0499/16.py)

[📖 02. Two Pointers lesson](../learning/02-two-pointers.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 02. Two Pointers problems](../rmap-practice/02-two-pointers.md)

---

Given an integer array `nums` of length `n` and an integer `target`, find three integers in `nums` whose sum is **closest** to `target`. Return that sum. Each input has exactly one solution.

```
nums = [-1,2,1,-4], target = 1   →  2      (-1 + 2 + 1 = 2, distance 1)
nums = [0,0,0],     target = 1   →  0
```

**Constraints:** `3 <= n <= 500` · `-1000 <= nums[i] <= 1000` · `-10⁴ <= target <= 10⁴`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**closest** to target" | Not an exact match — you're **minimizing `abs(sum - target)`**. That changes the loop from "search" to "track the best" |
| "return the **sum**" | Not the indices, not the triplet — just the value |
| "exactly **one** solution" | No tie-breaking rules to worry about |
| three integers | Three nested choices — brute force is O(n³) |
| `n` up to 500 | O(n³) is 1.25·10⁸ — borderline; O(n²) is 2.5·10⁵ — comfortable |
| duplicates allowed | But unlike [3Sum](15-3sum.md), you **don't** need to skip them — you're returning a value, not a set of distinct triplets |

This is [3Sum](15-3sum.md) with two changes, and both simplify things:

| | 3Sum | 3Sum Closest |
|---|---|---|
| Goal | all distinct triplets summing to 0 | the single closest sum |
| Duplicate handling | **required** (or you emit duplicates) | **unnecessary** — a duplicate just re-evaluates the same sum |
| Return | list of triplets | one integer |
| Early exit | none | ✅ exact match ⇒ done |

The technique is the same and is worth stating as a general principle:

> **Sort, fix one element, then two-pointer the rest.** Sorting converts an O(n²) inner search into an O(n) one, because a sorted array tells you *which direction* to move to change the sum.

That directional information is exactly what "closest" still gives you: if the current sum is **below** target, the only way to increase it is to move the left pointer right (to a larger value). If it's **above**, move the right pointer left. Same rule as 3Sum — you just record the best distance along the way instead of only reacting to zero.

🤔 **Before you open the next section:** once you've fixed one number, you need two more whose sum is closest to `target - fixed`. On a **sorted** array, how do you find that in one pass?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Brute force | All triples `(i, j, k)` | O(n³) | O(1) | ⚠️ 1.25·10⁸ — passes but wasteful |
| Fix two, hash the third | For each pair, look up the best complement | O(n²) | O(n) | ⚠️ "Closest" makes hash lookup awkward — you'd need a sorted structure anyway |
| Fix one, binary search | For each pair, binary search the third | O(n² log n) | O(1) | ⚠️ Worse than two pointers |
| **Sort + fix one + two pointers** | Sorted array lets pointers converge | **O(n²)** | O(1)\* | ✅ |

**The decision: sort, then for each `i`, converge two pointers over the remainder.**

Why sorting is the enabling step: in an unsorted array, knowing `sum < target` tells you nothing about which element to change. After sorting, it tells you everything — moving `l` right can only **increase** the sum, and moving `r` left can only **decrease** it. That monotonicity turns a two-dimensional search into a one-dimensional walk.

**The three moves at each step:**

| Condition | Meaning | Action |
|---|---|---|
| `s < target` | sum too small | `l += 1` — reach for a bigger number |
| `s > target` | sum too big | `r -= 1` — reach for a smaller number |
| `s == target` | **exact hit** | return immediately — distance 0 can't be beaten |

The early exit is genuinely free and worth taking: nothing beats a distance of zero.

**Why no duplicate-skipping?** In [3Sum](15-3sum.md) you must skip duplicates or you emit the same triplet repeatedly. Here you return a *number*, so re-evaluating an identical sum is harmless — it just fails to improve `res`. You **could** add skips as an optimization, but they're not needed for correctness. Knowing which of the two problems needs them, and why, is a good sign you understand the pattern rather than having memorized it.

**Why initialize `res = sum(nums[:3])`?** You need a valid starting candidate that's an actual achievable sum. Using `float('inf')` would work with care, but `abs(inf - target)` comparisons are clumsier, and the problem guarantees `n >= 3`, so the first three elements are always available. Simple and safe.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
nums.sort()
```

**The enabling step.** O(n log n), immediately dominated by the O(n²) main loop, so it's effectively free — and without it the two-pointer logic is meaningless.

Note it mutates the caller's array; mention that if asked.
→ [sorting-key](../syntax/sorting-key.md)

```python
res = sum(nums[:3])
```

A concrete starting answer — the sum of the three smallest elements. Guaranteed valid since `n >= 3`.
→ [list-slicing](../syntax/list-slicing.md)

```python
for i in range(len(nums) - 2):
```

Fix the first element. Stop at `n - 2` because you need two more elements after `i` — going further leaves no room for `l` and `r`.
→ [range-function](../syntax/range-function.md)

```python
    l, r = i + 1, len(nums) - 1
```

The two pointers span everything **after** `i`. Starting `l` at `i + 1` (not 0) is what prevents reusing `nums[i]` and also stops you re-examining pairs already covered by earlier `i` values.
→ [multiple-return-values](../syntax/multiple-return-values.md)

```python
    while l < r:
        s = nums[i] + nums[l] + nums[r]
```

`l < r` — strictly, so the two pointers never land on the same element (which would use one value twice).

```python
        if abs(s - target) < abs(res - target): res = s
```

**Track the best.** Compare *distances*, not sums. `abs(s - target)` is how far this triplet is from the goal; keep it only if it's strictly closer.

Strict `<` means the first-found candidate wins ties — irrelevant here, since the problem guarantees a unique answer.
→ [math-module-basics](../syntax/math-module-basics.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
        if s < target: l += 1
        elif s > target: r -= 1
        else: return s
```

**The directional move — this is where sortedness pays off.**

- `s < target` ⇒ need a **larger** sum ⇒ advance `l` to a bigger value
- `s > target` ⇒ need a **smaller** sum ⇒ retreat `r` to a smaller value
- `s == target` ⇒ **perfect**, return immediately

Each branch shrinks the window by one, guaranteeing the inner loop terminates in O(n).
→ [elif-else](../syntax/elif-else.md) · [if-return](../syntax/if-return.md)

```python
return res
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def threeSumClosest(self, nums: List[int], target: int) -> int:

        nums.sort()
        res = sum(nums[:3])

        for i in range(len(nums) - 2):
            l, r = i + 1, len(nums) - 1

            while l < r:
                s = nums[i] + nums[l] + nums[r]
                if abs(s - target) < abs(res - target): res = s

                if s < target: l += 1
                elif s > target: r -= 1
                else: return s

        return res
```

</details>

<details>
<summary>The brute force (also in the solution file)</summary>

```python
### Brute force ###
class Solution:
    def threeSumClosest(self, nums: List[int], target: int) -> int:
        n = len(nums)
        closest = float('inf')
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    s = nums[i] + nums[j] + nums[k]
                    if abs(s - target) < abs(closest - target):
                        closest = s
        return closest
```

O(n³) — 1.25·10⁸ at n = 500. It squeaks through the limits, but it's the answer you improve on, not the one you submit.

</details>

**Trace it** — `nums = [-1,2,1,-4]` → sorted `[-4,-1,1,2]`, `target = 1`. Initial `res = -4 + -1 + 1 = -4` (distance 5).

| `i` | `nums[i]` | `l` | `r` | `s` | `|s-1|` | Best? | Move |
|---|---|---|---|---|---|---|---|
| 0 | −4 | 1 | 3 | `-4-1+2 = -3` | 4 | ✅ `res=-3` | `s<1` → `l=2` |
| 0 | −4 | 2 | 3 | `-4+1+2 = -1` | 2 | ✅ `res=-1` | `s<1` → `l=3` |
| 0 | −4 | 3 | 3 | `l < r` false → inner loop ends | | | |
| 1 | −1 | 2 | 3 | `-1+1+2 = 2` | **1** | ✅ `res=2` | `s>1` → `r=2` |
| 1 | −1 | 2 | 2 | `l < r` false → ends | | | |
| 2 | — | `range(4-2)` = `0,1` → loop ends | | | | | |

Return **2** ✅ — distance 1 from the target, and no triplet does better.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n²)</summary>

**O(n²).**

- Sorting: O(n log n)
- Outer loop: `n - 2` iterations
- Inner two-pointer loop: **O(n)** — every iteration moves `l` right or `r` left, so the window shrinks by one each time and can run at most `n` times

Total: O(n log n) + O(n) × O(n) = **O(n²)**. The sort is dominated and effectively free.

At n = 500 that's ~2.5·10⁵ operations — instant. The brute force is 1.25·10⁸, roughly 500× more.

**Why the inner loop is O(n), not O(n²):** the pointers only ever move *toward* each other and never reset within an iteration of `i`. It's the same converging-pointer argument as [Two Sum II](167-two-sum-ii-input-array-is-sorted.md) — the search space shrinks monotonically.

**Can you beat O(n²)?** Not by any known general method — 3SUM is conjectured to require Ω(n²) in the standard model, and this variant inherits that. O(n²) is the expected answer.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1) auxiliary</summary>

**O(1) auxiliary** — a handful of integers (`res`, `i`, `l`, `r`, `s`).

The asterisk: `nums.sort()` is in place, but CPython's Timsort can use O(n) temporary space in the general case. Most analyses call this O(1) or "O(log n) for the sort's stack." If the caller needs `nums` unmodified, `sorted(nums)` costs a genuine O(n).

**Compare to the hash-based alternative:** fixing two elements and hashing the third is O(n) space and doesn't even help here — "closest" isn't a lookup, it's a nearest-neighbour query, which a hash map can't answer. You'd need a sorted structure or binary search, at which point two pointers are simpler and faster.

That's a useful distinction to carry:

> **Hash maps answer "is this exact value present?" Sorted arrays answer "what's nearest?"** When the question is about proximity or ordering, sort.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Brute force is O(n³) over all triples. I can do better by sorting first — then for each fixed first element, I need two more whose sum is closest to `target - nums[i]`, and on a sorted array that's a converging two-pointer scan. If the current sum is below target I move the left pointer right to increase it; if it's above I move the right pointer left. Each step I check whether `abs(sum - target)` beats my best and update. If I ever hit the target exactly I return immediately, since distance zero can't be beaten. O(n²) time after an O(n log n) sort, O(1) extra space. Unlike 3Sum I don't need to skip duplicates, because I'm returning a sum rather than a set of distinct triplets."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "How does this differ from [3Sum](15-3sum.md)?" | Same sort + two-pointer skeleton. 3Sum needs duplicate-skipping to avoid repeated triplets; here duplicates are harmless. And this one can early-exit on an exact hit. |
| "4Sum Closest?" | Add another nested loop — O(n³). Generalizes to k-sum at O(n^(k-1)). See [4Sum](18-4sum.md). |
| "Return the **triplet**, not the sum." | Track `(nums[i], nums[l], nums[r])` alongside `res`. |
| "What if there are **ties**?" | The problem guarantees uniqueness. Otherwise define the rule — strict `<` keeps the first found. |
| "Can you beat O(n²)?" | Not in general; 3SUM is conjectured Ω(n²). |
| "Why not a hash map?" | Hash maps answer exact-membership, not nearest-value. "Closest" needs ordering. |
| "Would skipping duplicates help?" | As an optimization, yes — `if i > 0 and nums[i] == nums[i-1]: continue` avoids redundant work. Not needed for correctness. |

**Traps:**

- **Forgetting to sort.** The two-pointer directional logic is meaningless on unsorted input, and the answer will be wrong rather than merely slow.
- **Comparing sums instead of distances.** You want `abs(s - target) < abs(res - target)`, not `s < res`.
- **Initializing `res = 0`** or some arbitrary constant. It must be an achievable sum, or you can return a value no triplet produces.
- **`l` starting at 0.** Reuses `nums[i]` and re-covers pairs from earlier iterations.
- **`while l <= r`.** Lets both pointers land on the same element, using one value twice.
- **Looping `i` to `len(nums)`.** Leaves no room for two more elements; `range(len(nums) - 2)` is the bound.
- **Adding 3Sum's duplicate skips and mangling them.** They're optional here — if you're unsure, leave them out.

**This same move shows up in:** [3Sum](15-3sum.md) (the same sort + fix-one + two-pointer skeleton, with duplicate handling) · [4Sum](18-4sum.md) (one more nesting level) · [Two Sum II](167-two-sum-ii-input-array-is-sorted.md) (the converging two-pointer core this is built on) · [Container With Most Water](11-container-with-most-water.md) (converging pointers driven by a greedy directional rule).

</details>

---
