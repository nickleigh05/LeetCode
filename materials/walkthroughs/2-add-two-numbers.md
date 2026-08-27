# 2. Add Two Numbers

**Medium** · [LeetCode](https://leetcode.com/problems/add-two-numbers/)

[📖 06. Linked List lesson](../learning/06-linked-list.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 06. Linked List problems](../rmap-practice/06-linked-list.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

You're given two non-empty linked lists representing two non-negative integers. The digits are stored in **reverse order**, one digit per node. Add the two numbers and return the sum as a linked list, also in reverse order.

```
l1 = [2,4,3], l2 = [5,6,4]  →  [7,0,8]        (342 + 465 = 807)
l1 = [0],     l2 = [0]      →  [0]
l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]  →  [8,9,9,9,0,0,0,1]
```

**Constraints:** `1 <= nodes in each list <= 100` · `0 <= Node.val <= 9` · no leading zeros except the number 0 itself

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| digits in **reverse order** | ⚠️ **A gift, not an obstacle.** The head is the *ones* digit — exactly where column addition starts. You add left to right, which is the direction a linked list already walks |
| one digit per node | Values 0–9; every sum of two digits plus a carry is at most 19, so the carry is always 0 or 1 |
| lists may differ in length | `[9,9,9]` + `[1]` — the shorter one runs out mid-addition |
| up to 100 digits | The numbers can exceed 64-bit range, so converting to integers is fragile in most languages |
| return a **linked list** | You're *building* a list → dummy head |

The whole problem is elementary-school column addition:

```
   3 4 2          walk from the ones place →  2+5=7
 + 4 6 5                                      4+6=0 carry 1
 -------                                      3+4+1=8
   8 0 7
```

And because the digits are stored in reverse, **the natural traversal direction is already the ones-first direction**. If they were stored forward you'd have to reverse both lists first, or use recursion to reach the end. The "reverse order" in the statement is the problem making itself easier.

**Three details do all the work:**
1. `total = v1 + v2 + carry`
2. the digit to emit is `total % 10`
3. the new carry is `total // 10`

**The case people forget:** a final carry. `[5] + [5]` gives `[0, 1]` — a *third* node beyond either input's length.

🤔 **Before you open the next section:** what should your loop condition be, so that it handles unequal lengths **and** a leftover carry after both lists are exhausted?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Verdict |
|---|---|---|
| Convert to ints, add, rebuild | Read both lists into numbers, sum, split into digits | ⚠️ Works **in Python** (arbitrary-precision ints), but overflows in C/Java at 100 digits. A red flag answer |
| Recursion | Recurse down both lists carrying the carry | ✅ Works; O(n) stack |
| **Column addition, one pass** | Simulate digit-by-digit with a carry | ✅ |

**The decision: a single pass simulating column addition, building the result with a [dummy head](../data-structures/linked-list.md).**

**Why not convert to integers?** In Python it genuinely works — ints are arbitrary-precision. But say that out loud and an interviewer will ask about a language where they aren't: 100 digits is ~333 bits, far past 64. The digit-by-digit method is language-independent and is what the problem is testing. **Mention the shortcut, then write the real one.**

**The loop condition is the elegant part:**

```python
while l1 or l2 or carry:
```

Three termination concerns collapse into one line:
- **`l1 or l2`** — keep going while *either* list has digits, handling unequal lengths.
- **`or carry`** — keep going if there's a carry left even after both are exhausted, which appends that final `1`.

The alternative is a loop for the common prefix plus two cleanup loops plus a final carry check. **One condition replaces all of it.**

**Missing digits become zero.** `v1 = l1.val if l1 else 0` treats an exhausted list as a stream of zeros — which is arithmetically exact, since `342 + 5` is `342 + 005`. Same instinct as the sentinels in [Median of Two Sorted Arrays](4-median-of-two-sorted-arrays.md): **choose a value that makes the edge case behave like the normal case.**

**The dummy head** appears for the third time in this unit, again for *building* a list — you need somewhere to attach the first digit before the result exists.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
dummy = ListNode()
tail = dummy
carry = 0
```

The dummy gives `tail.next` a valid target before the result has any nodes; `tail` tracks where to append. `carry` starts at 0 — nothing carried into the ones column.
→ [class-basics](../syntax/class-basics.md) · [linked-list](../data-structures/linked-list.md)

```python
while l1 or l2 or carry:
```

**The three-part condition.** Continue while either list has digits remaining, **or** a carry is still pending.

That last clause is what produces the extra node in `[5] + [5] = [0,1]`: both lists are exhausted, but `carry == 1` keeps the loop alive for one final iteration.

A node object is truthy and `None` is falsy, so this reads directly.
→ [while-loop](../syntax/while-loop.md) · [truthy-falsy-values](../syntax/truthy-falsy-values.md) · [logical-operators](../syntax/logical-operators.md)

```python
    v1 = l1.val if l1 else 0
    v2 = l2.val if l2 else 0
```

**Exhausted list ⇒ digit 0.** Arithmetically exact, and it means unequal lengths need no separate loop — the shorter number is simply zero-padded.
→ [ternary-expression](../syntax/ternary-expression.md)

```python
    total = v1 + v2 + carry
    carry = total // 10
```

The column sum, at most `9 + 9 + 1 = 19`. So `total // 10` is always **0 or 1** — the carry into the next column.
→ [integer-division-modulo](../syntax/integer-division-modulo.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
    tail.next = ListNode(total % 10)
    tail = tail.next
```

`total % 10` is the digit that stays in this column. Append it and advance the tail.

`//` and `%` are the natural pair here — quotient carries, remainder stays. The same split appears in [Search a 2D Matrix](74-search-a-2d-matrix.md)'s index math, for the same structural reason.

```python
    l1 = l1.next if l1 else None
    l2 = l2.next if l2 else None
```

Advance each list **only if it still has nodes**. Once exhausted a list stays `None`, and the ternaries above keep feeding zeros.

Writing plain `l1 = l1.next` would raise `AttributeError` once `l1` is `None` — which happens on any unequal-length input.

```python
return dummy.next
```

`dummy.next` is the first digit (the ones place). Returning `dummy` would prepend a phantom zero.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:

        dummy = ListNode()
        tail = dummy
        carry = 0

        while l1 or l2 or carry:
            v1 = l1.val if l1 else 0
            v2 = l2.val if l2 else 0

            total = v1 + v2 + carry
            carry = total // 10
            tail.next = ListNode(total % 10)
            tail = tail.next

            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None

        return dummy.next
```

</details>

**Trace it** — `l1 = [2,4,3]` (342), `l2 = [5,6,4]` (465):

| Step | `v1` | `v2` | `carry` in | `total` | digit (`%10`) | `carry` out |
|---|---|---|---|---|---|---|
| 1 | 2 | 5 | 0 | 7 | **7** | 0 |
| 2 | 4 | 6 | 0 | 10 | **0** | 1 |
| 3 | 3 | 4 | 1 | 8 | **8** | 0 |

Result `[7,0,8]` = 807 = 342 + 465 ✅

**The unequal-length + final-carry case** — `l1 = [9,9]` (99), `l2 = [1]` (1):

| Step | `v1` | `v2` | `carry` in | `total` | digit | `carry` out | Loop continues? |
|---|---|---|---|---|---|---|---|
| 1 | 9 | 1 | 0 | 10 | **0** | 1 | yes (`l1` remains) |
| 2 | 9 | **0** ← exhausted | 1 | 10 | **0** | 1 | yes (**carry**) |
| 3 | **0** | **0** | 1 | 1 | **1** | 0 | no |

Result `[0,0,1]` = 100 ✅

Step 3 exists *only* because of the `or carry` clause — both lists were empty, and without it the answer would be a wrong `[0,0]`.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(max(m, n))</summary>

**O(max(m, n))**, where m and n are the two list lengths.

The loop runs once per digit of the result, which has `max(m, n)` digits — possibly **one more** if there's a final carry. Each iteration is O(1): two comparisons, an addition, a division, a modulo, and one node allocation.

**O(max(m, n))** total, which is optimal — you must read every digit of both inputs and write every digit of the output.

**Versus the convert-to-int approach:** also O(m + n) in Python, but it walks both lists, builds two big integers, adds them, then splits the result back into digits. Same order, more work, and it breaks entirely in fixed-width-integer languages.

**No early exit** — every digit affects the result.

**Note the carry can propagate all the way**, as in `[9,9,9,9] + [1]`. Each step is still O(1), so the total stays linear — the carry never causes a re-pass.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1) auxiliary</summary>

**O(max(m, n))** for the output list, **O(1) auxiliary**.

Make the distinction explicitly, since it's the one interviewers probe:

- **The result list** — `max(m, n)` or `max(m, n) + 1` new nodes. This is the **required output**; you can't return a sum without allocating it.
- **Auxiliary space** — `dummy`, `tail`, `carry`, `v1`, `v2`, `total`. Constant.

So: *"O(1) auxiliary space, plus the O(max(m,n)) output that the problem requires."*

**This is the first problem in Unit 06 that legitimately allocates.** Every previous one relinked existing nodes:

| Problem | Allocates? |
|---|---|
| [206](206-reverse-linked-list.md), [21](21-merge-two-sorted-lists.md), [143](143-reorder-list.md), [19](19-remove-nth-node-from-end-of-list.md) | No — relink in place |
| [138](138-copy-list-with-random-pointer.md) | Yes — a deep copy is required |
| **2** | **Yes** — the sum is new data |

Worth noticing *why*: relinking works when the answer is a rearrangement of the input. Here the digits of the sum are genuinely new values, so nodes must be created. **Ask "is the answer made of the input's parts, or of new values?"** — it tells you immediately whether O(1) space is even possible.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The digits are stored in reverse, which means the head is the ones place — so walking the lists forward is exactly the order column addition wants. I add corresponding digits plus a carry, emit `total % 10` as the digit, and keep `total // 10` as the next carry, building the result with a dummy head. The loop condition is `while l1 or l2 or carry`, which handles three things at once: unequal lengths, and a leftover carry that needs one extra node — `[5] + [5]` becomes `[0,1]`. An exhausted list contributes 0, which is arithmetically exact. O(max(m,n)) time, O(1) auxiliary space plus the output. I could convert to integers and add in Python, but that would overflow in a fixed-width language at 100 digits."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "What if the digits were in **forward** order?" | Reverse both lists first (problem [206](206-reverse-linked-list.md)), add, then reverse the result — or use a stack per list to read digits back to front. LeetCode 445. |
| "Why not convert to integers?" | Fine in Python, but 100 digits is ~333 bits — overflow in C/Java. The digit-by-digit method is language-independent. |
| "Why `or carry` in the loop?" | **The question.** Without it, `[5] + [5]` returns `[0]` instead of `[0,1]`. |
| "Add **three** numbers?" | Same loop; the carry can now reach 2, but `//10` and `%10` still work unchanged. |
| "**Subtract** instead?" | Borrowing instead of carrying, plus sign handling and stripping leading zeros — noticeably fiddlier. |
| "Reuse the input nodes to save space?" | Possible — overwrite `l1`'s nodes and extend if needed. Saves allocation but destroys an input, which is usually a bad API. |
| "Multiply two such numbers?" | Long multiplication, O(m·n). See [Multiply Strings](43-multiply-strings.md). |

**Traps:**

- **Forgetting the final carry.** `[5] + [5]` → `[0]` instead of `[0,1]`. *The* bug of this problem.
- **`l1 = l1.next` without the guard** — `AttributeError` as soon as one list is exhausted.
- **Handling unequal lengths with extra loops.** Correct but three times the code; the `if l1 else 0` trick makes it one loop.
- **Returning `dummy`** instead of `dummy.next` — prepends a phantom digit.
- **`carry = total % 10` and digit `total // 10`** — swapped. Check on `total = 10`: digit 0, carry 1.
- **Assuming equal lengths.** The constraints don't promise it.

**This same move shows up in:** [Merge Two Sorted Lists](21-merge-two-sorted-lists.md) (dummy head while building) · [Multiply Strings](43-multiply-strings.md) (digit-by-digit arithmetic with carries) · [Plus One](66-plus-one.md) (carry propagation in an array) · [Reverse Linked List](206-reverse-linked-list.md) (needed if the digits arrive forward-ordered).

</details>

---
