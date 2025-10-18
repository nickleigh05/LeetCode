# Tries (Prefix Trees)

## What is a Trie?
A Trie (pronounced "try") is a tree-like data structure used to store and retrieve strings efficiently. It's particularly useful for prefix-based searches, autocomplete, and spell checking. Each path from root to node represents a string, and nodes share common prefixes.

## Visual Representation

### Basic Trie Structure
```
Empty Trie:
    root
    └─ ∅ (no children)

Trie with "cat":
    root
     └─ c
        └─ a
           └─ t*  (* = end of word)

Trie with "cat", "car", "dog":
    root
    ├─ c
    │  └─ a
    │     ├─ t*
    │     └─ r*
    └─ d
       └─ o
          └─ g*
```

### Detailed Node Structure
```
Each node contains:
┌─────────────────────┐
│  is_end_of_word     │ ← Boolean flag
│  children[26]       │ ← Array/Map of child nodes
│  (or HashMap)       │
└─────────────────────┘

Example for word "cat":
    c → is_end: False, children: {'a': node}
    a → is_end: False, children: {'t': node}
    t → is_end: True,  children: {}
```

## Building a Trie Step-by-Step

### Insert "cat", "car", "dog", "door"

```
Step 1: Insert "cat"
    root
     └─ c
        └─ a
           └─ t*

Step 2: Insert "car" (shares "ca" prefix)
    root
     └─ c
        └─ a
           ├─ t*
           └─ r*

Step 3: Insert "dog"
    root
    ├─ c
    │  └─ a
    │     ├─ t*
    │     └─ r*
    └─ d
       └─ o
          └─ g*

Step 4: Insert "door" (shares "do" prefix)
    root
    ├─ c
    │  └─ a
    │     ├─ t*
    │     └─ r*
    └─ d
       └─ o
          ├─ g*
          └─ o
             └─ r*

Visual with array representation:
root
├─ [c]: children[2] (0-indexed: a=0, b=1, c=2...)
│  └─ [a]: children[0]
│     ├─ [t]: end=True
│     └─ [r]: end=True
└─ [d]: children[3]
   └─ [o]: children[14]
      ├─ [g]: end=True
      └─ [o]: children[14]
         └─ [r]: end=True
```

## Trie Operations

### 1. Insert Operation

```
Insert "apple":

Start at root, iterate through each character:

Step 1: 'a'
    root
     └─ a (create if not exists)

Step 2: 'p'
    root
     └─ a
        └─ p (create if not exists)

Step 3: 'p'
    root
     └─ a
        └─ p
           └─ p (create if not exists)

Step 4: 'l'
    root
     └─ a
        └─ p
           └─ p
              └─ l (create if not exists)

Step 5: 'e'
    root
     └─ a
        └─ p
           └─ p
              └─ l
                 └─ e* (mark as end of word)

Time Complexity: O(m) where m = length of word
Space Complexity: O(m) for new word
```

### 2. Search Operation

```
Search for "car" in trie:
    root
    ├─ c
    │  └─ a
    │     ├─ t*
    │     └─ r*
    └─ d

Step 1: Start at root, look for 'c'
    root → c ✓ (found)

Step 2: At 'c', look for 'a'
    c → a ✓ (found)

Step 3: At 'a', look for 'r'
    a → r ✓ (found)

Step 4: Check if 'r' is end of word
    r.is_end = True ✓

Result: "car" exists in trie

Search for "ca" (prefix but not word):
root → c → a → is_end = False ✗
Result: "ca" does not exist as complete word

Search for "can" (doesn't exist):
root → c → a → n (no child 'n') ✗
Result: "can" does not exist

Time Complexity: O(m) where m = length of word
```

### 3. StartsWith (Prefix Search)

```
Check if any word starts with "do":
    root
    └─ d
       └─ o
          ├─ g*
          └─ o
             └─ r*

Step 1: root → d ✓
Step 2: d → o ✓
Step 3: o exists

Result: Prefix "do" exists
Words: "dog", "door"

Visual representation:
Prefix "do":
    d → o → [g*, o → r*]
    ✓     Found these completions

Prefix "ca":
    c → a → [t*, r*]
    ✓     Found these completions

Time Complexity: O(m) where m = length of prefix
```

### 4. Delete Operation

