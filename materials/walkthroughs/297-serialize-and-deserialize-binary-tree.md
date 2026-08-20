# 297. Serialize and Deserialize Binary Tree

**Hard** · [LeetCode](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/)

[📖 08. Trees lesson](../learning/08-trees.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 08. Trees problems](../rmap-practice/08-trees.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

**Serialization** is converting a data structure into a sequence of bits so it can be stored or transmitted, and reconstructed later.

Design an algorithm to **serialize** a binary tree to a string and **deserialize** that string back into the identical tree. You may use any format you like — there's no restriction on the encoding.

```
        1              serialize    "1,2,N,N,3,4,N,N,5,N,N"
      /   \       →                          ↓
     2     3            deserialize   the identical tree
          / \
         4   5
```

**Constraints:** `0 <= nodes <= 10⁴` · `-1000 <= Node.val <= 1000`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**Design** … you may use any format" | You invent the protocol. Design **encode and decode together** — every encoder choice is a decoder obligation |
| "reconstructed **later**" | The string must be *self-describing*; the decoder gets nothing else |
| the **identical** tree | Structure **and** values must round-trip exactly |
| tree can be **empty** | `None` must survive the round trip |
| values can be **negative** | ⚠️ So `-` appears in the data. Your null marker and delimiter must not collide with it |

**The core difficulty is ambiguity**, and it's the same lesson as [Encode and Decode Strings](271-encode-and-decode-strings.md): a format must be unambiguous *by construction*.

Consider serializing a plain preorder traversal with no null markers:

```
        1              preorder:  1, 2, 3
      /   \
     2     3

        1              preorder:  1, 2, 3   ← IDENTICAL string,
      /                                        different tree!
     2
    /
   3
```

Two different trees, one string. **The shape information was lost**, because nothing records where a child was missing.

**The fix: write a marker for every absent child.** Then the string encodes shape as well as values:

```
tree 1:  1, 2, N, N, 3, N, N
tree 2:  1, 2, 3, N, N, N, N      ← now distinguishable ✅
```

That connects directly to [problem 105](105-construct-binary-tree-from-preorder-and-inorder-traversal.md), where preorder alone was insufficient and **inorder** supplied the missing boundaries. Here, **null markers** supply them instead — and they're cheaper, since you only need one traversal.

🤔 **Before you open the next section:** with null markers included, why can the decoder rebuild the tree by reading the sequence strictly left to right, never needing to look ahead?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Verdict |
|---|---|---|
| Preorder, **no** null markers | Just the values | ❌ **Ambiguous** — different trees produce the same string |
| Preorder + inorder | Two traversals, rebuild as in [105](105-construct-binary-tree-from-preorder-and-inorder-traversal.md) | ⚠️ Works, but needs **unique values** and two passes |
| BFS level-order with markers | Queue-based, like LeetCode's own display format | ✅ Also correct |
| **Preorder DFS + null markers** | One traversal, `"N"` for absent children | ✅ |

**The decision: preorder DFS with an explicit null marker for every missing child.**

**Why preorder specifically.** Preorder emits the **node before its children**, so when decoding you always have the parent before you need to attach anything to it. The decoder can build top-down in a single left-to-right pass, never looking ahead or backtracking.

*(Postorder works too, read in reverse. **Inorder alone does not** — the root isn't identifiable in the sequence.)*

**Why the markers make it unambiguous.** With a marker for every absent child, every node contributes exactly its value plus placeholders for both children. The sequence becomes a complete description of the tree's shape — decoding is then purely mechanical, with no ambiguity to resolve.

**The elegance of the decoder.** It mirrors the encoder exactly:

```
encode:  write value  →  encode left  →  encode right
decode:  read value   →  decode left  →  decode right
```

Same order, opposite direction. **That symmetry is the sign of a well-designed serialization format** — and it's why designing the two together matters.

**Why an iterator rather than an index.** `iter()` plus `next()` gives a shared cursor that advances automatically as nested calls consume values. With a plain index you'd need a mutable counter (`self.i`, or an index passed by reference) — the iterator handles the shared position for free.
→ [iterators-iterables](../syntax/iterators-iterables.md)

**Why `"N"` and `","` are safe here.** Values are integers in `[-1000, 1000]`, so they contain digits and `-`, but never `N` or `,`. If values were arbitrary strings, you'd need length prefixing — exactly the technique from [Encode and Decode Strings](271-encode-and-decode-strings.md).

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

**Serializing:**

```python
def serialize(self, root):
    values = []
```

Collect tokens in a list, joined at the end. Building a string with `+=` in a loop would be O(n²), since Python strings are immutable and each concatenation copies.
→ [class-basics](../syntax/class-basics.md) · [string-immutability](../syntax/string-immutability.md)

```python
    def dfs(node):
        if not node:
            values.append("N")
            return
```

**The null marker** — the line that makes the format unambiguous. An absent child still writes a token, so the shape is recorded rather than inferred.

Note it appends *and then returns*: a missing child has no children of its own to record.
→ [function-basics](../syntax/function-basics.md) · [closures](../syntax/closures.md) · [truthy-falsy-values](../syntax/truthy-falsy-values.md)

```python
        values.append(str(node.val))
        dfs(node.left)
        dfs(node.right)
```

**Preorder: node, then left, then right.** Writing the value first is what lets the decoder create the parent before its children.

`str()` because we're building a text format; the decoder will convert back with `int()`.
→ [type-conversion](../syntax/type-conversion.md) · [recursion-basics](../syntax/recursion-basics.md)

```python
    dfs(root)
    return ",".join(values)
```

One `join` — O(n), versus O(n²) for repeated concatenation.
→ [string-join-slice](../syntax/string-join-slice.md)

**Deserializing:**

```python
def deserialize(self, data):
    values = iter(data.split(","))
```

`.split(",")` recovers the token list; `iter()` wraps it in a **shared cursor**.

This is the key mechanism: every nested `dfs()` call pulls from the *same* iterator, so the position advances automatically as the tree is rebuilt — no index bookkeeping.
→ [string-methods](../syntax/string-methods.md) · [iterators-iterables](../syntax/iterators-iterables.md)

```python
    def dfs():
        val = next(values)
        if val == "N":
            return None
```

`next()` consumes exactly one token. A marker means "no node here" — return `None` and, crucially, **consume nothing further**, since a null has no children in the stream.
→ [comparison-operators](../syntax/comparison-operators.md) · [none-type](../syntax/none-type.md)

```python
        node = TreeNode(int(val))
        node.left = dfs()
        node.right = dfs()
        return node
```

**The mirror of the encoder.** Create the node, then recursively build its left subtree, then its right — the same order the encoder wrote them.

The recursion's structure *is* the parsing logic: because both sides agree on the order, the tokens line up automatically. **No delimiters between subtrees are needed** — the null markers already say where each subtree ends.
→ [type-conversion](../syntax/type-conversion.md) · [binary-tree](../data-structures/binary-tree.md)

```python
    return dfs()
```

<details>
<summary>The whole thing together</summary>

```python
class Codec:

    def serialize(self, root: Optional[TreeNode]) -> str:
        values = []

        def dfs(node):
            if not node:
                values.append("N")
                return
            values.append(str(node.val))
            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return ",".join(values)

    def deserialize(self, data: str) -> Optional[TreeNode]:
        values = iter(data.split(","))

        def dfs():
            val = next(values)
            if val == "N":
                return None
            node = TreeNode(int(val))
            node.left = dfs()
            node.right = dfs()
            return node

        return dfs()
```

</details>

**Trace serialization** — the example tree:

```
        1
      /   \
     2     3
          / \
         4   5
```

| Visit | Emits |
|---|---|
| 1 | `1` |
| 2 | `2` |
| 2's left (None) | `N` |
| 2's right (None) | `N` |
| 3 | `3` |
| 4 | `4`, `N`, `N` |
| 5 | `5`, `N`, `N` |

Result: **`"1,2,N,N,3,4,N,N,5,N,N"`**

**Trace deserialization** of that string:

| `next()` | Action |
|---|---|
| `1` | create node 1 → build its left |
| `2` | create node 2 → build its left |
| `N` | 2.left = None |
| `N` | 2.right = None; node 2 done, return to 1 |
| `3` | 1.right = node 3 → build its left |
| `4` | create node 4 |
| `N`, `N` | 4's children are None |
| `5` | 3.right = node 5 |
| `N`, `N` | 5's children are None |

The identical tree ✅

**And the empty tree:** serializes to `"N"`, deserializes to `None` — handled with no special case.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)** for both directions.

**Serialize:** each node emits one token, and each of the n+1 null positions emits one. That's 2n+1 tokens, each appended in O(1), then one `join` over them → **O(n)**.

**Deserialize:** `.split()` is O(n), and each `next()` plus node creation is O(1), performed 2n+1 times → **O(n)**.

**⚠️ The `+=` trap.** Building the string with `result += token` inside the loop would be **O(n²)**, because Python strings are immutable and each concatenation copies everything so far. `"".join()` over a list is the fix — same issue flagged in [Encode and Decode Strings](271-encode-and-decode-strings.md).

**Versus the preorder + inorder approach** ([105](105-construct-binary-tree-from-preorder-and-inorder-traversal.md)): that needs two traversals, requires **unique values**, and naively costs O(n²) to rebuild. The null-marker format is one traversal, works with duplicates, and rebuilds in O(n). **Strictly better for this purpose.**

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** for both.

- **The serialized string:** 2n+1 tokens → O(n). Required output.
- **The recursion stack:** O(h) — O(log n) balanced, **O(n)** skewed.
- **The token list / split result:** O(n).

**O(n)** overall, which is unavoidable: representing an n-node tree needs Ω(n) characters.

**The null-marker overhead is real but bounded.** A binary tree with n nodes has exactly **n+1** null child positions, so the format is roughly **2× the minimum**. You could compress it — e.g. a bitmask of which children exist — but the readability cost rarely pays off.

⚠️ At n = 10⁴, a skewed tree means 10⁴ recursion frames, past Python's default limit of 1000. An iterative decoder using an explicit stack avoids it, and BFS-based serialization sidesteps recursion entirely on both sides.
→ [recursion-limit](../syntax/recursion-limit.md)

**The BFS alternative** uses O(w) for the queue instead of O(h) for the stack — the usual trade, better on deep narrow trees, worse on wide ones.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The trap is ambiguity: a bare preorder traversal doesn't determine the tree, because two different shapes can produce the same value sequence. So I write an explicit marker for every absent child — then the string encodes shape as well as values. I use preorder because it emits the node before its children, which means the decoder can build top-down in one left-to-right pass, creating each parent before it needs to attach anything. The decoder mirrors the encoder exactly: read a value, build left, build right. I use an iterator over the tokens so nested calls share a cursor automatically. O(n) time and space both ways, and the empty tree round-trips as a single marker with no special case."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why are null markers necessary?" | **The question.** Without them, `[1,2,3]` as preorder matches multiple trees. Demo two. |
| "Why preorder rather than inorder?" | Preorder emits the node first, so the decoder always has the parent before the children. Inorder can't identify the root in the stream. |
| "What if values were arbitrary strings?" | `N` and `,` could appear in the data. Use length prefixing — see [Encode and Decode Strings](271-encode-and-decode-strings.md). |
| "Use BFS instead." | Level-order with markers, decoded with a queue. Also O(n), and it's the format LeetCode displays. |
| "Make it more compact." | Drop markers for leaves via a shape bitmask, or use postorder with a count. Rarely worth the complexity. |
| "Serialize a **BST** specifically?" | Preorder alone suffices — no markers needed, since the BST bounds tell you where each subtree ends. LeetCode 449. |
| "What about a 10⁴-deep tree?" | Recursion overflows; use an explicit stack or BFS. |

**Traps:**

- **Omitting null markers.** The defining bug — the format becomes ambiguous and the round trip silently produces a different tree.
- **Building the string with `+=`** → O(n²).
- **Using a marker or delimiter that can appear in the data.** Safe here (integers only), but not in general.
- **Reading right before left** in the decoder — it must mirror the encoder's order exactly.
- **Using an index variable without sharing it** across recursive calls. Each call would restart from the same position; use an iterator or a mutable counter.
- **Forgetting the empty tree.** Works here for free — but confirm it rather than assuming.

**This same move shows up in:** [Encode and Decode Strings](271-encode-and-decode-strings.md) (the same "make the format unambiguous by construction" lesson) · [Construct Binary Tree from Preorder and Inorder](105-construct-binary-tree-from-preorder-and-inorder-traversal.md) (rebuilding from traversals, using inorder instead of markers) · [tree-traversal-orders](../algorithms/tree-traversal-orders.md) · [Same Tree](100-same-tree.md) (why null markers matter when comparing).

</details>

---
