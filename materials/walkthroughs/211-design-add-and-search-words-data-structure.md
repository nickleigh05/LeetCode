# 211. Design Add and Search Words Data Structure

**Medium** · [LeetCode](https://leetcode.com/problems/design-add-and-search-words-data-structure/)

[📖 08. Tries lesson](../learning/08-tries.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 08. Tries problems](../rmap-practice/08-tries.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Design a data structure that supports adding new words and searching for whether a string matches any previously added word.

- **`addWord(word)`** — add a word to the structure
- **`search(word)`** — return `true` if any added word matches. The search string may contain **`.`**, which matches **any single character**

```
addWord("bad"); addWord("dad"); addWord("mad")
search("pad")   →  false
search("bad")   →  true
search(".ad")   →  true      (matches bad, dad, mad)
search("b..")   →  true      (matches bad)
```

**Constraints:** `1 <= word.length <= 25` · `addWord` uses lowercase letters only · `search` may use lowercase letters and `.` · **at most 2 dots** per search · up to 10⁴ calls

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| add + search words | [Problem 208](208-implement-trie-prefix-tree.md)'s trie, unchanged for `addWord` |
| "**`.` matches any character**" | ⚠️ The entire new difficulty. At a dot you can't follow *one* path — you must try **all** children |
| "at most **2 dots**" | ⚠️ A deliberate constraint bounding the branching. Without it, `"....."` would explode |
| `search` is exact-length | A dot matches exactly one character, never zero or many — so lengths must agree |
| word length ≤ 25 | Short words; recursion depth is trivially safe |

**Everything except `search` is unchanged.** `addWord` is exactly [208](208-implement-trie-prefix-tree.md)'s `insert`.

**Why the wildcard breaks the simple walk.** Without dots, matching is deterministic: at each character you follow exactly one child, or fail. It's a **walk** — no decisions.

A dot removes that determinism:

```
        root
        /  |  \
       b   d   m
       |   |   |
       a   a   a
       |   |   |
       d*  d*  d*

search(".ad")  →  at the dot, ANY of b/d/m could be right
```

You can't know which branch leads to a match without trying. So the walk becomes a **search over a tree of possibilities** — and "try each option, succeed if any works" is depth-first search with backtracking.

**The structural shift is the lesson:**

| | Traversal | Result |
|---|---|---|
| [208](208-implement-trie-prefix-tree.md) `search` | a **walk** — one path | O(L) |
| **211** `search` | a **DFS** — branch at each dot | O(26^d · L) |

🤔 **Before you open the next section:** at a dot you recurse into every child. What should the function return if *one* branch matches but the others don't?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Search time | Verdict |
|---|---|---|---|
| List of words + pattern match | Compare the query against every stored word | O(n·L) | ❌ No sharing; scales with word count |
| Bucket words by length, then scan | Narrows the candidates | O(n·L) worst | ⚠️ A useful optimization, same order |
| **Trie + DFS with branching at dots** | Follow one child, or all | **O(L)** without dots, **O(26^d · L)** with d dots | ✅ |

**The decision: [problem 208](208-implement-trie-prefix-tree.md)'s trie, with `search` upgraded from a loop to a recursive DFS.**

The recursion has three cases, and they map directly onto the problem statement:

| At position `i` | Action |
|---|---|
| `i == len(word)` | **Base case** — the whole pattern is consumed. Return `node.is_end`: a path existing isn't enough, a word must *end* here |
| `word[i]` is a normal character | Follow that single child, or fail if absent — the deterministic case |
| `word[i]` is `"."` | **Branch** — recurse into *every* child; succeed if **any** succeeds |

**`any()` is exactly the right combiner.** You need *some* branch to work, not all — and `any()` short-circuits, stopping at the first success. That's the same `or` semantics as [Subtree of Another Tree](572-subtree-of-another-tree.md), where a match anywhere sufficed.

Contrast with [Same Tree](100-same-tree.md), where `and` was correct because *every* pair had to match. **Picking `any`/`or` versus `all`/`and` is the recurring question in these branching recursions**, and it's decided by whether you need existence or universality.

**Why the base case must still check `is_end`.** Consuming the whole pattern means you've reached the right *depth*, but `"ba"` matching the path toward `"bad"` isn't a match — no word ends at the `a`. Same distinction as [208](208-implement-trie-prefix-tree.md)'s `search` versus `startsWith`.

**Why the "at most 2 dots" constraint matters.** Each dot multiplies the branching by up to 26. With 2 dots that's ≤ 676 paths — trivial. Unbounded dots would make `"........"` explode to 26⁸. **The constraint is the problem telling you the exponential solution is acceptable** — the same signal as `n <= 8` in [Generate Parentheses](22-generate-parentheses.md).

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
```

A standard trie node — character → child, plus the end-of-word flag.

Note this uses a **separate node class** with `WordDictionary` holding a `root`, unlike [208](208-implement-trie-prefix-tree.md) where the trie *was* its own node. Both designs work; separating them is clearer when the public API and the internal structure differ, as they do here.
→ [class-basics](../syntax/class-basics.md) · [init-method](../syntax/init-method.md) · [trie](../data-structures/trie.md)

```python
def __init__(self):
    self.root = TrieNode()

def addWord(self, word: str) -> None:
    node = self.root
    for char in word:
        if char not in node.children:
            node.children[char] = TrieNode()
        node = node.children[char]
    node.is_end = True
```

**Identical to [208](208-implement-trie-prefix-tree.md)'s `insert`** — walk the word, create missing nodes, flag the end. The wildcard affects only searching, never storage.
→ [for-loop](../syntax/for-loop.md) · [membership-operators](../syntax/membership-operators.md) · [dict-basics](../syntax/dict-basics.md)

```python
def search(self, word: str) -> bool:
    def dfs(node, i):
        if i == len(word):
            return node.is_end
```

**Base case.** The pattern is fully consumed, so we're at the right depth — but a match requires a word to actually **end** here.

The two parameters are the complete state: *where we are in the trie* and *how far through the pattern*.
→ [function-basics](../syntax/function-basics.md) · [closures](../syntax/closures.md) · [recursion-basics](../syntax/recursion-basics.md)

```python
        char = word[i]
        if char == ".":
            return any(dfs(child, i + 1) for child in node.children.values())
```

**The wildcard case — the heart of the problem.** A dot matches any character, so try **every** child, advancing one position in the pattern.

`any()` returns `True` if *any* branch succeeds, and **short-circuits** on the first success — so a match found in the first child skips the other 25.

`.values()` gives the child nodes; the characters don't matter here, since a dot matches all of them.
→ [any-all](../syntax/any-all.md) · [generator-expressions](../syntax/generator-expressions.md) · [dict-methods](../syntax/dict-methods.md)

```python
        if char not in node.children:
            return False
        return dfs(node.children[char], i + 1)
```

**The deterministic case.** A normal character follows exactly one child — no branching, exactly as in [208](208-implement-trie-prefix-tree.md). If that child doesn't exist, this path fails.

Note this is a **single** recursive call, not a loop — the walk from 208 expressed recursively so it can interleave with the branching case.
→ [if-return](../syntax/if-return.md)

```python
    return dfs(self.root, 0)
```

Start at the root, position 0.

<details>
<summary>The whole thing together</summary>

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False


class WordDictionary:

    def __init__(self):
        self.root = TrieNode()

    def addWord(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word: str) -> bool:
        def dfs(node, i):
            if i == len(word):
                return node.is_end

            char = word[i]
            if char == ".":
                return any(dfs(child, i + 1) for child in node.children.values())
            if char not in node.children:
                return False
            return dfs(node.children[char], i + 1)

        return dfs(self.root, 0)
```

</details>

**Trace it** — after `addWord("bad")`, `addWord("dad")`, `addWord("mad")`:

```
        root
        /  |  \
       b   d   m
       |   |   |
       a   a   a
       |   |   |
       d*  d*  d*
```

**`search("bad")`** — no dots, a pure walk:

| `i` | char | Action |
|---|---|---|
| 0 | `b` | follow `b` |
| 1 | `a` | follow `a` |
| 2 | `d` | follow `d` |
| 3 | — | base case: `is_end` ✅ → **`True`** |

**`search(".ad")`** — branches at position 0:

| Branch | Path | Result |
|---|---|---|
| child `b` | `b` → `a` → `d`, `is_end` ✅ | **`True`** |
| children `d`, `m` | — | **never tried** — `any()` short-circuited |

→ **`True`** ✅

**`search("b..")`** — branches at positions 1 and 2:

| `i` | char | Action |
|---|---|---|
| 0 | `b` | follow `b` (one child) |
| 1 | `.` | `b`'s only child is `a` → one branch |
| 2 | `.` | `a`'s only child is `d` → one branch |
| 3 | — | `is_end` ✅ → **`True`** |

Note the branching was cheap here because each node had **one** child. The 26× factor is worst-case, not typical.

**`search("pad")`** — `p` isn't a child of root → **`False`** immediately ✅

</details>

<details>
<summary><b>4 · Time complexity</b> — O(L) to O(26^d · L)</summary>

| Operation | Cost |
|---|---|
| `addWord` | **O(L)** — one node step per character |
| `search`, **no dots** | **O(L)** — a deterministic walk, same as [208](208-implement-trie-prefix-tree.md) |
| `search`, **d dots** | **O(26^d · L)** worst case |

**Where the exponent comes from.** Each dot can branch into up to 26 children, and each branch continues independently. With d dots that's up to 26^d root-to-leaf paths, each costing O(L).

**Why the constraint saves you:** at most **2 dots** → 26² = **676** paths maximum. With L ≤ 25 that's ~17,000 steps per search — trivial.

**The worst case is rarely reached.** 26 branches assumes every node has a full alphabet of children, which requires an enormous, dense word set. In the trace above each node had **one** child, so the dots cost nothing. Real tries are sparse, and `any()` short-circuits on the first success.

**Versus scanning a word list:** O(n·L) per search, growing with the number of stored words. The trie's cost depends on the **pattern**, not the corpus — the same property that made [208](208-implement-trie-prefix-tree.md) worthwhile.

**A useful optimization to mention:** bucket words by length, since a dot matches exactly one character and lengths must agree. It prunes candidates before the search even starts.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(total characters)</summary>

**O(total characters added)** for the trie, plus **O(L)** recursion depth per search.

- **The trie:** one node per unique character path, with prefix sharing — exactly [208](208-implement-trie-prefix-tree.md)'s analysis. `"bad"`, `"dad"`, `"mad"` share no prefixes, so 9 nodes; a set of words sharing prefixes would use far fewer.
- **The recursion:** depth is bounded by the pattern length L ≤ 25 — trivially safe, no recursion-limit concern.

**Note the branching costs no extra space.** `any()` with a **generator expression** evaluates branches one at a time, so only one path is live at any moment:

```python
any(dfs(child, i + 1) for child in ...)     # ← generator: lazy, O(L) stack
any([dfs(child, i + 1) for child in ...])   # ← list: evaluates ALL branches first
```

The list-comprehension version would compute every branch even after finding a match — same space, but **losing the short-circuit** and doing needless work. A small but real reason to prefer the generator.
→ [generator-expressions](../syntax/generator-expressions.md)

**The alternative — storing words in a list** — is O(total characters) too, but with no prefix sharing and no fast prefix search. The trie's memory buys the query flexibility.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Adding words is a standard trie insert — the wildcard only affects searching. Without dots, search is a deterministic walk: follow one child per character. A dot breaks that, because any child could lead to a match and I can't know which without trying — so search becomes a DFS that branches at each dot, recursing into every child and succeeding if any branch does. I use `any()` with a generator so it short-circuits on the first match. The base case still checks `is_end`, since reaching the right depth isn't enough — a word has to actually end there. Search is O(L) without dots and O(26^d · L) with d dots, and the problem caps dots at 2, so that's at most 676 paths."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why does a dot force branching?" | **The question.** Any child could lead to a match, and you can't tell which without exploring. Deterministic walk → search. |
| "What if dots were unbounded?" | 26^d explodes. Mitigate by bucketing words by length, memoizing `(node, i)` states, or switching to an automaton-based matcher. |
| "Why `any` and not `all`?" | You need *some* word to match, not every branch. `all` would require every child to succeed. |
| "Why check `is_end` at the end?" | Reaching the right depth isn't a match — `"ba"` walks partway into `"bad"` but no word ends there. |
| "Support `*` (zero or more)?" | Substantially harder — a `*` can consume any number of characters, so you'd recurse on both "use it" and "skip it". That's [Regular Expression Matching](10-regular-expression-matching.md). |
| "Optimize for many searches on a fixed set?" | Bucket by length; precompute per-node child sets; or memoize `(node, position)` results. |
| "Why a separate `TrieNode` class here?" | The public API (`WordDictionary`) differs from the internal node, so separating them is clearer. [208](208-implement-trie-prefix-tree.md) merged them, which is also fine. |

**Traps:**

- **Returning `True` from the base case** instead of `node.is_end` — prefixes would match as words.
- **Using `all` instead of `any`** at a dot — you'd require every child to lead to a match.
- **Using a list comprehension inside `any()`** — loses the short-circuit and evaluates every branch.
- **Treating `.` as matching zero or more characters.** It matches exactly one; lengths must agree.
- **Trying to write the wildcard case iteratively** with a single pointer. Branching needs a stack or recursion — you can't track multiple candidate positions with one variable.
- **Forgetting that `addWord` is unchanged.** Only `search` differs from [208](208-implement-trie-prefix-tree.md).

**This same move shows up in:** [Implement Trie](208-implement-trie-prefix-tree.md) (the structure this extends) · [Word Search II](212-word-search-ii.md) (trie + DFS with backtracking) · [Subtree of Another Tree](572-subtree-of-another-tree.md) (`or` semantics — a match anywhere suffices) · [Generate Parentheses](22-generate-parentheses.md) (branching recursion where the constraint signals an exponential solution).

</details>