```
Delete "car" from trie:

Before deletion:
    root
    └─ c
       └─ a
          ├─ t*
          └─ r*

Step 1: Traverse to 'r'
    root → c → a → r

Step 2: Unmark 'r' as end
    r.is_end = False

Step 3: Check if 'r' has children
    r has no children → can delete

Step 4: Backtrack and remove unused nodes
    'r' deleted
    'a' still needed (has child 't')

After deletion:
    root
    └─ c
       └─ a
          └─ t*

Delete "cat" (last word in branch):
    root → c → a → t
    t.is_end = False
    t has no children → delete t
    a has no children → delete a
    c has no children → delete c

After deletion:
    root (empty)

Time Complexity: O(m) where m = length of word
```

## Common Use Cases

### 1. Autocomplete System

```
Dictionary: ["apple", "application", "apply", "app"]

Trie structure:
    root
     └─ a
        └─ p
           └─ p*
              ├─ l
              │  ├─ y*
              │  └─ e*
              └─ i
                 └─ c
                    └─ a
                       └─ t
                          └─ i
                             └─ o
                                └─ n*

User types "app":
    root → a → p → p

Suggestions (DFS from 'p'):
    ├─ "" → "app"*
    ├─ "l" → "y" → "apply"*
    ├─ "l" → "e" → "apple"*
    └─ "l" → "i" → ... → "application"*

Result: ["app", "apple", "application", "apply"]
```

### 2. Word Search (Boggle)

```
Board:
    a b c
    d e f
    g h i

Dictionary: ["abc", "def", "bed"]

Build Trie from dictionary:
    root
    ├─ a → b → c*
    ├─ d → e → f*
    └─ b → e → d*

Search on board:
Starting at 'a':
    a → b → c (path exists in trie) ✓ "abc" found

Starting at 'd':
    d → e → f (path exists in trie) ✓ "def" found

Starting at 'b':
    b → e → d (path exists in trie) ✓ "bed" found
```

### 3. IP Routing (Longest Prefix Matching)

```
Routing table:
    192.168.1.0/24
    192.168.0.0/16
    192.0.0.0/8

Trie (binary representation):
    root
     └─ 1 (192)
        └─ 1
           └─ 0
              └─ 1
                 └─ 0
                    └─ 1
                       └─ 0
                          └─ 0
                             ├─ /24 route
                             └─ continue...

Lookup 192.168.1.5:
Find longest matching prefix → 192.168.1.0/24
```

### 4. Spell Checker

```
Dictionary: ["hello", "help", "hero"]

Trie:
    root
     └─ h
        └─ e
           ├─ l
           │  ├─ l → o*
           │  └─ p*
           └─ r
              └─ o*

Input: "helo" (typo)
Search: root → h → e → l → o
        'l' doesn't have child 'o' ✗

Suggestions (edit distance 1):
    - Insert: "hello", "helpo"
    - Delete: "heo"
    - Replace: "help", "hero"

Filter by trie: ["hello", "help", "hero"]
```

## Advanced Trie Variations

### 1. Compressed Trie (Radix Tree)

```
Regular Trie for "test", "testing", "tester":
    root
     └─ t
        └─ e
           └─ s
              └─ t*
                 ├─ e
                 │  └─ r*
                 └─ i
                    └─ n
                       └─ g*

Compressed Trie (merge single-child nodes):
    root
     └─ "test"*
            ├─ "er"*
            └─ "ing"*

Space savings: 9 nodes → 3 nodes
```

### 2. Ternary Search Tree

```
Each node has 3 children: left, middle, right
- Left: characters < current
- Middle: next character in word
- Right: characters > current

Insert "cat", "cut", "at":
        c
       /│\
      a c u
       │  │
       t* t*
      /
     a
      \
       t*

Properties:
- More space-efficient than array-based tries
- Combines BST and Trie properties
```

### 3. Suffix Trie

```
String: "banana"
Suffixes: "banana", "anana", "nana", "ana", "na", "a"

Trie:
    root
    ├─ b → a → n → a → n → a*
    ├─ a → n → a → n → a*
    │      └─ a*
    │          └─ (shared)
    └─ n → a → n → a*
           └─ a* (shared)

Used for:
- Pattern matching
- Finding all occurrences of substring
```

## Comparison with Other Data Structures

```
Operation comparison:

                Trie    HashMap   BST
Insert:         O(m)    O(1)      O(log n)
Search:         O(m)    O(1)      O(log n)
Prefix Search:  O(m)    O(n)      O(n)
Space:          O(m*n)  O(n)      O(n)
Sorted Order:   Yes     No        Yes

m = length of word
n = number of words

Trie advantages:
✓ Fast prefix searches
✓ No hash collisions
✓ Alphabetically ordered
✓ Common prefixes shared

Trie disadvantages:
✗ More space (especially sparse)
✗ Cache-unfriendly
✗ Complex implementation
```

