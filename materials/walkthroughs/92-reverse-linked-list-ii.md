# 92. Reverse Linked List II

**Medium** · [LeetCode](https://leetcode.com/problems/reverse-linked-list-ii/) · [Solution file (no hints)](../../problems/0001-0499/92.py)

[📖 06. Linked List lesson](../learning/06-linked-list.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 06. Linked List problems](../rmap-practice/06-linked-list.md)

---

Given the head of a singly linked list and two integers `left` and `right` where `left <= right`, reverse the nodes from position `left` to position `right` (**1-indexed**) and return the list.

```
head = [1,2,3,4,5], left = 2, right = 4  →  [1,4,3,2,5]
head = [5], left = 1, right = 1          →  [5]
```

**Constraints:** `1 <= n <= 500` · `-500 <= Node.val <= 500` · `1 <= left <= right <= n`

**Follow-up:** could you do it in **one pass**?

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| reverse **positions `left` to `right`** | A **sublist** reversal, not the whole list — the surrounding nodes must stay put |
| **1-indexed** | ⚠️ Position 1 is the head. Off-by-one errors live here |
| `left` can be **1** | ⚠️ The head itself may be inside the reversed segment ⇒ **dummy node** |
| `left == right` | Reversing one node is a no-op — must not corrupt anything |
| follow-up: **one pass** | The straightforward approach already achieves this |
| `n <= 500` | Small; correctness matters far more than constants |

**Why this is harder than [Reverse Linked List](206-reverse-linked-list.md).** Reversing an entire list is a clean three-pointer loop. Reversing a *middle segment* means you must also **reconnect** it correctly at both ends:

```
      1  →  2  →  3  →  4  →  5
      ↑     └────────────┘     ↑
   before      reverse       after
      
result:  1 → 4 → 3 → 2 → 5
         ↑   ↑           ↑
    before  new head   old head of the
            of segment  segment now points here
```

Four nodes matter, and naming them is most of the battle:

| Name | Role | After reversal |
|---|---|---|
| **`prev`** | node at position `left - 1` | must point at the segment's **new** head |
| **`start`** | node at position `left` (segment's old head) | becomes the segment's **tail** |
| — | node at position `right` (segment's old tail) | becomes the segment's **new head** |
| — | node at position `right + 1` | `start` must point here |

**The two reconnections** are what people get wrong:

1. `prev.next` → the node that was at `right`
2. the node originally at `left` → the node that was at `right + 1`

Miss either and you get a truncated list or a cycle.

**Why a dummy node.** If `left == 1`, there *is* no node at position `left - 1`, and the head changes. A sentinel before the head supplies the missing predecessor and makes `dummy.next` the reliable return — same reasoning as [Remove Linked List Elements](203-remove-linked-list-elements.md) and [Swap Nodes in Pairs](24-swap-nodes-in-pairs.md).

🤔 **Before you open the next section:** if you reverse the segment in place, which node ends up as its tail — and what should that tail point to?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Collect values, rewrite | Copy the segment's values, reverse, write back | O(n) | **O(k)** | ⚠️ Correct, but it's a value swap in disguise |
| Cut, reverse, rejoin | Detach the segment, reverse it, splice it back | O(n) | O(1) | ✅ Correct, needs care with the cut |
| **Head-insertion in place** | Repeatedly move the node after `start` to the front | **O(n)** | **O(1)** | ✅✅ One pass, no detaching |
| **Standard reversal + reconnect** | Walk to `left`, run the three-pointer loop `k` times, reconnect | **O(n)** | **O(1)** | ✅ Most familiar |

**The decision: walk to position `left - 1`, run the standard reversal for `right - left + 1` nodes, then reconnect both ends.**

This reuses the reversal loop you already know from [Reverse Linked List](206-reverse-linked-list.md) rather than inventing new machinery — usually the right call under interview pressure.

**The algorithm:**

1. Place a `dummy` before the head; set `prev = dummy`.
2. Advance `prev` by `left - 1` steps, so it sits at position `left - 1`.
3. Let `start = prev.next` — the segment's original head, which will become its tail.
4. Run the three-pointer reversal for exactly `right - left + 1` nodes.
5. Reconnect: `prev.next = <new segment head>` and `start.next = <node after the segment>`.

**The head-insertion alternative** is worth knowing because it's shorter and needs no separate reconnect step:

```python
for _ in range(right - left):
    moved = start.next          # node just after start
    start.next = moved.next     # unlink it
    moved.next = prev.next      # put it at the segment's front
    prev.next = moved
```

Each iteration lifts the node *after* `start` and re-inserts it immediately after `prev`. After `right - left` moves the segment is reversed, and — crucially — **the connections at both ends stay correct throughout**, because `start` never moves and always trails the segment. It's the tidier solution once it clicks; the explicit reversal is the more obviously-correct one.

**Why one pass is achievable.** You walk to `left` once (`left - 1` steps), then reverse `k` nodes (`k` steps). No node is visited more than twice, and you never restart from the head. The follow-up is satisfied by the natural solution.

**Why not collect values?** Copying the segment's values into a list, reversing, and writing them back is O(k) space — and it sidesteps the pointer manipulation the problem is testing, much like the value-swap shortcut in [Swap Nodes in Pairs](24-swap-nodes-in-pairs.md).

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
if not head or left == right:
    return head
```

**Early exit.** A single-node segment needs no work, and this also covers `left == right == 1`. Cheap, and it removes a class of edge cases from everything below.
→ [truthy-falsy-values](../syntax/truthy-falsy-values.md) · [if-return](../syntax/if-return.md)

```python
dummy = ListNode(0)
dummy.next = head
prev = dummy
```

**The sentinel**, so `left == 1` needs no special case and `dummy.next` is always the correct head to return.
→ [class-basics](../syntax/class-basics.md)

```python
for _ in range(left - 1):
    prev = prev.next
```

**Walk to the node before the segment.**

`left - 1` steps from `dummy` lands `prev` on position `left - 1` — because `dummy` is effectively position 0. When `left == 1` the loop runs zero times and `prev` stays at `dummy`, which is exactly right.
→ [range-function](../syntax/range-function.md) · [for-loop](../syntax/for-loop.md)

```python
start = prev.next
```

The segment's original head. **After reversal this becomes the segment's tail**, so we save it now — we'll need it to make the second reconnection.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
current = start
previous = None

for _ in range(right - left + 1):
    next_node = current.next
    current.next = previous
    previous = current
    current = next_node
```

**The standard reversal**, run exactly `right - left + 1` times — the segment's length.

Same four-step dance as [Reverse Linked List](206-reverse-linked-list.md): save, flip, advance, advance. The `next_node` save is mandatory; without it the link to the rest of the list is destroyed.

When this finishes:
- `previous` = the segment's **new head** (originally the node at `right`)
- `current` = the node **after** the segment (originally at `right + 1`), or `None`

```python
prev.next = previous
start.next = current
```

**The two reconnections — the part unique to this problem.**

1. `prev.next = previous` — the node before the segment now points at its new head.
2. `start.next = current` — the segment's new tail (which was its head) points at whatever followed the segment.

Getting either wrong produces a truncated list or a cycle. Both are needed, always.

```python
return dummy.next
```

`dummy.next` rather than `head`, since the head may have been inside the reversed segment.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def reverseBetween(self, head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:

        if not head or left == right:
            return head

        dummy = ListNode(0)
        dummy.next = head
        prev = dummy

        for _ in range(left - 1):
            prev = prev.next

        start = prev.next
        current = start
        previous = None

        for _ in range(right - left + 1):
            next_node = current.next
            current.next = previous
            previous = current
            current = next_node

        prev.next = previous
        start.next = current

        return dummy.next
```

</details>

<details>
<summary>The head-insertion variant (shorter, no explicit reconnect)</summary>

```python
class Solution:
    def reverseBetween(self, head, left, right):
        dummy = ListNode(0)
        dummy.next = head
        prev = dummy

        for _ in range(left - 1):
            prev = prev.next

        start = prev.next
        for _ in range(right - left):
            moved = start.next
            start.next = moved.next
            moved.next = prev.next
            prev.next = moved

        return dummy.next
```

Each iteration lifts the node after `start` and re-inserts it right after `prev`. Because `start` never moves and always trails the segment, both boundary connections remain valid at every step — so no reconnection is needed at the end.

</details>

**Trace it** — `head = [1,2,3,4,5]`, `left = 2`, `right = 4`:

*Setup:* `dummy → 1 → 2 → 3 → 4 → 5`. Walk `left - 1 = 1` step → `prev` = node **1**. `start` = node **2**.

*Reverse `right - left + 1 = 3` nodes, beginning at node 2:*

| Iteration | `current` | `next_node` | Flip | `previous` after |
|---|---|---|---|---|
| 1 | 2 | 3 | 2 → `None` | 2 |
| 2 | 3 | 4 | 3 → 2 | 3 |
| 3 | 4 | 5 | 4 → 3 | **4** |

After the loop: `previous` = node **4** (new segment head), `current` = node **5** (the node after the segment).

The segment now reads `4 → 3 → 2 → None`, and node 1 still points at node 2 — the list is temporarily broken.

*Reconnect:*

| Step | Operation | Effect |
|---|---|---|
| 1 | `prev.next = previous` | node 1 → node 4 |
| 2 | `start.next = current` | node 2 → node 5 |

Final: `dummy → 1 → 4 → 3 → 2 → 5`

Return **`[1,4,3,2,5]`** ✅

**The `left == 1` case** — `[1,2,3]`, `left = 1`, `right = 3`: the walk loop runs **zero** times so `prev` stays at `dummy`, `start` = node 1. After reversing all three, `prev.next = 3` makes `dummy → 3 → 2 → 1`, and `start.next = None` terminates it. Return `[3,2,1]` ✅ — handled entirely by the sentinel, with no branch.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)**, in a **single pass**.

- Walking to position `left - 1`: `left - 1` steps
- Reversing the segment: `right - left + 1` steps

Total = `right` steps, which is at most `n`. No node is visited more than twice, and you never return to the head.

That satisfies the follow-up directly — the natural solution is already one-pass, so there's no clever second version to reach for.

**Best case** is O(1)-ish when `left == right` (the early exit fires immediately). **Worst case** is `left = 1, right = n`, where you reverse the entire list — which is exactly [Reverse Linked List](206-reverse-linked-list.md).

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — the dummy node plus a fixed set of pointers, regardless of `n` or the segment's length.

| | Space |
|---|---|
| Collect values, rewrite | O(k) for the segment's values |
| Recursive reversal | O(k) stack |
| **In-place rewiring** | **O(1)** ✅ |

**The four pointers you must keep straight** — writing them down before coding is the single best defence against bugs here:

| Pointer | Meaning |
|---|---|
| `prev` | node before the segment (position `left - 1`) |
| `start` | segment's original head → becomes its **tail** |
| `previous` | after reversal, the segment's **new head** |
| `current` | node after the segment (position `right + 1`) |

The reversal itself is mechanical; the difficulty is entirely in the bookkeeping. That's why the head-insertion variant is appealing — it maintains both boundary connections automatically and needs only `prev` and `start`.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "This is a sublist reversal, so beyond the standard three-pointer reversal I need to reconnect both ends. I use a dummy node because `left` can be 1, which means the head is inside the reversed segment. I walk `prev` forward `left - 1` steps to sit just before the segment, save `start = prev.next` — that's the segment's current head, which will become its tail — then run the standard reversal for exactly `right - left + 1` nodes. Afterwards `previous` is the segment's new head and `current` is the node after it, so I reconnect `prev.next = previous` and `start.next = current`. One pass, O(n) time, O(1) space. There's also a head-insertion variant that repeatedly moves the node after `start` to the front of the segment — slightly shorter, and it keeps both boundary links valid throughout."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "One pass?" | **The stated follow-up** — already satisfied. You walk to `left` once and reverse once; nothing is revisited. |
| "Why a dummy node?" | `left` can be 1, so the head may change and position `left - 1` may not exist. |
| "What are the two reconnections?" | `prev.next` → the segment's new head; the segment's original head → the node after the segment. |
| "Show the head-insertion version." | Repeatedly lift `start.next` and re-insert it after `prev`, `right - left` times. No explicit reconnect needed. |
| "Reverse in **k-sized groups** instead." | [Reverse Nodes in k-Group](25-reverse-nodes-in-k-group.md) — apply this repeatedly, checking a full group exists first. |
| "What if `left == right`?" | The early exit returns immediately; reversing one node is a no-op. |
| "What if `right == n`?" | `current` ends as `None`, so `start.next = None` correctly terminates the list. |

**Traps:**

- **Forgetting one of the two reconnections.** Missing `prev.next` orphans the segment; missing `start.next` truncates the list or creates a cycle.
- **Off-by-one on the walk.** It's `left - 1` steps from `dummy`, not `left`. 1-indexing is the hazard.
- **Off-by-one on the reversal count.** The segment has `right - left + 1` nodes; dropping the `+ 1` leaves the last one unreversed.
- **Omitting the dummy.** `left == 1` then needs a special case for the changed head.
- **Losing `start`.** You must save the segment's original head *before* reversing — afterwards there's no way to find it.
- **Returning `head`.** It may now be in the middle of the list. Return `dummy.next`.
- **Forgetting `next_node` in the reversal loop.** Destroys the rest of the list.

**This same move shows up in:** [Reverse Linked List](206-reverse-linked-list.md) (the reversal loop this builds on) · [Reverse Nodes in k-Group](25-reverse-nodes-in-k-group.md) (this operation applied repeatedly) · [Swap Nodes in Pairs](24-swap-nodes-in-pairs.md) (the k=2 special case, with a dummy for the same reason) · [Remove Linked List Elements](203-remove-linked-list-elements.md) (the dummy-node pattern in its simplest form).

</details>

---
