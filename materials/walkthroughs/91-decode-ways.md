# 91. Decode Ways

**Medium** · [LeetCode](https://leetcode.com/problems/decode-ways/)

[📖 13. 1-D Dynamic Programming lesson](../learning/14-dp-1d.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 13. 1-D Dynamic Programming problems](../rmap-practice/13-dp-1d.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

A message of letters is encoded to digits by the mapping `"A" → 1`, `"B" → 2`, …, `"Z" → 26`. Given a **digit string** `s`, return the **number of ways to decode it**. The grouping must map to a valid letter with **no leading zeros** — so `"06"` is not a valid encoding of `"F"`.

```
s = "12"      →  2      "AB" (1 2)  or  "L" (12)
s = "226"     →  3      "BZ" (2 26), "VF" (22 6), "BBF" (2 2 6)
s = "06"      →  0      leading zero — nothing decodes
s = "10"      →  1      only "J" (10); the 0 cannot stand alone
```

**Constraints:** `1 <= s.length <= 100` · `s` contains only digits, and **may contain leading zeros**.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**number of ways**" | Counting, so the combining operator is `+`. Same family as [Climbing Stairs](70-climbing-stairs.md) |
| letters map to **1–26** | At each position you consume **one digit or two** — never three, since 100 > 26. Two choices per step, exactly like a 1-or-2 staircase |
| "no leading zeros" | `"06"` ≠ `"F"`. A two-digit group must be **10–26**, not merely ≤ 26 |
| a `0` alone decodes to nothing | There's no letter 0, so a standalone `"0"` kills the entire branch. This is the constraint that turns a clean Fibonacci into a conditional one |
| `n <= 100` | Tiny. O(n) is overkill-fast; the difficulty here is **correctness on edge cases**, not performance |

The skeleton is Climbing Stairs. Stand at position `i` and ask what the *first* move can be:

- **Take one digit** — valid if `s[i]` isn't `"0"`. Then the rest is however many ways `s[i+1:]` decodes.
- **Take two digits** — valid if `s[i:i+2]` is between 10 and 26. Then the rest is however many ways `s[i+2:]` decodes.

```
ways(i) = ways(i+1)   [if s[i] ≠ "0"]
        + ways(i+2)   [if 10 ≤ int(s[i:i+2]) ≤ 26]
```

That's `f(n) = f(n-1) + f(n-2)` with **guards on each term**. On a string like `"1111"` both guards always pass and you get exact Fibonacci; the zeros and the >26 pairs are what prune it.

The two guards are where all the failures live, so read them precisely:
- `"0"` alone → **no** valid single, and if nothing pairs with it, the whole decoding dies.
- `"27"` → 27 > 26, so no pair; only two singles.
- `"06"` → the pair is 6, not "06" — a leading zero means it isn't a two-digit group at all. Testing `int(s[i:i+2]) <= 26` alone would wrongly accept it, which is exactly why the lower bound is **10**, not 1.

🤔 **Before you open the next section:** what should `ways("")` be — the number of ways to decode an empty string? Think carefully: is it 0 or 1? Your answer determines whether the whole recursion returns anything at all.

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Recursion over both splits | Try 1 digit, try 2 digits, sum | **O(2ⁿ)** | O(n) | ❌ Exponential, and subproblems repeat |
| Recursion + memo | Same, cached by index | O(n) | O(n) + stack | ⚠️ Correct, and the most natural first draft |
| DP array | `dp[i] = dp[i+1] + dp[i+2]` with guards | O(n) | O(n) | ⚠️ Correct; stores n values, reads 2 |
| **Two rolling variables** | Same recurrence, backwards, keeping two values | O(n) | **O(1)** | ✅ |

**The decision:** the guarded recurrence, computed **backwards** with two rolling variables.

**Why backwards?** Because the recurrence is naturally stated in terms of *suffixes*: `ways(i)` means "ways to decode `s[i:]`", which depends on `s[i+1:]` and `s[i+2:]`. Iterating from the end means those are already computed when you need them. You can equally define `dp[i]` over *prefixes* and go forwards — that version is just as correct and equally common. Suffix-backwards is chosen here because the base case is cleaner, which brings us to the question from section 1.

**`ways("") = 1`, not 0.** This trips everyone. The empty string has exactly **one** decoding: the empty message. Setting it to 0 makes every path multiply through zero and the answer is always 0. Think of it as *"you successfully consumed the whole string"* — reaching the end is a success, and it should be counted once. That single value seeds the entire computation.

**Why not greedy?** There's nothing to be greedy about — you're counting all possibilities, not picking one. Any approach that commits to a split loses the other branch.

**Why this is [Climbing Stairs](70-climbing-stairs.md) with guards.** Identical structure: two choices per position, sum the branches, two-cell dependency, collapse to rolling variables. The only additions are the two `if` conditions that decide whether each branch is legal. Being able to say *"this is Fibonacci where each term is conditionally included"* is the recognition move — and it tells the interviewer you see the family, not just this instance.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
n = len(s)
dp_next = 1    # ways to decode s[i + 1:]
dp_next2 = 0   # ways to decode s[i + 2:]
```
The rolling window, holding the two suffix answers the recurrence needs. Read them at the moment the loop is about to process the **last** character (`i = n-1`):

- `dp_next` = ways to decode `s[n:]` = the empty string = **1**. The base case discussed above — reaching the end is one successful decoding.
- `dp_next2` = ways to decode `s[n+1:]`, which is past the end and doesn't exist → **0**. It's never used on the first iteration anyway, because the two-digit guard `i + 1 < n` fails there.

Getting these two seeds right *is* the problem. Everything else is mechanical.
→ [variables-assignment](../syntax/variables-assignment.md) · [string-basics](../syntax/string-basics.md)

```python
for i in range(n - 1, -1, -1):
```
Walk **backwards** from the last index to 0. The three arguments to [`range`](../syntax/range-function.md) are start, stop-exclusive, step — so `-1` as the stop is what makes index 0 the final iteration, and `-1` as the step is the direction.

Backwards because `ways(i)` depends on `ways(i+1)` and `ways(i+2)`, which must already exist.
→ [range-function](../syntax/range-function.md) · [for-loop](../syntax/for-loop.md)

```python
    if s[i] == "0":
        current = 0
```
**The zero rule, and it dominates everything else.** A `"0"` can never start a group: there's no letter 0, and a two-digit group starting with 0 would have a leading zero. So *no* decoding of `s[i:]` exists that begins here → **0 ways**.

Note this doesn't mean the whole answer is 0 — the zero may still be legally absorbed as the *second* digit of a `"10"` or `"20"` pair, which happens when position `i-1` looks ahead on a later iteration. This branch only says "nothing can start here."
→ [if-return](../syntax/if-return.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
    else:
        current = dp_next
```
**Branch one: decode `s[i]` as a single letter.** Since `s[i]` isn't `"0"`, it's 1–9 — always a valid letter. So every decoding of `s[i+1:]` extends to a decoding of `s[i:]`, one-for-one.
→ [elif-else](../syntax/elif-else.md)

```python
        if i + 1 < n and 10 <= int(s[i:i + 2]) <= 26:
            current += dp_next2
```
**Branch two: decode `s[i:i+2]` as a single letter**, added to branch one because both are valid and they're distinct decodings.

Three things packed in here:
- `i + 1 < n` — there must actually *be* a second digit. Without it, the slice silently returns one character and you'd count a phantom pair.
- `10 <= … <= 26` — a [chained comparison](../syntax/chained-comparisons.md), reading as one range test. The **10** is the leading-zero rule: `"06"` converts to 6, which fails the lower bound and is correctly rejected. Writing `<= 26` alone accepts `"06"` and overcounts.
- `int(...)` — [converts](../syntax/type-conversion.md) the two-character slice to a number so it can be range-checked.

And the [`and`](../syntax/logical-operators.md) short-circuits, so the bounds check protects the slice.
→ [chained-comparisons](../syntax/chained-comparisons.md) · [type-conversion](../syntax/type-conversion.md) · [list-slicing](../syntax/list-slicing.md) · [logical-operators](../syntax/logical-operators.md)

```python
    dp_next2 = dp_next
    dp_next = current
```
Slide the window one position left. `dp_next2` must be updated **before** `dp_next` is overwritten — the same ordering constraint as [Climbing Stairs](70-climbing-stairs.md).
→ [variables-assignment](../syntax/variables-assignment.md) · [swap-tuple-assign](../syntax/swap-tuple-assign.md)

```python
return dp_next
```
After the final slide at `i = 0`, `dp_next` holds `ways(0)` — the ways to decode the whole string.
→ [if-return](../syntax/if-return.md) · [dynamic-programming](../algorithms/dynamic-programming.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def numDecodings(self, s: str) -> int:

        n = len(s)
        dp_next = 1    # ways to decode s[i + 1:]
        dp_next2 = 0   # ways to decode s[i + 2:]

        for i in range(n - 1, -1, -1):
            if s[i] == "0":
                current = 0
            else:
                current = dp_next
                if i + 1 < n and 10 <= int(s[i:i + 2]) <= 26:
                    current += dp_next2

            dp_next2 = dp_next
            dp_next = current

        return dp_next
```
</details>

**Trace it** — `s = "226"`, so `n = 3`. Start: `dp_next = 1`, `dp_next2 = 0`.

| `i` | `s[i]` | single | pair | `current` | `dp_next2` after | `dp_next` after |
|---|---|---|---|---|---|---|
| 2 | `"6"` | `dp_next` = 1 | `i+1 = 3` not < 3 → no pair | **1** | 1 | 1 |
| 1 | `"2"` | `dp_next` = 1 | `"26"` → 26 ✓ → `+dp_next2` = +1 | **2** | 1 | 2 |
| 0 | `"2"` | `dp_next` = 2 | `"22"` → 22 ✓ → `+dp_next2` = +1 | **3** | 2 | 3 |

Return **3** ✅ — `"BZ"`, `"VF"`, `"BBF"`.

**And `s = "06"`:**

| `i` | `s[i]` | `current` | `dp_next` after |
|---|---|---|---|
| 1 | `"6"` | 1 (single only) | 1 |
| 0 | **`"0"`** | **0** — nothing can start here | **0** |

Return **0** ✅ — the zero rule firing at the top level.

**And `s = "10"`:**

| `i` | `s[i]` | single | pair | `current` |
|---|---|---|---|---|
| 1 | **`"0"`** | — | — | **0** |
| 0 | `"1"` | `dp_next` = **0** | `"10"` → 10 ✓ → `+dp_next2` = +1 | **1** |

Return **1** ✅ — and this is the case worth studying. At `i = 0`, the *single*-digit branch contributes **0**, because decoding `"1"` alone strands the `"0"` with nothing to do. Only the pair `"10"` = `"J"` survives. The recurrence found that without any special-casing: the zero's own 0 propagated up and killed exactly the branch it should.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

- One backward pass over the digits → **n iterations**.
- Each iteration does a character comparison, at most one 2-character slice, one `int()` conversion, a range check, and two assignments. The slice and conversion are on a **fixed 2-character** string, so they're **O(1)** — not O(n).
- n × O(1) = **O(n)**.

At n = 100 this is 100 iterations. The constraints are nowhere near binding, which is the tell that **this problem is graded on edge cases, not speed**. Zeros, `"27"`, `"06"`, a leading `"0"` — those are what the test suite is made of.

**Against the alternatives:** the naive recursion is **O(2ⁿ)** because each position branches two ways and `ways(i)` is recomputed along many paths. Memoization collapses it to O(n) — there are only n distinct suffixes. Bottom-up gets the same without a stack.

**Faster?** No. Every digit can change the answer (a single `"0"` anywhere can zero it out), so **Ω(n)** is a floor.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — three integers (`dp_next`, `dp_next2`, `current`) plus the loop index, regardless of input length.

The 2-character slice `s[i:i+2]` allocates a tiny transient string each iteration, but it's bounded by a constant, so it doesn't affect the class.

| Version | Space | Why |
|---|---|---|
| Recursion + memo | **O(n)** | n cache entries plus up to n stack frames |
| Bottom-up DP array | **O(n)** | A `dp` array of size n + 1 |
| **Rolling variables** | **O(1)** | The recurrence reads exactly two suffixes ahead |

Same reduction as the rest of this unit, same reason: **a fixed-width dependency window needs only that many variables.** Fourth time in Unit 13 — at this point recognizing it should be automatic.

**What you'd need the array for:** listing the actual decodings rather than counting them. That's a different problem (the output can be exponential), and it'd be backtracking rather than DP.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "At each position I can consume one digit or two, and I sum both branches — so it's Climbing Stairs, but each branch is guarded. The single-digit branch is valid unless the character is '0'. The two-digit branch is valid when the pair is between 10 and 26 — and the lower bound of 10 is what enforces 'no leading zeros', since '06' converts to 6 and gets rejected. A '0' can't start any group, so its position contributes 0 ways, which then propagates and kills exactly the branches that would have stranded it. I go backwards over suffixes, and the critical base case is that the empty string has **one** decoding, not zero — if you seed that as 0 the whole answer collapses to 0. Two rolling variables, so O(n) time and O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why is `ways("") = 1`?" | The empty string has exactly one decoding — the empty message. It represents "successfully consumed the whole string," which is one valid way. Seeding 0 makes everything multiply out to 0. |
| "Why `10 <= x`, not `1 <= x`?" | Leading zeros. `"06"` converts to 6, which passes `<= 26` but isn't a valid two-digit group. The 10 rejects any pair starting with `"0"`. |
| "Walk through `"10"`." | At index 1 the `"0"` gives 0 ways. At index 0 the single-digit branch inherits that 0, so only the pair `"10"` counts → answer 1. The recurrence handles it with no special case. |
| "Do it forwards instead." | Define `dp[i]` = ways to decode the first `i` characters, with `dp[0] = 1`. Then `dp[i] += dp[i-1]` if `s[i-1] != "0"`, and `dp[i] += dp[i-2]` if `s[i-2:i]` is 10–26. Equally correct; the 1-indexing is slightly fussier. |
| "What if letters went up to 100?" | Three branches — one, two, or three digits — with a guard each, and three rolling variables. Same shape. |
| "Return the actual decodings, not the count." | Backtracking, not DP. The output can be exponentially large, so no polynomial algorithm exists for listing them. |
| "What about a string of all zeros?" | 0. The first iteration sets `current = 0`, and it stays 0 all the way up. |
| "Can `s` start with `"0"`?" | Yes — the constraints allow it, and the answer is 0. Handled by the same zero rule, no separate check needed. |

**Traps:**
- **Seeding the empty-string base case as 0.** Every answer becomes 0. The single most common failure.
- **Using `int(s[i:i+2]) <= 26` without the lower bound.** Accepts `"06"` and overcounts.
- **Forgetting `i + 1 < n`.** At the last index the slice returns one character, `int()` succeeds, and you count a two-digit group that doesn't exist.
- Treating `"0"` as merely "skip it" rather than "0 ways from here." It must zero the position out so the invalid branch dies.
- Assuming a `"0"` always makes the answer 0. `"10"` and `"20"` are fine — the zero is absorbed by the preceding digit.
- Sliding the rolling variables in the wrong order.

**This same move shows up in:** [Climbing Stairs](70-climbing-stairs.md) (the same 1-or-2 recurrence, unguarded) · [Word Break](139-word-break.md) (suffix DP over a string, asking "is there a valid split?" rather than "how many?") · [Coin Change](322-coin-change.md) (multiple guarded branches per position) · [House Robber](198-house-robber.md) (the same two-cell rolling window).

</details>

---
