# 763. Partition Labels

**Medium** · [LeetCode](https://leetcode.com/problems/partition-labels/)

[📖 16. Greedy lesson](../learning/16-greedy.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 16. Greedy problems](../rmap-practice/16-greedy.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

You're given a string `s`. Partition it into **as many parts as possible** so that each letter appears in **at most one part**. The parts, concatenated in order, must reproduce `s`. Return a list of the part sizes.

```
s = "ababcbacadefegdehijhklij"   →  [9,7,8]
        "ababcbaca" | "defegde" | "hijhklij"
        every letter is confined to exactly one part

s = "eccbbbbdec"                 →  [10]
        one part — 'e' spans from index 0 to index 8, forcing everything together
```

**Constraints:** `1 <= s.length <= 500` · `s` consists of lowercase English letters.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "as **many** parts as possible" | Optimization — but a maximization achieved by making each part as **small** as legally possible |
| "each letter in **at most one** part" | The binding constraint. If a letter appears at index 3 and again at index 20, **everything from 3 to 20 must be in the same part** |
| parts must concatenate back to `s` | The parts are **contiguous**. You're choosing cut points, not rearranging |
| lowercase letters only | At most 26 distinct characters, so any per-letter bookkeeping is O(1) space |
| `n <= 500` | Tiny. Even O(n²) would pass — so the difficulty is the insight, not the performance |

The constraint in row 2 is everything. Rephrase it as a concrete obligation:

> If a letter occurs anywhere in the current part, that part **cannot end** before that letter's **last** occurrence in the whole string.

So a part's endpoint isn't something you choose freely — it's **pushed outward** by every letter you encounter. Take `"ababcbacadefegde…"`: starting at index 0 with `'a'`, and `'a'` last appears at index 8, so the part must extend to at least index 8. Along the way you meet `'b'` (last at 5) and `'c'` (last at 7) — neither pushes further than 8. So the part ends exactly at 8.

That gives the algorithm shape: **scan forward, keeping a running "earliest possible end" that only ever grows, and cut the moment you arrive at it.**

The greedy claim is that cutting *as soon as it's legal* is optimal. That's easy to justify: if you could legally cut at index `e` but continued to some later index `e'`, you'd merge two parts that could have been separate — strictly fewer parts. **Cutting early never costs you anything, because the remainder of the string is unaffected by where the earlier cuts fell.**

🤔 **Before you open the next section:** to know how far a letter forces the part to extend, you need its **last** position — which is information about the *future*. What's the cheapest way to have that available while scanning left to right?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Try every set of cut points | Enumerate all 2ⁿ⁻¹ partitions, keep the valid one with most parts | **O(2ⁿ)** | O(n) | ❌ |
| For each candidate end, verify | At each index, re-scan to check no letter crosses the boundary | O(n²) | O(1) | ⚠️ Correct, and passes at n = 500 — but it recomputes what one pass could precompute |
| Interval merging | Turn each letter into a `[first, last]` interval and merge overlaps | O(n log n) | O(1) | ✅ Correct, and a genuinely illuminating reframing |
| **Last-occurrence map + one greedy pass** | Precompute each letter's final index, then extend a running boundary | **O(n)** | **O(1)** | ✅ |

**The decision:** **precompute last occurrences, then one greedy scan.**

**The two-pass structure is the answer to section 1's question.** The scan needs to know the future — specifically, where each letter last appears. Rather than looking ahead repeatedly (which is what makes the O(n²) version quadratic), you spend **one cheap pass up front** recording it, and the main scan becomes O(1) per character.

That's a broadly reusable pattern: **when a left-to-right greedy needs future information, precompute exactly that information in a prior pass.** Same idea as the last-index tables in string algorithms, and as the total-sum check in [Gas Station](134-gas-station.md) — establish a global fact first, then the local scan becomes trivial.

**Why the greedy is safe.** Suppose the algorithm cuts at index `e`. Every letter appearing in `[start, e]` has its last occurrence at or before `e`, so no letter leaks into a later part — the cut is **legal**. And it's **earliest**, because `e` was the maximum last-occurrence among letters seen, meaning any smaller endpoint would strand a letter. Since the parts after `e` are determined only by the suffix `s[e+1:]`, cutting as early as legally possible can only increase the total count. **Exchange argument complete.**

**Why interval merging is the same algorithm in disguise** — and worth mentioning, because it connects this to [Merge Intervals](56-merge-intervals.md). Each letter defines an interval `[first occurrence, last occurrence]`. Two letters must share a part exactly when their intervals overlap. So the answer is the set of **merged** intervals, and the part sizes are their widths. The greedy scan is precisely a merge pass that exploits the fact that the intervals are already encountered in order of their start points.

**Why not the O(n²) verification?** At n = 500 it passes fine. But it re-derives per index what one precomputation pass gives you for free, and it misses the structural insight the problem is testing.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
last_index = {char: i for i, char in enumerate(s)}
```
**The precomputation, in one line.** A [dict comprehension](../syntax/dict-comprehension.md) mapping each character to its index.

The trick is that **later assignments overwrite earlier ones**, so after the full pass every key holds that character's **last** occurrence — exactly what's needed, with no explicit `max` and no conditional. Building a *first*-occurrence map would require a membership check; last-occurrence falls out of dict semantics for free.

At most 26 entries, since the alphabet is lowercase letters.
→ [dict-comprehension](../syntax/dict-comprehension.md) · [enumerate](../syntax/enumerate.md) · [hashmap](../data-structures/hashmap.md)

```python
result = []
start = 0
end = 0
```
- **`result`** — the part sizes to return.
- **`start`** — the index where the current part begins, needed to compute its width.
- **`end`** — the current part's **earliest legal endpoint**, which grows as letters are encountered.

Both indices start at 0: the first part begins at index 0, with no constraints discovered yet.
→ [variables-assignment](../syntax/variables-assignment.md) · [list-basics](../syntax/list-basics.md)

```python
for i, char in enumerate(s):
```
The main pass, left to right. [`enumerate`](../syntax/enumerate.md) supplies both the position (to compare against `end`) and the character (to look up its last occurrence).
→ [enumerate](../syntax/enumerate.md) · [for-loop](../syntax/for-loop.md)

```python
    end = max(end, last_index[char])
```
**Push the boundary outward.** This character appears again at `last_index[char]`, so the current part cannot close before then.

`max` rather than assignment, because a later character doesn't necessarily reach further — in `"abac"`, the `'b'` at index 1 has last occurrence 1, but `end` is already 2 from the `'a'`. **Overwriting would let the part close too early and split a letter across parts.**

Identical in spirit to the frontier line in [Jump Game](55-jump-game.md): a running maximum of a constraint discovered along the way.
→ [min-max-key](../syntax/min-max-key.md) · [dict-basics](../syntax/dict-basics.md)

```python
    if i == end:
        result.append(end - start + 1)
        start = i + 1
```
**The cut.** Arriving at `end` means every letter seen in this part has already had its final occurrence — nothing inside will reappear later. The part is complete and closing it here is legal.

- `end - start + 1` is the width, inclusive of both endpoints — the `+1` is the usual inclusive-range adjustment.
- `start = i + 1` opens the next part at the following index.

Note `end` is **not** reset. It doesn't need to be: the next character's `last_index` is necessarily ≥ `i`, so the very next `max` sets it correctly. Resetting would be harmless but redundant.

And `==` rather than `>=`: since `i` advances by one and `end` only grows, arrival is exact.
→ [comparison-operators](../syntax/comparison-operators.md) · [list-methods](../syntax/list-methods.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
return result
```
The part widths, in order. No final flush is needed — the last character of the string is necessarily the last occurrence of *something*, so `i == end` always fires on the final index.
→ [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def partitionLabels(self, s: str) -> List[int]:

        last_index = {char: i for i, char in enumerate(s)}

        result = []
        start = 0
        end = 0

        for i, char in enumerate(s):
            end = max(end, last_index[char])

            if i == end:
                result.append(end - start + 1)
                start = i + 1

        return result
```
</details>

**Trace it** — `s = "ababcbacadefegdehijhklij"` (24 characters)

Last occurrences: `a:8, b:5, c:7, d:14, e:15, f:11, g:13, h:19, i:22, j:23, k:20, l:21`

| `i` | `char` | `last_index[char]` | `end` after | `i == end`? | action |
|---|---|---|---|---|---|
| 0 | a | 8 | **8** | no | — |
| 1 | b | 5 | 8 | no | — |
| 2 | a | 8 | 8 | no | — |
| 3 | b | 5 | 8 | no | — |
| 4 | c | 7 | 8 | no | — |
| 5 | b | 5 | 8 | no | — |
| 6 | a | 8 | 8 | no | — |
| 7 | c | 7 | 8 | no | — |
| 8 | a | 8 | 8 | **yes** | append `8 - 0 + 1` = **9**, `start = 9` |
| 9 | d | 14 | **14** | no | — |
| 10 | e | 15 | **15** | no | — |
| 11 | f | 11 | 15 | no | — |
| 12 | e | 15 | 15 | no | — |
| 13 | g | 13 | 15 | no | — |
| 14 | d | 14 | 15 | no | — |
| 15 | e | 15 | 15 | **yes** | append `15 - 9 + 1` = **7**, `start = 16` |
| 16 | h | 19 | **19** | no | — |
| 17 | i | 22 | **22** | no | — |
| 18 | j | 23 | **23** | no | — |
| 19 | h | 19 | 23 | no | — |
| 20 | k | 20 | 23 | no | — |
| 21 | l | 21 | 23 | no | — |
| 22 | i | 22 | 23 | no | — |
| 23 | j | 23 | 23 | **yes** | append `23 - 16 + 1` = **8** |

Return **[9, 7, 8]** ✅

Rows 1–7 show `max` doing its job: `'b'` and `'c'` both have last occurrences *before* 8, so the boundary set by `'a'` holds. Overwriting instead of maximizing would have cut at index 5 and split the `'a'`s across parts.

Rows 9–10 show the boundary being pushed twice in quick succession: `'d'` extends it to 14, then `'e'` pushes further to 15. The part can't close until the later of the two.

And row 18 is the decisive one for the third part — `'j'` last appears at 23, the very end of the string, so everything from index 16 onward is locked into a single part.

**And the single-part case** — `s = "eccbbbbdec"`:

Last occurrences: `e:8, c:9, b:6, d:7`

At `i = 0`, `'e'` sets `end = 8`. At `i = 1`, `'c'` pushes it to **9**. From there nothing exceeds 9, and `i == end` fires only at `i = 9`, appending `9 - 0 + 1` = **10**.

Return **[10]** ✅ — the interleaving of `'e'` and `'c'` across the whole string makes any cut illegal.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)**, from two linear passes.

- **Building `last_index`** — one pass over the string, one dict write per character → **O(n)**.
- **The greedy scan** — one pass, with each iteration doing a dict lookup, a `max`, and a comparison, all **O(1)** → **O(n)**.
- 2 × O(n) = **O(n)**.

At n = 500 that's a thousand operations. The constraints are generous enough that even the O(n²) approach passes — which is a sign the problem is graded on the *insight*, not the runtime.

**Against the alternatives:** enumerating partitions is **O(2ⁿ)**. Verifying each candidate boundary by re-scanning is **O(n²)** — and the only difference between that and this solution is that the future information gets computed **once** instead of repeatedly. **One precomputation pass eliminates an entire factor of n.**

The interval-merging formulation is **O(n log n)** because it sorts the 26 intervals — though with a fixed alphabet that sort is O(1), making it O(n) too.

**Faster?** No. Every character must be read at least once to know where it last appears, so **Ω(n)** is a floor.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — the `last_index` map holds at most **26 entries**, one per lowercase letter, regardless of how long the string is.

That's the technically-correct-and-worth-saying answer: it's O(alphabet size), and the alphabet is fixed by the constraints. If the input allowed arbitrary Unicode you'd call it **O(k)** for k distinct characters, bounded by n.

The `result` list is output, not working memory. `start` and `end` are two integers.

| Component | Space | Why |
|---|---|---|
| `last_index` | **O(1)** | ≤ 26 entries — bounded by the alphabet, not the input |
| `start`, `end` | O(1) | Two integers |
| `result` | O(n) *output* | At most n parts, but that's the answer being returned |

**Why nothing more is needed.** The greedy carries no history: it doesn't remember which letters it has seen, only how far they force the boundary. **A running maximum absorbs all of that information into one integer** — the same compression as the frontier in [Jump Game](55-jump-game.md) and the running sum in [Maximum Subarray](53-maximum-subarray.md).

Contrast the interval-merging view, which materializes 26 intervals and merges them. Same asymptotic space, but it makes explicit what the scan keeps implicit.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The constraint is that a letter can't span two parts — so if a letter appears in the current part, that part can't end before that letter's *last* occurrence anywhere in the string. That means a part's endpoint isn't chosen, it's pushed outward by every character I meet. So I precompute each letter's last index in one pass — a dict comprehension does it, since later writes overwrite earlier ones — then scan left to right keeping a running boundary, `end = max(end, last_index[char])`, and cut the moment I arrive at it. Cutting as early as legally possible is optimal, because the rest of the string doesn't care where earlier cuts fell, so an early cut can only increase the part count. Two linear passes, O(n) time, and O(1) space since the map is bounded by the 26-letter alphabet."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why is cutting as early as possible optimal?" | The suffix after a cut is unaffected by where earlier cuts fell. So closing a part at the first legal point can never reduce the number of parts you get later — and continuing past it would merge two parts that could have been separate. |
| "Why precompute last occurrences?" | The scan needs future information. Computing it once up front turns an O(n²) look-ahead into O(1) per character. |
| "Why `max` and not assignment?" | A later character may have an *earlier* last occurrence. In `"abac"`, `'b'` would pull the boundary back to index 1 and split the `'a'`s. |
| "Solve it as interval merging." | Each letter is an interval `[first, last]`. Letters must share a part exactly when their intervals overlap, so merge them — the merged widths are the answer. Same algorithm, made explicit. |
| "What if the alphabet were unbounded?" | Space becomes O(k) for k distinct characters, bounded by n. The algorithm is unchanged. |
| "Return the actual substrings, not sizes." | Track `start` and slice `s[start:end+1]` at each cut. Output space becomes O(n). |
| "Why no final flush after the loop?" | The last character of the string is necessarily some letter's last occurrence, so `i == end` always fires on the final index. |
| "Do you need to reset `end` after a cut?" | No — the next character's last occurrence is at least the current index, so the following `max` sets it correctly. Resetting is harmless but redundant. |

**Traps:**
- **Assigning instead of maximizing** the boundary. Splits letters across parts whenever a short-lived character follows a long-lived one.
- **Building a first-occurrence map by accident.** The dict comprehension gives *last* occurrence because later writes win — if you switch to an explicit loop with a `if char not in last_index` guard, you'd get the wrong map.
- Forgetting the `+1` in `end - start + 1`. Every part comes out one character short.
- Resetting `end = 0` after a cut and then comparing against it before the `max` — an off-by-one waiting to happen.
- Attempting to cut at the *first* occurrence of a repeated letter rather than the last.
- Using `>=` instead of `==` for the cut test. Equivalent here, but it obscures that arrival is exact.

**This same move shows up in:** [Jump Game](55-jump-game.md) (a running boundary extended by a `max`, cut/checked on arrival) · [Merge Intervals](56-merge-intervals.md) (this problem *is* interval merging, with the intervals derived from character positions) · [Gas Station](134-gas-station.md) (establish a global fact in a prior pass so the local scan becomes trivial) · [Jump Game II](45-jump-game-ii.md) (arriving at a boundary triggers an action and opens the next segment).

</details>

---
