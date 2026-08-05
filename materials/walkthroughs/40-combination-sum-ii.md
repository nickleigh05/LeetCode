# 40. Combination Sum II

**Medium** · [LeetCode](https://leetcode.com/problems/combination-sum-ii/)

[📖 10. Backtracking lesson](../learning/10-backtracking.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 10. Backtracking problems](../rmap-practice/10-backtracking.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Given a collection of candidate numbers (**which may contain duplicates**) and a target, find all **unique combinations** where the candidates sum to the target.

**Each number may be used only once** in each combination. The solution set must not contain duplicate combinations.

```
candidates = [10,1,2,7,6,1,5], target = 8
  →  [[1,1,6], [1,2,5], [1,7], [2,6]]

candidates = [2,5,2,1,2], target = 5
  →  [[1,2,2], [5]]
```

**Constraints:** `1 <= candidates.length <= 100` · `1 <= candidates[i] <= 50` · `1 <= target <= 30`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

This problem is the **synthesis** of the two before it — it takes one rule from each.

| The statement says | Which really means | Comes from |
|---|---|---|
| "each number used **only once**" | ⚠️ Advance with `i + 1`, **not** `i` | the opposite of [Combination Sum](39-combination-sum.md) |
| "may contain **duplicates**" | ⚠️ Skip repeated values at the same loop level | [Subsets II](90-subsets-ii.md) |
| "**unique** combinations" | Compared by contents, not by which indices produced them | [Subsets II](90-subsets-ii.md) |
| sums to `target` | Track a shrinking remainder | [Combination Sum](39-combination-sum.md) |

**The distinction that trips people up.** "Each number may be used only once" refers to each **occurrence in the input array**, not each **value**.

So with `candidates = [1,1,6]`, the combination `[1,1,6]` is **valid** — there are genuinely two 1s available, and each is used once. What's forbidden is using the *same* 1 twice.

That's why `i + 1` is the right advance: it moves past the specific occurrence just consumed, while leaving any later duplicates of that value available.

**And the duplicate-combination rule is separate.** With `[1,1,6]` and target 7, the combination `[1,6]` can be formed using either 1 — producing the same answer twice. That must be prevented, and it's the same skip rule as [Subsets II](90-subsets-ii.md).

**Two rules, two purposes** — and they must not be confused:

| Rule | Prevents |
|---|---|
| `backtrack(i + 1, …)` | reusing the **same occurrence** |
| `if i > start and c[i] == c[i-1]: continue` | producing the **same combination twice** |

🤔 **Before you open the next section:** with `[1,1,6]` and target 7, why does `[1,6]` need suppressing while `[1,1,...]` must still be reachable?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Verdict |
|---|---|
| [Combination Sum](39-combination-sum.md)'s code with `i + 1` | ❌ Handles no-reuse, but emits duplicate combinations |
| Generate everything, dedupe with a set | ⚠️ Correct; wasteful, and needs O(2ⁿ) memory |
| Count occurrences, choose 0..k of each value | ✅ Elegant alternative |
| **Sort + `i + 1` + skip duplicates at the level** | ✅ |

**The decision: [Combination Sum](39-combination-sum.md)'s structure, with [Subsets II](90-subsets-ii.md)'s skip rule bolted on.**

Three mechanisms, each earning its place:

| Line | Purpose |
|---|---|
| `for i in range(start, len(candidates))` | No permutations — non-decreasing index order |
| `if i > start and c[i] == c[i-1]: continue` | **No duplicate combinations** |
| `backtrack(i + 1, remaining - c[i])` | **No reuse of an occurrence** |
| `if c[i] > remaining: break` | Pruning (needs the sort) |

**Why `i > start` is again the crucial qualifier.** It restricts the skip to a single loop level:

- **Same level, second 1:** would restart an identical branch → **skip**.
- **Deeper level, second 1 as the first candidate:** `i == start`, so the check doesn't fire → `[1,1,…]` remains reachable ✅

Using `i > 0` instead would block the second 1 everywhere and lose `[1,1,6]` entirely — the same bug as in [Subsets II](90-subsets-ii.md), and it's worth being able to name why.

**Note the order of the two guards.** The duplicate skip comes **before** the `break`:

```python
if i > start and candidates[i] == candidates[i - 1]:
    continue          # skip this duplicate
if candidates[i] > remaining:
    break             # and everything after it is too big
```

Both work in either order here (a duplicate of an oversized value is also oversized), but `continue` before `break` reads more naturally: *reject this candidate specifically, then reject the whole tail.*

**Sorting does triple duty:** it makes duplicates adjacent (enabling the skip), enables the `break` pruning, and produces sorted output. **One sort, three benefits** — worth pointing out.

**The counting alternative:** group equal values and choose how many copies of each to take. Duplicate-free by construction, no skip condition needed. Worth naming.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
candidates.sort()
result = []
path = []
```

**Sorting is doing three jobs**: making duplicates adjacent for the skip check, enabling the `break` pruning, and giving sorted output.
→ [list-methods](../syntax/list-methods.md) · [sorting-key](../syntax/sorting-key.md)

```python
def backtrack(start, remaining):
    if remaining == 0:
        result.append(path[:])
        return
```

**Base case: the remainder hit exactly zero.** Record a copy — `path` is one shared mutating list, as always.

Unlike [Subsets II](90-subsets-ii.md), results are recorded only when the target is met, not at every node — because here not every partial path is an answer.
→ [recursion-basics](../syntax/recursion-basics.md) · [list-slicing](../syntax/list-slicing.md) · [if-return](../syntax/if-return.md)

```python
    for i in range(start, len(candidates)):
        if i > start and candidates[i] == candidates[i - 1]:
            continue
```

**The duplicate skip**, verbatim from [Subsets II](90-subsets-ii.md).

`i > start` confines the rule to this loop level, so a repeated value can't *start* two identical branches here — while remaining available at deeper levels where `i == start`.
→ [for-loop](../syntax/for-loop.md) · [break-continue](../syntax/break-continue.md) · [logical-operators](../syntax/logical-operators.md)

```python
        if candidates[i] > remaining:
            break
```

**The pruning**, verbatim from [Combination Sum](39-combination-sum.md). Sorted order means everything after an oversized candidate is also oversized, so `break` abandons the whole tail.
→ [comparison-operators](../syntax/comparison-operators.md)

```python
        path.append(candidates[i])
        backtrack(i + 1, remaining - candidates[i])
        path.pop()
```

**Choose → explore → un-choose**, with the single most important character being the **`i + 1`**.

That advance is what enforces "each number used only once": it moves past the occurrence just consumed. [Combination Sum](39-combination-sum.md) passed `i` here to allow reuse — **one character apart, opposite semantics.**

The remainder shrinks by what was taken, driving the base case.
→ [list-methods](../syntax/list-methods.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
backtrack(0, target)
return result
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:

        candidates.sort()
        result = []
        path = []

        def backtrack(start, remaining):
            if remaining == 0:
                result.append(path[:])
                return

            for i in range(start, len(candidates)):
                if i > start and candidates[i] == candidates[i - 1]:
                    continue
                if candidates[i] > remaining:
                    break
                path.append(candidates[i])
                backtrack(i + 1, remaining - candidates[i])
                path.pop()

        backtrack(0, target)
        return result
```

</details>

**Trace it** — `candidates = [10,1,2,7,6,1,5]`, `target = 8`. Sorted: **`[1,1,2,5,6,7,10]`**

```
backtrack(0, 8)
├─ i=0, take 1 → backtrack(1, 7)  path=[1]
│  ├─ i=1, take 1 → backtrack(2, 6)  path=[1,1]      ← i==start, skip doesn't fire ✅
│  │  ├─ i=2, take 2 → backtrack(3, 4) [1,1,2]
│  │  │  └─ i=3: 5 > 4 → BREAK
│  │  ├─ i=3: 5 ≤ 6, take 5 → backtrack(4, 1) [1,1,5] → i=4: 6 > 1 BREAK
│  │  ├─ i=4, take 6 → backtrack(5, 0) → ✅ RECORD [1,1,6]
│  │  └─ i=5: 7 > 6 → BREAK
│  ├─ i=2, take 2 → backtrack(3, 5) [1,2]
│  │  └─ i=3, take 5 → backtrack(4, 0) → ✅ RECORD [1,2,5]
│  ├─ i=3, take 5 → backtrack(4, 2) [1,5] → 6 > 2 BREAK
│  ├─ i=4, take 6 → backtrack(5, 1) [1,6] → 7 > 1 BREAK
│  └─ i=5, take 7 → backtrack(6, 0) → ✅ RECORD [1,7]
├─ i=1: i>start(0) and c[1]==c[0] → SKIP ⛔        ← would duplicate everything above
├─ i=2, take 2 → backtrack(3, 6)  path=[2]
│  ├─ i=3, take 5 → backtrack(4, 1) → 6 > 1 BREAK
│  └─ i=4, take 6 → backtrack(5, 0) → ✅ RECORD [2,6]
├─ i=3, take 5 → backtrack(4, 3) → 6 > 3 BREAK
├─ i=4, take 6 → backtrack(5, 2) → 7 > 2 BREAK
├─ i=5, take 7 → backtrack(6, 1) → 10 > 1 BREAK
└─ i=6: 10 > 8 → BREAK
```

Result: `[[1,1,6], [1,2,5], [1,7], [2,6]]` ✅

**The two 1s, doing exactly the right thing:**

- At the **top level**, `i=1` is skipped — starting a branch with the second 1 would reproduce every combination the first 1 already generated.
- At **depth 1** (inside `path=[1]`), `i=1` has `i == start`, so the skip doesn't fire and `[1,1,6]` is found ✅

**That's the whole problem in one pair of decisions**, and it's why `i > start` rather than `i > 0`.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(2ⁿ) worst case</summary>

**O(2ⁿ)** in the worst case, where n is the number of candidates — each is either in a combination or not.

More precisely: **O(n · 2ⁿ)** including the O(n) cost of copying each recorded combination.

**In practice it's far below that**, thanks to two prunings:

| Pruning | Effect |
|---|---|
| `break` on oversized candidates | Cuts off the entire tail of the loop |
| Duplicate skip | Eliminates whole redundant subtrees |

With `target <= 30` and `candidates[i] >= 1`, the recursion depth is at most **30** — and typically much less, since the sorted `break` kills branches quickly.

**The trace shows this vividly:** of 7 candidates, most branches died at the first `break`. Only 4 combinations were found, and the tree explored was a small fraction of 2⁷.

**Sorting costs O(n log n)**, dominated by the search, and it pays for itself immediately — it enables both prunings.

**As always, this is output-sensitive**: the cost tracks the number of valid combinations plus the dead branches explored. No polynomial bound exists, and the small constraints are the problem confirming that's expected.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(target) auxiliary</summary>

**O(target) auxiliary** — plus the output.

- **Recursion depth:** each frame subtracts at least 1 from the remainder, so at most `target` frames → **≤ 30** here.
- **`path`:** bounded by the same depth.
- **`result`:** the required output, potentially exponential.

So: **"O(target) auxiliary space, plus the output."**

**No deduplication structure is needed** — the skip rule prevents duplicates at the source rather than filtering them afterwards. The set-based alternative would need up to O(2ⁿ) tuples just to detect repeats.

**The depth bound is worth stating precisely.** [Combination Sum](39-combination-sum.md) was `target / min_candidate` because reuse allowed long paths of small values. Here each occurrence is used at most once, so the depth is bounded by **both** `target / min_candidate` **and** `n` — whichever is smaller.

**`candidates.sort()` mutates the input.** Fine on LeetCode; worth flagging as an API consideration, with `sorted(candidates)` as the non-destructive alternative at O(n) extra space.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "This combines the two previous problems. From Combination Sum I keep the `start` index, the shrinking remainder, and the sorted `break` pruning — but I advance with `i + 1` instead of `i`, because each number may be used only once. From Subsets II I take the duplicate skip: within one loop level, skip a candidate equal to its predecessor. The two rules do different jobs — `i + 1` prevents reusing the same *occurrence*, while the skip prevents generating the same *combination* twice. The `i > start` qualifier is what keeps them separate: it blocks a repeated value from starting two branches at the same level, but still allows it at a deeper level where it's the first choice, so `[1,1,6]` is found while a duplicate `[1,6]` isn't. Sorting does three jobs at once — makes duplicates adjacent, enables the break, and sorts the output."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "How does this differ from [Combination Sum](39-combination-sum.md)?" | **The question.** `i + 1` instead of `i` (no reuse), plus the duplicate skip. |
| "Why `i > start` and not `i > 0`?" | `i > 0` would block the second 1 everywhere, losing `[1,1,6]`. `start` localizes the rule to one loop level. |
| "Isn't `[1,1,6]` reusing the number 1?" | No — there are two 1s in the input, each used once. The rule is per *occurrence*, not per *value*. |
| "Why not dedupe with a set at the end?" | Correct but wasteful — it generates duplicates then discards them, and needs O(2ⁿ) space. |
| "Alternative without the skip rule?" | Count occurrences and choose 0..k copies of each distinct value. Duplicate-free by construction. |
| "What if candidates could be zero?" | A 0 doesn't change the remainder, so it could be added indefinitely — but `i + 1` still forces progress, so it terminates. It would produce combinations differing only by zeros. |
| "Does the guard order matter?" | Not for correctness here. `continue` before `break` reads more naturally: reject the candidate, then the tail. |

**Traps:**

- **Passing `i` instead of `i + 1`** — allows reuse, turning this back into [Combination Sum](39-combination-sum.md).
- **`i > 0` instead of `i > start`** — loses valid combinations that legitimately use two copies of a value.
- **Omitting the duplicate skip entirely** — output contains repeats.
- **Forgetting to sort** — both the skip and the `break` silently stop working.
- **Appending `path` instead of `path[:]`** — every result aliases the same list.
- **Confusing "each number once" with "each value once."** The input's duplicates are distinct occurrences.

**This same move shows up in:** [Combination Sum](39-combination-sum.md) (same structure, reuse allowed) · [Subsets II](90-subsets-ii.md) (the duplicate-skip rule) · [Subsets](78-subsets.md) (the underlying skeleton) · [Permutations](46-permutations.md) (where the duplicate rule needs an extra `used` check) · [backtracking](../algorithms/backtracking.md).

</details>

---
