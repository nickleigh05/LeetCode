# 312. Burst Balloons

**Hard** · [LeetCode](https://leetcode.com/problems/burst-balloons/)

[📖 15. 2-D Dynamic Programming lesson](../learning/15-dp-2d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 15. 2-D Dynamic Programming problems](../rmap-practice/15-dp-2d.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

You have `n` balloons in a row, the i-th painted with the number `nums[i]`. Burst them **all**. Bursting balloon `i` earns `nums[i-1] * nums[i] * nums[i+1]` coins, using its **current** neighbours — and after it bursts, its neighbours become adjacent. If a neighbour is out of bounds, treat it as a balloon painted **1**. Return the **maximum coins** you can collect.

```
nums = [3,1,5,8]   →  167
        burst 1:  3*1*5  = 15    → [3,5,8]
        burst 5:  3*5*8  = 120   → [3,8]
        burst 3:  1*3*8  = 24    → [8]
        burst 8:  1*8*1  = 8     → []
                                   15 + 120 + 24 + 8 = 167

nums = [1,5]       →  10
        burst 1:  1*1*5 = 5      → [5]
        burst 5:  1*5*1 = 5      → []      5 + 5 = 10
```

**Constraints:** `n == nums.length` · `1 <= n <= 300` · `0 <= nums[i] <= 100`.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**maximum** coins" | Optimization → `max` |
| "burst them **all**" | Every balloon is popped. You're choosing an **order**, not a subset — n! orderings |
| "using its **current** neighbours" | The killer. The reward for a balloon **depends on what's already been burst**. Bursting one balloon changes the value of every future burst |
| out of bounds counts as **1** | A hint about padding — 1 is the multiplicative identity, so a virtual balloon at each end changes nothing |
| `n <= 300` | n! is beyond hopeless. n³ = 2.7 × 10⁷ — which is a strong signal, since n³ is an unusual target and points at interval DP |

The thing that makes this Hard is in row 3. Every DP so far in this unit has had **independent subproblems**: in [Edit Distance](72-edit-distance.md), what you do to the left of a position doesn't change what the right half costs. Here, bursting a balloon in the middle **joins its two neighbours**, so the left and right halves stop being independent.

Try the obvious framing and watch it fail. "Which balloon do I burst **first**?" Say you burst `i` first. Now the problem splits into the balloons left of `i` and the balloons right of `i` — except it doesn't, because those two groups are now **adjacent to each other**. A later burst on the left can score using a balloon from the right. **The subproblems are entangled, so there's no recurrence.**

Now reverse the question — and this single inversion is the entire problem:

> **Which balloon do I burst *last*?**

Suppose within some range, balloon `i` is the last one standing. Then at the moment it bursts, **everything else in the range is already gone**, so its neighbours are whatever sits immediately *outside* the range — and those are fixed, known values.

More importantly: every balloon left of `i` was burst while `i` was still there, and every balloon right of `i` likewise. **So no burst on the left ever saw a balloon from the right, and vice versa.** `i` acted as a permanent wall between them.

**The two sides are genuinely independent**, and now there *is* a recurrence:

```
coins(left, right) = max over i strictly between them of
                        nums[left] * nums[i] * nums[right]     ← i burst last
                      + coins(left, i) + coins(i, right)       ← the two independent halves
```

where `left` and `right` are the **surviving boundary balloons**, not part of the range being burst.

🤔 **Before you open the next section:** why does the "burst first" framing fail while "burst last" works? Say precisely what each one guarantees about the two halves — the difference is one word.

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Try every order | Permute all n! burst sequences | **O(n!)** | O(n) | ❌ 300! is beyond astronomical |
| Greedy — burst the smallest first | Pop low-value balloons to preserve big products | O(n log n) | O(1) | ❌ **Wrong.** `[3,1,5,8]` — greedy pops the 1 first, which is correct here by luck, but no local rule survives in general |
| Greedy — burst the largest first | Cash in the big products early | O(n log n) | O(1) | ❌ Also wrong. Bursting 8 first forfeits the 3×5×8 = 120 later |
| DP on "which burst **first**" | Split at the first burst | — | — | ❌ **No valid recurrence.** The two halves become adjacent and can interact |
| **DP on "which burst *last*"** | Split at the last burst; the halves stay separated | **O(n³)** | O(n²) | ✅ |

**The decision:** **interval DP over `(left, right)` boundaries, choosing which balloon bursts last.**

**The first-vs-last distinction, stated precisely** — this is the answer to section 1's question, and the one thing to be able to articulate:

- **"Burst `i` first"** guarantees only that `i` is gone before everything else. Afterwards the left and right groups are adjacent, and later bursts can pair a left balloon with a right one. **The halves are not independent.**
- **"Burst `i` last"** guarantees that `i` is still standing during *every* other burst in the range. It's a wall. No burst on the left can ever see past it, and no burst on the right can either. **The halves are independent** — which is exactly the *optimal substructure* a DP requires.

One word: **first** separates the halves *after* the split; **last** separates them *during* it. The second is what a recurrence needs.

**Why the state is `(left, right)` boundaries rather than a subarray.** The two indices are the balloons that **survive** on either side — they're never burst within this subproblem, they only supply the multipliers. That framing is what makes `nums[left] * nums[i] * nums[right]` correct at the moment `i` bursts: with everything strictly between them gone, `left` and `right` really are `i`'s neighbours.

**Why pad with 1s.** The real balloons at the ends have no outside neighbour, and the problem says to treat that as 1. Adding a literal 1 at each end means **every** balloon has real neighbours, so no boundary special-casing is needed anywhere. It works precisely because 1 is the multiplicative identity — the padding contributes nothing to any product. Same trick as a dummy head node in [Remove Nth Node From End of List](19-remove-nth-node-from-end-of-list.md): **add a fake element so the general case covers the edge case.**

**Why this is called interval DP.** The state is a *range*, and it's solved by trying every split point within it. Same family as matrix-chain multiplication and optimal BST construction — and the O(n³) bound is its signature: **O(n²) intervals × O(n) split points.**

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
balloons = [1] + nums + [1]
n = len(balloons)
memo = {}
```
**The padding**, and it's the line that removes every edge case. A virtual balloon painted **1** at each end means every real balloon has genuine neighbours to multiply with, and since 1 is the multiplicative identity, the padding never distorts a score.

`memo` caches by `(left, right)` — the interval's boundaries.
→ [list-basics](../syntax/list-basics.md) · [dict-basics](../syntax/dict-basics.md) · [hashmap](../data-structures/hashmap.md)

```python
def dp(left, right):
    if left + 1 == right:
        return 0
```
`dp(left, right)` = the maximum coins obtainable by bursting **everything strictly between** `left` and `right`, with those two balloons still standing.

**The base case:** `left + 1 == right` means the two boundaries are adjacent, so there's nothing between them to burst → **0 coins**. Note it's an *empty range*, not a single balloon — the exclusive-boundary convention is what makes this clean.
→ [function-basics](../syntax/function-basics.md) · [comparison-operators](../syntax/comparison-operators.md) · [recursion-basics](../syntax/recursion-basics.md)

```python
    if (left, right) in memo:
        return memo[(left, right)]
```
The cache check. The value depends only on the interval — never on how the surrounding balloons were burst — which is what makes memoization valid and turns O(n!) into O(n³).
→ [membership-operators](../syntax/membership-operators.md) · [tuple-basics](../syntax/tuple-basics.md)

```python
    best = 0
```
The running maximum. Starting at 0 is safe because all values are non-negative, so no arrangement can score less than nothing.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
    for i in range(left + 1, right):   # try every balloon as the last one burst
```
**Try every interior balloon as the one burst *last*.** The range excludes both boundaries, since they're not part of this subproblem.

There's no way to know which choice is best, so all are tried — and each choice cleanly partitions the rest. This loop is the O(n) factor in the O(n³).
→ [range-function](../syntax/range-function.md) · [for-loop](../syntax/for-loop.md)

```python
        coins = balloons[left] * balloons[i] * balloons[right]
```
**The score for bursting `i` last.** Because everything strictly between `left` and `right` is already gone by then, `i`'s neighbours at that moment are exactly `balloons[left]` and `balloons[right]`.

This is the payoff of the whole "last" framing: the multipliers are **known and fixed**, not dependent on the burst order within the halves. Under a "first" framing you couldn't write this line at all.
→ [arithmetic-operators](../syntax/arithmetic-operators.md) · [list-basics](../syntax/list-basics.md)

```python
        coins += dp(left, i) + dp(i, right)
```
**The two independent halves.** Everything strictly between `left` and `i`, and everything strictly between `i` and `right`.

Both subproblems use `i` as one of *their* boundaries — which is precisely correct, because `i` is still standing while they're being burst. It's the wall, and it supplies the multiplier for the outermost bursts on each side.

The two calls **add**, not `max`, because both halves must be fully cleared — you're not choosing between them.
→ [recursion-basics](../syntax/recursion-basics.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
        best = max(best, coins)
```
Keep the best split point found for this interval.
→ [min-max-key](../syntax/min-max-key.md)

```python
    memo[(left, right)] = best
    return best
```
Cache and return.
→ [dict-basics](../syntax/dict-basics.md) · [dynamic-programming](../algorithms/dynamic-programming.md)

```python
return dp(0, n - 1)
```
The full problem: burst everything strictly between the two padding balloons — that is, every real balloon.
→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def maxCoins(self, nums: List[int]) -> int:

        balloons = [1] + nums + [1]
        n = len(balloons)
        memo = {}

        def dp(left, right):
            if left + 1 == right:
                return 0
            if (left, right) in memo:
                return memo[(left, right)]

            best = 0
            for i in range(left + 1, right):   # try every balloon as the last one burst
                coins = balloons[left] * balloons[i] * balloons[right]
                coins += dp(left, i) + dp(i, right)
                best = max(best, coins)

            memo[(left, right)] = best
            return best

        return dp(0, n - 1)
```
</details>

**Trace it** — `nums = [3, 1, 5, 8]`, so `balloons = [1, 3, 1, 5, 8, 1]` with indices 0–5.

Working from the smallest intervals outward. Each entry is `dp(left, right)` — the best coins from bursting everything strictly between:

**Width-2 intervals** (one balloon inside):

| interval | inner balloon | score | `dp` |
|---|---|---|---|
| `dp(0,2)` | `balloons[1]=3` | 1×3×1 = 3 | **3** |
| `dp(1,3)` | `balloons[2]=1` | 3×1×5 = 15 | **15** |
| `dp(2,4)` | `balloons[3]=5` | 1×5×8 = 40 | **40** |
| `dp(3,5)` | `balloons[4]=8` | 5×8×1 = 40 | **40** |

**Width-3 intervals** (two balloons inside — try each as last):

| interval | last = first inner | last = second inner | `dp` |
|---|---|---|---|
| `dp(0,3)` | i=1: 1×3×5 + 0 + `dp(1,3)`=15 → **20** | i=2: 1×1×5 + `dp(0,2)`=3 + 0 → 8 | **20** |
| `dp(1,4)` | i=2: 3×1×8 + 0 + `dp(2,4)`=40 → **64** | i=3: 3×5×8 + `dp(1,3)`=15 + 0 → **135** | **135** |
| `dp(2,5)` | i=3: 1×5×1 + 0 + `dp(3,5)`=40 → 45 | i=4: 1×8×1 + `dp(2,4)`=40 + 0 → **48** | **48** |

**Width-4 intervals**, each trying three split points:

| interval | choices for the last burst | `dp` |
|---|---|---|
| `dp(0,4)` | i=1: 1×3×8 + 0 + `dp(1,4)`=135 → **159**<br>i=2: 1×1×8 + `dp(0,2)`=3 + `dp(2,4)`=40 → 51<br>i=3: 1×5×8 + `dp(0,3)`=20 + 0 → 60 | **159** |
| `dp(1,5)` | i=2: 3×1×1 + 0 + `dp(2,5)`=48 → 51<br>i=3: 3×5×1 + `dp(1,3)`=15 + `dp(3,5)`=40 → 70<br>i=4: 3×8×1 + `dp(1,4)`=135 + 0 → **159** | **159** |

**The full interval** `dp(0,5)` — four choices for the last balloon burst:

| last burst | score for it | left half | right half | total |
|---|---|---|---|---|
| i=1 (`3`) | 1×3×1 = 3 | `dp(0,1)` = 0 | `dp(1,5)` = 159 | 162 |
| i=2 (`1`) | 1×1×1 = 1 | `dp(0,2)` = 3 | `dp(2,5)` = 48 | 52 |
| i=3 (`5`) | 1×5×1 = 5 | `dp(0,3)` = 20 | `dp(3,5)` = 40 | 65 |
| **i=4 (`8`)** | 1×8×1 = 8 | `dp(0,4)` = 159 | `dp(4,5)` = 0 | **167** |

Return **167** ✅

The winning line is worth reading backwards, because it explains the example in the problem statement: **`8` bursts last** (scoring 1×8×1 = 8), and before that, within `dp(0,4)`, **`3` bursts last** (scoring 1×3×8 = 24), and before that `dp(1,4)` has **`5`** bursting last (3×5×8 = 120), preceded by `1` (3×1×5 = 15). Reversing gives the burst order **1, 5, 3, 8** — exactly the sequence in the statement, with 15 + 120 + 24 + 8 = 167.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n³)</summary>

**O(n³).**

Using **states × work per state**:

- **States:** `(left, right)` pairs with `left < right` → **O(n²)** intervals.
- **Work per state:** the loop tries every interior balloon as the last burst → up to **O(n)** iterations, each doing O(1) arithmetic plus two cached lookups.
- O(n²) × O(n) = **O(n³)**.

At the limit, 300³ = **2.7 × 10⁷** operations. That's why the constraint is 300 rather than 1000 — the cubic bound is exactly what the input size was chosen for. **An unusual constraint like 300 is itself a hint: it points at O(n³).**

**Against the alternatives:** trying every burst order is **O(n!)**. At n = 300 that number has over 600 digits. The DP works because all those orderings pass through only O(n²) distinct intervals — the most dramatic collapse in this unit.

**Faster?** No better bound is known. Interval DP problems in this family — matrix-chain multiplication, optimal BST — are generally Θ(n³), though some admit Knuth's optimization down to O(n²) when the cost function satisfies a quadrangle inequality. That doesn't apply here, so **O(n³) is the answer**.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n²)</summary>

**O(n²)**, from two sources:

- The **memo** holds one entry per `(left, right)` interval → **O(n²)**, up to ~45,000 entries at n = 300.
- The **recursion stack** nests once per level of interval nesting → **O(n)**.

The memo dominates.

| Version | Space | Notes |
|---|---|---|
| Brute force over orderings | O(n) | Just the stack — but O(n!) time |
| **Memoized recursion** | **O(n²)** | One entry per interval; O(n) stack |
| Bottom-up interval DP | **O(n²)** | Same table, filled by increasing interval width, no recursion |

**Why this can't collapse to O(n)** like [Unique Paths](62-unique-paths.md) or [Longest Common Subsequence](1143-longest-common-subsequence.md): those had `dp[i][j]` depending only on the adjacent row, so a rolling row worked. Here `dp(left, right)` depends on `dp(left, i)` and `dp(i, right)` for **every** interior `i` — dependencies reach across the whole table, not to a neighbouring row. **Interval DP genuinely needs the full triangular table.**

**The bottom-up form**, if recursion depth is a concern (it shouldn't be — depth is O(n), not O(n²)):

```python
dp = [[0] * n for _ in range(n)]
for width in range(2, n):                    # interval width, smallest first
    for left in range(n - width):
        right = left + width
        for i in range(left + 1, right):
            dp[left][right] = max(dp[left][right],
                                  balloons[left] * balloons[i] * balloons[right]
                                  + dp[left][i] + dp[i][right])
return dp[0][n - 1]
```

**Iterating by increasing width is essential** — every subproblem an interval depends on is strictly narrower, so widths must be filled in ascending order. That ordering requirement is the signature of interval DP, and it's why the bottom-up version looks unlike the row-by-row sweeps elsewhere in this unit.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The hard part is that bursting a balloon changes its neighbours' rewards, so the subproblems aren't independent. If I ask 'which balloon do I burst first?', splitting at it doesn't help — the two halves become adjacent and later bursts can pair across the boundary. The fix is to invert the question and ask **which balloon bursts last**. If `i` is last in a range, then `i` was standing during every other burst in that range, so it acts as a wall: nothing on the left ever saw the right. The halves become genuinely independent, and I get a recurrence. And because everything between the boundaries is gone when `i` finally bursts, its neighbours are exactly the surviving boundary balloons — a fixed, known product. I pad the array with 1s so every balloon has real neighbours, which works because 1 is the multiplicative identity. That's interval DP: O(n²) intervals times O(n) split points, so O(n³) time and O(n²) space — and n ≤ 300 is exactly the constraint you'd pick for a cubic algorithm."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why 'last' rather than 'first'?" | "First" only guarantees `i` is gone before the others, so the halves become adjacent and can interact. "Last" guarantees `i` is *present* during every other burst in the range, so it separates the halves permanently. Independence is what a recurrence needs. |
| "Why pad with 1s?" | So every balloon has real neighbours and no boundary case exists. 1 is the multiplicative identity, so the padding contributes nothing to any product. |
| "What do `left` and `right` mean exactly?" | They're the balloons that **survive** — never burst in this subproblem, only supplying multipliers. The range burst is strictly between them. |
| "Why is greedy wrong?" | No local rule works. Bursting the largest first forfeits the big products it would have multiplied into later; bursting the smallest first has no guarantee either. The value of a burst depends on the entire remaining configuration. |
| "Write it bottom-up." | Fill by increasing interval width, since every dependency is a strictly narrower interval. Same O(n³)/O(n²), no recursion. |
| "Can you get below O(n³)?" | Not known. Some interval DPs admit Knuth's optimization to O(n²) under a quadrangle inequality, but this cost function doesn't satisfy it. |
| "What if balloons could be left unburst?" | Then it's a different problem — you'd add "burst nothing in this range" as an option, and since all values are non-negative, bursting everything is still at least as good. |
| "How does this relate to matrix-chain multiplication?" | Same family. There you choose the last multiplication to perform in a range; here the last balloon to burst. Both are O(n²) intervals × O(n) split points. |

**Traps:**
- **Framing it as "which to burst first."** The defining mistake — it yields no valid recurrence, and people often don't notice why their subproblems give wrong answers.
- **Including the boundaries in the burst range.** `range(left + 1, right)` is exclusive on both ends deliberately; `left` and `right` are survivors.
- **Using `max` instead of `+` for the two halves.** Both must be cleared entirely; you're not choosing between them.
- Forgetting the padding and then special-casing the ends — workable but far more error-prone.
- Base case as `left == right` instead of `left + 1 == right` — the empty range is when the boundaries are *adjacent*.
- Computing the score with `balloons[i-1]` and `balloons[i+1]` (the original neighbours) rather than `balloons[left]` and `balloons[right]`. The whole point is that the *boundaries* are the neighbours at burst time.

**This same move shows up in:** [Longest Increasing Path in a Matrix](329-longest-increasing-path-in-a-matrix.md) (memoizing a state whose value is independent of the path taken to it) · [Unique Binary Search Trees](https://leetcode.com/problems/unique-binary-search-trees/) (interval DP choosing a root, the same split-the-range structure) · [Palindrome Partitioning](131-palindrome-partitioning.md) (splitting a sequence at a chosen boundary) · [Merge k Sorted Lists](23-merge-k-sorted-lists.md) (divide-and-conquer where the split point determines the subproblems).

</details>

---
