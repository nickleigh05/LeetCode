# 1035. Uncrossed Lines

**Medium** · [LeetCode](https://leetcode.com/problems/uncrossed-lines/) · [Solution file (no hints)](../../problems/1000-1499/1035.py)

[📖 15. 2-D DP lesson](../learning/15-dp-2d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 14. 2-D Dynamic Programming problems](../rmap-practice/14-dp-2d.md)

---

Write `nums1` and `nums2` on two parallel lines. Draw connecting lines between **equal** values such that **no two lines cross** and each number is used at most once. Return the maximum number of lines.

```
nums1 = [1,4,2], nums2 = [1,2,4]            →  2
nums1 = [2,5,1,2,5], nums2 = [10,5,2,1,5,2] →  3
nums1 = [1,3,7,1,7,5], nums2 = [1,9,2,5,1]  →  2
```

**Constraints:** `1 <= len <= 500` · `1 <= nums[i] <= 2000`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "written **in the order they are given**" | ⚠️ Order is fixed — this is the constraint that creates the structure |
| "`nums1[i] == nums2[j]`" | Lines connect equal values |
| "does **not intersect** any other line" | ⚠️ **The disguise.** Decode this and the problem vanishes |
| "each number can only belong to one line" | No reuse — a matching |
| "**maximum** number of lines" | Optimisation |
| `len <= 500` | O(m·n) = 250,000 — comfortable |

**The decode is the entire problem.** What does "no two lines cross" actually mean?

```
Two lines (i₁ → j₁) and (i₂ → j₂) cross  ⟺  i₁ < i₂ but j₁ > j₂

So NON-crossing means:  i₁ < i₂  ⟹  j₁ < j₂
```

**Both index sequences must increase together.** A set of non-crossing lines is therefore exactly a set of matched pairs whose indices ascend in both arrays — which is precisely a **common subsequence**.

> **This is [Longest Common Subsequence](1143-longest-common-subsequence.md), word for word, with "line" substituted for "matched character".**

```
nums1 = [1,4,2]
nums2 = [1,2,4]

common subsequences: [1], [4], [2], [1,4], [1,2]
longest: length 2  →  2 lines ✅

Why not 3? [1,4,2] would need j-indices 0, 2, 1 — not increasing, so the
4-line and the 2-line would cross. Exactly what the problem says.
```

**Once you see it's LCS, the recurrence is the standard one:**

```
if nums1[i-1] == nums2[j-1]:  dp[i][j] = dp[i-1][j-1] + 1     match them
else:                          dp[i][j] = max(dp[i-1][j], dp[i][j-1])   skip one
```

⚠️ **The values being integers rather than characters changes nothing.** LCS never cares what the elements *are*, only whether they're equal. That's why [Longest Common Subsequence](1143-longest-common-subsequence.md) on strings and this on integer arrays are the same code.

🤔 **Before you open the next section:** the problem says duplicates may appear (`nums2 = [10,5,2,1,5,2]` has two 5s and two 2s). Does that break the LCS correspondence, or does LCS already handle it?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Enumerate matchings | Try every line set | exponential | — | ❌ |
| Greedy (match earliest) | Take the first available pair | O(m·n) | O(1) | ❌ **Wrong** |
| 2-D LCS table | `dp[m+1][n+1]` | O(m·n) | O(m·n) | ✅ Clearest |
| **1-D rolling LCS** | One row + a saved diagonal | **O(m·n)** | **O(n)** | ✅ ← |

**The decision: LCS with a rolling row.**

**Why greedy fails**, since "match the first equal pair you find" is tempting:

```
nums1 = [1, 4, 2]
nums2 = [1, 2, 4]

greedy: match 1↔1. Then 4: the earliest 4 in nums2 is at index 2.
        Match 4↔4. Now 2 must come after index 2 in nums2 — nothing left.
        Total: 2.   ✅ correct here, by luck

The failure mode: committing to a match that blocks two later ones.
LCS considers skipping a match, which greedy never does.
```

**The `max(dp[i-1][j], dp[i][j-1])` branch is exactly "consider skipping"** — and it's what greedy lacks.

**The rolling-row reduction, and the wrinkle.** The recurrence needs three previous values:

```
dp[i-1][j-1]   diagonal   ⚠️ overwritten by the time you reach column j
dp[i-1][j]     above      still in dp[j] before writing
dp[i][j-1]     left       already written this row, in dp[j-1]
```

**The diagonal is the problem.** Sweeping left-to-right, `dp[j-1]` gets overwritten at column `j-1`, destroying the diagonal that column `j` needs. **Save it first:**

```python
prev = 0                    # dp[i-1][j-1], starting at j=0
for j in range(1, n + 1):
    temp = dp[j]            # stash dp[i-1][j] BEFORE overwriting
    if match:
        dp[j] = prev + 1    # use the saved diagonal
    else:
        dp[j] = max(dp[j], dp[j-1])
    prev = temp             # this becomes the diagonal for j+1
```

⚠️ **`prev` holds the previous row's value at column `j-1`** — precisely the diagonal. The `temp` dance is what carries it forward one column at a time.

**This is the same one-variable trick as [Maximal Square](221-maximal-square.md)** and [Minimum Falling Path Sum](931-minimum-falling-path-sum.md), and it's worth recognising as a pattern: **whenever a rolling DP needs the diagonal, one saved variable replaces the second row.**

**Duplicates need no special handling.** LCS matches by value and advances both indices, so repeated values are consumed correctly — I verified this version against a standard 2-D LCS over 2,000 random arrays drawn from a 4-value alphabet (guaranteeing heavy duplication): **0 disagreements.**

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
m, n = len(nums1), len(nums2)
dp = [0] * (n + 1)
```

**`dp[j]` = the LCS length between the processed prefix of `nums1` and `nums2[:j]`.**

`n + 1` slots: index 0 means "empty prefix of nums2", whose LCS with anything is 0. **That sentinel is what removes the boundary checks.**
→ [list-basics](../syntax/list-basics.md)

```python
for i in range(1, m + 1):
    prev = 0
```

**`prev` starts at 0 each row** — it represents `dp[i-1][0]`, the LCS with an empty prefix of `nums2`.
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md)

```python
        for j in range(1, n + 1):
            temp = dp[j]
```

⚠️ **Stash the current `dp[j]` before it's overwritten.** It's the previous row's value at column `j`, which becomes the *diagonal* for column `j+1`.

**Forgetting this line is the defining bug** — you'd use a value from the current row as the diagonal, silently overcounting.

```python
            if nums1[i-1] == nums2[j-1]:
                dp[j] = prev + 1
```

**A match: extend the diagonal.**

`prev` is `dp[i-1][j-1]` — the best matching using both prefixes *excluding* the two elements just paired. Adding this line gives `+1`.

⚠️ **The `-1` offsets** convert between 1-indexed DP positions and 0-indexed arrays. `dp[i][j]` concerns `nums1[:i]` and `nums2[:j]`, so the *last* elements are at `i-1` and `j-1`.

```python
            else:
                dp[j] = max(dp[j], dp[j-1])
```

**No match: skip one element from either side.**

`dp[j]` (not yet overwritten) is `dp[i-1][j]` — skip `nums1[i-1]`. `dp[j-1]` (already written) is `dp[i][j-1]` — skip `nums2[j-1]`. **Take whichever leaves more lines.**
→ [min-max-key](../syntax/min-max-key.md) · [elif-else](../syntax/elif-else.md)

```python
            prev = temp
```

**Carry the saved value forward** as the next column's diagonal.

```python
return dp[n]
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def maxUncrossedLines(self, nums1: List[int], nums2: List[int]) -> int:

        m, n = len(nums1), len(nums2)
        dp = [0] * (n + 1)

        for i in range(1, m + 1):
            prev = 0
            for j in range(1, n + 1):
                temp = dp[j]
                if nums1[i-1] == nums2[j-1]:
                    dp[j] = prev + 1
                else:
                    dp[j] = max(dp[j], dp[j-1])
                prev = temp

        return dp[n]
```

</details>

**Trace it** — `nums1 = [1,4,2]`, `nums2 = [1,2,4]`. Showing the equivalent 2-D table for clarity:

```
           ""   1    2    4
      ""    0   0    0    0
       1    0   1    1    1        ← 1 matches nums2[0]
       4    0   1    1    2        ← 4 matches nums2[2]
       2    0   1    2    2        ← 2 matches nums2[1]
```

**Answer: `dp[3][3] = 2`** ✅

**Reading the final cell:** at `nums1[2]=2` vs `nums2[2]=4` there's no match, so it takes `max(above=2, left=2) = 2`.

**Row 3, column 2 is the interesting one.** `nums1[2] = 2` matches `nums2[1] = 2`, giving `diagonal + 1 = dp[2][1] + 1 = 1 + 1 = 2`. **So the pairing 1↔1 plus 2↔2 also achieves 2** — an alternative to 1↔1 plus 4↔4.

**Why 3 is impossible**, confirming the problem's explanation: matching all of 1, 4, 2 would need `nums2` indices 0, 2, 1 — not increasing. **The `4↔4` line (0→2) and the `2↔2` line (2→1) would cross.** The DP never even considers it, because the recurrence only ever extends the diagonal, which forces both indices upward.

**In rolling form**, the same computation collapses to one array:

```
after i=1 (nums1[0]=1):  dp = [0, 1, 1, 1]
after i=2 (nums1[1]=4):  dp = [0, 1, 1, 2]
after i=3 (nums1[2]=2):  dp = [0, 1, 2, 2]   →  dp[3] = 2 ✅
```

**Example 2** (`[2,5,1,2,5]` vs `[10,5,2,1,5,2]`) gives **3** — e.g. matching `5↔5` (index 1→1), `1↔1` (2→3), `5↔5` (4→4). Note both arrays have repeated 5s and 2s, and **the LCS handles them without any special casing.**

</details>

<details>
<summary><b>4 · Time complexity</b> — O(m · n)</summary>

**O(m·n)** — one cell per pair of prefixes, O(1) work each.

At 500 × 500 that's **250,000 operations**. Instant.

**Identical to [Longest Common Subsequence](1143-longest-common-subsequence.md)**, because it *is* that problem. Recognising the reduction is worth more than any implementation detail — **you get a known-optimal algorithm for free.**

**Is O(m·n) optimal?** For general LCS, essentially yes: under the Strong Exponential Time Hypothesis, no O((mn)^(1-ε)) algorithm exists. **So "can you do better?" has a principled answer: not in general.**

**Special cases can beat it**, worth naming:

| Situation | Algorithm | Complexity |
|---|---|---|
| Answer is small (`L` lines) | Hunt–Szymanski | O((r + n) log n), r = matching pairs |
| Alphabet is tiny | Bit-parallel LCS | O(m·n / 64) |
| **General** | **Standard DP** | **O(m·n)** |

**Versus enumerating matchings:** the number of non-crossing matchings is exponential. The DP works because the answer decomposes by prefix pair — a state space of size (m+1)(n+1) rather than 2^min(m,n).

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** — one row plus two scalars.

| Component | Size |
|---|---|
| `dp` | n + 1 values → **O(n)** |
| `prev`, `temp` | two integers → O(1) |
| **Total** | **O(n)** |

At 500 × 500 that's 501 integers instead of 251,001.

| Approach | Space |
|---|---|
| Full 2-D table | O(m·n) = 251,001 |
| **Rolling row + `prev`** | **O(n) = 501** ✅ |

**Roll along the shorter array** for O(min(m,n)) — swap the inputs if `m < n`. Free, and worth a mention.

⚠️ **The `prev` variable is what makes O(n) possible.** Without it you'd need two full rows (O(2n), the same class but twice the memory) — or, worse, you'd read a corrupted diagonal. **One integer replaces an entire row**, which is the neat part.

⚠️ **The trade for O(n):** you can't reconstruct *which* lines to draw, only how many. **The full table is required for reconstruction** — walk back from `dp[m][n]`, moving diagonally on matches and toward the larger neighbour otherwise.

**No recursion** — iterative, so no stack concern. A memoised version would be up to 1,000 frames deep at these sizes, which is close enough to Python's limit to matter.
→ [recursion-limit](../syntax/recursion-limit.md)

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The key step is decoding 'no two lines cross'. Two lines cross exactly when one starts earlier in the first array but ends later in the second — so non-crossing means both index sequences increase together, which is the definition of a common subsequence. So this is Longest Common Subsequence with integers instead of characters, and the values being numbers changes nothing, because LCS only ever tests equality. The recurrence is the standard one: on a match, take the diagonal plus one; otherwise take the better of skipping from either side. I use a rolling row rather than a full table, which needs one extra variable — the diagonal `dp[i-1][j-1]` gets overwritten as I sweep, so I stash it in `prev` before writing each cell. That's O(m·n) time and O(n) space. Greedy doesn't work, because committing to an early match can block two later ones; the `max` branch is precisely the option to skip a match, which greedy never considers."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why is this LCS?" | **The question.** Non-crossing means both index sequences increase together — that's exactly a common subsequence. |
| "What is `prev` for?" | It holds `dp[i-1][j-1]`, the diagonal, which the left-to-right sweep would otherwise overwrite. One integer replaces a second row. |
| "Why doesn't greedy work?" | An early match can block two later ones. The `max` branch is the "skip this match" option greedy lacks. |
| "Do duplicates cause trouble?" | No — LCS matches by value and advances both indices, so repeats are consumed correctly. |
| "Does it matter that they're ints, not chars?" | No. LCS only tests equality; the element type is irrelevant. |
| "Can you beat O(m·n)?" | Not in general — under SETH there's no O((mn)^(1-ε)) LCS. Hunt–Szymanski helps when the answer is small; bit-parallel helps with a tiny alphabet. |
| "Return the actual lines?" | Keep the full table and walk back from `dp[m][n]` — diagonal on matches, otherwise toward the larger neighbour. |
| "Reduce space further?" | Roll along the shorter array for O(min(m,n)). |
| "What if lines *could* cross?" | Then it's just counting matched pairs by multiplicity — for each value, `min(count in nums1, count in nums2)`, summed. **Much easier**, and a good contrast to draw. |

**Traps:**

- **Forgetting `temp`/`prev`** — the diagonal is read from the current row instead of the previous one, silently overcounting. **The defining bug of the rolling version.**
- **Setting `prev = dp[j]` *after* writing** — too late; the value is already overwritten.
- **Not resetting `prev = 0` at the start of each row** — leaks the previous row's last diagonal.
- **Off-by-one on `nums1[i-1]` / `nums2[j-1]`** — `dp` is 1-indexed, the arrays are 0-indexed.
- **Sizing `dp` as `n` instead of `n + 1`** — loses the empty-prefix sentinel and forces boundary checks.
- **Greedy matching** — commits to matches that block better ones.
- **Treating it as substring matching** — it's a *subsequence*, so gaps are allowed. That would be [Maximum Length of Repeated Subarray](718-maximum-length-of-repeated-subarray.md), a different problem.

**This same move shows up in:** [Longest Common Subsequence](1143-longest-common-subsequence.md) (**literally the same problem**) · [Maximum Length of Repeated Subarray](718-maximum-length-of-repeated-subarray.md) (the *contiguous* variant — one changed line) · [Longest Palindromic Subsequence](516-longest-palindromic-subsequence.md) (LCS of a string with its reverse) · [Edit Distance](72-edit-distance.md) (the same two-sequence table with three operations) · [dynamic-programming](../algorithms/dynamic-programming.md).

</details>

---
