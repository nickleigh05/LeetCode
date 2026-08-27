# 90. Subsets II

**Medium** · [LeetCode](https://leetcode.com/problems/subsets-ii/)

[📖 10. Backtracking lesson](../learning/10-backtracking.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 10. Backtracking problems](../rmap-practice/10-backtracking.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Given an integer array `nums` that **may contain duplicates**, return all possible subsets (the power set).

The solution set **must not contain duplicate subsets**. Return the answer in any order.

```
nums = [1,2,2]  →  [[], [1], [1,2], [1,2,2], [2], [2,2]]
                    note: only ONE [2] and ONE [1,2]

nums = [0]      →  [[], [0]]
```

**Constraints:** `1 <= nums.length <= 10` · `-10 <= nums[i] <= 10`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "may contain **duplicates**" | ⚠️ The only change from [Subsets](78-subsets.md) — and it's the entire problem |
| "must not contain **duplicate subsets**" | Subsets are compared by *contents*, not by which indices produced them |
| "any order" | No output sorting required |
| n ≤ 10 | Exponential enumeration is expected, same as [78](78-subsets.md) |

**Where the duplicates come from.** Run [Subsets](78-subsets.md)'s algorithm on `[1,2,2]` and it produces 2³ = 8 results:

```
[], [2], [2], [2,2], [1], [1,2], [1,2], [1,2,2]
      ↑    ↑              ↑      ↑
   the two 2's are at different INDICES but have the same VALUE
```

`[2]` appears twice — once from index 1, once from index 2. Same for `[1,2]`. The algorithm distinguishes them by *position*; the problem compares them by *content*.

**The fix, and the reasoning behind it.** Sort first so equal values sit next to each other. Then, **within a single loop level**, only allow the *first* of a run of equal values to start a branch:

```
at one recursion level, scanning [1, 2, 2]:
  i=1 (first 2)  →  explore  ✅
  i=2 (second 2) →  SKIP     ← would duplicate the branch above
```

⚠️ **The crucial nuance:** the skip applies **across the loop at one level**, *not* down the recursion.

- Choosing 2 at index 1, then 2 at index 2 in a **deeper** call gives `[2,2]` — a legitimate distinct subset. **Must be allowed.**
- Choosing 2 at index 2 *instead of* index 1 at the **same** level gives `[2]` again — a duplicate. **Must be blocked.**

The condition `i > start` is exactly what separates these two cases: `start` marks where this level's loop began, so `i > start` means "this isn't the first candidate I'm trying here."

🤔 **Before you open the next section:** why is `i > start` the right test, rather than `i > 0`?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Verdict |
|---|---|---|
| Generate all, dedupe with a set | Run [78](78-subsets.md), store `tuple(sorted(subset))` in a set | ⚠️ Correct, but wastes work generating duplicates then discarding them |
| Count occurrences, choose 0..k of each value | Group duplicates, pick how many to take | ✅ Elegant alternative |
| **Sort + skip duplicates at the same level** | Prevent duplicates from ever being generated | ✅ |

**The decision: sort, then skip a candidate equal to its predecessor when it isn't the first choice at this level.**

**Why prevention beats deduplication.** The set-based approach generates all 2ⁿ subsets and throws away the repeats — correct, but it does the work anyway and needs O(2ⁿ) extra memory for the set. Skipping at the source means duplicate branches are **never explored**, which prunes the tree rather than filtering its output. Same instinct as [Generate Parentheses](22-generate-parentheses.md): *prune at the branch, don't validate at the leaf.*

**The condition, decomposed:**

```python
if i > start and nums[i] == nums[i - 1]:
    continue
```

| Part | Meaning |
|---|---|
| `i > start` | "This is **not** the first candidate at this level" — so a branch for this value already ran here |
| `nums[i] == nums[i-1]` | "Same value as the previous candidate" — only meaningful because the array is **sorted** |

Both must hold. When `i == start`, this is the level's first choice and must always be explored — even if it equals something used *higher up* the recursion, since that's a deeper, legitimate combination.

**Why `i > start` and not `i > 0`.** `i > 0` would block the second 2 even when it's the *first* candidate of a deeper level — killing `[2,2]`, which is a valid subset. **`start` is what localizes the rule to a single loop.**

**The other structural change from [78](78-subsets.md):** the result is recorded at the **top of every call**, not only at a base case. This "loop over remaining candidates" formulation naturally visits every subset as a node in the tree, rather than only at leaves. It's the same shape as [Combination Sum](39-combination-sum.md) — and it's why there's no explicit `if i == len(nums)` base case; the loop simply ends.

**The counting alternative:** group equal values, and for a value appearing k times choose 0, 1, …, or k copies. Avoids duplicates by construction with no skip condition. Worth mentioning.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
nums.sort()
result = []
path = []
```

**Sorting is mandatory here**, not an optimization — it puts equal values adjacent so the duplicate check can compare against the immediate predecessor. Without it, `[2,1,2]` would hide its duplicates from the `nums[i] == nums[i-1]` test.
→ [list-methods](../syntax/list-methods.md) · [sorting-key](../syntax/sorting-key.md)

```python
def backtrack(start):
    result.append(path[:])
```

**Record at every node**, not just at leaves. In this formulation each recursive call represents a distinct subset — the one built so far — so every call contributes exactly one result.

The very first call records `[]`, giving the empty subset for free.

`path[:]` copies, as always.
→ [recursion-basics](../syntax/recursion-basics.md) · [list-slicing](../syntax/list-slicing.md)

```python
    for i in range(start, len(nums)):
```

Only consider candidates at index `start` or later — the same non-decreasing-index rule as [Combination Sum](39-combination-sum.md), which prevents generating reorderings of the same subset.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md)

```python
        if i > start and nums[i] == nums[i - 1]:
            continue
```

**The duplicate skip — the one line that distinguishes this from [Subsets](78-subsets.md).**

- **`i > start`** — not the first candidate at this level, so an identical-valued branch already ran here.
- **`nums[i] == nums[i-1]`** — same value as the previous candidate (meaningful because sorted).

Skipping means the second 2 never *starts* a branch at this level, so `[2]` is generated once instead of twice. But when `i == start`, the check is bypassed — which is what still permits `[2,2]` via a deeper call.
→ [break-continue](../syntax/break-continue.md) · [logical-operators](../syntax/logical-operators.md)

```python
        path.append(nums[i])
        backtrack(i + 1)
        path.pop()
```

**Choose → explore → un-choose**, unchanged from [Subsets](78-subsets.md).

**`i + 1`** — each *occurrence* is used at most once, since this is a subset problem. (Contrast [Combination Sum](39-combination-sum.md), which passed `i` to allow reuse.)
→ [list-methods](../syntax/list-methods.md)

```python
backtrack(0)
return result
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:

        nums.sort()
        result = []
        path = []

        def backtrack(start):
            result.append(path[:])

            for i in range(start, len(nums)):
                if i > start and nums[i] == nums[i - 1]:
                    continue
                path.append(nums[i])
                backtrack(i + 1)
                path.pop()

        backtrack(0)
        return result
```

</details>

**Trace it** — `nums = [1,2,2]` (already sorted):

```
backtrack(0)  path=[]                    → record []
├─ i=0, take 1 → backtrack(1)  path=[1]  → record [1]
│  ├─ i=1, take 2 → backtrack(2) [1,2]   → record [1,2]
│  │  └─ i=2, take 2 → backtrack(3) [1,2,2] → record [1,2,2]
│  └─ i=2: i>start(1) and nums[2]==nums[1] → SKIP ⛔
├─ i=1, take 2 → backtrack(2)  path=[2]  → record [2]
│  └─ i=2, take 2 → backtrack(3) [2,2]   → record [2,2]
└─ i=2: i>start(0) and nums[2]==nums[1] → SKIP ⛔
```

Result: `[[], [1], [1,2], [1,2,2], [2], [2,2]]` ✅ — **6 unique subsets**, versus [78](78-subsets.md)'s 8 with two duplicates.

The two skips are exactly where the duplicates would have appeared:

- The last skip (at `start=0`) would have produced a second `[2]`.
- The earlier one (at `start=1`) would have produced a second `[1,2]`.

**And crucially, `[2,2]` and `[1,2,2]` survive** — those come from taking the second 2 at a *deeper* level where `i == start`, so the check doesn't fire. That's the `i > start` condition doing precisely its job.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n · 2ⁿ)</summary>

**O(n · 2ⁿ)** worst case — the same bound as [Subsets](78-subsets.md).

- Up to 2ⁿ subsets when all elements are distinct (no skips fire).
- O(n) per subset to copy.
- Plus O(n log n) for the sort, dominated by the exponential.

**With duplicates the real count is lower.** If a value appears k times, it contributes k+1 choices (take 0, 1, …, k) rather than 2^k. So `[2,2,2]` gives 4 subsets instead of 8 — the skip prunes those branches away entirely.

**The exact count** is the product over distinct values of (count + 1). For `[1,2,2]`: 2 × 3 = **6** ✅ — matching the trace.

**Prevention versus deduplication, concretely:**

| Approach | Work done | Extra space |
|---|---|---|
| Generate all + set-dedupe | **2ⁿ** subsets generated, then filtered | **O(2ⁿ)** for the set |
| **Skip at the source** | Only unique subsets generated | **O(1)** |

Same asymptotic class in the worst case, but on duplicate-heavy input the skipping version explores a genuinely smaller tree — and never allocates the set. **Pruning at the branch beats filtering at the leaf.**

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n) auxiliary</summary>

**O(n) auxiliary**, plus the output.

| Component | Size |
|---|---|
| `result` (required output) | up to 2ⁿ subsets → **O(n · 2ⁿ)** |
| Recursion depth | at most n → **O(n)** |
| `path` | at most n → O(n) |
| Sorting | O(n) for Timsort |

**No deduplication structure is needed** — that's the space win over the set-based approach, which would hold up to 2ⁿ tuples just to detect repeats.

**The recursion is n deep, not 2ⁿ** — one frame per element chosen along the current path. Same point as [Subsets](78-subsets.md).

**Sorting mutates the input.** `nums.sort()` reorders the caller's array in place. Usually fine on LeetCode, but worth flagging as an API concern — `sorted(nums)` would cost O(n) extra and leave the input untouched. **A small thing to mention; interviewers notice when you're aware of it.**

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "This is Subsets plus one problem: duplicate *values* at different *indices* produce identical subsets. I sort first so equal values are adjacent, then within a single loop level I skip any candidate equal to its predecessor. The condition is `i > start and nums[i] == nums[i-1]` — the `i > start` part is essential, because it localizes the rule to one recursion level. Skipping the second 2 at the same level prevents a duplicate `[2]`, but when the second 2 is the *first* candidate of a deeper call the check doesn't fire, so `[2,2]` is still generated correctly. I prevent duplicates rather than generating everything and deduplicating with a set — that prunes the tree instead of filtering its output, and needs no extra memory. O(n·2ⁿ) worst case, O(n) auxiliary."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why `i > start` and not `i > 0`?" | **The question.** `i > 0` would block the second 2 even as a deeper level's first choice, killing `[2,2]`. `start` localizes the rule to one loop. |
| "Why must you sort?" | The check compares against the immediate predecessor, which only finds duplicates if equal values are adjacent. |
| "Why not generate everything and dedupe?" | Correct but wasteful — it generates duplicates then discards them, and needs O(2ⁿ) space for the set. |
| "Alternative without the skip condition?" | Count occurrences of each distinct value, then choose 0..k copies of each. Duplicate-free by construction. |
| "Same idea for **permutations** with duplicates?" | Similar but subtler: `if i > 0 and nums[i] == nums[i-1] and not used[i-1]: continue`. The extra `used` check is needed because permutations have no `start`. LeetCode 47. |
| "How many unique subsets are there?" | The product of (count + 1) over distinct values. For `[1,2,2]`: 2 × 3 = 6. |
| "Does sorting mutate the input?" | Yes — `sorted(nums)` avoids it at O(n) extra space. |

**Traps:**

- **`i > 0` instead of `i > start`.** Over-skips and loses valid subsets like `[2,2]`. The defining bug here.
- **Forgetting to sort** — the adjacency check finds nothing and duplicates slip through.
- **Comparing `nums[i] == nums[i+1]`** instead of `i-1` — skips the *first* occurrence rather than the repeats.
- **Skipping based on `path` contents** rather than loop position. It's about which branches you start at this level, not what's already chosen.
- **Passing `i` instead of `i + 1`** — that allows reuse, which is [Combination Sum](39-combination-sum.md), not subsets.
- **Recording only at a base case** — in this formulation every call *is* a subset.

**This same move shows up in:** [Subsets](78-subsets.md) (this without duplicates) · [Combination Sum II](40-combination-sum-ii.md) (the same skip rule plus a target) · [Combination Sum](39-combination-sum.md) (the `start` mechanism) · [Permutations](46-permutations.md) (where the duplicate rule needs an extra `used` check) · [backtracking](../algorithms/backtracking.md).

</details>

---
