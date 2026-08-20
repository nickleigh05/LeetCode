# 208. Implement Trie (Prefix Tree)

**Medium** · [LeetCode](https://leetcode.com/problems/implement-trie-prefix-tree/) · [Solution file (no hints)](../../problems/0001-0499/208.py)

[📖 09. Tries lesson](../learning/09-tries.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 09. Tries problems](../rmap-practice/09-tries.md)

---

A **trie** (pronounced "try", from re*trie*val) is a tree used to store and retrieve strings efficiently by prefix. Implement it with three operations:

- **`insert(word)`** — insert a word into the trie
- **`search(word)`** — return `true` if the **exact word** was inserted
- **`startsWith(prefix)`** — return `true` if any inserted word begins with `prefix`

```
insert("apple")
search("apple")     →  true
search("app")       →  false     ← "app" is a prefix, not an inserted word
startsWith("app")   →  true
insert("app")
search("app")       →  true      ← now it is
```

**Constraints:** `1 <= word.length <= 2000` · lowercase English letters only · up to 3·10⁴ calls

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**prefix** tree" | ⚠️ The structure is built *around* prefixes — words sharing a prefix share a path |
| `search` vs `startsWith` | ⚠️ **The key distinction.** One asks "was this word inserted?", the other "does any word start this way?" — same walk, different final test |
| lowercase letters only | 26 possible children per node |
| up to 3·10⁴ calls | Each operation should be **O(word length)**, independent of how many words are stored |

**Why not just use a hash set of words?** For `search` a set is perfect — O(1). But `startsWith` would need scanning **every** stored word, O(n·L). The trie exists to make prefix queries as cheap as exact ones.

**The structure.** Each node represents a *position* in a string, and its edges are labelled with characters. A word is a **path** from the root:

```
insert "app", "apple", "bat":

        root
        /   \
      a       b
      |       |
      p       a
      |       |
      p*      t*         * = is_end, a word finishes here
      |
      l
      |
      e*
```

Two ideas do all the work:

1. **Shared prefixes share nodes.** `"app"` and `"apple"` overlap for three characters, so those nodes are stored once. That's the space win *and* the reason prefix queries are fast.
2. **`is_end` marks where words terminate.** Without it you couldn't tell that `"app"` was inserted but `"appl"` wasn't — both are valid paths.

That flag is precisely the difference between the two queries: **`search` requires the path to exist *and* `is_end` to be true; `startsWith` requires only the path.**

🤔 **Before you open the next section:** both `search` and `startsWith` walk the same path down the tree. What single line distinguishes them at the end?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | `insert` | `search` | `startsWith` | Verdict |
|---|---|---|---|---|
| Hash set of words | O(L) | **O(1)** | **O(n·L)** — scan everything | ❌ Prefix queries are the whole point |
| Sorted list + binary search | O(n) insert | O(L log n) | O(L log n) | ⚠️ Works; insertion is expensive |
| **Trie** | **O(L)** | **O(L)** | **O(L)** | ✅ |

**The decision: a [trie](../data-structures/trie.md) where each node holds a dict of children plus an end-of-word flag.**

Every operation walks one character at a time, so all three cost **O(L)** — completely independent of how many words are stored. Storing a million words doesn't slow down a five-character lookup.

**Why a dict for children rather than a 26-slot array.** Both are valid:

| | Dict | 26-array |
|---|---|---|
| Lookup | O(1) hash | O(1) index |
| Memory | only existing children | **26 slots always**, mostly empty |
| Alphabet | any characters | lowercase only |

The dict wins on sparsity — most nodes have few children, and an array wastes 26 pointers each. It also generalizes beyond lowercase letters for free. Mention the array version as the constant-factor optimization when the alphabet is small and dense.
→ [dict-basics](../syntax/dict-basics.md)

**The design detail worth noticing:** this implementation makes `Trie` *itself* the node type — `self` is the root, and children are more `Trie` objects. That's compact and works because a trie node and a trie are structurally identical (any node is the root of a sub-trie). The alternative, a separate `TrieNode` class with `Trie` holding a `root`, is used in [problem 211](211-design-add-and-search-words-data-structure.md) and is arguably clearer. Both are fine; know that they're the same idea.

**The `find` helper is the real design win.** `search` and `startsWith` differ only in their final test, so factoring the shared walk into one method removes duplication and makes the distinction a single line.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
def __init__(self):
    self.children = {}
    self.is_end = False
```

A node holds two things: a map from **character → child node**, and a flag saying whether a word *ends* here.

The root is an empty node representing the empty prefix — it stores no character itself. Characters live on the **edges** (as dict keys), not in the nodes.
→ [class-basics](../syntax/class-basics.md) · [init-method](../syntax/init-method.md) · [trie](../data-structures/trie.md)

```python
def insert(self, word: str) -> None:
    node = self
    for char in word:
        if char not in node.children:
            node.children[char] = Trie()
        node = node.children[char]
    node.is_end = True
```

Walk the word one character at a time, **creating nodes only where the path doesn't already exist**. That's the prefix sharing: inserting `"apple"` after `"app"` reuses the first three nodes and adds only two.

`node = node.children[char]` descends whether the child was just created or already existed — no branching needed.

The final `is_end = True` is what makes this word *findable* by `search` rather than merely being a prefix.
→ [for-loop](../syntax/for-loop.md) · [membership-operators](../syntax/membership-operators.md) · [dict-basics](../syntax/dict-basics.md)

```python
def find(self, s: str):
    node = self
    for char in s:
        if char not in node.children:
            return None
        node = node.children[char]
    return node
```

**The shared walk.** Follow the path; if any character is missing, the prefix isn't present at all → `None`.

Returning the **node** rather than a boolean is the key design choice — it lets both public methods reuse this and then apply their own final test.
→ [none-type](../syntax/none-type.md) · [if-return](../syntax/if-return.md)

```python
def search(self, word: str) -> bool:
    node = self.find(word)
    return node is not None and node.is_end
```

**Two conditions.** The path must exist, **and** a word must actually terminate there.

That `and node.is_end` is the entire difference between the two queries. Without it, `search("app")` would return `True` before `"app"` was ever inserted, just because `"apple"` created the path.

`and` short-circuits, so `node.is_end` is never evaluated on `None`.
→ [identity-operators](../syntax/identity-operators.md) · [logical-operators](../syntax/logical-operators.md)

```python
def startsWith(self, prefix: str) -> bool:
    return self.find(prefix) is not None
```

**One condition.** The path existing is sufficient — some word passes through here, which is exactly what "starts with" means. No `is_end` check.

<details>
<summary>The whole thing together</summary>

```python
class Trie:

    def __init__(self):
        self.children = {}
        self.is_end = False

    def insert(self, word: str) -> None:
        node = self
        for char in word:
            if char not in node.children:
                node.children[char] = Trie()
            node = node.children[char]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self.find(word)
        return node is not None and node.is_end

    def startsWith(self, prefix: str) -> bool:
        return self.find(prefix) is not None

    def find(self, s: str):
        node = self
        for char in s:
            if char not in node.children:
                return None
            node = node.children[char]
        return node
```

</details>

**Trace it** — the example sequence:

**`insert("apple")`** — creates 5 nodes; `is_end` set on the final `e`:

```
root → a → p → p → l → e*
```

**`search("apple")`** — path exists, final node has `is_end` ✅ → **`True`**

**`search("app")`** — path exists (the second `p`), but that node's `is_end` is **False** → **`False`** ✅

**`startsWith("app")`** — path exists, no flag check → **`True`** ✅

**`insert("app")`** — the path already exists, so **no new nodes**; it just sets `is_end` on the second `p`:

```
root → a → p → p* → l → e*
```

**`search("app")`** — now `is_end` is True → **`True`** ✅

That last insert is the clearest illustration of the design: it allocated nothing and changed a single boolean.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(L) per operation</summary>

**O(L)** for all three operations, where L is the length of the word or prefix.

| Operation | Work |
|---|---|
| `insert` | L steps, each an O(1) dict lookup and possibly one node creation |
| `search` | L steps + one flag check |
| `startsWith` | L steps |

**The crucial property: the cost is independent of how many words are stored.** Whether the trie holds 10 words or 10 million, looking up a 5-character prefix takes 5 steps. That's what makes tries the right structure for autocomplete and dictionary lookups.

**Versus a hash set:** `search` would be O(1) — faster — but `startsWith` would be **O(n·L)**, scanning every stored word. The trie trades a small constant on exact search for a dramatic win on prefix search.

**Versus a sorted list:** `startsWith` via binary search is O(L log n) — decent, but insertion becomes O(n) because the list must stay sorted.

**Note dict lookups are O(1) average, not worst case** — the usual hashing asterisk, though with single characters as keys collisions are effectively a non-issue.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(total characters)</summary>

**O(total characters inserted)**, in the worst case — but typically much less, because prefixes are shared.

- **Worst case:** no two words share a prefix, so every word contributes L nodes → O(n·L).
- **Best case:** heavy sharing. Inserting `"a"`, `"ab"`, `"abc"`, `"abcd"` creates just **4** nodes total, not 1+2+3+4 = 10.

**Prefix sharing is the space win**, and it's exactly what makes prefix queries fast — the same structure serves both purposes.

**Per node:** a dict with up to 26 entries plus a boolean. Python dicts have real overhead (~64+ bytes even when small), which is why the **26-slot array** variant is worth knowing:

| | Space per node | Best for |
|---|---|---|
| Dict | proportional to actual children | sparse tries, large alphabets |
| 26-array | 26 pointers always | dense tries, small fixed alphabet |

**A practical note:** for storing a large static word list, a trie can actually use *more* memory than a plain hash set, because of per-node overhead. You pay that for the prefix operations. If you never need prefixes, use a set — **choose the structure by the queries you need to answer**, which is the real lesson of this problem.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "A hash set handles exact search in O(1), but `startsWith` would have to scan every stored word. A trie makes prefix queries as cheap as exact ones: each node maps a character to a child, so a word is a path from the root, and words sharing a prefix share nodes. Insert walks the word creating missing nodes, then sets an `is_end` flag on the last one. That flag is the whole distinction between the two queries — `search` needs the path to exist *and* `is_end` to be true, while `startsWith` only needs the path. I factor the shared walk into one helper that returns the final node or `None`, so both queries reuse it. All three operations are O(L), independent of how many words are stored."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why do you need `is_end`?" | **The question.** Without it you can't distinguish an inserted word from a mere prefix — `search("app")` would wrongly return `True` after inserting only `"apple"`. |
| "Dict or a 26-element array?" | Dict for sparse tries and arbitrary alphabets; array for a small dense alphabet, saving hashing overhead at the cost of 26 slots per node. |
| "Implement **delete**." | Walk to the word's end, clear `is_end`, then prune upward while a node has no children *and* isn't itself a word end. |
| "Return **all** words with a given prefix." | `find(prefix)`, then DFS the subtree collecting every node with `is_end`. That's autocomplete. |
| "Count words with a prefix." | Store a counter per node, incremented on each insert passing through — O(L) instead of a subtree walk. |
| "Why not just use a hash set?" | Fine if you only need exact lookups. The trie exists for prefix queries. |
| "Where are tries used for real?" | Autocomplete, spell-checkers, IP routing tables, and [Word Search II](212-word-search-ii.md) — where a trie prunes a search over a grid. |

**Traps:**

- **Forgetting `is_end`**, or checking it in `startsWith`. That inverts both queries' semantics.
- **Storing the character *in* the node** rather than as the dict key. It works, but it duplicates information and complicates lookups.
- **Creating a new node unconditionally** in `insert`, overwriting an existing child and orphaning every word beneath it.
- **Returning a boolean from the shared walk** instead of the node — then `search` can't check `is_end` and the helper isn't reusable.
- **Not short-circuiting** in `search` — `None.is_end` raises `AttributeError`.
- **Assuming a trie is always more compact than a set.** Per-node overhead is real; you're buying prefix queries.

**This same move shows up in:** [Design Add and Search Words](211-design-add-and-search-words-data-structure.md) (this trie, with wildcard matching) · [Word Search II](212-word-search-ii.md) (a trie used to prune a grid search) · [trie](../data-structures/trie.md) (the reference page) · [Encode and Decode Strings](271-encode-and-decode-strings.md) (another design problem where the API contract is the work).

</details>

---
