# 202. Happy Number

**Easy** · [LeetCode](https://leetcode.com/problems/happy-number/)

[📖 18. Math & Geometry lesson](../learning/18-math-geometry.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 18. Math & Geometry problems](../rmap-practice/18-math-geometry.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

A **happy number** is defined by this process: starting with any positive integer, replace it with **the sum of the squares of its digits**, and repeat. The number is happy if this eventually reaches **1**; if it loops endlessly without reaching 1, it is not.

Return `true` if `n` is happy.

```
n = 19  →  true
        1² + 9² = 82
        8² + 2² = 68
        6² + 8² = 100
        1² + 0² + 0² = 1  ✓

n = 2   →  false
        4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4 → …  (cycles)
```

**Constraints:** `1 <= n <= 2³¹ − 1`.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**repeat** the process" | An iterative sequence where each value determines the next — a **deterministic** function applied over and over |
| "eventually reaches 1" | One terminating condition |
| "or **loops endlessly**" | The other. And "endlessly" is the giveaway — you can't detect an infinite loop by waiting, you have to detect a **repeat** |
| deterministic transformation | Once a value recurs, the entire sequence from that point repeats identically. **A repeat *is* a cycle** |
| `n` up to 2³¹ − 1 | Ten digits at most — which turns out to bound the whole problem |

Two things need establishing before you can write anything.

**First: why must the sequence terminate or cycle — why can't it just grow forever?**

Because squaring digits **shrinks large numbers dramatically**. For a `d`-digit number the maximum possible next value is `d × 81` (all nines). Compare that against the smallest `d`-digit number, `10^(d-1)`:

| digits `d` | largest input | max next value (`d × 81`) |
|---|---|---|
| 4 | 9,999 | 324 |
| 10 | 9,999,999,999 | 810 |

So any number with 4+ digits immediately drops below 1000. And once below 1000, the next value is at most `3 × 81 = 243`. **The sequence is trapped in the range 1–243 within a couple of steps**, forever.

That's the key structural fact: **a finite state space with a deterministic transition function must eventually repeat.** It cannot escape upward, so by the pigeonhole principle it either hits 1 or revisits a value it has seen — and revisiting means it will revisit forever.

**Second: what kind of problem is this, really?**

Once you see "deterministic function, finite states, does it reach a target or loop," this is **cycle detection** — exactly [Linked List Cycle](141-linked-list-cycle.md), with `next_number(x)` playing the role of `node.next`. The "linked list" is implicit: nodes are integers, and the pointer is the digit-square-sum function.

That reframing is the whole insight. **A number-theory-flavoured problem is actually a graph traversal in disguise.**

🤔 **Before you open the next section:** if this is [Linked List Cycle](141-linked-list-cycle.md) in disguise, and that problem has a famous O(1)-space solution, what would that look like here — and would it need any extra machinery?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Loop with an iteration cap | Run ~1000 steps; if 1 hasn't appeared, call it unhappy | O(1) | O(1) | ❌ Correct only by luck — the bound is a guess, not a proof |
| **Hash set of seen values** | Stop when a value repeats | O(log n) | **O(1)** bounded | ✅ |
| [Floyd's cycle detection](../algorithms/floyd-cycle-detection.md) | Slow and fast pointers; they meet inside a cycle | O(log n) | **O(1)** genuinely | ✅ No set at all |
| Hard-code the known cycle | Check membership in `{4,16,37,58,89,145,42,20}` | O(log n) | O(1) | ⚠️ Works — every unhappy number reaches that one cycle — but it's memorized trivia, not reasoning |

**The decision:** the **hash set**, with Floyd's as the O(1)-space alternative worth naming.

**Why the set is the right default.** It expresses the reasoning directly: *"if I ever see a value twice, the sequence will repeat forever, so it's not happy."* No cleverness, no cycle-structure knowledge, and it's obviously correct.

**Why Floyd's is the interesting follow-up** — the answer to section 1's question. Since this is [Linked List Cycle](141-linked-list-cycle.md) with `next_number` as the pointer, [Floyd's tortoise and hare](../algorithms/floyd-cycle-detection.md) transfers with **no adaptation at all**:

```python
slow = n
fast = next_number(n)
while fast != 1 and slow != fast:
    slow = next_number(slow)
    fast = next_number(next_number(fast))
return fast == 1
```

Two variables, no set. If there's a cycle the fast pointer laps the slow one and they meet; if the sequence reaches 1, `next_number(1) = 1` is a fixed point and the fast pointer parks there. **Recognizing that the linked-list technique applies to a numeric sequence is the strongest thing you can demonstrate on this problem.**

**Why the hard-coded cycle works but shouldn't be your answer.** It's a genuine mathematical fact that **every** unhappy number eventually reaches the cycle `4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4`, so testing membership in that set is correct. But it's recall, not derivation — and if the problem changed to cubes of digits, the fact evaporates while the set and Floyd's approaches keep working unchanged.

**Why the iteration cap is not acceptable.** "Loop 1000 times and give up" happens to work, but you'd be asserting a bound you haven't justified. **The pigeonhole argument is what makes the termination rigorous**, and once you have it, you may as well detect the repeat directly.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
def next_number(num):
    total = 0
    while num:
        digit = num % 10
        total += digit * digit
        num //= 10
    return total
```
**The transformation, extracted as a helper.** Isolating it keeps the main loop about *cycle detection* rather than digit arithmetic — and it's what makes swapping in Floyd's algorithm a two-line change.

The digit extraction is the standard idiom:
- **`num % 10`** — the last digit ([modulo](../syntax/integer-division-modulo.md)).
- **`num //= 10`** — drop it with floor division.
- **`while num:`** — loop until nothing remains, relying on `0` being [falsy](../syntax/truthy-falsy-values.md).

Doing it arithmetically rather than via `str(num)` avoids the string conversion, though `sum(int(d)**2 for d in str(num))` is a perfectly readable alternative worth mentioning.
→ [integer-division-modulo](../syntax/integer-division-modulo.md) · [while-loop](../syntax/while-loop.md) · [truthy-falsy-values](../syntax/truthy-falsy-values.md) · [function-basics](../syntax/function-basics.md)

```python
seen = set()
```
Every value the sequence has produced. A [set](../data-structures/hashset.md) rather than a list, because the only operation is membership testing — **O(1) average versus O(n) for a list scan**.
→ [set-basics](../syntax/set-basics.md) · [hashset](../data-structures/hashset.md)

```python
while n != 1 and n not in seen:
    seen.add(n)
    n = next_number(n)
```
**The two exit conditions, both in the loop header.**

- **`n != 1`** — reaching 1 means happy; stop.
- **`n not in seen`** — a repeat means the sequence will cycle forever from here; stop.

The pigeonhole argument from section 1 guarantees **one of these must eventually fire**, since the values are confined to a finite range and the transition is deterministic. Without that argument, this loop would just be hopeful.

Order inside the body matters: add `n` to `seen` **before** advancing, so the current value is recorded before it's replaced.
→ [while-loop](../syntax/while-loop.md) · [logical-operators](../syntax/logical-operators.md) · [membership-operators](../syntax/membership-operators.md) · [set-operations](../syntax/set-operations.md)

```python
return n == 1
```
**Disambiguate which condition ended the loop.** If `n` is 1 the number is happy; otherwise the loop exited on a repeat, meaning a cycle.

This is neater than returning `True`/`False` from inside the loop — one exit point, and the condition reads as the definition of the problem.
→ [if-return](../syntax/if-return.md) · [comparison-operators](../syntax/comparison-operators.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def isHappy(self, n: int) -> bool:

        def next_number(num):
            total = 0
            while num:
                digit = num % 10
                total += digit * digit
                num //= 10
            return total

        seen = set()
        while n != 1 and n not in seen:
            seen.add(n)
            n = next_number(n)

        return n == 1
```
</details>

**Trace it** — `n = 19`

| `n` | in `seen`? | `seen` after add | `next_number(n)` |
|---|---|---|---|
| 19 | no | `{19}` | 1² + 9² = **82** |
| 82 | no | `{19, 82}` | 8² + 2² = **68** |
| 68 | no | `{19, 82, 68}` | 6² + 8² = **100** |
| 100 | no | `{19, 82, 68, 100}` | 1² + 0² + 0² = **1** |
| **1** | loop exits on `n != 1` | — | — |

Return `1 == 1` → **true** ✅

**And the unhappy case** — `n = 2`:

| `n` | in `seen`? | next |
|---|---|---|
| 2 | no | **4** |
| 4 | no | **16** |
| 16 | no | 1 + 36 = **37** |
| 37 | no | 9 + 49 = **58** |
| 58 | no | 25 + 64 = **89** |
| 89 | no | 64 + 81 = **145** |
| 145 | no | 1 + 16 + 25 = **42** |
| 42 | no | 16 + 4 = **20** |
| 20 | no | 4 + 0 = **4** |
| **4** | **yes — already in `seen`** | loop exits |

Return `4 == 1` → **false** ✅

The cycle closed after 8 distinct values. Notice the sequence never climbed above 145 — that's the trapping behaviour from section 1, and it's why the set stays tiny.

**And the shrinking, on a large input** — `n = 2147483647` (the maximum allowed):

| step | value | digits | next |
|---|---|---|---|
| 1 | 2,147,483,647 | 10 | 4+1+16+49+16+64+9+36+16+49 = **260** |
| 2 | 260 | 3 | 4 + 36 + 0 = **40** |
| 3 | 40 | 2 | 16 + 0 = **16** |

**One step took a ten-digit number down to 260.** From there it joins the familiar territory below 243 and resolves quickly — in this case into the same `4 → 16 → …` cycle, so the answer is **false**.

That collapse is why the iteration count is essentially independent of how large `n` is.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(log n)</summary>

**O(log n)**, and the analysis is more interesting than the bound.

- **`next_number`** processes one digit per loop, and `n` has **⌊log₁₀ n⌋ + 1** digits → **O(log n)** per call.
- **The number of calls** is where the pigeonhole argument pays off. After **one** step, any input collapses to at most `10 × 81 = 810`. After that, every value is at most `3 × 81 = 243`. So the sequence is confined to `1..243` and must reach 1 or repeat within **at most 243 steps** — a **constant**, independent of `n`.
- Total: **O(log n)** for the first call, plus O(1) calls each on tiny numbers → **O(log n)**.

In practice the cycle closes in well under 20 steps, as both traces show.

**The important framing:** the input size barely matters. A 10-digit number and a 3-digit number take almost the same number of iterations, because the very first step destroys the magnitude. **The digit-sum-of-squares operation is enormously contractive**, and that's what makes the problem tractable at all.

**Against the alternatives:** Floyd's version is also **O(log n)** — it performs about 3× the `next_number` calls (the fast pointer moves twice per step) but has the same asymptotic behaviour. The hard-coded-cycle version is likewise O(log n), just with a smaller constant.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — and this is worth stating carefully, because the "obvious" answer is O(k) for k distinct values seen.

The set can only ever hold values from the trapped range. After the first step, every value is **≤ 810**, and thereafter **≤ 243**. So `seen` is bounded by a **constant** — at most a couple of hundred entries, no matter how large `n` is.

| Component | Space | Why |
|---|---|---|
| `seen` | **O(1)** | Bounded by ~250 values, independent of n |
| `next_number` locals | O(1) | Two integers |

**So calling it O(1) is correct**, and being able to justify *why* — via the same shrinking argument that bounds the running time — is what separates a real analysis from a hand-wave. Saying "O(k) where k is the number of values seen" isn't wrong, but it misses that k is bounded.

**Floyd's version is O(1) in the stronger sense** — two integer variables and no collection at all:

```python
slow = n
fast = next_number(n)
while fast != 1 and slow != fast:
    slow = next_number(slow)
    fast = next_number(next_number(fast))
return fast == 1
```

Both are O(1), but Floyd's has no allocation whatsoever, which matters if you're arguing constant space without relying on the boundedness argument. **It's the better answer when the interviewer asks for O(1) space explicitly** — and it's a direct lift from [Linked List Cycle](141-linked-list-cycle.md).

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The first thing to establish is that this always terminates or cycles — it can never grow without bound. For a d-digit number the next value is at most 81d, so anything with four or more digits immediately drops below 1000, and from there it's capped around 243. So the sequence is trapped in a small finite range with a deterministic transition, which by pigeonhole means it must eventually repeat. That makes this a **cycle detection** problem — it's Linked List Cycle with `next_number` as the pointer. I use a hash set: if a value repeats before I hit 1, it's not happy. Time is O(log n), dominated by the first digit-sum on a large input, since after that the values are tiny and the iteration count is constant. Space is O(1), because the set is bounded by that same trapped range. And since it's really cycle detection, I could use Floyd's tortoise and hare instead for genuinely allocation-free O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "How do you know it terminates?" | A d-digit number maps to at most 81d, which is far below the smallest d-digit number once d ≥ 4. So values collapse below 1000 immediately and stay under ~243. Finite states plus a deterministic transition means it must repeat. |
| "Do it in O(1) space." | [Floyd's cycle detection](../algorithms/floyd-cycle-detection.md) — slow advances one step, fast two; they meet in a cycle, or fast reaches 1, which is a fixed point. Two variables, no set. |
| "Why is the set O(1) rather than O(k)?" | Because k is bounded — the sequence can't escape the range 1–243 after the first couple of steps, so the set holds at most a couple of hundred values regardless of n. |
| "What's the actual cycle?" | Every unhappy number reaches `4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4`. You could test membership in that set, but it's a memorized fact rather than derived. |
| "What if it were cubes of digits instead of squares?" | The set and Floyd's approaches work unchanged — only the bound shifts (a d-digit number maps to at most 729d). The hard-coded cycle would be wrong. |
| "Why not just loop a fixed number of times?" | It'd happen to work, but you'd be asserting a bound with no justification. The pigeonhole argument is what makes termination rigorous. |
| "Can you compute the digit sum differently?" | `sum(int(d)**2 for d in str(n))` is more readable; the arithmetic version avoids the string conversion. Same complexity. |
| "What about `n = 1`?" | The loop condition fails immediately and it returns `True`. 1 is happy by definition. |

**Traps:**
- **Adding `n` to `seen` after advancing** — the current value never gets recorded, so cycles are missed and the loop runs forever.
- **Checking `n in seen` before adding the first value** in a way that lets the initial `n` slip through unrecorded.
- Using a list instead of a set — correct, but membership becomes O(k) per check.
- Returning `True` when the loop ends, without checking *which* condition fired.
- Assuming any repeat means unhappy — true here, but only because 1 is checked first; `next_number(1) = 1` is itself a cycle.
- Hard-coding the known cycle as your primary answer. It's correct and it's recall, not reasoning.

**This same move shows up in:** [Linked List Cycle](141-linked-list-cycle.md) (the same cycle detection, where the "next" function is a real pointer — this problem is that one in disguise) · [Find the Duplicate Number](287-find-the-duplicate-number.md) (Floyd's algorithm applied to an array read as an implicit linked list) · [Reverse Integer](7-reverse-integer.md) (the same `% 10` / `// 10` digit-extraction idiom) · [Plus One](66-plus-one.md) (digit-level arithmetic on a number's decimal representation).

</details>

---