## Memory Optimization Techniques

### 1. HashMap-based Children

```
Instead of array[26]:
┌─────────────────┐
│ children[26]    │ ← 26 * 8 bytes = 208 bytes
└─────────────────┘

Use HashMap:
┌─────────────────┐
│ children: {}    │ ← Only stores existing children
└─────────────────┘

Trade-off:
- Array: O(1) lookup, more space
- HashMap: O(1) average lookup, less space
```

### 2. Bit Representation

```
For small alphabets, use bit flags:

26 letters → 26 bits = 4 bytes

Node:
┌─────────────────┐
│ exists: 0b...   │ ← Bit i set if child i exists
│ children: []    │ ← Only non-null children
└─────────────────┘

Example:
exists = 0b...00101 (children at positions 0 and 2)
children = [node_a, node_c]
```

## Time and Space Complexity

### Time Complexity
| Operation | Complexity | Description |
|-----------|-----------|-------------|
| Insert    | O(m)      | m = word length |
| Search    | O(m)      | m = word length |
| Delete    | O(m)      | m = word length |
| StartsWith| O(m)      | m = prefix length |
| Autocomplete | O(p + n) | p = prefix length, n = suggestions |

### Space Complexity
| Case | Complexity | Description |
|------|-----------|-------------|
| Total | O(ALPHABET_SIZE * N * M) | Worst case |
| Average | O(N * M) | With shared prefixes |
| Per node (array) | O(ALPHABET_SIZE) | 26 for lowercase |
| Per node (HashMap) | O(k) | k = actual children |

```
Example space calculation:

Words: "cat", "car", "dog" (avg length = 3)

Array-based:
Nodes: c, a, t, r, d, o, g = 7 nodes
Space per node: 26 pointers + metadata ≈ 220 bytes
Total: 7 * 220 = 1,540 bytes

HashMap-based:
Same 7 nodes
Space per node: 1-2 pointers + metadata ≈ 30 bytes
Total: 7 * 30 = 210 bytes

Space saved: 86% reduction!
```

## Python Implementation

```python
class TrieNode:
    def __init__(self):
        self.children = {}  # HashMap-based for efficiency
        self.is_end_of_word = False
        # Optional: store word here for easier autocomplete
        self.word = None

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """
        Insert a word into the trie.
        Time: O(m), Space: O(m)
        """
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.word = word

    def search(self, word: str) -> bool:
        """
        Search for exact word match.
        Time: O(m), Space: O(1)
        """
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        """
        Check if any word starts with prefix.
        Time: O(m), Space: O(1)
        """
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

    def delete(self, word: str) -> bool:
        """
        Delete a word from trie.
        Time: O(m), Space: O(m) for recursion
        """
        def _delete(node, word, index):
            if index == len(word):
                if not node.is_end_of_word:
                    return False  # Word doesn't exist
                node.is_end_of_word = False
                return len(node.children) == 0

            char = word[index]
            if char not in node.children:
                return False

            child = node.children[char]
            should_delete = _delete(child, word, index + 1)

            if should_delete:
                del node.children[char]
                return len(node.children) == 0 and not node.is_end_of_word

            return False

        return _delete(self.root, word, 0)

    def autocomplete(self, prefix: str, max_results: int = 10) -> list:
        """
        Get all words with given prefix.
        Time: O(p + n), Space: O(n)
        """
        node = self.root
        # Navigate to prefix
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]

        # DFS to find all words
        results = []

        def dfs(node, path):
            if len(results) >= max_results:
                return

            if node.is_end_of_word:
                results.append(prefix + path)

            for char, child in sorted(node.children.items()):
                dfs(child, path + char)

        dfs(node, "")
        return results

    def longest_common_prefix(self) -> str:
        """
        Find longest common prefix of all words.
        Time: O(m), Space: O(1)
        """
        node = self.root
        prefix = ""

        while len(node.children) == 1 and not node.is_end_of_word:
            char, child = next(iter(node.children.items()))
            prefix += char
            node = child

        return prefix


# Usage examples
trie = Trie()

# Insert words
words = ["apple", "app", "application", "apply"]
for word in words:
    trie.insert(word)

# Search
print(trie.search("app"))      # True
print(trie.search("appl"))     # False

# Prefix search
print(trie.starts_with("app")) # True

# Autocomplete
print(trie.autocomplete("app"))
# ["app", "apple", "application", "apply"]

# Delete
trie.delete("app")
print(trie.search("app"))      # False
print(trie.search("apple"))    # True (not affected)


# Word Search II (Boggle) - Classic Trie Problem
class Solution:
    def findWords(self, board, words):
        """
        Find all words from list that exist on board.
        Time: O(m*n*4^L), Space: O(k)
        m*n = board size, L = max word length, k = total chars in words
        """
        # Build trie
        trie = Trie()
        for word in words:
            trie.insert(word)

        result = set()
        rows, cols = len(board), len(board[0])

        def dfs(r, c, node, path):
            if node.is_end_of_word:
                result.add(node.word)

            if r < 0 or r >= rows or c < 0 or c >= cols:
                return

            char = board[r][c]
            if char not in node.children:
                return

            # Mark visited
            board[r][c] = '#'

            # Explore neighbors
            for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
                dfs(r + dr, c + dc, node.children[char], path + char)

            # Unmark
            board[r][c] = char

        # Start DFS from each cell
        for r in range(rows):
            for c in range(cols):
                if board[r][c] in trie.root.children:
                    dfs(r, c, trie.root, "")

        return list(result)


# Design Add and Search Words Data Structure
class WordDictionary:
    def __init__(self):
        self.trie = Trie()

    def addWord(self, word: str) -> None:
        self.trie.insert(word)

    def search(self, word: str) -> bool:
        """
        Search word with '.' matching any character.
        Time: O(m) best case, O(26^m) worst case
        """
        def dfs(node, i):
            if i == len(word):
                return node.is_end_of_word

            char = word[i]
            if char == '.':
                # Try all possible children
                for child in node.children.values():
                    if dfs(child, i + 1):
                        return True
                return False
            else:
                if char not in node.children:
                    return False
                return dfs(node.children[char], i + 1)

        return dfs(self.trie.root, 0)
```

