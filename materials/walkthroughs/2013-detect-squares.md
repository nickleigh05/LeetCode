# 2013. Detect Squares

**Medium** · [LeetCode](https://leetcode.com/problems/detect-squares/)

[📖 17. Math & Geometry lesson](../learning/19-math-geometry.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 17. Math & Geometry problems](../rmap-practice/17-math-geometry.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Design a data structure that stores 2-D points and counts **axis-aligned squares**.

- **`add(point)`** — add a point to the structure. **Duplicate points are allowed** and stored separately.
- **`count(point)`** — given a query point, return the number of ways to pick **three** points from the structure that, together with the query point, form an axis-aligned square with **positive area**.

```
ds = DetectSquares()
ds.add([3,10]); ds.add([11,2]); ds.add([3,2])

ds.count([11,10])  →  1     the square (3,10) (11,10) (11,2) (3,2)
ds.count([14,8])   →  0     no square possible

ds.add([11,2])              a second copy of (11,2)
ds.count([11,10])  →  2     two copies of one corner → two distinct squares
```

**Constraints:** `point.length == 2` · `0 <= x, y <= 1000` · at most **3000** calls total to `add` and `count`.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| **axis-aligned** squares | Enormous simplification. Sides are parallel to the axes, so corners share x- or y-coordinates exactly — no rotation, no diagonal geometry |
| duplicates are **stored separately** | You need **counts**, not a set. Two copies of a corner produce two distinct squares |
| "**positive area**" | Degenerate zero-side "squares" don't count, so the case where the query point equals a candidate corner must be excluded |
| pick **three** points to join the query | The query point is a fixed corner; you're choosing the other three |
| ≤ 3000 total calls | So an O(n) `count` is fine — 3000 × 3000 = 9 × 10⁶ worst case |

The naive `count` would try every combination of three stored points — O(n³), around 2.7 × 10¹⁰ at the limits. Hopeless.

**The structural insight is that an axis-aligned square is determined by two of its corners** — specifically, by a **diagonal pair**. Fix the query point at `(x, y)` and pick any other point `(x2, y2)` as the **opposite** corner of the diagonal. For the four points to form an axis-aligned square:

- The side length is `|x2 - x|`, which must equal `|y2 - y|` — otherwise it's a rectangle, not a square.
- The other two corners are then forced: **`(x, y2)` and `(x2, y)`**.

So each candidate diagonal partner determines the entire square, and you just check whether the two remaining corners exist.

**But this implementation takes a slightly different route**, and it's worth understanding why. Instead of scanning for diagonal partners, it scans for points **sharing the query's x-coordinate** — points `(x, py)` directly above or below the query.

Each such point gives a **vertical side** of length `side = py - y`. The square must then extend horizontally by that same amount, either left or right, giving two candidates:

- corners `(x + side, y)` and `(x + side, py)`, or
- corners `(x - side, y)` and `(x - side, py)`.

**Why scan the vertical side rather than the diagonal?** Because it makes the side length explicit and the two remaining corners trivially derivable — no need to check `|dx| == |dy|`, since the horizontal offset is *constructed* to equal the vertical one. **The square-ness is guaranteed by construction rather than verified by a test.**

🤔 **Before you open the next section:** the count for each candidate square is a **product** of three counts, not a sum or a check for existence. Why multiplication — and what does it represent?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time per `count` | Space | Verdict |
|---|---|---|---|---|
| Try every triple of points | Check all C(n,3) combinations | **O(n³)** | O(n) | ❌ 2.7 × 10¹⁰ |
| Try every pair as the diagonal | For each stored point, test if it's a valid diagonal partner | O(n) | O(n) | ✅ Correct — the other standard solution |
| Grid of booleans over the coordinate space | A 1001 × 1001 occupancy grid | O(n) | O(10⁶) | ⚠️ Works given the coordinate bound, but wastes space and loses duplicate counts |
| **Hash map of point → count, scan for a shared x** | Find vertical sides, derive the other two corners | **O(n)** | **O(n)** | ✅ |

**The decision:** a **[hash map](../data-structures/hashmap.md) from point to count**, scanned for points sharing the query's x-coordinate.

**Why a map of counts rather than a set.** Duplicates matter: adding `(11,2)` twice must double the squares that use that corner. A set would collapse them and undercount. **The multiplicity is part of the answer**, which is what makes `defaultdict(int)` the right structure rather than a `set`.

**Why multiplication, not addition** — the answer to section 1's question. This is the crux of the problem.

If a square needs corners A, B, C (plus the query point), and the structure holds **2 copies of A, 3 of B, and 1 of C**, then the number of *distinct* squares is `2 × 3 × 1 = 6` — every choice of which A pairs with which B pairs with which C is a different square, since the points are stored as separate entities.

**That's the multiplication rule for independent choices**, and it's the reason `count` returns a product per candidate and sums those products across candidates. Getting this wrong — checking mere existence and adding 1 — silently undercounts on any input with duplicates, which is exactly what the problem's third example tests.

**Why the query point's own multiplicity isn't included.** The query point is *given*, not chosen from the structure — you're picking three points to join it. So its stored count (if any) doesn't multiply in.

**Why `add` is O(1) and `count` is O(n).** The problem gives ≤ 3000 total calls, so even if all were `count` on 3000 points, that's 9 × 10⁶ operations. **Making `add` fast and `count` linear is the right split** — the alternative (precomputing all squares on `add`) would make `add` expensive and gain nothing.

**Why not the coordinate grid?** Coordinates are bounded by 1000, so a 1001 × 1001 array is feasible. But it's 10⁶ cells for at most 3000 points, and you'd still need counts rather than booleans. The hash map scales with what's actually stored.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
from collections import defaultdict

class DetectSquares:

    def __init__(self):
        self.point_count = defaultdict(int)
```
**The single piece of state: a map from point to how many copies exist.**

[`defaultdict(int)`](../syntax/defaultdict.md) returns **0** for any unseen key, which is exactly what's wanted — a missing corner contributes 0 to the product, and the multiplication handles it with no membership check anywhere.

That's a real simplification: without it, every corner lookup below would need an `if point in ...` guard.
→ [defaultdict](../syntax/defaultdict.md) · [hashmap](../data-structures/hashmap.md) · [init-method](../syntax/init-method.md) · [class-basics](../syntax/class-basics.md)

```python
    def add(self, point: List[int]) -> None:
        self.point_count[tuple(point)] += 1
```
**O(1) insertion**, incrementing rather than setting so duplicates accumulate.

`tuple(point)` converts the input list to a tuple because **lists are unhashable** in Python and can't be dict keys — tuples are immutable and therefore hashable. This is a small but mandatory conversion.
→ [tuple-basics](../syntax/tuple-basics.md) · [dict-basics](../syntax/dict-basics.md) · [type-conversion](../syntax/type-conversion.md)

```python
    def count(self, point: List[int]) -> int:
        x, y = point
        total = 0
```
Unpack the query coordinates and start the accumulator.
→ [tuple-unpacking](../syntax/tuple-unpacking.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
        for (px, py), cnt in list(self.point_count.items()):
```
**Scan every distinct stored point**, unpacking the coordinate tuple and its multiplicity in one step.

The `list(...)` wrapper takes a snapshot of the items. It isn't strictly required here — nothing mutates the dict during iteration — but reading `self.point_count[(x2, y)]` inside the loop **would insert missing keys** thanks to `defaultdict`'s behaviour, and mutating a dict while iterating it raises `RuntimeError`. **The snapshot makes that safe**, which is a genuine subtlety of combining `defaultdict` with iteration.
→ [dict-methods](../syntax/dict-methods.md) · [tuple-unpacking](../syntax/tuple-unpacking.md) · [for-loop](../syntax/for-loop.md)

```python
            if px != x or py == y:
                continue
```
**Keep only the points that form a valid vertical side with the query.**

Two conditions, both rejections:
- **`px != x`** — the point must share the query's x-coordinate to be directly above or below it.
- **`py == y`** — it must not be the query point's own row, or the side length would be **zero**. That's the "positive area" requirement: a degenerate square isn't a square.

Written as a rejection with [`continue`](../syntax/break-continue.md) rather than a positive test, which keeps the main body unindented.
→ [break-continue](../syntax/break-continue.md) · [logical-operators](../syntax/logical-operators.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
            side = py - y
```
**The side length**, as a *signed* difference. The sign doesn't matter because both directions are tried next — `x + side` and `x - side` cover left and right regardless of whether `side` is positive or negative.
→ [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
            for x2 in (x + side, x - side):
                total += cnt * self.point_count[(x2, y)] * self.point_count[(x2, py)]
```
**The two candidate squares, and the multiplication rule.**

For each horizontal direction, the square's other two corners are `(x2, y)` — level with the query — and `(x2, py)` — level with the vertical partner. Both are **forced** by the geometry; nothing needs checking beyond whether they exist.

The product `cnt × count[(x2,y)] × count[(x2,py)]` counts every combination of copies:
- `cnt` copies of the vertical partner,
- times the copies of the third corner,
- times the copies of the fourth.

**Each combination is a distinct square**, which is why this is a product rather than an existence check. And if any corner is missing, `defaultdict` returns 0 and the whole term vanishes — **no conditional required**.

Iterating over the tuple `(x + side, x - side)` handles both directions without duplicating the line.
→ [defaultdict](../syntax/defaultdict.md) · [arithmetic-operators](../syntax/arithmetic-operators.md) · [tuple-basics](../syntax/tuple-basics.md)

```python
        return total
```
Summed across every vertical partner and both horizontal directions.
→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
from collections import defaultdict

class DetectSquares:

    def __init__(self):
        self.point_count = defaultdict(int)

    def add(self, point: List[int]) -> None:
        self.point_count[tuple(point)] += 1

    def count(self, point: List[int]) -> int:
        x, y = point
        total = 0

        for (px, py), cnt in list(self.point_count.items()):
            if px != x or py == y:
                continue

            side = py - y
            for x2 in (x + side, x - side):
                total += cnt * self.point_count[(x2, y)] * self.point_count[(x2, py)]

        return total
```
</details>

**Trace it** — the example sequence

After `add([3,10])`, `add([11,2])`, `add([3,2])`:

```
point_count = {(3,10): 1, (11,2): 1, (3,2): 1}
```

**`count([11, 10])`** — query at `x = 11`, `y = 10`:

| stored point | `px == 11`? | `py == 10`? | verdict |
|---|---|---|---|
| `(3,10)` | 3 ≠ 11 ✗ | — | **skip** |
| `(11,2)` | ✓ | 2 ≠ 10 ✓ | **use it** |
| `(3,2)` | 3 ≠ 11 ✗ | — | **skip** |

Only `(11,2)` qualifies. `side = 2 - 10 = -8`.

| `x2` | corner `(x2, y)` = `(x2, 10)` | corner `(x2, py)` = `(x2, 2)` | product |
|---|---|---|---|
| `11 + (−8)` = **3** | `(3,10)` → count **1** | `(3,2)` → count **1** | 1 × 1 × 1 = **1** |
| `11 − (−8)` = **19** | `(19,10)` → count 0 | `(19,2)` → count 0 | 1 × 0 × 0 = 0 |

Return **1** ✅ — the square with corners (3,10), (11,10), (11,2), (3,2).

**`count([14, 8])`** — query at `x = 14`, `y = 8`. No stored point has `px == 14`, so every iteration skips. Return **0** ✅

**Now `add([11,2])` again:**

```
point_count = {(3,10): 1, (11,2): 2, (3,2): 1}
```

**`count([11, 10])`** again:

| `x2` | `(x2, 10)` | `(x2, 2)` | `cnt` | product |
|---|---|---|---|---|
| 3 | `(3,10)` → 1 | `(3,2)` → 1 | **2** | 2 × 1 × 1 = **2** |
| 19 | 0 | 0 | 2 | 0 |

Return **2** ✅

**This is the case that proves the multiplication rule.** Geometrically there's only one square, but `(11,2)` exists twice, so there are **two distinct ways** to choose the corner — and the problem counts them separately. An existence check would have returned 1.

**And a duplicate-heavy case.** Suppose the structure held `(3,10) × 2`, `(11,2) × 3`, `(3,2) × 1`, and you query `(11,10)`:

- Vertical partner `(11,2)` with `cnt = 3`
- `side = -8`, `x2 = 3`
- Product: `3 × count[(3,10)] × count[(3,2)]` = `3 × 2 × 1` = **6**

Six distinct squares from a single geometric shape — three choices for one corner, times two for another. **The product is doing exactly the combinatorial counting the problem asks for.**

</details>

<details>
<summary><b>4 · Time complexity</b> — `add` O(1), `count` O(n)</summary>

**`add` — O(1).** One tuple construction and one hash-map increment, both constant time on average.

**`count` — O(n)**, where n is the number of **distinct** points stored.

- The loop iterates every distinct point → **n iterations**.
- Each iteration does two comparisons, a subtraction, and — for qualifying points — **four hash lookups** and a few multiplications, all **O(1)** average.
- Total: **O(n)**.

With ≤ 3000 total calls, the worst case is roughly 1500 `add`s followed by 1500 `count`s, each scanning 1500 points → about **2 × 10⁶** operations. Comfortable.

**Against the alternatives:** checking every triple is **O(n³)** ≈ 2.7 × 10¹⁰ per call. Choosing every *pair* as a diagonal is also O(n) and equally good — the two approaches differ in framing, not complexity.

**Could `count` be faster?** You could bucket points by x-coordinate — a map from x to a list of y-values — so the scan only visits points actually sharing the query's x, rather than all n. That's **O(k)** where k is the number of points in that column, which is much better when points are spread out and identical in the worst case (all points in one column). **Same worst case, much better average**, and worth naming as the natural optimization.

**Why not precompute squares on `add`?** Each new point could form squares with many existing pairs, so `add` would become O(n²) — trading a cheap operation for an expensive one with no benefit given the call budget.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** — one hash-map entry per **distinct** point, regardless of how many duplicates each holds.

| Component | Space | Why |
|---|---|---|
| `point_count` | **O(n)** | One key per distinct point; duplicates only increment a counter |
| `list(self.point_count.items())` | **O(n)** | A transient snapshot per `count` call |
| Loop scalars | O(1) | Coordinates and accumulators |

With ≤ 3000 `add` calls there are at most 3000 distinct points. Trivial.

**The duplicate handling is a genuine space win:** storing `(11,2)` a thousand times costs **one** entry with a count of 1000, not a thousand entries. That's the difference between a counting map and a list of points.

**Against the coordinate-grid alternative:** a 1001 × 1001 array is **O(10⁶)** cells — fixed, regardless of how few points exist. For 3000 points that's 300× more memory than the hash map, and you'd need ints rather than booleans anyway to track duplicates. **The hash map scales with the data, not the coordinate space.**

**On the `list(...)` snapshot:** it allocates O(n) per `count` call. You could avoid it by iterating `self.point_count.items()` directly *if* you were careful never to touch a missing key inside the loop — but `defaultdict` inserts on read, so `self.point_count[(x2, y)]` on an absent corner would mutate the dict mid-iteration and raise `RuntimeError`. **Using `.get(key, 0)` instead would avoid both the insertion and the snapshot**, which is the cleaner fix if the allocation mattered.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The squares are axis-aligned, which is the big simplification — corners share coordinates exactly, so no rotation to handle. Checking every triple would be O(n³), but a square is fully determined by two corners. I fix the query point and scan for stored points sharing its x-coordinate; each one gives me a vertical side, and the side length forces the other two corners to be at `x ± side`. So I look those up and, if they exist, I've found a square. The important detail is that I **multiply** the three corner counts rather than checking existence — duplicates are stored separately, so two copies of a corner mean two distinct squares. I skip any point at the same y as the query, since that would be a zero-length side and the problem requires positive area. I use a defaultdict so missing corners return 0 and the product vanishes with no conditional. `add` is O(1), `count` is O(n) — and I could bucket by x-coordinate to make the common case much faster."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why multiply the counts instead of checking existence?" | Duplicates are separate points. With 2 copies of one corner and 3 of another, there are 2 × 3 = 6 distinct squares. Existence-checking would report 1. |
| "Why exclude `py == y`?" | That's the query point's own row, giving a side length of 0 — a degenerate square with no area, which the problem excludes. |
| "Why a map instead of a set?" | Duplicates must be counted, not deduplicated. A set would undercount every square using a repeated corner. |
| "Can `count` be faster?" | Bucket points by x-coordinate — a map from x to the y-values in that column. Then the scan visits only points in the query's column, O(k) instead of O(n). Same worst case, far better typically. |
| "Why not precompute squares on `add`?" | Each new point can form squares with many existing pairs, making `add` O(n²). The call budget makes a cheap `add` and linear `count` the better split. |
| "What if the squares could be rotated?" | Much harder — you'd iterate over pairs as diagonals and compute the other two corners by rotating the diagonal vector 90°, which requires the midpoint and perpendicular offset. Corners may land on non-integer coordinates. |
| "Why `tuple(point)` and not the list?" | Lists are unhashable in Python, so they can't be dict keys. Tuples are immutable and hashable. |
| "Why the `list(...)` around `.items()`?" | `defaultdict` inserts missing keys on read, so looking up an absent corner inside the loop would mutate the dict mid-iteration and raise. Using `.get(key, 0)` would avoid both issues. |

**Traps:**
- **Adding 1 per square found instead of multiplying counts.** The defining bug — it passes every duplicate-free test and fails the moment a point repeats.
- **Forgetting the `py == y` exclusion**, producing degenerate zero-area "squares."
- **Including the query point's own count** in the product. It's given, not chosen from the structure.
- Using a `set` of points and losing multiplicity entirely.
- Iterating `.items()` directly while doing `defaultdict` lookups inside the loop — a `RuntimeError` from mutation during iteration.
- Checking only one horizontal direction. Both `x + side` and `x - side` are valid squares.
- Passing a list as a dict key — `TypeError: unhashable type`.

**This same move shows up in:** [Time Based Key-Value Store](981-time-based-key-value-store.md) (a design problem trading `add` cost against query cost) · [Design Twitter](355-design-twitter.md) (choosing what to precompute versus compute on demand) · [Two Sum](1-two-sum.md) (a hash map turning a pairwise search into a single lookup) · [Top K Frequent Elements](347-top-k-frequent-elements.md) (a count map where multiplicity is the point).

</details>

---
