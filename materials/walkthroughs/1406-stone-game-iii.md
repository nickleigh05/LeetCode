# 1406. Stone Game III

**Hard** · [LeetCode](https://leetcode.com/problems/stone-game-iii/) · [Solution file (no hints)](../../problems/1000-1499/1406.py)

[📖 13. 1-D Dynamic Programming lesson](../learning/14-dp-1d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 13. 1-D Dynamic Programming problems](../rmap-practice/13-dp-1d.md)

---

Alice and Bob play with a row of stones, `stoneValue[i]` each (values may be **negative**). Alice goes first. On a turn, the player takes **1, 2, or 3 stones from the front** of the row. A player's score is the sum of the values they take. Both play **optimally**. Return `"Alice"` if she wins, `"Bob"` if he wins, or `"Tie"`.

```
stoneValue = [1, 2, 3, 7]     →  "Bob"      (Alice can't avoid leaving Bob the 7)
stoneValue = [1, 2, 3, -9]    →  "Alice"    (she takes 1+2+3 = 6 and leaves Bob the -9)
stoneValue = [1, 2, 3, 6]     →  "Tie"
```

**Constraints:** `1 <= stoneValue.length <= 5 * 10⁴` · `-1000 <= stoneValue[i] <= 1000`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "take 1, 2, or 3 from the front" | The game state is just **how many stones are gone**: index `i`. A one-dimensional state |
| "both play optimally" | **Minimax**: you maximise your result, the opponent maximises theirs |
| compare Alice's score to Bob's | You only need the **difference** `me − opponent` |
| negative values | Greed ("take as much as you can") fails: sometimes you must take a loss to avoid a bigger one |
| `n` up to `5 * 10⁴` | Needs O(n) or O(n log n): no exponential game tree |

**The difference trick** turns a two-player game into a single DP. Define `dp[i]` = the **best (my score − opponent's score)** the player *to move* can achieve from stones `i..n-1`. If I take `k` stones, I gain their sum, and then the opponent faces `dp[i+k]`, which is *their* advantage from there. So my net is `sum − dp[i+k]`. I pick the best `k`:

`dp[i] = max over k in {1,2,3} of ( stones[i..i+k-1] summed − dp[i+k] )`, with `dp[n] = 0`.

The final answer looks at `dp[0]`: positive → Alice, negative → Bob, zero → Tie.

🤔 **Before you open the next section:** why is it `− dp[i+k]` and not `+ dp[i+k]`?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Time | Verdict |
|---|---|---|
| Plain recursion over all moves | O(3ⁿ) | ❌ |
| Top-down with memo on `i` | O(n) | ✅ Same DP, with a stack at depth `n` (risky at `5 * 10⁴`) |
| **Bottom-up [DP](../algorithms/dynamic-programming.md) from the end** | **O(n)** | ✅ No recursion limit issue |
| Track score pairs `(Alice, Bob)` | O(n) | ⚠️ Same thing, and messier |

**The decision: a bottom-up 1-D DP over score difference, filled from the last stone to the first.** It's the [minimax](../algorithms/minimax.md) idea compressed into a table, because a game whose only state is "where are we" needs no recursion tree.

`dp[i]` only reads `dp[i+1]`, `dp[i+2]`, `dp[i+3]`, so a 3-wide window is enough for O(1) space, but the full array is clearer.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
n = len(stoneValue)
dp = [0] * (n + 1)
```

`dp[i]` is the best advantage for whoever moves with stones `i..n-1` remaining. `dp[n] = 0`: no stones left, no advantage either way.
→ [list-basics](../syntax/list-basics.md) · [dynamic-programming](../algorithms/dynamic-programming.md)

```python
for i in range(n - 1, -1, -1):
    best = float('-inf')
    total = 0
```

Fill backwards, because `dp[i]` depends on later positions. `best` tracks the best advantage for this `i`. `total` accumulates the stones taken on this turn.
→ [range-function](../syntax/range-function.md) · [float-inf](../syntax/float-inf.md) · [for-loop](../syntax/for-loop.md)

```python
    for k in range(1, 4):
        if i + k > n:
            break
        total += stoneValue[i + k - 1]
        best = max(best, total - dp[i + k])
    dp[i] = best
```

Try taking `k = 1, 2, 3` stones (stopping if that runs past the end). `total` is the sum of those `k` stones. The opponent then faces `i + k` with advantage `dp[i + k]`, so my net gain is `total - dp[i + k]`. Keep the best choice.
→ [break-continue](../syntax/break-continue.md) · [min-max-key](../syntax/min-max-key.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
if dp[0] > 0:
    return "Alice"
if dp[0] < 0:
    return "Bob"
return "Tie"
```

`dp[0]` is Alice's best advantage over Bob. Its sign decides the result.
→ [if-return](../syntax/if-return.md) · [comparison-operators](../syntax/comparison-operators.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def stoneGameIII(self, stoneValue: List[int]) -> str:
        n = len(stoneValue)
        dp = [0] * (n + 1)

        for i in range(n - 1, -1, -1):
            best = float('-inf')
            total = 0
            for k in range(1, 4):
                if i + k > n:
                    break
                total += stoneValue[i + k - 1]
                best = max(best, total - dp[i + k])
            dp[i] = best

        if dp[0] > 0:
            return "Alice"
        if dp[0] < 0:
            return "Bob"
        return "Tie"
```

</details>

**Trace it.** `stoneValue = [1, 2, 3, 7]`:

| `i` | Options (`sum − dp[i+k]`) | `dp[i]` |
|---|---|---|
| 4 | none | 0 |
| 3 | take `[7]`: `7 − 0` | **7** |
| 2 | `[3]`: `3 − 7 = −4`; `[3,7]`: `10 − 0 = 10` | **10** |
| 1 | `[2]`: `2 − 10 = −8`; `[2,3]`: `5 − 7 = −2`; `[2,3,7]`: `12 − 0 = 12` | **12** |
| 0 | `[1]`: `1 − 12 = −11`; `[1,2]`: `3 − 10 = −7`; `[1,2,3]`: `6 − 7 = −1` | **−1** |

`dp[0] = −1 < 0` → **`"Bob"`** ✅.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n):** `n` positions, 3 choices each. For `n = 5 * 10⁴` that's about 150,000 steps.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n), or O(1)</summary>

**O(n)** for the table. Since `dp[i]` reads only `dp[i+1..i+3]`, a rolling window of 4 values brings it to **O(1)**.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The state is just how many stones are gone, so I'll define `dp[i]` as the best score difference, mover minus opponent, from stones `i` onward. If I take k stones I gain their sum, then the opponent is the one to move at `i+k` with advantage `dp[i+k]`, so my net is the sum minus that. I take the best k out of 1, 2, 3, filling from the back. The sign of `dp[0]` decides Alice, Bob or Tie. O(n) time, and O(1) space with a rolling window."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why track a difference, not both scores?" | The opponent's optimal play depends only on position, so one number captures the whole future |
| "Why not greedy?" | With negative stones, taking more can be worse. Taking `[1,2,3]` there leaves Bob the −9 |
| "Space?" | Keep only `dp[i+1], dp[i+2], dp[i+3]` |
| "Take 1 or 2 stones only?" | Same recurrence with `k` up to 2. The classic version has a math answer for some rules |
| "Related games?" | [Stone Game](877-stone-game.md) (take from either end) · [Stone Game II](1140-stone-game-ii.md) (take up to `2M`) |

**Traps:**

- **`+ dp[i+k]`** instead of `−`. The next state's value belongs to the *opponent*.
- **Iterating forwards.** `dp[i]` needs later entries filled first.
- **Not stopping `k` at the end of the row** (index error).
- **Starting `best` at 0.** A forced loss can be negative: use `-inf`.

**This same move shows up in:** [Stone Game](877-stone-game.md) · [Stone Game II](1140-stone-game-ii.md) · [House Robber](198-house-robber.md) (a 1-D DP over positions).

</details>

---
