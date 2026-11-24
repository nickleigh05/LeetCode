# 1871. Jump Game VII

**Medium** · [LeetCode](https://leetcode.com/problems/jump-game-vii/) · [Solution file (no hints)](../../problems/1500-1999/1871.py)

[📖 15. Greedy lesson](../learning/16-greedy.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 15. Greedy problems](../rmap-practice/15-greedy.md)

---

You have a binary string `s` and start at index `0` (`s[0] == '0'`). From index `i` you can jump to index `j` if **both**:

- `i + minJump <= j <= min(i + maxJump, n - 1)`, and
- `s[j] == '0'`.

Return `True` if you can reach the **last index** `n - 1`.

```
s = "011010",  minJump = 2,  maxJump = 3   →  True     0 → 3 → 5
s = "01101110", minJump = 2,  maxJump = 3   →  False
```

**Constraints:** `2 <= s.length <= 10⁵` · `s[i]` is `'0'` or `'1'` · `s[0] == '0'` · `1 <= minJump <= maxJump < s.length`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| jump `minJump..maxJump` steps forward | From each reachable index, a **window** of targets opens |
| land only on `'0'` | Cells with `'1'` are walls |
| "reach the last index" | `reachable[n-1]` is the answer: a boolean DP |
| `n` up to `10⁵` | The window can be ~`10⁵` wide, so naive "mark every target of every source" is O(n²) |

**Flip the question.** Instead of "from `i`, where can I go?", ask **"for target `j`, was any index in `[j − maxJump, j − minJump]` reachable?"** That's a **range query over a sliding window**.

`reachable[j] = (s[j] == '0') and (at least one reachable index lies in [j - maxJump, j - minJump])`

Count the reachable indices in that window with a **running counter** that updates as `j` moves right: add `reachable[j - minJump]` when it enters the window, remove `reachable[j - maxJump - 1]` when it leaves. That makes each cell O(1).

🤔 **Before you open the next section:** as `j` increases by one, which index enters the window and which leaves?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Time | Space | Verdict |
|---|---|---|---|
| BFS, marking every target in each source's window | O(n · maxJump) | O(n) | ❌ Up to 10¹⁰ |
| BFS with a "farthest marked" pointer (each cell enqueued once) | O(n) | O(n) | ✅ Also fine |
| DP + prefix sums over `reachable` | O(n) | O(n) | ✅ |
| **DP + a sliding-window counter** | **O(n)** | O(n) | ✅ Simplest |

**The decision: a boolean DP array plus a [sliding window](../learning/03-sliding-window.md) count.** `dp[j]` says "index `j` is reachable". The counter `window` holds `sum(dp[j - maxJump .. j - minJump])`. When `window > 0` and `s[j]` is `'0'`, `dp[j]` is true. This is the same "range of earlier answers" idea as a prefix sum, but incremental.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
n = len(s)
dp = [False] * n
dp[0] = True
window = 0
```

`dp[i]` = "can I be at index `i`". Index 0 is the start. `window` is the number of reachable indices currently inside the jump window of the cell being decided.
→ [list-basics](../syntax/list-basics.md) · [boolean-basics](../syntax/boolean-basics.md)

```python
for j in range(1, n):
    if j >= minJump and dp[j - minJump]:
        window += 1
```

Moving to `j`, the index `j - minJump` is the **newest** source that can jump exactly `minJump` to `j`. If it's reachable, it enters the window.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md) · [logical-operators](../syntax/logical-operators.md)

```python
    if j > maxJump and dp[j - maxJump - 1]:
        window -= 1
```

The index `j - maxJump - 1` is now one step too far to reach `j`: it **leaves** the window. Subtract it if it had been counted.
→ [comparison-operators](../syntax/comparison-operators.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
    dp[j] = window > 0 and s[j] == '0'

return dp[n - 1]
```

`j` is reachable if **some** source in range exists and the destination is a `'0'`. The last cell's value is the answer.
→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def canReach(self, s: str, minJump: int, maxJump: int) -> bool:
        n = len(s)
        dp = [False] * n
        dp[0] = True
        window = 0

        for j in range(1, n):
            if j >= minJump and dp[j - minJump]:
                window += 1
            if j > maxJump and dp[j - maxJump - 1]:
                window -= 1
            dp[j] = window > 0 and s[j] == '0'

        return dp[n - 1]
```

</details>

**Trace it.** `s = "011010"`, `minJump = 2`, `maxJump = 3`:

| `j` | enters (`j-2`) | leaves (`j-4`) | `window` | `s[j]` | `dp[j]` |
|---|---|---|---|---|---|
| 1 | `j < 2` | | 0 | `1` | F |
| 2 | `dp[0]` T → +1 | | 1 | `1` | F |
| 3 | `dp[1]` F | | 1 | `0` | **T** |
| 4 | `dp[2]` F | `dp[0]` T → −1 | 0 | `1` | F |
| 5 | `dp[3]` T → +1 | `dp[1]` F | 1 | `0` | **T** |

`dp[5] = True` ✅ (path 0 → 3 → 5).

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n):** one pass; each step adds at most one index and removes at most one.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** for `dp`. It could shrink to a queue of the last `maxJump` entries but the array is clearer.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The naive way marks every target in every reachable index's window, which is O(n·maxJump). Instead I flip it: index j is reachable if it's a '0' and at least one reachable index lies in `[j − maxJump, j − minJump]`. I keep a running count of reachable indices in that window. When j advances, `j − minJump` enters and `j − maxJump − 1` leaves, each an O(1) update. One pass: O(n) time, O(n) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "BFS version?" | Keep a `farthest` pointer so each index is enqueued once: for each popped `i`, scan from `max(i + minJump, farthest + 1)` to `min(i + maxJump, n-1)` |
| "Prefix-sum version?" | `pre[k]` = reachable count among the first `k` indices. Window count = `pre[j - minJump + 1] - pre[j - maxJump]` |
| "Why not greedy?" | Reachability isn't monotone: the farthest jump isn't always the right one because of the `'1'` walls |
| "Why `j > maxJump`?" | So that index `j - maxJump - 1 >= 0` |
| "Related?" | [Jump Game](55-jump-game.md) · [Jump Game II](45-jump-game-ii.md) · [Sliding Window Maximum](239-sliding-window-maximum.md) |

**Traps:**

- **Off-by-one on the leaving index.** It's `j - maxJump - 1`, not `j - maxJump`.
- **Adding the entering index only when `s[...] == '0'`.** It's a source: only whether it's *reachable* matters.
- **Forgetting that the destination must be `'0'`.**
- **O(n · maxJump) marking.** It times out at `10⁵`.

**This same move shows up in:** [Jump Game](55-jump-game.md) · [Sliding Window Maximum](239-sliding-window-maximum.md) (sliding window over earlier values) · [Climbing Stairs](70-climbing-stairs.md) (each state depends on a window of earlier states).

</details>

---
