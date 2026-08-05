# 128. Longest Consecutive Sequence

**Medium** · [LeetCode](https://leetcode.com/problems/longest-consecutive-sequence/) · [Solution file (no hints)](../../problems/0001-0499/128.py)

[📖 01. Arrays & Hashing lesson](../learning/01-arrays-hashing.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 01. Arrays & Hashing problems](../rmap-practice/01-arrays-hashing.md)

---

Given an unsorted array of integers `nums`, return the length of the **longest consecutive elements sequence**.

You must write an algorithm that runs in **O(n)** time.

```
nums = [100,4,200,1,3,2]        →  4      (the run 1,2,3,4)
nums = [0,3,7,2,5,8,4,6,0,1]    →  9      (the run 0..8)
```

**Constraints:** `0 <= nums.length <= 10⁵` · `-10⁹ <= nums[i] <= 10⁹`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**consecutive** elements" | Consecutive by **value** (`5,6,7`), not by position. Where they sit in the array is irrelevant |
| "**unsorted**" | Sorting would make this trivial — which is exactly why the next row exists |
| "must run in **O(n)**" | ⚠️ The whole challenge. Sorting is O(n log n), so **the intended solution is explicitly not the obvious one** |
| "return the **length**" | You don't have to produce the run itself, just count it |
| values up to ±10⁹, n ≤ 10⁵ | The *range* is enormous but the *count* is small — you can't index by value, so no counting-sort trick |
| `nums.length` can be **0** | Empty input must return 0, not crash |
| duplicates aren't excluded | There's a repeated `0` in the second example — duplicates must not inflate the count |

The O(n) requirement is the entire problem. Sorting is ruled out by the complexity, so you need a way to measure run lengths **without ever putting the numbers in order**.

The reframe that unlocks it: a run like `1,2,3,4` gets counted repeatedly if you start walking from every one of its members. But every run has exactly **one** starting element — and there's a local test for it: **`x` starts a run if and only if `x - 1` is absent.** Only walk from those, and each run is measured exactly once.

🤔 **Before you open the next section:** if you could ask "is the value `x` present?" in O(1), how would you find where a run *begins* — and why does only starting there keep the total work linear?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Brute force | For each `x`, scan the array for `x+1`, `x+2`, … | O(n³) | ❌ Hopeless |
| Sort, then scan | Sort and count adjacent runs | O(n log n) | ⚠️ Correct and easy — but violates the stated O(n) |
| **Hash set + start test** | Set for O(1) lookup; expand only from run starts | **O(n)** | ✅ |
| [Union-Find](../data-structures/union-find.md) | Union each `x` with `x+1`, take the largest component | ~O(n·α) | ⚠️ Works and is worth naming; far more machinery for the same result |

**The decision: a [hashset](../data-structures/hashset.md) plus the "only expand from a run start" rule.**

Two ideas doing separate jobs:

1. **The set** turns "is `x + 1` present?" into an O(1) question — the [Contains Duplicate](217-contains-duplicate.md) move — and it deduplicates for free.
2. **The start test** is what keeps it linear. Expanding from *every* element would re-walk each run once per member — `1,2,3,4` walked from 1, then from 2, then 3, then 4 — which is O(n²) on a single long run. Expanding **only** from elements with no left neighbour means each run is traversed exactly once.

Both halves are load-bearing. The set alone does not give you O(n); the start test is what earns it.

**Why not sort?** It's a perfectly good solution and you should name it as your baseline — but the problem explicitly asks for O(n), so it's the thing you're being asked to beat. Say *"sorting gives O(n log n), but I can do better"*, then do better.

**Why not union-find?** It genuinely solves it, and mentioning it shows range. But it's much heavier code for an identical answer, and its near-constant α factor buys nothing the set doesn't already provide.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
num_set = set(nums)
```

One structure, two jobs: **O(1) membership tests**, and **automatic deduplication** — so `[0,0,1]` can't count 0 twice. Building it is a single O(n) pass.
→ [set-basics](../syntax/set-basics.md)

```python
longest = 0
```

The running best. Starting at 0 is what makes empty input correct with no special handling — the loop simply never runs.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
for num in num_set:
```

Iterate the **set**, not the list. On `[5,5,5,…]` the list has n entries and the set has one, so duplicates cost nothing.
→ [for-loop](../syntax/for-loop.md)

```python
    if (num - 1) not in num_set:
```

**The line that makes it O(n).** `num` starts a run precisely when nothing sits immediately below it. If `num - 1` exists, `num` is mid-run and will be counted when we reach *that* run's start — so we skip it and do zero work.
→ [membership-operators](../syntax/membership-operators.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
        length = 1
        while (num + length) in num_set:
            length += 1
```

Confirmed start, so walk **upward**, counting. `length` serves as both the counter and the offset: when `length` is 3 we're asking whether `num + 3` exists, which is exactly the next value needed to extend the run.

It stops the instant a value is missing — that's the end of this run.
→ [while-loop](../syntax/while-loop.md)

```python
        longest = max(longest, length)
```

Keep the best run seen so far.
→ [min-max-key](../syntax/min-max-key.md)

```python
return longest
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:

        num_set = set(nums)
        longest = 0

        for num in num_set:
            if (num - 1) not in num_set:
                length = 1
                while (num + length) in num_set:
                    length += 1
                longest = max(longest, length)
        return longest
```

</details>

**Trace it** — `nums = [100, 4, 200, 1, 3, 2]`, so `num_set = {1, 2, 3, 4, 100, 200}`:

| `num` | `num - 1` present? | Start? | Work done | `longest` |
|---|---|---|---|---|
| 1 | 0 → no | ✅ | walk 2, 3, 4; 5 missing → length 4 | **4** |
| 2 | 1 → yes | ❌ | skipped | 4 |
| 3 | 2 → yes | ❌ | skipped | 4 |
| 4 | 3 → yes | ❌ | skipped | 4 |
| 100 | 99 → no | ✅ | 101 missing → length 1 | 4 |
| 200 | 199 → no | ✅ | 201 missing → length 1 | 4 |

Note the shape: only **3 of 6** elements trigger any walking, and the four members of the run `1,2,3,4` are visited by the inner loop exactly once *in total*.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** — worth being able to *defend*, because the code has a loop inside a loop and still isn't quadratic.

- Building the set: O(n).
- The outer loop: at most n iterations, each doing one O(1) membership test.
- The inner `while`: this is the interesting part.

**Why the nested loop is still linear.** The inner loop only ever runs from a **run start**, and it walks that run's members once. Distinct runs are disjoint — no value belongs to two runs — so summed across the entire outer loop the inner loop performs at most n steps **in total**. Not n steps per iteration; n steps overall.

So O(n) for the set + O(n) outer + O(n) total inner = **O(n)**.

That's an **amortized** argument, and it's the entire reason the start test exists. Delete `if (num - 1) not in num_set` and the code stays *correct* — but on `[1,2,3,…,n]` it walks the full run from every element and becomes **O(n²)**. One line separates the intended solution from a rejected one.

**Say it out loud like this:** *"Nested loops, but the inner one only runs from run starts and each run is walked exactly once — so total inner work is bounded by n, giving O(n) overall."*

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n).**

The set holds every distinct value → O(n) worst case, when all values differ. `longest` and `length` are O(1).

**Could you avoid it?** Only by sorting in place — O(1) extra space, but O(n log n) time. The trade in its clearest form:

| | Time | Space |
|---|---|---|
| Sort in place | O(n log n) | **O(1)** |
| Hash set | **O(n)** | O(n) |

You can't have both here, and the problem chose speed for you by stating O(n). Naming what you gave up — memory — is the point of the exercise.

**Why the value range doesn't matter:** values span ±10⁹, but the set stores only the n values actually present, not the range they're drawn from. An array-of-flags approach *would* be destroyed by that range — it'd need 2×10⁹ slots. This is exactly where hashing beats direct indexing.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Sorting makes this easy, but that's O(n log n) and I'm asked for O(n). So: put everything in a hash set for O(1) membership — which also deduplicates. Then the key idea is that every run has exactly one starting element, and I can detect it locally: `x` is a start if `x - 1` isn't in the set. I only expand upward from starts, so each run gets walked exactly once and the total inner work is bounded by n. O(n) time, O(n) space. Without the start check it'd still be correct, but O(n²) on a long run."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why isn't that nested loop O(n²)?" | **The question they're really asking.** Runs are disjoint and each is walked once from its start, so total inner steps ≤ n. Amortized, not per-iteration. |
| "Return the sequence, not the length." | Track the best run's starting value alongside the best length, then emit `range(start, start + longest)`. |
| "Do it in O(1) space." | Sort in place and count adjacent runs, skipping equal neighbours. O(n log n) time — trading back. |
| "What if duplicates should count?" | Then don't dedupe: keep a `Counter` and define what "consecutive" means for repeats. Clarify before coding. |
| "The values fit in a small range, say 0–1000." | Use a boolean array instead of a set — same algorithm, better constants, no hashing. |
| "Solve it with union-find." | Union each present `x` with `x+1`; the answer is the largest component size. See [union-find](../data-structures/union-find.md). |
| "Consecutive by *index* instead of value?" | A completely different problem — a linear scan, no set needed. |

**Traps:**

- **Dropping the start test.** Still correct, silently O(n²). This is *the* failure mode of this problem.
- **Iterating `nums` instead of `num_set`.** Duplicates then redo identical work — `[5] * 10⁵` degrades badly.
- **Walking downward too**, after you've already established there's nothing below. Wasted work, and it double-counts runs.
- **Initializing `longest = 1`.** Empty input then wrongly returns 1. Start at 0 and let the loop speak.
- **Off-by-one with `num + length`.** It's correct only because `length` starts at 1 — check that when you write it from memory.
- **Reaching for sorting** after being told O(n). Name it as the baseline, then beat it.

**This same move shows up in:** [Contains Duplicate](217-contains-duplicate.md) (the set-membership primitive this builds on) · [Two Sum](1-two-sum.md) (asking a hash structure a question instead of searching) · [Number of Islands](200-number-of-islands.md) (expand fully from each unvisited start, so total work stays linear — structurally the same amortized argument).

</details>

---
