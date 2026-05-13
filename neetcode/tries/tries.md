# Tries

## How to use this README

Problems are split into three tiers: Blind 75 covers the three foundational trie problems — implement, design with wildcards, and use with grid DFS. NeetCode 150 adds nothing new beyond Blind 75 for this topic. NeetCode 250 adds one problem that combines a trie with dynamic programming. Work through tiers in order — the Core Patterns and Syntax Reference sections below map directly to the problems in each table, so when you hit a new problem, determine first whether you need a plain search, a wildcard DFS, or a trie-backed DP before writing the node structure.

---

## Problems

### Blind 75
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved |
|-----------|------------|--------------|---------------|--------|
| 208 | Medium | Implement Trie (Prefix Tree) | [Link](https://leetcode.com/problems/implement-trie-prefix-tree/) | ☐ |
| 211 | Medium | Design Add and Search Words Data Structure | [Link](https://leetcode.com/problems/design-add-and-search-words-data-structure/) | ☐ |
| 212 | Hard | Word Search II | [Link](https://leetcode.com/problems/word-search-ii/) | ☐ |

### NeetCode 150
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved |
|-----------|------------|--------------|---------------|--------|

> No problems are added in NeetCode 150 beyond Blind 75 for this topic.

### NeetCode 250
| Problem # | Difficulty | Problem Name | LeetCode Link | Solved | Pattern |
|-----------|------------|--------------|---------------|--------|---------|
| 2707 | Medium | Extra Characters in a String | [Link](https://leetcode.com/problems/extra-characters-in-a-string/) | ☐ | Trie + DP |

---

## Complexity Reference

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| Insert word of length L | O(L) | O(L × ALPHA) | Creates up to L new nodes |
| Search word of length L | O(L) | O(1) | Traverses existing nodes |
| Prefix search (startsWith) | O(L) | O(1) | Same as search, skip is_end check |
| Wildcard search (DFS) | O(L × ALPHA^d) | O(L) | d = number of '.' characters |
| Word Search II (grid DFS) | O(M × N × 4^L) | O(N × L) | Grid cells × branching factor |
| Build trie from N words | O(N × L) | O(N × L × ALPHA) | L = average word length |

> ALPHA = alphabet size (26 for lowercase English letters). In practice, shared prefixes dramatically reduce actual node count.

---

## Data Structures

### Trie (Prefix Tree)

A tree where each edge represents a single character, and each node represents the prefix formed by following edges from the root to that node. Children are stored in a hash map (`dict`) keyed by character, so any branch factor is supported without wasting space on empty slots. A boolean flag `is_end` marks nodes that are the final character of a complete inserted word.

```
Insert: "car", "card", "care", "cat", "bat"

root
├── c
│   └── a
│       ├── r  (is_end=True: "car")
│       │   ├── d  (is_end=True: "card")
│       │   └── e  (is_end=True: "care")
│       └── t  (is_end=True: "cat")
└── b
    └── a
        └── t  (is_end=True: "bat")
```

**When it matters:** Tries shine when you need to check many different prefixes against the same set of words — O(L) per query regardless of vocabulary size. A hash set of words also gives O(L) lookups but cannot answer "does any word start with this prefix?" without iterating every word.

### Memory Layout

Each `TrieNode` holds a `dict` of children and a boolean. With 26-character alphabets and long words, a trie can use more memory than a hash set because every character gets its own node rather than the whole word being hashed at once. Shared prefixes offset this: "pre", "prefix", "preview" share the nodes for p → r → e rather than storing those characters three times.

```
Hash set approach (3 full strings stored):
{"pre", "prefix", "preview"}

Trie approach (shared prefix nodes):
p → r → e (is_end) → f → i → x (is_end)
                              → e → w (is_end)

Savings: "pre" prefix stored once instead of three times
```

**When it matters:** For large vocabularies with common prefixes (dictionary, autocomplete), a trie uses less memory than storing full strings. For small vocabularies or when only exact-match lookups are needed, a plain set is simpler.

---

## Core Patterns

### Insert + Search
**When to use:** Building a trie from a word list and querying whether exact words exist.  
**Complexity:** O(L) per insert, O(L) per search — L is the word length  
**Problems:** #208  
**Common mistake:** Checking `is_end` during prefix search (`startsWith`) — `startsWith` should return `True` as long as all characters are found, regardless of `is_end`.

```python
def insert(self, word):
    node = self.root
    for ch in word:
        if ch not in node.children:
            node.children[ch] = TrieNode()   # create missing edge
        node = node.children[ch]
    node.is_end = True                        # mark complete word boundary

def search(self, word):
    node = self.root
    for ch in word:
        if ch not in node.children:
            return False
        node = node.children[ch]
    return node.is_end                        # True only if this is a full word
```

### Prefix Search (startsWith)
**When to use:** Autocomplete, "does any inserted word start with this prefix?" checks.  
**Complexity:** O(L)  
**Problems:** #208, #2707  
**Common mistake:** Returning `node.is_end` instead of `True` — `startsWith` doesn't require a complete word at the end of the prefix.

```python
def startsWith(self, prefix):
    node = self.root
    for ch in prefix:
        if ch not in node.children:
            return False           # prefix path doesn't exist in the trie
        node = node.children[ch]
    return True                    # reached end of prefix — is_end irrelevant here
```

### Wildcard Search with DFS ('.')
**When to use:** Pattern matching where '.' can match any single character.  
**Complexity:** O(L × 26^d) where d = number of wildcards  
**Problems:** #211  
**Common mistake:** Returning early on the first successful child match without letting the loop try remaining children — the loop must try all children when the character is '.'.

```python
def search(self, word):
    def dfs(node, i):
        if i == len(word):
            return node.is_end
        ch = word[i]
        if ch == '.':
            for child in node.children.values():   # try every possible character
                if dfs(child, i + 1):
                    return True
            return False
        if ch not in node.children:
            return False
        return dfs(node.children[ch], i + 1)
    return dfs(self.root, 0)
```

### Word Search II (Trie + Grid DFS)
**When to use:** Find all words from a list that exist as paths in a 2D character grid.  
**Complexity:** O(M × N × 4^L) where M×N is grid size and L is max word length  
**Problems:** #212  
**Common mistake:** Not deleting found words from the trie — without pruning, the same word can be reported multiple times and DFS revisits dead branches unnecessarily.

```python
def findWords(self, board, words):
    trie = Trie()
    for w in words:
        trie.insert(w)

    rows, cols = len(board), len(board[0])
    result = set()

    def dfs(node, r, c, path):
        if node.is_end:
            result.add(path)
            node.is_end = False    # prune: don't report the same word twice
        tmp, board[r][c] = board[r][c], '#'   # mark visited in-place
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                ch = board[nr][nc]
                if ch in node.children:
                    dfs(node.children[ch], nr, nc, path + ch)
        board[r][c] = tmp          # restore cell after backtracking

    for r in range(rows):
        for c in range(cols):
            ch = board[r][c]
            if ch in trie.root.children:
                dfs(trie.root.children[ch], r, c, ch)

    return list(result)
```

### Trie + DP (Extra Characters)
**When to use:** Count or minimize something while building a string, where valid "chunks" come from a dictionary.  
**Complexity:** O(n² × L) time with trie; O(n × N × L) without — trie prunes dead branches early  
**Problems:** #2707  
**Common mistake:** Using a plain set for the dictionary and iterating all substrings naively — the trie lets you stop exploring a substring the moment no word can extend it further.

```python
def minExtraChar(self, s, dictionary):
    trie = Trie()
    for w in dictionary:
        trie.insert(w)

    n = len(s)
    dp = [0] * (n + 1)   # dp[i] = min extra chars in s[i:]

    for i in range(n - 1, -1, -1):
        dp[i] = dp[i + 1] + 1   # worst case: skip s[i] (counts as extra)
        node = trie.root
        for j in range(i, n):
            if s[j] not in node.children:
                break                        # no word starts with s[i..j], stop early
            node = node.children[s[j]]
            if node.is_end:
                dp[i] = min(dp[i], dp[j + 1])  # use word s[i..j], no extra chars here
    return dp[0]
```

---

## Syntax Reference

### TrieNode and Trie classes

The complete implementation used as a base for all trie problems.

```python
class TrieNode:
    def __init__(self):
        self.children = {}     # char → TrieNode; dict supports any alphabet size
        self.is_end = False    # True when this node is the last char of an inserted word

class Trie:
    def __init__(self):
        self.root = TrieNode()   # root has no character; it's the entry point

    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True
```

### Fixed-size array alternative (26 lowercase letters only)

Replaces the `dict` with a list of 26 slots indexed by `ord(ch) - ord('a')`. Faster constant factor, but wastes memory if the alphabet is sparse.

```python
class TrieNode:
    def __init__(self):
        self.children = [None] * 26   # index 0='a', 1='b', ..., 25='z'
        self.is_end = False

# insert character ch:
idx = ord(ch) - ord('a')
if not node.children[idx]:
    node.children[idx] = TrieNode()
node = node.children[idx]
```

### In-place grid marking (Word Search II backtracking)

Avoids a separate `visited` set by temporarily overwriting the cell value. Must restore it after the recursive call returns.

```python
tmp = board[r][c]
board[r][c] = '#'       # any character not in the alphabet works as a sentinel

# ... recursive DFS calls ...

board[r][c] = tmp       # always restore, even if DFS found nothing
```

### Trie pruning after finding a word

Deleting found words from the trie prevents duplicate results and speeds up subsequent DFS calls by eliminating dead branches.

```python
if node.is_end:
    result.add(current_word)
    node.is_end = False    # turn off flag so this path is not reported again

# optional: remove leaf nodes with no children to compact the trie
def prune(node, ch):
    if not node.children[ch].children and not node.children[ch].is_end:
        del node.children[ch]
```

### Four-directional movement on a grid

Standard delta-pair loop for grid DFS. Always bounds-check before accessing `board[nr][nc]`.

```python
directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]   # right, left, down, up

for dr, dc in directions:
    nr, nc = r + dr, c + dc
    if 0 <= nr < rows and 0 <= nc < cols:
        # safe to access board[nr][nc]
```

### DP array for string segmentation problems

`dp[i]` represents the answer for the suffix `s[i:]`. Fill right-to-left so smaller indices depend on already-computed larger indices.

```python
n = len(s)
dp = [float('inf')] * (n + 1)
dp[n] = 0                       # empty suffix has answer 0 (base case)

for i in range(n - 1, -1, -1):
    # try all substrings s[i..j] that exist in the trie
    # dp[i] = min over valid j of dp[j + 1] + (cost of using s[i..j])
    pass
```
