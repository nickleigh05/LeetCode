# 105. Construct Binary Tree from Preorder and Inorder Traversal

**Medium** · [LeetCode](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/)

[📖 07. Trees lesson](../learning/07-trees.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 07. Trees problems](../rmap-practice/07-trees.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Given two integer arrays `preorder` and `inorder` — the preorder and inorder traversals of the same binary tree, with **unique** values — construct and return the tree.

```
preorder = [3,9,20,15,7]
inorder  = [9,3,15,20,7]

        3
      /   \
     9     20
          /  \
        15    7
```

**Constraints:** `1 <= n <= 3000` · all values **unique** · `inorder` is guaranteed to be a permutation of `preorder`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

First, recall what each traversal order actually emits:

| Order | Visits | So the first element is… |
|---|---|---|
| **Preorder** | **node**, left, right | ⚠️ **the root** |
| **Inorder** | left, **node**, right | the leftmost node |
| Postorder | left, right, node | (the *last* element is the root) |

| The statement says | Which really means |
|---|---|
| "**preorder** and **inorder**" | ⚠️ Preorder identifies roots; inorder splits left from right. Each supplies exactly what the other lacks |
| "values are **unique**" | ⚠️ Essential — you locate the root in `inorder` by value, which requires no duplicates |
| "construct the tree" | You're **building** nodes, not traversing existing ones |
| n up to 3000 | O(n²) = 9·10⁶ passes, but O(n) is achievable and is the real answer |

**The two facts that combine into a solution:**

1. **`preorder[0]` is the root.** By definition — preorder visits the node before anything else.
2. **Finding that value in `inorder` splits the tree.** Since inorder is *left, node, right*, everything **before** the root's position belongs to the left subtree and everything **after** belongs to the right.

```
preorder = [3, 9, 20, 15, 7]        root = 3
inorder  = [9, 3, 15, 20, 7]
            ↑  ↑  ─────────
          left root  right
```

So the left subtree has 1 node (`9`) and the right has 3 (`15, 20, 7`). Now split `preorder` by those **counts** — the next 1 element is the left subtree's preorder, the remaining 3 are the right's:

```
preorder:  [3] [9] [20, 15, 7]
             ↑   ↑      ↑
           root left  right
```

Recurse on each half. **Neither traversal alone is enough** — preorder gives roots but no boundaries, inorder gives boundaries but no roots. Together they determine the tree uniquely.

🤔 **Before you open the next section:** if you know the left subtree contains `m` nodes, which slice of `preorder` is that subtree's own preorder traversal?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| **Recursive, slicing both arrays** | Split at the root's inorder position | **O(n²)** | O(n²) | ✅ Correct and readable — the version to write first |
| Recursive + **hash map** of value→index, passing index ranges | No slicing, O(1) root lookup | **O(n)** | **O(n)** | ✅ The optimal answer |
| Iterative with a stack | Build while scanning preorder | O(n) | O(n) | ⚠️ Clever, hard to explain |

**The decision: recursion, splitting `preorder` and `inorder` at the root.**

Per call:
1. `preorder[0]` → create the root node.
2. Find that value's index `mid` in `inorder`.
3. **Left subtree:** `inorder[:mid]` (its nodes) and `preorder[1 : mid+1]` (the next `mid` preorder elements).
4. **Right subtree:** `inorder[mid+1:]` and `preorder[mid+1:]`.
5. Recurse on both, attach, return.

**The slice arithmetic is where mistakes happen**, so anchor it: `mid` is both the root's position in `inorder` **and** the number of nodes in the left subtree (everything before it). So in `preorder`, skipping the root at index 0, the left subtree occupies the next `mid` elements — indices `1` through `mid`, i.e. `preorder[1 : mid+1]`.

**Why unique values matter.** You locate the root by `inorder.index(preorder[0])`. With duplicates that lookup is ambiguous, and the tree isn't even uniquely determined. The constraint isn't decoration.

**Why the naive version is O(n²).** Two costs per call, each O(n): `.index()` scans the array, and each slice **copies** it. Across n nodes that's O(n²) time *and* space.

**The O(n) upgrade — worth stating even if you write the simple version:**
- Precompute `{value: index}` from `inorder` once → root lookup becomes **O(1)**.
- Pass **index ranges** instead of slices → no copying.
- Track a shared `preorder` pointer that advances as nodes are created.

That's O(n) time and O(n) space. **Write the slicing version, then say "I'd optimize with a hash map and index ranges" — that's the ideal interview arc.**

**Why preorder + postorder alone is ambiguous:** both tell you roots but neither splits left from right, so the tree isn't determined. Inorder is the one that provides the boundary — worth knowing for the follow-up.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
if not preorder or not inorder:
    return None
```

**Base case:** no values left means an empty subtree.

This is what terminates the recursion — a leaf's children receive empty slices and return `None`.
→ [truthy-falsy-values](../syntax/truthy-falsy-values.md) · [if-return](../syntax/if-return.md) · [none-type](../syntax/none-type.md)

```python
root = TreeNode(preorder[0])
```

**Preorder's first element is always the root** of the current subtree — the defining property of preorder, used directly.

Note we're **creating** a node here, not visiting one. This is the first tree problem in the unit that builds rather than reads.
→ [class-basics](../syntax/class-basics.md) · [binary-tree](../data-structures/binary-tree.md)

```python
mid = inorder.index(preorder[0])
```

**Locate the root in `inorder`.** This index does double duty:

- It's the **boundary** — everything before is the left subtree, everything after is the right.
- Its value is also the **size of the left subtree**, since exactly `mid` elements precede it.

That second reading is what makes the preorder slicing work. `.index()` is O(n) — the bottleneck the hash-map version removes.
→ [list-methods](../syntax/list-methods.md)

```python
root.left = self.buildTree(preorder[1:mid + 1], inorder[:mid])
```

**Build the left subtree.**

- `inorder[:mid]` — everything before the root, which is exactly the left subtree's inorder.
- `preorder[1:mid + 1]` — skip the root at index 0, then take `mid` elements. In preorder, the entire left subtree is emitted immediately after the root, so those `mid` values *are* its preorder.

⚠️ The `+ 1` is the classic off-by-one. Verify it on the example: `mid = 1`, so `preorder[1:2] = [9]` — one node ✅
→ [list-slicing](../syntax/list-slicing.md) · [recursion-basics](../syntax/recursion-basics.md)

```python
root.right = self.buildTree(preorder[mid + 1:], inorder[mid + 1:])
```

**Build the right subtree** — everything after the root in both arrays. Both use `mid + 1` to skip past the root itself.

```python
return root
```

Return the assembled subtree so the caller can attach it.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:

        if not preorder or not inorder:
            return None

        root = TreeNode(preorder[0])
        mid = inorder.index(preorder[0])

        root.left = self.buildTree(preorder[1:mid + 1], inorder[:mid])
        root.right = self.buildTree(preorder[mid + 1:], inorder[mid + 1:])

        return root
```

</details>

**Trace it** — `preorder = [3,9,20,15,7]`, `inorder = [9,3,15,20,7]`:

**Call 1** — root **3**, `mid = 1` (position of 3 in inorder)
- left: `preorder[1:2] = [9]`, `inorder[:1] = [9]`
- right: `preorder[2:] = [20,15,7]`, `inorder[2:] = [15,20,7]`

**Call 2** (left) — root **9**, `mid = 0`
- left: `preorder[1:1] = []` → `None`
- right: `preorder[1:] = []` → `None`
- → leaf node 9 ✅

**Call 3** (right) — `preorder = [20,15,7]`, `inorder = [15,20,7]` → root **20**, `mid = 1`
- left: `preorder[1:2] = [15]`, `inorder[:1] = [15]` → leaf 15
- right: `preorder[2:] = [7]`, `inorder[2:] = [7]` → leaf 7

Assembled:
```
        3
      /   \
     9     20
          /  \
        15    7
```
✅

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n²) as written, O(n) optimized</summary>

