# 2807. Insert Greatest Common Divisors in Linked List

**Medium** · [LeetCode](https://leetcode.com/problems/insert-greatest-common-divisors-in-linked-list/) · [Solution file (no hints)](../../problems/2500-2999/2807.py)

[📖 17. Math & Geometry lesson](../learning/19-math-geometry.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 17. Math & Geometry problems](../rmap-practice/17-math-geometry.md)

---

Given the `head` of a linked list of positive integers, insert **between every two adjacent nodes** a new node whose value is the **greatest common divisor** of those two nodes' values. Return the head of the modified list.

```
head = [18, 6, 10, 3]   →  [18, 6, 6, 2, 10, 1, 3]
                              gcd(18,6)=6  gcd(6,10)=2  gcd(10,3)=1

head = [7]              →  [7]     (no adjacent pair)
```

**Constraints:** `1 <= nodes <= 5000` · `1 <= Node.val <= 1000`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "between every two adjacent nodes" | Walk the list pair by pair and **insert in the gap** |
| "greatest common divisor" | The **Euclidean algorithm** (`gcd(a, b) = gcd(b, a % b)`) |
| return `head` | The head never changes. A single-node list is already the answer |
| in a linked list | Insertion is O(1) once you hold the node **before** the gap |

Two skills are combined: [Euclid's GCD](../algorithms/euclidean-gcd.md), and **linked-list insertion without losing the rest of the list**.

**Insertion order is the danger.** To put a node `g` between `cur` and `cur.next`, make `g.next` point at the old `cur.next` **first**, then `cur.next = g`. Do it the other way and the rest of the list is lost.

After inserting, `cur` must jump **past the new node and past the original next node's predecessor**: move to `g.next` (the original next node), so the next pair is the next *original* pair. Otherwise you'd compute the GCD of the new node with its neighbour forever.

🤔 **Before you open the next section:** after inserting `g` between `cur` and `nxt`, which node should `cur` be on the next iteration?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Time | Space | Verdict |
|---|---|---|---|
| Build a new list from scratch | O(n log m) | O(n) | ⚠️ Works, but allocates a whole second list |
| **Insert in place while walking** | **O(n log m)** | **O(1) extra** (plus the new nodes) | ✅ |
| `math.gcd` | same | same | ✅ Fine if the interviewer allows it. Show Euclid if not |

**The decision: one pass, in-place insertion, with a hand-written Euclidean GCD.** `m` is the largest value; Euclid takes O(log m) steps per pair. The Python standard library has `math.gcd`, but writing the loop shows you know the algorithm.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
cur = head
while cur.next:
```

`cur` is the node **before** the gap to fill. While it has a next node, there's a gap. A single-node list skips the loop and is returned unchanged.
→ [while-loop](../syntax/while-loop.md) · [none-type](../syntax/none-type.md) · [linked-list](../data-structures/linked-list.md)

```python
    a, b = cur.val, cur.next.val
    while b:
        a, b = b, a % b
```

**Euclid's algorithm.** Replace `(a, b)` with `(b, a mod b)` until `b` is 0. At that point `a` holds the GCD. The tuple assignment swaps without a temporary.
→ [swap-tuple-assign](../syntax/swap-tuple-assign.md) · [integer-division-modulo](../syntax/integer-division-modulo.md) · [euclidean-gcd](../algorithms/euclidean-gcd.md)

```python
    cur.next = ListNode(a, cur.next)
```

**Splice in the new node.** The constructor sets `new.next = cur.next` (the old next node) *before* `cur.next` is overwritten, because the right-hand side is evaluated first. No part of the list is lost.
→ [class-basics](../syntax/class-basics.md) · [init-method](../syntax/init-method.md)

```python
    cur = cur.next.next

return head
```

`cur.next` is the **new** node, so `cur.next.next` is the original next node. Landing there makes the next gap the next original pair.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def insertGreatestCommonDivisors(self, head: Optional[ListNode]) -> Optional[ListNode]:
        cur = head

        while cur.next:
            a, b = cur.val, cur.next.val
            while b:
                a, b = b, a % b

            cur.next = ListNode(a, cur.next)
            cur = cur.next.next

        return head
```

</details>

**Trace it.** `[18, 6, 10, 3]`:

| `cur` | pair | gcd | list after |
|---|---|---|---|
| 18 | (18, 6) | 6 | `18 → 6 → 6 → 10 → 3` |
| 6 (original) | (6, 10) | 2 | `… 6 → 2 → 10 → 3` |
| 10 | (10, 3) | 1 | `… 10 → 1 → 3` |
| 3 | `cur.next` is `None` | | stop |

Result `[18, 6, 6, 2, 10, 1, 3]` ✅.

Euclid for `(18, 6)`: `(18, 6) → (6, 0)` → gcd 6. For `(10, 3)`: `(10, 3) → (3, 1) → (1, 0)` → gcd 1.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n log m)</summary>

`n − 1` insertions, each needing a GCD of two numbers up to `m`, which takes **O(log m)** steps: **O(n log m)**. With `m <= 1000` that's about 10 steps per pair.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1) extra</summary>

Only the new nodes are allocated (`n − 1` of them, which is the output). Beyond that, a few pointers: **O(1)**.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "I walk the list holding the node before each gap. For each adjacent pair I compute the GCD with Euclid's algorithm, then splice in a new node: the constructor points the new node at the old next, then I point `cur.next` at it, so nothing is lost. Then I jump two steps, past the new node, so the next gap is the next original pair. One pass, O(n log m) time, O(1) extra space apart from the inserted nodes."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why does Euclid terminate?" | `a % b < b`, so the second argument strictly shrinks to 0 |
| "Recursive version?" | `gcd(a, b) = a if b == 0 else gcd(b, a % b)`. Same complexity, with O(log m) stack |
| "Use the standard library?" | `math.gcd(a, b)`. Mention it and then write it out if asked |
| "Empty list?" | The problem guarantees at least one node. Add `if not head: return head` for safety |
| "Related?" | [Merge Two Sorted Lists](21-merge-two-sorted-lists.md) · [Swap Nodes in Pairs](24-swap-nodes-in-pairs.md) (pointer rewiring in pairs) · [Greatest Common Divisor of Strings](1071-greatest-common-divisor-of-strings.md) |

**Traps:**

- **Setting `cur.next = new` before linking `new.next`.** The rest of the list is lost. The constructor argument avoids it.
- **`cur = cur.next`** after inserting. You'd compute the GCD of the new node and its neighbour in an endless loop.
- **Not handling the last node.** `cur.next.val` would crash. The `while cur.next` guard prevents it.
- **Modifying `a`, `b` aliases of node values.** They're integers: no harm, but copy them to local names anyway.

**This same move shows up in:** [Swap Nodes in Pairs](24-swap-nodes-in-pairs.md) · [Reverse Linked List](206-reverse-linked-list.md) · [Reorder List](143-reorder-list.md).

</details>

---
