# 274. H-Index

**Medium** · [LeetCode](https://leetcode.com/problems/h-index/) · [Solution file (no hints)](../../problems/0001-0499/274.py)

[📖 01. Arrays & Hashing lesson](../learning/01-arrays-hashing.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 01. Arrays & Hashing problems](../rmap-practice/01-arrays-hashing.md)

---

Given an array `citations` where `citations[i]` is the number of citations for the researcher's `i`-th paper, return their **h-index**: the maximum value `h` such that the researcher has published at least `h` papers that have each been cited **at least `h`** times.

```
citations = [3,0,6,1,5]  →  3     (3 papers with ≥3 citations: 3, 6, 5)
citations = [1,3,1]      →  1     (1 paper with ≥1 citation)
```

**Constraints:** `n == citations.length` · `1 <= n <= 5000` · `0 <= citations[i] <= 1000`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**at least `h` papers**" with "**at least `h` citations**" | `h` appears on **both sides** — it's a self-referential threshold, which is what makes this feel slippery |
| "**maximum** value of `h`" | Among all valid `h`, take the largest. Validity is monotonic (see below), so the answer is a boundary |
| `h` is bounded by `n` | You can't have more qualifying papers than papers. So **`h ∈ [0, n]`** — a small, enumerable range |
| citations up to 1000, `n` up to 5000 | ⚠️ Citations can far **exceed** `n`. A paper with 1000 citations is capped in usefulness at `h = n` |
| `n >= 1` | Never empty, but the answer can still be **0** (e.g. `[0]`) |
| nothing about sortedness | Input is arbitrary — but sorting is legal and clarifies everything |

The definition is genuinely confusing on first read because `h` constrains itself. The clarifying reframe:

> For each candidate `h`, ask a simple yes/no question: **"do at least `h` papers have ≥ `h` citations?"** Then take the largest `h` that answers yes.

**And validity is monotonic:** if 5 papers have ≥5 citations, then certainly at least 4 papers have ≥4 citations (those same 5 qualify). So the yes-answers form a prefix `0, 1, …, h` and the no-answers follow. You're looking for the **last yes** — a boundary, not a search through scattered candidates.

That monotonicity is what makes both the sorted scan and (in the [sorted variant](https://leetcode.com/problems/h-index-ii/)) binary search valid.

🤔 **Before you open the next section:** if you sorted the citations ascending, and you're standing at index `i`, how many papers have *at least* as many citations as `citations[i]`?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Brute force | For each `h` in `n..0`, count papers with ≥ `h` citations | O(n²) | O(1) | ⚠️ Correct; 2.5·10⁷ — passes here, but sloppy |
| **Sort ascending, scan** | At index `i`, exactly `n - i` papers have ≥ `citations[i]` | **O(n log n)** | O(1)\* | ✅ Cleanest reasoning |
| Sort descending, scan | Find the last `i` where `citations[i] >= i + 1` | O(n log n) | O(1)\* | ✅ Equivalent |
| **Counting sort / bucket** | Bucket by citation count, capped at `n`; sweep down | **O(n)** | O(n) | ✅✅ Optimal |
| Binary search on `h` | Binary search `[0, n]`, O(n) count per check | O(n log n) | O(1) | ⚠️ No better than sorting |

**The decision: sort ascending, then scan** — and know the O(n) counting version for the follow-up. The solution file carries both, plus the brute force.

**The sorted-ascending insight** is worth deriving carefully, because it's the whole solution:

After sorting ascending, standing at index `i`:
- Papers at indices `i, i+1, …, n-1` all have **≥ `citations[i]`** citations (sorted!)
- That's exactly **`n - i`** papers

So define `h = n - i`. If `citations[i] >= h`, then those `n - i` papers each have at least `h` citations — **`h` is valid**. And since we scan from the smallest `i` upward, `h = n - i` starts at its **largest** and decreases, so the **first** valid one we hit is the maximum.

```
citations = [3,0,6,1,5]  →  sorted: [0, 1, 3, 5, 6]
                                     0  1  2  3  4   ← i
                              h=n-i: 5  4  3  2  1
                                           ↑
                              citations[2]=3 >= h=3 ✅  → answer 3
```

Read the picture: at `i = 2`, there are 3 papers (`3, 5, 6`) each with ≥3 citations. Exactly the definition.

**The counting-sort version** exploits the cap. A paper with 10⁶ citations is no more useful than one with `n` — because `h` can never exceed `n`. So bucket citation counts into `0..n`, lumping everything ≥ `n` into bucket `n`, then sweep `h` from `n` down accumulating "papers with ≥ h citations." First `h` where the running total reaches `h` wins. **O(n) time, O(n) space** — no comparison sort needed.

**Why not binary search here?** With unsorted input, each validity check costs O(n), so binary search gives O(n log n) — the same as just sorting, but with more moving parts. Binary search *is* the right answer for [H-Index II](https://leetcode.com/problems/h-index-ii/), where the input arrives pre-sorted and each check is O(1), yielding **O(log n)**.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

**Approach A — sort and scan** (write this one)

```python
citations.sort()
n = len(citations)
```

Ascending sort. Note this **mutates the caller's array** — worth flagging aloud; use `sorted(citations)` if that's unacceptable.
→ [sorting-key](../syntax/sorting-key.md) · [list-methods](../syntax/list-methods.md)

```python
for i, cite in enumerate(citations):
    h = n - i
```

**The count of papers from `i` onward.** Because the array is sorted ascending, every paper at index ≥ `i` has at least `citations[i]` citations — so `n - i` is precisely how many papers clear that bar.

Scanning from `i = 0` means `h` starts at `n` and decreases, so the first success is the maximum.
→ [enumerate](../syntax/enumerate.md)

```python
    if cite >= h:
        return h
```

**The validity test, straight from the definition.** `h` papers exist (indices `i..n-1`), and the *smallest* of them has `cite` citations — so if `cite >= h`, all `h` of them clear `h`. Return immediately; anything later would be smaller.
→ [comparison-operators](../syntax/comparison-operators.md) · [if-return](../syntax/if-return.md)

```python
return 0
```

No index satisfied the condition ⇒ not even `h = 1` is achievable ⇒ every paper has 0 citations. `[0, 0, 0]` is the case to check.

<details>
<summary>Approach A together</summary>

```python
class Solution:
    def hIndex(self, citations: List[int]) -> int:

        citations.sort()
        n = len(citations)

        for i, cite in enumerate(citations):
            h = n - i
            if cite >= h:
                return h

        return 0
```

</details>

---

**Approach B — counting sort** (the O(n) follow-up)

```python
n = len(citations)
counts = [0] * (n + 1)
```

`n + 1` buckets, indices `0..n`. **The cap is the point:** `h` can never exceed `n`, so citation counts above `n` are indistinguishable from `n`.
→ [list-basics](../syntax/list-basics.md)

```python
for c in citations:
    if c >= n:
        counts[n] += 1
    else:
        counts[c] += 1
```

Bucket each paper, clamping anything ≥ `n` into the top bucket. This clamping is what keeps the array size O(n) instead of O(max citation).
→ [for-loop](../syntax/for-loop.md)

```python
total_papers = 0
for h in range(n, -1, -1):
    total_papers += counts[h]
    if total_papers >= h:
        return h
```

Sweep `h` downward from `n`, accumulating. After adding `counts[h]`, `total_papers` is the number of papers with **at least** `h` citations — a suffix sum built as we go.

The first `h` where `total_papers >= h` is the answer, and because we descend, it's the largest such `h`.

`range(n, -1, -1)` counts down to and **includes** 0 — the stop value is exclusive, so `-1` is required to reach `h = 0`.
→ [range-function](../syntax/range-function.md)

<details>
<summary>Approach B together</summary>

```python
### Counting sort approach ###
class Solution:
    def hIndex(self, citations: List[int]) -> int:

        n = len(citations)
        counts = [0] * (n + 1)

        for c in citations:
            if c >= n:
                counts[n] += 1
            else:
                counts[c] += 1

        total_papers = 0
        for h in range(n, -1, -1):
            total_papers += counts[h]
            if total_papers >= h:
                return h

        return 0
```

</details>

**Trace approach A** — `citations = [3,0,6,1,5]` → sorted `[0,1,3,5,6]`, `n = 5`:

| `i` | `cite` | `h = n - i` | `cite >= h`? | Meaning |
|---|---|---|---|---|
| 0 | 0 | 5 | 0 ≥ 5? no | 5 papers exist but the weakest has 0 |
| 1 | 1 | 4 | 1 ≥ 4? no | 4 papers, weakest has 1 |
| 2 | 3 | 3 | **3 ≥ 3? yes** | 3 papers (3,5,6) each ≥3 ✅ |

Return **3**.

**Trace approach B** on the same input (`n = 5`, buckets `0..5`):

| Paper | 3 | 0 | 6 | 1 | 5 |
|---|---|---|---|---|---|
| Bucket | 3 | 0 | **5** (capped) | 1 | **5** (capped) |

`counts = [1, 1, 0, 1, 0, 2]`

| `h` | `counts[h]` | `total_papers` | `total >= h`? |
|---|---|---|---|
| 5 | 2 | 2 | 2 ≥ 5? no |
| 4 | 0 | 2 | 2 ≥ 4? no |
| 3 | 1 | **3** | **3 ≥ 3? yes** ✅ |

Return **3** ✅ — same answer, no sort.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n log n) or O(n)</summary>

| Approach | Time | Dominated by |
|---|---|---|
| Brute force | O(n²) | Counting papers for each candidate `h` |
| **Sort + scan** | **O(n log n)** | The sort; the scan is O(n) |
| **Counting sort** | **O(n)** | Two linear passes |

**Sort + scan:** the comparison sort is the bottleneck at O(n log n), and the scan adds a single O(n) pass with an early return. At n = 5000 that's trivial either way.

**Counting sort achieves O(n)** by sidestepping comparisons entirely — and it can only do so because of the cap. Bucketing normally costs O(max_value), which would be O(1000) here, or unbounded in general. Clamping at `n` makes the bucket array O(n) *regardless of how large citations get*. That's the trick, and it's the same reasoning behind [counting sort](../algorithms/counting-sort.md) and [bucket sort](../algorithms/bucket-sort.md) generally.

**Is O(n) optimal?** Yes — you must read every paper's citation count, so Ω(n) is a hard floor.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1) or O(n)</summary>

| Approach | Space | Note |
|---|---|---|
| Sort + scan | **O(1)** auxiliary | `list.sort()` is in place — though CPython's Timsort uses O(n) temp in the general case |
| Counting sort | **O(n)** | The `n + 1` bucket array |

The classic trade, inverted from the usual direction:

- Sorting: **less space, more time** — O(1) extra, O(n log n).
- Counting: **more space, less time** — O(n) extra, O(n).

Neither dominates. At n = 5000 both are instant, so prefer the one whose reasoning you can explain cleanly under pressure — usually sort + scan.

**One real consideration:** `citations.sort()` **mutates the input**. If the caller needs it preserved, `sorted(citations)` costs O(n) space and erases the sort version's only space advantage. Say this out loud — interviewers notice when you flag input mutation unprompted.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The definition is self-referential, so I'll reframe it: for a candidate `h`, do at least `h` papers have at least `h` citations? Validity is monotonic — if `h` works, so does `h-1` — so I'm looking for the boundary. If I sort ascending, then at index `i` there are exactly `n - i` papers with at least `citations[i]` citations. So I scan from the left and return `n - i` the first time `citations[i] >= n - i`, which is the largest valid `h` since `n - i` decreases. That's O(n log n) from the sort, O(1) space. There's also an O(n) counting-sort version: `h` can't exceed `n`, so I bucket citation counts capped at `n` and sweep down accumulating — first `h` where the running total reaches `h` wins."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "What if the input is already **sorted**?" | [H-Index II](https://leetcode.com/problems/h-index-ii/) — binary search the boundary in **O(log n)**, since each validity check is now O(1). |
| "Can you beat O(n log n)?" | Counting sort — O(n) time, O(n) space, using the cap at `n`. |
| "Why is capping at `n` valid?" | `h ≤ n` always, so any citation count above `n` is indistinguishable from `n` for this purpose. |
| "Why does scanning left-to-right give the *maximum*?" | `h = n - i` decreases as `i` grows, so the first success is the largest. |
| "Don't mutate the input." | `sorted(citations)` — O(n) space — or use the counting version, which never sorts. |
| "What's the answer for all zeros?" | 0. The loop never fires the condition and the final `return 0` catches it. |
| "Prove validity is monotonic." | If `h` papers have ≥ `h` citations, those same papers have ≥ `h−1` citations, and `h ≥ h−1` of them exist. So `h−1` is valid. |

**Traps:**

- **Forgetting the final `return 0`.** All-zero input falls through the loop; without it Python returns `None`.
- **Sorting descending and reusing the ascending formula.** Descending needs `citations[i] >= i + 1`, tracking the last success rather than returning on the first. Pick one orientation and derive its condition — don't mix.
- **Off-by-one in `h = n - i`.** At `i = 0` there are `n` papers, not `n - 1`. Sanity-check the endpoints.
- **`range(n, 0, -1)` in the counting version.** Stops at 1 and never tests `h = 0`. It must be `range(n, -1, -1)`.
- **Sizing the bucket array by max citation** instead of `n`. Correct but wasteful — and unbounded if citations can be huge.
- **Assuming `h` is the count of papers with the median citation** or similar shortcuts. Go back to the definition; the intuition traps are worse than the arithmetic.

**This same move shows up in:** [Sort Colors](75-sort-colors.md) (counting sort on a tiny fixed value range) · [Top K Frequent Elements](347-top-k-frequent-elements.md) (bucket sort by frequency, capped at `n` for exactly the same reason) · [Koko Eating Bananas](875-koko-eating-bananas.md) (monotonic validity predicate + binary search on the answer) · [H-Index II](https://leetcode.com/problems/h-index-ii/) (this problem with the sort already done).

</details>

---
