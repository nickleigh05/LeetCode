# 649. Dota2 Senate

**Medium** · [LeetCode](https://leetcode.com/problems/dota2-senate/) · [Solution file (no hints)](../../problems/0500-0999/649.py)

[📖 15. Greedy lesson](../learning/16-greedy.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 15. Greedy problems](../rmap-practice/15-greedy.md)

---

The senate has two parties, **Radiant** (`'R'`) and **Dire** (`'D'`). Voting proceeds in **rounds**, in the order the senators are listed. In his turn, a senator can either:

- **ban** one opposing senator (who then loses all rights, now and later), or
- **announce victory** if all remaining senators belong to his party.

Every senator plays optimally for his own party. Return `"Radiant"` or `"Dire"` for the winner.

```
senate = "RD"       →  "Radiant"   (the first R bans the D, and the D never gets a turn)
senate = "RDD"      →  "Dire"      (R bans a D, the other D bans R)
```

**Constraints:** `1 <= senate.length <= 10⁴` · each character is `'R'` or `'D'`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| rounds in listed order | A senator's **position** decides who acts first. Earlier is more powerful |
| "ban one opposing senator" | Each action removes someone from the other party |
| "optimal for his own party" | What's the best ban? |
| banned senators lose rights "now and later" | A banned senator who hasn't yet acted this round loses that turn too |

**The greedy insight: ban the next opponent who would act soonest.** The opponent who will move next is the most dangerous: they would ban one of *yours* before you act again. Removing a far-away opponent leaves the near one free to hit you first.

**Simulate with two queues of indices.** Keep the positions of each party in order. Each step, compare the **front** senator of each queue: the one with the smaller index acts first. He bans the other (removes that front), and then he **re-enters the queue for the next round**, with index `+ n` to keep the ordering correct (his next turn comes after everyone in this round).

The game ends when one queue is empty.

🤔 **Before you open the next section:** after `R` at index 2 bans `D` at index 3, why does the `R` rejoin the queue as index `2 + n`, and not as index `2`?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Time | Space | Verdict |
|---|---|---|---|
| Simulate rounds on a list, scanning for the next opponent to ban | O(n²) | O(n) | ⚠️ Works, with lots of removal bookkeeping |
| **Two queues of indices (greedy)** | **O(n)** | O(n) | ✅ |
| Counters of pending bans per party | O(n) per round | O(1) | ⚠️ Works, but harder to reason about |

**The decision: two [deques](../data-structures/deque.md) of indices.** Everything that matters about a senator is **when he next acts**, so store that number: the index in the current round, or `index + n` after he survives into the next. Popping both fronts and comparing finds who acts first. The loser is gone for good, and the winner goes back to the end of the line.

This is a "simulate with queues" greedy, in the same family as [Task Scheduler](621-task-scheduler.md).

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
n = len(senate)
radiant = deque()
dire = deque()
for i, party in enumerate(senate):
    if party == 'R':
        radiant.append(i)
    else:
        dire.append(i)
```

Split the senators into two queues holding their **turn order** (initially their positions). Because we scan left to right, each queue is already sorted.
→ [deque-basics](../syntax/deque-basics.md) · [deque](../data-structures/deque.md) · [enumerate](../syntax/enumerate.md)

```python
while radiant and dire:
    r = radiant.popleft()
    d = dire.popleft()
```

While both parties have senators, take the next one from each. These two are about to face off.
→ [while-loop](../syntax/while-loop.md) · [truthy-falsy-values](../syntax/truthy-falsy-values.md)

```python
    if r < d:
        radiant.append(r + n)
    else:
        dire.append(d + n)
```

The **smaller index acts first and bans the other**. The loser's index is simply not re-added: he's out. The winner survives into the **next round**, so he goes to the back with `+ n`, which puts him after every current-round senator but keeps the relative order of survivors.
→ [comparison-operators](../syntax/comparison-operators.md) · [if-return](../syntax/if-return.md)

```python
return "Radiant" if radiant else "Dire"
```

When one queue empties, the other party has won.
→ [ternary-expression](../syntax/ternary-expression.md)

<details>
<summary>The whole thing together</summary>

```python
from collections import deque


class Solution:
    def predictPartyVictory(self, senate: str) -> str:
        n = len(senate)
        radiant = deque()
        dire = deque()

        for i, party in enumerate(senate):
            if party == 'R':
                radiant.append(i)
            else:
                dire.append(i)

        while radiant and dire:
            r = radiant.popleft()
            d = dire.popleft()
            if r < d:
                radiant.append(r + n)
            else:
                dire.append(d + n)

        return "Radiant" if radiant else "Dire"
```

</details>

**Trace it.** `senate = "RDD"` (`n = 3`): `radiant = [0]`, `dire = [1, 2]`:

| Step | Fronts | Who acts first | Result |
|---|---|---|---|
| 1 | `r = 0`, `d = 1` | R (0 < 1) | R bans D#1. `radiant = [3]`, `dire = [2]` |
| 2 | `r = 3`, `d = 2` | D (2 < 3) | D bans R. `dire = [5]`, `radiant = []` |

Radiant is empty → **`"Dire"`** ✅.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).** Each loop iteration removes one senator for good (the loser), so there are at most `n - 1` iterations, each O(1).

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** for the two queues, which together hold at most `n` indices.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The best move is to ban the opponent who'd act next, because they're the biggest threat. So I keep two queues of indices, one per party, ordered by next turn. I compare the front of each: the smaller index acts first and bans the other, so the loser is dropped and the winner re-queues for the next round with index plus n. The first queue to empty loses. Each iteration removes one senator, so it's O(n) time and space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why ban the *next* opponent?" | Banning a distant one lets the nearest opponent ban one of yours first. An exchange argument shows banning the nearest is never worse |
| "Why `+ n`?" | It orders the winner after all remaining senators in the *current* round while preserving the order among survivors |
| "A counter-based O(1)-space approach?" | Track a running count of pending bans for each side as you sweep repeatedly. Fiddly: the queue version is easier to defend |
| "Three parties?" | The greedy changes, since there are choices about whom to ban |
| "Related?" | [Task Scheduler](621-task-scheduler.md) · [Reorganize String](767-reorganize-string.md) · [Hand of Straights](846-hand-of-straights.md) |

**Traps:**

- **Re-adding the winner with the *same* index.** The comparison then misorders future rounds.
- **Re-adding the loser** (they should vanish).
- **Banning from the back** instead of the front: ignoring who acts next.
- **Declaring the winner too early.** Loop until one queue is empty.

**This same move shows up in:** [Task Scheduler](621-task-scheduler.md) · [Last Stone Weight](1046-last-stone-weight.md) · [Implement Queue using Stacks](232-implement-queue-using-stacks.md).

</details>

---
