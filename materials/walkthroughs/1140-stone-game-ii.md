# 1140. Stone Game II

**Medium** · [LeetCode](https://leetcode.com/problems/stone-game-ii/) · [Solution file (no hints)](../../problems/1000-1499/1140.py)

[📖 14. 2-D Dynamic Programming lesson](../learning/15-dp-2d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 14. 2-D Dynamic Programming problems](../rmap-practice/14-dp-2d.md)

---

Piles of stones lie in a row, `piles[i]` each. Alice goes first, then they alternate. Initially `M = 1`. On a turn, a player takes **all the stones from the first `X` remaining piles**, for any `1 <= X <= 2M`, and then sets `M = max(M, X)`. The game ends when no piles remain. Both play optimally to **maximise their own stones**. Return the **most stones Alice can get**.

```
piles = [2, 7, 9, 4, 4]   →  10     (Alice takes 2, Bob takes 7 and 9, Alice takes 4 and 4)
piles = [1, 2, 3, 4, 5, 100]   →  104
```

**Constraints:** `1 <= piles.length <= 100` · `1 <= piles[i] <= 10⁴`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| take from the **front** `X` piles | Remaining stones are always a **suffix** starting at some index `i` |
| `1 <= X <= 2M`, then `M = max(M, X)` | The state also needs the current `M` |
| both maximise **their own** stones | A zero-sum game: what I take, the opponent doesn't |
| "most stones Alice can get" | A DP value in stones (not a win/lose bit) |
| `n <= 100` | State `(i, M)` has at most `100 × 100` combinations |

**State:** `best(i, M)` = the most stones the player to move can collect from piles `i..n-1` when the current limit is `M`.

**Trick for the zero-sum part.** Whatever the mover doesn't collect goes to the opponent, so the mover's total is `suffix[i] − (opponent's best from the position I leave)`. A **suffix sum** array makes that an O(1) lookup.

For each choice `x` in `1..2M`:

`best(i, M) = max over x of ( suffix[i] − best(i + x, max(M, x)) )`

**Shortcut:** if `i + 2M >= n`, the mover can simply take **everything** that remains, so `best = suffix[i]`.

🤔 **Before you open the next section:** why is `best(i, M)` equal to `suffix[i]` when `i + 2M >= n`?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Time | Verdict |
|---|---|---|
| Plain recursion over `(i, M, X)` | exponential | ❌ |
| **Top-down memoised recursion on `(i, M)`** | **O(n³)** | ✅ About 100³ / 2 = 500,000 steps |
| Bottom-up table `dp[i][M]` | O(n³) | ✅ Same, filled from the end |

**The decision: memoised recursion over `(i, M)` with a suffix-sum array.** It's the [minimax](../algorithms/minimax.md) idea in [dynamic programming](../algorithms/dynamic-programming.md) form, a 2-D table where one axis is the index and the other is the current `M`.

Number of states: `n × n` (since `M <= n`). Work per state: up to `2M <= 2n` choices. Total **O(n³)**, perfect for `n = 100`.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
n = len(piles)
suffix = [0] * (n + 1)
for i in range(n - 1, -1, -1):
    suffix[i] = suffix[i + 1] + piles[i]
```

`suffix[i]` = stones in piles `i..n-1`. Build it right to left. `suffix[n] = 0` handles "nothing left".
→ [list-basics](../syntax/list-basics.md) · [range-function](../syntax/range-function.md) · [prefix sums idea](../learning/01b-prefix-sums.md)

```python
memo = {}

def best(i: int, m: int) -> int:
    if i >= n:
        return 0
    if i + 2 * m >= n:
        return suffix[i]
```

`best(i, m)` is the most the mover can take from `i` onwards with limit `m`. **Base cases:** no piles left → 0. If the mover can reach the end with one move (`i + 2m >= n`), they take everything.
→ [dict-basics](../syntax/dict-basics.md) · [closures](../syntax/closures.md) · [functools-cache](../syntax/functools-cache.md)

```python
    key = (i, m)
    if key in memo:
        return memo[key]
```

Memoise on the pair `(i, m)`. Different move orders reach the same `(i, m)`, so this removes the exponential blow-up.
→ [tuple-basics](../syntax/tuple-basics.md) · [membership-operators](../syntax/membership-operators.md)

```python
    result = 0
    for x in range(1, 2 * m + 1):
        result = max(result, suffix[i] - best(i + x, max(m, x)))
    memo[key] = result
    return result
```

Try each `x`. After taking `x` piles, the opponent moves from `i + x` with limit `max(m, x)` and collects `best(...)` of what remains. I keep the rest: `suffix[i] − best(...)`. Take the maximum over `x`.
→ [for-loop](../syntax/for-loop.md) · [min-max-key](../syntax/min-max-key.md)

```python
return best(0, 1)
```

Alice starts at index 0 with `M = 1`.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def stoneGameII(self, piles: List[int]) -> int:
        n = len(piles)
        suffix = [0] * (n + 1)
        for i in range(n - 1, -1, -1):
            suffix[i] = suffix[i + 1] + piles[i]

        memo = {}

        def best(i: int, m: int) -> int:
            if i >= n:
                return 0
            if i + 2 * m >= n:
                return suffix[i]

            key = (i, m)
            if key in memo:
                return memo[key]

            result = 0
            for x in range(1, 2 * m + 1):
                result = max(result, suffix[i] - best(i + x, max(m, x)))

            memo[key] = result
            return result

        return best(0, 1)
```

</details>

**Trace it.** `piles = [2, 7, 9, 4, 4]` (`suffix = [26, 24, 17, 8, 4, 0]`):

`best(0, 1)`: Alice may take `x = 1` or `2`.

| `x` | Alice takes | Bob's best from `(i+x, max(1,x))` | Alice's total |
|---|---|---|---|
| 1 | `[2]` | `best(1, 1)` = 16 (Bob takes 7 and 9, since `1+2·1 = 3 < 5`, computed recursively) | `26 − 16 = 10` |
| 2 | `[2, 7]` | `best(2, 2)`: `2 + 4 >= 5`, takes all: 17 | `26 − 17 = 9` |

`max(10, 9) = 10` ✅.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n³)</summary>

