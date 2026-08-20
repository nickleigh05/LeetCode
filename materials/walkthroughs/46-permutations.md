# 46. Permutations

**Medium** · [LeetCode](https://leetcode.com/problems/permutations/) · [Solution file (no hints)](../../problems/0001-0499/46.py)

[📖 11. Backtracking lesson](../learning/11-backtracking.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 11. Backtracking problems](../rmap-practice/11-backtracking.md)

---

Given an array `nums` of **distinct** integers, return **all possible permutations**. You may return the answer in any order.

```
nums = [1,2,3]  →  [[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]]
nums = [0,1]    →  [[0,1], [1,0]]
nums = [1]      →  [[1]]
```

**Constraints:** `1 <= nums.length <= 6` · `-10 <= nums[i] <= 10` · all integers **distinct**

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**permutations**" | ⚠️ **Order matters.** `[1,2,3]` and `[2,1,3]` are different answers — the opposite of [Combination Sum](39-combination-sum.md), where they'd be the same |
| "all possible" | Exactly **n!** results |
| every element used **exactly once** | Each element appears in every permutation, once |
| elements are **distinct** | No duplicate handling needed |
| **`n <= 6`** | ⚠️ 6! = 720. The tiny bound signals factorial enumeration is expected |

**The structural inversion.** [Subsets](78-subsets.md) and [Combination Sum](39-combination-sum.md) both used a `start` index to enforce non-decreasing order — precisely so that permutations of the same selection *wouldn't* be generated separately.

Here you want exactly what those problems suppressed. So **the `start` index goes away**: at every position, any unused element is a valid choice.

```
[1,2,3]

position 1:  choose 1, 2, or 3
position 2:  choose either of the two remaining
position 3:  the last one

3 × 2 × 1 = 6 = 3! ✅
```

**Which creates a new problem.** Without `start`, the loop scans all n elements every time — so what stops it choosing the same element twice and producing `[1,1,1]`?

You need to track which elements are **already in the current path**. That's the `used` array, and maintaining it is the new bookkeeping this problem introduces:

```
choose:     used[i] = True,  path.append(nums[i])
un-choose:  path.pop(),      used[i] = False
```

Two things to undo instead of one — and both must be undone, or the search corrupts.

🤔 **Before you open the next section:** [Subsets](78-subsets.md) needed no `used` tracker. What did the `start` index do that made it unnecessary?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| `itertools.permutations` | Standard library | O(n·n!) | ⚠️ Right in production; sidesteps the exercise |
| Insert-into-every-position | Build up by inserting each new element everywhere | O(n·n!) | ✅ Neat alternative |
| **Backtracking with a `used` array** | Try every unused element at each position | **O(n·n!)** | ✅ |
| Swap-based backtracking | Swap element `i` into position, recurse, swap back | O(n·n!) | ✅ O(1) extra space |

**The decision: backtracking, choosing any unused element at each position.**

The structure, with the two changes from [Subsets](78-subsets.md) highlighted:

| | [Subsets](78-subsets.md) | **Permutations** |
|---|---|---|
| Loop range | `range(start, n)` | **`range(n)`** — every element is a candidate |
| Skip rule | none needed | **`if used[i]: continue`** |
| Base case | index reached n | **path length reached n** |
| Undo | `path.pop()` | **`path.pop()` and `used[i] = False`** |

**Why the base case changed.** In [Subsets](78-subsets.md) the recursion advanced an index, so `i == len(nums)` meant "all decisions made". Here there's no index — the loop scans everything each time — so completeness is measured by **how full the path is**: `len(path) == len(nums)`.

**Why `used` is necessary and `start` is not.** These are two different mechanisms for two different requirements:

- **`start`** prevents *revisiting earlier indices* → suppresses reorderings → gives **combinations**.
- **`used`** prevents *reusing the same element* → allows all orderings → gives **permutations**.

Getting this pairing right is most of Unit 10. When a problem says "order matters", drop `start` and add `used`; when it says "combinations", do the reverse.

**The swap-based alternative** avoids the `used` array entirely by permuting `nums` in place:

```python
def backtrack(i):
    if i == len(nums):
        res.append(nums[:]); return
    for j in range(i, len(nums)):
        nums[i], nums[j] = nums[j], nums[i]
        backtrack(i + 1)
        nums[i], nums[j] = nums[j], nums[i]      # swap back
```

O(1) extra space instead of O(n), and elegant — but it mutates the input and the ordering of results is less intuitive. **Worth naming; the `used` version is easier to explain.**

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
res = []
path = []
used = [False] * len(nums)
```

`path` is the permutation being built; `used[i]` records whether `nums[i]` is already in it.

`[False] * n` is safe here — booleans are immutable, so there's no shared-reference trap like `[[]] * n`.
→ [list-basics](../syntax/list-basics.md)

```python
def backtrack():
    if len(path) == len(nums):
        res.append(path[:])
        return
```

**Base case: the path is full**, so it's a complete permutation.

Note this measures **length**, not an index — because the loop below scans all positions every time, there's no index being advanced.

`path[:]` copies, for the same reason as [Subsets](78-subsets.md): `path` is one shared list that keeps mutating.
→ [recursion-basics](../syntax/recursion-basics.md) · [list-slicing](../syntax/list-slicing.md) · [if-return](../syntax/if-return.md)

```python
    for i in range(len(nums)):
        if used[i]:
            continue
```

**Every element is a candidate** — `range(len(nums))`, not `range(start, ...)`. That's what allows all orderings.

`continue` skips elements already in the path, which is what prevents `[1,1,1]`. This check is doing exactly the job the `start` index did in [Subsets](78-subsets.md), for the opposite purpose.
→ [for-loop](../syntax/for-loop.md) · [break-continue](../syntax/break-continue.md)

```python
        used[i] = True
        path.append(nums[i])
```

**Choose** — and note there are now **two** pieces of state to update: mark it used, and add it to the path.

```python
        backtrack()
```

**Explore.** No arguments — all the state lives in the enclosing `path` and `used`, which the closure can see.
→ [closures](../syntax/closures.md)

```python
        path.pop()
        used[i] = False
```

**Un-choose, both parts.** Forgetting either one breaks the search:

- Skip `path.pop()` → the path keeps growing and permutations come out malformed.
- Skip `used[i] = False` → the element stays permanently marked, and later branches can never use it — so you'd get only one permutation instead of n!.

**Two chooses, two un-chooses.** The symmetry is the thing to internalize: *every* piece of state you mutate on the way down must be restored on the way back up.
→ [list-methods](../syntax/list-methods.md)

```python
backtrack()
return res
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:

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
                used[i] = True
                path.append(nums[i])
                backtrack()
                path.pop()
                used[i] = False

        backtrack()
        return res
```

</details>

**Trace it** — `nums = [1,2,3]`, following the first complete branch and the first backtrack:

| Depth | Action | `path` | `used` |
|---|---|---|---|
| 0 | choose 1 | `[1]` | `T F F` |
| 1 | choose 2 | `[1,2]` | `T T F` |
| 2 | choose 3 | `[1,2,3]` | `T T T` |
| 3 | **base case** | | → record **`[1,2,3]`** ✅ |
| 2 | un-choose 3 | `[1,2]` | `T T F` |
| 1 | un-choose 2 | `[1]` | `T F F` |
| 1 | choose 3 | `[1,3]` | `T F T` |
| 2 | choose 2 | `[1,3,2]` | `T T T` |
| 3 | **base case** | | → record **`[1,3,2]`** ✅ |

…and so on. The full decision tree:

```
                    []
        1 ╱         2 │         ╲ 3
      [1]          [2]           [3]
    2 ╱ ╲ 3      1 ╱ ╲ 3       1 ╱ ╲ 2
 [1,2] [1,3]  [2,1] [2,3]   [3,1] [3,2]
   │      │     │     │       │     │
[1,2,3][1,3,2][2,1,3][2,3,1][3,1,2][3,2,1]
```

**6 leaves = 3! ✅**

Watch the `used` array at depth 1 in the trace: after un-choosing 2, `used` is back to `T F F` — so the 3 becomes selectable. **If `used[1] = False` had been forgotten, the branch `[1,3,...]` could never place the 2**, and you'd lose half the results.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n · n!)</summary>

**O(n · n!)**.

- **n! permutations** — n choices for the first position, n−1 for the second, and so on.
- **O(n) per permutation** to copy it into the result.

n! × O(n) = **O(n · n!)**.

At n = 6 that's 6 × 720 = **4,320 operations** — trivial. The `n <= 6` constraint is the problem telling you factorial growth is fine.

**Why factorial rather than exponential.** [Subsets](78-subsets.md) was 2ⁿ because each element had 2 options (in or out). Here the *first* position has n options, the second n−1, and so on — the product is n!, which grows far faster:

| n | 2ⁿ (subsets) | n! (permutations) |
|---|---|---|
| 6 | 64 | **720** |
| 10 | 1,024 | **3,628,800** |
| 15 | 32,768 | **1.3 × 10¹²** |

That's why the constraint here is 6 while [Subsets](78-subsets.md) allowed 10.

**This is output-bound and optimal.** Producing n! results of length n requires Ω(n·n!) work. **No polynomial algorithm exists** — don't look for one.

**The `used` scan adds a constant factor:** each frame loops over all n elements, skipping used ones. That's O(n) per node, already counted.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n) auxiliary</summary>

**O(n) auxiliary**, plus **O(n · n!)** for the required output.

| Component | Size |
|---|---|
| `res` (required output) | n! permutations × n elements → **O(n · n!)** |
| **Recursion depth** | exactly n — one frame per position → **O(n)** |
| `path` | at most n → O(n) |
| `used` | exactly n booleans → O(n) |

So: **"O(n) auxiliary, plus the factorial output the problem requires."**

**The recursion is only n deep**, not n! — the same point as [Subsets](78-subsets.md). n! counts root-to-leaf *paths*; only one path is on the stack at a time.

**The swap-based variant gets O(1) auxiliary** (beyond recursion) by permuting `nums` in place rather than keeping `path` and `used`:

| Approach | Auxiliary (beyond recursion) |
|---|---|
| **`used` array** | **O(n)** — `path` + `used` |
| Swap-based | **O(1)** — mutates `nums` directly |

⚠️ But it **mutates the input**, which is a real API concern — the caller's array is scrambled during the search (and restored only at the end). Worth mentioning as the space optimization while noting the trade.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Permutations differ from subsets and combinations in one crucial way: order matters, so `[1,2,3]` and `[2,1,3]` are both answers. In the combination problems I used a `start` index specifically to *prevent* reorderings — here I want them, so `start` goes away and every position considers all n elements. That creates the opposite problem: without `start`, nothing stops me reusing an element, so I track a `used` array and skip anything already in the path. The base case becomes 'path is full' rather than 'index reached the end', since there's no index advancing. And the un-choose step now has two parts — pop from the path *and* clear the used flag — because I mutated two pieces of state on the way down. O(n·n!) time, which is output-bound, and O(n) auxiliary."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why `used` here but `start` in Subsets?" | **The question.** `start` suppresses reorderings (giving combinations); `used` allows all orderings while preventing reuse (giving permutations). Different mechanisms for opposite requirements. |
| "What if there were **duplicates**?" | Sort first, then skip a value equal to its predecessor *when that predecessor is unused* — the standard `if i > 0 and nums[i] == nums[i-1] and not used[i-1]: continue`. LeetCode 47. |
| "Avoid the `used` array." | Swap-based: swap element `j` into position `i`, recurse, swap back. O(1) extra space but mutates the input. |
| "Why n! and not 2ⁿ?" | Each position has a shrinking number of choices: n × (n−1) × … × 1. Subsets had 2 choices per element. |
| "Generate the **k-th** permutation directly?" | Factorial number system — no enumeration needed. O(n²) or O(n log n). LeetCode 60. |
| "The **next** permutation in lexicographic order?" | An in-place O(n) algorithm: find the pivot, swap with the successor, reverse the suffix. LeetCode 31. |
| "What about `itertools.permutations`?" | The right production answer; mention it, then write the manual version since that's what's being tested. |

**Traps:**

- **Forgetting `used[i] = False`.** The element stays marked forever, so later branches can't use it — you'd get one permutation instead of n!. The defining bug here.
- **Forgetting `path.pop()`** — the path grows without bound.
- **Undoing in the wrong order.** Both must be undone; the order between them doesn't matter, but *omitting either* does.
- **Keeping a `start` index** out of habit — you'd generate combinations, not permutations.
- **Appending `path` instead of `path[:]`** — every result aliases the same list.
- **Using `len(path) == len(nums)` but forgetting to `return`** — the loop would run again with a full path.

**This same move shows up in:** [Subsets](78-subsets.md) (the skeleton, with `start` instead of `used`) · [Combination Sum](39-combination-sum.md) (where `start` deliberately suppresses reorderings) · [Subsets II](90-subsets-ii.md) and [Combination Sum II](40-combination-sum-ii.md) (duplicate handling) · [N-Queens](51-n-queens.md) (multiple pieces of state chosen and un-chosen together) · [backtracking](../algorithms/backtracking.md).

</details>

---
