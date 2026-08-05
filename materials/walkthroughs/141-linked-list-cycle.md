# 141. Linked List Cycle

**Easy** · [LeetCode](https://leetcode.com/problems/linked-list-cycle/) · [Solution file (no hints)](../../problems/0001-0499/141.py)

[📖 06. Linked List lesson](../learning/06-linked-list.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 06. Linked List problems](../rmap-practice/06-linked-list.md)

---

Given the head of a linked list, determine if it has a **cycle** — that is, whether some node can be reached again by continuously following `next`.

```
head = [3,2,0,-4], tail connects to index 1   →  true

    3 → 2 → 0 → -4
        ↑         │
        └─────────┘

head = [1,2], tail connects to index 0        →  true
head = [1],   no cycle                        →  false
```

**Constraints:** `0 <= nodes <= 10⁴` · `-10⁵ <= Node.val <= 10⁵` · **follow-up: solve it using O(1) memory**

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**cycle**" | Following `next` never reaches `None` — you loop forever |
| "some node reached **again**" | Revisiting a node is the definition. That suggests remembering what you've seen… |
| "**O(1) memory**" follow-up | ⚠️ …which rules out the obvious hash-set solution. This is the actual challenge |
| return `true`/`false` | Existence only — you don't have to locate where the cycle starts |
| 0 nodes allowed | Empty list → `false`, without crashing |

**The obvious solution first.** Walk the list, storing each node in a [hash set](../data-structures/hashset.md). If you meet a node already in the set, there's a cycle; if you reach `None`, there isn't. O(n) time, **O(n) space** — and the follow-up specifically asks you to beat that.

**So how do you detect a loop with no memory?** Think about a running track. Two runners start together, one twice as fast. On a straight track the fast one finishes and leaves. On a **circular** track the fast one laps the slow one and they meet again — inevitably.

That's Floyd's cycle detection, the "tortoise and hare":

- **No cycle** → `fast` reaches the end and you return `false`.
- **Cycle** → `fast` enters the loop, `slow` follows, and `fast` gains one position per step until it catches up.

**Why they must meet, not jump past each other.** Once both are inside the cycle, the gap between them shrinks by exactly **1** every step (fast moves 2, slow moves 1). A quantity decreasing by exactly 1 must hit 0 — it can't skip over. That's the proof, and it's the thing to be able to state.

🤔 **Before you open the next section:** if `fast` moved **three** steps per iteration instead of two, would they still be guaranteed to meet?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Hash set of visited nodes | Remember every node seen | O(n) | **O(n)** | ⚠️ Correct, easy — but the follow-up forbids it |
| Mark nodes as visited | Mutate a flag on each node | O(n) | O(1) | ❌ Destroys the input; often not allowed |
| Count steps against a limit | If you exceed n steps, there's a cycle | O(n) | O(1) | ❌ Needs a known length; fragile |
| **Floyd's two pointers** | Fast laps slow inside a cycle | **O(n)** | **O(1)** | ✅ |

**The decision: [Floyd's cycle detection](../algorithms/floyd-cycle-detection.md) — `slow` moves one node per step, `fast` moves two.**

- **They meet** (`slow == fast`) → cycle.
- **`fast` hits `None`** → no cycle, because only a terminating list has an end.

**The correctness argument, worth having ready.** Suppose a cycle of length `C` exists. Once both pointers are inside it, consider the gap from `fast` to `slow` measured *around the loop*. Each step `fast` advances 2 and `slow` advances 1, so that gap shrinks by exactly 1 per step. Since it decreases by 1 and never skips a value, it must reach 0 — they land on the same node. **They cannot pass each other**, which is precisely why a 2:1 ratio is chosen.

*(With a 3:1 ratio the gap shrinks by 2 each step and could alternate parity, potentially skipping 0 — it still works out for other reasons, but 2:1 is the ratio with the clean proof. Good follow-up material.)*

**Why the loop condition needs both checks.** `while fast is not None and fast.next is not None` — you're about to evaluate `fast.next.next`, so *both* `fast` and `fast.next` must exist. Checking only `fast` raises `AttributeError` on a list of even length. Python's `and` short-circuits, so the order matters.

**Why this appears in Unit 06 for the third time.** Fast/slow pointers found the midpoint in [Reorder List](143-reorder-list.md), a fixed gap located "nth from the end" in [Remove Nth Node](19-remove-nth-node-from-end-of-list.md), and here differing *speeds* detect a loop. **Two pointers moving at different rates is the core linked-list technique** — the specific question just changes what you read from their relationship.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
slow = head
fast = head
```

Both start at the head. Starting them together is fine — the first iteration immediately separates them, and `slow == fast` is only tested *after* both have moved.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
while fast is not None and fast.next is not None:
```

**Both checks are required**, because the body dereferences `fast.next.next`:

- `fast is not None` — `fast` itself must exist.
- `fast.next is not None` — the node after it must exist too.

Odd-length lists end with `fast` on the last node (so `fast.next` is `None`); even-length lists end with `fast` becoming `None`. One condition covers each case.

Reaching the end at all *proves there's no cycle* — a cyclic list has no end, so this loop would never terminate on one.
→ [while-loop](../syntax/while-loop.md) · [identity-operators](../syntax/identity-operators.md) · [logical-operators](../syntax/logical-operators.md)

```python
    slow = slow.next
    fast = fast.next.next
```

**The 2:1 speed ratio.** `slow` advances one node, `fast` two. Inside a cycle this closes the gap by exactly one node per iteration.
→ [linked-list](../data-structures/linked-list.md)

```python
    if slow == fast:
        return True
```

They've landed on the **same node** — only possible if `fast` lapped `slow`, which only happens inside a cycle.

Comparing *after* both have moved is what prevents a false positive on the first iteration, when both still sit at `head`.

*(`==` on node objects falls back to identity comparison here, since `ListNode` defines no `__eq__`. `is` would be more explicit about the intent and is arguably better style.)*
→ [comparison-operators](../syntax/comparison-operators.md) · [identity-operators](../syntax/identity-operators.md) · [if-return](../syntax/if-return.md)

```python
return False
```

The loop exited, meaning `fast` reached the end of the list. A list with an end has no cycle. This also covers empty input — `head` is `None`, the loop never runs.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:

        slow = head
        fast = head

        while fast is not None and fast.next is not None:
            slow = slow.next
            fast = fast.next.next

            if slow == fast:
                return True

        return False
```

</details>

**Trace it** — `3 → 2 → 0 → -4`, with `-4` pointing back to `2` (a 3-node cycle):

Label the nodes A(3) → B(2) → C(0) → D(−4) → back to B.

| Step | `slow` | `fast` | Met? |
|---|---|---|---|
| start | A | A | (not yet tested) |
| 1 | B | C | no |
| 2 | C | **B** (D → B) | no |
| 3 | D | **D** (C → D) | ✅ **`return True`** |

Watch the gap close: at step 1 `fast` is 1 ahead, at step 2 it has wrapped and is 2 behind... and at step 3 they coincide. The gap shrank by exactly one each step, so a collision was unavoidable.

**And a list with no cycle** — `1 → 2 → None`:

| Step | `slow` | `fast` | Condition |
|---|---|---|---|
| start | 1 | 1 | `fast` ✓, `fast.next` ✓ |
| 1 | 2 | **None** | `fast is None` → loop ends |

`return False` ✅

**The hash-set version**, for comparison:

```python
seen = set()
while head:
    if head in seen:
        return True
    seen.add(head)
    head = head.next
return False
```
→ [set-basics](../syntax/set-basics.md)

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

**No cycle:** `fast` traverses the list at two nodes per step, finishing in n/2 iterations → O(n).

**Cycle present:** two phases.
1. `slow` walks the non-cyclic prefix (length `μ`) to enter the loop — at most n steps.
2. Once both are inside the cycle (length `C`), the gap shrinks by 1 per step, so they meet within at most `C` more steps.

Total ≤ `μ + C` ≤ n → **O(n)**.

The key bound is that **the meeting happens within one lap**, because the gap is at most `C` and decreases by exactly one each iteration. No re-lapping, no unbounded spinning.

**Same complexity as the hash set** — the win is entirely in space. That's the shape of this problem: both solutions are O(n) time, and the follow-up exists to push you from O(n) to O(1) memory.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — two pointers, nothing else. This is the point of the problem.

| Approach | Time | Space |
|---|---|---|
| Hash set | O(n) | **O(n)** |
| **Floyd's** | O(n) | **O(1)** |

**How the memory was eliminated.** The hash set remembers *every node visited* to detect a repeat. Floyd's remembers **nothing** — it detects the repeat through a *relationship between two pointers* instead. The cycle reveals itself through motion rather than history.

That's a genuinely deep idea, and it's the same family as the elimination arguments from earlier units:

| Speedup / saving source | Example |
|---|---|
| Remember what you've seen | [Two Sum](1-two-sum.md), the hash-set version here — **O(n)** |
| Exploit a structural relationship | Two pointers, binary search, **Floyd's** — **O(1)** |

**Where this generalizes:** Floyd's works on any "sequence with a next function" — not just linked lists. [Find the Duplicate Number](287-find-the-duplicate-number.md) applies it to an *array*, treating values as pointers to indices. Same algorithm, unrecognizably different problem.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The easy solution is a hash set of visited nodes — O(n) time and O(n) space. To get O(1) space I use Floyd's cycle detection: a slow pointer moving one node per step and a fast one moving two. If the list ends, `fast` hits null and there's no cycle. If there is a cycle, both pointers eventually enter it, and then the gap between them shrinks by exactly one each step — so it must reach zero and they land on the same node. They can't jump past each other, which is exactly why the 2:1 ratio is chosen. O(n) time, O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Prove they must meet." | **The question.** Inside the cycle the gap decreases by exactly 1 per step. A value decreasing by 1 can't skip 0. |
| "Find where the cycle **starts**." | After they meet, reset one pointer to `head` and advance both one step at a time — they meet at the cycle's entrance. LeetCode 142. (The proof is a short bit of modular arithmetic.) |
| "Find the cycle's **length**." | From the meeting point, walk `fast` alone until it returns there, counting steps. |
| "What if `fast` moved 3 steps?" | The gap then shrinks by 2 per step and could skip 0 on a cycle of the wrong parity — the clean guarantee is lost. 2:1 is the ratio with the simple proof. |
| "Use the hash set instead." | Simpler and equally fast, but O(n) space — which the follow-up rules out. |
| "Detect a duplicate in an array with this?" | Yes — treat `nums[i]` as a pointer to index `nums[i]`; a duplicate creates a cycle. See [Find the Duplicate Number](287-find-the-duplicate-number.md). |
| "Could you mark visited nodes instead?" | O(1) space but mutates the input, and it needs a spare field. Usually disallowed. |

**Traps:**

- **Only checking `while fast is not None`.** `fast.next.next` then raises `AttributeError` on even-length lists. You need `fast.next` too.
- **Comparing before moving.** Both start at `head`, so an initial `if slow == fast` returns `True` for every list.
- **Advancing `fast` by one** — it never catches up, and the loop just terminates.
- **Comparing values (`slow.val == fast.val`)** instead of the nodes. Duplicate values give false positives.
- **Forgetting empty input.** Handled here, since `head = None` fails the loop condition immediately.
- **Assuming the meeting point is the cycle's start.** It isn't — locating the entrance takes the extra phase described above.

**This same move shows up in:** [Reorder List](143-reorder-list.md) (fast/slow to find the midpoint) · [Remove Nth Node From End](19-remove-nth-node-from-end-of-list.md) (two pointers with a fixed gap) · [Find the Duplicate Number](287-find-the-duplicate-number.md) (Floyd's applied to an array) · [floyd-cycle-detection](../algorithms/floyd-cycle-detection.md) (the algorithm's reference page).

</details>

---
