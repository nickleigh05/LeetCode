# 269. Alien Dictionary

**Hard** · [LeetCode](https://leetcode.com/problems/alien-dictionary/)

[📖 12. Advanced Graphs lesson](../learning/13-advanced-graphs.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 12. Advanced Graphs problems](../rmap-practice/12-advanced-graphs.md)

---

Solution: not yet solved in this repo.

Given words sorted according to an unknown alien alphabet, derive a valid character ordering. Why does comparing each pair of adjacent words letter-by-letter give you edges for a character-ordering graph, and why does a topological sort turn that into an alphabet?

<details>
<summary>Hint</summary>

For each pair of adjacent words, find the first differing character — that gives an edge `earlier_char -> later_char`. Build this graph over all 26 possible letters, then run a [topological sort](../algorithms/topological-sort.md); a cycle (or word being a prefix of an earlier word incorrectly) means no valid ordering exists.
</details>

<details>
<summary>Solution</summary>

```python
from collections import deque

class Solution:
    def alienOrder(self, words: List[str]) -> str:

        graph = {char: set() for word in words for char in word}

        for w1, w2 in zip(words, words[1:]):
            min_len = min(len(w1), len(w2))
            if w1[:min_len] == w2[:min_len] and len(w1) > len(w2):
                return ""
            for c1, c2 in zip(w1, w2):
                if c1 != c2:
                    graph[c1].add(c2)
                    break

        indegree = {char: 0 for char in graph}
        for char in graph:
            for neighbor in graph[char]:
                indegree[neighbor] += 1

        queue = deque([char for char in graph if indegree[char] == 0])
        order = []

        while queue:
            char = queue.popleft()
            order.append(char)
            for neighbor in graph[char]:
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    queue.append(neighbor)

        return "".join(order) if len(order) == len(graph) else ""
```

Building blocks: [dict-comprehension](../syntax/dict-comprehension.md) · [zip-function](../syntax/zip-function.md) · [deque](../data-structures/deque.md) · [while-loop](../syntax/while-loop.md)
</details>

<details>
<summary>Time & space complexity</summary>

**Time: O(C)** — C is the total length of all words (building edges), plus O(V + E) for the topological sort over the alphabet.
**Space: O(1)** — bounded by 26 letters for the graph and indegree map.
</details>

---
