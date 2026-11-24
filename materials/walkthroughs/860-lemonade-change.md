# 860. Lemonade Change

**Easy** · [LeetCode](https://leetcode.com/problems/lemonade-change/) · [Solution file (no hints)](../../problems/0500-0999/860.py)

[📖 15. Greedy lesson](../learning/16-greedy.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 15. Greedy problems](../rmap-practice/15-greedy.md)

---

At a lemonade stand each lemonade costs **$5**. Customers queue in order and each buys **one** lemonade, paying with a `$5`, `$10` or `$20` bill. You start with **no change**. Give every customer the correct change, so the net transaction is exactly $5. Return `True` if you can serve everyone.

```
bills = [5, 5, 5, 10, 20]   →  True
bills = [5, 5, 10, 10, 20]  →  False     (two `$10`s but no `$5` left to go with them for the `$20`)
```

**Constraints:** `1 <= bills.length <= 10⁵` · `bills[i]` is `5`, `10`, or `20`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "start with no change" | You can only give change from bills customers have already handed you |
| change = bill − 5 | `$5` → nothing, `$10` → one `$5`, `$20` → `$15` |
| only three denominations | You only need to track **how many `$5`s and `$10`s** you hold. `$20`s are never given out |
| customers processed in order | Simulate the queue left to right and fail at the first customer you can't serve |

**The only real decision is how to make `$15` for a `$20` bill.** Two ways exist: one `$10` + one `$5`, or three `$5`s.

**Greedy choice: use the `$10` first.** `$5` bills are the **more flexible** currency (they can serve both `$10` and `$20` customers), whereas a `$10` can only ever be used for a `$20`. So spend the less flexible bill when you can, and keep the `$5`s.

🤔 **Before you open the next section:** why is it never worse to hand out `$10 + $5` than `$5 + $5 + $5` when both are possible?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Time | Space | Verdict |
|---|---|---|---|
| Track the full multiset of bills in hand | O(n) | O(n) | ⚠️ Works, with unneeded memory |
| **Two counters (`fives`, `tens`) + greedy** | **O(n)** | **O(1)** | ✅ |
| Try both ways to give `$15` (backtracking) | exponential | | ❌ Unnecessary: the greedy choice is provably safe |

**The decision: [greedy](../learning/16-greedy.md) with two counters.** Exchange argument: keeping a `$5` instead of a `$10` can only help in the future, because every future customer a `$10` could serve, a `$5`-plus-something could also serve, and `$5`s serve the `$10` customers too. So always prefer giving a `$10 + $5` pair for a `$20` over three `$5`s.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
fives = 0
tens = 0
```

The bills you can give as change. `$20`s never need counting: they can't be given back (change is at most $15).
→ [variables-assignment](../syntax/variables-assignment.md)

```python
for bill in bills:
    if bill == 5:
        fives += 1
```

A `$5` payment needs no change: pocket it.
→ [for-loop](../syntax/for-loop.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
    elif bill == 10:
        if fives == 0:
            return False
        fives -= 1
        tens += 1
```

A `$10` needs one `$5` back. If there's none, fail. Otherwise swap: `$5` out, `$10` in.
→ [elif-else](../syntax/elif-else.md) · [if-return](../syntax/if-return.md)

```python
    else:
        if tens > 0 and fives > 0:
            tens -= 1
            fives -= 1
        elif fives >= 3:
            fives -= 3
        else:
            return False
```

A `$20` needs `$15` back. **Prefer `$10 + $5`** (the greedy choice). Only if that's impossible, use three `$5`s. If neither works, fail.
→ [logical-operators](../syntax/logical-operators.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
return True
```

Nobody was turned away.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def lemonadeChange(self, bills: List[int]) -> bool:
        fives = 0
        tens = 0

        for bill in bills:
            if bill == 5:
                fives += 1
            elif bill == 10:
                if fives == 0:
                    return False
                fives -= 1
                tens += 1
            else:
                if tens > 0 and fives > 0:
                    tens -= 1
                    fives -= 1
                elif fives >= 3:
                    fives -= 3
                else:
                    return False

        return True
```

</details>

**Trace it.** `bills = [5, 5, 10, 10, 20]`:

| Bill | Action | `fives` | `tens` |
|---|---|---|---|
| 5 | keep | 1 | 0 |
| 5 | keep | 2 | 0 |
| 10 | give a 5 | 1 | 1 |
| 10 | give a 5 | 0 | 2 |
| 20 | needs `$15`: `tens > 0` but `fives == 0`; `fives < 3` | | |

**`False`** ✅. Two `$10`s are useless without a `$5` to go with them. This is exactly why you protect `$5`s.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n):** one pass, O(1) work per customer.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1):** two counters.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "I simulate the queue and track only the number of $5 and $10 bills, because $20s never go back as change. A $5 needs nothing, a $10 needs one $5. A $20 needs $15, and I have two ways to make that, $10 + $5 or three $5s. I always prefer the $10 + $5, since $5s are the more useful bill: they can serve both $10 and $20 customers, while a $10 can only help with a $20. If I can't make change at any point I return False. O(n) time, O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why is greedy safe?" | Exchange argument: any future use of a retained `$10` could be replaced with `$5`s at least as flexibly, while a `$5` can be used where a `$10` can't |
| "More denominations?" | Greedy may stop working (coin systems that aren't canonical), and you'd need DP or backtracking. See [Coin Change](322-coin-change.md) |
| "Different ticket price?" | The change amounts change but the structure is the same: spend the less flexible bills first |
| "Start with some change?" | Initialise `fives` and `tens` |
| "Related greedy problems?" | [Jump Game](55-jump-game.md) · [Gas Station](134-gas-station.md) |

**Traps:**

- **Using three `$5`s first for a `$20`.** It can strand later `$10`s.
- **Storing `$20` bills.** They're never useful as change.
- **Forgetting to count the `$10` you receive** (`tens += 1`).
- **Returning `True` early** without processing everyone.

**This same move shows up in:** [Jump Game](55-jump-game.md) · [Gas Station](134-gas-station.md) · [Partition Labels](763-partition-labels.md).

</details>

---
