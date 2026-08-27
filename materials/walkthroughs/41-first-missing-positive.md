# 41. First Missing Positive

**Hard** · [LeetCode](https://leetcode.com/problems/first-missing-positive/) · [Solution file (no hints)](../../problems/0001-0499/41.py)

[📖 01. Arrays & Hashing lesson](../learning/01-arrays-hashing.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 01. Arrays & Hashing problems](../rmap-practice/01-arrays-hashing.md)

---

Given an unsorted integer array `nums`, return the smallest **positive** integer that is **not** present. You must implement an algorithm running in **O(n)** time and using **O(1)** auxiliary space.

```
nums = [1,2,0]       →  3
nums = [3,4,-1,1]    →  2
nums = [7,8,9,11,12] →  1
```

**Constraints:** `1 <= nums.length <= 10⁵` · `-2³¹ <= nums[i] <= 2³¹ - 1`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "smallest **positive**" | Zero and negatives are irrelevant — they can never be the answer, so they're **noise to be ignored**, not data |
| "**not present**" | You need membership queries — normally a hash set, which the space constraint forbids |
| "**O(n)** time" | No sorting (O(n log n)) |
| "**O(1)** auxiliary space" | ⚠️ No hash set, no boolean array, no counter. The *only* memory you may use is `nums` itself |
| values span the **full int range** | You cannot index by value directly — most values are wildly out of range |
| `n` up to 10⁵ | Confirms O(n²) is dead |

Together, O(n) time *and* O(1) space is what makes this Hard. Either constraint alone is easy; both at once forces the key realization:

> **If you can't allocate memory, the input array must become your memory.**

And the observation that makes that possible — this is the crux:

> With `n` elements, the answer is **always in `[1, n+1]`**.

Why? At best, `nums` contains exactly `1, 2, …, n`, and then the answer is `n+1`. Any other arrangement leaves a gap somewhere in `1..n`. So values outside `[1, n]` — negatives, zeros, and anything larger than `n` — **cannot affect the answer** and can be discarded.

That collapses an unbounded problem into a bounded one: you only care about which of the `n` values `1..n` are present. And you have exactly `n` array slots. **One slot per candidate value** — the array is exactly the right size to be its own lookup table.

🤔 **Before you open the next section:** if you could rearrange `nums` so that value `v` sits at index `v-1` whenever `1 <= v <= n`, how would you then read off the answer?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Brute force | For `i = 1, 2, …`, scan for `i` | O(n²) | O(1) | ❌ 10¹⁰ ops |
| Hash set | Add all, then probe `1, 2, 3, …` | O(n) | **O(n)** | ⚠️ Correct, violates the space bound |
| Sort, then scan | Sort and walk looking for the first gap | O(n log n) | O(1) | ⚠️ Correct, violates the time bound |
| Sign marking | Negate `nums[v-1]` to mark `v` present | O(n) | O(1) | ⚠️ Works, but needs pre-cleaning of non-positives |
| **Cyclic sort** | Swap each value `v` to index `v-1`, then scan | **O(n)** | **O(1)** | ✅ |

**The decision: [cyclic sort](../algorithms/counting-sort.md) — place each value at its "home" index, then find the first index whose resident is wrong.**

The idea in one line: **value `v` belongs at index `v - 1`.** So `1` goes to index 0, `2` to index 1, and so on. After rearranging, the first index `i` where `nums[i] != i + 1` tells you `i + 1` is missing.

```
[3, 4, -1, 1]   →  place each value at index (value-1)
[1, -1, 3, 4]      index 0 holds 1 ✅
                   index 1 holds -1 ✗  → answer is 2
```

**Why swapping rather than sign-marking?** Sign marking (used in [448](448-find-all-numbers-disappeared-in-an-array.md)) needs all values positive to be unambiguous, so you'd first have to sweep negatives and zeros into some harmless value. Swapping doesn't care about signs at all — out-of-range values simply never get placed, and their slots are exactly the evidence you need. It's a cleaner fit for this problem's messier input.

**The three conditions that make the inner loop safe** — each is load-bearing:

1. **`1 <= nums[i] <= n`** — only in-range values have a home. Negatives, zeros, and values > `n` are irrelevant, so leave them where they lie.
2. **`nums[nums[i] - 1] != nums[i]`** — only swap if the home slot doesn't *already* hold the correct value. Without this, duplicates cause an **infinite loop**: swapping two identical values forever.
3. **`while`, not `if`** — after a swap, the newly arrived value at `i` also needs placing, and it might too, in a chain. Keep going until `nums[i]` is either home or out of range.

**Why it's still O(n) despite the nested loop** — the amortized argument, which you must be able to give:

> Every swap puts **at least one value into its permanent, correct home**. A value that reaches its home is never moved again. There are at most `n` values, so there are at most `n` swaps **in total across the entire outer loop** — not `n` per iteration. Total work is O(n).

Same shape as the argument in [Longest Consecutive Sequence](128-longest-consecutive-sequence.md): a nested loop whose *total* iterations are bounded by a global budget, not by the outer loop count.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
n = len(nums)
```

Cached because it bounds the valid value range — the `[1, n]` window from section 1.

```python
for i in range(n):
    while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
```

**The guard, and every clause earns its place.**

- `1 <= nums[i] <= n` — is this value even a candidate? Out-of-range values are noise; skip them.
- `nums[nums[i] - 1] != nums[i]` — is the home slot already correct? If it holds this exact value, we're done (or it's a duplicate) and swapping would loop forever.

`nums[nums[i] - 1]` is a **double indirection**: read the value, convert to its home index, then read what currently lives there. Slow down and read it twice — this is the line people misread.

`while` rather than `if`: each swap brings a new value into position `i`, which may itself need relocating. Chains are common.
→ [while-loop](../syntax/while-loop.md) · [chained-comparisons](../syntax/chained-comparisons.md) · [logical-operators](../syntax/logical-operators.md)

```python
        correct = nums[i] - 1
        nums[i], nums[correct] = nums[correct], nums[i]
```

Send the value home.

**Capturing `correct` before the swap is essential.** The tuple assignment evaluates the entire right-hand side first, but the *targets* on the left are resolved as it assigns — so writing `nums[nums[i]-1], nums[i] = nums[i], nums[nums[i]-1]` changes `nums[i]` partway through and corrupts the second index. Store the destination in a plain variable and the ambiguity disappears.
→ [swap-tuple-assign](../syntax/swap-tuple-assign.md) · [tuple-unpacking](../syntax/tuple-unpacking.md)

```python
for i in range(n):
    if nums[i] != i + 1:
        return i + 1
```

**The read-off.** After placement, index `i` should hold `i + 1`. The first index that doesn't is the first missing positive.
→ [for-loop](../syntax/for-loop.md)

```python
return n + 1
```

Every slot was correct ⇒ `nums` is a permutation of `1..n` ⇒ the answer is `n + 1`. This is the `[1,2,3]` → `4` case, and forgetting it is a common miss.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:

        n = len(nums)

        for i in range(n):
            while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
                correct = nums[i] - 1
                nums[i], nums[correct] = nums[correct], nums[i]

        for i in range(n):
            if nums[i] != i + 1:
                return i + 1

        return n + 1
```

</details>

**Trace it** — `nums = [3, 4, -1, 1]`, `n = 4`:

| `i` | `nums` before | `nums[i]` | In range & misplaced? | Swap | `nums` after |
|---|---|---|---|---|---|
| 0 | `[3,4,-1,1]` | 3 | yes — home idx 2 holds −1 | swap 0↔2 | `[-1,4,3,1]` |
| 0 | `[-1,4,3,1]` | −1 | **out of range** → stop | — | `[-1,4,3,1]` |
| 1 | `[-1,4,3,1]` | 4 | yes — home idx 3 holds 1 | swap 1↔3 | `[-1,1,3,4]` |
| 1 | `[-1,1,3,4]` | 1 | yes — home idx 0 holds −1 | swap 1↔0 | `[1,-1,3,4]` |
| 1 | `[1,-1,3,4]` | −1 | **out of range** → stop | — | `[1,-1,3,4]` |
| 2 | `[1,-1,3,4]` | 3 | home idx 2 **already holds 3** → stop | — | unchanged |
| 3 | `[1,-1,3,4]` | 4 | home idx 3 **already holds 4** → stop | — | unchanged |

Final array `[1, -1, 3, 4]`. Second pass:

| `i` | `nums[i]` | expected `i+1` | match? |
|---|---|---|---|
| 0 | 1 | 1 | ✅ |
| 1 | **−1** | 2 | ❌ → **return 2** |

Answer **2** ✅

Note `i = 1` triggered a *chain* of two swaps — exactly why the inner loop is a `while`. And note the total swap count across the whole run was 3, comfortably under `n = 4`.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** — and defending this is most of the interview, because the code visibly has a loop inside a loop.

- Outer loop: exactly `n` iterations.
- Second pass: `n` iterations.
- Inner `while`: **the part that needs an argument.**

**The amortized argument:**

> Every swap moves at least one value into its final correct position, and a value at home is never moved again. With `n` values there can be at most `n` such placements, so the inner loop executes **at most n times summed over the entire outer loop** — not n times per iteration.

Total: O(n) outer + O(n) total inner + O(n) second pass = **O(n)**.

**Say it out loud like this:** *"Nested loops, but each swap permanently places a value, so total swaps are bounded by n across the whole run — that makes it linear, not quadratic."*

The same accounting appears in [Longest Consecutive Sequence](128-longest-consecutive-sequence.md) (each run walked once) and in the analysis of [union-find](../data-structures/union-find.md). Recognizing "a nested loop with a global work budget" as a *pattern* is what lets you spot it under pressure.

**Why the guards matter for termination:** without `nums[nums[i]-1] != nums[i]`, a duplicate like `[1, 1]` swaps the two 1s back and forth forever. The condition isn't just an optimization — it's what makes the algorithm *terminate*.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1) auxiliary.** Two integers (`i`, `correct`) and the swap temporary. Nothing scales with `n`.

