# 417. Pacific Atlantic Water Flow

**Medium** · [LeetCode](https://leetcode.com/problems/pacific-atlantic-water-flow/)

[📖 11. Graphs lesson](../learning/11-graphs.md) · [📖 Grids primer](../learning/10b-grids-primer.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 11. Graphs problems](../rmap-practice/11-graphs.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

There is an `m × n` rectangular island bordered by the **Pacific Ocean** (top and left edges) and the **Atlantic Ocean** (bottom and right edges).

`heights[r][c]` is the height above sea level of cell `(r, c)`. Rain water can flow from a cell to a **4-directionally adjacent** cell **only if that neighbour's height is less than or equal** to the current cell's height. Water can flow from any cell adjacent to an ocean into that ocean.

Return a list of coordinates from which water can flow to **both** oceans.

```
heights = [[1,2,2,3,5],
           [3,2,3,4,4],       →  [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]
           [2,4,5,3,1],
           [6,7,1,4,5],
           [5,1,1,2,4]]
```

**Constraints:** `1 <= m, n <= 200` · `0 <= heights[r][c] <= 10⁵`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| Pacific = **top + left**, Atlantic = **bottom + right** | ⚠️ Two different border sets — and corners touch both |
| flow to a neighbour "**less than or equal**" | Water moves downhill or level. `<=`, not `<` |
| "flow to **both** oceans" | The **intersection** of two reachability sets |
| 200 × 200 = 40,000 cells | ⚠️ A per-cell forward search would be O((m·n)²) = 1.6 × 10⁹ — too slow |

**The obvious approach and why it fails.** For each cell, run a search to see whether water reaches the Pacific, and another for the Atlantic. That's a full traversal per cell — **O((m·n)²)**, and at 40,000 cells it's hopeless.

**The reframe: reverse the flow.** Rather than asking *"from this cell, can water reach an ocean?"*, ask the inverse:

> **"From this ocean, which cells could water have come from?"**

Start at the ocean borders and walk **uphill** — moving to a neighbour only if it's **equal or higher**. Every cell you reach is one from which water could flow down to that ocean.

```
forward:   cell → ocean,   moving to LOWER or equal   (m·n searches)
reverse:   ocean → cells,  moving to HIGHER or equal  (2 searches)
```

**Two traversals replace 40,000.** One flood-fill from all Pacific-border cells, one from all Atlantic-border cells, then intersect the two visited sets.

**Why reversing is valid.** "Water flows from A to B" requires `height[B] <= height[A]`. Reversed, "B could have received from A" means `height[A] >= height[B]` — the *same* condition read backwards. So walking uphill from the ocean traces exactly the paths water would take downhill to it.

**That's the transferable idea:** *when a problem asks "which sources reach a target?", it's often far cheaper to search backwards from the target.* The same instinct appears in [Walls and Gates](286-walls-and-gates.md) and multi-source BFS generally.

🤔 **Before you open the next section:** the two searches must not share a visited set. What would go wrong if they did?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| DFS from every cell toward each ocean | Test each cell independently | **O((m·n)²)** | ❌ 1.6 × 10⁹ |
| **Reverse DFS from both ocean borders** | Walk uphill from the edges | **O(m·n)** | ✅ |
| Reverse BFS from both borders | Same idea, queue-based | O(m·n) | ✅ Equally valid |

**The decision: two reverse flood-fills — one per ocean — then intersect.**

Three parts:

1. **Seed from the borders.** Pacific: every cell in row 0 and column 0. Atlantic: every cell in the last row and last column.
2. **Walk uphill.** Recurse into a neighbour only if `heights[neighbor] >= heights[current]` — the reverse of the flow rule.
3. **Intersect.** A cell in both sets can drain to both oceans.

**Why two separate `visited` sets.** They record *different facts* — "reaches the Pacific" versus "reaches the Atlantic". Sharing one set would conflate them, and the intersection step would be meaningless. **Passing the set as a parameter** lets one `dfs` function serve both, which is why the signature takes `visited`.

**Why `prev_height` is passed down.** The uphill check compares the current cell against **where you came from**. Rather than looking backwards, each call receives the previous cell's height as a parameter — the same top-down context-passing as [Count Good Nodes](1448-count-good-nodes-in-binary-tree.md), where the parent's information travels down as an argument.

**Why the border cells seed with their own height.** `dfs(0, col, pacific, heights[0][col])` passes the cell's *own* height, so the check `heights[0][col] >= heights[0][col]` is trivially true and the border cell is always included — which is correct, since a border cell drains directly into its ocean. **A neat way to avoid a special case.**

**This is multi-source flood-fill**, like [Rotting Oranges](994-rotting-oranges.md) — many starting points, one traversal. The difference is that DFS suffices here because the question is *reachability*, not *distance*.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
rows = len(heights)
cols = len(heights[0])
pacific = set()
atlantic = set()
```

**Two separate sets**, recording which cells can drain to each ocean. Keeping them apart is what makes the final intersection meaningful.
→ [set-basics](../syntax/set-basics.md) · [nested-lists](../syntax/nested-lists.md)

```python
def dfs(row, col, visited, prev_height):
    if row < 0 or row >= rows or col < 0 or col >= cols:
        return
```

The function takes **which set to fill** and **the height it came from** — so one implementation serves both oceans.

Standard bounds check first.
→ [function-basics](../syntax/function-basics.md) · [closures](../syntax/closures.md) · [logical-operators](../syntax/logical-operators.md)

```python
    if (row, col) in visited or heights[row][col] < prev_height:
        return
```

**Two stopping conditions:**

- **Already visited** — this cell's reachability is settled; revisiting would loop forever on flat regions.
- **`heights[row][col] < prev_height`** — ⚠️ **the reversed flow rule.** Water flows *downhill*, so tracing backwards means only moving to cells that are **equal or higher**. A lower neighbour couldn't have sent water here.

Note it's `<`, so equal heights **do** pass — matching the problem's "less than or equal" flow rule.
→ [membership-operators](../syntax/membership-operators.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
    visited.add((row, col))
    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        dfs(row + dr, col + dc, visited, heights[row][col])
```

Mark, then explore all four neighbours — **passing this cell's height** as the new `prev_height`, so each neighbour compares against where it came from.

Marking before recursing prevents infinite recursion between equal-height neighbours.
→ [set-operations](../syntax/set-operations.md) · [tuple-unpacking](../syntax/tuple-unpacking.md) · [recursion-basics](../syntax/recursion-basics.md)

```python
for col in range(cols):
    dfs(0, col, pacific, heights[0][col])
    dfs(rows - 1, col, atlantic, heights[rows - 1][col])

for row in range(rows):
    dfs(row, 0, pacific, heights[row][0])
    dfs(row, cols - 1, atlantic, heights[row][cols - 1])
```

**Seed from all four borders.** Top row and left column feed the Pacific; bottom row and right column feed the Atlantic.

Each seed passes the cell's **own** height, making the first comparison trivially true — so border cells are always included without a special case.

Corners are seeded twice (once per loop), which is harmless: the second call finds the cell already in `visited` and returns.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md)

```python
result = []
for row in range(rows):
    for col in range(cols):
        if (row, col) in pacific and (row, col) in atlantic:
            result.append([row, col])
return result
```

**The intersection** — cells reachable from both oceans.

*(Equivalently `[[r, c] for r, c in pacific & atlantic]` using set intersection — shorter, though the explicit scan gives a deterministic order.)*
→ [list-methods](../syntax/list-methods.md) · [set-operations](../syntax/set-operations.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:

        rows = len(heights)
        cols = len(heights[0])
        pacific = set()
        atlantic = set()

        def dfs(row, col, visited, prev_height):
            if row < 0 or row >= rows or col < 0 or col >= cols:
                return
            if (row, col) in visited or heights[row][col] < prev_height:
                return

            visited.add((row, col))
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                dfs(row + dr, col + dc, visited, heights[row][col])

        for col in range(cols):
            dfs(0, col, pacific, heights[0][col])
            dfs(rows - 1, col, atlantic, heights[rows - 1][col])

        for row in range(rows):
            dfs(row, 0, pacific, heights[row][0])
            dfs(row, cols - 1, atlantic, heights[row][cols - 1])

        result = []
        for row in range(rows):
            for col in range(cols):
                if (row, col) in pacific and (row, col) in atlantic:
                    result.append([row, col])
        return result
```

</details>

**Trace it** — a small 3×3 grid:

```
heights:   1  2  3          Pacific borders: row 0, col 0
           8  9  4          Atlantic borders: row 2, col 2
           7  6  5
```

**Pacific flood-fill** (uphill from top row and left column):

| Seed | Reaches |
|---|---|
| (0,0)=1 | (0,0); (0,1)=2 ≥ 1 ✅; (0,2)=3 ≥ 2 ✅; (1,2)=4 ≥ 3 ✅; (2,2)=5 ≥ 4 ✅; (2,1)=6 ≥ 5 ✅; (2,0)=7 ≥ 6 ✅; (1,0)=8 ≥ 7 ✅; (1,1)=9 ≥ 8 ✅ |

The whole grid — it's a spiral of increasing heights, so from (0,0) everything is uphill.

**Atlantic flood-fill** (uphill from bottom row and right column):

| Seed | Reaches |
|---|---|
| (2,0)=7 | (2,0); (1,0)=8 ≥ 7 ✅; (1,1)=9 ≥ 8 ✅ |
| (2,1)=6, (2,2)=5 | themselves, plus upward where higher |
| (0,2)=3, (1,2)=4 | themselves |

Atlantic reaches everything too, via the increasing spiral.

**Intersection:** all 9 cells ✅ — correct, since this grid's monotone spiral lets every cell drain both ways.

**A clearer contrast** — the LeetCode example's cell `(0,0)` has height 1 with neighbours 2 and 3, both higher. It's on the Pacific border (so trivially Pacific-reachable) but water can't climb to reach the Atlantic, so it's **excluded** from the answer. That's why `[0,0]` doesn't appear in the expected output.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(m · n)</summary>

**O(m · n)**.

| Step | Cost |
|---|---|
| Pacific flood-fill | each cell visited at most once → O(m·n) |
| Atlantic flood-fill | O(m·n) |
| Final intersection scan | O(m·n) |

Three linear passes → **O(m·n)**.

Each cell is added to a given `visited` set once, and every later attempt to reach it returns immediately. A cell can be reached from up to 4 neighbours, so the constant is small.

At 200 × 200 = 40,000 cells, that's ~10⁵ operations. Instant.

**Versus the forward approach: O((m·n)²).** Testing each cell separately means a full traversal per cell — 40,000 traversals of 40,000 cells = **1.6 × 10⁹**. Reversing the direction turns 40,000 searches into **2**.

**That's the entire win, and it's worth stating plainly:** the problem has many sources and two targets, so searching from the targets is 20,000× cheaper than searching from the sources.

**DFS is fine here because the question is reachability, not distance** — unlike [Rotting Oranges](994-rotting-oranges.md), where BFS was required. Both DFS and BFS give O(m·n).

</details>

<details>
<summary><b>5 · Space complexity</b> — O(m · n)</summary>

**O(m · n)**.

| Component | Size |
|---|---|
| `pacific` set | up to every cell → **O(m·n)** |
| `atlantic` set | **O(m·n)** |
| Recursion stack | up to m·n frames on a monotone grid → **O(m·n)** |
| `result` | required output, up to O(m·n) |

⚠️ **The recursion depth is a genuine risk at these constraints.** A grid with monotonically increasing heights makes the DFS traverse all 40,000 cells in one chain — **far past Python's default limit of 1000**, raising `RecursionError`.

**BFS avoids it**, using a queue bounded by the frontier:

```python
from collections import deque
def bfs(starts, visited):
    queue = deque(starts)
    visited.update(starts)
    while queue:
        r, c = queue.popleft()
        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols
                    and (nr, nc) not in visited
                    and heights[nr][nc] >= heights[r][c]):
                visited.add((nr, nc))
                queue.append((nr, nc))
```

**On a 200×200 grid, BFS is the safer implementation** — worth saying, since the recursion limit is reachable with the given constraints rather than hypothetical.

**Both sets are needed.** They record different facts, and the answer is their intersection — so neither can be dropped or merged.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The naive approach runs a search from every cell to see if it reaches each ocean — that's O((m·n)²), about 1.6 billion operations at these constraints. The key move is to reverse the question: instead of 'can water get from this cell to the ocean?', ask 'which cells could have sent water to this ocean?' So I flood-fill inward from the ocean borders, walking *uphill* — moving to a neighbour only if it's equal or higher, which is the flow rule read backwards. That replaces 40,000 searches with two. I keep separate visited sets for the two oceans, since they record different facts, and the answer is their intersection. I pass the previous cell's height down as a parameter so each step compares against where it came from, and I seed border cells with their own height so they're trivially included. O(m·n) time and space — though at 200×200 I'd use BFS, since a monotone grid would blow the recursion limit."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why search backwards from the oceans?" | **The question.** Many sources, two targets — so searching from the targets is two traversals instead of m·n. |
| "Why is walking uphill correct?" | "A flows to B" means `height[B] <= height[A]`. Reversed, "B received from A" means `height[A] >= height[B]` — the same condition. |
| "Why two separate visited sets?" | They record different facts. Sharing one would conflate the oceans and make the intersection meaningless. |
| "What if the grid is 200×200 and monotone?" | The DFS recursion hits 40,000 frames, past Python's limit. Use BFS. |
| "Why `>=` and not `>`?" | The flow rule is "less than **or equal**", so water moves across level ground — and the reverse must allow it too. |
| "Could you use one DFS pass?" | No — the two reachability sets are independent, so they need separate traversals. |
| "What if there were three oceans?" | Three sets, three flood-fills, and intersect all three. The approach scales. |

**Traps:**

- **Searching forward from every cell** — correct but O((m·n)²).
- **Using `>` instead of `>=`** in the uphill check — water can't cross flat regions and cells are wrongly excluded.
- **Sharing one `visited` set** between the two oceans — the intersection becomes meaningless.
- **Seeding border cells with a sentinel** like `-1` or `0` instead of their own height. It usually works, but passing the cell's own height is clearer and provably correct.
- **Forgetting to mark before recursing** — infinite recursion across equal-height neighbours.
- **Comparing against the *ocean* rather than the previous cell** — the check is local, between adjacent cells.

**This same move shows up in:** [Surrounded Regions](130-surrounded-regions.md) (flood-fill inward from the borders to identify what's *safe*) · [Rotting Oranges](994-rotting-oranges.md) (multi-source traversal) · [Number of Islands](200-number-of-islands.md) (the grid flood-fill skeleton) · [Count Good Nodes](1448-count-good-nodes-in-binary-tree.md) (passing context down as a parameter) · [grids primer](../learning/10b-grids-primer.md).

</details>
