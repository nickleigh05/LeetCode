# Tries

## 8. Tries (3 problems)

| Problem # | Difficulty | Problem Name | LeetCode Link |
|-----------|------------|--------------|---------------|
| 208 | Medium | Implement Trie (Prefix Tree) | [Link](https://leetcode.com/problems/implement-trie-prefix-tree/) |
| 211 | Medium | Design Add and Search Words Data Structure | [Link](https://leetcode.com/problems/design-add-and-search-words-data-structure/) |
| 212 | Hard | Word Search II | [Link](https://leetcode.com/problems/word-search-ii/) |

---

## Data Structures

### Trie (Prefix Tree)
A tree where each node represents one character in a string. The path from the root to a node spells out a prefix. Each node has up to 26 children (one per letter) and a boolean `is_end` flag marking where a complete word ends. Lookup and insertion are O(L) where L is the word length — independent of how many words are stored.

A trie node in Python:
```python
class TrieNode:
    def __init__(self):
        self.children = {}   # char -> TrieNode
        self.is_end = False
```

---

## Core Patterns

### Insert
Walk the trie character by character. If the next character doesn't have a child node, create one. After processing all characters, mark `is_end = True` on the last node.

### Search (Exact Match)
Walk the trie character by character. If any character is missing from `children`, return False. If you reach the end of the word, return `node.is_end` (True only if a complete word was inserted here, not just a prefix).

### StartsWith (Prefix Check)
Same as search but don't check `is_end` at the end — just check that every character exists. Return True if you walk through all characters without hitting a missing child.

### Wildcard Search with DFS
When a `.` wildcard is encountered, branch into all existing children and recurse. This turns the search into a DFS. Used in Design Add and Search Words.

### Trie + DFS on Grid (Word Search II)
Build a trie from all target words. Then DFS from every cell in the grid, walking the trie at the same time — if the current character isn't in the trie node's children, prune the DFS branch early. When you reach a `is_end` node, record the found word. This is much faster than running a separate DFS for each word. Used in Word Search II.
