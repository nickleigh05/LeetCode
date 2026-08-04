# 23. Merge k Sorted Lists

**Hard** · [LeetCode](https://leetcode.com/problems/merge-k-sorted-lists/) · [Solution file (no hints)](../../problems/0001-0499/23.py)

[📖 06. Linked List lesson](../learning/06-linked-list.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 06. Linked List problems](../rmap-practice/06-linked-list.md)

---

You're given an array of `k` linked lists, each sorted in ascending order. **Merge them all into one sorted linked list** and return it.

```
lists = [[1,4,5], [1,3,4], [2,6]]  →  [1,1,2,3,4,4,5,6]
lists = []                         →  []
lists = [[]]                       →  []
```

**Constraints:** `0 <= k <= 10⁴` · `0 <= lists[i].length <= 500` · total nodes ≤ 10⁴ · each list sorted ascending

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**k** sorted lists" | The generalization of [Merge Two Sorted Lists](21-merge-two-sorted-lists.md), which handled k = 2 |
| each list **sorted** | The next node of the answer is always one of the k current heads — never anything deeper |
| `k` up to 10⁴ | ⚠️ Scanning all k heads for the minimum on every step is O(N·k). Too slow |
| `lists` can be **empty**, and contain **empty lists** | `[]` and `[[]]` must both return `None` |
| total nodes ≤ 10⁴ | O(N log k) is comfortable |

Start from what you know. With two lists you compared two heads and took the smaller. With k lists the same logic holds — **the smallest of the k current heads is always the next node overall**, since each list is sorted and nothing behind a head can be smaller than it.

So the algorithm is clear: *repeatedly take the minimum of the k heads.*

The only question is **how fast you can find that minimum**, and how cheaply you can maintain it after removing one element and revealing its successor.

- Scan all k heads each time → O(k) per node → **O(N·k)** total. At k = 10⁴, dead.
- You need the minimum in better than linear time, with cheap updates.

**That is exactly what a [min-heap](../data-structures/heap.md) is for**: O(1) to peek the minimum, O(log k) to remove it, O(log k) to insert the replacement.

🤔 **Before you open the next section:** the heap only ever needs to hold *one node per list* — never all N. Why is that enough?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Collect all values, sort, rebuild | Extract N values, sort, make new nodes | O(N log N) | **O(N)** | ⚠️ Works; discards sortedness and allocates |
| Merge one at a time | Merge list 1 with 2, result with 3, … | **O(N·k)** | O(1) | ❌ Early lists get re-traversed k times |
| Scan k heads each step | Linear search for the minimum | O(N·k) | O(1) | ❌ Same problem |
| **Min-heap of k heads** | Heap gives the minimum in O(log k) | **O(N log k)** | **O(k)** | ✅ |
| Divide and conquer | Merge lists pairwise in rounds | O(N log k) | O(log k) | ✅ Equally good |

**The decision: a [min-heap](../data-structures/heap.md) holding one node from each list.**

The loop:
1. Seed the heap with every list's head (skipping empty lists).
2. Pop the smallest node, append it to the result.
3. Push that node's `next` — its list's new head.
4. Repeat until the heap empties.

**Why the heap only holds k nodes.** At any moment you only need the *current front* of each list; everything behind a front is larger and can't be next. So the heap stays at size ≤ k, giving O(log k) operations rather than O(log N).

**⚠️ The tuple trick, and why it's mandatory.** You push `(value, list_index, node)` rather than the node alone. Python's `heapq` compares tuples element by element — so if two nodes have the **same value**, it falls through to comparing the second element. Without `list_index`, it would reach the third and try to compare two `ListNode` objects, which define no ordering:

```
TypeError: '<' not supported between instances of 'ListNode' and 'ListNode'
```

Since list indices are distinct integers, the comparison **always resolves at the second element** and never touches the nodes. This bites people constantly — the example `[[1,4,5],[1,3,4],[2,6]]` has duplicate 1s specifically to trigger it.

**Why not merge one at a time?** Merging sequentially re-traverses the accumulated result each round: list 1's nodes get walked k times. That's O(N·k). **Divide and conquer fixes it** by pairing lists so every node is touched only log k times — an equally valid O(N log k) answer worth naming.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
import heapq

min_heap = []
```

Python has no heap class — `heapq` provides functions that treat a **plain list** as a binary min-heap. An empty list is a valid empty heap.
→ [import-basics](../syntax/import-basics.md) · [heapq-module](../syntax/heapq-module.md) · [heap](../data-structures/heap.md)

```python
for list_index in range(len(lists)):
    head_node = lists[list_index]
    if head_node is not None:
        heapq.heappush(min_heap, (head_node.val, list_index, head_node))
```

**Seed the heap** with one node per list — each list's head.

`if head_node is not None` skips empty lists, which handles the `[[]]` and `[]` inputs with no extra guard.

The three-part tuple is the crux: **value** for ordering, **index** as a tie-breaker so nodes are never compared, **node** as the payload.
→ [for-loop](../syntax/for-loop.md) · [tuple-basics](../syntax/tuple-basics.md) · [identity-operators](../syntax/identity-operators.md)

```python
dummy_head = ListNode()
current_node = dummy_head
```

The [dummy head](21-merge-two-sorted-lists.md) again — a valid attachment point before the result has any nodes. Fourth appearance in this unit.

```python
while min_heap:
    smallest_val, list_index, smallest_node = heapq.heappop(min_heap)
```

`heappop` removes and returns the **smallest** tuple in O(log k). Unpacking gives all three components; `list_index` is needed to re-push the successor from the same list.

An empty list is falsy, so `while min_heap` means "while any list still has nodes".
→ [while-loop](../syntax/while-loop.md) · [tuple-unpacking](../syntax/tuple-unpacking.md) · [truthy-falsy-values](../syntax/truthy-falsy-values.md)

```python
    current_node.next = smallest_node
    current_node = current_node.next
```

Append the winning node to the result and advance the tail. Nodes are **relinked**, not copied.

```python
    next_node = smallest_node.next
    if next_node is not None:
        heapq.heappush(min_heap, (next_node.val, list_index, next_node))
```

**Refill from the same list.** Having consumed one node, push its successor so that list stays represented. If the list is exhausted, push nothing — the heap shrinks, and it empties exactly when every list does.

This is what keeps the heap at size ≤ k throughout.
→ [heapq-module](../syntax/heapq-module.md)

```python
current_node.next = None
```

**Terminate the result.** The last appended node still carries its original `next` from its source list — pointing at a node that may already have been placed elsewhere. Without this line you can produce a corrupted list or a cycle.

```python
return dummy_head.next
```

<details>
<summary>The whole thing together</summary>

```python
import heapq

class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:

        min_heap = []

        for list_index in range(len(lists)):
            head_node = lists[list_index]
            if head_node is not None:
                heapq.heappush(min_heap, (head_node.val, list_index, head_node))

        dummy_head = ListNode()
        current_node = dummy_head

        while min_heap:
            smallest_val, list_index, smallest_node = heapq.heappop(min_heap)

            current_node.next = smallest_node
            current_node = current_node.next

            next_node = smallest_node.next
            if next_node is not None:
                heapq.heappush(min_heap, (next_node.val, list_index, next_node))

        current_node.next = None

        return dummy_head.next
```

</details>

**Trace it** — `lists = [[1,4,5], [1,3,4], [2,6]]`:

Seed: heap holds `(1,0,·) (1,1,·) (2,2,·)`

| Pop | Value taken | Push next | Heap after (values) | Result |
|---|---|---|---|---|
| `(1,0)` | **1** | `(4,0)` | 1, 2, 4 | `1` |
| `(1,1)` | **1** | `(3,1)` | 2, 3, 4 | `1,1` |
| `(2,2)` | **2** | `(6,2)` | 3, 4, 6 | `1,1,2` |
| `(3,1)` | **3** | `(4,1)` | 4, 4, 6 | `1,1,2,3` |
| `(4,0)` | **4** | `(5,0)` | 4, 5, 6 | `1,1,2,3,4` |
| `(4,1)` | **4** | — (list 1 done) | 5, 6 | `…,4,4` |
| `(5,0)` | **5** | — | 6 | `…,5` |
| `(6,2)` | **6** | — | empty | `1,1,2,3,4,4,5,6` ✅ |

Rows 1–2 are exactly where the tie-breaker earns its place: two entries both with value 1, resolved by comparing `0 < 1` rather than attempting to compare two `ListNode`s.

Note the heap never exceeded **3** entries (= k), despite 8 nodes total.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(N log k)</summary>

**O(N log k)**, where N is the total number of nodes and k the number of lists.

| Step | Cost |
|---|---|
| Seed the heap | k pushes × O(log k) = O(k log k) |
| Per node: one pop + one push | O(log k) each |
| All N nodes | **O(N log k)** |

Since k ≤ N, the seeding is absorbed: **O(N log k)** overall.

**Why `log k` and not `log N`:** the heap holds at most one node per list, so it never exceeds k entries. Every node is pushed once and popped once, but each operation costs only log of the *heap size*.

**Versus the alternatives:**

| Approach | Time | At N=10⁴, k=10⁴ |
|---|---|---|
| Sequential merging | O(N·k) | 10⁸ |
| Collect + sort | O(N log N) | ~1.3·10⁵ |
| **Heap** | **O(N log k)** | ~1.3·10⁵ |

The heap and the sort look comparable here because k ≈ N. The heap wins decisively when **k is small and N is large** — say 10 lists of 10⁶ nodes: O(N log 10) versus O(N log N), a 6× difference. It also streams: it never needs all N values in memory at once.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(k)</summary>

**O(k)** auxiliary — the heap holds at most one node per list.

The result list is **not** additional space: nodes are relinked, not copied. So the honest phrasing is *"O(k) auxiliary; the output reuses the input nodes."*

| Approach | Auxiliary space |
|---|---|
| **Heap** | **O(k)** |
| Divide and conquer | O(log k) recursion, or O(1) iterative |
| Collect + sort | **O(N)** — an array *and* new nodes |

**Why O(k) and not O(N)** is the design win. A naive approach dumps every node into one structure; the heap holds only the k *frontiers*, because everything behind a frontier is provably not next. **Keeping only the candidates that could win** is the same discipline as the monotonic stack in [Daily Temperatures](739-daily-temperatures.md) — different structure, identical instinct.

This also makes the algorithm work on **streams**: you never need a list in memory, only its current head. That's precisely how external merge sort combines sorted runs from disk.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Each list is sorted, so the next node of the answer is always the smallest of the k current heads. The question is how fast I can find that minimum and refresh it. Scanning all k each time is O(N·k), which is too slow at k = 10⁴ — so I use a min-heap holding one node per list. Pop the smallest, append it, then push that node's successor so its list stays represented. The heap stays at size k, so each operation is O(log k) and the total is O(N log k), O(k) space. One detail: I push `(value, list_index, node)` tuples, because on equal values Python would otherwise fall through to comparing ListNode objects and raise a TypeError — the list index breaks the tie first."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why include the list index in the tuple?" | **The question.** Equal values make `heapq` compare the next element; without the index it reaches the nodes, which aren't comparable → `TypeError`. |
| "Solve it without a heap." | Divide and conquer: merge lists pairwise in rounds using [problem 21](21-merge-two-sorted-lists.md). O(N log k) time, O(1) auxiliary iteratively. |
| "Why not merge them one at a time?" | Early lists get re-traversed once per round → O(N·k). Pairwise merging touches each node only log k times. |
| "What if the lists were **arrays**?" | Same heap approach with `(value, array_index, position)`. This is the merge step of external sorting. |
| "What if k is enormous but each list is tiny?" | The heap is O(k) memory — that's the cost. Divide and conquer uses O(log k). |
| "Why `current_node.next = None` at the end?" | The last node still points into its source list. Without cutting it you can emit a corrupted list or a cycle. |
| "Can you avoid the heap entirely for k = 2?" | Yes — that's [Merge Two Sorted Lists](21-merge-two-sorted-lists.md), a straight two-pointer comparison. |

**Traps:**

- **Pushing bare nodes** into the heap → `TypeError` on the first duplicate value. The signature bug of this problem.
- **Forgetting `current_node.next = None`** — a dangling pointer into an already-consumed list.
- **Not skipping empty lists** when seeding — `head_node.val` on `None` raises `AttributeError`. Inputs `[]` and `[[]]` are explicitly in the constraints.
- **Pushing all N nodes up front.** It works but makes the heap O(N) and every operation O(log N) — pointlessly worse.
- **Losing the list index**, so you can't tell which list to refill from.
- **Merging sequentially** and calling it O(N log k). It's O(N·k).

**This same move shows up in:** [Merge Two Sorted Lists](21-merge-two-sorted-lists.md) (the k = 2 case, and the divide-and-conquer building block) · [K Closest Points to Origin](973-k-closest-points-to-origin.md) (a heap keeping only the candidates that matter) · [Find Median from Data Stream](295-find-median-from-data-stream.md) (heaps maintaining an aggregate under updates) · [merge-sort](../algorithms/merge-sort.md) (the k-way generalization of its merge step).

</details>