This is the constraint that makes the problem Hard, and the trick that satisfies it:

> **The array is both the data and the lookup table.** Because the answer lives in `[1, n+1]` and there are `n` slots, position `i` can encode the boolean "is `i+1` present?" — no separate structure needed.

Compare the honest alternatives:

| | Time | Space | Meets the brief? |
|---|---|---|---|
| Hash set | O(n) | **O(n)** | ❌ space |
| Sort + scan | **O(n log n)** | O(1) | ❌ time |
| Sign marking | O(n) | O(1) | ✅ (needs a pre-cleaning pass) |
| **Cyclic sort** | **O(n)** | **O(1)** | ✅ |

**The cost:** the input is destroyed — permuted, not just marked. If the caller needs `nums` intact, this approach is out, and you should say so unprompted.

**Sign marking as an alternative:** first overwrite every non-positive with something harmless (e.g. `n + 1`), then for each value `v ≤ n` negate `nums[|v|-1]`, then find the first positive slot. Also O(n)/O(1). Cyclic sort is usually cleaner here because it needs no pre-pass and doesn't care about signs — but knowing both, and *why* 448 prefers signs while 41 prefers swaps, is the kind of distinction that reads as real understanding.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The key observation is that with `n` elements the answer must be in `[1, n+1]` — if all of `1..n` are present the answer is `n+1`, otherwise it's a gap in that range. So values outside `[1, n]` are irrelevant. That gives me exactly `n` candidate values and `n` array slots, so I can use the array as its own hash table: put value `v` at index `v-1` by swapping. I loop with a `while` because each swap brings in a new value that may also need placing, and I guard on the value being in range and not already home — the second guard prevents infinite loops on duplicates. It's O(n) overall because every swap permanently places a value, so there are at most `n` swaps total. Then one more pass: the first index where `nums[i] != i+1` gives the answer, else `n+1`. O(n) time, O(1) space — but it destroys the input."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why is the answer bounded by `n+1`?" | **The unlock.** Best case `nums` holds exactly `1..n` → answer `n+1`. Otherwise a gap exists in `1..n`. |
| "Why doesn't the nested loop make it O(n²)?" | Each swap permanently homes a value; at most `n` placements exist, so total inner iterations ≤ n. |
| "What stops an infinite loop on duplicates?" | The `nums[nums[i]-1] != nums[i]` guard — never swap when the home slot already holds that value. |
| "Can you do it without mutating the input?" | Not in O(1) space. You'd need a hash set — O(n) space — or accept O(n log n) with a sorted copy. |
| "Solve it with sign marking instead." | Replace non-positives with `n+1`, negate `nums[|v|-1]` for each `v ≤ n`, return the first positive index + 1. |
| "First missing positive **≥ k**?" | Shift the mapping: value `v` homes at index `v - k`, and only `k <= v < k + n` is in range. |
| "Find all missing positives in `1..n`." | [448](448-find-all-numbers-disappeared-in-an-array.md) — same family; collect every index where `nums[i] != i+1`. |
| "What if the array is read-only and space is O(1)?" | Provably impossible in O(n). You need somewhere to record what you've seen — say so plainly. |

