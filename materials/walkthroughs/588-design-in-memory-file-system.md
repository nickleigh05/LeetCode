# 588. Design In-Memory File System

**Hard** · 🔒 Premium · [LeetCode](https://leetcode.com/problems/design-in-memory-file-system/) · [Solution file (no hints)](../../problems/0500-0999/588.py)

[📖 08. Tries lesson](../learning/08-tries.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 08. Tries problems](../rmap-practice/08-tries.md)

---

Design a data structure that simulates an in-memory file system. Implement the `FileSystem` class:

- `FileSystem()`: start with an empty root directory `"/"`.
- `ls(path)`: if `path` is a **file**, return a list containing just the file's name. If it's a **directory**, return the names of its files and subdirectories in **lexicographic order**.
- `mkdir(path)`: create the directory at `path`, creating any **missing parent directories** along the way.
- `addContentToFile(filePath, content)`: if the file doesn't exist, create it with `content`. If it exists, **append** `content`.
- `readContentFromFile(filePath)`: return the file's content.

```
fs = FileSystem()
fs.ls("/")                          →  []
fs.mkdir("/a/b/c")
fs.addContentToFile("/a/b/c/d", "hello")
fs.ls("/")                          →  ["a"]
fs.readContentFromFile("/a/b/c/d")  →  "hello"
fs.ls("/a/b/c/d")                   →  ["d"]       (a file: just its own name)
```

**Constraints:** paths are **absolute**, start with `/`, and don't end with `/` (except `"/"` itself) · names are lowercase letters · all operations are valid (you never read a missing file or `mkdir` over a file) · at most 300 calls

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| paths like `/a/b/c` | A **tree**. Each `/`-separated part is one level down |
| `mkdir` creates missing parents | Walking a path should **create nodes as needed**, like `mkdir -p` |
| `ls` on a **file** returns `[name]` | Each node needs to know whether it's a file or a directory |
| `ls` on a directory is **sorted** | Sort the child names when listing |
| append on repeated writes | A file holds a string that grows |

**This is a trie, with path parts instead of characters.** A [Trie](208-implement-trie-prefix-tree.md) stores words one **character** per level. Here you store paths one **directory name** per level:

```
       (root)
         │
         a
         │
         b
         │
         c
         │
         d   ← file, content "hello"
```

Every operation starts the same way: **walk** the path from the root, one part at a time. So write that walk once, as a helper, and have it **create missing nodes** as it goes. That one helper does `mkdir`'s job directly and gives every other operation the node it needs.

**Telling files from directories.** Give each node a `content` field: `None` for a directory, a string for a file. A file created with empty content `""` is still a file, because `""` is not `None`. Checking `is not None` rather than truthiness gets that edge case right.

🤔 **Before you open the next section:** `"/a/b".split('/')` gives `['', 'a', 'b']`. What does `"/".split('/')` give, and how should the walk handle the empty strings?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Per operation | Verdict |
|---|---|---|---|
| Flat dict of full paths | `{"/a/b/c/d": "hello", …}` | `ls` must scan every key | ❌ `ls` is O(total paths) |
| **Trie of path parts** | Each node: `children` dict + `content` | O(path length) to walk, plus a sort for `ls` | ✅ |
| Trie with sorted children | Keep children in a sorted structure | Faster `ls`, slower inserts | ⚠️ Overkill at 300 calls |

**The decision: a [trie](../data-structures/trie.md) whose nodes are plain dicts.**

Each node is `{'children': {name: node}, 'content': None or str}`. The [hash map](../data-structures/hashmap.md) of children gives O(1) steps down the tree, and sorting only happens on `ls`.

**Why a node class or dict instead of nested dicts of names?** A bare nested dict (`{'a': {'b': {}}}`) has nowhere to put a file's content without mixing it in with child names. A separate `content` field keeps "what's inside" apart from "what's below."

**One walk helper serves all four methods.** `_walk(path)` splits the path, skips empty parts (from the leading `/`), creates missing children, and returns the final node. `mkdir` is just a walk. `addContentToFile` walks and then appends. `readContentFromFile` walks and reads. `ls` walks and then either names the file or sorts the children.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
def __init__(self):
    self.root = {'children': {}, 'content': None}
```

The root directory. `content` is `None`, which marks a directory.
→ [init-method](../syntax/init-method.md) · [dict-basics](../syntax/dict-basics.md)

```python
def _walk(self, path):
    node = self.root
    for part in path.split('/'):
        if part == '':
            continue
```

**Split the path into parts.** `"/a/b".split('/')` is `['', 'a', 'b']`, and `"/"` gives `['', '']`. Skipping empty strings handles the leading slash and the root itself. The leading underscore marks `_walk` as an internal helper.
→ [string-methods](../syntax/string-methods.md) · [break-continue](../syntax/break-continue.md) · [function-basics](../syntax/function-basics.md)

```python
        if part not in node['children']:
            node['children'][part] = {'children': {}, 'content': None}
        node = node['children'][part]
    return node
```

**Step down, creating as you go.** A missing part becomes a new empty directory. This is the `mkdir -p` behaviour, and it's why `mkdir` needs no code of its own. Return the node at the end of the path.
→ [membership-operators](../syntax/membership-operators.md)

```python
def ls(self, path: str) -> List[str]:
    node = self._walk(path)
    if node['content'] is not None:
        return [path.split('/')[-1]]
    return sorted(node['children'])
```

**List a path.**
- A **file** (content is not `None`): return just its own name, the last part of the path.
- A **directory**: return its child names, sorted. `sorted(dict)` sorts the keys.

`is not None` (rather than `if node['content']`) keeps an empty file `""` counted as a file.
→ [identity-operators](../syntax/identity-operators.md) · [sorting-key](../syntax/sorting-key.md) · [list-slicing](../syntax/list-slicing.md)

```python
def mkdir(self, path: str) -> None:
    self._walk(path)
```

The walk creates every missing directory, so `mkdir` is one line.

```python
def addContentToFile(self, filePath: str, content: str) -> None:
    node = self._walk(filePath)
    if node['content'] is None:
        node['content'] = ''
    node['content'] += content
```

**Create or append.** The walk creates the file's node if needed, as a directory-shaped node. Setting `content` to `''` turns it into a file, and then the new text is appended.
→ [string-basics](../syntax/string-basics.md)

```python
def readContentFromFile(self, filePath: str) -> str:
    return self._walk(filePath)['content']
```

Walk to the file and return its content. The problem guarantees the file exists.

<details>
<summary>The whole thing together</summary>

```python
class FileSystem:

    def __init__(self):
        self.root = {'children': {}, 'content': None}

    def _walk(self, path):
        node = self.root
        for part in path.split('/'):
            if part == '':
                continue
            if part not in node['children']:
                node['children'][part] = {'children': {}, 'content': None}
            node = node['children'][part]
        return node

    def ls(self, path: str) -> List[str]:
        node = self._walk(path)
        if node['content'] is not None:
            return [path.split('/')[-1]]
        return sorted(node['children'])

    def mkdir(self, path: str) -> None:
        self._walk(path)

    def addContentToFile(self, filePath: str, content: str) -> None:
        node = self._walk(filePath)
        if node['content'] is None:
            node['content'] = ''
        node['content'] += content

    def readContentFromFile(self, filePath: str) -> str:
        return self._walk(filePath)['content']
```

</details>

**Trace it.** The example:

| Call | Walk | Effect | Returns |
|---|---|---|---|
| `ls("/")` | root | directory with no children | `[]` |
| `mkdir("/a/b/c")` | creates a → b → c | three directories | |
| `addContentToFile("/a/b/c/d", "hello")` | a → b → c → creates d | d.content = `"hello"` | |
| `ls("/")` | root | children `{a}` | `["a"]` |
| `readContentFromFile("/a/b/c/d")` | a → b → c → d | | `"hello"` |
| `ls("/a/b/c/d")` | d | d is a file | `["d"]` ✅ |

</details>

<details>
<summary><b>4 · Time complexity</b> — O(L) per call, plus O(k log k) for `ls`</summary>

Let L be the length of the path string and k the number of entries in a directory.

- **Walking:** O(L) to split the path, plus O(1) per part to step down.
- **`mkdir`**, **`readContentFromFile`:** O(L).
- **`addContentToFile`:** O(L + c), where c is the content length. Python strings are immutable, so `+=` builds a new string, which is O(existing + new) in general.
- **`ls`** on a directory: O(L + k log k) for the sort.

At 300 calls, all of this is trivial. Keeping each directory's children in a sorted structure (or caching the sorted list) would speed up repeated `ls` calls.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(total path parts + total content)</summary>

One node per distinct path part ever created, plus the stored file contents. That's proportional to everything the user has created, which is the minimum any file system needs to remember.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Paths form a tree, so I'll use a trie keyed by path parts instead of characters. Each node has a children dict and a content field, which is None for a directory and a string for a file. One helper walks a path from the root, skipping empty parts from the leading slash and creating missing nodes. That gives mkdir for free. addContentToFile walks, makes the node a file if it isn't one, and appends. readContent walks and returns. ls walks, and returns the file's own name for a file or the sorted child names for a directory. Each walk is O(path length), with an extra sort for ls."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Faster `ls` on big directories?" | Keep children in a sorted container, such as `SortedDict` from `sortedcontainers`, or cache the sorted list and invalidate it on insert. |
| "Delete a file or directory?" | Walk to the parent and remove the child. Deleting a directory removes its whole subtree automatically. |
| "Move or rename?" | Detach the node from its old parent and attach it under the new name. O(path length), with no copying. |
| "Large appends?" | Store content as a list of chunks and join on read, avoiding repeated string copying. |
| "Wildcard search like `ls /a/*/c`?" | A trie DFS that branches at `*`, like [Design Add and Search Words](211-design-add-and-search-words-data-structure.md). |

**Traps:**

- **Not skipping empty parts.** `"/a".split('/')` starts with `''`, which would create a nameless child.
- **`if node['content']:` to detect files.** An empty file `""` is falsy and would be treated as a directory.
- **Returning the full path from `ls` on a file.** It should be just the name, `["d"]`.
- **Unsorted `ls` output.** Dict order is insertion order, not alphabetical.
- **A flat dict of full paths.** `ls` then has to scan every path to find a directory's children.

**This same move shows up in:** [Implement Trie (Prefix Tree)](208-implement-trie-prefix-tree.md) (the same walk-and-create structure, per character) · [Design Add and Search Words](211-design-add-and-search-words-data-structure.md) (a trie walk with branching) · [Simplify Path](71-simplify-path.md) (splitting a Unix path on `/` and handling the parts) · [Map Sum Pairs](677-map-sum-pairs.md) (a trie with extra data stored on each node).

</details>

---
