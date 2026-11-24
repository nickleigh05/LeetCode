# 877. Stone Game

**Medium** · [LeetCode](https://leetcode.com/problems/stone-game/) · [Solution file (no hints)](../../problems/0500-0999/877.py)

[📖 14. 2-D Dynamic Programming lesson](../learning/15-dp-2d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 14. 2-D Dynamic Programming problems](../rmap-practice/14-dp-2d.md)

---

Alice and Bob play with a row of piles, `piles[i]` stones each. The total is **odd** and the number of piles is **even**. Players alternate, Alice first. On a turn a player takes **the whole pile from either end**. The player with more stones at the end wins. Both play optimally. Return `True` if Alice wins.

```
piles = [5, 3, 4, 5]   →  True      (Alice takes the first 5, then plays so Bob can't catch up)
piles = [3, 7, 2, 3]   →  True
```

**Constraints:** `2 <= piles.length <= 500` · `piles.length` is even · `1 <= piles[i] <= 500` · `sum(piles)` is odd

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "take from either end" | The remaining piles are always a **contiguous interval** `[i..j]` |
| "both play optimally" | **Minimax**: track the best *difference* the player to move can force |
| total is odd | **No ties**: someone always has more |
| even number of piles | A hint at a mathematical shortcut (see below) |
| `n <= 500` | `O(n²)` is fine (250,000 states) |

**The interval DP.** Let `dp[i][j]` = the best `(mover's stones − opponent's stones)` the player to move can get from piles `i..j`.

- Take the left pile: gain `piles[i]`, then the opponent moves on `[i+1..j]` with advantage `dp[i+1][j]`, so my net is `piles[i] − dp[i+1][j]`.
- Take the right pile: `piles[j] − dp[i][j−1]`.
- `dp[i][j] = max` of the two, and `dp[i][i] = piles[i]`.

Alice wins when `dp[0][n−1] > 0`.

**The shortcut to know about.** With an even number of piles, Alice can always take all the even-indexed piles or all the odd-indexed ones. One of those sets is bigger (the total is odd), and she can force it. So the answer is **always `True`**. Interviewers like candidates who find the DP *and* mention this.

🤔 **Before you open the next section:** in `dp[i][j]`, which cells does it depend on, and so in what order must you fill the table?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Time | Space | Verdict |
|---|---|---|---|
| `return True` | O(1) | O(1) | ✅ Correct (the parity argument), but it hides the technique. Mention it *after* the DP |
| Recursion over every move sequence | O(2ⁿ) | O(n) | ❌ |
| **Interval [DP](../algorithms/dynamic-programming.md) on score difference** | **O(n²)** | O(n²) | ✅ The reusable technique |

**The decision: an interval DP.** It's the 2-D cousin of [Stone Game III](1406-stone-game-iii.md). There the state was one index. Here, taking from either end means the state is a **range** `[i..j]`, so two indices. This is the [minimax](../algorithms/minimax.md) pattern on a table.

Fill by **increasing interval length**: a length-`L` interval depends only on length `L−1` intervals.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
n = len(piles)
dp = [[0] * n for _ in range(n)]
for i in range(n):
    dp[i][i] = piles[i]
```

`dp[i][j]` is the mover's best advantage on piles `i..j`. With one pile left, the mover simply takes it.
→ [nested-lists](../syntax/nested-lists.md) · [list-comprehension](../syntax/list-comprehension.md) · [dynamic-programming](../algorithms/dynamic-programming.md)

```python
for length in range(2, n + 1):
    for i in range(n - length + 1):
        j = i + length - 1
        dp[i][j] = max(piles[i] - dp[i + 1][j], piles[j] - dp[i][j - 1])
```

Grow the interval length from 2 up to `n`. For each `[i..j]`, the mover picks the better of: take the left pile (then the opponent is the mover on `[i+1..j]`) or take the right pile (opponent moves on `[i..j-1]`). Subtracting the opponent's advantage is the minimax step.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md) · [min-max-key](../syntax/min-max-key.md)

```python
return dp[0][n - 1] > 0
```

If the first mover (Alice) can get a positive advantage over the whole row, she wins.
→ [comparison-operators](../syntax/comparison-operators.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def stoneGame(self, piles: List[int]) -> bool:
        n = len(piles)
        dp = [[0] * n for _ in range(n)]

        for i in range(n):
            dp[i][i] = piles[i]

        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                dp[i][j] = max(piles[i] - dp[i + 1][j], piles[j] - dp[i][j - 1])

        return dp[0][n - 1] > 0
```

</details>

**Trace it.** `piles = [5, 3, 4, 5]`:

| Interval | Options | `dp` |
|---|---|---|
| `[5]`, `[3]`, `[4]`, `[5]` | take it | 5, 3, 4, 5 |
| `[5,3]` | `5−3 = 2`, `3−5 = −2` | **2** |
| `[3,4]` | `3−4`, `4−3` | **1** |
| `[4,5]` | `4−5`, `5−4` | **1** |
| `[5,3,4]` | left `5 − dp[3,4]=1` → 4; right `4 − dp[5,3]=2` → 2 | **4** |
| `[3,4,5]` | left `3 − 1 = 2`; right `5 − 1 = 4` | **4** |
| `[5,3,4,5]` | left `5 − dp[3,4,5]=4` → 1; right `5 − dp[5,3,4]=4` → 1 | **1** |

`1 > 0` → **`True`** ✅.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n²)</summary>

**O(n²):** about `n²/2` intervals, each computed in O(1).

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n²), reducible to O(n)</summary>

**O(n²)** for the table. Since a length-`L` row depends only on length `L−1`, a one-dimensional rolling array suffices: **O(n)**.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Each state is a contiguous range of piles, since players only take from the ends. I define `dp[i][j]` as the best score difference the mover can get on that range. Taking the left pile gives `piles[i]` minus whatever advantage the opponent then has on `[i+1..j]`, and similarly for the right. I fill by interval length and Alice wins if `dp[0][n−1]` is positive. That's O(n²). Actually, with an even number of piles she can always grab all the odd-indexed or all the even-indexed piles, and one of those sets wins, so the true answer is always True. But the DP is the technique that generalises."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why is it always `True`?" | Alice can choose to take all even-position or all odd-position piles by always leaving Bob a pile of the other parity. One set has the larger sum (total is odd) |
| "What if the number of piles were odd?" | The parity argument fails and the DP is required |
| "Space?" | Roll the table by interval length, or index by `(i, length)` with a single row |
| "Related?" | [Stone Game III](1406-stone-game-iii.md) (1-D, take from the front) · [Stone Game II](1140-stone-game-ii.md) · [Predict the Winner](../algorithms/minimax.md) (identical DP without the guarantees) |
| "Memoised recursion?" | `f(i, j) = max(piles[i] − f(i+1, j), piles[j] − f(i, j−1))`, with `lru_cache` |

**Traps:**

- **Adding instead of subtracting** the opponent's `dp`.
- **Filling in the wrong order.** `dp[i][j]` needs shorter intervals, so loop by length.
- **Returning `dp[0][n-1] >= 0`.** Ties are impossible here, but `> 0` is the correct condition in general.
- **Assuming greedy works** ("always take the bigger end"). It fails.

**This same move shows up in:** [Stone Game III](1406-stone-game-iii.md) · [Stone Game II](1140-stone-game-ii.md) · [Burst Balloons](312-burst-balloons.md) (another interval DP).

</details>

---
