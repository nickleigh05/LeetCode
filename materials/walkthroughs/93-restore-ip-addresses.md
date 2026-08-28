# 93. Restore IP Addresses

**Medium** · [LeetCode](https://leetcode.com/problems/restore-ip-addresses/) · [Solution file (no hints)](../../problems/0001-0499/93.py)

[📖 10. Backtracking lesson](../learning/10-backtracking.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 10. Backtracking problems](../rmap-practice/10-backtracking.md)

---

Given a digit string `s`, return **all valid IP addresses** obtainable by inserting dots. Digits may not be reordered or removed. A valid address is **four** integers, each **0–255**, with **no leading zeros**.

```
s = "25525511135"  →  ["255.255.11.135", "255.255.111.35"]
s = "0000"         →  ["0.0.0.0"]
s = "101023"       →  ["1.0.10.23", "1.0.102.3", "10.1.0.23", "10.10.2.3", "101.0.2.3"]
```

**Constraints:** `1 <= s.length <= 20` · `s` is digits only

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**inserting dots**", no reordering | ⚠️ This is a **partitioning** problem, not a selection problem — same shape as [Palindrome Partitioning](131-palindrome-partitioning.md) |
| "**exactly four** integers" | Fixed-depth base case: `len(path) == 4` |
| each between **0 and 255** | Segments are **at most 3 digits** → the branching factor is 3, not n |
| **no leading zeros** | `"01"` invalid, but bare `"0"` is fine. The subtle rule |
| return **all** valid | Enumerate, don't just count |
| `s.length <= 20` | ⚠️ A red herring — anything over 12 digits is **instantly impossible** |

**The reframe that makes this easy.** "Insert three dots" sounds like choosing positions. It's cleaner as: **repeatedly take a prefix of what's left**, four times.

```
"101023"

take "1"    → left: "01023"
  take "0"  → left: "1023"
    take "10" → left: "23"
      take "23" → left: "" ✅  →  1.0.10.23
```

That's exactly the [Palindrome Partitioning](131-palindrome-partitioning.md) skeleton — cut a prefix, recurse on the rest — with two changes: the depth is capped at **4**, and the validity test is "is this a legal IP segment" instead of "is this a palindrome".

**Three separate validity rules**, each of which must be checked:

| Rule | Rejects | Note |
|---|---|---|
| Length 1–3 | `"1234"` | Enforced by the loop range, not an `if` |
| No leading zero unless the segment *is* `"0"` | `"01"`, `"00"` | ⚠️ The one people get wrong |
| Value ≤ 255 | `"256"`, `"999"` | Only needs checking at length 3 |

**Why `"0000"` → `["0.0.0.0"]` is the test case that matters.** A naive leading-zero check like `if seg[0] == "0": skip` rejects the single digit `"0"` too, and returns an empty list. The rule is specifically about *leading zeros in a multi-digit segment*: `len(seg) > 1 and seg[0] == "0"`.

**The length bound nobody uses but should:** four segments of 1–3 digits means `s` must have **4 to 12 digits**. At `len(s) = 20` the answer is empty before you start.

🤔 **Before you open the next section:** if the segment starting here is `"01"` and it's rejected for a leading zero, what about `"010"`? And `"0102"`? Should the loop `continue` to the next length, or can it stop entirely?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| **Triple nested loop** | Three explicit dot positions, validate all four parts | O(1) — ≤ 27 splits | ✅ Genuinely fine here |
| Regex | Match the IP grammar over insertions | — | ❌ Awkward; doesn't enumerate cleanly |
| **Backtracking on prefixes** | Take 1–3 digits, recurse, depth 4 | **O(1)** — ≤ 27 splits | ✅ ← generalises |
| DP | Overkill — no overlapping subproblems worth caching | — | ❌ |

**The decision: backtracking, taking a 1–3 digit prefix at each of four levels.**

**Be honest that the loop version is competitive.** With exactly three dots to place and each segment 1–3 digits, there are at most **3 × 3 × 3 = 27** candidate splits (the fourth segment's length is forced by the first three). A triple `for` loop is a completely reasonable answer and some interviewers prefer it.

Backtracking wins for two reasons worth saying out loud: it **prunes** invalid prefixes instead of validating all 27 at the end, and it **generalises** — change `4` to `k` and it still works, which the hard-coded loops don't.

**The structure, against its two neighbours:**

| | [Palindrome Partitioning](131-palindrome-partitioning.md) | **Restore IP** | [Combination Sum III](216-combination-sum-iii.md) |
|---|---|---|---|
| Choice at each node | a prefix | **a prefix (1–3 chars)** | a digit |
| Validity test | is it a palindrome? | **1–3 digits, ≤ 255, no leading zero** | none |
| Base case | consumed the whole string | **4 segments *and* string consumed** | k digits *and* sum |
| Depth | up to n | **exactly 4** | exactly k |

Notice 93 and [Combination Sum III](216-combination-sum-iii.md) share the **two-condition base case** shape: the path being full is what *stops* the recursion, and a second test decides whether it *counts*.

```
len(path) == 4  and  start == len(s)   →  record
len(path) == 4  and  start <  len(s)   →  discard (digits left over)
```

Forgetting the `start == len(s)` half is the classic bug: `"101023"` would emit `1.0.1.0`, leaving `23` unconsumed.

**Three prunes, and why each is a `break` not a `continue`.** All three exploit the fact that the loop tries lengths in **increasing** order, so failure at length L implies failure at every longer length:

| Check | Why longer is also doomed |
|---|---|
| `start + length > len(s)` | Ran off the end; longer runs further off |
| `len(seg) > 1 and seg[0] == "0"` | ⚠️ The prefix still starts with `0`, so `"01"`, `"010"`, `"0102"` all fail identically |
| `int(seg) > 255` | With no leading zero, a longer digit string is a **larger** number |

The middle one is the interesting case: **once a two-digit segment is rejected for a leading zero, every longer segment from that position has the same leading zero.** `break` is correct, and skipping straight past the whole subtree.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
res = []
path = []
```

`path` holds the segments chosen so far (as strings — no need to convert back).
→ [list-basics](../syntax/list-basics.md)

```python
def backtrack(start):
    if len(path) == 4:
        if start == len(s):
            res.append(".".join(path))
        return
```

**The two-condition base case.** Four segments means stop, no matter what. Recording additionally requires `start == len(s)` — every digit consumed.

The `return` is **outside** the inner `if`, so a four-segment path with digits left over is abandoned rather than extended into a fifth segment.

`".".join(path)` builds the dotted string; since `path` holds strings already, no conversion is needed.
→ [string-join-slice](../syntax/string-join-slice.md) · [if-return](../syntax/if-return.md) · [recursion-basics](../syntax/recursion-basics.md)

```python
    for length in range(1, 4):
```

**Segment lengths 1, 2, 3** — `range(1, 4)` is exclusive at the top. This is where the "at most 3 digits" rule lives; it's structural, not an `if`.
→ [range-function](../syntax/range-function.md) · [for-loop](../syntax/for-loop.md)

```python
        if start + length > len(s):
            break
```

**Prune 1 — ran off the end.** `break`, since longer only runs further past.

```python
        segment = s[start:start + length]
        if len(segment) > 1 and segment[0] == "0":
            break
```

**Prune 2 — leading zero.** ⚠️ **The rule that decides whether `"0000"` works.**

`len(segment) > 1` is what keeps the bare `"0"` legal while rejecting `"01"`. Dropping that clause rejects `"0"` too, and `"0000"` returns `[]` instead of `["0.0.0.0"]`.

`break` and not `continue`: if `"01"` is invalid then so are `"010"` and `"0102"` — the offending zero doesn't go anywhere.
→ [string-basics](../syntax/string-basics.md) · [list-slicing](../syntax/list-slicing.md)

```python
        if int(segment) > 255:
            break
```

**Prune 3 — out of range.** Reachable only at `length == 3`. `break` is safe because leading zeros are already gone, so a longer string is strictly a larger number.
→ [type-conversion](../syntax/type-conversion.md)

```python
        path.append(segment)
        backtrack(start + length)
        path.pop()
```

**Choose, explore, un-choose.** `start + length` moves past the segment just taken — the partitioning analogue of `i + 1`.
→ [list-methods](../syntax/list-methods.md)

```python
backtrack(0)
return res
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def restoreIpAddresses(self, s: str) -> List[str]:

        res = []
        path = []

        def backtrack(start):
            if len(path) == 4:
                if start == len(s):
                    res.append(".".join(path))
                return

            for length in range(1, 4):
                if start + length > len(s):
                    break
                segment = s[start:start + length]
                if len(segment) > 1 and segment[0] == "0":
                    break
                if int(segment) > 255:
                    break

                path.append(segment)
                backtrack(start + length)
                path.pop()

        backtrack(0)
        return res
```

</details>

**Trace it** — `s = "101023"`, the whole `"1"` subtree. Verified output, including every prune:

| Depth | Action | `path` | `start` |
|---|---|---|---|
| 0 | take `"1"` | `["1"]` | 1 |
| 1 | take `"0"` | `["1","0"]` | 2 |
| 2 | take `"1"` | `["1","0","1"]` | 3 |
| 3 | take `"0"` | `["1","0","1","0"]` | 4 |
| 4 | full, but `start 4 ≠ len 6` | | **discard — digits left** ✗ |
| 3 | `"02"` leading zero | | **break** ⚠️ |
| 2 | take `"10"` | `["1","0","10"]` | 4 |
| 3 | take `"2"` → full, `start 5 ≠ 6` | | discard ✗ |
| 3 | take `"23"` → full, `start 6 == 6` | | → **record `1.0.10.23`** ✅ |
| 3 | length 3 runs past end | | **break** |
| 2 | take `"102"` | `["1","0","102"]` | 5 |
| 3 | take `"3"` → full, `start 6 == 6` | | → **record `1.0.102.3`** ✅ |
| 1 | `"01"` leading zero | | **break** ⚠️ |

Then the `"10"` subtree yields `10.1.0.23` and `10.10.2.3`, and `"101"` yields `101.0.2.3`. **Five results** ✅

**Both ⚠️ rows are the leading-zero prune**, and they're doing real work. At depth 1, rejecting `"01"` also skips `"010"` — one `break` removes two branches. Note the digit `"0"` at depth 1 was accepted *before* this: the rule fires on `"01"`, not on `"0"`.

**The discard rows show the second base-case condition earning its place.** `["1","0","1","0"]` is four perfectly valid segments — and still wrong, because `"23"` is left unconsumed. Only `start == len(s)` catches that.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(1)</summary>

**O(1)** — genuinely constant, and saying so is the right answer.

The reasoning:

- Depth is fixed at **4**.
- Branching factor is at most **3** (segment lengths 1–3).
- So at most **3³ = 27** candidate splits (the fourth length is forced by the first three).
- Each is validated and joined in O(1), since segments are ≤ 3 characters.

**27 × constant = O(1).** The input length doesn't appear, because a valid answer can only ever consume 4–12 characters — anything beyond that is unreachable.

**The output is bounded too.** The maximum number of valid addresses for any input is **19**, achieved at `s = "11111111"`:

```
1.1.111.111   1.11.11.111   1.11.111.11   1.111.1.111   1.111.11.11
1.111.111.1   11.1.11.111   11.1.111.11   11.11.1.111   11.11.11.11
11.11.111.1   11.111.1.11   11.111.11.1   111.1.1.111   111.1.11.11
111.1.111.1   111.11.1.11   111.11.11.1   111.111.1.1
```

(That's the number of ways to write 8 as an ordered sum of four terms each in {1,2,3}.)

**The general form, if pressed:** for k segments of at most m digits it's **O(mᵏ · k)**. Give that when asked to generalise — it shows you know *why* it's constant here rather than just asserting it.

**The `len(s) > 12` early exit** is worth a mention: it changes nothing asymptotically but returns instantly on the `s.length <= 20` inputs the constraints deliberately allow.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1) auxiliary**, and the output is bounded too.

| Component | Size |
|---|---|
| **Recursion depth** | exactly 4 frames → **O(1)** |
| `path` | at most 4 segments × 3 chars → **O(1)** |
| `res` | at most 19 addresses × 15 chars → **O(1)** |
| Slices `s[start:start+length]` | ≤ 3 chars each → O(1) |

Everything is bounded by a constant. **This is one of the rare problems where both time and space are honestly O(1)** — because the *structure of an IP address*, not the input, caps the work.

**The slicing is cheap here, unlike in [Palindrome Partitioning](131-palindrome-partitioning.md).** There, `s[start:i+1]` can be O(n) per cut and the slices add up. Here every slice is at most 3 characters, so slicing costs nothing. Worth noting when comparing the two — it's the same code shape with a very different cost profile.
→ [string-immutability](../syntax/string-immutability.md)

**If you wanted zero allocation**, carry `(start, length)` pairs instead of substrings and build the result string only at the base case. Pointless at these sizes, but it's the honest answer to "can you avoid the slices?"

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "I read this as a partitioning problem rather than a dot-placement one: at each level I take a prefix of one to three digits and recurse on the rest, stopping at four segments. The base case has two parts — four segments is what stops the recursion, but I only record if `start` has reached the end of the string, otherwise I'd accept an address that leaves digits unconsumed. The validity rules are length ≤ 3, value ≤ 255, and no leading zeros unless the segment is a single `0` — that last clause is what makes `'0000'` work. All three failures use `break` rather than `continue`, because lengths are tried in increasing order: if `'01'` has a leading zero then so does `'010'`. It's O(1) — depth 4, branching 3, so at most 27 splits. A triple nested loop is honestly just as good here; I prefer the backtracking because it prunes early and generalises to k segments."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why does `"0000"` work but `"0100"` reject the `01`?" | **The question.** The rule is `len(seg) > 1 and seg[0] == "0"` — bare `"0"` is legal, multi-digit with a leading zero is not. |
| "`break` or `continue` on an invalid segment?" | `break`, for all three checks. Lengths ascend, so failure at L implies failure at every longer L — including the leading-zero case, since the zero doesn't move. |
| "Why check `start == len(s)`?" | Four valid segments isn't enough; they must consume the whole string. Without it `"101023"` emits `1.0.1.0` and drops `23`. |
| "Complexity?" | O(1). Fixed depth 4, branching 3, ≤ 27 splits. Generalises to O(mᵏ·k). |
| "Faster on long inputs?" | Return `[]` immediately when `len(s) < 4 or len(s) > 12`. |
| "Do it without recursion?" | Three nested loops over the dot positions. At most 27 iterations — completely reasonable, and arguably simpler. |
| "What about **IPv6**?" | 8 groups of 1–4 hex digits, leading zeros *allowed*, plus `::` compression. Same skeleton, different validity test — a good "does he see the structure?" question. |
| "Count them instead of listing them?" | Same recursion returning an int; or DP over (position, segments used). |
| "Why not regex?" | It validates an address well but doesn't enumerate insertions cleanly. Wrong tool. |

**Traps:**

- **Rejecting the bare `"0"`.** Writing `if segment[0] == "0": break` without the length check. `"0000"` → `[]`. **The defining bug.**
- **Forgetting `start == len(s)`** in the base case — emits addresses that don't use the whole string.
- **Putting the `return` inside `if start == len(s)`** — a four-segment path with leftovers keeps recursing.
- **`range(1, 3)`** instead of `range(1, 4)` — silently never tries 3-digit segments, so `"255.255.11.135"` is missed.
- **Comparing strings instead of ints** — `"9" > "255"` is `True` lexicographically. Convert with `int()`.
- **Using `continue` on the leading-zero check** — correct but wasteful; it retests prefixes that share the same leading zero.
- **Validating only at the leaf** instead of pruning at each level — correct, but explores all 27 splits including obviously dead ones.

**This same move shows up in:** [Palindrome Partitioning](131-palindrome-partitioning.md) (the same take-a-prefix skeleton, different validity test) · [Combination Sum III](216-combination-sum-iii.md) (the same two-condition base case) · [Word Break](139-word-break.md) (prefix-splitting again, memoised) · [backtracking](../algorithms/backtracking.md).

</details>

---
