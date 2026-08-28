# 160. Intersection of Two Linked Lists

**Easy** · [LeetCode](https://leetcode.com/problems/intersection-of-two-linked-lists/) · [Solution file (no hints)](../../problems/0001-0499/160.py)

[📖 06. Linked List lesson](../learning/06-linked-list.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 06. Linked List problems](../rmap-practice/06-linked-list.md)

---

Given the heads of two singly linked lists, return the node where they **intersect**. If they don't intersect, return `None`. Intersection is by **reference**, not value — the lists share actual nodes from that point on.

```
listA = [4,1,8,4,5], listB = [5,6,1,8,4,5], intersect at node 8   →  8
listA = [2,6,4],     listB = [1,5]                                →  None
```

**Constraints:** `1 <= m, n <= 3·10⁴` · `1 <= Node.val <= 10⁵` · the lists retain their original structure

**Follow-up:** can you solve it in **O(m + n)** time and **O(1)** memory?

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "intersect" by **reference** | ⚠️ Compare **node identity** (`is`), not values. Two nodes with the same `val` are not an intersection |
| "return the **node**" | Not a value or index |
| singly linked | Forward-only; no way to walk back from the tails |
| follow-up: **O(1) memory** | Rules out the hash-set solution |
| lists may have **different lengths** | ⚠️ That's the obstacle. Walking both from the head misaligns them |

**The structural fact.** Once two singly linked lists intersect, they **share the entire tail** — a node has only one `next` pointer, so from the intersection onward there's exactly one path:

```
A: 4 → 1 ↘
           8 → 4 → 5 → None
B: 5 → 6 → 1 ↗
```

So the lists look like a **Y**, never an **X**. That means the intersection is at the same *distance from the end* in both lists — but at different distances from the head, because the leading segments differ in length.

**The naive fix:** compute both lengths, advance the longer list's pointer by the difference to align them, then walk together comparing identity. That's correct, O(m+n), O(1) — and needs two passes plus explicit arithmetic.

**The elegant fix — the two-pointer switch:**

> Walk `pA` through A then continue into B. Walk `pB` through B then continue into A. They will meet at the intersection.

Why it works: each pointer traverses **exactly `m + n` nodes** before reaching the end. Let the pre-intersection lengths be `a` and `b`, and the shared tail `c`:

- `pA` travels `a + c` (all of A) then `b` (B's prefix) = `a + b + c` to reach the intersection
- `pB` travels `b + c` (all of B) then `a` (A's prefix) = `a + b + c` to reach the intersection

**Identical distances.** The switch cancels the length difference without ever computing it.

🤔 **Before you open the next section:** if the two lists *don't* intersect, what happens when both pointers have travelled `m + n` nodes?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Brute force | For each node in A, scan all of B | O(m·n) | O(1) | ❌ 9·10⁸ |
| Hash set of A's nodes | Store A, then scan B checking membership | O(m+n) | **O(m)** | ⚠️ Correct, fails the follow-up |
| Align by length difference | Measure both, skip ahead, walk together | O(m+n) | O(1) | ✅ Correct, more bookkeeping |
| **Two-pointer switch** | Each pointer runs A→B and B→A | **O(m+n)** | **O(1)** | ✅✅ |

**The decision: the two-pointer switch.**

Both pointers walk `a + b + c` nodes to reach the intersection, so they arrive **simultaneously** — no length computation, no alignment step, no special cases.

**Why the no-intersection case works for free** — and this is the part worth understanding, because it's where naive implementations loop forever:

If the lists don't intersect, `c = 0`. `pA` walks `a + b` nodes and reaches `None`; `pB` walks `b + a` nodes and reaches `None` at the same moment. Since `None is None`, the loop condition `pA is not pB` becomes false and both pointers are `None` — which is exactly the answer to return.

**The critical detail that makes that work:** each pointer must switch to the *other* head only **once**, and must be allowed to become `None`. The implementation achieves this by checking the pointer itself:

```python
if pointer_a is not None:
    pointer_a = pointer_a.next
else:
    pointer_a = headB           # switch, exactly once
```

Because the switch happens when the pointer *is* `None`, and after switching it walks a finite list, each pointer can only switch once before reaching `None` again — at which point the loop has already ended (both are `None` simultaneously).

Compare with the common shorthand `pA = pA.next if pA else headB`, which is the same logic. What you must **not** write is `pA = pA.next.next if ...` or a version that skips the `None` state — then the two pointers never land on `None` together and the loop spins forever on non-intersecting lists.

**Why `is` and not `==`.** Intersection is defined by identity. `==` on `ListNode` objects falls back to identity in Python unless `__eq__` is overridden — so it happens to work — but `is` states the intent precisely and is immune to a custom `__eq__`. See [identity-operators](../syntax/identity-operators.md).

**Why not the hash set?** It's the natural first answer, it's O(m+n) time, and it's perfectly correct. But it's O(m) space and the follow-up explicitly asks you to beat that. Name it, then show the switch.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
pointer_a: Optional[ListNode] = headA
pointer_b: Optional[ListNode] = headB
```

One pointer per list, each starting at its own head.
→ [variables-assignment](../syntax/variables-assignment.md) · [type-hints](../syntax/type-hints.md)

```python
while pointer_a is not pointer_b:
```

**Loop until the pointers are the same object.**

`is not` compares **identity**, which is the problem's definition of intersection. This condition terminates in both cases:

- **Intersecting:** both reach the shared node after `a + b + c` steps
- **Not intersecting:** both become `None` after `a + b` steps, and `None is None`

→ [while-loop](../syntax/while-loop.md) · [identity-operators](../syntax/identity-operators.md)

```python
    if pointer_a is not None:
        pointer_a = pointer_a.next
    else:
        pointer_a = headB
```

**Advance, or switch lists.**

While `pointer_a` still has list left, step forward. When it falls off the end (becomes `None`), redirect it to **B's** head.

The switch happens exactly once per pointer, because after switching it traverses a finite list and the loop ends when both are `None` together.
→ [none-type](../syntax/none-type.md) · [elif-else](../syntax/elif-else.md)

```python
    if pointer_b is not None:
        pointer_b = pointer_b.next
    else:
        pointer_b = headA
```

The mirror image — `pointer_b` switches to **A's** head.

Both pointers advance **once per iteration**, keeping them in lockstep. That synchronization is what makes the equal-distance argument hold.

```python
return pointer_a
```

Either the intersection node, or `None` if there isn't one. The loop's exit condition guarantees `pointer_a is pointer_b`, so returning either is correct.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:

        pointer_a: Optional[ListNode] = headA
        pointer_b: Optional[ListNode] = headB

        while pointer_a is not pointer_b:
            if pointer_a is not None:
                pointer_a = pointer_a.next
            else:
                pointer_a = headB

            if pointer_b is not None:
                pointer_b = pointer_b.next
            else:
                pointer_b = headA

        return pointer_a
```

</details>

**Trace the intersecting case** — `A = [4,1,8,4,5]`, `B = [5,6,1,8,4,5]`, intersecting at the node `8`.

Here `a = 2` (nodes 4,1), `b = 3` (nodes 5,6,1), `c = 3` (nodes 8,4,5).

| Step | `pointer_a` | `pointer_b` | Same? |
|---|---|---|---|
| 0 | 4 (A) | 5 (B) | no |
| 1 | 1 (A) | 6 (B) | no |
| 2 | **8** (shared) | 1 (B) | no |
| 3 | 4 (shared) | **8** (shared) | no |
| 4 | 5 (shared) | 4 (shared) | no |
| 5 | `None` | 5 (shared) | no |
| 6 | **5 (B head)** ← switch | `None` | no |
| 7 | 6 (B) | **4 (A head)** ← switch | no |
| 8 | 1 (B) | 1 (A) | no |
| 9 | **8** (shared) | **8** (shared) | ✅ **match** |

Return node **8** ✅

Note steps 5 and 6: each pointer passes **through `None`** before switching. That extra step is why they meet at step 9 rather than at `a + b + c = 8` — this implementation treats `None` as a position. What matters is that both pointers pass through the same number of positions, so they arrive **together**.

**Trace the non-intersecting case** — `A = [2,6,4]`, `B = [1,5]`:

| Step | `pointer_a` | `pointer_b` | Same? |
|---|---|---|---|
| 0 | 2 (A) | 1 (B) | no |
| 1 | 6 (A) | 5 (B) | no |
| 2 | 4 (A) | `None` | no |
| 3 | `None` | **2 (A head)** ← switch | no |
| 4 | **1 (B head)** ← switch | 6 (A) | no |
| 5 | 5 (B) | 4 (A) | no |
| 6 | `None` | `None` | ✅ **both `None`** |

Return **`None`** ✅ — the loop terminated because `None is None`, with no special-case code.

Watch the switches happen on **different steps** (3 and 4) because the lists differ in length — yet both pointers still land on `None` simultaneously at step 6, having each covered `3 + 2 = 5` nodes plus two `None` positions.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(m + n)</summary>

**O(m + n).**

Each pointer traverses at most `m + n` nodes: its own list, then the other one. Both advance once per iteration, so the loop runs at most `m + n + 1` times.

At `m = n = 3·10⁴` that's ~6·10⁴ steps — trivial.

**Why it terminates in both cases:**

| Case | Steps to meet |
|---|---|
| Intersecting | `a + b + c` — both arrive simultaneously |
| Not intersecting | `a + b` — both hit `None` simultaneously |

**Compare:** brute force is O(m·n) = 9·10⁸ — the hash set and the two-pointer switch are both O(m+n), so the only differentiator is space.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — two pointers, no allocation. This is what the follow-up asks for.

**The comparison that matters:**

| | Time | Space | Meets the follow-up? |
|---|---|---|---|
| Brute force | O(m·n) | O(1) | ❌ time |
| Hash set | O(m+n) | **O(m)** | ❌ space |
| Align by length | O(m+n) | O(1) | ✅ |
| **Two-pointer switch** | **O(m+n)** | **O(1)** | ✅ — and no arithmetic |

Both O(1) solutions are valid; the switch is preferred because it never computes lengths, has no subtraction, and handles the non-intersecting case without a branch. Less code, fewer places to be wrong.

**The idea worth extracting:**

> **When two sequences have different lengths but a common suffix, making each traverse both sequences equalizes their path lengths.** The difference cancels itself without ever being measured.

It's the same flavour of trick as the modular indexing in [Next Greater Element II](503-next-greater-element-ii.md) — restructure the traversal so an awkward asymmetry disappears, rather than special-casing it.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Since each node has one `next` pointer, two intersecting lists share their entire tail — the shape is a Y, not an X. So the intersection is equidistant from both ends, but not from both heads, because the prefixes differ in length. The obvious O(1)-space fix is to measure both lengths and skip the longer list ahead by the difference. But there's a neater way: walk one pointer through A then continue into B, and the other through B then into A. Each travels exactly `m + n` nodes, so they arrive at the intersection at the same moment — the length difference cancels without being computed. If the lists don't intersect, both become `None` after `m + n` steps and the identity check `None is None` ends the loop, returning `None` correctly. I compare with `is` rather than `==` because intersection is defined by reference. O(m+n) time, O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why does the switch work?" | **The key question.** Each pointer covers `a + b + c` to reach the intersection — the prefixes are traversed by both, so the difference cancels. |
| "What if they don't intersect?" | Both hit `None` after `a + b` steps simultaneously; `None is None` ends the loop and `None` is returned. |
| "Solve it with O(m) space." | Put all of A's nodes in a set, then scan B for the first member. Simpler, but fails the follow-up. |
| "Solve it by aligning lengths." | Measure both, advance the longer pointer by the difference, then walk in lockstep comparing identity. |
| "Why `is` and not `==`?" | Intersection is by reference. `==` happens to work without a custom `__eq__`, but `is` states the intent. |
| "What if a list had a **cycle**?" | This breaks — the pointers might never become `None`. You'd detect cycles first with [Floyd's algorithm](../algorithms/floyd-cycle-detection.md). |
| "Could you modify the lists?" | You could mark visited nodes, or join A's tail to B's head and run cycle detection — but the problem requires preserving structure. |

**Traps:**

- **Comparing values instead of identity.** `[4,1,8]` and `[5,6,1]` share the *value* 1 without intersecting. Use `is`.
- **Skipping the `None` state on a switch.** If a pointer jumps straight from the last node to the other head without passing through `None`, the two never align on non-intersecting lists and the loop runs forever.
- **Switching more than once.** Guard on the pointer being `None`, not on a counter.
- **Advancing only one pointer per iteration.** They must move in lockstep or the equal-distance argument collapses.
- **Special-casing the no-intersection result.** Unnecessary — it falls out of the identity check.
- **Assuming equal lengths.** The differing prefixes are the entire difficulty.

**This same move shows up in:** [Linked List Cycle](141-linked-list-cycle.md) (two pointers whose meeting condition encodes structure) · [Middle of the Linked List](876-middle-of-the-linked-list.md) (pointers at different effective speeds) · [Next Greater Element II](503-next-greater-element-ii.md) (restructuring a traversal to make an asymmetry vanish) · [Merge Two Sorted Lists](21-merge-two-sorted-lists.md) (walking two lists in coordination).

</details>

---