**O(n²)** for this version. Two O(n) operations per node:

| Per call | Cost |
|---|---|
| `inorder.index(...)` | O(n) — a linear scan |
| Four slices | O(n) — each copies its elements |

n nodes × O(n) = **O(n²)** → 9·10⁶ at n = 3000. It passes, but it's not the intended answer.

**⚠️ The worst case is a skewed tree.** A balanced tree gives the recurrence `T(n) = 2T(n/2) + O(n)` = O(n log n), but a fully skewed one gives `T(n) = T(n−1) + O(n)` = **O(n²)**.

**The O(n) version** removes both costs:

```python
index_map = {val: i for i, val in enumerate(inorder)}   # O(n) once
self.pre_idx = 0

def build(left, right):                  # index range in inorder
    if left > right: return None
    root_val = preorder[self.pre_idx]
    self.pre_idx += 1
    node = TreeNode(root_val)
    mid = index_map[root_val]            # O(1) lookup
    node.left = build(left, mid - 1)     # left FIRST — matches preorder order
    node.right = build(mid + 1, right)
    return node
```

- The hash map makes the root lookup **O(1)**.
- Passing index ranges means **no copying**.
- The shared `pre_idx` advances in preorder sequence, so no preorder slicing is needed at all.

**O(n) time.** Note `build(left, ...)` must be called **before** `build(mid+1, ...)` — preorder emits the entire left subtree first, so the pointer has to consume it in that order.
→ [dict-comprehension](../syntax/dict-comprehension.md) · [enumerate](../syntax/enumerate.md)

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n²) as written, O(n) optimized</summary>

