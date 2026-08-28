# 733. Flood Fill

**Easy** · [LeetCode](https://leetcode.com/problems/flood-fill/) · [Solution file (no hints)](../../problems/0500-0999/733.py)

[📖 11. Graphs lesson](../learning/11-graphs.md) · [📖 Grids primer](../learning/10b-grids-primer.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 11. Graphs problems](../rmap-practice/11-graphs.md)

---

Starting at pixel `(sr, sc)` in `image`, repaint it and every **4-directionally connected** pixel of the **same original colour** with `color`. Return the modified image.

```
image = [[1,1,1],          sr=1, sc=1, color=2      [[2,2,2],
         [1,1,0],                          →        [2,2,0],
         [1,0,1]]                                   [2,0,1]]

The bottom-right 1 is NOT repainted — it's not connected to the start.
```

**Constraints:** `1 <= m, n <= 50` · `0 <= image[i][j], color < 2^16`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**directly adjacent**, horizontally or vertically" | 4 directions, not 8. No diagonals |
| "shares the **same colour** as the starting pixel" | ⚠️ Compare against the **original** colour, captured *before* you overwrite anything |
| "keep repeating… until no more" | A connected-component traversal — DFS or BFS |
| "the bottom corner is not coloured" | Connectivity is the whole point: same colour ≠ same region |
| Example 2: `color` already equals the start | ⚠️ **The trap.** Guard this or you loop forever |
| `m, n <= 50` | 2,500 cells. Recursion depth is fine |

**This is the grid-traversal template**, the same one behind [Number of Islands](200-number-of-islands.md) and [Max Area of Island](695-max-area-of-island.md). If you've done those, you have this — the only differences are what counts as "part of the region" and what you do on arrival.

```
                    marker for "visited"        what you do at each cell
Number of Islands   overwrite '1' → '0'         count components
Max Area of Island  overwrite 1 → 0             sum cells
Flood Fill          overwrite old → new         (the overwrite IS the task)
```

**The elegant part:** repainting a pixel *is* marking it visited. Because the new colour differs from the old one, an already-repainted pixel automatically fails the `== old_color` test. **No `visited` set is needed** — the image itself carries that state.

**Which is exactly why example 2 breaks it.** If `color == old_color`, repainting changes nothing, so the "visited" mark is invisible:

```
image = [[0,0,0],[0,0,0]], start (0,0), color = 0

paint (0,0) with 0  →  still 0  →  looks unvisited
visit (0,1), which comes back to (0,0), which still matches...
                                        ↳ infinite recursion 💥
```

The problem hands you this case as Example 2 — a deliberate hint. One guard fixes it:

```python
if old_color == color:
    return image
```

🤔 **Before you open the next section:** if you captured `old_color` *after* painting the first pixel instead of before, what would the algorithm do?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| **DFS (recursive)** | Recurse into the 4 neighbours | **O(m·n)** | ✅ Shortest to write |
| BFS (queue) | Expand ring by ring | O(m·n) | ✅ Same cost; O(m·n) queue, no stack limit |
| DFS with explicit stack | Iterative | O(m·n) | ✅ When recursion depth is a worry |
| Union-Find | Group same-colour cells, repaint the start's group | O(m·n·α) | ❌ Massive overkill |

**The decision: recursive DFS**, with the equal-colour guard.

**DFS vs BFS is a genuine toss-up here** — unlike [Rotting Oranges](994-rotting-oranges.md) or [Walls and Gates](286-walls-and-gates.md), where BFS is *required* because the answer is a shortest distance. Flood fill just needs to touch every cell in the component; the order is irrelevant. Pick DFS because it's four lines shorter.

**The one thing worth checking: recursion depth.** A 50×50 grid that's entirely one colour makes a component of 2,500 cells, and DFS can go 2,500 frames deep — under Python's default limit of 1,000? **No.** In the worst case it exceeds it.

In practice the recursion follows a snake-like path and CPython usually survives LeetCode's tests, but **it's the honest thing to raise**: *"At 50×50 the component can be 2,500 cells, so worst-case depth exceeds Python's default recursion limit — I'd use BFS or an explicit stack if that's a concern."* Knowing the limit exists is the point.
→ [recursion-limit](../syntax/recursion-limit.md)

**The structure, against its neighbours:**

| | [Number of Islands](200-number-of-islands.md) | **Flood Fill** | [Surrounded Regions](130-surrounded-regions.md) |
|---|---|---|---|
| What defines the region | cells equal to `'1'` | **cells equal to `old_color`** | cells equal to `'O'` |
| Visited marker | overwrite with `'0'` | **overwrite with `color`** | overwrite with `'T'` |
| Where the search starts | every unvisited land cell | **one given pixel** | border cells only |
| Answer | component count | **the mutated grid** | the mutated grid |

**Why the guards go at the top of the recursion, not before the call.** Two styles work:

```python
# A: check inside (used here)          # B: check before recursing
def dfs(r, c):                          for dr, dc in dirs:
    if out of bounds: return                nr, nc = r+dr, c+dc
    if wrong colour:  return                if in bounds and right colour:
    paint; recurse 4 ways                       dfs(nr, nc)
```

**A is easier to get right** — one place to validate instead of four, and the bounds check can't be forgotten on one of the four calls. It costs a few extra function calls that immediately return; irrelevant here.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
old_color = image[sr][sc]

if old_color == color:
    return image
```

**Capture the original colour first**, then the guard that prevents infinite recursion.

⚠️ **Order matters.** Read `old_color` *before* painting anything — once the first pixel is overwritten, the value that defines the region is gone.

The guard handles Example 2: if the target colour is already the current one, there's nothing to do, and proceeding would recurse forever because repainting wouldn't mark anything as visited.
→ [nested-lists](../syntax/nested-lists.md) · [if-return](../syntax/if-return.md)

```python
rows = len(image)
cols = len(image[0])
```

Dimensions hoisted out so the recursion doesn't recompute them. `len(image[0])` is safe — the constraints guarantee at least one row and one column.
→ [list-basics](../syntax/list-basics.md)

```python
def dfs(r, c):
    if r < 0 or r >= rows or c < 0 or c >= cols:
        return
```

**Bounds check first.** Must come before touching `image[r][c]`, or you'd index out of range.

⚠️ Python's negative indexing makes this critical: `image[-1][0]` doesn't raise, it silently reads the **last row**. Without `r < 0`, the fill would wrap around the grid and quietly produce wrong output. **Missing bounds checks in grid problems fail silently rather than crashing** — that's what makes them dangerous.
→ [comparison-operators](../syntax/comparison-operators.md) · [logical-operators](../syntax/logical-operators.md)

```python
    if image[r][c] != old_color:
        return
```

**The one condition that does three jobs:**

| It rejects | Because |
|---|---|
| Cells of a different colour | Not part of this region |
| Cells already repainted | They now hold `color`, not `old_color` |
| Re-entry from a neighbour | Same reason — the paint *is* the visited mark |

This is why no `visited` set appears anywhere. **And why the equal-colour guard above is mandatory** — it's the one case where the second job silently stops working.

```python
    image[r][c] = color
```

**Paint it.** Simultaneously the task and the visited-marking.

```python
    dfs(r + 1, c)
    dfs(r - 1, c)
    dfs(r, c + 1)
    dfs(r, c - 1)
```

**All four neighbours**, no bounds checking here — the callee's first line handles it.
→ [recursion-basics](../syntax/recursion-basics.md)

```python
dfs(sr, sc)
return image
```

One call from the start pixel; the whole component follows.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def floodFill(self, image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:

        old_color = image[sr][sc]

        if old_color == color:
            return image

        rows = len(image)
        cols = len(image[0])

        def dfs(r, c):
            if r < 0 or r >= rows or c < 0 or c >= cols:
                return

            if image[r][c] != old_color:
                return

            image[r][c] = color
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)

        dfs(sr, sc)
        return image
```

</details>

**Trace it** — `image = [[1,1,1],[1,1,0],[1,0,1]]`, start `(1,1)`, `color = 2`. `old_color = 1`:

| Step | Call | Check | Grid after |
|---|---|---|---|
| 1 | `dfs(1,1)` | is 1 ✓ paint | `[[1,1,1],[1,2,0],[1,0,1]]` |
| 2 | `dfs(2,1)` | is 0 ✗ | — |
| 3 | `dfs(0,1)` | is 1 ✓ paint | `[[1,2,1],[1,2,0],[1,0,1]]` |
| 4 | ↳ `dfs(-1,1)` | **out of bounds** ✗ | — |
| 5 | ↳ `dfs(0,2)` | is 1 ✓ paint | `[[1,2,2],[1,2,0],[1,0,1]]` |
| 6 | ↳↳ `dfs(1,2)` | is 0 ✗ | — |
| 7 | ↳ `dfs(0,0)` | is 1 ✓ paint | `[[2,2,2],[1,2,0],[1,0,1]]` |
| 8 | ↳↳ `dfs(1,0)` | is 1 ✓ paint | `[[2,2,2],[2,2,0],[1,0,1]]` |
| 9 | ↳↳↳ `dfs(2,0)` | is 1 ✓ paint | `[[2,2,2],[2,2,0],[2,0,1]]` |
| 10 | ↳↳↳↳ `dfs(2,1)` | is 0 ✗ | — |
| 11 | `dfs(1,0)` again | is **2** now ✗ | — |

**Result: `[[2,2,2],[2,2,0],[2,0,1]]`** ✅

**Step 11 is the mechanism.** `(1,0)` is reached a second time from a different neighbour — and rejected, because it's already been painted 2 and no longer equals `old_color`. That's the visited check, for free.

**The bottom-right `1` at `(2,2)`** is never reached: every route to it passes through a `0`. Same colour, different component — exactly the distinction the problem is testing.

**Step 4 shows why bounds come first.** `dfs(-1, 1)` would otherwise read `image[-1][1]` = the last row's middle cell = `0`. Here that happens to be rejected anyway — but flip that cell to a `1` and the fill would leak across the grid with no error.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(m · n)</summary>

**O(m · n)** — at most every cell is visited once.

- Each cell is painted **at most once**: after painting, it fails `== old_color` forever.
- Each painted cell makes 4 recursive calls, each O(1) to reject or O(1) to accept.
- So total work is bounded by 4 × (number of cells) = **O(m·n)**.

At 50×50 that's 2,500 cells and ≤10,000 calls — instant.

**Why it isn't O(4^(m·n))**, the usual worry with 4-way recursion: the paint marks each cell permanently, so the recursion tree can't revisit. **Without the marking it would be exponential** — the marking is what makes it linear, and that's the sentence to say.

**Best case is O(1)**: the equal-colour guard returns immediately, and a start pixel with no same-colour neighbours paints one cell.

**BFS is identical** — O(m·n), same reasoning. The choice is about stack depth, not speed.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(m · n) worst case</summary>

**O(m · n)** in the worst case, from the **recursion stack**.

| Component | Size |
|---|---|
| **Recursion depth** | as deep as the component is long → **O(m·n)** worst case |
| `visited` structure | **none** — the image is the marker → **O(1)** |
| Output | the input, mutated in place → **O(1)** extra |

**The worst case is a single-colour grid**: one component of m·n cells, and DFS can nest that deep.

⚠️ **At 50×50 that's up to 2,500 frames, above Python's default limit of 1,000.** The recursion typically snakes rather than nesting maximally, so it usually passes — but this is a real answer to "what breaks at scale?", and BFS or an explicit stack removes the concern:

| Approach | Extra space | Depth risk |
|---|---|---|
| Recursive DFS | O(m·n) stack | ⚠️ Yes |
| BFS with a queue | O(m·n) queue | ✅ None |
| Iterative DFS | O(m·n) stack (heap-allocated) | ✅ None |

All three are O(m·n); only the recursive one risks a `RecursionError`. **Same asymptotic space, different failure mode** — worth naming.
→ [recursion-limit](../syntax/recursion-limit.md) · [deque-basics](../syntax/deque-basics.md)

**No auxiliary `visited` set** is the space win here, and it's specific to problems where you're allowed to mutate the input. [Number of Islands](200-number-of-islands.md) uses the same trick; when mutation isn't allowed, you pay O(m·n) for a `visited` set.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "This is a connected-component traversal on a grid. I capture the starting pixel's colour first, because that's what defines the region and it's destroyed the moment I paint. Then DFS in four directions, recursing only into cells that still hold the original colour. The neat part is that repainting doubles as the visited mark — a repainted cell no longer matches `old_color`, so I don't need a separate visited set. The one case that breaks is when the new colour equals the old one: painting then marks nothing and the recursion never terminates, so I guard that up front and return immediately. It's O(m·n) time since each cell is painted at most once, and O(m·n) worst-case stack depth — at 50×50 that can exceed Python's recursion limit, so I'd switch to BFS or an explicit stack if that mattered."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "What if `color == old_color`?" | **The question.** Infinite recursion — painting no longer marks anything visited. Guard and return early. |
| "Why no `visited` set?" | The repaint *is* the mark. Only valid because the new colour differs from the old — which is exactly what the guard ensures. |
| "DFS or BFS?" | Either; both O(m·n). BFS avoids the stack-depth risk. Unlike [Rotting Oranges](994-rotting-oranges.md), there's no shortest-path requirement forcing BFS. |
| "Stack overflow?" | Worst case 2,500 frames at 50×50, over Python's 1,000 default. Use BFS or an explicit stack. |
| "8-directional fill?" | Add the four diagonals to the direction list. Everything else is unchanged. |
| "Can't mutate the input?" | Copy it, or keep a separate `visited` set — O(m·n) extra either way. |
| "Why does `(2,2)` keep its colour?" | It's the same colour but a different component; every path to it crosses a `0`. Connectivity, not colour, defines the region. |
| "A tolerance-based fill, like a real paint bucket?" | Compare `abs(pixel - old) <= tolerance`. ⚠️ Then you **do** need a `visited` set — a cell within tolerance of itself stays within tolerance after painting, so the mark stops working. |
| "Very large images?" | Scanline flood fill — fill whole horizontal runs at once, pushing only the runs above and below. Far fewer stack frames. |

**Traps:**

- **Not guarding `old_color == color`.** Infinite recursion, and the problem *hands* you this as Example 2. The defining bug.
- **Reading `old_color` after painting the start pixel** — it would then equal `color` and nothing else would match.
- **Omitting the `r < 0` / `c < 0` checks.** Python's negative indexing wraps instead of raising, so the fill leaks to the opposite edge **with no error**. Silent wrong answers.
- **Checking bounds after indexing** — `if image[r][c] != old_color` before the bounds test raises `IndexError` on the high side, wraps on the low side.
- **Adding diagonals** — the problem says horizontal/vertical only.
- **Building a `visited` set anyway** — harmless, just redundant given the repaint.
- **Returning `None`** — the signature returns the image; mutating in place isn't enough.

**This same move shows up in:** [Number of Islands](200-number-of-islands.md) (the same overwrite-as-visited trick) · [Max Area of Island](695-max-area-of-island.md) (identical traversal, summing instead of painting) · [Surrounded Regions](130-surrounded-regions.md) and [Number of Enclaves](1020-number-of-enclaves.md) (flood fill seeded from the border) · [Island Perimeter](463-island-perimeter.md) (same grid, no traversal needed) · [dfs](../algorithms/dfs.md) · [graph](../data-structures/graph.md).

</details>

---