## Common Patterns and Problems

### 1. Word Dictionary with Wildcards
```
Pattern: Trie + DFS for wildcard matching

Problem: Support search with '.' matching any character
Solution: When encountering '.', try all children

Example:
Trie: ["bad", "dad", "mad"]
Search ".ad" → try all first chars → all match
Search "b.." → only "bad" matches
```

### 2. Maximum XOR Queries
```
Pattern: Binary Trie for bit manipulation

Problem: Find pair with maximum XOR
Solution: Build binary trie, greedily choose opposite bits

Example:
Numbers: [3, 10, 5, 25]
Binary:  [011, 1010, 0101, 11001]

Binary Trie:
    root
    ├─ 0 → 0 → 1 → 1 (3)
    │  └─ 1 → 0 → 1 (5)
    └─ 1 → 0 → 0 → 1 (10)
       └─ 1 → 0 → 0 → 1 (25)

Max XOR: 25 XOR 5 = 11001 XOR 00101 = 11100 = 28
```

### 3. Stream of Characters
```
Pattern: Suffix Trie

Problem: Check if suffix of stream matches any word
Solution: Insert reversed words, search reversed stream

Example:
Words: ["ab", "ba", "aaab"]
Reverse and insert: ["ba", "ab", "baaa"]

Stream: "aaaaabbb"
Check: "b", "bb", "bbb" against trie
```

## Key Takeaways

1. **Structure**: Tree with characters on edges/nodes, shared prefixes
2. **Best For**:
   - Prefix/suffix searches
   - Autocomplete systems
   - Spell checkers
   - IP routing
   - Word games (Boggle, Scrabble)

3. **Implementation Choices**:
   - Array: Fast but space-heavy
   - HashMap: Balanced approach
   - Ternary: Space-efficient

4. **Time Complexity**: O(m) for most operations (m = word length)
5. **Space Trade-off**: Uses more space for faster prefix operations

6. **Common Patterns**:
   - DFS for word collection
   - Backtracking for board games
   - Binary trie for bit manipulation
   - Reverse trie for suffix matching

7. **When to Use**:
   - Need fast prefix matching (vs HashMap: O(n))
   - Multiple words share prefixes
   - Ordered traversal needed
   - Autocomplete/search suggestions

8. **When NOT to Use**:
   - Simple exact-match lookups (use HashMap)
   - Memory-constrained (try compressed variants)
   - Very sparse data (few shared prefixes)
