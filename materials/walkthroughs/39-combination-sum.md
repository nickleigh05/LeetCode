# 39. Combination Sum

**Medium** · [LeetCode](https://leetcode.com/problems/combination-sum/) · [Solution file (no hints)](../../problems/0001-0499/39.py)

[📖 10. Backtracking lesson](../learning/10-backtracking.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 10. Backtracking problems](../rmap-practice/10-backtracking.md)

---

Given an array of **distinct** integers `candidates` and a target integer `target`, return a list of **all unique combinations** of candidates where the chosen numbers sum to `target`.

**The same number may be chosen an unlimited number of times.** Two combinations are different if the *frequency* of at least one chosen number differs.

```
candidates = [2,3,6,7], target = 7   →  [[2,2,3], [7]]
candidates = [2,3,5],   target = 8   →  [[2,2,2,2], [2,3,3], [3,5]]
candidates = [2],       target = 1   →  []
```

**Constraints:** `1 <= candidates.length <= 30` · `2 <= candidates[i] <= 40` · all **distinct** · `1 <= target <= 40`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**unlimited** number of times" | ⚠️ After choosing a candidate you may choose it **again** — so the recursion doesn't advance past it |
| "**unique** combinations" | `[2,2,3]` and `[2,3,2]` are the same combination. You must generate each **multiset** once |
| "candidates are **distinct**" | No duplicate values in the input — that complication is [Combination Sum II](40-combination-sum-ii.md)'s |
| candidates ≥ 2, target ≤ 40 | ⚠️ Depth is bounded: at least 2 per step means at most **20** levels |
| small bounds throughout | Exponential enumeration is expected |

**The reuse point.** In [Subsets](78-subsets.md) each element was decided once and you moved on. Here, choosing a 2 doesn't exhaust the 2 — you can take another. So after picking `candidates[i]`, the next call still starts at **`i`**, not `i + 1`.

**The uniqueness point — this is the subtle one.** How do you generate `[2,2,3]` but *not* `[2,3,2]` and `[3,2,2]`, which are the same combination?

By enforcing **non-decreasing index order**: each recursive call may only choose candidates at index `i` or later, never earlier.

```
allowed:  2 → 2 → 3    (indices 0, 0, 1 — never decreasing)
blocked:  2 → 3 → 2    (would need to go back to index 0 from index 1)
```

Every multiset then has exactly **one** representation — the one in sorted index order. **Ordering the choices is what eliminates permutations**, without any deduplication step.

**The pruning point.** If you sort the candidates first, then once a candidate exceeds the remaining target, every later candidate does too — so you can `break` out of the loop entirely rather than `continue`.

🤔 **Before you open the next section:** if the recursion passes `i` rather than `i + 1`, what stops it recursing forever on the same candidate?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Verdict |
|---|---|---|
| Generate all subsets, filter by sum | Enumerate everything, keep sums matching | ❌ Doesn't allow reuse, and no pruning |
| Include/exclude per candidate | Binary tree as in [Subsets](78-subsets.md), staying on include | ✅ Equivalent formulation |
| **Loop from `start`, recurse at `i`** | Try each candidate ≥ start, allow reuse | ✅ |
| Dynamic programming | Build up sums | ⚠️ Good for *counting* combinations, awkward for *listing* them |

**The decision: backtracking with a `start` index and a running remainder, iterating from `start` and recursing at `i`.**

Three mechanisms, each solving one requirement:

| Mechanism | Solves |
|---|---|
| `for i in range(start, len(candidates))` | Only choose at index ≥ start → **no permutations** |
| `backtrack(i, ...)` — not `i + 1` | **Unlimited reuse** of the same candidate |
| `if candidates[i] > remaining: break` | **Pruning** dead branches early |

**Why `remaining` counts down rather than tracking a running sum.** Subtracting means the base case is simply `remaining == 0`, and the pruning test is a direct comparison against what's left. Both read more naturally than comparing an accumulated total against `target`.

**Why sorting enables `break` instead of `continue`.** Sorted candidates mean that if `candidates[i]` already exceeds `remaining`, so does everything after it — so the whole rest of the loop is dead. `break` abandons it in one step. Without sorting you'd need `continue` and would keep testing hopeless candidates.

That's a real optimization, not a cosmetic one: it turns "check every remaining candidate" into "stop at the first that's too big."

**Why the recursion terminates despite reuse.** Every choice subtracts at least the smallest candidate (≥ 2 here) from `remaining`, so `remaining` strictly decreases and hits 0 or goes negative within `target / min_candidate` steps. **Reuse doesn't mean infinite recursion, because the remainder is always shrinking.**

**Compare with [Subsets](78-subsets.md):**

| | Advance | Result |
|---|---|---|
| [Subsets](78-subsets.md) | `i + 1` | each element used at most once |
| **Combination Sum** | **`i`** | unlimited reuse |
| [Combination Sum II](40-combination-sum-ii.md) | `i + 1` + skip duplicates | each *occurrence* used once |

**One character — `i` versus `i + 1` — is the whole difference.**

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
result = []
candidates.sort()
```

**Sorting enables the `break`.** Once a candidate is too large, all later ones are too — so the loop can be abandoned rather than continued.

It also means combinations come out in sorted order, which makes the output tidy (though the problem doesn't require it).
→ [list-methods](../syntax/list-methods.md) · [sorting-key](../syntax/sorting-key.md)

```python
def backtrack(start, remaining, path):
    if remaining == 0:
        result.append(path[:])
        return
```

**Base case: the remainder hit exactly zero** ⇒ the path sums to the target. Record a **copy**, for the same reason as [Subsets](78-subsets.md) — `path` is one shared list that keeps mutating.

Note there's no `remaining < 0` case, because the pruning below never lets an oversized candidate be chosen.
→ [recursion-basics](../syntax/recursion-basics.md) · [list-slicing](../syntax/list-slicing.md) · [if-return](../syntax/if-return.md)

```python
    for i in range(start, len(candidates)):
```

**Start at `start`, never earlier.** This is what enforces non-decreasing index order and therefore generates each combination exactly once — `[2,3,2]` is unreachable because reaching index 1 forbids returning to index 0.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md)

```python
        if candidates[i] > remaining:
            break
```

**The pruning.** This candidate alone overshoots the remainder, so it can't be part of any solution from here — and because the list is sorted, **neither can anything after it**.

`break`, not `continue`: abandoning the entire rest of the loop is the whole benefit of sorting.
→ [break-continue](../syntax/break-continue.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
        path.append(candidates[i])
        backtrack(i, remaining - candidates[i], path)
        path.pop()
```

**Choose → explore → un-choose**, the [Subsets](78-subsets.md) skeleton, with two problem-specific details:

- **`backtrack(i, ...)` — not `i + 1`.** Staying at `i` is what permits reusing the same candidate. This single character is the defining line of the problem.
- **`remaining - candidates[i]`** — the remainder shrinks by what was just taken, which both drives the base case and guarantees termination.

The `pop()` restores `path` before the next candidate is tried.
→ [list-methods](../syntax/list-methods.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
backtrack(0, target, [])
return result
```

Start at index 0 with the full target remaining and an empty path.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:

        result = []
        candidates.sort()

        def backtrack(start, remaining, path):
            if remaining == 0:
                result.append(path[:])
                return

            for i in range(start, len(candidates)):
                if candidates[i] > remaining:
                    break
                path.append(candidates[i])
                backtrack(i, remaining - candidates[i], path)
                path.pop()

        backtrack(0, target, [])
        return result
```

</details>

**Trace it** — `candidates = [2,3,6,7]` (already sorted), `target = 7`:

```
backtrack(0, 7, [])
├─ i=0, take 2 → backtrack(0, 5, [2])           ← still index 0: reuse allowed
│  ├─ i=0, take 2 → backtrack(0, 3, [2,2])
│  │  ├─ i=0, take 2 → backtrack(0, 1, [2,2,2])
│  │  │  └─ i=0: 2 > 1 → BREAK (dead end)
│  │  ├─ i=1, take 3 → backtrack(1, 0, [2,2,3])  → remaining 0 ✅ RECORD [2,2,3]
│  │  └─ i=2: 6 > 3 → BREAK
│  ├─ i=1, take 3 → backtrack(1, 2, [2,3])
│  │  └─ i=1: 3 > 2 → BREAK
│  └─ i=2: 6 > 5 → BREAK
├─ i=1, take 3 → backtrack(1, 4, [3])
│  ├─ i=1, take 3 → backtrack(1, 1, [3,3]) → 3 > 1 → BREAK
│  └─ i=2: 6 > 4 → BREAK
├─ i=2, take 6 → backtrack(2, 1, [6]) → 6 > 1 → BREAK
└─ i=3, take 7 → backtrack(3, 0, [7]) → remaining 0 ✅ RECORD [7]
```

Result: `[[2,2,3], [7]]` ✅

Two things to notice:

- **`[3,2,2]` never appears.** Once the recursion reaches index 1 (the 3), it can't return to index 0, so that ordering is structurally unreachable — no deduplication needed.
- **The `break`s cut off large regions.** At `[2,2,2]` with remaining 1, every remaining candidate is too big, and the branch dies immediately rather than testing 3, 6 and 7 individually.

</details>

<details>
<summary><b>4 · Time complexity</b> — exponential, roughly O(n^(T/m))</summary>

**O(n^(T/m))** in the worst case, where n = number of candidates, T = target, and m = the smallest candidate.

The reasoning: each level of recursion picks one candidate (up to n choices), and the depth is bounded by **T/m** — since every choice subtracts at least `m` from the remainder.

**With these constraints:** candidates ≥ 2 and target ≤ 40, so the depth is at most **20** levels. That, plus the pruning, keeps it entirely manageable.

**This is output-sensitive.** The true cost tracks the number of valid combinations plus the explored dead branches. There's no useful polynomial bound because the output itself can be exponential — recognizing that from the constraints is the point.

**What the pruning buys.** Without the sorted `break`, every branch would test all n candidates even when they obviously overshoot. With it, a branch dies at the first too-large candidate — cutting off large regions of the tree, as the trace shows.

**Why `break` beats `continue`:** `continue` would keep checking the remaining candidates one by one, all of them doomed. `break` discards them in a single step. Same asymptotic class, dramatically fewer nodes visited.

**Copying costs O(len(path)) per solution**, which is folded into the output size.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(T/m) auxiliary</summary>

**O(T/m) auxiliary** — the recursion depth — plus the output.

- **Recursion depth:** each frame subtracts at least `m` from the remainder, so at most **T/m** frames. With T ≤ 40 and m ≥ 2, that's **≤ 20**.
- **`path`:** at most the same depth → O(T/m).
- **`result`:** the required output, potentially exponential.

So: **"O(target / min_candidate) auxiliary, plus the output."** With these bounds, effectively **O(20) = O(1)**.

**The single shared `path`** is what keeps this small. Passing a fresh list to each recursive call would cost O(depth) *per frame* and O(depth²) overall — the same trade discussed in [Subsets](78-subsets.md).

**Note `path` is passed as a parameter here** but is still the *same list object* throughout — Python passes the reference, not a copy. So the `append`/`pop` discipline is exactly as essential as when it was a closure variable in [Subsets](78-subsets.md). Passing it explicitly is a style choice, not a semantic one.

**Sorting is O(n log n) time and O(n) space** for Timsort — negligible against the exponential search, and it pays for itself immediately through the pruning.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Two requirements shape this. Unlimited reuse means that after choosing a candidate the recursion stays at the same index rather than advancing — that one character is the difference from Subsets. And uniqueness means I must not generate permutations of the same multiset, which I enforce by only ever choosing candidates at index `start` or later. That makes each combination reachable by exactly one path, so no deduplication is needed. I sort first so that once a candidate exceeds the remaining target I can `break` out of the loop entirely, since everything after it is also too large. The remainder counts down, which makes the base case `remaining == 0` and also guarantees termination despite the reuse. O(target / min_candidate) recursion depth — at most 20 here."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why `backtrack(i)` and not `i + 1`?" | **The question.** Staying at `i` allows the same candidate to be reused. `i + 1` would give each candidate at most once. |
| "How do you avoid permutations like `[2,3,2]`?" | Only choose at index ≥ `start`, so index order never decreases and each multiset has exactly one representation. |
| "Why does reuse not recurse forever?" | Every choice subtracts at least the minimum candidate, so `remaining` strictly decreases. |
| "What if candidates could **repeat** in the input?" | Skip duplicate values at the same recursion level, and advance with `i + 1` — that's [Combination Sum II](40-combination-sum-ii.md). |
| "Just **count** the combinations?" | Then it's DP, not backtracking — see [Coin Change II](518-coin-change-ii.md). Listing them requires enumeration; counting doesn't. |
| "What if candidates could be negative or zero?" | Termination breaks — the remainder no longer strictly decreases and you'd loop forever. You'd need an explicit depth or usage cap. |
| "Why `break` rather than `continue`?" | Sorted order means everything after an oversized candidate is also oversized, so the rest of the loop is dead. |

**Traps:**

- **Advancing with `i + 1`** — silently forbids reuse and returns only combinations of distinct candidates.
- **Starting the loop at 0** instead of `start` — generates every permutation, so `[2,2,3]`, `[2,3,2]` and `[3,2,2]` all appear.
- **Appending `path` instead of `path[:]`** — every result aliases the same eventually-empty list.
- **`continue` instead of `break`** after sorting — correct, but wastes the pruning.
- **Forgetting to sort** while still using `break` — you'd cut off valid smaller candidates that come later.
- **Handling `remaining < 0`** as a base case. Not wrong, but the pruning already prevents it — a redundant branch.

**This same move shows up in:** [Subsets](78-subsets.md) (the skeleton, with `i + 1`) · [Combination Sum II](40-combination-sum-ii.md) (this problem with input duplicates) · [Permutations](46-permutations.md) (where order *does* matter, so the `start` trick is dropped) · [Coin Change](322-coin-change.md) (the same reuse structure, solved by DP because it only needs a count) · [backtracking](../algorithms/backtracking.md).

</details>

---
