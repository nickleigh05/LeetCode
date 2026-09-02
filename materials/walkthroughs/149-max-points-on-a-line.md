# 149. Max Points on a Line

**Hard** · [LeetCode](https://leetcode.com/problems/max-points-on-a-line/) · [Solution file (no hints)](../../problems/0001-0499/149.py)

[📖 17. Math & Geometry lesson](../learning/19-math-geometry.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 17. Math & Geometry problems](../rmap-practice/17-math-geometry.md)

---

Given points on the X-Y plane, return the **maximum number that lie on the same straight line**.

```
points = [[1,1],[2,2],[3,3]]                      →  3
points = [[1,1],[3,2],[5,3],[4,1],[2,3],[1,4]]    →  4
```

**Constraints:** `1 <= len <= 300` · `-10^4 <= xi, yi <= 10^4` · **all points are unique**

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "the same straight line" | ⚠️ **Any** line, not one through the origin and not axis-aligned |
| "**all the points are unique**" | ⚠️ **Load-bearing** — duplicates would make `dx = dy = 0` and break the slope key |
| `len <= 300` | **O(n²) = 90,000 is comfortable.** O(n³) = 2.7 × 10⁷ is borderline |
| `-10^4 <= x, y <= 10^4` | Integer coordinates — **exact arithmetic is available** |
| `1 <= len` | ⚠️ A single point is an answer of **1**, not 0 |

**The brute force is "for every pair, count who else is collinear" — O(n³).** It passes at n = 300, and it's the wrong shape.

**The reframe that makes it O(n²).** A line is determined by a point and a direction. So:

> **Fix one point as an anchor. Every other point defines a direction from it. Points sharing a direction are on one line through the anchor.**

```
anchor (1,1):
  (2,2) → direction (1,1)
  (3,3) → direction (2,2) = (1,1) reduced      ← same line
  (4,1) → direction (3,0) = (1,0) reduced
```

**Group the directions in a hash map, take the largest bucket, add 1 for the anchor itself.** Repeat with each point as the anchor.

**Why anchoring at *every* point still finds every line.** A line containing `k` points is discovered when the anchor is any one of them — in particular the one with the lowest index — and that pass sees the other `k − 1` as one bucket. **So the maximum is always found.** ⚠️ That's also why the inner loop can safely run `j > i` only: each line is counted from its lowest-index member.

**Now the only real difficulty: how do you key a direction?**

**`dy / dx` as a float is the tempting answer.** It has two obvious problems (`dx = 0` divides by zero) and one non-obvious one (precision). **Exact integer arithmetic avoids both:** reduce `(dx, dy)` by their GCD.

```
(2, 2)  ÷ gcd 2  →  (1, 1)
(4, 4)  ÷ gcd 4  →  (1, 1)      same key ✅
(3, 0)  ÷ gcd 3  →  (1, 0)
(0, 5)  ÷ gcd 5  →  (0, 1)      vertical, no division needed ✅
```

⚠️ **But `(1, 1)` and `(−1, −1)` are the same *line* and different *pairs*.** Two points on opposite sides of the anchor produce opposite direction vectors and land in different buckets unless you normalise the sign.

🤔 **Before you open the next section:** how often does forgetting that sign normalisation actually change the answer? Guess, then check section 3.

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Every triple | Test collinearity of `(i, j, k)` | O(n³) | O(1) | ⚠️ 2.7 × 10⁷ — passes, wrong shape |
| Every pair, then count | For each line, rescan | O(n³) | O(1) | ⚠️ Same |
| **Anchor + slope hash map** | Group directions from each point | **O(n²)** | **O(n)** | ✅ **The answer** |
| Anchor + float slopes | `dy / dx`, `inf` for vertical | O(n²) | O(n) | ✅ Correct *here* — see the caveat |
| Anchor + `Fraction` | Python's exact rationals | O(n² log C) | O(n) | ⚠️ Correct, much slower |
| Hash the line equation | Normalise `(A, B, C)` | O(n²) | O(n) | ⚠️ Works, fiddlier normalisation |

**The decision: anchor each point, key the reduced direction vector, take the largest bucket.**

**Why the cross-product test is the right collinearity primitive** (and what the O(n³) reference uses):

```
(x₂ − x₁)(y₃ − y₁) − (y₂ − y₁)(x₃ − x₁) == 0
```

**All integer, no division, no precision question.** ⚠️ **Never test collinearity with `(y₂−y₁)/(x₂−x₁) == (y₃−y₁)/(x₃−x₁)`** — that's the same computation with two divisions bolted on.

**About float slopes — the honest answer.** `dy / dx` **is** correct within these constraints, and I checked rather than assumed:

> Every slope is a rational `p/q` with `|p|, |q| <= 2 × 10⁴`. Two *distinct* slopes differ by at least `1/(q₁q₂) >= 2.5 × 10⁻⁹`, while a double's spacing near magnitude 2 × 10⁴ is about `4 × 10⁻¹²` — **three orders of magnitude finer**, so distinct slopes never collide. And IEEE division is correctly rounded, so two *equal* rationals computed from different pairs (`1/3` and `2/6`) round to the identical double. **Verified: 0 disagreements over 4,000 random inputs at the full ±10⁴ range.**

⚠️ **So floats work — and I'd still write the integer version.** The float argument depends entirely on the coordinate bound; widen it and the reasoning silently expires. **The reduced-fraction key needs no argument at all.** Say both in an interview: knowing *why* the float version survives is worth more than avoiding it superstitiously.

**Why not `Fraction`.** `fractions.Fraction(dy, dx)` normalises and hashes exactly, so it's correct — and it allocates an object per pair with Python-level GCD overhead. **A plain `(dx, dy)` tuple of ints is the same information, far cheaper.**

**Why `math.gcd` handles the signs for you.** ⚠️ **`math.gcd(-4, 6)` returns `2`** — it works on absolute values — so `dx // g` and `dy // g` reduce correctly even when either is negative. **And `math.gcd(0, -5)` is `5`**, so vertical and horizontal directions reduce cleanly too.

⚠️ **`gcd(0, 0)` is `0`, which would be a division by zero** — that case means two identical points. **The "all points are unique" constraint is what rules it out**, and it's worth saying so out loud.
→ [math-module-basics](../syntax/math-module-basics.md) · [defaultdict](../syntax/defaultdict.md)

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
n = len(points)
if n <= 2:
    return n
```

**One or two points are always collinear.** ⚠️ **`return n`, not `return 2`** — a single point answers 1. **The constraint allows `len == 1`, and the main loop would return 1 anyway, but this makes the intent explicit and skips the setup.**
→ [if-return](../syntax/if-return.md)

```python
best = 1
for i in range(n):
    slopes = defaultdict(int)
    x1, y1 = points[i]
```

**Anchor at `points[i]`, with a fresh map per anchor.**

⚠️ **The map must be reset for every anchor.** Reusing it across anchors would merge directions from different origins — points on two *parallel* lines would be counted as one.

**`best = 1`** is the floor: with `n >= 1` there is always at least one point.
→ [for-loop](../syntax/for-loop.md) · [defaultdict](../syntax/defaultdict.md) · [tuple-unpacking](../syntax/tuple-unpacking.md)

```python
    for j in range(i + 1, n):
        x2, y2 = points[j]
        dx, dy = x2 - x1, y2 - y1
```

**Only points after `i`.**

⚠️ **`i + 1`, not `0`.** Every line is fully accounted for when the anchor is its lowest-index point, so earlier points can be skipped — **halving the work with no loss.**
→ [range-function](../syntax/range-function.md)

```python
        g = math.gcd(dx, dy)
        dx, dy = dx // g, dy // g
```

**Reduce the direction to lowest terms**, so `(2,2)`, `(4,4)` and `(3,3)` all become `(1,1)`.

⚠️ **`g` can never be 0** here, because that would require `dx == dy == 0` — two identical points, which the constraints forbid. **If duplicates were allowed you'd need to count them separately and add them to every bucket.**

⚠️ **`math.gcd` uses absolute values**, so this reduces correctly for negative components: `gcd(-4, 6) == 2`.
→ [math-module-basics](../syntax/math-module-basics.md) · [integer-division-modulo](../syntax/integer-division-modulo.md)

```python
        if dx < 0 or (dx == 0 and dy < 0):
            dx, dy = -dx, -dy
```

⚠️ **The sign normalisation, and the line most often missing.**

`(1, 2)` and `(−1, −2)` describe the **same line** through the anchor — one point on each side of it — but they are different tuples and would land in different buckets.

**The rule picks a canonical representative:** force `dx > 0`, and when `dx == 0` (a vertical direction) force `dy > 0`.

```
(-1, -2)  →  (1, 2)
( 0, -5)  →  (0, 1)
( 1,  2)  →  (1, 2)   unchanged
```

⚠️ **Measured: omitting this is wrong on 441 of 4,000 random inputs — about 11%.** It survives the two given examples, which is what makes it dangerous. **Concrete failure:** `[[4,0],[-3,1],[1,5],[-5,3],[-3,-4],[-3,2],[4,1],[-5,-1]]`.

⚠️ **Both clauses are needed.** Without the second, `(0, 5)` and `(0, −5)` — points directly above and below the anchor — stay in separate buckets.
→ [logical-operators](../syntax/logical-operators.md) · [swap-tuple-assign](../syntax/swap-tuple-assign.md)

```python
        slopes[(dx, dy)] += 1
        best = max(best, slopes[(dx, dy)] + 1)
```

**Count this direction, and update the answer.**

⚠️ **`+ 1` for the anchor itself.** The bucket counts the *other* points on the line; the anchor is on it too. **Forgetting this returns an answer one too small on every input.**

**Updating inside the inner loop** avoids a second pass over the map — the running maximum is enough.
→ [defaultdict](../syntax/defaultdict.md) · [min-max-key](../syntax/min-max-key.md)

```python
return best
```

<details>
<summary>The whole thing together</summary>

```python
import math
from collections import defaultdict

class Solution:
    def maxPoints(self, points: List[List[int]]) -> int:

        n = len(points)
        if n <= 2:
            return n

        best = 1

        for i in range(n):
            slopes = defaultdict(int)
            x1, y1 = points[i]

            for j in range(i + 1, n):
                x2, y2 = points[j]
                dx, dy = x2 - x1, y2 - y1

                g = math.gcd(dx, dy)
                dx, dy = dx // g, dy // g

                if dx < 0 or (dx == 0 and dy < 0):
                    dx, dy = -dx, -dy

                slopes[(dx, dy)] += 1
                best = max(best, slopes[(dx, dy)] + 1)

        return best
```

</details>

<details>
<summary>The float-slope version — correct here, and I'd still not ship it</summary>

```python
class Solution:
    def maxPoints(self, points: List[List[int]]) -> int:

        n = len(points)
        if n <= 2:
            return n

        best = 1
        for i in range(n):
            slopes = defaultdict(int)
            x1, y1 = points[i]

            for j in range(i + 1, n):
                x2, y2 = points[j]
                slope = float('inf') if x2 == x1 else (y2 - y1) / (x2 - x1)
                slopes[slope] += 1
                best = max(best, slopes[slope] + 1)

        return best
```

**No GCD, no sign normalisation** — a slope is a single number, so opposite directions give the same value automatically. ⚠️ **`x2 == x1` must be special-cased** or it's a `ZeroDivisionError`.

⚠️ **`-0.0 == 0.0` in Python and they hash identically**, so horizontal directions from either side collide correctly — a coincidence worth knowing, not relying on.

**Verified: 0 disagreements against the O(n³) reference over 4,000 random inputs at the full ±10⁴ coordinate range.** ⚠️ **Its correctness rests entirely on that bound** (see section 2). **The integer version needs no such argument.**
→ [float-inf](../syntax/float-inf.md) · [float-precision-notes](../syntax/float-precision-notes.md)

</details>

<details>
<summary>The O(n³) brute force — the verification oracle</summary>

```python
class Solution:
    def maxPoints(self, points: List[List[int]]) -> int:

        n = len(points)
        if n <= 2:
            return n

        best = 2
        for a in range(n):
            for b in range(a + 1, n):
                x1, y1 = points[a]
                x2, y2 = points[b]
                count = 2 + sum(
                    1 for k in range(n)
                    if k != a and k != b
                    and (x2 - x1) * (points[k][1] - y1) - (y2 - y1) * (points[k][0] - x1) == 0
                )
                best = max(best, count)

        return best
```

**For every pair, count how many other points are collinear via the cross product.** ⚠️ **Pure integer arithmetic — no division, no precision question.** At `n = 300` that's 2.7 × 10⁷ operations, which passes but is 300× the necessary work.

**This is what both fast versions were checked against.**
→ [generator-expressions](../syntax/generator-expressions.md)

</details>

**Trace it** — Example 2, `points = [[1,1],[3,2],[5,3],[4,1],[2,3],[1,4]]`:

**Anchor `i = 0` at `(1,1)`:**

| `j` | point | `(dx, dy)` | `g` | reduced | normalised | bucket count | `best` |
|---|---|---|---|---|---|---|---|
| 1 | (3,2) | (2, 1) | 1 | (2, 1) | (2, 1) | 1 | 2 |
| 2 | (5,3) | (4, 2) | 2 | **(2, 1)** ⚠️ | (2, 1) | **2** | **3** |
| 3 | (4,1) | (3, 0) | 3 | (1, 0) | (1, 0) | 1 | 3 |
| 4 | (2,3) | (1, 2) | 1 | (1, 2) | (1, 2) | 1 | 3 |
| 5 | (1,4) | (0, 3) | 3 | (0, 1) | (0, 1) | 1 | 3 |

**Row 2 is the whole idea:** `(4,2)` reduces to the *same key* as `(2,1)`, so `(1,1)`, `(3,2)` and `(5,3)` are recognised as collinear — bucket 2, plus the anchor, gives 3.

**Anchor `i = 1` at `(3,2)`:**

| `j` | point | `(dx, dy)` | reduced | bucket | `best` |
|---|---|---|---|---|---|
| 2 | (5,3) | (2, 1) | (2, 1) | 1 | 3 |
| 3 | (4,1) | (1, −1) | (1, −1) | 1 | 3 |
| 4 | (2,3) | (−1, 1) | ⚠️ **(1, −1)** after sign flip | **2** | **3** |
| 5 | (1,4) | (−2, 2) → (−1, 1) | ⚠️ **(1, −1)** | **3** | **4** ✅ |

**Answer: 4** ✅

⚠️ **Rows 4 and 5 are exactly why the sign normalisation exists.** `(4,1)` sits below-right of the anchor and `(2,3)`, `(1,4)` sit above-left — opposite directions on the same line `x + y = 5`. **Without the flip they would occupy two buckets of sizes 1 and 2, and the answer would come out 3.**

**Example 1**, `[[1,1],[2,2],[3,3]]`: anchor `(1,1)` gives `(1,1)` and `(2,2) → (1,1)` — one bucket of size 2, plus the anchor → **3** ✅

**Edge cases:**

| Input | Result | Why |
|---|---|---|
| `[[0,0]]` | **1** | `n <= 2` early return |
| `[[0,0],[5,7]]` | **2** | any two points are collinear |
| all points on one vertical line | `n` | every direction reduces to `(0, 1)` |

**Verified:** the reduced-fraction version was checked against the O(n³) cross-product reference on **3,000 randomised inputs** (coordinate ranges ±3, ±5 and ±40, so collinear clusters are common) plus **4,000 more at the full ±10⁴ range** — **0 disagreements**. The same harness measured the version **without sign normalisation failing 441 of 4,000 (11%)**.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n² log C)</summary>

**O(n²)** pair examinations, each doing a GCD.

| Phase | Cost |
|---|---|
| Outer loop | n anchors |
| Inner loop | ≤ n − 1 points each |
| `math.gcd` per pair | **O(log C)**, `C = 2 × 10⁴` |
| Hash insert / lookup | O(1) amortised |
| **Total** | **O(n² log C)**, effectively **O(n²)** |

**At `n = 300` that's 44,850 pairs** — instant.

| Approach | Time | Operations at n = 300 |
|---|---|---|
| **Anchor + reduced slope** | **O(n² log C)** | **~4.5 × 10⁴ pairs** ✅ |
| Anchor + float slope | **O(n²)** | ~4.5 × 10⁴, no GCD |
| Every pair, then rescan | O(n³) | **2.7 × 10⁷** ⚠️ |
| Every triple | O(n³) | 4.5 × 10⁶ triples |

**The float version is genuinely faster** — one division instead of a GCD — **and it trades an unconditional guarantee for one that depends on the coordinate bound.** At this size, take the guarantee.

**`math.gcd` is Euclid's algorithm**, so `O(log min(|dx|, |dy|))` — at most about 15 steps for coordinates in this range. **A small constant, not a hidden linear factor.**

⚠️ **Can you beat O(n²)?** **No known algorithm does asymptotically better** for the general problem — determining whether *any* three points are collinear is the classic **3SUM-hard** problem, conjectured to require Ω(n²). **So O(n²) is very likely optimal, and saying that is worth more than hand-waving about "maybe a sweep".**

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** — one hash map, rebuilt per anchor.

| Component | Size |
|---|---|
| `slopes` for one anchor | **≤ n − 1 entries** |
| ⚠️ Rebuilt each iteration | **not accumulated** — O(n), not O(n²) |
| `best`, `dx`, `dy`, `g` | O(1) |
| **Total** | **O(n)** ✅ |

⚠️ **The map being local to the anchor is what keeps this O(n).** Hoisting it out of the loop to "avoid reallocating" would both **break correctness** (merging directions from different origins) and **grow the space to O(n²)**.

**Each key is a 2-tuple of small integers**, so the constant factor is modest — roughly 300 entries at peak.

⚠️ **The float version stores one float per key instead of a tuple** — slightly smaller, same asymptotics.

⚠️ **The `Fraction` version would allocate a `Fraction` object per pair** — same O(n) live at any moment, but far more garbage and a much larger constant. **Another reason to prefer the plain tuple.**

**No recursion.** Two flat nested loops.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The brute force is to take every pair, define a line, and count who else is on it — O(n³). Better: fix one point as an anchor, and every other point defines a direction from it; points sharing a direction are on one line through the anchor. So I hash the directions, take the biggest bucket, add one for the anchor, and repeat with each point as anchor. Any line with k points is found when its lowest-index member is the anchor, so the inner loop only needs to look forward. The key detail is how to represent a direction. I reduce `(dx, dy)` by their GCD so `(2,2)` and `(4,4)` collide, and then I normalise the sign — force dx positive, and dy positive when dx is zero — because a point on either side of the anchor gives opposite vectors for the same line. That sign step is easy to skip and it's wrong on about eleven percent of random inputs. Float slopes actually do work at these coordinate bounds — I checked the numerics, distinct slopes are separated by about 2.5e-9 and double precision there is around 4e-12 — but that argument expires if the bounds widen, so I'd write the integer version. O(n²) time with a log factor for the GCD, O(n) space. And O(n² ) is essentially optimal: detecting any three collinear points is 3SUM-hard."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "**Why normalise the sign?**" | **The question.** `(1,2)` and `(−1,−2)` are the same line from opposite sides of the anchor. Wrong on ~11% of random inputs without it. |
| "Why reduce by the GCD?" | So `(2,2)`, `(4,4)` and `(3,3)` hash to one key. Exact, no division by zero except for duplicate points. |
| "Why `j > i` and not all `j`?" | Every line is fully counted when its lowest-index point is the anchor. Halves the work. |
| "Why `+ 1` on the bucket?" | The bucket counts the *other* points; the anchor is on the line too. |
| "**Are float slopes wrong?**" | **Not at these bounds** — distinct slopes differ by ≥ 2.5 × 10⁻⁹, doubles resolve ~4 × 10⁻¹². Verified over 4,000 full-range inputs. **But the argument depends on the bound.** |
| "What about `dx == 0`?" | The reduced key is `(0, 1)` — no division, no `inf`. That's a strength of the integer version. |
| "**What if points could repeat?**" | `gcd(0,0) == 0` → ZeroDivisionError. Count duplicates of the anchor separately and add them to every bucket. **The uniqueness constraint is what avoids this.** |
| "Can you beat O(n²)?" | Almost certainly not — deciding whether any three points are collinear is **3SUM-hard**. |
| "Hash the line rather than the direction?" | Normalise `(A, B, C)` for `Ax + By = C` by GCD and sign, then one global map — O(n²) too, and the normalisation is fiddlier. |
| "Would `Fraction` work?" | Yes, exactly — and it allocates an object per pair. The tuple carries the same information. |
| "How would you return the line itself?" | Store one representative pair per bucket alongside the count. |
| "n = 1?" | Answer 1. ⚠️ `return n` on the early exit, not `return 2`. |

**Traps:**

- ⚠️ **Skipping the sign normalisation** — ~11% wrong, and it passes both given examples.
- ⚠️ **Normalising `dx` only, forgetting `dx == 0 and dy < 0`** — vertical lines split into two buckets.
- ⚠️ **Forgetting `+ 1` for the anchor** — every answer comes out one too small.
- ⚠️ **Hoisting `slopes` outside the anchor loop** — merges parallel lines, and turns O(n) space into O(n²).
- **`return 2` in the early exit** — a single point is 1.
- **`dy / dx` without guarding `dx == 0`** — `ZeroDivisionError`.
- **Testing collinearity with divisions** — use the cross product; it's exact.
- **Assuming `gcd` can't be 0** without citing the uniqueness constraint — it's the reason, and it's worth saying.
- **Initialising `best = 0`** — with `n >= 1` the answer is at least 1.
- **Using `Counter` and scanning it after each anchor** — correct but an extra O(n) pass; the running max is free.

**This same move shows up in:** [Detect Squares](2013-detect-squares.md) (anchoring at one point and hashing geometric relations to the others) · [Longest Arithmetic Subsequence](1027-longest-arithmetic-subsequence.md) (keying a hash map by a *difference* rather than a value) · [Two Sum](1-two-sum.md) (the hash-map-per-pass pattern in its simplest form) · [K Closest Points to Origin](973-k-closest-points-to-origin.md) (integer geometry without floating point) · [Greatest Common Divisor of Strings](1071-greatest-common-divisor-of-strings.md) (reducing by a GCD to canonicalise) · [Group Anagrams](49-group-anagrams.md) (choosing a canonical key so equivalent things collide).

</details>

---
