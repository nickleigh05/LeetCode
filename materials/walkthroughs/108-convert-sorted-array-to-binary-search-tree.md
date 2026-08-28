# 108. Convert Sorted Array to Binary Search Tree

**Easy** · [LeetCode](https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/) · [Solution file (no hints)](../../problems/0001-0499/108.py)

[📖 07. Trees lesson](../learning/07-trees.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 07. Trees problems](../rmap-practice/07-trees.md)

---

Given an integer array `nums` sorted in **ascending** order, convert it to a **height-balanced** binary search tree. Height-balanced means the depths of the two subtrees of every node differ by at most one.

```
nums = [-10,-3,0,5,9]  →  [0,-3,9,-10,null,5]   (or any valid balanced BST)
nums = [1,3]           →  [3,1]  or  [1,null,3]
```

**Constraints:** `1 <= nums.length <= 10⁴` · `-10⁴ <= nums[i] <= 10⁴` · `nums` is sorted **strictly increasing**

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| input is **sorted ascending** | ⚠️ That's exactly a BST's **inorder** traversal — so the array already encodes the answer's ordering |
| "**height-balanced**" | Subtree depths differ by ≤ 1 at every node — so you can't just chain nodes |
| "**a** height-balanced BST" | ⚠️ Not unique. Multiple valid answers exist, and any is accepted |
| strictly increasing | No duplicates to place |
| `n` up to 10⁴ | Recursion depth is `log n` ≈ 14 for a balanced tree — perfectly safe |

**The two properties you must satisfy simultaneously:**

1. **BST ordering** — everything in the left subtree is smaller than the node, everything right is larger.
2. **Balance** — the two subtrees of every node have nearly equal height.

The sorted array hands you the first for free (its order *is* the inorder traversal), so the question becomes: **how do you also get balance?**

**The insight:** balance means each node splits its remaining elements roughly in half. In a sorted array, the element that splits it in half is the **middle** one.

```
[-10, -3, 0, 5, 9]
           ↑ middle → root

left half  [-10, -3]        right half  [5, 9]
              ↑ middle                     ↑ middle
```

So: **pick the middle as the root, recurse on the left half for the left subtree, the right half for the right subtree.** Both properties fall out at once — the middle is greater than everything left and less than everything right (BST ✅), and the halves differ in size by at most one (balance ✅).

This is structurally the same divide-and-conquer as [binary search](../algorithms/binary-search.md) — and that's not a coincidence. Searching this tree *is* binary search made physical.

🤔 **Before you open the next section:** if you always take the middle element as the root, how much can the left and right subtree sizes differ — and why does that guarantee balance?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Insert each value into a BST | Repeated BST insertion | O(n²) | O(n) | ❌ Sorted input degenerates into a chain — the worst possible shape |
| Build any BST, then rebalance | Construct, then rotate | O(n log n) | O(n) | ❌ Vastly over-complicated |
| **Recursive middle-as-root** | Divide the range in half | **O(n)** | **O(log n)** | ✅ |
| Iterative with an explicit stack | Same idea, manual stack | O(n) | O(log n) | ⚠️ Correct, no benefit here |

**The decision: recursive divide-and-conquer, taking the middle of each range as that subtree's root.**

**Why inserting sequentially is catastrophic.** Inserting `[-10,-3,0,5,9]` one at a time into an empty BST gives:

```
-10
   \
    -3
      \
        0
          \
            5
              \
                9
```

A linked list — height `n` instead of `log n`, and O(n²) to build. **Sorted input is the pathological case for naive BST insertion**, which is precisely why balanced structures (AVL, red-black) exist. Worth naming, because it explains why this problem is posed at all.

**Why passing indices beats slicing.** You could write `build(nums[:mid])` and `build(nums[mid+1:])`, which is shorter — but every slice **copies** its portion of the array, giving O(n log n) time and O(n log n) total allocation. Passing `left`/`right` **indices** into the original array keeps it O(n) time and O(1) auxiliary space beyond the recursion.

That's a genuinely important habit: **recursion over ranges, not over copies.**