There are `O(n²)` states `(i, M)` and each tries up to `2M = O(n)` moves: **O(n³)**. For `n = 100` that's roughly half a million operations.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n²)</summary>

**O(n²)** for the memo, plus O(n) for the suffix sums and recursion depth.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The remaining stones are always a suffix, and the only other thing that matters is M, so the state is `(i, M)`. I define `best(i, M)` as the most stones the player to move can collect from there. If they can reach the end in one move, they take everything. Otherwise, for each x up to 2M, they take x piles and the opponent then plays `best(i + x, max(M, x))`; what's left over is mine, so it's the suffix sum minus the opponent's best. I memoise on `(i, M)`: O(n³) time and O(n²) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why use suffix sums?" | The game is zero-sum: my total is what remains minus the opponent's total |
| "Bottom-up?" | `dp[i][m]` for `i` from `n` down and `m` from `n` down, same recurrence |
| "Can you reduce the state?" | `M` never needs to exceed `n/2` usefully, since `2M >= n` immediately ends the game |
| "Related games?" | [Stone Game](877-stone-game.md) · [Stone Game III](1406-stone-game-iii.md) |
| "Why does `M` appear in the state?" | It limits future choices, so two positions at the same `i` with different `M` can have different outcomes |

**Traps:**

- **Forgetting `max(m, x)`** when passing the new `M`.
- **Omitting the `i + 2m >= n` shortcut.** It's an optimisation, but without the `i >= n` base case it crashes.
- **Returning the difference** instead of the stone count. This problem wants Alice's stones.
- **No memoisation.** `n = 100` times out.

**This same move shows up in:** [Stone Game III](1406-stone-game-iii.md) · [Stone Game](877-stone-game.md) · [Coin Change](322-coin-change.md) (memoised recursion on a small state).

</details>

---
