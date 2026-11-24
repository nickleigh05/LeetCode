# 997. Find the Town Judge

**Easy** · [LeetCode](https://leetcode.com/problems/find-the-town-judge/) · [Solution file (no hints)](../../problems/0500-0999/997.py)

[📖 11. Graphs lesson](../learning/11-graphs.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 11. Graphs problems](../rmap-practice/11-graphs.md)

---

A town has `n` people labelled `1..n`. Rumour says one of them is the **town judge**. If the judge exists:

1. The judge **trusts nobody**.
2. **Everybody else** trusts the judge.
3. There is exactly one person who satisfies 1 and 2.

`trust[i] = [a, b]` means person `a` trusts person `b`. Return the judge's label, or `-1` if there isn't one.

```
n = 2, trust = [[1, 2]]                    →  2
n = 3, trust = [[1, 3], [2, 3]]            →  3
n = 3, trust = [[1, 3], [2, 3], [3, 1]]    →  -1     (3 trusts someone)
```

**Constraints:** `1 <= n <= 1000` · `0 <= trust.length <= 10⁴` · all pairs distinct · `a != b`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| `trust` pairs `[a, b]` | A **directed graph**: an edge `a → b` ("a trusts b") |
| judge trusts nobody | The judge has **out-degree 0** |
| everyone else trusts the judge | The judge has **in-degree `n - 1`** |
| exactly one such person | Find the one node with `in = n - 1` and `out = 0`, or report none |

So it's a degree problem on a directed graph. No traversal required.

**One number per person.** Define `score[p] = (people who trust p) − (people p trusts)`, which is in-degree minus out-degree. For the judge, `score = (n - 1) - 0 = n - 1`.

Can anyone else reach `n - 1`? Anyone else has in-degree at most `n - 1`, and reaches it only with **out-degree 0**, but then they'd satisfy both conditions: they *are* the judge. So `score == n - 1` pins down the judge exactly.

🤔 **Before you open the next section:** with `n = 1` and no trust pairs, who is the judge? Does the score rule give that answer?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Time | Space | Verdict |
|---|---|---|---|
| Two arrays: `trusts[a]` count and `trusted_by[b]` count | O(n + E) | O(n) | ✅ Clear, with two arrays |
| **One array of scores** (`+1` for being trusted, `-1` for trusting) | **O(n + E)** | **O(n)** | ✅ Same, in half the code |
| Build an adjacency list and scan | O(n + E) | O(n + E) | ⚠️ More memory than needed |
| Check every person against every pair | O(n · E) | O(1) | ❌ Slower |

**The decision: a single [graph](../data-structures/graph.md) degree array.** Each trust pair `[a, b]` is one `-1` for `a` (trusts someone, so can't be the judge) and one `+1` for `b` (one more supporter). Read off the person whose score is exactly `n - 1`.

It's the "count in-degrees" trick used in [topological sort](../algorithms/topological-sort.md), here applied to find a **sink** node.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
score = [0] * (n + 1)
```

One slot per person. Index `0` is unused so labels `1..n` map straight to indices.
→ [list-basics](../syntax/list-basics.md)

```python
for a, b in trust:
    score[a] -= 1
    score[b] += 1
```

Each trust edge costs the truster a point (they trust someone, so they can't be the judge) and gives the trusted person a point. The judge only ever gains points.
→ [for-loop](../syntax/for-loop.md) · [tuple-unpacking](../syntax/tuple-unpacking.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
for person in range(1, n + 1):
    if score[person] == n - 1:
        return person
return -1
```

The judge is the only person who can reach `n - 1`: everyone else trusts them (`+n-1`) and they trust nobody (no deductions). If nobody has that score, there's no judge. This also handles `n = 1`: `score[1] = 0 = n - 1`, so person 1 is the judge.
→ [range-function](../syntax/range-function.md) · [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def findJudge(self, n: int, trust: List[List[int]]) -> int:
        score = [0] * (n + 1)

        for a, b in trust:
            score[a] -= 1
            score[b] += 1

        for person in range(1, n + 1):
            if score[person] == n - 1:
                return person

        return -1
```

</details>

**Trace it.** `n = 3`, `trust = [[1, 3], [2, 3], [3, 1]]`:

| Edge | `score[1]` | `score[2]` | `score[3]` |
|---|---|---|---|
| start | 0 | 0 | 0 |
| `[1, 3]` | -1 | 0 | +1 |
| `[2, 3]` | -1 | -1 | +2 |
| `[3, 1]` | 0 | -1 | +1 |

Is anyone at `n - 1 = 2`? No, so **`-1`** ✅. Person 3 had `+2` until they trusted person 1, which disqualified them.

With `[[1, 3], [2, 3]]` the scores end at `-1, -1, +2`, so person 3 is the judge.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n + E)</summary>

**O(n + E)**, where `E = len(trust)`: one pass over the edges and one pass over the people.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** for the score array. No adjacency list is stored.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "This is a directed graph where the judge is a sink: in-degree n−1 and out-degree 0. I keep one score per person: minus one for each person they trust, plus one for each person who trusts them. The judge's score is exactly n−1, and no one else can reach it, because reaching it would require trusting nobody, which makes them the judge. One pass over the edges and one over the people: O(n + E) time and O(n) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why not just count who's trusted `n - 1` times?" | A person trusted by everyone could still trust someone, so they'd fail rule 1. The `-1` for trusting handles it in the same number |
| "Two arrays instead?" | Equivalent: `in_count[p] == n - 1 and out_count[p] == 0` |
| "The celebrity problem?" | Same idea with a `knows(a, b)` API: eliminate candidates in O(n) calls with two pointers |
| "Duplicates in `trust`?" | The problem says pairs are distinct. Otherwise a set of edges is needed first |
| "Multiple judges?" | Impossible by the rules: two judges would each have to trust the other, contradicting rule 1 |

**Traps:**

- **Only counting in-degree.** Missing the "trusts nobody" rule.
- **A 0-indexed array of size `n`.** Labels start at 1.
- **Forgetting `n = 1`**: no edges, yet person 1 is the judge. `score[1] == 0 == n - 1` handles it.
- **Returning the first person with a positive score.**

**This same move shows up in:** [Course Schedule](207-course-schedule.md) (in-degree counting) · [Find if Path Exists in Graph](1971-find-if-path-exists-in-graph.md) · [Number of Provinces](547-number-of-provinces.md).

</details>

---
