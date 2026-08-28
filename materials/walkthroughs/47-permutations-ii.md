# 47. Permutations II

**Medium** · [LeetCode](https://leetcode.com/problems/permutations-ii/) · [Solution file (no hints)](../../problems/0001-0499/47.py)

[📖 10. Backtracking lesson](../learning/10-backtracking.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 10. Backtracking problems](../rmap-practice/10-backtracking.md)

---

Given a collection `nums` that **might contain duplicates**, return all possible **unique** permutations, in any order.

```
nums = [1,1,2]  →  [[1,1,2], [1,2,1], [2,1,1]]        (3, not 6)
nums = [1,2,3]  →  [[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]]
```

**Constraints:** `1 <= nums.length <= 8` · `-10 <= nums[i] <= 10`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**permutations**" | Order matters → `used` array, no `start` index — the [Permutations](46-permutations.md) skeleton |
| "**might contain duplicates**" | ⚠️ The whole problem. `[1,1,2]` has 3 distinct permutations, not 3! = 6 |
| "**unique** permutations" | Duplicates must be suppressed **during** the search, not filtered afterwards |
| `n <= 8` | 8! = 40,320. Small, but the all-duplicates case makes brute force absurd |

**This is [Permutations](46-permutations.md) + [Subsets II](90-subsets-ii.md).** You already own both halves:

- from [Permutations](46-permutations.md): the `used` array, the "path is full" base case, the two-part un-choose
- from [Subsets II](90-subsets-ii.md) / [Combination Sum II](40-combination-sum-ii.md): **sort first, then skip a value equal to its predecessor**

The only new thinking is *what exactly the skip condition has to be*, because the combination version doesn't transfer unchanged.

**Where the duplicates come from.** Label the two 1s as `1ᵃ` and `1ᵇ` so you can tell them apart. The plain [Permutations](46-permutations.md) code produces all 3! = 6 orderings:

```
[1ᵃ,1ᵇ,2]   [1ᵇ,1ᵃ,2]     ← identical once labels are dropped
[1ᵃ,2,1ᵇ]   [1ᵇ,2,1ᵃ]     ← identical
[2,1ᵃ,1ᵇ]   [2,1ᵇ,1ᵃ]     ← identical
```

Every distinct permutation is generated **twice** — once for each ordering of the interchangeable 1s. The fix must pick exactly **one** representative from each pair.

**The rule that picks a representative:** among equal values, insist they are used **left to right**. `1ᵃ` must be placed before `1ᵇ`. That kills `[1ᵇ,1ᵃ,2]` and keeps `[1ᵃ,1ᵇ,2]`, cutting each pair to one.

**Why the [Combination Sum II](40-combination-sum-ii.md) skip line won't work as-is.** There the rule was:

```python
if i > start and nums[i] == nums[i - 1]:
    continue
```

But there is no `start` in a permutation problem — the loop runs over *all* indices every time. So `i > start` has nothing to compare against, and the condition has to be rebuilt out of the state that *does* exist: the `used` array.

🤔 **Before you open the next section:** you want to allow `1ᵃ` then `1ᵇ`, but forbid `1ᵇ` then `1ᵃ`. At the moment you're considering `1ᵇ`, what does `used[index of 1ᵃ]` tell you about which of those two you're in?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Generate all n!, dedupe with a set | Plain [Permutations](46-permutations.md), then `set()` | O(n·n!) always | ❌ `[2]*8` does 40,320 permutations to return **1** |
| `set(itertools.permutations(nums))` | Library + dedupe | O(n·n!) | ⚠️ One-liner, same waste, sidesteps the exercise |
| **Sort + skip-duplicate-branch** | Prune duplicates at the node | **O(n · unique perms)** | ✅ |
| **Counter-based** (choose *values*, not indices) | Loop over distinct values with counts | O(n · unique perms) | ✅ Arguably cleaner; no sort needed |

**The decision: sort, then skip a value whose equal predecessor is unused.**

```python
if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
    continue
```

**Reading the three parts:**

| Clause | Job |
|---|---|
| `i > 0` | Guard so `nums[i-1]` doesn't wrap to the last element |
| `nums[i] == nums[i-1]` | Only equal values can produce duplicate branches (this is why the **sort** matters — it makes equal values adjacent) |
| `not used[i-1]` | **The representative rule.** The twin to my left is *not* in the current path, so placing me now would mean using the pair right-to-left |

**Why `not used[i-1]` means "duplicate branch".** Consider choosing a value at some position, with two equal candidates `1ᵃ` (index 0) and `1ᵇ` (index 1):

- `used[0] == True` → `1ᵃ` is already in the path, so putting `1ᵇ` next continues the **left-to-right** order. **Allowed.**
- `used[0] == False` → `1ᵃ` is *not* in the path. Placing `1ᵇ` first would use the pair **right-to-left** — and the branch that places `1ᵃ` here instead is generated separately by this same loop and produces an identical result. **Skip.**

So the condition doesn't reject duplicate *values*; it rejects duplicate *branches*, keeping one canonical representative of each.

⚠️ **A widely repeated claim that is wrong.** You will often read that `not used[i-1]` is required and `used[i-1]` is broken. **Both produce correct output** — I checked both against `set(itertools.permutations(...))` over 3000 random inputs, 0 failures each. The difference is efficiency, and it is dramatic:

| `nums` | unique perms | nodes with `not used[i-1]` | nodes with `used[i-1]` |
|---|---|---|---|
| `[1,1,1,1]` | 1 | **5** | 23 |
| `[1,1,2,2,3,3]` | 90 | **271** | 550 |
| `[2,2,2,2,2,2,2,2]` | 1 | **9** | 2,781 |
| `[1,1,2,2,3,3,4,4]` | 2,520 | **7,365** | 16,201 |
| `[1,2,3,4,5,6,7,8]` (no dups) | 40,320 | 109,601 | 109,601 |

`not used[i-1]` prunes the duplicate branch at its **root**; `used[i-1]` prunes it only at the **leaf**, after descending the whole subtree. Same answers, up to 300× the work. **Use `not used[i-1]`** — and knowing *why* both work is a strong thing to be able to say.

**The Counter alternative** avoids the sort and the index reasoning entirely by iterating over **distinct values** rather than positions:

```python
counts = Counter(nums)
def backtrack():
    if len(path) == len(nums):
        res.append(path[:]); return
    for num in counts:
        if counts[num] == 0:
            continue
        counts[num] -= 1; path.append(num)
        backtrack()
        path.pop(); counts[num] += 1
```

Duplicates become **structurally impossible** — each distinct value is offered once per node, so no skip rule is needed at all. I verified this against the sort-based version over the same 3000 cases: identical output. **Worth naming as the cleaner formulation**; the sorted version is the one usually expected, because the skip-rule idea transfers to [Subsets II](90-subsets-ii.md) and [Combination Sum II](40-combination-sum-ii.md).

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
nums.sort()
res = []
path = []
used = [False] * len(nums)
```

**The sort is load-bearing**, not cosmetic: it makes equal values **adjacent**, which is the only reason comparing `nums[i]` to `nums[i-1]` detects duplicates at all. Without it, `[1,2,1]` never puts the two 1s side by side and the skip rule silently does nothing.
→ [sorting-key](../syntax/sorting-key.md) · [list-basics](../syntax/list-basics.md)

```python
def backtrack():
    if len(path) == len(nums):
        res.append(path[:])
        return
```

**Base case unchanged from [Permutations](46-permutations.md):** the path is full. Length, not an index — there is no index advancing.
→ [recursion-basics](../syntax/recursion-basics.md) · [list-slicing](../syntax/list-slicing.md)

```python
    for i in range(len(nums)):
        if used[i]:
            continue
```

Every index is a candidate (no `start` — order matters), skipping ones already in the path.
→ [for-loop](../syntax/for-loop.md) · [break-continue](../syntax/break-continue.md)

```python
        if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
            continue
```

**The one new line in the whole problem.** "I'm equal to my left neighbour, and my left neighbour isn't in the path — so this branch is a mirror of one already being explored. Skip it."

Note it must come **after** the `used[i]` check but **before** choosing. And it's `continue`, not `break`: later indices may hold *different* values that are perfectly valid.
→ [logical-operators](../syntax/logical-operators.md)

```python
        used[i] = True
        path.append(nums[i])
        backtrack()
        path.pop()
        used[i] = False
```

**Choose, explore, un-choose — both parts**, exactly as in [Permutations](46-permutations.md). Two mutations down, two restorations up.
→ [list-methods](../syntax/list-methods.md)

```python
backtrack()
return res
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def permuteUnique(self, nums: List[int]) -> List[List[int]]:

        nums.sort()
        res = []
        path = []
        used = [False] * len(nums)

        def backtrack():
            if len(path) == len(nums):
                res.append(path[:])
                return

            for i in range(len(nums)):
                if used[i]:
                    continue
                if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                    continue

                used[i] = True
                path.append(nums[i])
                backtrack()
                path.pop()
                used[i] = False

        backtrack()
        return res
```

</details>

**Trace it** — `nums = [1,1,2]` after sorting, indices `0:1  1:1  2:2`. This is verified output; every skip is shown:

| Depth | `i` | What happens | `path` | `used` |
|---|---|---|---|---|
| 0 | 0 | choose `1` | `[1]` | `T F F` |
| 1 | 0 | already used → skip | | |
| 1 | 1 | choose `1` — twin at 0 **is** used, so allowed | `[1,1]` | `T T F` |
| 2 | 0,1 | already used → skip | | |
| 2 | 2 | choose `2` | `[1,1,2]` | `T T T` |
| 3 | — | **base case** → record **`[1,1,2]`** ✅ | | |
| 1 | 2 | choose `2` | `[1,2]` | `T F T` |
| 2 | 1 | choose `1` — twin at 0 **is** used, allowed | `[1,2,1]` | `T T T` |
| 3 | — | **base case** → record **`[1,2,1]`** ✅ | | |
| 0 | 1 | `nums[1]==nums[0]` and twin **unused** → **SKIP** ⚠️ | | |
| 0 | 2 | choose `2` | `[2]` | `F F T` |
| 1 | 0 | choose `1` | `[2,1]` | `T F T` |
| 2 | 1 | choose `1` — twin used, allowed | `[2,1,1]` | `T T T` |
| 3 | — | **base case** → record **`[2,1,1]`** ✅ | | |
| 1 | 1 | twin at 0 unused → **SKIP** ⚠️ | | |

**3 results, not 6** ✅

The two ⚠️ rows are the entire mechanism. Both occur at the moment index 1 is offered while index 0 is still unused — that is precisely "starting a branch with `1ᵇ` before `1ᵃ`". The first one, at depth 0, prunes an entire subtree that would have re-derived `[1,1,2]` and `[1,2,1]`.

Compare against the decision tree without the skip:

```
without skip (6 leaves)          with skip (3 leaves)
        []                              []
   1ᵃ ╱ 1ᵇ│ ╲ 2                    1ᵃ ╱   ✂    ╲ 2
   ╱     │    ╲                      ╱            ╲
[1ᵃ]  [1ᵇ]    [2]                 [1ᵃ]            [2]
 ⋮      ⋮      ⋮                   ⋮      1ᵇ✂ ╱  ╲ 1ᵃ
2 each  2 each  2 each          2 leaves          1 leaf
```

The middle subtree is cut at the root — that's why the savings compound so hard on inputs like `[2]*8`.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n · P) where P is the number of *unique* permutations</summary>

**O(n · P)**, where **P = n! / (m₁! · m₂! · … )** and each `mⱼ` is the multiplicity of a distinct value.

- **P leaves** — the multinomial coefficient, i.e. the true number of distinct permutations.
- **O(n)** to copy each one into the result.
- Sorting costs O(n log n), swallowed entirely.

**This is the payoff of pruning at the node rather than the leaf.** The generate-then-dedupe approach is O(n·n!) *regardless* of the input; this one scales with the actual output size:

| `nums` | n! (dedupe approach) | P (this approach) | ratio |
|---|---|---|---|
| `[1,2,3,4,5,6,7,8]` | 40,320 | 40,320 | 1× |
| `[1,1,2,2,3,3,4,4]` | 40,320 | **2,520** | 16× |
| `[1,1,1,1,2,2,2,2]` | 40,320 | **70** | 576× |
| `[2,2,2,2,2,2,2,2]` | 40,320 | **1** | **40,320×** |

The last row is the argument in one line: for eight identical values this algorithm visits **9 nodes total**, while generate-then-dedupe builds all 40,320 permutations to throw away 40,319 of them.

**Node overhead is a small constant factor.** Measured on `[1,1,2,2,3,3,4,4]`: 7,365 nodes for 2,520 results, ≈2.9 nodes per result — the internal nodes of the tree, not wasted work.

**This is output-optimal.** You cannot produce P results of length n in less than Ω(n·P) time. **Don't look for better.**

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n) auxiliary</summary>

**O(n) auxiliary**, plus **O(n·P)** for the required output.

| Component | Size |
|---|---|
| `res` (required output) | P permutations × n → **O(n·P)** |
| **Recursion depth** | exactly n → **O(n)** |
| `path` | at most n → O(n) |
| `used` | exactly n booleans → O(n) |
| Sort | O(n) or O(log n) depending on implementation |

So: **"O(n) auxiliary, plus the output."**

**Versus generate-then-dedupe**, which needs a set holding up to n! tuples — **O(n·n!) auxiliary**. On `[2]*8` that's 40,320 stored tuples to return one answer, against O(n) here. The space gap is as stark as the time gap.

**The Counter variant** uses O(u) for the counter where u is the number of distinct values, u ≤ n — asymptotically the same, and it drops the `used` array.

**⚠️ The sort mutates the input.** `nums.sort()` reorders the caller's list. Harmless on LeetCode; worth a `nums = sorted(nums)` if you care about not surprising a caller. The Counter version avoids the question entirely.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "This is Permutations plus the duplicate-handling idea from Subsets II. The `used` array and the full-path base case carry over unchanged. The new part is suppressing duplicate branches: I sort so equal values sit adjacent, then skip index `i` when it equals `i-1` and `i-1` is **not** currently used. That enforces a canonical order — among equal values I always place the leftmost one first — so each distinct permutation is generated exactly once. The key property is that I prune at the node rather than filtering at the end, so the cost is O(n · number of *unique* permutations) instead of O(n · n!). For eight identical values that's nine nodes instead of forty thousand. Alternatively I'd use a Counter and loop over distinct values, which makes duplicates structurally impossible and needs no skip rule at all."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why `not used[i-1]` rather than `used[i-1]`?" | **The question.** Both are *correct*; `not used[i-1]` prunes the duplicate branch at its root, the other at the leaf. On `[2]*8`: 9 nodes vs 2,781. Say both work and that one is vastly faster — that's the complete answer. |
| "Why must you sort?" | The skip rule compares `nums[i]` with `nums[i-1]`, which only detects duplicates when equal values are adjacent. Unsorted `[1,2,1]` slips through and you get 6 results. |
| "Can you drop the sort?" | Yes — with the Counter formulation, which iterates distinct values instead of indices. |
| "Why not generate all and dedupe?" | Correct but O(n·n!) time *and* space regardless of input. This prunes to O(n·P). |
| "Why is the [Combination Sum II](40-combination-sum-ii.md) rule (`i > start`) different?" | There a `start` index exists; here the loop scans all indices, so there's no `start` to compare against. The `used` array supplies the equivalent information. |
| "How many unique permutations are there?" | The multinomial `n! / (m₁!·m₂!·…)`. Good sanity check on your own output. |
| "Extend to the **k-th** unique permutation without enumerating?" | Count subtree sizes with the multinomial formula and walk down — the same factorial-number-system idea as LeetCode 60. |
| "What about the swap-based permutation trick?" | It needs a per-level `set` of already-placed values to dedupe, since swapping destroys the sorted adjacency the skip rule depends on. |

**Traps:**

- **Forgetting to sort.** The single most common failure — the skip rule becomes a no-op and you get duplicates. Sorting is what the rule *runs on*.
- **Writing `used[i-1]` instead of `not used[i-1]`.** Still correct, quietly hundreds of times slower. Not a wrong-answer bug, which is what makes it hard to notice.
- **Putting the skip check before the `used[i]` check** — harmless in practice, but the ordering above reads more clearly.
- **Using `break` instead of `continue`** — later indices hold different values and are legitimate; `break` would truncate the loop and lose results.
- **Forgetting `used[i] = False`** — the [Permutations](46-permutations.md) trap, still live here.
- **Appending `path` instead of `path[:]`** — every result aliases the same list.
- **Deduping with a `set` of tuples "just to be safe"** — masks a broken skip rule and reintroduces the O(n·n!) cost you were avoiding.

**This same move shows up in:** [Permutations](46-permutations.md) (the skeleton, without duplicates) · [Subsets II](90-subsets-ii.md) and [Combination Sum II](40-combination-sum-ii.md) (the same sort-then-skip idea, with `start` instead of `used`) · [Combination Sum III](216-combination-sum-iii.md) (a pool with no duplicates, so no skip needed) · [backtracking](../algorithms/backtracking.md).

</details>

---
