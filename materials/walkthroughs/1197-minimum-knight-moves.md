# 1197. Minimum Knight Moves

**Medium** · 🔒 Premium · [LeetCode](https://leetcode.com/problems/minimum-knight-moves/) · [Solution file (no hints)](../../problems/1000-1499/1197.py)

[📖 11. Graphs lesson](../learning/11-graphs.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 11. Graphs problems](../rmap-practice/11-graphs.md)

---

On an **infinite** chessboard, a knight starts at `[0, 0]`. A knight has 8 possible moves: two squares in one direction (horizontal or vertical), then one square at right angles.

```
. 8 . 1 .
7 . . . 2
. . N . .
6 . . . 3
. 5 . 4 .
```

Return the **minimum number of steps** to move the knight to `[x, y]`. The answer is guaranteed to exist.

```
x = 2, y = 1   →  1      [0,0] → [2,1]
x = 5, y = 5   →  4      [0,0] → [2,1] → [4,2] → [3,4] → [5,5]
```

**Constraints:** `-300 <= x, y <= 300` · `0 <= |x| + |y| <= 300`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**minimum** number of steps" | Every move costs 1, so it's unweighted shortest path, which means **BFS** |
| **infinite** board | No edges to stop the search. Without a bound, BFS spreads in every direction and visits far more squares than needed |
| target anywhere in `[-300, 300]` | The board is symmetric. A target in any quadrant takes the same steps as its mirror image in the first quadrant |
| `|x| + |y| <= 300` | The BFS stays within a few hundred squares of the origin in each direction |

**Use symmetry.** Reflecting the board across either axis maps knight moves to knight moves. So the number of steps to `(x, y)` equals the steps to `(|x|, |y|)`. Take absolute values and search the first quadrant only.

**But you can't completely ban negative coordinates.** Sometimes the shortest path dips just below zero. To reach `(1, 1)`, the fastest route is `(0,0) → (2,-1) → (1,1)`, which is 2 moves. If you forbade every negative square, you'd get 4. A knight never needs to go more than **two squares** into negative territory, so allow `x >= -2` and `y >= -2`. That's enough room for every shortcut near the axes, while still cutting off most of the infinite board.

🤔 **Before you open the next section:** why is restricting the search to `x >= -2, y >= -2` safe, but `x >= 0, y >= 0` wrong?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Plain BFS, unbounded | Expand all 8 moves everywhere | O(d²) squares, large constant | O(d²) | ⚠️ Correct, explores all four quadrants |
| **BFS with symmetry + bound** | `abs` the target, allow only `x, y >= -2` | **O(d²)**, ~4× fewer squares | O(d²) | ✅ |
| Bidirectional BFS | Search from both ends, meet in the middle | O(d²), smaller constant | O(d²) | ✅ Faster, more code |
| DP / formula with memo | Recursive on `(x, y)` with base cases near the origin | O(x·y) | O(x·y) | ✅ Clever, harder to justify |

Here d is about `|x| + |y|`, the distance to the target.

**The decision: [BFS](../algorithms/bfs.md) with a [queue](../data-structures/queue.md), plus symmetry and a small bound.**

BFS guarantees the first time you reach the target is by a shortest route. Symmetry and the bound reduce the search area by about 4× with one line each. That's enough to pass comfortably.

**What about the DP formula?** There's a known recursion: `f(x, y) = min(f(|x-1|, |y-2|), f(|x-2|, |y-1|)) + 1`, with base cases `f(0,0) = 0` and `f(x,y) = 2` when `x + y == 2`. It's elegant, but proving the base cases is harder than the BFS. Mention it as an optimisation.

**Bidirectional BFS** grows two smaller frontiers that meet in the middle. It's a big win in theory, but it adds complexity that this input size doesn't need.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
x, y = abs(x), abs(y)
```

**Symmetry.** Mirror the target into the first quadrant. The step count is unchanged.
→ [math-module-basics](../syntax/math-module-basics.md) · [tuple-unpacking](../syntax/tuple-unpacking.md)

```python
moves = [(1, 2), (2, 1), (2, -1), (1, -2),
         (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
```

All 8 knight moves as `(dx, dy)` pairs. Each is `(±1, ±2)` or `(±2, ±1)`.
→ [list-basics](../syntax/list-basics.md) · [tuple-basics](../syntax/tuple-basics.md)

```python
queue = deque([(0, 0, 0)])
visited = {(0, 0)}
```

Start at the origin with 0 steps taken. `visited` holds coordinate tuples, so each square is queued at most once.
→ [deque-basics](../syntax/deque-basics.md) · [set-basics](../syntax/set-basics.md)

```python
while queue:
    r, c, steps = queue.popleft()
    if (r, c) == (x, y):
        return steps
```

**Standard BFS.** Squares come off the queue in order of distance, so the first time the target appears, `steps` is the minimum. Tuple equality compares both coordinates.
→ [while-loop](../syntax/while-loop.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
    for dr, dc in moves:
        nr, nc = r + dr, c + dc
        if nr >= -2 and nc >= -2 and (nr, nc) not in visited:
            visited.add((nr, nc))
            queue.append((nr, nc, steps + 1))
```

**Expand, with the bound.** Allow squares only up to two into negative territory. That keeps the shortcuts near the axes (like reaching `(1,1)` through `(2,-1)`) and cuts off the rest of the other three quadrants. Mark each square when you queue it, so it's never queued twice.
→ [logical-operators](../syntax/logical-operators.md) · [membership-operators](../syntax/membership-operators.md)

<details>
<summary>The whole thing together</summary>

```python
from collections import deque

class Solution:
    def minKnightMoves(self, x: int, y: int) -> int:
        x, y = abs(x), abs(y)
        moves = [(1, 2), (2, 1), (2, -1), (1, -2),
                 (-1, -2), (-2, -1), (-2, 1), (-1, 2)]

        queue = deque([(0, 0, 0)])
        visited = {(0, 0)}

        while queue:
            r, c, steps = queue.popleft()
            if (r, c) == (x, y):
                return steps

            for dr, dc in moves:
                nr, nc = r + dr, c + dc
                if nr >= -2 and nc >= -2 and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append((nr, nc, steps + 1))
```

</details>

**Trace it.** `x = 1, y = 1`, the case that needs the negative margin:

| Ring | Some squares reached | Target? |
|---|---|---|
| 0 | (0,0) | no |
| 1 | (1,2), (2,1), **(2,−1)**, (−1,2), (−2,1), (1,−2), … | no |
| 2 | from (2,−1): (2−1, −1+2) = **(1,1)** | **yes → 2** ✅ |

With a bound of `x, y >= 0`, the squares `(2,−1)` and `(−1,2)` would be banned, and the shortest route to `(1, 1)` would take **4** moves. That's why the margin is −2, not 0.

**`x = 5, y = 5`** returns **4**, matching the example's path.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(d²)</summary>

**O(d²)** squares, where d ≈ `|x| + |y|`.

BFS explores roughly every square within d knight moves of the origin. A knight covers about 2–3 squares of distance per move, so that region is about the size of a d × d patch. Each square is visited once and checks 8 moves, which is O(1) per square.

With `|x| + |y| <= 300`, that's at most around 10⁵ squares, which is quick. Symmetry and the bound cut the explored area to roughly a quarter of the unbounded search.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(d²)</summary>

**O(d²).** The `visited` set holds every explored square, and the queue holds the current frontier.

Bidirectional BFS shrinks both: two searches of radius d/2 cover about half the area of one search of radius d.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Every move costs 1, so it's BFS from the origin. The board is infinite, so I need to limit the search. The board is symmetric, so I take the absolute value of the target and work in the first quadrant. I can't ban negative squares entirely, because shortcuts near the axes dip below zero, like (0,0) to (2,-1) to (1,1). So I allow coordinates down to -2. The first time the target comes off the queue, that's the answer. O(d²) time and space for target distance d."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why −2 and not 0?" | `(1,1)` needs a detour through `(2,−1)`. Two squares of margin is enough for any knight shortcut near the axes. |
| "Faster?" | Bidirectional BFS, or the memoised recursion `f(x,y) = 1 + min(f(|x−1|,|y−2|), f(|x−2|,|y−1|))` with small base cases. |
| "Finite board with obstacles?" | Plain BFS with a bounds check and a blocked set, like [Shortest Path to Get Food](1730-shortest-path-to-get-food.md). Symmetry no longer holds. |
| "Return the path?" | Store each square's parent when you queue it, then walk back from the target. |

**Traps:**

- **No bound at all.** It still finds the answer, but it explores all four quadrants, roughly 4× the work.
- **Bounding at 0.** Wrong answers near the axes: `(1,1)` gives 4 instead of 2.
- **Marking visited on dequeue.** The same square is queued many times.
- **Using DFS.** It doesn't find the shortest path and may never finish on an infinite board.
- **Forgetting `abs`.** The `>= -2` bound then rules out targets in the negative quadrants entirely.

**This same move shows up in:** [Shortest Path to Get Food](1730-shortest-path-to-get-food.md) (grid BFS with four moves instead of eight) · [01 Matrix](542-01-matrix.md) (BFS rings as distances) · [Word Ladder](127-word-ladder.md) (BFS over states, often done bidirectionally) · [Open the Lock](https://leetcode.com/problems/open-the-lock/) (LeetCode 752, BFS over a finite state space).

</details>

---
