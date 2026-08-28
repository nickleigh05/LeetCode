# 96. Unique Binary Search Trees

**Medium** · [LeetCode](https://leetcode.com/problems/unique-binary-search-trees/) · [Solution file (no hints)](../../problems/0001-0499/96.py)

[📖 14. 1-D DP lesson](../learning/14-dp-1d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 13. 1-D Dynamic Programming problems](../rmap-practice/13-dp-1d.md)

---

Return the number of **structurally unique BSTs** holding exactly the values `1..n`.

```
n = 1  →  1
n = 3  →  5
```

**Constraints:** `1 <= n <= 19`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**structurally** unique" | Only shape matters — but the BST property pins each shape to one labelling |
| "**binary search trees**" | ⚠️ Left subtree < root < right subtree. This is what makes counting tractable |
| "values from **1 to n**" | Consecutive integers, so any contiguous range behaves identically |
| "return the **number**" | Count, don't build |
| `n <= 19` | ⚠️ The answer at 19 is ~1.77 × 10⁹ — right at the 32-bit limit |

**The insight: pick the root, and the rest follows.**

Choose any value `r` from `1..n` as the root. The BST property then *forces* the split:

```
root = r

left subtree  holds  1 .. r-1     →  r - 1 values
right subtree holds  r+1 .. n     →  n - r values
```

**No choice is involved** — everything smaller must go left, everything larger must go right. And crucially, the two subtrees are built **independently**, so the counts multiply:

```
trees with root r  =  (ways to build the left)  ×  (ways to build the right)
```

**The second insight — only the *size* matters, not the values.** The number of BSTs on `{4,5,6}` is the same as on `{1,2,3}`: three consecutive values arrange identically regardless of what they are. **So `dp[k]` can depend on `k` alone.**

That collapses what looks like a 2-D problem into a 1-D one:

```
dp[k] = number of BSTs holding k consecutive values

dp[n] = Σ  dp[r-1] × dp[n-r]     over r = 1..n
```

**Worked at n = 3**, which the problem says is 5:

```
root 1:  left has 0 values, right has 2   →  dp[0] × dp[2] = 1 × 2 = 2
root 2:  left has 1 value,  right has 1   →  dp[1] × dp[1] = 1 × 1 = 1
root 3:  left has 2 values, right has 0   →  dp[2] × dp[0] = 2 × 1 = 2
                                                          total = 5 ✅
```

⚠️ **`dp[0] = 1`, not 0.** There is exactly **one** empty tree, and it must count as 1 — because it appears as a *multiplicand*. Setting it to 0 would zero out every root that has an empty side, which is most of them.

🤔 **Before you open the next section:** the recurrence multiplies two independent counts and sums over a split point. Where else have you seen a sum of products over every way to split a size?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Build every tree and count | Enumerate structures | O(Catalan(n)·n) | ❌ 1.77 × 10⁹ trees at n=19 |
| Memoised recursion | Top-down on size | O(n²) | ✅ Equivalent |
| **Bottom-up DP** | `dp[k]` for k = 0..n | **O(n²)** | ✅ |
| **Catalan formula** | `C(2n,n)/(n+1)` | **O(n)** | ✅ Fastest, needs the identity |

**The decision: bottom-up DP.** It derives from the problem rather than requiring you to recognise a sequence.

**The recurrence is the Catalan convolution:**

```python
dp = [0] * (n + 1)
dp[0] = 1
for nodes in range(1, n + 1):
    for root in range(1, nodes + 1):
        dp[nodes] += dp[root - 1] * dp[nodes - root]
```

**Reading the inner line:** with `nodes` values and `root` chosen as the k-th smallest, the left subtree gets `root - 1` values and the right gets `nodes - root`. **The two indices always sum to `nodes - 1`** — one value went to the root. That's a good invariant to check your indices against.

**These are the Catalan numbers**, and recognising them is worth a lot:

| n | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| `dp[n]` | 1 | 2 | **5** | 14 | 42 | 132 | 429 | 1430 | 4862 | 16796 |

The closed form is:

```
C(n) = (2n)! / (n! · (n+1)!) = binomial(2n, n) / (n + 1)
```

which gives an **O(n)** solution:

```python
return math.comb(2 * n, n) // (n + 1)
```

I verified the DP, the Catalan formula, and a memoised recursion all agree for every `n` from 1 to 19.

⚠️ **Use integer division `//`, not `/`.** At n = 19 the value is 1,767,263,190; float division would lose precision and return a float. **The division is always exact** — that's a theorem about Catalan numbers, not luck.

| | DP | Catalan formula |
|---|---|---|
| Time | O(n²) = 361 | **O(n)** |
| Space | O(n) | **O(1)** |
| Requires | nothing | ⚠️ recognising the sequence |
| Generalises to variants | ✅ | ❌ |

**Both are instant at n ≤ 19**, so this is a clarity decision. **Write the DP** — it shows the reasoning. **Mention Catalan** — it shows breadth, and the interviewer is often fishing for exactly that word.

**Why not enumerate the trees:** at n = 19 there are 1.77 billion of them. **The problem asks for a count precisely because construction is infeasible.**

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
dp = [0] * (n + 1)
dp[0] = 1
```

**`dp[k]` = the number of BSTs on `k` consecutive values.**

⚠️ **`dp[0] = 1` is essential**: exactly one empty tree. It appears as a factor whenever a root has no left or no right child — which is most roots — so setting it to 0 would collapse the whole table to zero.
→ [list-basics](../syntax/list-basics.md)

```python
for nodes in range(1, n + 1):
```

**Build up by subtree size**, so every smaller `dp` value is final before it's read.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md)

```python
    for root in range(1, nodes + 1):
        dp[nodes] += dp[root - 1] * dp[nodes - root]
```

**Every value gets a turn as the root**, and the results are summed.

| Expression | Meaning |
|---|---|
| `root - 1` | how many values fall **below** the root → the left subtree's size |
| `nodes - root` | how many fall **above** → the right subtree's size |
| `×` | the subtrees are **independent**, so their counts multiply |
| `+=` | different roots give **disjoint** sets of trees, so they add |

⚠️ **`range(1, nodes + 1)` is inclusive of `nodes`** — the largest value must be allowed as the root (giving an empty right subtree). Writing `range(1, nodes)` silently drops one term.

**Index check:** `(root - 1) + (nodes - root) = nodes - 1` ✅ — the root itself accounts for the missing one.
→ [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
return dp[n]
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def numTrees(self, n: int) -> int:

        dp = [0] * (n + 1)
        dp[0] = 1

        for nodes in range(1, n + 1):
            for root in range(1, nodes + 1):
                dp[nodes] += dp[root - 1] * dp[nodes - root]

        return dp[n]
```

</details>

<details>
<summary>The O(n) Catalan version, for comparison</summary>

```python
class Solution:
    def numTrees(self, n: int) -> int:
        return math.comb(2 * n, n) // (n + 1)
```

⚠️ `//` not `/` — the result is always an integer, and float division loses precision at n = 19.
→ [math-module-basics](../syntax/math-module-basics.md) · [integer-division-modulo](../syntax/integer-division-modulo.md)

</details>

**Trace it** — building up to `n = 4`. Verified output:

| | Sum over roots | `dp` |
|---|---|---|
| `dp[0]` | base case — the empty tree | **1** |
| `dp[1]` | `dp[0]·dp[0]` = 1·1 | **1** |
| `dp[2]` | `dp[0]·dp[1]` + `dp[1]·dp[0]` = 1 + 1 | **2** |
| `dp[3]` | `dp[0]·dp[2]` + `dp[1]·dp[1]` + `dp[2]·dp[0]` = 2 + 1 + 2 | **5** ✅ |
| `dp[4]` | `dp[0]·dp[3]` + `dp[1]·dp[2]` + `dp[2]·dp[1]` + `dp[3]·dp[0]` = 5 + 2 + 2 + 5 | **14** |

**The five trees at n = 3**, matching `dp[3]`'s three terms:

```
root 1 (dp[0]×dp[2] = 2)      root 2 (dp[1]×dp[1] = 1)   root 3 (dp[2]×dp[0] = 2)

  1            1                        2                   3          3
   ╲            ╲                      ╱ ╲                 ╱          ╱
    2            3                    1   3               1          2
     ╲          ╱                                          ╲        ╱
      3        2                                            2      1
```

**Two trees with root 1, one with root 2, two with root 3 — five total** ✅

**Notice the symmetry** in each row: `dp[3]`'s terms are 2, 1, 2 and `dp[4]`'s are 5, 2, 2, 5. That's because `dp[a]·dp[b]` and `dp[b]·dp[a]` are equal — roots equidistant from the ends give mirror-image counts. **A useful sanity check when you're unsure of your indices.**

**Why the middle root gives the fewest trees:** a central root splits the values evenly, and `dp` grows faster than linearly, so lopsided splits (one side empty, the other holding everything) yield more arrangements than balanced ones.

**At the constraint limit `n = 19`:** `dp[19] = 1,767,263,190` — just under 2³¹, which is exactly why the constraint stops there.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n²)</summary>

