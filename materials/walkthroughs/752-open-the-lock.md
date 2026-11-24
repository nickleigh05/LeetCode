# 752. Open the Lock

**Medium** · [LeetCode](https://leetcode.com/problems/open-the-lock/) · [Solution file (no hints)](../../problems/0500-0999/752.py)

[📖 11. Graphs lesson](../learning/11-graphs.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 11. Graphs problems](../rmap-practice/11-graphs.md)

---

A lock has **4 circular wheels**, each showing `0-9`. It starts at `"0000"`. One move turns **one wheel one step** (`9` wraps to `0` and `0` wraps to `9`). Some combinations are **deadends**: if the lock ever shows one, it jams. Return the **minimum number of moves** to reach `target`, or `-1` if impossible.

```
deadends = ["0201", "0101", "0102", "1212", "2002"],  target = "0202"   →  6
    "0000" → "1000" → "1100" → "1200" → "1201" → "1202" → "0202"

deadends = ["8888"],  target = "0009"                                    →  1    (turn the last wheel back from 0 to 9)
deadends = ["8887", "8889", "8878", "8898", "8788", "8988", "7888", "9888"],  target = "8888"   →  -1
```

**Constraints:** `1 <= deadends.length <= 500` · `deadends[i].length == target.length == 4` · `target` is not in `deadends`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "minimum number of moves" | **Shortest path** with equal-cost steps: the signature of **BFS** |
| lock states, one-wheel moves | A **graph** with `10⁴` nodes (every 4-digit string). Edges link states one move apart |
| each state has 8 neighbours | 4 wheels × 2 directions |
| deadends | **Forbidden nodes**: never enter them |
| "or `-1`" | The target may be unreachable (walled off by deadends) |

You don't build the graph in advance. Each state's neighbours are generated on demand by turning each wheel up or down.

**Edge case:** if `"0000"` is itself a deadend, the lock jams immediately: the answer is `-1`.

🤔 **Before you open the next section:** why does BFS find the *fewest* moves, and why do you need a `visited` set when each state has only 8 neighbours?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Time | Verdict |
|---|---|---|
| DFS | explores deep paths first and doesn't give shortest | ❌ |
| **BFS from `"0000"`** | **O(10⁴ · 8)** | ✅ Level by level, so the first time you reach `target` is the shortest |
| Bidirectional BFS | about √ of BFS in practice | ✅ A good follow-up |
| Dijkstra | unnecessary: all edges cost 1 | ⚠️ Overkill |

**The decision: [BFS](../algorithms/bfs.md) over the implicit graph.** The queue holds `(state, moves)`. Deadends are put in the `visited` set at the start, so the loop treats them as walls with no special case. This is the same "grid/state-space BFS" as [Rotting Oranges](994-rotting-oranges.md) and [Word Ladder](127-word-ladder.md), where the nodes are strings and a neighbour is one change away.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
visited = set(deadends)
if "0000" in visited:
    return -1
```

Pre-load the deadends into `visited`. Anything already "visited" is never entered, so deadends and repeats are handled by one check. A deadend start means the lock jams at once.
→ [set-basics](../syntax/set-basics.md) · [membership-operators](../syntax/membership-operators.md) · [if-return](../syntax/if-return.md)

```python
queue = deque([("0000", 0)])
visited.add("0000")
```

BFS queue of `(combination, moves so far)`. Mark the start visited the moment it's enqueued.
→ [deque-basics](../syntax/deque-basics.md) · [deque](../data-structures/deque.md) · [bfs](../algorithms/bfs.md)

```python
while queue:
    state, moves = queue.popleft()
    if state == target:
        return moves
```

Take the oldest state. **BFS reaches nodes in order of distance**, so the first time `target` is dequeued, `moves` is minimal.
→ [while-loop](../syntax/while-loop.md) · [tuple-unpacking](../syntax/tuple-unpacking.md)

```python
    for i in range(4):
        for step in (1, -1):
            digit = (int(state[i]) + step) % 10
            nxt = state[:i] + str(digit) + state[i + 1:]
```

Generate the 8 neighbours: wheel `i` up or down. `% 10` handles the wrap in both directions (Python gives `(-1) % 10 == 9`). Strings are immutable, so rebuild with a slice on either side of the changed digit.
→ [integer-division-modulo](../syntax/integer-division-modulo.md) · [list-slicing](../syntax/list-slicing.md) · [type-conversion](../syntax/type-conversion.md) · [string-immutability](../syntax/string-immutability.md)

```python
            if nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, moves + 1))

