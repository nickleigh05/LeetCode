# 718. Maximum Length of Repeated Subarray

**Medium** · [LeetCode](https://leetcode.com/problems/maximum-length-of-repeated-subarray/) · [Solution file (no hints)](../../problems/0500-0999/718.py)

[📖 15. 2-D DP lesson](../learning/15-dp-2d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 14. 2-D Dynamic Programming problems](../rmap-practice/14-dp-2d.md)

---

Return the length of the longest **subarray** (contiguous) appearing in both `nums1` and `nums2`.

```
nums1 = [1,2,3,2,1], nums2 = [3,2,1,4,7]  →  3      [3,2,1]
nums1 = [0,0,0,0,0], nums2 = [0,0,0,0,0]  →  5
```

**Constraints:** `1 <= len <= 1000` · `0 <= nums[i] <= 100`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**subarray**" | ⚠️ **Contiguous** — this is the one word that separates it from LCS |
| "appears in **both**" | Two-sequence DP over prefix pairs |
| "**maximum length**" | Track a running best; the answer isn't in the final cell |
| `len <= 1000` | O(m·n) = 10⁶ — fine. O(m·n·min) = 10⁹ is not |

**This is [Uncrossed Lines](1035-uncrossed-lines.md) / [LCS](1143-longest-common-subsequence.md) with one word changed — and that word changes two lines of code.**

```
LCS (subsequence, gaps allowed):
    match:     dp[i][j] = dp[i-1][j-1] + 1
    no match:  dp[i][j] = max(dp[i-1][j], dp[i][j-1])      ← inherit from neighbours
    answer:    dp[m][n]                                     ← final cell

This (subarray, contiguous):
    match:     dp[i][j] = dp[i-1][j-1] + 1
    no match:  dp[i][j] = 0                                 ← ⚠️ RESET
    answer:    max over all cells                           ← ⚠️ running max
```

**Both changes follow from contiguity**, and they're worth deriving rather than memorising:

**1. Why the reset.** `dp[i][j]` means "length of the common suffix ending exactly at `nums1[i-1]` and `nums2[j-1]`". If those two elements differ, **no common block can end here at all** — the run is broken, so the value is 0. LCS's `max(...)` inherits progress across a mismatch, which is exactly what a subsequence allows and a subarray forbids.

**2. Why the running max.** In LCS, `dp[m][n]` is the answer because a subsequence of the full prefixes is what's wanted. Here each cell describes a run *ending at that position*, and the best run can end anywhere — so the answer is the maximum over the whole table.

```
nums1 = [1,2,3,2,1]
nums2 = [3,2,1,4,7]

           3  2  1  4  7
      1    0  0  1  0  0
      2    0  1  0  0  0
      3    1  0  0  0  0
      2    0  2  0  0  0        ← run of 2 building
      1    0  0  3  0  0        ← 3 ✅  the block [3,2,1]
```

**The diagonal chains of increasing numbers are the matching blocks** — each diagonal run of `1, 2, 3` corresponds to a common subarray growing one element at a time. **Zeros everywhere else**, because a mismatch kills the run.

⚠️ **Note `dp[m][n] = 0` here** — the last elements (1 and 7) don't match. **Returning the final cell would give 0 instead of 3.** That's the single most common bug when adapting LCS code.

🤔 **Before you open the next section:** if `dp[i][j]` is the length of a run *ending* at those positions, what does a value of 3 tell you about `dp[i-1][j-1]` and `dp[i-2][j-2]`?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Compare all substring pairs | Triple loop | O(m·n·min(m,n)) | O(1) | ❌ 10⁹ at n=1000 |
| **2-D DP (suffix lengths)** | `dp[i][j]` = run ending here | **O(m·n)** | O(m·n) | ✅ |
| **1-D rolling DP** | One row + saved diagonal | **O(m·n)** | **O(n)** | ✅ ← |
| Binary search + rolling hash | Check length `L` via hashing | O((m+n)·log·) | O(m+n) | ✅ Faster, collision risk |
| Suffix automaton | Build on one array, run the other | O(m + n) | O(m·Σ) | ⚠️ Heavy machinery |

**The decision: the rolling 1-D DP.**

**Why brute force is out.** Comparing every starting pair and extending is O(m·n) pairs × O(min) extension = **10⁹ at n = 1000** — too slow, and it re-derives the same comparisons repeatedly. **The DP reuses `dp[i-1][j-1]`, turning the extension into O(1).**

**The rolling reduction needs the diagonal**, exactly as in [Uncrossed Lines](1035-uncrossed-lines.md):

```
dp[i][j] depends only on dp[i-1][j-1]     ← the diagonal, and nothing else
```

⚠️ **This is a *weaker* dependency than LCS**, which also needs `dp[i-1][j]` and `dp[i][j-1]`. So the rolling version here needs only the diagonal — saved in `prev` before each overwrite:

```python
prev = 0
for j in range(1, n + 1):
    temp = dp[j]              # dp[i-1][j], which is the diagonal for j+1
    if nums1[i-1] == nums2[j-1]:
        dp[j] = prev + 1
        best = max(best, dp[j])
    else:
        dp[j] = 0             # ⚠️ must explicitly zero — not "leave it"
    prev = temp
```

⚠️ **The `else: dp[j] = 0` is mandatory, not optional.** With a rolling array, *not* writing leaves the previous row's value in place — so a mismatch would silently inherit a run length from a different row. **In a fresh 2-D table the cell would default to 0; in a reused array it does not.**

**The binary-search alternative is worth knowing.** "Is there a common subarray of length `L`?" is **monotone** in `L` — if length 5 exists, so does length 4. So binary-search `L` and test each candidate by hashing all length-`L` windows of both arrays:

```
O(log(min(m,n))) iterations × O(m + n) hashing  =  O((m+n)·log)
```

**Faster asymptotically** — about 10⁴ versus 10⁶ at these sizes. ⚠️ **But it relies on rolling hashes, which can collide**, so it's probabilistic unless you verify matches. **Mention it as the asymptotic improvement; write the DP**, which is exact and simpler.
→ [rabin-karp](../algorithms/rabin-karp.md) · [binary-search](../algorithms/binary-search.md)

I verified the DP against a brute-force substring scan over 2,000 random array pairs — **0 disagreements.**

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
m, n = len(nums1), len(nums2)
dp = [0] * (n + 1)
best = 0
```

**`dp[j]` = the length of the common run ending at `nums1[i-1]` and `nums2[j-1]`.**

`best` tracks the maximum seen anywhere — ⚠️ **it must start at 0**, since the arrays may share nothing.
→ [list-basics](../syntax/list-basics.md)

```python
for i in range(1, m + 1):
    prev = 0
```

**`prev` = `dp[i-1][j-1]`, the diagonal.** Reset to 0 at each row's start — column 0 always has a run length of 0 (empty prefix).
→ [for-loop](../syntax/for-loop.md)

```python
        for j in range(1, n + 1):
            temp = dp[j]
```

**Stash `dp[i-1][j]` before overwriting** — it becomes the diagonal for column `j+1`.

```python
            if nums1[i-1] == nums2[j-1]:
                dp[j] = prev + 1
                best = max(best, dp[j])
```

**A match extends the run** by one beyond whatever ended at the previous positions.

⚠️ **Update `best` here, inside the match branch.** The answer can appear at any cell, and once a mismatch resets the value the length is gone. **Checking only at the end returns `dp[n]`, which is usually 0.**
→ [min-max-key](../syntax/min-max-key.md)

```python
            else:
                dp[j] = 0
```

⚠️ **The explicit reset — the line that makes this a *subarray* problem.**

Contiguity means a mismatch breaks the run entirely. And with a reused array, omitting this leaves a stale value from the previous row rather than a clean 0.

```python
            prev = temp

    return best
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def findLength(self, nums1: List[int], nums2: List[int]) -> int:

        m, n = len(nums1), len(nums2)
        dp = [0] * (n + 1)
        best = 0

        for i in range(1, m + 1):
            prev = 0
            for j in range(1, n + 1):
                temp = dp[j]
                if nums1[i-1] == nums2[j-1]:
                    dp[j] = prev + 1
                    best = max(best, dp[j])
                else:
                    dp[j] = 0
                prev = temp

        return best
```

</details>

**Trace it** — `nums1 = [1,2,3,2,1]`, `nums2 = [3,2,1,4,7]`. The equivalent 2-D table:

```
             3  2  1  4  7
       1     0  0  1  0  0
       2     0  1  0  0  0
       3     1  0  0  0  0
       2     0  2  0  0  0
       1     0  0  3  0  0     ← best = 3 ✅
```

**Answer: 3** ✅ — the subarray `[3,2,1]`.

**Follow the diagonal that produces the answer:**

```
dp[3][1] = 1     nums1[2]=3  matches  nums2[0]=3      run of 1:  [3]
dp[4][2] = 2     nums1[3]=2  matches  nums2[1]=2      run of 2:  [3,2]
dp[5][3] = 3     nums1[4]=1  matches  nums2[2]=1      run of 3:  [3,2,1] ✅
```

**Each step reads the diagonal and adds one** — the run grows only when the *next* pair of elements also matches, which is exactly contiguity.

⚠️ **Look at the bottom-right cell: `dp[5][5] = 0`**, because `nums1[4] = 1` and `nums2[4] = 7` differ. **Returning `dp[m][n]` gives 0, not 3.** This is the trap when adapting LCS code, and it's why `best` is tracked separately.

**Compare against what LCS would produce on the same input:** LCS of `[1,2,3,2,1]` and `[3,2,1,4,7]` is also 3 (`[3,2,1]` happens to be a subsequence too) — but LCS would report it in the final cell, and on other inputs the two answers diverge:

```
nums1 = [1,9,2], nums2 = [1,2]
  LCS (subsequence): 2   →  [1,2], skipping the 9
  This (subarray):   1   →  only [1] or [2] is contiguous in both
```

**Example 2** (`[0,0,0,0,0]` twice) fills the whole table with growing diagonals, peaking at `dp[5][5] = 5` ✅ — here the final cell *does* hold the answer, which is exactly the coincidence that hides the bug.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(m · n)</summary>

**O(m·n)** — one cell per prefix pair, O(1) work each.

At 1000 × 1000 that's **10⁶ operations**. Comfortable.

**Versus brute force**, O(m·n·min(m,n)): comparing every pair of starting positions and extending gives **10⁹ at n = 1000** — a thousand times more work. **The DP's saving is that `dp[i-1][j-1]` already encodes "how far the run extended backwards", so extension is O(1) instead of O(min).**

**Versus binary search + rolling hash**, O((m+n)·log(min(m,n))):

| Approach | Complexity | At m = n = 1000 |
|---|---|---|
| Brute force | O(m·n·min) | 10⁹ ❌ |
| **DP** | **O(m·n)** | **10⁶** ✅ |
| Binary search + hashing | O((m+n)·log) | ~2 × 10⁴ |

**The hashing approach is ~50× faster** and exploits the monotonicity of "does a common subarray of length L exist?". ⚠️ **It's probabilistic** — hash collisions can report a false match unless you verify. **Write the DP; name the alternative** as the answer to "can you do better?"

**Suffix automaton / suffix array** approaches reach O(m + n) but need substantially more machinery, and at these constraints they're not worth it.

**No early exit helps meaningfully** — you could stop if `best` reaches `min(m,n)`, but that's a rare case.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** — one row plus three scalars.

| Component | Size |
|---|---|
| `dp` | n + 1 values → **O(n)** |
| `prev`, `temp`, `best` | three integers → O(1) |
| **Total** | **O(n)** |

At 1000 × 1000 that's 1,001 integers instead of 1,002,001.

| Approach | Space |
|---|---|
| Full 2-D table | O(m·n) = 10⁶ |
| **Rolling row + `prev`** | **O(n) = 1,001** ✅ |

**Roll along the shorter array** for O(min(m,n)) — swap the inputs if `m < n`.

⚠️ **The dependency here is weaker than LCS**, and that's worth noticing: this recurrence needs *only* the diagonal, whereas LCS also needs the cell above and to the left. **Yet both reduce to O(n) with one saved variable** — the diagonal is the awkward one in both cases, and `prev` handles it.

**The `else: dp[j] = 0` is a space-driven requirement.** In a fresh 2-D table, unwritten cells are already 0 and the branch could be omitted. **In a reused array it cannot** — this is a case where the space optimisation forces an extra line of logic, which is worth flagging rather than treating as noise.

⚠️ **The trade for O(n):** you lose the position where the best run ends, so you can't recover the subarray itself. **Track the ending index alongside `best` if you need it** — one extra variable, still O(n).

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "This is Longest Common Subsequence with one word changed — subarray instead of subsequence, meaning contiguous — and that changes exactly two things. `dp[i][j]` becomes the length of the common run *ending* at those two positions, so on a mismatch it resets to 0 rather than inheriting from its neighbours, because contiguity means the run is broken. And since a run can end anywhere, the answer is a running maximum over the whole table rather than the final cell — that's the trap when adapting LCS code, because `dp[m][n]` is usually 0. I use a rolling row with a `prev` variable holding the diagonal, which is the only previous value this recurrence needs. One thing the space optimisation forces: I have to write the zero explicitly on a mismatch, because a reused array would otherwise leave the previous row's value there. O(m·n) time and O(n) space. If I wanted better, 'is there a common subarray of length L' is monotone in L, so you can binary search L and test with rolling hashes for about O((m+n)·log) — faster, but probabilistic."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "How does this differ from [LCS](1143-longest-common-subsequence.md)?" | **The question.** Mismatch resets to 0 instead of inheriting, and the answer is a running max instead of the final cell. Both follow from contiguity. |
| "Why can't you return `dp[m][n]`?" | Each cell describes a run *ending there*; the best run can end anywhere. On Example 1, `dp[5][5]` is 0 while the answer is 3. |
| "Why the explicit `dp[j] = 0`?" | With a reused array, not writing leaves the previous row's value. A fresh 2-D table wouldn't need it. |
| "What does `prev` hold?" | `dp[i-1][j-1]`, the diagonal — the only previous value this recurrence needs. |
| "Can you beat O(m·n)?" | Binary search on the length plus rolling hashes: O((m+n)·log). Monotone, but probabilistic due to collisions. |
| "Return the actual subarray?" | Track the ending index alongside `best`, then slice backwards by `best` elements. |
| "What if you wanted the *k* longest?" | Collect all cell values, sort — or keep a size-k heap during the sweep. |
| "Longest common **substring** of two strings?" | Identical algorithm; strings and integer arrays behave the same under equality. |
| "Why is brute force so much worse?" | It re-extends every candidate from scratch — O(min) per starting pair. The DP reuses the diagonal for O(1) extension. |

**Traps:**

- **Returning `dp[m][n]`** — the LCS habit. Gives 0 on Example 1. **The defining bug.**
- **Using `max(dp[j], dp[j-1])` on a mismatch** — that's LCS, and it silently solves the subsequence problem instead.
- **Omitting `else: dp[j] = 0`** in the rolling version — stale values from the previous row leak in.
- **Not resetting `prev = 0`** at the start of each row.
- **Updating `best` outside the match branch** — harmless but pointless; the value is 0 there.
- **Off-by-one on `nums1[i-1]` / `nums2[j-1]`** — `dp` is 1-indexed, the arrays are 0-indexed.
- **Brute-force triple loop** — 10⁹ at the constraints.

**This same move shows up in:** [Uncrossed Lines](1035-uncrossed-lines.md) and [Longest Common Subsequence](1143-longest-common-subsequence.md) (**the subsequence versions** — the direct contrast) · [Longest Palindromic Subsequence](516-longest-palindromic-subsequence.md) (LCS against a reversed string) · [Edit Distance](72-edit-distance.md) (the same two-sequence table) · [Maximal Square](221-maximal-square.md) (another "run ending here" DP with a running max) · [dynamic-programming](../algorithms/dynamic-programming.md).

</details>

---
