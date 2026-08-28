# 876. Middle of the Linked List

**Easy** · [LeetCode](https://leetcode.com/problems/middle-of-the-linked-list/) · [Solution file (no hints)](../../problems/0500-0999/876.py)

[📖 06. Linked List lesson](../learning/06-linked-list.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 06. Linked List problems](../rmap-practice/06-linked-list.md)

---

Given the head of a singly linked list, return the **middle node**. If there are two middle nodes, return the **second** one.

```
head = [1,2,3,4,5]     →  [3,4,5]      (node 3 is the middle)
head = [1,2,3,4,5,6]   →  [4,5,6]      (two middles: 3 and 4 — return the second)
```

**Constraints:** `1 <= number of nodes <= 100` · `1 <= Node.val <= 100`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| **singly** linked list | ⚠️ You can only walk **forward**, and there's no `.length`. You can't index or go back |
| "return the **middle node**" | The node itself, not its value — so returning it also returns the rest of the list |
| "if two middles, return the **second**" | ⚠️ The tie-break that determines your loop condition exactly |
| `1 <= nodes` | Never empty, though handling `None` costs nothing |
| ≤ 100 nodes | Tiny — so this is about technique, not performance |

**The obstacle:** to find the middle you'd normally need the length, and getting that requires a full traversal. So the natural solution is **two passes** — count, then walk halfway. That's correct and O(n).

**The one-pass insight** — the technique this problem exists to teach:

> Run **two pointers at different speeds**. If `fast` moves twice as fast as `slow`, then when `fast` reaches the end, `slow` is exactly halfway.

```
[1] → [2] → [3] → [4] → [5] → None

start:  slow=1, fast=1
step 1: slow=2, fast=3
step 2: slow=3, fast=5
step 3: fast.next is None → stop.  slow=3 ✅
```

This is the **fast/slow pointer** (or "tortoise and hare") pattern, and it's the foundation for [Linked List Cycle](141-linked-list-cycle.md), [Palindrome Linked List](234-palindrome-linked-list.md), [Reorder List](143-reorder-list.md), and [Remove Nth Node From End](19-remove-nth-node-from-end-of-list.md). Learn it here where it's simplest.

🤔 **Before you open the next section:** if `fast` moves two steps for every one of `slow`'s, and `fast` has travelled the whole list, how far has `slow` travelled?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Copy to an array | Store all nodes, index the middle | O(n) | **O(n)** | ⚠️ Correct, wasteful |
| **Two passes** | Count, then walk `count // 2` | O(n) | O(1) | ✅ Correct, two traversals |
| **Fast/slow pointers** | One pass, two speeds | **O(n)** | **O(1)** | ✅✅ One traversal |

**The decision: fast and slow pointers.** The solution file carries the two-pass version too, and it's worth understanding both — the two-pass one is more obviously correct, the one-pass one is the technique that generalizes.

**Why `slow` lands on the middle.** When the loop ends, `fast` has taken roughly `n` steps and `slow` roughly `n/2`. More precisely: `slow` advances once per iteration and `fast` twice, so `fast`'s position is always about `2 × slow`'s. When `fast` runs out of list, `slow` is at the midpoint.

**The loop condition is where the tie-break lives**, and it's the only real decision in the problem:

| Condition | Even-length behaviour |
|---|---|
| `while fast and fast.next` | returns the **second** middle ✅ |
| `while fast.next and fast.next.next` | returns the **first** middle |

For `[1,2,3,4]`: the first condition gives node 3, the second gives node 2. The problem asks for the second middle, so `while fast and fast.next` is correct.

**Why both checks are needed.** `fast` moves two steps per iteration, so before doing `fast = fast.next.next` you must know:

- `fast` is not `None` (else `fast.next` raises `AttributeError`)
- `fast.next` is not `None` (else `fast.next.next` raises)

Python's `and` short-circuits left to right, so `fast and fast.next` checks them in the right order. Reversing them to `fast.next and fast` would crash on the very check meant to prevent the crash.

**Why not build an array?** It works and is easy, but it's O(n) memory to answer a question that needs none — and it defeats the purpose of practising pointer manipulation. Mention it, then do better.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

**Approach A — fast/slow pointers** (the one to write)

```python
slow = head
fast = head
```

Both start at the head. Starting them together is what makes `slow` land on the **second** middle for even-length lists — a subtle but deliberate choice.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
while fast and fast.next:
```

**The guard, and the tie-break, in one line.**

- `fast` — not `None`, so `fast.next` is safe to read
- `fast.next` — not `None`, so `fast.next.next` is safe

Short-circuit evaluation means the second check only runs if the first passed. Order matters here.
→ [while-loop](../syntax/while-loop.md) · [logical-operators](../syntax/logical-operators.md) · [none-type](../syntax/none-type.md)

```python
    slow = slow.next
    fast = fast.next.next
```

One step for `slow`, two for `fast`. The 2:1 ratio is the entire mechanism.
→ [class-basics](../syntax/class-basics.md)

```python
return slow
```

`fast` has exhausted the list, so `slow` sits at the middle. Returning the **node** means the caller receives that node and everything after it — which is why the expected output looks like a sublist.

<details>
<summary>Approach A together</summary>

```python
class Solution:
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:

        slow = head
        fast = head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        return slow
```

</details>

---

**Approach B — two passes** (also in the solution file)

```python
count = 0
node = head
while node:
    count += 1
    node = node.next
```

Pass 1: count the nodes. This is the traversal the one-pass version avoids.

```python
middle_index = count // 2
node = head
for _ in range(middle_index):
    node = node.next
return node
```

Pass 2: walk forward `count // 2` steps.

**Why `count // 2` gives the second middle.** For `n = 5`, `5 // 2 = 2`, so we take 2 steps from index 0 → index 2, the middle of five ✅. For `n = 6`, `6 // 2 = 3` → index 3, which is the **second** of the two middles (indices 2 and 3) ✅. Floor division happens to produce exactly the required tie-break.
→ [integer-division-modulo](../syntax/integer-division-modulo.md) · [range-function](../syntax/range-function.md)

<details>
<summary>Approach B together</summary>

```python
### Two passes ###
class Solution:
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:

        # Pass 1: count nodes
        count = 0
        node = head
        while node:
            count += 1
            node = node.next

        # Pass 2: walk to the middle index
        middle_index = count // 2
        node = head
        for _ in range(middle_index):
            node = node.next

        return node
```

</details>

**Trace the odd case** — `[1,2,3,4,5]`:

| Iteration | `slow` | `fast` | `fast and fast.next`? |
|---|---|---|---|
| start | 1 | 1 | ✅ (1, 2 exist) |
| 1 | 2 | 3 | ✅ (3, 4 exist) |
| 2 | 3 | 5 | ❌ `fast.next` is `None` → stop |

`return slow` = node **3** ✅ — the middle of five.

**Trace the even case** — `[1,2,3,4,5,6]`:

| Iteration | `slow` | `fast` | Continue? |
|---|---|---|---|
| start | 1 | 1 | ✅ |
| 1 | 2 | 3 | ✅ |
| 2 | 3 | 5 | ✅ (5, 6 exist) |
| 3 | 4 | `None` | ❌ `fast` is `None` → stop |

`return slow` = node **4** ✅ — the **second** of the two middles (3 and 4), exactly as specified.

Note the two exit conditions differ: the odd case stopped because `fast.next` was `None`, the even case because `fast` itself became `None`. Both checks earn their place.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** for both approaches.

- **Fast/slow:** `slow` takes `n/2` steps, `fast` takes `n` — about `1.5n` pointer moves in **one** traversal.
- **Two passes:** `n` steps to count plus `n/2` to walk — about `1.5n` moves across **two** traversals.

Identical operation counts, so the practical difference is small. The real advantages of one pass are:

1. **It works on a stream** — you never need to revisit the start, which matters if the list can only be read once.
2. **It generalizes.** The same skeleton detects cycles ([Linked List Cycle](141-linked-list-cycle.md)), finds the `k`-th node from the end ([Remove Nth Node](19-remove-nth-node-from-end-of-list.md)), and splits a list for reversal ([Palindrome Linked List](234-palindrome-linked-list.md)).

You can't beat O(n) — the middle's position depends on the length, and finding the length requires reading every node.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — two pointers, regardless of list length.

The array-copy approach would be O(n), storing every node just to index one of them. That trade is never worth it here.

**Why this matters beyond the problem:** linked lists are the classic setting where you *cannot* fall back on indexing, so pointer techniques have to substitute for random access. Fast/slow pointers are the general answer to "find a position defined relative to the list's length, in one pass and constant space."

The pattern's shape is worth memorizing:

| Goal | Pointer setup |
|---|---|
| **Middle** | both at head; `fast` moves 2× |
| **Cycle detection** | both at head; `fast` moves 2×; they meet iff there's a cycle |
| **`k`-th from the end** | `fast` starts `k` ahead; both move 1× |
| **Split for reversal** | find the middle, then reverse from there |

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "I can't index into a linked list and there's no length, so the obvious solution is two passes — count the nodes, then walk halfway. But I can do it in one pass with fast and slow pointers: `slow` advances one node per step, `fast` advances two, so when `fast` reaches the end, `slow` is at the middle. The loop condition `while fast and fast.next` does two jobs — it guards both dereferences before `fast = fast.next.next`, and it produces the *second* middle on even-length lists, which is what the problem asks for. If I wanted the first middle I'd condition on `fast.next and fast.next.next` instead. O(n) time, O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Return the **first** middle on even lengths." | Change the condition to `while fast.next and fast.next.next`. |
| "Find the node **1/3** of the way in?" | Move `fast` three steps per one of `slow`'s — the ratio generalizes. |
| "Detect a **cycle**." | Same two pointers; if they ever meet, there's a cycle. [Linked List Cycle](141-linked-list-cycle.md). |
| "Find the `k`-th node from the end." | Start `fast` `k` nodes ahead, then advance both by one. [Remove Nth Node](19-remove-nth-node-from-end-of-list.md). |
| "Why not count first?" | You can — it's equally O(n)/O(1). One pass is preferable for streams and generalizes to cycle detection. |
| "What if the list were **doubly** linked?" | You could walk from both ends inward and meet in the middle — same complexity, different mechanics. |
| "Empty list?" | Constraints forbid it, but `head = None` returns `None` correctly since the loop never runs. |

**Traps:**

- **Checking `fast.next` before `fast`.** `AttributeError` on the exact case the guard exists for. Order the `and` correctly.
- **Only checking `while fast`.** `fast.next.next` then crashes on even-length lists.
- **Using `while fast.next and fast.next.next`** when the problem wants the second middle. It returns the first.
- **Returning `slow.val`.** The problem asks for the **node**.
- **Advancing `fast` by one.** Then both pointers move together and `slow` ends at the tail, not the middle.
- **Starting `fast = head.next`.** Shifts the tie-break; it returns the first middle instead.

**This same move shows up in:** [Linked List Cycle](141-linked-list-cycle.md) (fast/slow to detect a loop) · [Palindrome Linked List](234-palindrome-linked-list.md) (find the middle, then reverse the second half) · [Reorder List](143-reorder-list.md) (split at the middle, reverse, interleave) · [Remove Nth Node From End of List](19-remove-nth-node-from-end-of-list.md) (two pointers with a fixed gap).

</details>

---
