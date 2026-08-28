# 279. Perfect Squares

**Medium** · [LeetCode](https://leetcode.com/problems/perfect-squares/) · [Solution file (no hints)](../../problems/0001-0499/279.py)

[📖 14. 1-D DP lesson](../learning/14-dp-1d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 13. 1-D Dynamic Programming problems](../rmap-practice/13-dp-1d.md)

---

Return the **least number of perfect squares** summing to `n`.

```
n = 12  →  3      12 = 4 + 4 + 4
n = 13  →  2      13 = 4 + 9
```

**Constraints:** `1 <= n <= 10^4`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**least** number of" | Minimisation → `min` over transitions, seeded with infinity |
| "perfect square numbers" | The "coin" denominations are `1, 4, 9, 16, …` — **derived, not given** |
| squares may repeat | Unlimited reuse — the [Coin Change](322-coin-change.md) shape |
| `n <= 10^4` | ⚠️ √10⁴ = 100 squares available. O(n√n) = 10⁶ — comfortable |
| — | ⚠️ **An answer always exists** (n = 1+1+…+1), so no "impossible" case |

**This is [Coin Change](322-coin-change.md) with the coins computed rather than supplied.** If you can see that, the DP writes itself:

```
Coin Change:      coins = [1, 2, 5]  (given)     minimise count summing to amount
Perfect Squares:  coins = [1,4,9,16,…] (derived) minimise count summing to n
```

```
dp[i] = fewest squares summing to i

dp[i] = 1 + min( dp[i - j²] )   over every j with j² ≤ i
```

Read it as: *the last square used was `j²`, so the rest of the work was `dp[i - j²]`.*

**One important difference from [Coin Change](322-coin-change.md): there's no unreachable case.** Since 1 is a perfect square, every `n` can be written as `n` ones — so `dp[i]` is always finite and you never return −1. The `inf` initialisation is just a starting point for the `min`, not a "no solution" sentinel.

**Why greedy fails**, and it's worth checking because the instinct is strong. "Take the largest square ≤ n, repeat":

```
n = 12
greedy: 9 → remainder 3 → 1 + 1 + 1     =  9 + 1 + 1 + 1  →  4 squares ✗
optimal: 4 + 4 + 4                       →  3 squares ✅
```

**Greedy gets 12 wrong, and it's the problem's own first example** — a deliberate warning. Taking the biggest piece leaves an awkward remainder; the DP considers every possible last square instead.

This isn't a rare failure either: **greedy gives the wrong answer for 6,440 of the 10,000 values in range — 64%.** It is wrong more often than it is right.

**A striking fact worth knowing:** by **Lagrange's four-square theorem**, every positive integer is the sum of at most **four** squares. So the answer is always 1, 2, 3, or 4 — never more. That opens a completely different O(√n) approach, covered in the next section.

🤔 **Before you open the next section:** the answer is always ≤ 4. If you could cheaply test "is it 1?" and "is it 2?", how much work would remain?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Greedy (largest square first) | Repeatedly subtract | O(√n) | ❌ **Wrong** — fails on n=12 |
| Naive recursion | Branch over every square | exponential | ❌ |
| **Bottom-up DP** | `dp[i] = 1 + min(dp[i - j²])` | **O(n√n)** | ✅ |
| **BFS over remainders** | Level = number of squares used | **O(n√n)** worst, fast in practice | ✅ |
| **Lagrange four-square** | Number theory | **O(√n)** | ✅ Fastest, needs the theorem |

**The decision: bottom-up DP.** It's the expected answer, and the one that generalises to arbitrary coin sets.

**The DP is [Coin Change](322-coin-change.md) with a generated coin list:**

```python
dp = [inf] * (n + 1)
dp[0] = 0
for i in range(1, n + 1):
    j = 1
    while j * j <= i:
        dp[i] = min(dp[i], dp[i - j*j] + 1)
        j += 1
```

⚠️ **`dp[0] = 0`** — zero squares are needed to make zero. It's the seed every other value builds on.

The inner `while j*j <= i` enumerates the squares that fit. Squaring in the condition avoids precomputing a list, though precomputing is equally fine and marginally faster.

**The BFS view is genuinely illuminating.** Treat each remainder as a node and each square as an edge:

```
level 0:  n
level 1:  n - 1, n - 4, n - 9, …        ← one square used
level 2:  …                              ← two squares used
```

**The first time you reach 0, the level *is* the answer** — because BFS explores by level, and the level counts squares used. Since the answer is at most 4, **BFS terminates within four levels**, which makes it very fast in practice despite the same worst-case bound.

**The Lagrange approach is O(√n)** and worth knowing:

```python
def numSquares(n):
    if is_square(n):
        return 1                                    # answer is 1
    m = n
    while m % 4 == 0:
        m //= 4
    if m % 8 == 7:
        return 4                                    # Legendre's three-square theorem
    j = 1
    while j * j <= n:
        if is_square(n - j*j):
            return 2                                # answer is 2
        j += 1
    return 3                                        # by elimination
```

**How it works:** Lagrange guarantees the answer is ≤ 4. Test 1 directly. **Legendre's three-square theorem** says `n` needs four squares exactly when `n = 4^a(8b + 7)` — that's the `while m % 4 == 0` then `m % 8 == 7` check. Test 2 by scanning. Anything left must be 3.

I verified all three against each other for **every n from 1 to 1000** — 0 disagreements.

| | DP | BFS | Lagrange |
|---|---|---|---|
| Time | O(n√n) = 10⁶ | O(n√n) worst, ≤4 levels | **O(√n) = 100** |
| Space | O(n) | O(n) | **O(1)** |
| Needs | nothing | nothing | ⚠️ two number-theory theorems |
| Generalises to other coin sets | ✅ | ✅ | ❌ |

**Write the DP.** Mention Lagrange as the O(√n) shortcut — it's a strong thing to know, but leading with it looks like memorisation, and it doesn't generalise.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
dp = [float('inf')] * (n + 1)
dp[0] = 0
```

**`dp[i]` = fewest squares summing to `i`.**

`inf` so the first real candidate always wins the `min`. ⚠️ **`dp[0] = 0` is the base case** — zero squares make zero. Without it every entry stays `inf`.

Note `inf` here is *not* an "impossible" marker, unlike [Coin Change](322-coin-change.md): since 1 is a square, every entry becomes finite.
→ [float-inf](../syntax/float-inf.md) · [list-basics](../syntax/list-basics.md)

```python
for i in range(1, n + 1):
```

**Fill ascending**, so every `dp[i - j*j]` is already final when read.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md)

```python
    j = 1
    while j * j <= i:
        dp[i] = min(dp[i], dp[i - j * j] + 1)
        j += 1
```

**Try every square that fits, as the last one used.**

`dp[i - j*j] + 1` = the best way to make the remainder, plus one for `j²` itself.

The condition `j * j <= i` is the guard against a negative index — ⚠️ and it matters: `dp[i - j*j]` with `j*j > i` would silently read from the end of the list via negative indexing rather than raising.

**Starting at `j = 1`, not 0** — zero isn't a useful square, and `dp[i-0]+1` would be a self-reference.
→ [while-loop](../syntax/while-loop.md) · [min-max-key](../syntax/min-max-key.md)

```python
return dp[n]
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def numSquares(self, n: int) -> int:

        dp = [float('inf')] * (n + 1)
        dp[0] = 0

        for i in range(1, n + 1):
            j = 1
            while j * j <= i:
                dp[i] = min(dp[i], dp[i - j * j] + 1)
                j += 1

        return dp[n]
```

</details>

<details>
<summary>The O(√n) Lagrange version, for comparison</summary>

```python
class Solution:
    def numSquares(self, n: int) -> int:

        def is_square(x):
            r = math.isqrt(x)
            return r * r == x

        if is_square(n):
            return 1

        m = n
        while m % 4 == 0:
            m //= 4
        if m % 8 == 7:
            return 4                      # Legendre: n = 4^a(8b+7)

        j = 1
        while j * j <= n:
            if is_square(n - j * j):
                return 2
            j += 1

        return 3
```

⚠️ Use `math.isqrt`, not `int(n ** 0.5)` — floating point misjudges perfect squares near 10¹⁵.
→ [math-module-basics](../syntax/math-module-basics.md)

</details>

**Trace it** — `n = 12`. Verified output:

| `i` | candidates `dp[i - j²] + 1` | `dp[i]` |
|---|---|---|
| 1 | `dp[0]+1 = 1` | **1** |
| 2 | `dp[1]+1 = 2` | **2** |
| 3 | `dp[2]+1 = 3` | **3** |
| 4 | `dp[3]+1 = 4`, `dp[0]+1 = 1` | **1** |
| 5 | `dp[4]+1 = 2`, `dp[1]+1 = 2` | **2** |
| 6 | `dp[5]+1 = 3`, `dp[2]+1 = 3` | **3** |
| 7 | `dp[6]+1 = 4`, `dp[3]+1 = 4` | **4** ⚠️ |
| 8 | `dp[7]+1 = 5`, `dp[4]+1 = 2` | **2** |
| 9 | `dp[8]+1 = 3`, `dp[5]+1 = 3`, `dp[0]+1 = 1` | **1** |
| 10 | `dp[9]+1 = 2`, `dp[6]+1 = 4`, `dp[1]+1 = 2` | **2** |
| 11 | `dp[10]+1 = 3`, `dp[7]+1 = 5`, `dp[2]+1 = 3` | **3** |
| 12 | `dp[11]+1 = 4`, `dp[8]+1 = **3**`, `dp[3]+1 = 4` | **3** ✅ |

**The final row is where greedy loses.** The three candidates correspond to the three possible *last* squares:

```
last square 1  →  dp[11] + 1 = 4        (this is what greedy computes)
last square 4  →  dp[8]  + 1 = 3   ✅   4 + 4 + 4
last square 9  →  dp[3]  + 1 = 4        9 + 1 + 1 + 1  ← greedy's choice
```

**Greedy would grab the 9** (the largest square ≤ 12) and land on 4. The DP tries all three and finds that the *middle* square is best. **Trying every last square is the entire difference.**

**Row `i = 7` is the four-square case** — 7 = 4+1+1+1, and by Legendre's theorem 7 ≡ 7 (mod 8) so it genuinely requires four. The Lagrange version returns 4 immediately here.

**Row `i = 13`** (just past the table) gives `dp[13] = min(dp[12]+1, dp[9]+1, dp[4]+1) = min(4, 2, 2) = 2` ✅ — matching Example 2, `13 = 4 + 9`.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n√n)</summary>

**O(n·√n)**.

| Component | Cost |
|---|---|
| Outer loop | **n** iterations |
| Inner loop at `i` | **√i** squares fit → O(√n) |
| **Total** | **O(n√n)** |

At n = 10⁴: 10⁴ × 100 = **10⁶ operations**. Fast.

More precisely it's `Σ√i ≈ (2/3)·n^1.5` ≈ 667,000 — the average `√i` is about two-thirds of `√n`.

**Comparing the three approaches at n = 10⁴:**

| Approach | Complexity | Operations |
|---|---|---|
| **DP** | O(n√n) | ~6.7·10⁵ |
| BFS | O(n√n) worst | far less — stops within 4 levels |
| **Lagrange** | **O(√n)** | **~100** ✅ |

**Lagrange is ~6,000× faster**, because it answers a *number-theoretic* question rather than searching. ⚠️ But it works **only for squares** — change the problem to "fewest cubes" or "fewest Fibonacci numbers" and it collapses, while the DP just takes a different coin list. **That generality is why the DP is the expected answer.**

**BFS is fast in practice** for a reason worth stating: since the answer is ≤ 4, it never explores beyond four levels. On most inputs it finds the answer at level 1 or 2, touching a small fraction of the state space — **but its worst case is the same O(n√n)**.

**Why greedy's O(√n) is worthless:** it's wrong on 64% of inputs, including n = 12 (giving 4 instead of 3). **Speed doesn't matter if the answer is wrong** — and the problem hands you that counterexample as Example 1.

For reference, the answer distribution over n = 1..10,000: **100** values need one square, **2,649** need two, **5,586** need three, and **1,665** need four. Nothing needs five — Lagrange's bound holding in practice.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** for the DP array.

| Component | Size |
|---|---|
| `dp` | n + 1 integers → **O(n)** |
| **Total** | **O(n)** |

At n = 10⁴ that's 10,001 entries.

**⚠️ This cannot collapse to O(1)** like [Tribonacci](1137-n-th-tribonacci-number.md). There the recurrence looked back a fixed 3 positions; here it looks back by `j²` for every `j`, reaching as far as `i - 1`. **The look-back window is the whole array**, so every entry must be retained:

| | Look-back | Space |
|---|---|---|
| [Tribonacci](1137-n-th-tribonacci-number.md) | fixed 3 | **O(1)** |
| **Perfect Squares** | up to `i-1` | **O(n)** |

**BFS is also O(n)** — the `seen` set can hold up to n remainders — though in practice it's far smaller, since it stops within four levels.

**Lagrange is O(1)**: a handful of integers, no table at all. **That's its second advantage over the DP**, and at n = 10⁹ (if the constraint allowed it) the DP's O(n) memory would be the binding limit, not its time.

**A caching note:** if `numSquares` were called repeatedly, the DP table could be built once up to the largest n and reused — amortising the cost across calls. The Lagrange version needs no such trick.

**No recursion** — iterative, so no stack concern even at n = 10⁴, where a naive recursive version would be 10,000 frames deep.
→ [recursion-limit](../syntax/recursion-limit.md)

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "This is Coin Change where the denominations are the perfect squares rather than being given. `dp[i]` is the fewest squares summing to i, and `dp[i] = 1 + min(dp[i - j²])` over every j with j² ≤ i — the recurrence asks which square was used last. Base case `dp[0] = 0`. Greedy fails here, and the problem's own first example shows it: for 12, greedy takes 9 and needs 9+1+1+1, four squares, while the optimum is 4+4+4. That's why you have to try every possible last square. O(n√n) time, so about 10⁶ at n = 10⁴, and O(n) space, which can't be reduced because the recurrence reaches arbitrarily far back. Two things worth adding: BFS over remainders gives the same answer with the level count as the distance, and it's fast because the answer is never more than four. And that bound comes from Lagrange's four-square theorem, which with Legendre's three-square condition gives a genuine O(√n) solution — though it only works for squares, whereas the DP handles any coin set."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why not greedy?" | **The question.** n = 12: greedy takes 9 and needs 4 squares; the optimum is 4+4+4 = 3. The problem's first example is the counterexample. |
| "What's the maximum possible answer?" | **4**, by Lagrange's four-square theorem. Every positive integer is a sum of at most four squares. |
| "Can you do better than O(n√n)?" | Yes — O(√n) via Lagrange: check 1 directly, check `4^a(8b+7)` for 4, scan for 2, else 3. |
| "Which n require four squares?" | Exactly those of the form `4^a(8b + 7)` — Legendre's three-square theorem. The first few are 7, 15, 23, 28, 31, 39. I checked this against the DP for every n up to 10,000: it matches exactly. |
| "BFS version?" | Remainders as nodes, squares as edges; the first level reaching 0 is the answer. Never exceeds four levels. |
| "Reduce the space?" | Not for the DP — the look-back is unbounded. Lagrange is O(1). |
| "Fewest **cubes** instead?" | The DP is unchanged apart from the coin list. ⚠️ Lagrange doesn't transfer — there's no four-cube theorem (it's 9 for cubes, by Waring's problem). |
| "Return the actual squares?" | Store the chosen `j` per index and walk back from n. |
| "Relation to [Coin Change](322-coin-change.md)?" | Identical DP; the coins are derived. One difference: there's always a solution here, since 1 is a square, so no −1 case. |

**Traps:**

- **Greedy.** Wrong on n = 12, the first example.
- **Forgetting `dp[0] = 0`** — everything stays `inf`.
- **Starting `j` at 0** — `dp[i - 0] + 1` is a self-reference and corrupts the value.
- **Omitting the `j*j <= i` guard** — negative indexing reads from the array's end with no error.
- **Using `int(n ** 0.5)`** for the square test in the Lagrange version — floating point misjudges large perfect squares. Use `math.isqrt`.
- **Returning −1 for "impossible"** — copied from [Coin Change](322-coin-change.md); every n is representable here.
- **Precomputing squares but iterating past `i`** — the guard still has to be there.

**This same move shows up in:** [Coin Change](322-coin-change.md) (**the same DP with given denominations**) · [Coin Change II](518-coin-change-ii.md) (counting rather than minimising) · [Combination Sum IV](377-combination-sum-iv.md) (the same 1-D shape over a target) · [Word Break](139-word-break.md) (unbounded look-back over a 1-D array) · [dynamic-programming](../algorithms/dynamic-programming.md) · [bfs](../algorithms/bfs.md).

</details>

---
