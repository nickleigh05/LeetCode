# 212. Word Search II

**Hard** · [LeetCode](https://leetcode.com/problems/word-search-ii/)

[📖 08. Tries lesson](../learning/08-tries.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 08. Tries problems](../rmap-practice/08-tries.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Given an `m × n` board of characters and a list of strings `words`, return **all words on the board**.

Each word must be constructed from letters of **sequentially adjacent** cells (horizontally or vertically neighbouring), and **the same cell may not be used more than once** in a single word.

```
board = [["o","a","a","n"],       words = ["oath","pea","eat","rain"]
         ["e","t","a","e"],
         ["i","h","k","r"],       →  ["oath", "eat"]
         ["i","f","l","v"]]
```

**Constraints:** `1 <= m, n <= 12` · `1 <= words.length <= 3·10⁴` · `1 <= word.length <= 10` · lowercase letters · all words **unique**

> **Try it yourself first.** This is the hardest problem in the unit — the sections build up carefully.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**sequentially adjacent**" | A path through the grid, moving up/down/left/right — a DFS over a 2-D grid |
| "the same cell **may not be used twice**" | ⚠️ You must mark cells as visited during a path and **unmark on the way back** — that's backtracking |
| "return **all** words" | Collect matches, don't stop at the first |
| **3·10⁴ words** | ⚠️ **The crux.** Searching for each word separately is hopeless |
| board only **12 × 12** | Small grid, huge word list — the imbalance is the hint |
| word length ≤ 10 | Bounds the DFS depth |

**Why the obvious approach dies.** [Word Search I](79-word-search.md) finds *one* word: DFS from every cell, O(m·n·4^L). Running that once per word gives:

```
3·10⁴ words × 144 cells × 4^10 ≈ astronomically slow
```

**Where the waste is.** Suppose the list contains `"oath"`, `"oat"`, `"oatmeal"`, and `"oak"`. Searching each independently re-traces the path `o → a → t` **three times**. The words share prefixes, and the searches share work — but nothing exploits that.

**The insight: invert the loop.** Instead of *"for each word, search the grid"*, do *"walk the grid once, and check all words simultaneously."*

That requires a structure that can answer, at every step of a path: **"is this prefix the start of any word?"** and **"is this prefix a complete word?"**

That's exactly a **[trie](../data-structures/trie.md)**.

Walking the grid and the trie **in lockstep** means:
- Shared prefixes are explored **once**, not once per word.
- The moment a prefix leaves the trie, **every** word beginning that way is eliminated at a stroke — the pruning that makes it feasible.

🤔 **Before you open the next section:** if you're at grid cell `t` having traced `o → a → t`, what single check tells you whether it's worth continuing in any direction?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Verdict |
|---|---|---|
| Run [Word Search I](79-word-search.md) per word | 3·10⁴ independent grid searches | ❌ Hopeless — no shared work |
| Collect every possible path, check membership | Enumerate all paths, test each against a set | ❌ 4^L paths per cell, no pruning |
| **Trie + one backtracking DFS per cell** | Walk grid and trie together | ✅ |

**The decision: build one trie from all words, then run a backtracking DFS from every cell, advancing through the trie in step with the grid.**

Three mechanisms combine, and each earns its place:

**1. The trie prunes.** At each cell, the current letter must be a child of the current trie node. If not, **return immediately** — that kills every word with this prefix at once. This is what converts a hopeless search into a fast one: the trie says "no word goes this way" in O(1).

**2. Backtracking handles the no-reuse rule.** Mark the cell (here by overwriting it with `"#"`), explore the four neighbours, then **restore it**. The restore is essential — the cell must be available to paths that don't currently include it. Choose → explore → un-choose, exactly the [backtracking](../algorithms/backtracking.md) shape from [Generate Parentheses](22-generate-parentheses.md).

**3. Storing the word *at* the terminal node** rather than an `is_end` flag. When you reach a node with `node.word` set, you have the complete word immediately — no need to have tracked the path's characters. A small but genuinely elegant simplification over [208](208-implement-trie-prefix-tree.md)'s boolean.

**Why a `set` for results.** The same word can be reachable by different paths, and duplicates must not appear in the output. A set deduplicates for free.

**Why marking in-place beats a separate `visited` set.** Overwriting with `"#"` is O(1) with no allocation, and the check `board[r][c] != "#"` covers both "not visited" and "still a valid letter". A `visited` set of coordinates works identically and is less destructive — mention it if the interviewer objects to mutating the input.

**The classic optimization worth naming:** after finding a word, set `node.word = None` so it isn't re-found, and optionally prune leaf nodes from the trie once they're exhausted. This shrinks the trie as the search progresses.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None
```

**`word` instead of `is_end`.** A terminal node stores the actual string, so reaching it hands you the answer directly — no need to reconstruct the path.
→ [class-basics](../syntax/class-basics.md) · [trie](../data-structures/trie.md)

```python
root = TrieNode()
for word in words:
    node = root
    for char in word:
        if char not in node.children:
            node.children[char] = TrieNode()
        node = node.children[char]
    node.word = word
```

**Build one trie from all the words** — the standard insert from [208](208-implement-trie-prefix-tree.md), with `node.word = word` replacing the flag.

This is where shared prefixes get merged: `"oath"` and `"oat"` occupy overlapping paths, so the grid search explores them together.
→ [for-loop](../syntax/for-loop.md) · [membership-operators](../syntax/membership-operators.md) · [dict-basics](../syntax/dict-basics.md)

```python
rows = len(board)
cols = len(board[0])
found = set()
```

A **set** for results, since the same word may be reachable by multiple paths.
→ [set-basics](../syntax/set-basics.md) · [nested-lists](../syntax/nested-lists.md)

```python
def dfs(row, col, node):
    letter = board[row][col]
    if letter not in node.children:
        return
```

**The pruning check — the line that makes this feasible.** If the current letter isn't a child of the current trie node, **no word continues this way**, so abandon the entire branch.

One dict lookup eliminates every word sharing this dead prefix.
→ [function-basics](../syntax/function-basics.md) · [closures](../syntax/closures.md) · [if-return](../syntax/if-return.md)

```python
    next_node = node.children[letter]
    if next_node.word is not None:
        found.add(next_node.word)
```

Advance in the trie. If a word terminates here, record it.

⚠️ **No `return` after adding.** A longer word may continue past this point — finding `"oat"` mustn't stop the search for `"oath"`.
→ [none-type](../syntax/none-type.md) · [identity-operators](../syntax/identity-operators.md)

```python
    board[row][col] = "#"
```

**Mark as visited** by overwriting the cell. Since `"#"` is never a child in the trie, any path revisiting this cell fails the pruning check above — enforcing "no cell twice" with no extra structure.

```python
    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        r = row + dr
        c = col + dc
        if 0 <= r < rows and 0 <= c < cols and board[r][c] != "#":
            dfs(r, c, next_node)
```

**Explore the four neighbours.** The direction list is the standard 4-neighbour idiom from the [grids primer](../learning/10b-grids-primer.md).

The chained comparison `0 <= r < rows` checks both bounds at once — Python-specific and worth using.

Each recursive call passes `next_node`, keeping the grid position and trie position advancing together.
→ [chained-comparisons](../syntax/chained-comparisons.md) · [tuple-unpacking](../syntax/tuple-unpacking.md) · [for-loop](../syntax/for-loop.md)

```python
    board[row][col] = letter
```

**The un-choose step.** Restore the cell so other paths can use it. **Omit this and the board is progressively destroyed**, causing later searches to fail mysteriously — the defining bug of backtracking problems.

```python
for row in range(rows):
    for col in range(cols):
        dfs(row, col, root)

return list(found)
```

Start a search from **every** cell — a word can begin anywhere.

<details>
<summary>The whole thing together</summary>

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None


class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:

        root = TrieNode()
        for word in words:
            node = root
            for char in word:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
            node.word = word

        rows = len(board)
        cols = len(board[0])
        found = set()

        def dfs(row, col, node):
            letter = board[row][col]
            if letter not in node.children:
                return

            next_node = node.children[letter]
            if next_node.word is not None:
                found.add(next_node.word)

            board[row][col] = "#"
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                r = row + dr
                c = col + dc
                if 0 <= r < rows and 0 <= c < cols and board[r][c] != "#":
                    dfs(r, c, next_node)
            board[row][col] = letter

        for row in range(rows):
            for col in range(cols):
                dfs(row, col, root)

        return list(found)
```

</details>

**Trace it** — finding `"eat"` in the example board:

```
board:  o a a n        trie (partial):  root
        e t a e                         ├─ o → a → t → h*
        i h k r                         └─ e → a → t*
        i f l v
```

Starting DFS at cell `(1,0)` = `e`:

| Step | Cell | Letter | Trie node | Action |
|---|---|---|---|---|
| 1 | (1,0) | `e` | root → `e` ✅ | mark `#`, explore neighbours |
| 2 | (1,1) | `t` | `e` has no child `t` ❌ | **prune, return** |
| 3 | (0,0) | `o` | `e` has no child `o` ❌ | **prune** |
| 4 | (2,0) | `i` | no child `i` ❌ | **prune** |

Hmm — `e`'s only child is `a`, and no neighbour of (1,0) is an `a`. So this start fails.

The successful path is from cell **(1,3)** = `e`:

| Step | Cell | Letter | Trie | Action |
|---|---|---|---|---|
| 1 | (1,3) | `e` | root → `e` ✅ | mark, explore |
| 2 | (1,2) | `a` | `e` → `a` ✅ | mark, explore |
| 3 | (1,1) | `t` | `a` → `t` ✅, **`word = "eat"`** | **add "eat"** ✅ |

Then all three cells are restored on the way back out.

**And the pruning in action:** starting at cell (0,3) = `n`, the very first check finds no `n` child at the root → **immediate return**. All 3·10⁴ words are eliminated by one dict lookup.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(m · n · 4^L)</summary>

**O(m · n · 4·3^(L−1))**, commonly written **O(m · n · 4^L)**, where L is the maximum word length.

| Component | Cost |
|---|---|
| Build the trie | O(total characters in words) = O(W·L) |
| Start a DFS from each cell | m · n starts |
| Each DFS path | up to L deep, branching 4 ways (3 after the first, since you can't go back) |

**The 4^L is the worst case, and the trie is what stops it being reached.** Without the trie, every path of length L is explored from every cell. With it, a path dies the instant its prefix leaves the trie — and most prefixes do, immediately.

**The real win is in the comparison:**

| Approach | Cost |
|---|---|
| Word Search I per word | **W × m·n × 4^L** — 3·10⁴ separate searches |
| **Trie** | **m·n × 4^L** — one search, W eliminated from the exponent |

The word count drops out of the search entirely, appearing only in the O(W·L) trie construction. **That's the whole point:** shared prefixes are explored once, and dead prefixes are eliminated in bulk.

**With L ≤ 10 and a 12×12 board**, the bound is manageable, and real inputs are far below it because the pruning is so aggressive.

**Worth mentioning:** setting `node.word = None` after finding a word, and pruning exhausted trie leaves, shrinks the search space as it progresses.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(total characters)</summary>

**O(total characters in `words`)** for the trie, plus **O(L)** recursion depth.

- **The trie:** up to W·L nodes, minus whatever prefix sharing saves. With 3·10⁴ words of length ≤ 10, that's at most 3·10⁵ nodes — and far fewer in practice, since shared prefixes collapse.
- **The recursion:** at most L frames, since a path can't exceed the longest word. L ≤ 10, so no recursion-limit concern.
- **`found`:** at most W words.

**The board is modified in place** and restored, so it costs **no extra space** — that's why `"#"` marking is preferred over a `visited` set, which would be O(L) per path.

**Prefix sharing is doing double duty here**, and it's worth saying explicitly: it saves memory *and* it's the mechanism that saves time. The same merged node that stores `"oat"` and `"oath"` once is the node that lets one grid step advance both searches. **The structure and the speedup are the same fact.**

**If memory were tight:** you could process the words in batches, building a smaller trie per batch — trading repeated grid traversals for a smaller resident structure.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Running Word Search I once per word is hopeless with 3·10⁴ words — and it re-traces shared prefixes over and over. So I invert the loop: instead of searching the grid per word, I walk the grid once and check all the words at the same time. That needs a structure answering 'is this prefix the start of any word?', which is a trie. I build one trie from all the words, then DFS from every cell, advancing through the grid and the trie in lockstep. The pruning is the key: if the current letter isn't a child of the current trie node, no word goes this way, so I return immediately and eliminate every word with that prefix at once. I mark cells during a path and restore them on the way back to enforce no-reuse, and I store the word itself at terminal nodes so finding one is immediate. The word count leaves the search entirely — it only affects trie construction."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why a trie instead of per-word search?" | **The question.** Shared prefixes are explored once, and a failed prefix kills every word beginning with it in one check. The word count drops out of the search cost. |
| "Optimize further." | Set `node.word = None` after a match so it isn't re-found; prune trie leaves once exhausted, shrinking the structure as you go. |
| "Why restore the board cell?" | Backtracking — the cell must be available to other paths. Omit it and the board degrades permanently. |
| "Avoid mutating the input?" | Use a `visited` set of coordinates instead of `"#"`. O(L) extra per path, but non-destructive. |
| "Why a set for results?" | The same word can be reachable by multiple paths; a set deduplicates. |
| "What if words could be very long?" | The 4^L term dominates. Deeper pruning, or meeting in the middle, but the trie is still the base. |
| "How is this different from Word Search I?" | One word versus many. With one word a trie is pointless overhead — the win comes entirely from sharing across words. |

**Traps:**

- **Forgetting to restore the board cell.** The defining backtracking bug — the board is destroyed and later searches silently fail.
- **Returning after finding a word.** Longer words may extend past it — finding `"oat"` mustn't abort the search for `"oath"`.
- **Checking bounds before marking**, or in the wrong order — mark, explore, restore.
- **Using a list instead of a set** for results, producing duplicates.
- **Running one DFS per word** — correct, catastrophically slow.
- **Not pruning on the trie check**, so the DFS explores paths no word can complete.
- **`is_end` plus path reconstruction** instead of storing the word. It works, but storing the word is simpler and free.

**This same move shows up in:** [Implement Trie](208-implement-trie-prefix-tree.md) (the structure) · [Design Add and Search Words](211-design-add-and-search-words-data-structure.md) (trie + branching DFS) · [Word Search](79-word-search.md) (the single-word version this generalizes) · [Number of Islands](200-number-of-islands.md) and the [grids primer](../learning/10b-grids-primer.md) (grid DFS with visited marking) · [backtracking](../algorithms/backtracking.md).

</details>

---