**Why the answer isn't unique.** With an even number of elements there are two candidate middles. `(left + right) // 2` picks the lower; `(left + right + 1) // 2` picks the upper. Both produce valid height-balanced BSTs — LeetCode accepts either. Mention this rather than worrying that your output doesn't match the sample exactly.

**Why the base case is `left > right`, not `left >= right`.** When `left == right` the range holds exactly **one** element, which must become a leaf. Using `>=` would discard it and lose values.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
    def build(left, right):
```

**An inner helper taking index bounds.** The public signature only gives the array, but the recursion needs a *range* — the same "write a helper with the arguments the recursion needs" move as in [Symmetric Tree](101-symmetric-tree.md).

Using indices rather than sub-arrays is what keeps this O(n).
→ [function-basics](../syntax/function-basics.md) · [closures](../syntax/closures.md)

```python
        if left > right:
            return None
```

**Base case: an empty range.**

`>` not `>=` — when `left == right` there's still one element to place. This is also what terminates the recursion at the leaves, and it returns `None`, which correctly becomes an absent child.
→ [comparison-operators](../syntax/comparison-operators.md) · [none-type](../syntax/none-type.md)

```python
        mid = (left + right) // 2
```

**The middle element becomes this subtree's root.**

Floor division picks the lower middle for even-sized ranges. `(left + right + 1) // 2` would pick the upper and produce an equally valid — but differently shaped — tree.

This single choice is what delivers balance: the two resulting halves differ in size by at most one.
→ [integer-division-modulo](../syntax/integer-division-modulo.md)

```python
        node = TreeNode(nums[mid])
```

Create the node from the middle value.
→ [class-basics](../syntax/class-basics.md)

```python
        node.left = build(left, mid - 1)
        node.right = build(mid + 1, right)
```

**Recurse on the two halves.**

- `[left, mid-1]` — all values **less** than `nums[mid]` → left subtree ✅ BST property
- `[mid+1, right]` — all values **greater** → right subtree ✅

Excluding `mid` from both is essential; including it would duplicate the value and recurse forever.
→ [recursion-basics](../syntax/recursion-basics.md)

```python
        return node

    return build(0, len(nums) - 1)
```

Kick off with the full range. `len(nums) - 1` because `right` is an **inclusive** bound — matching the `left > right` base case.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:

        def build(left, right):
            if left > right:
                return None

            mid = (left + right) // 2
            node = TreeNode(nums[mid])
            node.left = build(left, mid - 1)
            node.right = build(mid + 1, right)
            return node

        return build(0, len(nums) - 1)
```

</details>

**Trace it** — `nums = [-10, -3, 0, 5, 9]`, indices 0–4:

| Call | Range | `mid` | Value | Left range | Right range |
|---|---|---|---|---|---|
| 1 | `[0,4]` | 2 | **0** | `[0,1]` | `[3,4]` |
| 2 | `[0,1]` | 0 | **−10** | `[0,-1]` → `None` | `[1,1]` |
| 3 | `[1,1]` | 1 | **−3** | `[1,0]` → `None` | `[2,1]` → `None` |
| 4 | `[3,4]` | 3 | **5** | `[3,2]` → `None` | `[4,4]` |
| 5 | `[4,4]` | 4 | **9** | `None` | `None` |

Resulting tree:

```
         0
       /   \
    -10     5
       \      \
       -3      9