return -1
```

Enqueue unseen, non-deadend states. **Mark visited when enqueuing**, not when dequeuing, so no state enters the queue twice. If the queue empties, the target was walled off.

<details>
<summary>The whole thing together</summary>

```python
from collections import deque


class Solution:
    def openLock(self, deadends: List[str], target: str) -> int:
        visited = set(deadends)
        if "0000" in visited:
            return -1

        queue = deque([("0000", 0)])
        visited.add("0000")

        while queue:
            state, moves = queue.popleft()
            if state == target:
                return moves

            for i in range(4):
                for step in (1, -1):
                    digit = (int(state[i]) + step) % 10
                    nxt = state[:i] + str(digit) + state[i + 1:]
                    if nxt not in visited:
                        visited.add(nxt)
                        queue.append((nxt, moves + 1))

        return -1
```

</details>

**Trace it.** `deadends = ["8888"]`, `target = "0009"`:

| Dequeued | Neighbours | Result |
|---|---|---|
| `"0000"`, 0 moves | `1000, 9000, 0100, 0900, 0010, 0090, 0001, 0009` | enqueued, all at 1 move |
| `"1000"` … `"0001"` | 7 more expansions | not the target |
| `"0009"`, 1 move | | **return 1** ✅ |

The final wheel went `0 → 9` backwards. Moving "down" from 0 wraps to 9.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(10⁴ · 8)</summary>

There are at most `10⁴` distinct states, each visited once, and each generates 8 neighbours with O(4) string work: about **10⁴ × 8 × 4 ≈ 3 × 10⁵** operations. In general terms, **O(S · W · d)** with `S = 10ᵈ` states, `d` wheels and `W = 2d` neighbours.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(10⁴)</summary>

**O(10⁴)** for the `visited` set and the queue, bounded by the number of possible combinations.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Every combination is a node and every single-wheel turn is an edge, so this is a shortest path in an unweighted graph: BFS. I start from 0000 with the deadends pre-loaded into the visited set, so they act as walls. For each state I generate eight neighbours, turning each wheel up or down with wraparound, and enqueue the unseen ones with moves + 1, marking them visited when enqueued. The first time I dequeue the target, that's the minimum. If the queue empties, it's -1, and if 0000 is itself a deadend, that's -1 straight away. At most 10⁴ states, so it's fast."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Faster?" | **Bidirectional BFS**: search from both `0000` and `target`, always expanding the smaller frontier. Reaches the meeting point in far fewer steps |
| "Why mark visited when enqueuing?" | Marking on dequeue lets the same state be enqueued many times before it's processed: wasted work and a larger queue |
| "A\* instead?" | Possible, with the heuristic "sum of wheel distances to the target", but it's more code than the problem needs |
| "Different move rules?" | Only the neighbour generator changes |
| "Related BFS-on-strings?" | [Word Ladder](127-word-ladder.md) · [Minimum Knight Moves](1197-minimum-knight-moves.md) · [Rotting Oranges](994-rotting-oranges.md) |

**Traps:**

- **Forgetting that `"0000"` can be a deadend.** The answer is `-1` and the BFS would otherwise start in a forbidden state.
- **Not wrapping** (`9 + 1`, `0 - 1`). `% 10` handles both.
- **Checking `target` only when generating neighbours**, which complicates the case `target == "0000"`. Checking on dequeue is cleaner.
- **Using DFS.** It finds *a* path, not the shortest.

**This same move shows up in:** [Word Ladder](127-word-ladder.md) · [Rotting Oranges](994-rotting-oranges.md) · [Minimum Knight Moves](1197-minimum-knight-moves.md).

</details>

---
