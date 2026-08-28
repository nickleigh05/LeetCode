# 83. Remove Duplicates from Sorted List

**Easy** · [LeetCode](https://leetcode.com/problems/remove-duplicates-from-sorted-list/) · [Solution file (no hints)](../../problems/0001-0499/83.py)

[📖 06. Linked List lesson](../learning/06-linked-list.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 06. Linked List problems](../rmap-practice/06-linked-list.md)

---

Given the head of a **sorted** linked list, delete all duplicates so each value appears only **once**. Return the sorted list.

```
head = [1,1,2]      →  [1,2]
head = [1,1,2,3,3]  →  [1,2,3]
```

**Constraints:** `0 <= number of nodes <= 300` · `-100 <= Node.val <= 100` · the list is sorted **ascending**

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**sorted**" | ⚠️ Duplicates are **adjacent**. Detecting one is a comparison with your immediate neighbour — no set, no memory |
| "each value appears **once**" | Keep the **first** occurrence of each value, drop the rest |
| "return the sorted list" | Order is preserved automatically; you're only deleting |
| `0 <= nodes` | The list may be empty |
| the head is **never** deleted | ⚠️ Unlike [Remove Linked List Elements](203-remove-linked-list-elements.md) — the first node of a sorted list can't be a duplicate of anything before it |

**Why this needs no dummy node.** In [problem 203](203-remove-linked-list-elements.md) the head could be removed, so a sentinel was needed to give it a predecessor and to report the true head. Here the head is **always kept** — it's the first occurrence of its value by definition. So `head` is always the correct return value, and you can work directly with a single pointer.

That contrast is worth internalizing:

| | Can the head be deleted? | Dummy needed? |
|---|---|---|
| [203 Remove Elements](203-remove-linked-list-elements.md) | ✅ yes | ✅ yes |
| **83 Remove Duplicates** | ❌ never | ❌ no |

**The mechanic.** Sortedness means equal values sit next to each other, so you only ever compare `current` with `current.next`:

```
[1] → [1] → [2] → [3] → [3] → None
 ↑     ↑
same → skip the second one
```

When they match, splice out the successor: `current.next = current.next.next`. When they differ, advance.

🤔 **Before you open the next section:** after you splice out a duplicate, should you advance `current` — or might the *new* successor also be a duplicate?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Hash set of seen values | Track values, unlink repeats | O(n) | **O(n)** | ❌ Ignores sortedness; wastes memory |
| Rebuild a new list | Copy first occurrences into a fresh list | O(n) | O(n) | ❌ Allocates needlessly |
| **Single pointer, compare neighbours** | Splice out equal successors in place | **O(n)** | **O(1)** | ✅ |
| Recursion | `head.next = deleteDuplicates(head.next)` then dedupe | O(n) | O(n) stack | ⚠️ Elegant, unnecessary stack |

**The decision: one pointer, comparing `current.val` with `current.next.val`.**

**Why sortedness makes O(1) space possible.** On an *unsorted* list you'd need to remember every value seen — that's a hash set and O(n) memory. Sorted input collapses "have I seen this value anywhere?" into "is it the same as my neighbour?", which needs no memory at all.

That's the same leverage as in [Remove Duplicates from Sorted Array](26-remove-duplicates-from-sorted-array.md) — recognizing that the word "sorted" is what buys the constant space.

**The critical decision: when to advance.**

```python
if current.val == current.next.val:
    current.next = current.next.next   # splice — do NOT advance
else:
    current = current.next             # advance
```

After splicing out a duplicate, **`current` must stay put**, because the newly attached successor might *also* be a duplicate. On `[1,1,1]`:

- stay: splice the second 1, then the third → `[1]` ✅
- advance: splice the second 1, move to the third, and it's now the last node → `[1,1]` ❌

Advancing unconditionally is the defining bug on this problem, and it only shows up with **three or more** consecutive equal values — so `[1,1,2]` passes and `[1,1,1]` fails. Test triples.

**Why no dummy node.** As established, the head survives unconditionally, so there's nothing for a sentinel to protect. Adding one isn't wrong, just unnecessary — and knowing *when* the pattern is needed is more valuable than always applying it.

**Why not recursion?** `head.next = self.deleteDuplicates(head.next); return head.next if head.val == head.next.val else head` works, but costs O(n) stack for no benefit. At 300 nodes it's safe, but the iterative version is strictly better.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
current: Optional[ListNode] = head
```

A single walking pointer, starting at the head. The type annotation documents that it may be `None` — the list can be empty.

Note there's no `prev`: because you're comparing `current` against `current.next` and splicing the *successor*, the node doing the unlinking is `current` itself.
→ [variables-assignment](../syntax/variables-assignment.md) · [type-hints](../syntax/type-hints.md)

```python
while current is not None and current.next is not None:
```

**Both checks, in this order.**

- `current is not None` — the list isn't empty and we haven't run off the end
- `current.next is not None` — there's a neighbour to compare against

Short-circuiting means `current.next` is only evaluated after `current` is known non-`None`. Reversing them crashes on an empty list.

Stopping when `current.next` is `None` is correct: the last node has no successor and therefore can't be followed by a duplicate.
→ [while-loop](../syntax/while-loop.md) · [logical-operators](../syntax/logical-operators.md) · [none-type](../syntax/none-type.md)

```python
    if current.val == current.next.val:
        current.next = current.next.next
```

**Splice out the duplicate.** Point past the neighbour, dropping it from the list.

`current` deliberately does **not** advance — the node now sitting at `current.next` is unexamined and may be another duplicate. Staying put re-tests it on the next iteration.

The orphaned node is garbage-collected once nothing references it.
→ [comparison-operators](../syntax/comparison-operators.md)

```python
    else:
        current = current.next
```

**Different value — advance.** The current node is finished; move on to start comparing the next distinct value.
→ [elif-else](../syntax/elif-else.md)

```python
return head
```

**Return `head` unchanged.** It was never removed, so it's still the correct head — no `dummy.next` needed.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:

        current: Optional[ListNode] = head

        while current is not None and current.next is not None:
            if current.val == current.next.val:
                current.next = current.next.next
            else:
                current = current.next

        return head
```

</details>

**Trace it** — `head = [1,1,2,3,3]`:

| `current` | `current.next` | Equal? | Action | List after |
|---|---|---|---|---|
| 1₁ | 1₂ | ✅ | splice; **stay** | `[1,2,3,3]` |
| 1₁ | 2 | ❌ | advance | unchanged |
| 2 | 3₁ | ❌ | advance | unchanged |
| 3₁ | 3₂ | ✅ | splice; **stay** | `[1,2,3]` |
| 3₁ | `None` | — | loop ends | `[1,2,3]` |

`return head` = **`[1,2,3]`** ✅

**The triple case that exposes the advance bug** — `[1,1,1]`:

| `current` | `current.next` | Equal? | Action | List after |
|---|---|---|---|---|
| 1₁ | 1₂ | ✅ | splice; **stay** | `[1,1]` (1₁ → 1₃) |
| 1₁ | 1₃ | ✅ | splice; **stay** | `[1]` |
| 1₁ | `None` | — | loop ends | `[1]` |

`return head` = **`[1]`** ✅

Had `current` advanced after the first splice, it would have moved to 1₃ — the last node — the loop would exit, and the result would be `[1,1]`. That single missing behaviour is the whole bug.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

Each iteration either **removes a node** or **advances `current`**. There are at most `n` removals and at most `n` advances, so the loop runs at most `2n` times — **O(n)**.

That's worth stating carefully, because the loop doesn't advance on every iteration, so "one pass" isn't quite the right description. The bound comes from a **decreasing quantity**: each iteration either shrinks the list or moves the pointer forward, and neither can happen more than `n` times.

Same amortized style of argument as in the sliding-window problems — a loop whose progress is guaranteed by a global budget rather than a simple counter.

**Splicing is O(1)**, versus O(n) for removing from the middle of an array. That's the linked list's structural advantage.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — a single pointer, no allocation, no sentinel.

**What sortedness bought you:**

| | Space | Requires sorted input? |
|---|---|---|
| Hash set of seen values | **O(n)** | ❌ works on any list |
| **Neighbour comparison** | **O(1)** | ✅ |

On unsorted input you genuinely need the set, because a duplicate can be arbitrarily far away. Sorted input localizes the question to adjacent nodes, and local questions need no memory.

This is exactly the same trade as [Remove Duplicates from Sorted Array](26-remove-duplicates-from-sorted-array.md) — different data structure, identical reasoning. Noticing that the word "sorted" is doing the work is the transferable skill.

**And note what you *didn't* need:** no dummy node, because the head is never deleted. Recognizing when a pattern is unnecessary is as useful as knowing when to apply it.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The list is sorted, so duplicates are adjacent — I don't need a set to detect them, just a comparison with the next node. I walk with a single pointer: if `current.val == current.next.val`, I splice out the successor with `current.next = current.next.next` and **don't** advance, because the new successor might also be a duplicate. Otherwise I advance. No dummy node is needed here, unlike Remove Linked List Elements, because the head of a sorted list is always the first occurrence of its value and can never be deleted — so I just return `head`. O(n) time, O(1) space, and the constant space comes directly from the sortedness."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Remove **all** nodes that have duplicates, keeping only distinct values." | [LeetCode 82](https://leetcode.com/problems/remove-duplicates-from-sorted-list-ii/) — `[1,1,2]` → `[2]`. Now the head *can* be deleted, so you **do** need a dummy, plus a skip-the-whole-run loop. Meaningfully harder. |
| "What if the list weren't sorted?" | You'd need a hash set of seen values — O(n) space. Sortedness is what buys O(1). |
| "Why no dummy node?" | The head is the first occurrence of its value, so it's never removed and `head` is always the right return. |
| "Why not advance after splicing?" | The new successor is unexamined and may also be a duplicate. `[1,1,1]` exposes it. |
| "Do it recursively." | `head.next = deleteDuplicates(head.next)`, then return `head.next` if the values match else `head`. O(n) stack. |
| "Keep the **last** occurrence instead?" | Symmetric — or reverse, dedupe, reverse back. |
| "Should you free the spliced node?" | Python garbage-collects it. In C/C++ save the pointer before unlinking, then free. |

**Traps:**

- **Advancing after a splice.** *The* bug — invisible on `[1,1,2]`, wrong on `[1,1,1]`. Always test a triple.
- **Checking `current.next` before `current`.** Crashes on an empty list; short-circuit order matters.
- **Adding an unnecessary dummy node.** Harmless but signals you haven't reasoned about whether the head can change.
- **Returning `current` instead of `head`.** `current` ends near the tail.
- **Confusing this with [LeetCode 82](https://leetcode.com/problems/remove-duplicates-from-sorted-list-ii/).** That one deletes *every* node in a duplicate run, including the first — a genuinely different problem needing a dummy.
- **Reaching for a hash set.** Correct but O(n) space, and it ignores the property the problem handed you.

**This same move shows up in:** [Remove Duplicates from Sorted Array](26-remove-duplicates-from-sorted-array.md) (identical reasoning on an array) · [Remove Linked List Elements](203-remove-linked-list-elements.md) (the same splice mechanic, but the head *can* be deleted so a dummy is required) · [Middle of the Linked List](876-middle-of-the-linked-list.md) (single-pass pointer traversal) · [Merge Two Sorted Lists](21-merge-two-sorted-lists.md) (exploiting sortedness to avoid extra structures).

</details>

---
