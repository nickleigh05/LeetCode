# 473. Matchsticks to Square

**Medium** · [LeetCode](https://leetcode.com/problems/matchsticks-to-square/) · [Solution file (no hints)](../../problems/0001-0499/473.py)

[📖 10. Backtracking lesson](../learning/10-backtracking.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 10. Backtracking problems](../rmap-practice/10-backtracking.md)

---

`matchsticks[i]` is the length of the `i`-th stick. Use **every** stick exactly once, without breaking any, to form a **square**. Return `True` if that's possible.

```
matchsticks = [1, 1, 2, 2, 2]   →  True    (sides: 2, 2, 2, and 1+1)
matchsticks = [3, 3, 3, 3, 4]   →  False
```

**Constraints:** `1 <= matchsticks.length <= 15` · `1 <= matchsticks[i] <= 10⁸`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "use every stick exactly once" | Partition **all** the sticks into groups |
| "form a square" | Exactly **4 groups**, each summing to `total / 4` |
| can't break a stick | A stick goes whole into one side |
| `length <= 15` | Exponential search (4¹⁵ ≈ 10⁹ worst) is intended, **pruned heavily** |
| sticks up to 10⁸ | Sums can be big, so you can't DP over sums |

**Quick rejections before any search:**

- `total % 4 != 0` → impossible.
- Any stick longer than `side = total / 4` → impossible.

**Then it's [Partition to K Equal Sum Subsets](698-partition-to-k-equal-sum-subsets.md) with `k = 4`.** Backtrack stick by stick: try placing the current stick on each of the 4 sides, if it fits, recurse. If all sticks are placed, every side is full (since the totals match).

🤔 **Before you open the next section:** why does placing the **longest sticks first** make the search faster? And why is it pointless to try a stick on two sides that currently have the same length?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Time | Verdict |
|---|---|---|
| Try all `4ⁿ` assignments | O(4ⁿ) | ❌ About 10⁹ for `n = 15`, without pruning |
| **Backtracking: stick → side, with pruning** | far less than 4ⁿ in practice | ✅ The standard answer |
| Bitmask DP over subsets | O(2ⁿ · n) | ✅ Strong alternative: `dp[mask]` = leftover length of the side being filled |

**The decision: [backtracking](../algorithms/backtracking.md) with three prunings.**

1. **Sort descending.** Big sticks have the fewest legal places, so they fail fast. Small sticks fill gaps last.
2. **Skip a side that doesn't fit** (`side_len + stick > target`).
3. **Skip duplicate states.** If two sides currently have the *same* length, putting the stick on either leads to identical futures. Try only one of them. This is the single most effective prune.

The same machinery solves [Partition to K Equal Sum Subsets](698-partition-to-k-equal-sum-subsets.md); here `k` is fixed at 4.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
total = sum(matchsticks)
if total % 4 != 0:
    return False
side = total // 4
matchsticks.sort(reverse=True)
if matchsticks[0] > side:
    return False
```

Reject impossible inputs immediately. Sorting **descending** puts the hardest sticks first, and the second check catches a stick longer than any side.
→ [integer-division-modulo](../syntax/integer-division-modulo.md) · [list-methods](../syntax/list-methods.md) · [sorting-key](../syntax/sorting-key.md)

```python
sides = [0] * 4
```

The current length of each of the four sides.
→ [list-basics](../syntax/list-basics.md)

```python
def place(i: int) -> bool:
    if i == len(matchsticks):
        return True
```

`place(i)` tries to place stick `i` and everything after it. **All sticks placed** means success: since the total is exactly `4 × side` and no side was allowed to exceed `side`, every side is exactly full.
→ [recursion-basics](../syntax/recursion-basics.md) · [closures](../syntax/closures.md)

```python
    seen = set()
    for j in range(4):
        if sides[j] + matchsticks[i] > side or sides[j] in seen:
            continue
        seen.add(sides[j])
```

Try each side, skipping two kinds. Sides where the stick **overflows**. And sides whose **current length was already tried** for this stick (`seen`), since equal-length sides are interchangeable.
→ [set-basics](../syntax/set-basics.md) · [break-continue](../syntax/break-continue.md) · [logical-operators](../syntax/logical-operators.md)

```python
        sides[j] += matchsticks[i]
        if place(i + 1):
            return True
        sides[j] -= matchsticks[i]
    return False
```

**Choose, explore, un-choose.** Add the stick, recurse. If it works, bubble `True` up. Otherwise **undo** the placement and try the next side. When no side works, this branch fails and the caller backs up.
→ [backtracking](../algorithms/backtracking.md)

```python
return place(0)
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def makesquare(self, matchsticks: List[int]) -> bool:
        total = sum(matchsticks)
        if total % 4 != 0:
            return False

        side = total // 4
        matchsticks.sort(reverse=True)
        if matchsticks[0] > side:
            return False

        sides = [0] * 4

        def place(i: int) -> bool:
            if i == len(matchsticks):
                return True

            seen = set()
            for j in range(4):
                if sides[j] + matchsticks[i] > side or sides[j] in seen:
                    continue
                seen.add(sides[j])

                sides[j] += matchsticks[i]
                if place(i + 1):
                    return True
                sides[j] -= matchsticks[i]

            return False

        return place(0)
```

</details>

**Trace it.** `[1, 1, 2, 2, 2]`: total 8, side 2, sorted `[2, 2, 2, 1, 1]`:

| Stick | Placement | `sides` |
|---|---|---|
| 2 | side 0 | `[2, 0, 0, 0]` |
| 2 | side 0 would overflow, side 1 | `[2, 2, 0, 0]` |
| 2 | side 2 | `[2, 2, 2, 0]` |
| 1 | sides 0-2 overflow, side 3 | `[2, 2, 2, 1]` |
| 1 | only side 3 fits | `[2, 2, 2, 2]` |
| end | `i == 5` | **`True`** ✅ |

</details>

<details>
<summary><b>4 · Time complexity</b> — O(4ⁿ) worst case, much less in practice</summary>

Each stick has up to 4 choices: **O(4ⁿ)** worst case. The prunings cut it hard: overflow checks stop most branches early, and the `seen` check divides symmetric branches. For `n = 15` this runs fast. The bitmask DP guarantees **O(2ⁿ · n)**.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** recursion depth (one frame per stick), plus the 4-element `sides` list and the per-call `seen` set of at most 4 values.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "A square needs four sides each equal to a quarter of the total, so I reject early if the total isn't divisible by 4 or a stick exceeds the side. Then I backtrack: sort descending, and for each stick try each side if it fits, recursing and undoing on failure. Two prunings make it fast: skipping sides whose current length I've already tried for this stick, since they're interchangeable, and putting big sticks first so dead ends appear early. Worst case O(4ⁿ), but with `n <= 15` and pruning it's quick. A bitmask DP would give O(2ⁿ·n)."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Guaranteed polynomial?" | No. This is a partition problem (NP-hard in general). Bitmask DP gives O(2ⁿ · n) for small `n` |
| "Bitmask DP?" | `dp[mask]` = the length filled in the side currently being built (or −1 if impossible). Add a stick to `mask` if it fits in the current side, wrapping modulo `side` |
| "Generalise to `k` groups?" | [Partition to K Equal Sum Subsets](698-partition-to-k-equal-sum-subsets.md): replace 4 with `k` |
| "Why sort descending?" | A large stick has few places, so failures show up early and the tree stays shallow |
| "Why does `seen` help?" | Equal side lengths are interchangeable. Trying one is equivalent to trying all of them |

**Traps:**

- **Forgetting to undo** (`sides[j] -= …`) after a failed recursion.
- **No total-divisible check**, so a `side` of the wrong size is explored.
- **Skipping the `matchsticks[0] > side` check.** The search does extra work before failing.
- **Mutating the input's order unexpectedly** (the sort). Mention it if the caller's list matters.

**This same move shows up in:** [Partition to K Equal Sum Subsets](698-partition-to-k-equal-sum-subsets.md) · [Partition Equal Subset Sum](416-partition-equal-subset-sum.md) (`k = 2`, solved with DP) · [Combination Sum](39-combination-sum.md) (choose, explore, un-choose).

</details>

---
