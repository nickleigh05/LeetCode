# 678. Valid Parenthesis String

**Medium** · [LeetCode](https://leetcode.com/problems/valid-parenthesis-string/)

[📖 16. Greedy lesson](../learning/16-greedy.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 16. Greedy problems](../rmap-practice/16-greedy.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Given a string `s` containing only `'('`, `')'` and `'*'`, return `true` if it can be a **valid** parenthesis string. Each `'*'` may be treated as a single `'('`, a single `')'`, or an **empty string**.

Valid means: every `(` has a matching `)` after it, every `)` has a matching `(` before it, and they nest properly.

```
s = "()"        →  true
s = "(*)"       →  true     the * is empty (or, equivalently, unused)
s = "(*))"      →  true     the * becomes '('  →  "(())"
s = ")("        →  false    no assignment fixes the ordering
s = "((*"       →  false    one * can close at most one of the two open parens
```

**Constraints:** `1 <= s.length <= 100` · `s` consists only of `'('`, `')'` and `'*'`.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "return true/false" | Feasibility — does **some** assignment of the wildcards work? You don't have to produce it |
| `*` has **three** interpretations | Ambiguity. With k wildcards there are **3ᵏ** assignments to consider naively |
| ordering matters, not just counts | `")("` has one of each and is still invalid. Any solution must respect **position**, not merely tally |
| "every `)` has a matching `(` **before** it" | The classic prefix invariant: scanning left to right, the count of unmatched `(` must **never go negative** |
| `n <= 100` | 3¹⁰⁰ is impossible; O(n) or O(n²) is fine. So the difficulty is handling the ambiguity, not the size |

Start from the version without wildcards, [Valid Parentheses](20-valid-parentheses.md). With only one bracket type you don't even need a stack — just a counter: `+1` for `(`, `−1` for `)`, fail if it ever goes negative, and require it to end at 0.

The `*` breaks that, because now the counter isn't a single number. After processing `"(*"`, the count of unmatched `(` could be **0** (star as `)`), **1** (star empty), or **2** (star as `(`).

The naive fix is to branch — try all three at every star, 3ᵏ paths. The insight that avoids it:

> **The set of possible counts is always a contiguous range.** So track its two endpoints instead of the set.

Why contiguous? Because from any achievable count, a star lets you move `−1`, `0`, or `+1`. Applying that to an interval `[lo, hi]` gives `[lo−1, hi+1]` — still an interval, with no gaps. So the reachable counts are fully described by two numbers:

- **`low`** — the fewest unmatched `(` possible, treating stars as helpfully as possible for *closing*.
- **`high`** — the most unmatched `(` possible, treating every star as `(`.

Then the two rules from the no-wildcard version lift naturally:

- **If `high < 0`**, even the most generous interpretation has too many `)`. Unrecoverable → `false`.
- **If `low < 0`**, that particular path is dead but others survive — so **clamp `low` to 0** rather than failing.
- **At the end**, valid iff `low == 0` is achievable — i.e. some assignment leaves nothing unmatched.

🤔 **Before you open the next section:** why clamp `low` at 0 instead of letting it go negative? What would a negative "fewest unmatched open parens" even mean, and what goes wrong if you keep it?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Try all wildcard assignments | Branch three ways per `*` | **O(3ᵏ)** | O(n) | ❌ 3¹⁰⁰ |
| Recursion + memo on `(index, open_count)` | Cache each state | O(n²) | O(n²) | ⚠️ Correct, and a fine answer — but heavier than needed |
| 2-D DP over `(index, open_count)` | Fill a table of reachable counts | O(n²) | O(n²) | ⚠️ Same |
| Two stacks of indices | One for `(`, one for `*`; match `)` against `(` first, then `*`; finally pair leftovers by position | O(n) | O(n) | ✅ Correct, and a nice alternative |
| **Track the range `[low, high]`** | Two counters bounding the possible unmatched-`(` count | **O(n)** | **O(1)** | ✅ |

**The decision:** **track the interval of possible open-paren counts** with two integers.

**Why the interval trick works, stated carefully.** At every prefix, the set of achievable "unmatched `(`" counts is a contiguous range. Each character transforms it:

| character | effect on the range |
|---|---|
| `(` | both endpoints `+1` — no choice involved |
| `)` | both endpoints `−1` — no choice involved |
| `*` | `low − 1` (star as `)`) and `high + 1` (star as `(`), covering the empty case in between |

Since every transformation maps an interval to an interval, **no gaps ever appear**, and two numbers capture the full state. That's what collapses 3ᵏ branches into O(1) space — and it's the same compression idea as [Jump Game](55-jump-game.md), where reachable indices formed an interval describable by one endpoint.

**Why clamp `low` at 0** — the answer to section 1's question. A negative count of unmatched `(` is meaningless: it would represent having closed more parens than were opened, which isn't a *state*, it's a **failure** of that particular assignment. But other assignments in the range may still be alive. Clamping says *"the paths that went negative are dead; the best remaining case is 0 unmatched."* **Letting `low` drift negative would then require a spurious `)` later just to climb back**, and the final `low == 0` test would accept invalid strings.

Concretely: `"())"` — without clamping, `low` ends at `−1`, and a later `(` could push it back to 0, wrongly reporting valid.

**Why `high < 0` is fatal, though.** `high` is the *most* unmatched `(` possible. If even that is negative, then **every** interpretation has surplus `)` at this prefix — the prefix invariant is violated no matter what, and no later character can fix a `)` that already had nothing to match. Fail immediately.

**Why the final test is `low == 0`.** The valid range at the end is `[low, high]`, and it contains 0 exactly when `low <= 0 <= high`. Since `low` is clamped at ≥ 0 and `high` is guaranteed ≥ 0 (we'd have returned otherwise), the condition reduces to `low == 0`. **`low > 0` means every assignment leaves at least one `(` unmatched.**

**Why not the two-stack version?** It's O(n) time but O(n) space, and it needs a careful final step pairing leftover `(` against leftover `*` by index order. Correct and worth knowing; the range version is shorter and O(1).

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
low = 0    # fewest possible unmatched open parens
high = 0   # most possible unmatched open parens
```
The interval `[low, high]` of achievable unmatched-`(` counts. Both start at 0 — before reading anything, the only possible count is zero.

The comments matter here. **`low` assumes stars help you close; `high` assumes every star opens.** Every other line follows from those two readings.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
for char in s:
```
One left-to-right pass. Direction is essential: the prefix invariant — never more `)` than `(` so far — is inherently a left-to-right property.
→ [for-loop](../syntax/for-loop.md) · [string-basics](../syntax/string-basics.md)

```python
    if char == "(":
        low += 1
        high += 1
```
**No ambiguity.** An open paren adds one unmatched `(` under every interpretation, so the whole interval shifts up by one.
→ [comparison-operators](../syntax/comparison-operators.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
    elif char == ")":
        low -= 1
        high -= 1
```
**Also unambiguous.** A close paren consumes one unmatched `(` in every interpretation, shifting the interval down.
→ [elif-else](../syntax/elif-else.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
    else:
        low -= 1
        high += 1
```
**The wildcard, and it's the only line that widens the interval.**

- `low -= 1` — the star acts as `)`, closing an open paren (the most aggressive closing choice).
- `high += 1` — the star acts as `(`, opening one more (the most aggressive opening choice).

And the third option, empty, needs **no code at all**: it corresponds to leaving the count unchanged, which is a value strictly between `low - 1` and `high + 1` and therefore already inside the new interval. **The contiguity of the range absorbs it for free** — that's the payoff of tracking bounds rather than an explicit set.
→ [elif-else](../syntax/elif-else.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
    if high < 0:
        return False
```
**The hard failure.** `high` is the most open parens possible; if even that is negative, every interpretation has an unmatchable `)` at this point. No later character can repair it, because a `)` needs a `(` **before** it.

Checking after each character rather than at the end is what catches `")("` — by the first character, `high` is `−1`.
→ [if-return](../syntax/if-return.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
    low = max(low, 0)
```
**The clamp**, and the subtlest line in the solution.

`low` going negative means the assignments that closed most aggressively have over-closed — those paths are dead. But paths that used fewer stars as `)` are still alive, and the best of *those* leaves 0 unmatched. So the floor of the range is 0.

Without this, a negative `low` would demand extra `(` later just to return to 0, and the final `low == 0` check would pass strings like `"())("`.
→ [min-max-key](../syntax/min-max-key.md)

```python
return low == 0
```
The final range is `[low, high]`, and validity requires 0 to be in it. Since `low` is clamped at ≥ 0 and `high` ≥ 0 (or we'd have returned), that reduces to **`low == 0`**.

`low > 0` means even the most closing-friendly assignment leaves unmatched `(` — as in `"(*("`.
→ [if-return](../syntax/if-return.md) · [comparison-operators](../syntax/comparison-operators.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def checkValidString(self, s: str) -> bool:

        low = 0    # fewest possible unmatched open parens
        high = 0   # most possible unmatched open parens

        for char in s:
            if char == "(":
                low += 1
                high += 1
            elif char == ")":
                low -= 1
                high -= 1
            else:
                low -= 1
                high += 1

            if high < 0:
                return False
            low = max(low, 0)

        return low == 0
```
</details>

**Trace it** — `s = "(*))"` (should be `true`)

| char | effect | `low` | `high` | `high < 0`? | `low` after clamp |
|---|---|---|---|---|---|
| `(` | both +1 | 1 | 1 | no | 1 |
| `*` | low −1, high +1 | 0 | **2** | no | 0 |
| `)` | both −1 | −1 | 1 | no | **0** ← clamped |
| `)` | both −1 | −1 | 0 | no | **0** ← clamped |

`low == 0` → **true** ✅

The valid reading is the star as `(`, giving `"(())"`. Notice the algorithm never *chooses* that — it just keeps the range wide enough to contain it. After the star, the interval is `[0, 2]`, meaning "0, 1, or 2 unmatched open parens are all achievable," and the two closing parens bring the upper end down to 0 while the clamp holds the floor.

**And a failure from too many opens** — `s = "((*"`:

| char | effect | `low` | `high` | `high < 0`? | `low` after clamp |
|---|---|---|---|---|---|
| `(` | both +1 | 1 | 1 | no | 1 |
| `(` | both +1 | 2 | 2 | no | 2 |
| `*` | low −1, high +1 | 1 | 3 | no | **1** |

`low == 1 ≠ 0` → **false** ✅

Here the clamp never fires — `low` stays positive throughout. That's the signal: **even the most closing-friendly assignment (star as `)`) leaves one open paren stranded.** One wildcard can't close two parens.

**And an ordering failure** — `s = ")("`:

| char | effect | `low` | `high` | `high < 0`? |
|---|---|---|---|---|
| `)` | both −1 | −1 | **−1** | **yes → return false** |

**false** ✅ — caught on the very first character, because a `)` with nothing before it is unfixable regardless of what follows.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

- One pass over the string → **n iterations**.
- Each iteration does one character comparison, two integer updates, one comparison, and one `max` — all **O(1)**.
- **O(n)** total.

At n = 100 this is a hundred operations. The constraints are tiny, which again signals that the problem is graded on the **insight**, not the runtime.

**Against the alternatives:** branching on every wildcard is **O(3ᵏ)** — with up to 100 stars, 3¹⁰⁰ ≈ 10⁴⁷. Memoizing on `(index, open_count)` brings it to **O(n²)**, since there are n positions × up to n possible counts. The range trick gets **O(n)** by recognizing that the set of counts at each position is an *interval*, so it needs two numbers rather than a whole row of a DP table.

**That's the progression worth narrating in an interview:** exponential → O(n²) with memoization → O(n) by exploiting structure in the state. Each step comes from noticing something more about the problem.

**Faster?** No. Every character can flip the answer, so **Ω(n)** is a floor.

**Best case is better:** `high < 0` returns immediately, so `")"` exits after one character.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — two integers, regardless of input length. No stack, no table, no allocation.

| Approach | Space | Why |
|---|---|---|
| Recursion + memo | **O(n²)** | A cache entry per `(index, count)` state, plus O(n) stack |
| 2-D DP table | **O(n²)** | Reachable counts per position, materialized |
| Two stacks of indices | **O(n)** | Positions of unmatched `(` and unused `*` |
| **Range `[low, high]`** | **O(1)** | The set of reachable counts is an interval |

**The compression is the whole point.** A DP table would store, for each position, *which* open-paren counts are reachable — a row of booleans. But that row is never an arbitrary set: it's always a contiguous run. **Storing a contiguous run needs two numbers, not n booleans**, so the entire table collapses to two variables.

That's the same structural observation as [Jump Game](55-jump-game.md) — reachable indices form an interval, so one endpoint suffices — and it generalizes: **before building a DP table, ask what shape the reachable set has.** Intervals compress to bounds; arbitrary sets don't.

**A note on the two-stack alternative**, since it's the other common answer: push indices of `(` and `*` onto separate stacks, match each `)` against a `(` first and a `*` otherwise, then at the end pair each leftover `(` with a later `*`. It's O(n) time and O(n) space, and it has the advantage of being able to *reconstruct* a valid assignment — which the range version cannot, since it only tracks bounds.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Without the wildcards this is a counter: +1 for `(`, −1 for `)`, fail if it goes negative, end at zero. The `*` breaks that because the count becomes a *set* of possibilities. But that set is always a contiguous range — from any count, a star moves you −1, 0, or +1, so an interval maps to an interval with no gaps. So I track just the two endpoints: `low`, the fewest unmatched open parens, and `high`, the most. A `(` shifts both up, a `)` shifts both down, and a `*` widens the range in both directions — the 'empty' case needs no code because it's already inside. If `high` ever goes negative, every interpretation has an unmatchable `)`, so I fail immediately. If `low` goes negative I clamp it to zero, because a negative count isn't a state, it's a dead path — and letting it drift negative would accept strings like `"())("`. At the end, valid iff `low == 0`. O(n) time, O(1) space, versus O(3^k) brute force or O(n²) with memoization."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why clamp `low` at 0?" | A negative count of unmatched `(` isn't a real state — it means that assignment over-closed and died. Other assignments survive, and the best of them leaves 0. Without the clamp, `"())("` would be accepted. |
| "Why is `high < 0` fatal but `low < 0` not?" | `high` is the most generous interpretation. If even it has surplus `)`, every interpretation does, and a `)` needs a `(` *before* it, so nothing later can fix it. `low < 0` only kills some interpretations. |
| "Why is the reachable set always contiguous?" | Each character maps an interval to an interval: `(` and `)` shift it, `*` widens it by one in each direction. No operation can punch a hole. |
| "Why doesn't the 'empty' star case need code?" | It leaves the count unchanged, and that value already lies strictly between `low−1` and `high+1`. Contiguity absorbs it. |
| "Solve it with stacks." | One stack of `(` indices and one of `*` indices. Match `)` against `(` first, then `*`. At the end, pair each leftover `(` with a `*` that comes *after* it. O(n) time, O(n) space — but it can reconstruct an actual assignment. |
| "What if `*` could only be `(` or `)`, not empty?" | Then the parity of the string matters, and the range steps by 2 instead of 1 — you'd track `low` and `high` moving `±1` with no "stay" option, and check that 0 has the right parity. |
| "Can you produce a valid assignment?" | Not from this version — it only tracks bounds. Use the two-stack approach, which records positions. |
| "What about multiple bracket types?" | Then a counter is insufficient regardless of wildcards — you'd need a stack, as in [Valid Parentheses](20-valid-parentheses.md). |

**Traps:**
- **Omitting the `low` clamp.** Accepts invalid strings like `"())("`. The defining bug.
- **Failing when `low < 0`** instead of clamping — rejects valid strings like `"(*))"`.
- **Checking `high < 0` only at the end.** `")("` would slip through, since `high` returns to 0 by the last character.
- Returning `low == 0 and high == 0` — too strict. `high` may legitimately be positive; what matters is that 0 is *in* the range.
- Treating `*` as only `(` or only `)` rather than widening in both directions.
- Reaching for a stack because the problem mentions parentheses. With a single bracket type, counters suffice — and the wildcard is what makes it two counters instead of one.

**This same move shows up in:** [Valid Parentheses](20-valid-parentheses.md) (the no-wildcard version, where one counter — or a stack for multiple types — is enough) · [Jump Game](55-jump-game.md) (a reachable set that happens to be an interval, compressed to its endpoint) · [Merge Triplets to Form Target Triplet](1899-merge-triplets-to-form-target-triplet.md) (reasoning about what's reachable instead of simulating every choice) · [Generate Parentheses](22-generate-parentheses.md) (the open/close counting invariant, used to prune a search).

</details>

---
