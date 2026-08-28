# 216. Combination Sum III

**Medium** · [LeetCode](https://leetcode.com/problems/combination-sum-iii/) · [Solution file (no hints)](../../problems/0001-0499/216.py)

[📖 10. Backtracking lesson](../learning/10-backtracking.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 10. Backtracking problems](../rmap-practice/10-backtracking.md)

---

Find all valid combinations of **`k` numbers** summing to **`n`**, where only the digits **1–9** may be used and **each at most once**. No duplicate combinations; any order.

```
k = 3, n = 7  →  [[1,2,4]]
k = 3, n = 9  →  [[1,2,6], [1,3,5], [2,3,4]]
k = 4, n = 1  →  []            (smallest 4-digit sum is 1+2+3+4 = 10)
```

**Constraints:** `2 <= k <= 9` · `1 <= n <= 60`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**combinations**" | Order does **not** matter → the `start` index is back (unlike [Permutations](46-permutations.md)) |
| "**numbers 1 through 9**" | ⚠️ The candidate pool is **hard-coded**, not an input. There is no `candidates` array |
| "each number **at most once**" | Recurse with `i + 1`, not `i` — like [Combination Sum II](40-combination-sum-ii.md), unlike [Combination Sum](39-combination-sum.md) |
| "must not contain the same combination twice" | Free here — the pool `1..9` has **no duplicates**, so no skip-rule is needed |
| "**k numbers**" that sum to `n` | ⚠️ **Two** conditions to satisfy at once, not one |
| `k <= 9`, `n <= 60` | The whole search space is 2⁹ = 512 subsets. Trivially small |

**Two constraints, one base case.** This is the wrinkle that separates 216 from every earlier Combination Sum. In [Combination Sum](39-combination-sum.md) the only question was "does the remaining target hit zero?" Here a combination is valid only if **both** are true at the same moment:

```
len(path) == k        ← exactly k numbers
remaining == 0        ← they sum to n
```

Hitting one without the other is a **dead end, not an answer**:

```
k = 3, n = 9

[1,2,3]  → 3 numbers ✓  but sums to 6, not 9   ✗
[4,5]    → sums to 9 ✓  but only 2 numbers     ✗
[1,3,5]  → 3 numbers ✓  and sums to 9 ✓        ✅
```

So the base case checks **length** to decide when the path is finished, and **sum** to decide whether the finished path counts.

**Why the pool being fixed matters.** Every previous problem in this family took a `candidates` list. Here the candidates are the literal digits `1..9`, which means:

- the loop is `range(start, 10)`, not `range(start, len(candidates))`
- the values are already **sorted and distinct**, so the `sort()` call and the duplicate-skip line from [Combination Sum II](40-combination-sum-ii.md) both disappear
- the depth is capped at 9, and so is the branching — the search cannot blow up

🤔 **Before you open the next section:** the base case has two conditions. Which one tells you to *stop recursing*, and which one only tells you whether to *record*? They are not the same job.

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| `itertools.combinations` | Generate all C(9,k), filter by sum | O(C(9,k)·k) | ⚠️ Correct and tiny; sidesteps the exercise |
| Enumerate all 512 bitmasks | Check popcount == k and sum == n | O(2⁹·9) | ✅ Fine at this size, but doesn't generalise |
| **Backtracking with `start` + `remaining`** | Choose ascending digits, prune on sum | **O(C(9,k)·k)** | ✅ |
| DP / subset-sum table | Count-based | O(9·k·n) | ❌ Counts well, but reconstructing all combinations is clumsy |

**The decision: backtracking over `1..9` with a `start` index and a running `remaining`.**

This is the [Combination Sum II](40-combination-sum-ii.md) skeleton with three edits. Seeing them as *edits* rather than new material is the point of the problem:

| | [Combination Sum II](40-combination-sum-ii.md) | **Combination Sum III** |
|---|---|---|
| Candidate pool | input array, may repeat | **fixed `1..9`, all distinct** |
| Pre-sort | required (`candidates.sort()`) | **unnecessary — already sorted** |
| Duplicate skip | `if i > start and c[i] == c[i-1]: continue` | **unnecessary — no duplicates exist** |
| Recurse with | `i + 1` (no reuse) | **`i + 1`** — same |
| Base case | `remaining == 0` | **`len(path) == k`, then check `remaining == 0`** |

**Why the base case flips to length.** If you keep `remaining == 0` as the *stopping* test, you accept `[4,5]` for `k=3` — right sum, wrong count. Length is what bounds the recursion depth, so length is what stops it; the sum is then a filter applied at the leaf.

You could write it with the tests in either order, but **stop on length** is the version that generalises: it is the same "the path is full" base case used in [Permutations](46-permutations.md) and [Combinations](77-combinations.md).

**The pruning that makes it fast.** Because the digits are ascending, the moment `num > remaining` every *later* digit also overshoots:

```python
if num > remaining:
    break          # not continue — everything after this is worse
```

`break` rather than `continue` is the same monotonic-cutoff reasoning as [Combination Sum](39-combination-sum.md), and it works for the same reason: **the candidates are sorted**, so one failure predicts all the rest.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
res = []
path = []
```

`path` is the combination under construction; `res` collects the finished ones.

No `candidates.sort()` here — the pool is the literal `1..9`, already in order.
→ [list-basics](../syntax/list-basics.md)

```python
def backtrack(start, remaining):
    if len(path) == k:
        if remaining == 0:
            res.append(path[:])
        return
```

**The two-part base case.** Read it as two separate jobs:

- `len(path) == k` — the path is **full**, so stop recursing no matter what. This is the depth bound.
- `remaining == 0` — the full path **is also valid**, so record it. This is the filter.

The `return` sits *outside* the inner `if`, so a full-but-wrong path (like `[1,2,3]` for `n=9`) is abandoned rather than extended.

`path[:]` copies, for the usual reason: `path` is a single list that keeps mutating.
→ [recursion-basics](../syntax/recursion-basics.md) · [list-slicing](../syntax/list-slicing.md) · [if-return](../syntax/if-return.md)

```python
    for num in range(start, 10):
```

**Candidates are the digits `start..9`.** `range(start, 10)` — the `10` is exclusive, so this ends at 9.

Starting at `start` rather than 1 is what enforces ascending order and therefore *combinations, not permutations*: `[1,2,6]` is generated, `[2,1,6]` never is.
→ [range-function](../syntax/range-function.md) · [for-loop](../syntax/for-loop.md)

```python
        if num > remaining:
            break
```

**The prune.** Since `num` only increases, once it overshoots the remaining target, so does every later digit — nothing after this point can work, so abandon the whole rest of the loop.

⚠️ **`break`, not `continue`.** `continue` would still be *correct*, just slower — it would test 8, then 9, and reject both. `break` is available only because the candidates are sorted ascending, which here they are by construction.
→ [break-continue](../syntax/break-continue.md)

```python
        path.append(num)
        backtrack(num + 1, remaining - num)
        path.pop()
```

**Choose, explore, un-choose.**

`num + 1` is the no-reuse rule: the next level starts *after* the digit just taken, so each digit is used at most once. (Compare [Combination Sum](39-combination-sum.md), which passes `i` to allow reuse.)

`remaining - num` carries the shrinking target down instead of re-summing the path each time.
→ [list-methods](../syntax/list-methods.md)

```python
backtrack(1, n)
return res
```

**Start at digit 1** with the full target `n`.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def combinationSum3(self, k: int, n: int) -> List[List[int]]:

        res = []
        path = []

        def backtrack(start, remaining):
            if len(path) == k:
                if remaining == 0:
                    res.append(path[:])
                return

            for num in range(start, 10):
                if num > remaining:
                    break
                path.append(num)
                backtrack(num + 1, remaining - num)
                path.pop()

        backtrack(1, n)
        return res
```

</details>

**Trace it** — `k = 3, n = 9`, the whole `start = 1` subtree (this is verified output, not a sketch):

| Depth | Action | `path` | `remaining` | Result |
|---|---|---|---|---|
| 0 | choose 1 | `[1]` | 8 | |
| 1 | choose 2 | `[1,2]` | 6 | |
| 2 | choose 3 | `[1,2,3]` | 3 | |
| 3 | base — full, sum ≠ n | | 3 | **discard** ✗ |
| 2 | choose 4 | `[1,2,4]` | 2 | → discard |
| 2 | choose 5 | `[1,2,5]` | 1 | → discard |
| 2 | choose 6 | `[1,2,6]` | 0 | → **record `[1,2,6]`** ✅ |
| 2 | 7 > remaining 6 | | | **break** |
| 1 | choose 3 | `[1,3]` | 5 | |
| 2 | choose 4 | `[1,3,4]` | 1 | → discard |
| 2 | choose 5 | `[1,3,5]` | 0 | → **record `[1,3,5]`** ✅ |
| 2 | 6 > remaining 5 | | | **break** |
| 1 | choose 4 | `[1,4]` | 4 | 5 > 4 → **break** immediately |
| 1 | choose 5 | `[1,5]` | 3 | 6 > 3 → **break** |
| 1 | choose 6…8 | | | all break at depth 2 |

Then `start = 2` finds `[2,3,4]`, and `start = 3` onwards finds nothing. Final: **`[[1,2,6], [1,3,5], [2,3,4]]`** ✅

Look at the rows where `path` has length 2 and `remaining` is small — `[1,4]` with 4 left, `[1,5]` with 3 left. The loop breaks on its **first** iteration every time, because the smallest available digit already exceeds what's left. That single `break` line is why the search barely explores anything.

**Watch the discard rows.** `[1,2,3]` reaches the base case and is thrown away. That's the two-condition base case doing its job: full length is what *stopped* it, and the sum test is what *rejected* it.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(C(9,k) · k), bounded by a constant</summary>

**O(C(9,k) · k)** — and since the pool is fixed at 9 digits, this is **O(1) in the input**.

- **C(9,k) combinations** to consider — the number of ways to pick k of the 9 digits.
- **O(k)** to copy each recorded path.

The worst case is k = 4 or 5, where C(9,k) = 126:

| k | C(9,k) |
|---|---|
| 2 | 36 |
| 3 | 84 |
| **4** | **126** |
| **5** | **126** |
| 6 | 84 |
| 9 | 1 |

Summed over all k, the entire space is **2⁹ = 512 subsets**. The algorithm can never do meaningful work — this is a **constant-time problem** in the formal sense, and saying so out loud is the right answer.

**The honest framing for an interview:** *"Technically O(1), because the candidate pool is fixed at nine digits. If you generalise the pool to size m, it's O(C(m,k)·k)."* Give the general form — that's what the question is really probing.

**The `break` prune** doesn't improve the asymptotic bound (the bound is already constant) but it cuts real work substantially — in the `k=3, n=9` trace above, most branches die on the loop's first iteration.

**Why not 9! or 9^k.** Both are wrong, and both are common answers:

- **9^k** would be right if digits could repeat and order mattered.
- **9!** would be right if this were a permutation problem.

The `start` index collapses all orderings of the same digit set into **one** path, which is exactly what turns 9^k into C(9,k).

</details>

<details>
<summary><b>5 · Space complexity</b> — O(k) auxiliary</summary>

**O(k) auxiliary**, plus the output.

| Component | Size |
|---|---|
| `res` (required output) | up to C(9,k) combinations × k → **O(C(9,k)·k)** |
| **Recursion depth** | at most k frames — one per digit chosen → **O(k)** |
| `path` | at most k → O(k) |

Since `k <= 9`, every one of these is bounded by a constant. **O(1) auxiliary, formally** — but the useful answer names the shape: *"O(k) for the recursion stack and path, where k ≤ 9."*

**No `used` array needed.** [Permutations](46-permutations.md) required O(n) of extra bookkeeping to prevent element reuse; here the `start` index does that job for free, because "already used" and "index below `start`" mean the same thing. That's the recurring trade in Unit 10:

| Mechanism | Costs | Gives you |
|---|---|---|
| `start` index | **O(1)** — one integer | combinations (order suppressed) |
| `used` array | **O(n)** — one flag per element | permutations (all orderings) |

**The recursion is k deep, not C(9,k) deep** — the usual point. C(9,k) counts root-to-leaf paths; only one path is on the stack at a time.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "This is the Combination Sum skeleton with a fixed candidate pool of the digits one through nine. Because the pool has no duplicates and is already sorted, I drop both the sort and the duplicate-skip line from Combination Sum II — but I keep recursing with `i + 1`, since each digit can be used at most once. The real difference is the base case: there are two conditions, `k` numbers *and* the right sum, so I stop when the path is full and only record it if the remaining target is zero. Stopping on length rather than sum is what rejects things like `[4,5]`, which sums correctly but is too short. Since the digits ascend, I `break` rather than `continue` once a digit exceeds what's left. It's C(9,k) work in the worst case, which is bounded by 2⁹, so formally constant time; O(k) stack depth."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why stop on **length** and not on sum?" | **The question.** Length bounds the depth; sum is a filter at the leaf. Stopping on sum accepts `[4,5]` for k=3 — right sum, too few numbers. |
| "Why no duplicate-skip line, when [Combination Sum II](40-combination-sum-ii.md) needs one?" | The pool `1..9` has no repeated values, so the situation that line guards against cannot arise. |
| "`break` or `continue` on the overshoot?" | `break` — the digits ascend, so one overshoot means all later ones do. `continue` is correct but wastes iterations. |
| "Add a **second** prune?" | Yes: if fewer than `k - len(path)` digits remain above `num`, bail. Same idea as the [Combinations](77-combinations.md) upper bound. Small gain here given the tiny pool. |
| "What's the tightest bound on the answer count?" | The smallest k-digit sum is `k(k+1)/2` and the largest is `k(19-k)/2`. If `n` falls outside that window the answer is empty — a nice O(1) early exit. |
| "Do it **without recursion**?" | Iterate all 512 bitmasks over `1..9`, keep those with popcount `k` and sum `n`. Genuinely competitive at this size. |
| "What if digits could **repeat**?" | Recurse with `num` instead of `num + 1` — that's [Combination Sum](39-combination-sum.md). |
| "Count them instead of listing them?" | DP over (digits used, count, sum) — O(9·k·n) with no enumeration. |

**Traps:**

- **Using `remaining == 0` as the stopping condition.** Accepts short paths like `[4,5]`. The defining bug of this problem.
- **Putting the `return` inside the `if remaining == 0`** — a full-but-wrong path would keep recursing (and then run off the end of the digit range).
- **Recursing with `num` instead of `num + 1`** — allows reuse, so `[3,3,3]` shows up for `n=9`.
- **Looping `range(start, 9)`** — off-by-one; `range` is exclusive, so this silently drops the digit 9.
- **Starting at `backtrack(0, n)`** — 0 is not in the pool, and it lets a useless zero into paths.
- **Appending `path` instead of `path[:]`** — every result aliases the same list.
- **Carrying a `sum(path)` recomputation** instead of a `remaining` parameter — correct but O(k) per node for no reason.

**This same move shows up in:** [Combination Sum](39-combination-sum.md) (the skeleton, with reuse allowed) · [Combination Sum II](40-combination-sum-ii.md) (no reuse, plus duplicate handling) · [Combinations](77-combinations.md) (the same fixed-length base case, with no sum condition) · [Subsets](78-subsets.md) (where every node is recorded rather than only full-length ones) · [backtracking](../algorithms/backtracking.md).

</details>

---
