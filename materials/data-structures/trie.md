# Trie (Prefix Tree)

```python
class TrieNode:
    def __init__(self):
        self.children = {}      # char -> TrieNode
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
```

A tree where each path from the root spells out a prefix, and nodes are shared between words with a common start — `"cat"` and `"car"` share the `c -> a` path, then split. Checking whether a string is a prefix of anything inserted takes O(k) (k = string length), regardless of how many words are stored — compare to scanning every stored word, which would be O(n·k).

**Complexity:** insert/search/prefix-check O(k) where k is the word/prefix length.

**Related:** [dict-basics (syntax)](../syntax/dict-basics.md) · [class-basics (syntax)](../syntax/class-basics.md) · [dfs](../algorithms/dfs.md)
