# 66. Plus One

**Easy** · [LeetCode](https://leetcode.com/problems/plus-one/) · [Solution file (no hints)](../../problems/0001-0499/66.py)

[📖 17. Math & Geometry lesson](../learning/19-math-geometry.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 17. Math & Geometry problems](../rmap-practice/17-math-geometry.md)

---

You're given a large integer represented as an integer array `digits`, where `digits[0]` is the **most significant** digit. Increment the integer by **one** and return the resulting array of digits.

```
digits = [1,2,3]     →  [1,2,4]        123 + 1 = 124
digits = [4,3,2,1]   →  [4,3,2,2]
digits = [9]         →  [1,0]          9 + 1 = 10 — the array grows
digits = [9,9,9]     →  [1,0,0,0]      every digit rolls over
```

**Constraints:** `1 <= digits.length <= 100` · `0 <= digits[i] <= 9` · `digits` contains no leading zeros (except the number 0 itself).

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| a number as an **array of digits** | You're doing arithmetic on a representation, not on a number. That's the point — the array can be longer than any native integer type |
| `digits[0]` is **most significant** | The array reads left-to-right like a written number, so **carrying propagates right-to-left** |
| "increment by **one**" | The simplest possible addition, which is what makes the carry logic the whole problem |
| no leading zeros | So `[0,1]` never appears as input — and the output shouldn't produce one either |
| `length <= 100` | Up to 100 digits, far beyond a 64-bit integer. **The array representation isn't decoration; it's necessary** |

The temptation on an "Easy" is to convert: join the digits into a string, `int()` it, add one, and split back out. In Python that actually **works**, because integers are arbitrary-precision. In Java or C++ it would overflow at 20 digits and fail. **The array representation exists precisely so you'll do digit arithmetic**, and treating it as a conversion exercise sidesteps the exercise.

So think about how adding one behaves, digit by digit, from the right:

- If the last digit is **less than 9**, increment it and you're done. `[1,2,3]` → `[1,2,4]`. **No carry, no further work.**
- If it's **9**, it becomes 0 and a carry moves left. `[1,2,9]` → last digit 0, carry into the 2 → `[1,3,0]`.
- The carry keeps propagating **only while it keeps hitting 9s**.

That last point is the insight worth naming: **the carry stops the instant it reaches a digit below 9.** So you don't need a general addition loop with a running carry variable — you need a loop that walks left over 9s and halts at the first non-9.

And there's exactly one case where the loop runs off the left edge: **every digit was a 9.** Then the entire array is now zeros and a leading 1 must be prepended — `[9,9,9]` → `[1,0,0,0]`. That's the only situation where the array's **length changes**.

🤔 **Before you open the next section:** the loop below returns from *inside* itself, and the `return [1] + digits` after the loop is reached only in one specific case. Which inputs reach it — and what does `digits` look like at that moment?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Convert to `int`, add, convert back | `int("".join(...)) + 1`, then split into digits | O(n) | O(n) | ⚠️ Works in Python only because ints are arbitrary-precision. **Overflows in most languages, and dodges the exercise** |
| General addition with a carry variable | Maintain `carry`, loop right-to-left adding it | O(n) | O(1) | ✅ Correct and fully general — but more machinery than "+1" needs |
| **Walk left over 9s, halt at the first non-9** | Increment and return early; prepend 1 only if all were 9 | **O(n)** | **O(1)** | ✅ |
| Recursion | Increment the last digit, recurse on carry | O(n) | O(n) stack | ⚠️ Correct, but the stack is pointless here |

**The decision:** **walk right-to-left, return as soon as a digit doesn't roll over.**

**Why the conversion approach is the wrong answer even though it passes.** With 100 digits, `int()` handles it fine in Python — but the problem gives you an array specifically because the number can exceed native integer range. An interviewer asking this wants to see **carry propagation**, and answering with a conversion is answering a different question. It's worth saying out loud: *"I could convert, since Python has big integers, but the array representation is clearly there because the number may not fit a native type, so I'll do the digit arithmetic."*

**Why no explicit `carry` variable is needed.** A general "add two numbers" routine tracks a carry because it can be 0 or 1 at any position. Here, **adding 1 means the carry is 1 at exactly the positions where it's still propagating, and 0 forever after.** So "does the carry continue?" reduces to "was this digit a 9?" — and the moment the answer is no, you're finished. The loop structure encodes the carry rather than storing it.

**Why the early return matters.** For a typical input like `[1,2,3]` the loop runs **once** and returns. Only pathological all-9s input walks the whole array. So although the worst case is O(n), the common case is O(1) — and structuring the code around an early return makes that automatic.

**Why prepending is safe** — and the answer to section 1's question. The `return [1] + digits` line is reached **only** when the loop completed without returning, meaning every digit was 9 and every one has been set to 0. So `digits` is all zeros at that point, and prepending 1 gives the correct `[1,0,…,0]`.

The alternative — `digits.insert(0, 1)` — mutates in place but is O(n) anyway (every element shifts), so `[1] + digits` is no more expensive and reads better.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
n = len(digits)
```
The digit count, used to start the reverse walk at the last index.
→ [list-basics](../syntax/list-basics.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
for i in range(n - 1, -1, -1):
```
**Walk right to left**, from the least significant digit to the most.

The three [`range`](../syntax/range-function.md) arguments are start, exclusive stop, and step: starting at `n - 1` (the last index), stopping *before* `-1` so index 0 is included, stepping by `-1`.

Direction is forced by the problem: carries propagate from the least significant digit toward the most, and `digits[0]` is the most significant.
→ [range-function](../syntax/range-function.md) · [for-loop](../syntax/for-loop.md)

```python
    if digits[i] < 9:
        digits[i] += 1
        return digits
```
**The common case, and the early exit.** A digit below 9 can absorb the +1 without rolling over — so increment it, and **everything to its left is unchanged.**

Returning immediately is what makes this O(1) on typical input. There's no need to continue: the carry has been consumed.
→ [comparison-operators](../syntax/comparison-operators.md) · [if-return](../syntax/if-return.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
    else:
        digits[i] = 0
```
**The rollover.** The digit was 9, so 9 + 1 = 10: write the 0 and let the loop carry the 1 leftward by continuing to the next iteration.

Note there's no carry variable — **continuing the loop *is* the carry.** The loop only advances left when a digit rolled over, which is exactly when a carry exists.
→ [elif-else](../syntax/elif-else.md) · [list-basics](../syntax/list-basics.md)

```python
return [1] + digits
```
**Reached only when every digit was 9** — the loop ran to completion without returning, having set every position to 0.

So `digits` is now all zeros, and the outstanding carry becomes a new leading 1: `[9,9,9]` → `[0,0,0]` → `[1,0,0,0]`.

This is the **only** case where the output is longer than the input, and it happens exactly when the input is all 9s. `[1] + digits` builds a new list rather than mutating, which is fine since we're returning it anyway.
→ [list-basics](../syntax/list-basics.md) · [if-return](../syntax/if-return.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:

        n = len(digits)

        for i in range(n - 1, -1, -1):
            if digits[i] < 9:
                digits[i] += 1
                return digits
            else:
                digits[i] = 0
        return [1] + digits
```
</details>

**Trace it** — `digits = [1, 2, 3]`

| `i` | `digits[i]` | `< 9`? | action | result |
|---|---|---|---|---|
| 2 | 3 | ✓ | increment → 4, **return** | **[1,2,4]** ✅ |

One iteration. The loop never looks at indices 1 or 0, and it doesn't need to.

**And a partial carry** — `digits = [1, 2, 9]`:

| `i` | `digits[i]` | `< 9`? | action | array after |
|---|---|---|---|---|
| 2 | 9 | ✗ | set to 0, carry left | `[1,2,0]` |
| 1 | 2 | ✓ | increment → 3, **return** | **[1,3,0]** ✅ |

The carry propagated exactly one position and stopped at the first non-9.

**And the all-9s case** — `digits = [9, 9, 9]`:

| `i` | `digits[i]` | `< 9`? | action | array after |
|---|---|---|---|---|
| 2 | 9 | ✗ | set to 0 | `[9,9,0]` |
| 1 | 9 | ✗ | set to 0 | `[9,0,0]` |
| 0 | 9 | ✗ | set to 0 | `[0,0,0]` |
| — | loop ends without returning | — | prepend 1 | **[1,0,0,0]** ✅ |

**This is the only path that reaches the final line**, and it's why that line can assume the array is all zeros. Note the output has four digits where the input had three — the single case where the length changes.

**And the smallest version** — `digits = [9]`: index 0 is a 9, set to 0, loop ends, return `[1] + [0]` = **[1,0]** ✅.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** worst case, **O(1)** best case.

- **Best case** — the last digit is below 9. One iteration, one increment, return. **O(1)**, and this covers 90% of possible inputs (any number not ending in 9).
- **Worst case** — every digit is a 9. The loop runs all n iterations, then builds a new list of n + 1 elements. **O(n)**.
- **Average** — the loop continues only while it hits 9s. For random digits the chance of k consecutive trailing 9s is 10⁻ᵏ, so the expected number of iterations is about **1.11**. Effectively constant.

At n = 100 even the worst case is trivial.

**The distinction is worth stating**, because it's the thing the early return buys: *"it's O(n) in the worst case, but the loop exits at the first digit below 9, so on typical input it's O(1)."* That's a more informative answer than "O(n)" alone, and it shows you understand where the work actually goes.

**Against the alternatives:** the conversion approach is O(n) unconditionally — you must read every digit to build the integer, and write every digit to rebuild the array. So the digit-walk version is **strictly better in the common case**, on top of not relying on arbitrary-precision integers.

**Faster?** Not in the worst case — all-9s input genuinely requires touching every digit, since every one changes. **Ω(n) worst case** is a floor.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1) usually, O(n) in the all-9s case</summary>

**O(1)** extra in every case except one, where it's **O(n)**.

| Case | Space | Why |
|---|---|---|
| Any digit below 9 exists | **O(1)** | The array is mutated in place and returned — nothing allocated |
| All digits are 9 | **O(n)** | `[1] + digits` builds a new list of n + 1 elements |

The all-9s case is unavoidable: the answer genuinely has one more digit than the input, so a longer array must exist. **You can't return an (n+1)-digit number in an n-element array.**

**A note on mutation:** this solution modifies the caller's `digits` array in place for the non-all-9s path. That's usually acceptable here (the problem returns the array anyway), but it's a side effect worth flagging — if the input needed preserving, you'd copy first at O(n).

**Could you avoid the allocation entirely?** Only by mutating in place *and* growing the array — `digits.insert(0, 1)`, which appends conceptually but shifts every element, so it's O(n) time and amortized O(1) space via the list's spare capacity. Not actually better, and less clear.

**Against the conversion approach:** that one is **O(n)** space unconditionally — the intermediate string and the rebuilt digit list both scale with n, regardless of input. So the digit walk wins here too.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "I could join the digits, convert to an int, add one, and split back — Python's integers are arbitrary-precision so it'd work — but the array representation is clearly there because the number may exceed native integer range, so I'll do the digit arithmetic. Adding one propagates a carry from right to left, and the key observation is that the carry stops the instant it hits a digit below 9. So I walk from the last digit backwards: if it's under 9, increment and return immediately — everything to the left is untouched. If it's a 9, set it to 0 and continue, which *is* the carry; no separate carry variable is needed. The loop only runs off the left edge when every digit was a 9, in which case the array is now all zeros and I prepend a 1. That's the only case where the length changes. O(n) worst case, but O(1) on any input not ending in 9."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why not convert to an integer?" | It works in Python but overflows in most languages at ~20 digits. The array representation exists precisely because the number can be 100 digits long. |
| "Why is there no carry variable?" | Because adding 1 means the carry is present exactly while digits are rolling over. Continuing the loop *is* the carry; halting at a non-9 *is* consuming it. |
| "When does the array get longer?" | Only when every digit is 9. Then all become 0 and a leading 1 is prepended. |
| "What if you had to add an arbitrary number, not 1?" | Now you need a real carry variable: `total = digits[i] + carry + addend_digit`, writing `total % 10` and carrying `total // 10`. The early-return shortcut no longer applies. |
| "Add two digit arrays together?" | Same structure as [Add Two Numbers](2-add-two-numbers.md) — walk both from the right with a carry, handling different lengths. |
| "Does this mutate the input?" | Yes, in the non-all-9s path. Copy first if the caller needs it preserved. |
| "Subtract one instead?" | Mirror image: walk right-to-left, and while a digit is 0 set it to 9 and borrow; stop at the first non-zero and decrement. Then strip any leading zero. |
| "What's the average number of iterations?" | About 1.11 for random digits — the probability of k trailing 9s is 10⁻ᵏ, so it's effectively constant. |

**Traps:**
- **Forgetting the all-9s case.** Returning `digits` after the loop gives `[0,0,0]` instead of `[1,0,0,0]` — the most commonly missed path.
- **Iterating left to right.** Carries move toward the most significant digit, which is index 0, so the walk must go right to left.
- **`range(n - 1, 0, -1)`** instead of `range(n - 1, -1, -1)` — stops before index 0 and never processes the leading digit.
- Adding a carry variable and then mishandling it. Unnecessary here, and more surface area for bugs.
- Using `digits.append(...)` or building the result forwards — the new digit goes on the **front**, not the back.
- Not returning early, and continuing to loop after the increment — harmless for correctness but it would keep zeroing digits that shouldn't change if written carelessly.

**This same move shows up in:** [Add Two Numbers](2-add-two-numbers.md) (carry propagation across a digit sequence, with a genuine carry variable) · [Multiply Strings](43-multiply-strings.md) (grade-school arithmetic on digit arrays, avoiding native integer limits) · [Happy Number](202-happy-number.md) (working with a number's decimal digits directly) · [Reverse Integer](7-reverse-integer.md) (digit-level manipulation with overflow awareness).

</details>

---