```

**Verify both properties:**

- **BST** — inorder traversal gives `-10, -3, 0, 5, 9` ✅ (the original sorted array)
- **Balanced** — every node's subtree heights differ by at most 1 ✅ (height 3 for 5 nodes; `⌈log₂6⌉ = 3`)

Calls 2 and 4 show the `left > right` base case doing its job: `build(0, -1)` and `build(3, 2)` both return `None`, becoming absent children rather than errors.

Note this differs from LeetCode's sample output `[0,-3,9,-10,null,5]` — that's the *upper*-middle choice. Both are accepted.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

Each array element is used to create **exactly one node**, and each `build` call does O(1) work beyond its recursive calls — one comparison, one arithmetic operation, one allocation.

With `n` nodes created, that's **O(n)** total.

**Why it's not O(n log n).** The recursion tree has depth `log n`, which tempts an `n log n` estimate — but the work at each *level* sums to O(number of nodes at that level), and across all levels each element is touched once. It's the "each element processed exactly once, just organized recursively" pattern.

**The slicing version *is* O(n log n)**, because `nums[:mid]` copies `mid` elements at every call, and those copies sum to O(n) per level × `log n` levels. Passing indices is what preserves linearity — a concrete reason to prefer it beyond style.

**Compare to sequential insertion:** O(n²) on sorted input, since each insert walks the ever-lengthening chain.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(log n)</summary>

**O(log n) auxiliary** — the recursion stack, whose depth equals the tree's height.

Because the tree is balanced by construction, the height is `⌈log₂(n+1)⌉` — about **14** at `n = 10⁴`. No recursion-limit concerns.

**The output tree is O(n)**, but that's the required result, not overhead.

| | Auxiliary space |
|---|---|
| Index-based recursion | **O(log n)** ✅ |
| Slice-based recursion | O(n log n) — copies at every level |
| Sequential insertion | O(n) stack on the degenerate chain |

**Why balance guarantees the log depth.** Each call halves its range, so the depth satisfies `T(n) = T(n/2) + 1`, giving `log n`. That's the same recurrence as [binary search](../algorithms/binary-search.md) — and searching the resulting tree performs exactly the comparisons binary search would make on the original array.

That equivalence is the satisfying part:

> **A balanced BST is binary search made into a data structure.** This problem builds one from the other.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "A sorted array is already a BST's inorder traversal, so ordering is free — the question is how to also get balance. Balance means each node splits its remaining elements roughly evenly, and in a sorted array the element that does that is the middle one. So I take the middle as the root, recurse on the left half for the left subtree and the right half for the right subtree. Both properties hold automatically: the middle is greater than everything to its left and less than everything to its right, and the halves differ in size by at most one. I pass **indices** rather than slices — slicing would copy at every level and make it O(n log n) time and space, whereas indices keep it O(n) time with O(log n) stack. The answer isn't unique; picking the upper middle gives a different but equally valid tree."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why not just insert each element?" | Sorted input degenerates a naive BST into a linked list — O(n²) to build, height `n`. This is the classic motivation for self-balancing trees. |
| "Why pass indices instead of slices?" | Slicing copies at every level: O(n log n) time and space. Indices keep it O(n)/O(log n). |
| "Is the answer unique?" | No. `(left+right)//2` and `(left+right+1)//2` both give valid balanced BSTs. |
| "Convert a **sorted linked list** instead?" | [LeetCode 109](https://leetcode.com/problems/convert-sorted-list-to-binary-search-tree/) — no random access, so use fast/slow pointers to find the middle (O(n log n)), or do an inorder simulation in O(n). |
| "Why is `left > right` the base case?" | `left == right` still holds one element that must become a leaf. `>=` would drop values. |
| "How tall is the result?" | `⌈log₂(n+1)⌉` — minimal for `n` nodes. |
| "Verify it's actually a BST?" | Inorder-traverse it and check the output equals the input array — see [Validate BST](98-validate-binary-search-tree.md). |

**Traps:**

- **`left >= right` as the base case.** Discards single-element ranges, silently losing values.
- **Slicing the array.** Correct output, but O(n log n) time and space.
- **Including `mid` in a recursive range.** Duplicates the value and recurses forever.
- **Passing `len(nums)` as the initial `right`.** The bound is inclusive, so it must be `len(nums) - 1`.
- **Inserting sequentially.** Produces a degenerate chain — exactly what the problem is designed to avoid.
- **Worrying that your tree differs from the sample.** Any height-balanced BST is accepted.

**This same move shows up in:** [Binary Search](704-binary-search.md) (the same halving recurrence — this problem materializes it as a tree) · [Construct Binary Tree from Preorder and Inorder](105-construct-binary-tree-from-preorder-and-inorder-traversal.md) (building a tree from traversal data with index ranges) · [Validate Binary Search Tree](98-validate-binary-search-tree.md) (checking the property this constructs) · [Balanced Binary Tree](110-balanced-binary-tree.md) (verifying the balance guaranteed here).

</details>

---