**O(n²)** for the slicing version, **O(n)** optimized — plus O(n) for the tree itself in both cases.

**Where the O(n²) comes from:** each call creates four new lists totalling O(n) elements, and up to h calls are live simultaneously. On a skewed tree that's n levels × O(n) per level = **O(n²)** of slice copies alive at once.

Easy to miss, because slicing *looks* free in Python.

| Version | Time | Auxiliary space |
|---|---|---|
| Slicing | O(n²) | **O(n²)** |
| **Hash map + index ranges** | **O(n)** | **O(n)** |

The optimized version's O(n) is the hash map plus O(h) recursion — no copies at all, since ranges are just two integers per frame.

**The output tree is O(n)** in both, and is required, not overhead.

**The general lesson:** *slicing in a recursive function silently multiplies your space by the recursion depth.* Passing indices into the original array is nearly always the better move — the same instinct as the virtual index in [Search a 2D Matrix](74-search-a-2d-matrix.md).

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The two traversals supply complementary information. Preorder visits the node first, so `preorder[0]` is always the root of the current subtree. Inorder visits left-node-right, so finding that root's position in inorder splits the remaining values into left and right subtrees. That position is also the *size* of the left subtree, which tells me how many of the following preorder elements belong to it. Then I recurse on both halves. Written with slicing it's O(n²), because `.index()` and the copies are each O(n) per node. I'd optimize by precomputing a value-to-index hash map for O(1) root lookup and passing index ranges instead of slices — that's O(n) time and space. Unique values matter, since I locate the root by value."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Make it O(n)." | **The key follow-up.** Hash map for the root lookup, index ranges instead of slices, and a shared preorder pointer. |
| "Build from **inorder + postorder**?" | Postorder's *last* element is the root. Same idea, consuming postorder from the right and building the **right** subtree first. LeetCode 106. |
| "Preorder + **postorder**?" | ⚠️ **Ambiguous** in general — neither splits left from right, so multiple trees fit. Only unique if every node has 0 or 2 children. LeetCode 889. |
| "What if values weren't unique?" | The root's position in inorder becomes ambiguous, and the tree isn't uniquely determined. You'd need node identity, not values. |
| "Why is the worst case O(n²)?" | A skewed tree gives `T(n) = T(n−1) + O(n)`. Balanced would be O(n log n). |
| "Iterative solution?" | Scan preorder with a stack, using inorder to decide when to pop and attach as a right child. O(n), but much harder to explain. |
| "Verify your tree is right?" | Traverse it in preorder and inorder and compare against the inputs. |

**Traps:**

- **`preorder[1:mid]`** instead of `preorder[1:mid + 1]`. The single most common bug — the left subtree has `mid` nodes, and slicing is end-exclusive.
- **Slicing `preorder` by position rather than by count.** The split point in preorder comes from the left subtree's *size*, which inorder supplies.
- **Assuming `preorder` and `inorder` split at the same index.** They don't — `mid` is an inorder index; preorder is split by counts.
- **Forgetting the base case** — infinite recursion on empty slices.
- **Building the right subtree first** in the optimized version. The shared preorder pointer must consume the left subtree first.
- **Not mentioning the O(n) optimization.** The slicing version is fine to write, but stopping there leaves the follow-up unanswered.

**This same move shows up in:** [tree-traversal-orders](../algorithms/tree-traversal-orders.md) (what each order emits, and why) · [Serialize and Deserialize Binary Tree](297-serialize-and-deserialize-binary-tree.md) (reconstructing a tree from a linear encoding) · [Kth Smallest Element in a BST](230-kth-smallest-element-in-a-bst.md) (inorder's ordering property) · [Search a 2D Matrix](74-search-a-2d-matrix.md) (indices instead of copies).

</details>