**Traps:**

- **Using `if` instead of `while`.** Leaves values misplaced after the first swap; produces wrong answers on chains like `[3,4,-1,1]`.
- **Dropping the "already home" guard.** Infinite loop on `[1,1]`. Test duplicates first — it's the fastest way to catch this.
- **Writing the swap without capturing `correct`.** The left-hand target index shifts mid-assignment. Store the destination in a variable.
- **Forgetting `return n + 1`.** `[1,2,3]` must give 4; without it you return `None`.
- **Off-by-one in the value↔index mapping.** Value `v` ↔ index `v-1`, always. Write it down before coding.
- **Trying to skip or clean negatives first.** Unnecessary — the range guard already ignores them, and their slots are precisely the evidence of what's missing.
- **Sorting because it's easier.** O(n log n) violates the stated bound. Name it as a baseline, then beat it.

**This same move shows up in:** [Find All Numbers Disappeared in an Array](448-find-all-numbers-disappeared-in-an-array.md) (the Easy sibling — same "array as hash table," solved with sign marking) · [Find the Duplicate Number](287-find-the-duplicate-number.md) (values-as-indices, exploited as a linked list with Floyd's cycle detection) · [Missing Number](268-missing-number.md) (single missing value, solvable by XOR or sum formula) · [Longest Consecutive Sequence](128-longest-consecutive-sequence.md) (the same amortized "nested loop with a global budget" argument).

</details>

---
