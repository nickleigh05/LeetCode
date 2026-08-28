# 234. Palindrome Linked List

**Easy** · [LeetCode](https://leetcode.com/problems/palindrome-linked-list/) · [Solution file (no hints)](../../problems/0001-0499/234.py)

[📖 06. Linked List lesson](../learning/06-linked-list.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 06. Linked List problems](../rmap-practice/06-linked-list.md)

---

Given the head of a singly linked list, return `true` if it is a **palindrome** — reads the same forwards and backwards.

```
head = [1,2,2,1]  →  true
head = [1,2]      →  false
head = [1,2,3,2,1]  →  true
```

**Constraints:** `1 <= number of nodes <= 10⁵` · `0 <= Node.val <= 9`

**Follow-up:** can you do it in **O(n) time and O(1) space**?

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**palindrome**" | Compare the first half against the reversed second half |
| **singly** linked | ⚠️ Forward-only. You cannot walk backwards, which is exactly what a palindrome check wants to do |
| follow-up: **O(1) space** | Rules out copying values into an array — the easy solution |
| `n` up to 10⁵ | Recursion would blow the stack; O(n²) would be too slow |
| values are single digits | Irrelevant to the algorithm, but it means value comparison is cheap |

**Why this is harder than the array version.** On an array, [Valid Palindrome](125-valid-palindrome.md) is two converging pointers — trivial, because you can index from both ends. A singly linked list has no backward pointer, so you cannot start from the tail.

**The easy solution:** copy all values into a list, then two-pointer it. O(n) time, **O(n) space**. Correct, and the right first answer — but the follow-up explicitly asks you to beat it.

**The O(1)-space plan**, which composes three techniques you already know:

1. **Find the middle** — fast/slow pointers ([Middle of the Linked List](876-middle-of-the-linked-list.md))
2. **Reverse the second half** — in-place pointer rewiring ([Reverse Linked List](206-reverse-linked-list.md))
3. **Walk both halves inward** comparing values

```
[1] → [2] → [2] → [1]
            ↑ slow stops here

reverse from slow:   first half: 1 → 2 → ...
                     second half (reversed): 1 → 2 → None

compare pairwise: 1==1 ✅, 2==2 ✅  → palindrome
```

That decomposition is the real lesson: a Hard-feeling problem becomes three Easy ones stacked. Recognizing that a problem is a **composition of known primitives** is often more valuable than any single trick.

🤔 **Before you open the next section:** if you reverse the second half in place, where do the two halves meet — and how do you know when to stop comparing?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Copy values to a list | Then two-pointer the array | O(n) | **O(n)** | ⚠️ Correct, fails the follow-up |
| Recursion | Recurse to the end, compare unwinding | O(n) | **O(n)** stack | ❌ Overflows at 10⁵ nodes |
| Use a stack | Push the first half, pop while walking the second | O(n) | O(n/2) | ⚠️ Still linear space |
| **Find middle + reverse half + compare** | Three in-place passes | **O(n)** | **O(1)** | ✅ |

**The decision: fast/slow to find the middle, reverse the second half, then compare.**

**Step 1 — find the middle.** Standard fast/slow: `slow` advances one, `fast` two. When `fast` runs out, `slow` is at the midpoint.

With `while fast is not None and fast.next is not None`, on even lengths `slow` lands on the **first node of the second half**, which is exactly where you want to start reversing.

**Step 2 — reverse from `slow`.** The classic three-pointer reversal:

```python
prev = None
current = slow
while current:
    next_node = current.next    # save
    current.next = prev         # flip
    prev = current              # advance prev
    current = next_node         # advance current
```

Afterwards `prev` is the head of the reversed second half.

**Step 3 — compare.** Walk `first` from `head` and `second` from `prev`, comparing values until `second` runs out.

**Why stopping when `second` is exhausted is correct** — this handles both parities without a branch:

- **Even** `[1,2,2,1]`: `slow` starts at the third node, so the reversed half has 2 nodes and the first half has 2. They meet cleanly.
- **Odd** `[1,2,3,2,1]`: `slow` lands on the middle node `3`, so the reversed half has 3 nodes (`1,2,3`) and overlaps the first half at the centre. Comparing until `second` ends compares the middle against itself — harmlessly true.

So the shorter traversal (`second`) is the right loop bound, and the middle element never causes a mismatch.

**A note on the list's final state.** The reversal **mutates the input**. A polished solution restores it by reversing the second half back before returning — interviewers often ask about this, since leaving a caller's data structure corrupted is a real-world bug. The solution file *intends* to do this but the restore is incomplete (see the code notes below).

**Why not recursion?** The recursive version is elegant — recurse to the tail, then compare while unwinding against a forward pointer — but it's O(n) stack. At 10⁵ nodes Python raises `RecursionError` well before finishing.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

**Step 1 — find the middle**

```python
slow = head
fast = head

while fast is not None and fast.next is not None:
    slow = slow.next
    fast = fast.next.next
```

Fast/slow pointers, exactly as in [Middle of the Linked List](876-middle-of-the-linked-list.md). Both guards are needed before `fast.next.next`.

When this ends, `slow` marks where the second half begins.
→ [while-loop](../syntax/while-loop.md) · [logical-operators](../syntax/logical-operators.md) · [none-type](../syntax/none-type.md)

---

**Step 2 — reverse the second half**

```python
prev = None
current = slow

while current is not None:
    next_node = current.next
    current.next = prev
    prev = current
    current = next_node
```

**The four-line reversal, and the order is non-negotiable:**

1. `next_node = current.next` — **save** the rest before you destroy the link
2. `current.next = prev` — **flip** the pointer backwards
3. `prev = current` — advance `prev`
4. `current = next_node` — advance `current` using the saved reference

Skip step 1 and you lose the remainder of the list irrecoverably. This is the single most important sequence in linked-list manipulation — see [Reverse Linked List](206-reverse-linked-list.md).

After the loop, `prev` heads the reversed second half.
→ [variables-assignment](../syntax/variables-assignment.md)

---

**Step 3 — compare the halves**

```python
first_half_pointer = head
second_half_pointer = prev
is_palindrome = True

while second_half_pointer is not None:
    if first_half_pointer.val != second_half_pointer.val:
        is_palindrome = False
        break
    first_half_pointer = first_half_pointer.next
    second_half_pointer = second_half_pointer.next
```

Walk both inward-facing halves in lockstep.

**Looping on `second_half_pointer`** is what makes odd and even lengths both work — it's the shorter (or equal) traversal, and on odd lengths the overlapping middle node compares against itself.

`break` exits early on the first mismatch; there's no point continuing.
→ [break-continue](../syntax/break-continue.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
prev = None
current = second_half_pointer if second_half_pointer is None else None
current = slow

return is_palindrome
```

⚠️ **Those three lines before the `return` are vestigial.** They set up variables that are never used — an unfinished attempt to reverse the second half back and restore the original list. `prev` and `current` are assigned and then immediately discarded, so they have **no effect** on the result.

The function is still **correct** — `is_palindrome` was already determined — but the list is left with its second half reversed. If you want the restore, the completed version is:

```python
# restore: reverse the second half back
prev2 = None
current = prev            # head of the reversed half
while current is not None:
    nxt = current.next
    current.next = prev2
    prev2 = current
    current = nxt

return is_palindrome
```

Worth cleaning up in your own copy — dead code that *looks* meaningful is worse than no code at all.

<details>
<summary>The whole thing together (as in the solution file)</summary>

```python
class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:

        slow = head
        fast = head
        while fast is not None and fast.next is not None:
            slow = slow.next
            fast = fast.next.next

        prev = None
        current = slow
        while current is not None:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node

        first_half_pointer = head
        second_half_pointer = prev
        is_palindrome = True
        while second_half_pointer is not None:
            if first_half_pointer.val != second_half_pointer.val:
                is_palindrome = False
                break
            first_half_pointer = first_half_pointer.next
            second_half_pointer = second_half_pointer.next

        prev = None
        current = second_half_pointer if second_half_pointer is None else None
        current = slow

        return is_palindrome
```

The last three lines before the `return` are dead — see the note above.

</details>

**Trace the even case** — `[1,2,2,1]`:

*Find the middle:*

| `slow` | `fast` | Continue? |
|---|---|---|
| 1₁ | 1₁ | ✅ |
| 2₁ | 2₂ | ✅ (`fast.next` = 1₂ exists) |
| 2₂ | `None` | ❌ stop |

`slow` = 2₂ — the first node of the second half ✅

*Reverse from `slow`:* the second half `2₂ → 1₂` becomes `1₂ → 2₂ → None`, so `prev` = 1₂.

*Compare:*

| `first` | `second` | Equal? |
|---|---|---|
| 1₁ | 1₂ | ✅ |
| 2₁ | 2₂ | ✅ |
| 2₂ | `None` | loop ends |

Return **`True`** ✅

**Trace the odd case** — `[1,2,3,2,1]`:

*Find the middle:* `slow` ends at the node `3` (the centre).

*Reverse from `slow`:* `3 → 2₂ → 1₂` becomes `1₂ → 2₂ → 3`, so `prev` = 1₂.

*Compare:*

| `first` | `second` | Equal? |
|---|---|---|
| 1₁ | 1₂ | ✅ |
| 2₁ | 2₂ | ✅ |
| 3 | 3 | ✅ (**the middle against itself**) |
| — | `None` | loop ends |

Return **`True`** ✅ — the overlapping centre node compares to itself and never causes a false mismatch.

**A failing case** — `[1,2]`: `slow` ends at node 2, reversal makes `prev` = 2, and the first comparison is `1 != 2` → `break` → **`False`** ✅

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

Three sequential passes, each linear:

| Phase | Cost |
|---|---|
| Find the middle | `n/2` iterations (`fast` covers `n`) |
| Reverse the second half | `n/2` |
| Compare | `n/2` |

Total ≈ `1.5n` pointer operations — **O(n)**. Adding the optional restore makes it `2n`, still O(n).

**Compare to the array approach:** also O(n) time, but O(n) space. The three-pass version trades a couple of extra traversals for constant memory — usually the right call, and exactly what the follow-up asks.

**Recursion is also O(n) time** but with O(n) stack, which at 10⁵ nodes means `RecursionError` rather than a slow answer. See [recursion-limit](../syntax/recursion-limit.md).

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — a fixed set of pointers, no allocation regardless of list length.

| | Space |
|---|---|
| Copy values to a list | O(n) |
| Recursion | O(n) stack |
| Stack of the first half | O(n/2) |
| **Middle + reverse + compare** | **O(1)** ✅ |

**The cost is mutation.** The reversal edits the caller's list in place. Three positions to take:

1. **Restore it** — reverse the second half back before returning. Best practice, and what an interviewer usually wants to hear.
2. **Document it** — acceptable if the caller doesn't care.
3. **Ignore it** — what the solution file effectively does, since its restore is incomplete.

Say this unprompted. "It's O(1) space, but it mutates the input — I'd reverse the second half back before returning" is exactly the kind of remark that separates a careful answer from a memorized one.

**The composition lesson**, which is the real value here:

> This problem is [Middle of the Linked List](876-middle-of-the-linked-list.md) + [Reverse Linked List](206-reverse-linked-list.md) + a comparison walk. None of the pieces are hard; recognizing the decomposition is the skill.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The easy version copies the values into an array and uses two converging pointers — O(n) time but O(n) space. For the O(1)-space follow-up I compose three things I already know. First, fast/slow pointers to find the middle. Second, reverse the second half in place with the standard save-flip-advance loop. Third, walk the first half and the reversed second half in lockstep comparing values, looping until the second half is exhausted — that bound handles odd lengths automatically, because the middle node ends up compared against itself. O(n) time, O(1) space. It does mutate the list, so I'd reverse the second half back before returning if the caller needs the original structure."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "O(1) space?" | **The stated follow-up** — find the middle, reverse the second half, compare. |
| "You mutated the input." | Reverse the second half back before returning. Still O(n)/O(1). |
| "How do odd lengths work?" | `slow` lands on the middle, so the reversed half includes it; looping on the second pointer compares it against itself. |
| "Do it recursively." | Recurse to the tail, compare while unwinding against a forward pointer. O(n) stack — `RecursionError` at 10⁵ nodes. |
| "Why not use a stack?" | Push the first half, pop while walking the second. Correct, but O(n/2) space. |
| "What if it were **doubly** linked?" | Trivial — two converging pointers from both ends, exactly like [Valid Palindrome](125-valid-palindrome.md). |
| "Those last three lines don't do anything." | Correct — they're a vestigial restore attempt. The result is unaffected; they should be deleted or completed. |

**Traps:**

- **Forgetting to save `next_node` during reversal.** Destroys the rest of the list. The single most common linked-list bug.
- **Looping the comparison on the first-half pointer.** It's longer on odd lengths and walks past the end.
- **Mishandling odd lengths with an explicit special case.** Unnecessary — the loop bound handles it.
- **Recursing at 10⁵ nodes.** Stack overflow.
- **Leaving the list mutated without mentioning it.** Correct output, but a real-world bug; say it out loud.
- **Leaving dead code in place.** The three vestigial lines here look purposeful and aren't — that's worse than omitting the restore entirely.

**This same move shows up in:** [Middle of the Linked List](876-middle-of-the-linked-list.md) (step 1 in isolation) · [Reverse Linked List](206-reverse-linked-list.md) (step 2 in isolation) · [Reorder List](143-reorder-list.md) (the same middle-then-reverse decomposition, then interleave) · [Valid Palindrome](125-valid-palindrome.md) (the array version, where random access makes it trivial).

</details>

---
