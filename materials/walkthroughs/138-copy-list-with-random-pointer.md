# 138. Copy List with Random Pointer

**Medium** · [LeetCode](https://leetcode.com/problems/copy-list-with-random-pointer/)

[📖 07. Linked List lesson](../learning/07-linked-list.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 07. Linked List problems](../rmap-practice/07-linked-list.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

A linked list of length `n` is given, where each node contains an additional **`random` pointer** which can point to **any node in the list, or `null`**.

Construct a **deep copy** of the list: the copy must consist of exactly `n` brand-new nodes, where each new node's `next` and `random` pointers point to **new nodes in the copied list** — never to nodes in the original.

```
original:  [7,null] → [13,0] → [11,4] → [10,2] → [1,0]
                       (the second value is the index its `random` points to)

copy:      an identical structure made entirely of new nodes
```

**Constraints:** `0 <= n <= 1000` · `random` is `null` or points to some node in the list

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**deep** copy" | ⚠️ Brand-new nodes. Not a shallow copy, not a reference to the same list |
| "pointers point to **new nodes**" | Every pointer in the copy must be *translated* — original node → its copy |
| "`random` can point to **any** node" | ⚠️ **Forwards, backwards, or at itself.** No traversal order can guarantee the target already exists |
| "`random` can be `null`" | An edge case to handle without a branch, ideally |
| n can be **0** | Empty input → return `None` |
| n ≤ 1000 | O(n) or O(n log n) both fine; O(n²) would also pass but isn't the point |

Copying `next` alone would be easy — walk the list, create each node, link as you go. The `random` pointer is what breaks that.

**Why:** suppose you're copying node 0, whose `random` points at node 3. Node 3's copy doesn't exist yet. You could create it on demand — but then when you reach node 3 in the normal traversal you'd need to know you already made it, or you'd create a duplicate.

Turn that into the actual requirement: you need a way to ask

> **"Given an original node, what is its copy?"**

for *any* node, at any moment — regardless of whether you've reached it yet in the traversal.

That's a **lookup from original → copy**. Which is a hash map.

And once you frame it that way, the fix falls out: **create all the nodes first, then wire all the pointers.** In the second pass every copy already exists, so every lookup succeeds.

🤔 **Before you open the next section:** if you did it in a single pass, what would go wrong when a `random` pointer aims at a node further down the list?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Copy `next` first, then find each `random` by index | For each node, walk to find the target's copy | O(n²) | O(1) | ⚠️ Correct, quadratic |
| Recursion + memo | Copy on demand, memoize by original node | O(n) | O(n) | ✅ Same idea, recursive |
| **Hash map, two passes** | Create all nodes, then wire all pointers | **O(n)** | **O(n)** | ✅ |
| Interleave copies into the original | Weave copies in, set randoms, unweave | O(n) | **O(1)** | ✅ The clever follow-up |

**The decision: a [hash map](../data-structures/hashmap.md) from original node → copied node, filled in two passes.**

- **Pass 1:** for every original node, create a copy holding just its value. Record `original → copy`. Pointers are left unset.
- **Pass 2:** for every original node, set `copy.next = map[original.next]` and `copy.random = map[original.random]`.

**Why two passes is the whole trick.** After pass 1, *every* copy exists. So in pass 2, any pointer the original has — forward, backward, self-referential — can be translated by a lookup that's guaranteed to hit. **Separating "create the objects" from "connect the objects" removes the ordering problem entirely.**

That's a genuinely general technique. The same shape appears when deserializing object graphs, resolving symbol references in a compiler, or fixing up foreign keys after a bulk database import.

**The `{None: None}` seed.** Initializing the map with `None → None` means `map[original.random]` works even when `random` is `null` — the lookup returns `None`, which is exactly the right value. **The null case is handled by data instead of by a branch**, which is the same instinct as the `±inf` sentinels in [Median of Two Sorted Arrays](4-median-of-two-sorted-arrays.md).

**Why nodes can be dict keys.** Python objects are hashable by identity by default, so `map[node]` keys on *which node it is*, not its value — correct here, since duplicate values are allowed.

**The O(1)-space alternative** is worth knowing: interleave each copy directly after its original (`A → A' → B → B' → …`), so each copy is reachable as `original.next`. Then `copy.random = original.random.next`. Finally unweave the two lists. Three passes, no map — a great follow-up answer, but harder to write correctly.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
old_to_copy = {None: None}
```

The translation table: **original node → its copy**.

Seeding it with `None: None` is the detail that removes every null check. When a node's `next` or `random` is `None`, the lookup returns `None` — the correct value — instead of raising `KeyError`. It also makes the empty-list case work: `old_to_copy[head]` with `head = None` returns `None`.
→ [dict-basics](../syntax/dict-basics.md) · [none-type](../syntax/none-type.md)

```python
curr = head
while curr:
    old_to_copy[curr] = Node(curr.val)
    curr = curr.next
```

**Pass 1 — create every node.** Walk the original list and make a copy of each, storing only the value. Both pointers are left at their default `None`.

Using the node object itself as the dict key works because Python hashes objects by identity — two different nodes with the same value are distinct keys.

After this loop, **every copy exists**, which is what makes pass 2 safe.
→ [while-loop](../syntax/while-loop.md) · [class-basics](../syntax/class-basics.md) · [truthy-falsy-values](../syntax/truthy-falsy-values.md)

```python
curr = head
while curr:
    copy = old_to_copy[curr]
    copy.next = old_to_copy[curr.next]
    copy.random = old_to_copy[curr.random]
    curr = curr.next
```

**Pass 2 — wire every pointer.** Walk the original list again. For each node, look up its copy, then translate both of its pointers through the map.

Read `copy.next = old_to_copy[curr.next]` carefully — it's the heart of the solution:
- `curr.next` is the **original** node that follows.
- `old_to_copy[...]` converts it to the **corresponding copy**.
- So the copy's `next` points into the copied list, never the original.

The `random` line is identical in form, and works no matter where the pointer aims — the map has every node. When `curr.random` is `None`, the seed entry returns `None`. ✅
→ [dict-basics](../syntax/dict-basics.md)

```python
return old_to_copy[head]
```

The copy of the original head. And if `head` is `None`, the seeded entry returns `None` — empty input handled with no guard.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def copyRandomList(self, head: Optional[Node]) -> Optional[Node]:

        old_to_copy = {None: None}

        curr = head
        while curr:
            old_to_copy[curr] = Node(curr.val)
            curr = curr.next

        curr = head
        while curr:
            copy = old_to_copy[curr]
            copy.next = old_to_copy[curr.next]
            copy.random = old_to_copy[curr.random]
            curr = curr.next

        return old_to_copy[head]
```

</details>

**Trace it** — original `A(7) → B(13) → C(11)`, with `A.random = C`, `B.random = A`, `C.random = None`:

**Pass 1** — create the nodes:

| Original | Copy created | Map after |
|---|---|---|
| A(7) | A'(7) | `{None:None, A:A'}` |
| B(13) | B'(13) | `… B:B'` |
| C(11) | C'(11) | `… C:C'` |

All three copies exist, all pointers still `None`.

**Pass 2** — wire them:

| Node | `copy.next = map[…]` | `copy.random = map[…]` |
|---|---|---|
| A | `map[B]` = **B'** | `map[C]` = **C'** |
| B | `map[C]` = **C'** | `map[A]` = **A'** |
| C | `map[None]` = **None** | `map[None]` = **None** |

Result: `A'(7) → B'(13) → C'(11)`, with `A'.random = C'`, `B'.random = A'`, `C'.random = None` ✅

Note row A: `A.random` pointed **forward** to C, which hadn't been visited yet in a single-pass approach — but after pass 1, `C'` already existed. That's the ordering problem dissolving.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

| Pass | Cost |
|---|---|
| Create every node | n iterations, each O(1) — one allocation, one dict insert |
| Wire every pointer | n iterations, each O(1) — three dict lookups |

Two **sequential** passes: O(n) + O(n) = **O(n)**. Sequential loops add rather than multiply — the same accounting as [Valid Anagram](242-valid-anagram.md).

Dict operations are O(1) average, so each pointer translation is constant.

**Versus the O(n²) alternative:** without the map, resolving each `random` means walking the list to find the target's position, then walking the copy to the same position — O(n) per node, O(n²) total. At n = 1000 that's 10⁶ operations versus 2000.

**This is the [arrays & hashing](../learning/01-arrays-hashing.md) trade in a new setting:** O(n) memory buys O(1) lookups and collapses a quadratic search into a linear pass. Same bargain as [Two Sum](1-two-sum.md), applied to object identity rather than values.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** for the map, holding one entry per node.

**Note the distinction interviewers care about:** the copied list itself is O(n), but that's the **required output**, not auxiliary space. The map is the genuine overhead — so the honest phrasing is *"O(n) auxiliary for the map, plus the O(n) output."*

**The O(1)-auxiliary alternative** — interleaving — is the natural follow-up:

```
1. Weave:    A → A' → B → B' → C → C'      (each copy right after its original)
2. Randoms:  A'.random = A.random.next     (a node's copy is always .next)
3. Unweave:  separate back into two lists
```

It replaces the map with the list's own structure: *"where is this node's copy?"* becomes *"one step forward."* Three passes, **O(1) auxiliary**.

| Approach | Time | Auxiliary space |
|---|---|---|
| **Hash map** | O(n) | **O(n)** |
| Interleaving | O(n) | **O(1)** |

The map version is much easier to write correctly and to explain. **Lead with it, then mention interleaving as the space optimization** — knowing it exists is usually worth as much as implementing it.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Copying `next` alone is easy, but `random` can point anywhere — forwards, backwards, or at itself — so in a single pass the target's copy might not exist yet. What I actually need is a way to ask 'given an original node, what's its copy?' at any moment, so I use a hash map keyed by the original node. Two passes: first create every copy and record the mapping, leaving pointers unset; then walk again and translate both pointers through the map. Separating creation from wiring removes the ordering problem entirely. I seed the map with `None → None` so null pointers and an empty list need no special cases. O(n) time, O(n) space — and there's an O(1)-space version that interleaves each copy after its original so a node's copy is just `next`."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Do it in O(1) extra space." | **The follow-up.** Weave copies in after their originals, set `copy.random = orig.random.next`, then unweave. Three passes, no map. |
| "Why two passes?" | A `random` pointer can target a node not yet copied. Creating everything first guarantees every lookup succeeds. |
| "Why does `{None: None}` help?" | It turns the null case into an ordinary lookup instead of a branch — including for the empty list. |
| "Can nodes really be dict keys?" | Yes — Python hashes objects by identity by default, which is what you want here since values may repeat. |
| "Recursive version?" | Recurse on `next` and `random` with a memo dict keyed by the original node. Same O(n)/O(n), plus O(n) stack. |
| "What if it were a general graph, not a list?" | Same technique — this *is* graph cloning. See [Clone Graph](133-clone-graph.md); the only change is DFS/BFS instead of a linear walk. |
| "Copy without a map, in one pass?" | Not reliably — forward `random` pointers force either a second pass or on-demand creation with memoization (which is a map again). |

**Traps:**

- **Shallow copying.** Assigning `copy.random = curr.random` points into the *original* list. The problem explicitly forbids it, and it's easy to do by reflex.
- **Copying `next` in pass 1** while creating nodes. Tempting, but it doesn't help — you still need pass 2 for `random`, and it complicates the loop.
- **No `None` handling.** `old_to_copy[curr.random]` raises `KeyError` on a null pointer without the seed.
- **Keying the map by `val`.** Values can repeat, so different nodes would collide. Key by the node object.
- **Creating a copy on demand** inside pass 2 without checking the map — you'd produce duplicate nodes for the same original.
- **Forgetting the empty-list case** if you skip the `None` seed.

**This same move shows up in:** [Clone Graph](133-clone-graph.md) (the identical original→copy map, on a graph) · [Two Sum](1-two-sum.md) (a hash map turning a quadratic search linear) · [Merge Two Sorted Lists](21-merge-two-sorted-lists.md) (relinking discipline) · [LRU Cache](146-lru-cache.md) (a map keyed to node objects).

</details>

---
