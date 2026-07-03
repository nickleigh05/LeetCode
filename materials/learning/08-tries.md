# 08. Tries
*Prefix trees: O(k) prefix queries, the dictionary stored once.*

[← Prev](07-trees.md) · [🗺 Roadmap](../../roadmap.md) · [Next →](09-heap-priority-queue.md)

---

A **trie** stores a set of strings as a tree of shared prefixes, so looking up a word or prefix costs O(k) in the length of the key — independent of how many words you've stored. It's the structure behind autocomplete and the fast way to search many words against a board at once.

## Concept

### Trie

```
  Words inserted: "cat", "car", "card", "care", "bat"

         root
        /    \
       c      b
       |      |
       a      a
      / \     |
     t*  r    t*
         |
         *    ← "car"
        / \
       d*  e*  ← "card", "care"

  * = end of word marker (is_end = True)

  Each node:
  ┌──────────────────────────────┐
  │ children: dict[char → Node]  │
  │ is_end:   bool               │
  └──────────────────────────────┘
```

**What it is:** A tree where each path from root to a marked node spells out a word. Each node represents a character, and children represent the next possible characters.

**Key Properties:**
- Insert and search are O(L) where L = length of the word — independent of how many words are stored
- Excellent for prefix queries ("all words starting with 'ca'")
- Space is O(ALPHABET_SIZE × L × N) — can be large for big alphabets

**Complexity:**

| Operation | Time |
|-----------|------|
| Insert word | O(L) |
| Search word | O(L) |
| Prefix search | O(L) |
| Space | O(L × N × A) |

L = word length, N = number of words, A = alphabet size

**Use when:**
- Autocomplete / prefix matching
- Word search on a board (combine with DFS)
- Checking if any word in a list is a prefix of another
- Implementing a spell checker

**Python:**
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end

    def starts_with(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True
```

## The Pattern

### Trie Search

```
  Inserted words: "apple", "app", "apply", "apt"

              root
               |
               a
               |
               p
              / \
             p   t*   ← "apt"
            / \
           *   l
           ↑   |
          "app" y*  ← "apply"
               |
               e*  ← "apple"

  Search "apply": a→p→p→l→y → is_end=True ✓
  Search "ap":    a→p → is_end=False → word not in trie
  Prefix "ap":    a→p → node exists → prefix found ✓
  Search "apl":   a→p → no child 'l' → False
```

**What it is:** Build a Trie from a set of words, then traverse it character by character for search, prefix matching, or DFS over all words. Enables O(L) search independent of how many words exist.

**Use this when:**
- [ ] Implement autocomplete / search suggestions
- [ ] Check if any word from a dictionary is a prefix of another
- [ ] Word Search II (find all words from dictionary on a board)
- [ ] Replace words with prefixes (shortest prefix match)
- [ ] Design a search system with prefix filtering

**Python:**
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_end = True

    def search(self, word):
        node = self._get_node(word)
        return node is not None and node.is_end

    def starts_with(self, prefix):
        return self._get_node(prefix) is not None

    def _get_node(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

# Word Search II — find all words from list on board
def find_words(board, words):
    trie = Trie()
    for w in words:
        trie.insert(w)

    rows, cols = len(board), len(board[0])
    result = set()

    def dfs(node, r, c, path):
        ch = board[r][c]
        if ch not in node.children:
            return
        next_node = node.children[ch]
        path.append(ch)
        if next_node.is_end:
            result.add(''.join(path))
        board[r][c] = '#'   # mark visited
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nr, nc = r+dr, c+dc
            if 0<=nr<rows and 0<=nc<cols and board[nr][nc] != '#':
                dfs(next_node, nr, nc, path)
        board[r][c] = ch    # restore
        path.pop()

    for r in range(rows):
        for c in range(cols):
            dfs(trie.root, r, c, [])
    return list(result)
```

**Complexity:** Insert/search: O(L). Word Search II: O(rows × cols × 4^L) with pruning.

**Blind 75 examples:** Implement Trie · Design Add and Search Words · Word Search II

## The Template

The reusable code skeleton for this pattern lives in [`appendix/templates/tries/`](../appendix/templates/tries/). Read the README (when to reach for it, variations, common bugs), then type out [`template.py`](../appendix/templates/tries/template.py) from memory before you drill problems.

## Practice

Work the matching set in the curated list: [**Tries problems →**](../../lists/recommended.md#10-tries-6-problems). Easy → hard, top to bottom. When the pattern feels automatic, move on — don't grind it forever.

## Check Yourself

- [ ] I can build a trie node and insert/search from memory.
- [ ] I can explain why a trie gives O(k) prefix queries where a hash set can't.
- [ ] I can implement prefix search (startsWith) and wildcard matching.
- [ ] I solved a 🔴 Hard trie problem (e.g. Word Search II).

---

**Up next:** [Heaps & Priority Queues](09-heap-priority-queue.md) — the always-available extreme element — for top-K and streaming.

[← Prev](07-trees.md) · [🗺 Roadmap](../../roadmap.md) · [Next →](09-heap-priority-queue.md)

