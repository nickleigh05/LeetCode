# 61. Rotate List

**Medium** · [LeetCode](https://leetcode.com/problems/rotate-list/) · [Solution file (no hints)](../../problems/0001-0499/61.py)

[📖 06. Linked List lesson](../learning/06-linked-list.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 06. Linked List problems](../rmap-practice/06-linked-list.md)

---

Given the head of a linked list, rotate it to the **right** by `k` places.

```
head = [1,2,3,4,5], k = 2  →  [4,5,1,2,3]
head = [0,1,2],     k = 4  →  [2,0,1]
```

**Constraints:** `0 <= number of nodes <= 500` · `-100 <= Node.val <= 100` · `0 <= k <= 2·10⁹`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "rotate to the **right** by `k`" | The last `k` nodes move to the front |
| `k` up to **2·10⁹** | ⚠️ Vastly larger than the list. Rotating `n` times is identity, so you need **`k % n`** — naively looping `k` times is 2 billion iterations |
| `0 <= nodes` | Empty list must work, and `n = 0` would make `k % n` a **division by zero** |
| singly linked | Forward-only, no length available |
| `k` can be **0** | Then it's a no-op |

**The reframe.** Rotating right by `k` means the list is cut at a specific point and the two pieces swap:

```
[1,2,3,4,5], k = 2

cut here:  1 → 2 → 3 | 4 → 5
                       └──┬──┘
                    last k nodes

result:    4 → 5 → 1 → 2 → 3
```

The new head is the node at position `n - k` (0-indexed), and the new tail is the node just before it, at position `n - k - 1`.

**Two things make this tractable:**

1. **`k % n` first.** Rotating by `n` returns the original list, so only `k mod n` matters. With `k` up to 2·10⁹ this isn't an optimization — it's the difference between instant and impossible.
2. **Close the loop, then reopen it.** Rather than tracking two pieces, connect the tail to the head to form a **circle**, then walk to the new tail and break there. One clean cut instead of two splices.

```
step 1:  1 → 2 → 3 → 4 → 5 ─┐
         └──────────────────┘   (circular)

step 2:  walk to position n-k-1 = 2 (node 3), break after it

result:  4 → 5 → 1 → 2 → 3
```

🤔 **Before you open the next section:** if you make the list circular, how many steps from the original head do you need to walk to find the new tail?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Rotate one place, `k` times | Move the last node to the front, repeatedly | O(n·k) | O(1) | ❌ 2·10⁹ × 500 — hopeless |
| Copy to an array, slice | `arr[-k:] + arr[:-k]`, rebuild | O(n) | **O(n)** | ⚠️ Correct, wasteful |
| Two pointers with a `k` gap | Fast pointer `k` ahead, advance together | O(n) | O(1) | ✅ Correct; still needs `k % n` first |
| **Close the loop, walk, break** | Make it circular, cut at `n - k - 1` | **O(n)** | **O(1)** | ✅ |

**The decision: measure the length while walking to the tail, close the loop, then break at the new tail.**

The algorithm in four steps:

1. **Walk to the tail, counting nodes** — this gives both `n` and a handle on the last node, in one pass.
2. **`k %= n`.** If the result is 0, the list is unchanged — return early.
3. **Close the loop:** `tail.next = head`.
4. **Walk `n - k - 1` steps** from the head to reach the new tail, set `new_head = new_tail.next`, then `new_tail.next = None`.

**Why `k % n` is essential, not cosmetic.** With `k = 2·10⁹` and `n = 3`, `k % n = 2` — you rotate by 2, not 2 billion. Skipping the modulo means either a 2-billion-iteration loop or walking off the end of the list.

**Why the empty-list guard must come first.** `k % n` with `n = 0` raises `ZeroDivisionError`. The guard `if not head or not head.next or k == 0: return head` handles empty lists, single-node lists (rotation is always identity), and `k = 0` — all before any arithmetic.

**Why `n - k - 1` steps.** The new head is at index `n - k`, so the new tail is at index `n - k - 1`. Starting from the head (index 0), reaching index `n - k - 1` takes exactly `n - k - 1` steps. Getting this off by one is the most common bug — verify it against a tiny example every time.

**Why closing the loop helps.** It removes the need to handle "the second piece is empty" as a special case: after `k %= n` we know `1 <= k < n`, so both pieces are non-empty — but more importantly, walking a circle means you can find the cut point with a single forward walk and one assignment, rather than splicing two separate lists together.

**The two-pointer alternative** (fast pointer `k` ahead, then advance both until fast hits the tail) is equally valid and equally O(n)/O(1) — it just still requires computing `n` first to reduce `k`, so it doesn't actually save the initial pass.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
if not head or not head.next or k == 0:
    return head
```

**Three degenerate cases, one guard.**

- `not head` — empty list; also prevents the `ZeroDivisionError` from `k % 0` below
- `not head.next` — a single node rotates to itself for any `k`
- `k == 0` — no rotation requested

→ [truthy-falsy-values](../syntax/truthy-falsy-values.md) · [logical-operators](../syntax/logical-operators.md) · [if-return](../syntax/if-return.md)

```python
length = 1
tail = head
while tail.next:
    tail = tail.next
    length += 1
```

**One pass that yields both the length and the tail.**

Starting `length = 1` and `tail = head` counts the head itself, then each step adds one. When the loop ends, `tail` is the last node and `length` is `n`.

Doing both in one traversal rather than two is a small but real efficiency — and you need the tail anyway to close the loop.
→ [while-loop](../syntax/while-loop.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
k = k % length
if k == 0:
    return head
```

**Reduce `k`, then check again.**

`k % length` collapses 2·10⁹ into a value below `n`. And if the reduced `k` is 0 — as with `k = 10, n = 5` — the rotation is a full cycle and the list is unchanged, so return before doing pointless surgery.

This second `k == 0` check is distinct from the first: the first catches a literal 0, this one catches an exact multiple of `n`.
→ [integer-division-modulo](../syntax/integer-division-modulo.md)

```python
tail.next = head
```

**Close the loop.** The list is now circular, so walking forward from any node eventually returns to it.

```python
new_tail = head
for _ in range(length - k - 1):
    new_tail = new_tail.next
```

**Walk to the new tail** at index `length - k - 1`.

Sanity check with `[1,2,3,4,5]`, `k = 2`: `5 - 2 - 1 = 2` steps from node 1 → node **3**, and node 3 is indeed the node just before the new head (node 4) ✅
→ [range-function](../syntax/range-function.md) · [for-loop](../syntax/for-loop.md)

```python
new_head = new_tail.next
new_tail.next = None

return new_head
```

**Break the circle.** The node after the new tail becomes the head, and severing `new_tail.next` reopens the list.

Order matters: read `new_tail.next` **before** setting it to `None`, or you lose the new head.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def rotateRight(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:

        if not head or not head.next or k == 0:
            return head

        length = 1
        tail = head
        while tail.next:
            tail = tail.next
            length += 1

        k = k % length
        if k == 0:
            return head

        tail.next = head

        new_tail = head
        for _ in range(length - k - 1):
            new_tail = new_tail.next

        new_head = new_tail.next
        new_tail.next = None

        return new_head
```

</details>

**Trace it** — `head = [1,2,3,4,5]`, `k = 2`:

| Step | Action | State |
|---|---|---|
| 1 | Walk to the tail | `length = 5`, `tail` = node 5 |
| 2 | `k = 2 % 5 = 2` | non-zero, continue |
| 3 | `tail.next = head` | circular: `1→2→3→4→5→1→…` |
| 4 | Walk `5 - 2 - 1 = 2` steps | `new_tail` = node **3** |
| 5 | `new_head = new_tail.next` | `new_head` = node **4** |
| 6 | `new_tail.next = None` | `3 → None`, breaking the circle |

Result: `4 → 5 → 1 → 2 → 3`

Return **`[4,5,1,2,3]`** ✅

**The large-`k` case** — `[0,1,2]`, `k = 4`:

| Step | Action | State |
|---|---|---|
| 1 | Walk | `length = 3`, `tail` = node 2 |
| 2 | `k = 4 % 3 = 1` | rotate by **1**, not 4 |
| 3 | Close the loop | `0→1→2→0→…` |
| 4 | Walk `3 - 1 - 1 = 1` step | `new_tail` = node **1** |
| 5–6 | `new_head` = node 2; `1 → None` | |

Return **`[2,0,1]`** ✅

**The full-cycle case** — `[1,2,3]`, `k = 6`: `6 % 3 = 0`, so the second guard returns `head` immediately — no pointer changes at all.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

- Pass 1: walk to the tail while counting — `n - 1` steps
- Pass 2: walk to the new tail — `n - k - 1` steps, at most `n`

Total under `2n` — **O(n)**, and independent of `k` thanks to the modulo.

**That independence is the headline.** Without `k % n`:

| | Operations at `k = 2·10⁹`, `n = 500` |
|---|---|
| Rotate one place, `k` times | **10¹²** ❌ |
| **With `k % n`** | **~1000** ✅ |

The modulo isn't a micro-optimization; it's what makes the problem solvable at all under these constraints. Any problem where a rotation/shift count can exceed the structure's size should trigger the same reflex — see [Next Greater Element II](503-next-greater-element-ii.md), where `% n` serves a similar role.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — four pointers and two integers, no allocation. The existing nodes are relinked, not copied.

The array approach (`arr[-k:] + arr[:-k]`, then rebuild) is O(n) space and does more work for the same result.

**Why closing the loop is a genuine simplification, not just a trick:** the alternative is to find the new tail, save `new_tail.next` as the new head, sever it, then walk to the *original* tail again to attach it to the old head — a third traversal plus more bookkeeping. Making the list circular means the "attach old tail to old head" step happens **first**, in O(1), and then a single break finishes the job.

That's a reusable idea:

> **When an operation splits a structure and rejoins it differently, connecting the ends first can turn two splices into one cut.**

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Rotating right by `k` moves the last `k` nodes to the front, so the new head is at index `n - k`. First I walk to the tail while counting, which gives me both the length and the tail in one pass. Then `k %= n`, which is essential because `k` can be 2 billion while the list has at most 500 nodes — rotating by `n` is the identity, so only the remainder matters. If the reduced `k` is 0 the list is unchanged and I return early. Otherwise I close the list into a circle by pointing the tail at the head, walk `n - k - 1` steps to reach the new tail, take its successor as the new head, and sever the link to break the circle. O(n) time, O(1) space. I guard the empty and single-node cases up front, which also avoids a division by zero in the modulo."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why `k % n`?" | **The key point.** `k` reaches 2·10⁹ while `n ≤ 500`. Rotating by `n` is the identity, so only the remainder matters — otherwise it's 10¹² operations. |
| "What if `k` were **negative**?" | That's a left rotation. Use `k = k % n` (Python's modulo already returns a non-negative result for a positive divisor), or convert with `n - (abs(k) % n)`. |
| "Rotate **left** by `k` instead?" | Equivalent to rotating right by `n - k`. Same code with the index adjusted. |
| "Why close the loop?" | It turns two splices into one cut — the old-tail-to-old-head connection is made first, in O(1). |
| "Why `n - k - 1` steps?" | The new head is at index `n - k`, so the new tail is one before it; from index 0 that's `n - k - 1` steps. |
| "What if `n = 0`?" | The first guard returns before the modulo, avoiding `ZeroDivisionError`. |
| "Could you do it without computing the length?" | Not really — you need `n` for the modulo. A two-pointer gap approach still requires `n` to reduce `k`. |

**Traps:**

- **Forgetting `k % n`.** Either a 2-billion-iteration loop or walking off the end. *The* bug on this problem.
- **Computing `k % n` before the empty-list guard.** `ZeroDivisionError` when `n = 0`.
- **Off-by-one on the walk.** `n - k` steps lands on the new *head*, not the new tail — leaving the list mis-cut by one.
- **Not breaking the circle.** Returning while the list is still circular hangs the judge.
- **Reading `new_tail.next` after setting it to `None`.** Save the new head first.
- **Not re-checking `k == 0` after the modulo.** `k = 10, n = 5` reduces to 0; proceeding does a full pointless cycle (still correct, but wasteful and easy to get wrong).
- **Rotating one node at a time.** O(n·k) — hopeless.

**This same move shows up in:** [Next Greater Element II](503-next-greater-element-ii.md) (modular indexing to simulate a circular structure) · [Reverse Linked List II](92-reverse-linked-list-ii.md) (cutting and reconnecting a list at computed positions) · [Middle of the Linked List](876-middle-of-the-linked-list.md) (finding a position defined relative to the list's length) · [Partition List](86-partition-list.md) (relinking existing nodes rather than allocating new ones).

</details>

---