**O(n²)** for the DP.

| Component | Cost |
|---|---|
| Outer loop | **n** iterations |
| Inner loop at `nodes` | **nodes** roots → O(n) |
| **Total** | **O(n²)** |

At n = 19 that's `19²/2 ≈ 190` multiply-adds. Instantaneous.

**The Catalan formula is O(n)** — one binomial coefficient. (Strictly, `math.comb(38, 19)` involves bignum arithmetic, but at these sizes it's a handful of machine-word operations.)

| Approach | Operations at n = 19 |
|---|---|
| DP | ~190 |
| **Catalan** | **~19** |

**Neither is a bottleneck** — this is a clarity decision, not a performance one.

**Versus enumerating trees:** Catalan(19) = **1,767,263,190**. Building nearly two billion trees to count them is hopeless, and it's why the problem asks for the count rather than the trees. A variant that *does* ask for the trees has to cap n around 8, where the count is only 1,430.

**The growth rate:** Catalan numbers grow like `4ⁿ / n^1.5`, so roughly ×4 per step:

| n | Catalan(n) |
|---|---|
| 10 | 16,796 |
| 15 | 9,694,845 |
| **19** | **1,767,263,190** |
| 25 | 4.86 × 10¹² |

**n ≤ 19 exists so the answer fits in a signed 32-bit integer** — 2³¹ − 1 ≈ 2.15 × 10⁹, and Catalan(20) = 6.56 × 10⁹ would overflow. **In Python that's a non-issue**, but naming the reason shows you read the constraint.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** for the DP array.

| Component | Size |
|---|---|
| `dp` | n + 1 integers → **O(n)** |
| **Total** | **O(n)** |

At n = 19 that's 20 entries.

**⚠️ This can't reduce to O(1)** like [Tribonacci](1137-n-th-tribonacci-number.md). Computing `dp[nodes]` reads **every** earlier entry, from `dp[0]` to `dp[nodes-1]` — the convolution touches the whole prefix, so nothing can be discarded:

| | Look-back | Space |
|---|---|---|
| [Tribonacci](1137-n-th-tribonacci-number.md) | fixed 3 | **O(1)** |
| **Unique BSTs** | the entire prefix | **O(n)** |

**The Catalan formula is O(1)** — no table at all. **That's its main practical advantage**, though at n ≤ 19 twenty integers is nothing.

**The recursive Catalan identity** `C(n+1) = C(n) × 2(2n+1)/(n+2)` also gives O(1) space with O(n) time, building up one value at a time without a table — a middle ground worth knowing if you like the DP's derivability but want the formula's memory profile.

**No recursion** — iterative, so no stack concern. A memoised recursive version would be at most 19 frames deep here anyway.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The key move is fixing the root. If I pick value r as the root, the BST property forces everything below r into the left subtree and everything above into the right — no choice at all. So the trees with root r number `left count × right count`, since the subtrees are independent. And because the values are consecutive, only the *size* of a range matters, not which values it holds — three consecutive numbers arrange the same way whether they're 1,2,3 or 4,5,6. That makes it 1-D: `dp[k]` is the number of BSTs on k values, and `dp[n]` is the sum over r of `dp[r-1] × dp[n-r]`. Base case `dp[0] = 1`, one empty tree — it has to be 1 because it appears as a multiplicand whenever a root has an empty side. O(n²) time, O(n) space. These are the Catalan numbers, so there's also a closed form, `C(2n,n)/(n+1)`, which is O(n) — I'd mention that but write the DP, since it derives from the problem instead of requiring you to recognise the sequence."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why does only the subtree *size* matter?" | **The question.** Consecutive values arrange identically regardless of their actual magnitudes — that's what collapses a 2-D range problem into 1-D. |
| "Why `dp[0] = 1`?" | Exactly one empty tree, and it's a multiplicand for every root with an empty side. Setting it to 0 zeroes the table. |
| "What sequence is this?" | The **Catalan numbers**: 1, 1, 2, 5, 14, 42, 132, … Closed form `C(2n,n)/(n+1)`. |
| "Can you do it in O(n)?" | Yes — the Catalan formula, or the recurrence `C(n+1) = C(n)·2(2n+1)/(n+2)`. |
| "Why does the constraint stop at 19?" | Catalan(19) ≈ 1.77 × 10⁹ fits in a signed 32-bit int; Catalan(20) ≈ 6.6 × 10⁹ overflows. |
| "What if you had to **build** the trees?" | Same recursive structure, but returning lists of nodes instead of counts — LeetCode 95. The constraint would have to drop to about n = 8, since the output explodes. |
| "What if the values weren't consecutive?" | Doesn't matter — only their *relative order* affects BST structure, so the count is identical for any n distinct values. |
| "Count binary trees, not *search* trees?" | Same Catalan count for shapes, but each shape then admits many labellings — for arbitrary labels it's `Catalan(n) × n!`. |
| "Where else do Catalan numbers appear?" | Balanced parentheses, triangulations of a polygon, mountain ranges, Dyck paths — all the same "sum over a split point of a product" structure. |

**Traps:**

- **`dp[0] = 0`.** Every product involving an empty subtree vanishes and the answer becomes 0. **The defining bug.**
- **`range(1, nodes)`** instead of `range(1, nodes + 1)` — drops the largest value as a root candidate, losing a term.
- **Adding instead of multiplying** the subtree counts — the subtrees are independent choices, so they multiply; different roots are disjoint cases, so those add.
- **Getting the split sizes wrong** — check `(root-1) + (nodes-root) = nodes-1`.
- **Using `/` in the Catalan formula** — returns a float and loses precision at n = 19.
- **Trying to enumerate the trees** — 1.77 billion at n = 19.
- **Making `dp` 2-D over (lo, hi)** — correct but wasteful; only the size matters.

**This same move shows up in:** [Integer Break](343-integer-break.md) (summing over a split point of a 1-D quantity) · [Validate Binary Search Tree](98-validate-binary-search-tree.md) (the BST ordering property that forces the split) · [dynamic-programming](../algorithms/dynamic-programming.md) · [binary-search-tree](../data-structures/binary-search-tree.md).

</details>

---
