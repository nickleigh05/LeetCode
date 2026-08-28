# 77. Combinations

**Medium** · [LeetCode](https://leetcode.com/problems/combinations/) · [Solution file (no hints)](../../problems/0001-0499/77.py)

[📖 10. Backtracking lesson](../learning/10-backtracking.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 10. Backtracking problems](../rmap-practice/10-backtracking.md)

---

Given integers `n` and `k`, return **all possible combinations of `k` numbers** chosen from the range `[1, n]`. Any order.

```
n = 4, k = 2  →  [[1,2], [1,3], [1,4], [2,3], [2,4], [3,4]]        (C(4,2) = 6)
n = 1, k = 1  →  [[1]]
```

**Constraints:** `1 <= n <= 20` · `1 <= k <= n`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**combinations**" | Order does **not** matter → `start` index, no `used` array |
| "`[1,2]` and `[2,1]` are the same" | The statement says this outright — it's telling you which mechanism to use |
| "**k numbers**" | Fixed-length base case: `len(path) == k` |
| "from the range `[1, n]`" | Candidates are the integers themselves, not an array — same as [Combination Sum III](216-combination-sum-iii.md) |
| `n <= 20` | ⚠️ C(20,10) = 184,756. Large enough that a wasteful search is noticeable |
| no target sum | **Simpler** than [Combination Sum III](216-combination-sum-iii.md) — one condition, not two |

**This is the purest problem in Unit 10.** Strip [Combination Sum III](216-combination-sum-iii.md) of its sum condition and this is exactly what's left: choose k things from n, in ascending order, no reuse. Nothing else.

That makes it the right place to isolate one idea: **the `start` index is what makes a combination a combination.**

```
n = 4, k = 2

with start (combinations)        without start (permutations)
[1,2] [1,3] [1,4]                [1,2] [2,1] [1,3] [3,1] …
[2,3] [2,4]
[3,4]
     6 = C(4,2)                       12 = P(4,2)
```

Every level starts *after* the number just taken, so numbers only ever ascend. `[2,1]` cannot be built — there is no path to it.

**Where the interesting part is.** With no sum to prune on, the obvious code explores branches that are **provably doomed**: paths too short to ever reach length k.

```
n = 4, k = 2, path = [4]

Only 4 is taken; nothing above 4 remains.
The path can never reach length 2 — but the naive
loop still recurses into this dead end and finds out the hard way.
```

Recognising that dead branch *before* entering it is this problem's actual lesson, and it's the same "bound the loop by what's still needed" reasoning that makes [Combination Sum](39-combination-sum.md)'s `break` work.

🤔 **Before you open the next section:** if the path has `len(path)` numbers so far and needs `k` total, how many more are needed? And given that the numbers must ascend and stop at `n`, what's the **largest** value it's still worth starting from?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| `itertools.combinations` | Standard library | O(k·C(n,k)) | ⚠️ Right in production; sidesteps the exercise |
| Bitmask enumeration | All 2ⁿ masks, keep popcount == k | O(2ⁿ·n) | ❌ 2²⁰ = 1M masks to find C(20,2) = 190 results |
| **Backtracking with `start`** | Ascending choices, no reuse | **O(k·C(n,k))** | ✅ |
| **…plus the pruning bound** | Stop the loop once too few numbers remain | **O(k·C(n,k))**, far smaller constant | ✅ ← |
| Iterative "next combination" | Advance an index vector in place | O(k·C(n,k)) | ✅ O(k) space, fiddly to write |

**The decision: backtracking with `start`, plus the upper-bound prune.**

**The naive loop first:**

```python
for i in range(start, n + 1):
```

Correct, and worth writing before optimising. Its flaw is that it will happily start a branch at `i = n` when the path still needs three more numbers — a branch with **zero** possible completions.

**The prune.** If the path holds `len(path)` numbers and needs `k` total, it still needs:

```
need = k - len(path)
```

Those must all come from `i, i+1, …, n`, which has `n - i + 1` numbers available. So a branch is worth entering only when `n - i + 1 >= need`, i.e.

```
i <= n - need + 1
```

Since `range` is exclusive at the top, the loop becomes:

```python
for i in range(start, n - (k - len(path)) + 2):
```

**Worked example**, `n = 4, k = 2` — the real bounds:

| `len(path)` | still needs | highest useful `i` |
|---|---|---|
| 0 | 2 | **3** — starting at 4 leaves nothing above it |
| 1 | 1 | **4** — any single number will do |

**How much it saves.** Measured node counts (verified, not estimated):

| n, k | C(n,k) | pruned nodes | unpruned nodes | saved |
|---|---|---|---|---|
| 4, 2 | 6 | 10 | 11 | 9% |
| 20, 2 | 190 | 210 | 211 | 0.5% |
| 20, 10 | 184,756 | 352,716 | 616,666 | **43%** |
| 20, 18 | 190 | 1,330 | 1,048,555 | **99.9%** |
| 20, 20 | 1 | 21 | 1,048,576 | **~100%** |

The pattern is worth reading: when **k is small** the prune barely matters (almost every branch is viable), but when **k approaches n** it is the difference between 21 nodes and a million. The unpruned version degenerates to enumerating all 2ⁿ subsets and discarding the wrong-sized ones; the pruned version walks straight to the answer.

**Both are O(k·C(n,k))** asymptotically — the prune removes only branches with no leaves under them, so it can't change the output-bound term. **It's a constant-factor win, and at n=20, k=20 that constant is 50,000×.** Say exactly that: *"same asymptotic bound, enormous constant-factor improvement when k is close to n."*

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
res = []
path = []
```

`path` is the combination being built; no `used` array — the `start` index handles reuse.
→ [list-basics](../syntax/list-basics.md)

```python
def backtrack(start):
    if len(path) == k:
        res.append(path[:])
        return
```

**Base case: the path is full.** One condition only — unlike [Combination Sum III](216-combination-sum-iii.md), there is no sum to also satisfy, so every full-length path is an answer.

`path[:]` copies, as always.
→ [recursion-basics](../syntax/recursion-basics.md) · [list-slicing](../syntax/list-slicing.md) · [if-return](../syntax/if-return.md)

```python
    for i in range(start, n - (k - len(path)) + 2):
```

**The pruned loop.** Unpack it right to left:

- `k - len(path)` — how many numbers are **still needed**
- `n - (that) + 1` — the **largest** value worth starting from
- `+ 2` instead of `+ 1` because `range` excludes its upper bound

Sanity check at `n = 4, k = 2`, empty path: `4 - 2 + 2 = 4`, so `range(1, 4)` → `i ∈ {1,2,3}`. Starting at 4 is correctly excluded — nothing above 4 could follow it. ✅

If this bound is hard to keep straight, **write `range(start, n + 1)` first, confirm it's correct, then tighten it.** A correct slow version beats a clever broken one.
→ [range-function](../syntax/range-function.md) · [for-loop](../syntax/for-loop.md)

```python
        path.append(i)
        backtrack(i + 1)
        path.pop()
```

**Choose, explore, un-choose.**

`i + 1` does two jobs at once: no reuse (can't pick `i` again) **and** ascending order (can't go back below `i`). That single argument is the entire combinations mechanism.
→ [list-methods](../syntax/list-methods.md)

```python
backtrack(1)
return res
```

Start at 1, since the range is `[1, n]`.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:

        res = []
        path = []

        def backtrack(start):
            if len(path) == k:
                res.append(path[:])
                return

            for i in range(start, n - (k - len(path)) + 2):
                path.append(i)
                backtrack(i + 1)
                path.pop()

        backtrack(1)
        return res
```

</details>

**Trace it** — `n = 4, k = 2`:

| Depth | `start` | loop range | Action | `path` |
|---|---|---|---|---|
| 0 | 1 | `1..3` | choose 1 | `[1]` |
| 1 | 2 | `2..4` | choose 2 | `[1,2]` |
| 2 | — | — | **base** → record **`[1,2]`** ✅ | |
| 1 | | | un-choose, choose 3 | `[1,3]` ✅ |
| 1 | | | un-choose, choose 4 | `[1,4]` ✅ |
| 0 | | | un-choose 1, choose 2 | `[2]` |
| 1 | 3 | `3..4` | choose 3, then 4 | `[2,3]` ✅ `[2,4]` ✅ |
| 0 | | | choose 3 | `[3]` |
| 1 | 4 | `4..4` | choose 4 | `[3,4]` ✅ |
| 0 | | | `i = 4` **excluded by the bound** ⚠️ | |

**6 results = C(4,2)** ✅

The decision tree:

```
                  []
        1 ╱     2 │    ╲ 3        ← 4 pruned: nothing above it
      [1]      [2]      [3]
   2╱ 3│ ╲4   3╱ ╲4      │4
 [1,2][1,3][1,4][2,3][2,4][3,4]
```

**The last row of the trace is the prune.** At depth 0 with an empty path, `i = 4` never runs — the loop's upper bound already excluded it. The naive `range(start, n + 1)` *would* enter that branch, recurse, find the loop empty, and back out having achieved nothing. One wasted node here; a million of them at `n = 20, k = 20`.

**Notice `path` shrinks and regrows** as the recursion unwinds — `[1,2]` → `[1]` → `[1,3]`. That's `path.pop()`, and it's why `path[:]` is mandatory at the base case: the list you appended would otherwise keep changing underneath the result.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(k · C(n,k))</summary>

**O(k · C(n,k))**.

- **C(n,k) combinations** in the output — the binomial coefficient.
- **O(k)** to copy each into the result.

**This is output-bound and therefore optimal.** Producing C(n,k) lists of length k cannot be done in less than Ω(k·C(n,k)). **No better algorithm exists** — don't go looking.

**The worst case is k = n/2**, where the binomial coefficient peaks:

| n = 20, k | C(20,k) |
|---|---|
| 1 | 20 |
| 5 | 15,504 |
| **10** | **184,756** ← peak |
| 15 | 15,504 |
| 20 | 1 |

At the peak that's 184,756 × 10 ≈ **1.8M operations** — comfortably fast, and the reason `n <= 20` is the stated bound.

**Internal nodes are a constant factor**, already counted: measured at n=20, k=10, the pruned search visits 352,716 nodes for 184,756 results, ≈1.9 nodes per result.

**Why not 2ⁿ.** The bitmask approach *is* 2ⁿ, and that's exactly its problem: at `k = 20` it examines 1,048,576 masks to find the single valid one. The pruned backtracking visits 21 nodes. **The gap between "enumerate everything and filter" and "only build what can succeed" is the lesson of this problem**, and it's the same lesson as [Permutations II](47-permutations-ii.md).

</details>

<details>
<summary><b>5 · Space complexity</b> — O(k) auxiliary</summary>

**O(k) auxiliary**, plus **O(k·C(n,k))** for the required output.

| Component | Size |
|---|---|
| `res` (required output) | C(n,k) combinations × k → **O(k·C(n,k))** |
| **Recursion depth** | exactly k — one frame per number chosen → **O(k)** |
| `path` | at most k → O(k) |

So: **"O(k) auxiliary, plus the binomial-sized output."**

**The recursion is k deep, not C(n,k) deep.** C(n,k) counts root-to-leaf paths; the stack holds one path at a time. With `k <= n <= 20`, depth never exceeds 20 — nowhere near Python's recursion limit.
→ [recursion-limit](../syntax/recursion-limit.md)

**No `used` array** — that's the `start` index earning its keep. The Unit 10 trade in one table:

| Mechanism | Space | Produces |
|---|---|---|
| **`start` index** | **O(1)** — one integer per frame | combinations |
| `used` array | O(n) — one flag per element | permutations |

**Streaming it instead.** If the caller only iterates the results, `yield` each combination rather than collecting into `res` — that drops the output term and leaves **O(k) total**. That's precisely what `itertools.combinations` does, and it's the right thing to mention when someone asks about memory on large n.
→ [yield-generators](../syntax/yield-generators.md)

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Combinations means order doesn't matter, so I use a `start` index rather than a `used` array — every level begins after the number just chosen, which forces ascending order and makes `[2,1]` unreachable by construction. The base case is 'path has k numbers'. The one refinement worth making is the loop's upper bound: if the path needs `k - len(path)` more numbers, there's no point starting at a value with fewer than that many above it, so the loop runs to `n - (k - len(path)) + 1`. It doesn't change the O(k·C(n,k)) bound — that's output-bound and optimal — but when k is close to n it's the difference between twenty nodes and a million. O(k) auxiliary space for the stack and path."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Explain the pruning bound." | **The question.** Need `k - len(path)` more; they must come from `i..n`, which holds `n - i + 1` numbers; so `i <= n - (k - len(path)) + 1`. Derive it live rather than reciting it. |
| "Does the prune change the complexity?" | No — it only removes branches with no leaves beneath them. Same O(k·C(n,k)); constant factor up to 50,000× at n=20, k=20. |
| "Why `start` and not `used`?" | `start` suppresses reorderings → combinations. `used` permits all orderings → permutations. Different tools for opposite requirements. |
| "Memory on large n?" | `yield` instead of collecting — O(k) total. Exactly what `itertools.combinations` does. |
| "Do it **iteratively**?" | Maintain the index vector and advance it: find the rightmost element that can increment, bump it, refill the suffix. O(k) space, no recursion. |
| "The **i-th** combination in lexicographic order?" | Combinatorial number system — walk down choosing each element by comparing `i` against C(remaining, needed). No enumeration. |
| "What if the range were an arbitrary array?" | Identical code over indices instead of values; if it has duplicates, add the [Subsets II](90-subsets-ii.md) skip rule. |
| "Relation to [Subsets](78-subsets.md)?" | Subsets is the union of `combine(n, k)` over all k — same tree, but every node is recorded instead of only depth-k leaves. |

**Traps:**

- **Getting the `+ 2` wrong.** `range` is exclusive, so the bound is `n - (k - len(path)) + 2`. Writing `+ 1` silently drops the last valid number — the highest-risk line in the problem. **Verify against a case you can count by hand** (`n=4, k=2` → 6).
- **Recursing with `i` instead of `i + 1`** — allows reuse, producing `[1,1]`.
- **Using `start` as the loop variable in the recursive call** (`backtrack(start + 1)`) — subtly wrong; it must be `i + 1`.
- **Starting at `backtrack(0)`** — 0 isn't in the range `[1, n]`.
- **Appending `path` instead of `path[:]`** — every result aliases the same list.
- **Reaching for the 2ⁿ bitmask approach** — correct, but catastrophically slow when k is near n.
- **Adding a `used` array out of habit** — pure overhead; `start` already prevents reuse.

**This same move shows up in:** [Combination Sum III](216-combination-sum-iii.md) (this plus a sum condition) · [Subsets](78-subsets.md) (the same tree, recording every node) · [Combination Sum](39-combination-sum.md) (reuse allowed, `i` instead of `i + 1`) · [Permutations](46-permutations.md) (the contrast — `used` instead of `start`) · [backtracking](../algorithms/backtracking.md).

</details>

---
