# 08. Tries — Practice

The Roadmap follows a curated list called the NeetCode 150 for practice problems. If you want more or fewer problems, check the other lists in [lists/](../../lists/).

---

### 208. Implement Trie (Prefix Tree) — Medium
[LeetCode](https://leetcode.com/problems/implement-trie-prefix-tree/)  
[Solution file (no hints)](../../problems/0001-0499/208.py)

Implement insert, search, and startsWith for a [trie](../data-structures/trie.md). Why does each node holding a hashmap of `char -> child node` let a search walk exactly one character at a time down the tree?

<details>
<summary>Hint</summary>

Each [trie](../data-structures/trie.md) node has a dict of children and an `is_end` flag. `insert` walks/creates a child per character; `search` requires the final node's `is_end` to be True, while `startsWith` only requires the path to exist.
</details>

<details>
<summary>Solution</summary>

```python
class TrieNode:
    def __init__(self):
        self.children = {}                 # char -> TrieNode
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for c in word:                        # for loop creating/walking nodes
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.is_end = True                    # mark the end of a complete word

    def _find(self, prefix):
        node = self.root
        for c in prefix:
            if c not in node.children:          # path doesn't exist
                return None
            node = node.children[c]
        return node

    def search(self, word):
        node = self._find(word)
        return node is not None and node.is_end

    def startsWith(self, prefix):
        return self._find(prefix) is not None
```

Building blocks: [class-basics](../syntax/class-basics.md) · [dict-basics](../syntax/dict-basics.md) · [for-loop](../syntax/for-loop.md) · [membership-operators](../syntax/membership-operators.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(L)** per operation, where L is the length of the word/prefix.
**Space: O(total characters inserted)** — one trie node per unique character path.
</details>

---

### 211. Design Add and Search Words Data Structure — Medium
[LeetCode](https://leetcode.com/problems/design-add-and-search-words-data-structure/)  
Solution: not yet solved in this repo.

Same as a trie, but search supports `.` as a wildcard matching any character. Why does a `.` force you to branch and try *every* child instead of following a single path?

<details>
<summary>Hint</summary>

Build a [trie](../data-structures/trie.md) exactly like [208](#208-implement-trie-prefix-tree--medium). For search, use DFS (see [DFS](../algorithms/dfs.md)): on a normal character follow that one child; on `.`, recurse into every child and return True if any path succeeds.
</details>

<details>
<summary>Solution</summary>

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class WordDictionary:
    def __init__(self):
        self.root = TrieNode()

    def addWord(self, word):
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.is_end = True

    def search(self, word):
        def dfs(node, i):
            if i == len(word):                  # consumed the whole word
                return node.is_end
            c = word[i]
            if c == ".":                          # wildcard: try every child
                return any(dfs(child, i + 1) for child in node.children.values())
            if c not in node.children:            # no matching path
                return False
            return dfs(node.children[c], i + 1)

        return dfs(self.root, 0)
```

Building blocks: [class-basics](../syntax/class-basics.md) · [recursion-basics](../syntax/recursion-basics.md) · [generator-expressions](../syntax/generator-expressions.md) (`any(... for ...)`) · [dict-methods](../syntax/dict-methods.md) (`.values()`)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(L)** for a word with no wildcards; **O(26^d · L)** worst case with d wildcards (branching at each).
**Space: O(total characters inserted)** for the trie, plus O(L) recursion depth per search.
</details>

---

### 212. Word Search II — Hard
[LeetCode](https://leetcode.com/problems/word-search-ii/)  
Solution: not yet solved in this repo.

Given a grid of letters and a list of words, find all words that can be traced through adjacent cells. Why is building a single [trie](../data-structures/trie.md) from all the words far more efficient than running "word search" separately for each word?

<details>
<summary>Hint</summary>

Insert every word into a shared [trie](../data-structures/trie.md), then run one [DFS](../algorithms/dfs.md)/[backtracking](../algorithms/backtracking.md) traversal per grid cell, walking the trie alongside the grid so multiple words with shared prefixes are explored together instead of duplicating work.
</details>

<details>
<summary>Solution</summary>

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None                    # stores the full word at end nodes

def build_trie(words):
    root = TrieNode()
    for w in words:
        node = root
        for c in w:
            node = node.children.setdefault(c, TrieNode())
        node.word = w
    return root

rows, cols = len(board), len(board[0])
root = build_trie(words)
res = set()

def dfs(r, c, node):
    letter = board[r][c]
    if letter not in node.children:        # no word continues this way
        return
    nxt = node.children[letter]
    if nxt.word:                              # completed a word
        res.add(nxt.word)

    board[r][c] = "#"                       # mark visited
    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:   # explore 4 neighbors
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != "#":
            dfs(nr, nc, nxt)
    board[r][c] = letter                    # un-mark (backtrack)

for r in range(rows):
    for c in range(cols):
        dfs(r, c, root)

return list(res)
```

Building blocks: [dict-methods](../syntax/dict-methods.md) (`.setdefault()`) · [recursion-basics](../syntax/recursion-basics.md) · [nested-lists](../syntax/nested-lists.md) · [set-basics](../syntax/set-basics.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(rows · cols · 4^L)** — L is the max word length; the trie prunes branches early once a prefix no longer matches.
**Space: O(total characters in words)** for the trie, plus O(L) recursion depth per DFS call.
</details>
