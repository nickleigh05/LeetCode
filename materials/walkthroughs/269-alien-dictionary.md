# 269. Alien Dictionary

**Hard** · [LeetCode](https://leetcode.com/problems/alien-dictionary/)

[📖 13. Advanced Graphs lesson](../learning/13-advanced-graphs.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 13. Advanced Graphs problems](../rmap-practice/13-advanced-graphs.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

There is a new alien language that uses the English alphabet, but the **order of the letters is unknown**. You're given a list of `words` from the alien dictionary, sorted **lexicographically by that unknown order**. Return a string of the unique letters in the correct order. If the ordering is invalid, return `""`. If several orderings are valid, return any of them.

```
words = ["wrt","wrf","er","ett","rftt"]  →  "wertf"
        wrt < wrf ⟹ t < f
        wrf < er  ⟹ w < e
        er  < ett ⟹ r < t
        ett < rftt⟹ e < r

words = ["z","x"]                        →  "zx"

words = ["z","x","z"]                    →  ""   (z < x and x < z — a cycle)

words = ["abc","ab"]                     →  ""   (a prefix can never sort after its own extension)
```

**Constraints:** `1 <= words.length <= 100` · `1 <= words[i].length <= 100` · lowercase English letters only.

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "the order of letters is unknown" | The **output** is an ordering. That word alone should put topological sort on your list of candidates |
| "words are sorted by that order" | The input is not data — it's **evidence**. Each adjacent pair of words constrains which letter comes first |
| "return **any** valid ordering" | Multiple answers are acceptable, which is the signature of a topological sort (a DAG usually has many valid linearizations). If a *unique* answer were demanded, you'd need extra checks |
| "return `""` if invalid" | Two failure modes to find. One is a **cycle** in the constraints; the other is hinted at by example 4 |
| lowercase letters only | At most 26 nodes. The graph is tiny regardless of input size |

The recognition step: *"I have pairwise ordering constraints and I need a total order consistent with all of them"* is **exactly** the job description of a [topological sort](../algorithms/topological-sort.md). Same as [Course Schedule II](210-course-schedule-ii.md), just with letters instead of courses.

The real work is **extracting the edges.** How does word-sorting tell you about letter order? Compare two adjacent words character by character. Everything matching tells you nothing. The **first position where they differ** is the one that decided their order — so if `wrt` comes before `wrf`, then `t < f`. And once you've found that first difference, **every later character is irrelevant** and you must stop: `wrt` vs `wrf` says nothing about `r` vs `f`.

That's one edge per adjacent pair, at most. Not one per differing character.

🤔 **Before you open the next section:** example 4 is `["abc","ab"]`, and it returns `""` without any cycle. What's wrong with it? What does real dictionary ordering say about a word and a word that starts with it?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Try all 26! permutations | Test each against the word list | O(26!) | — | ❌ |
| Sort with a custom comparator | Define "less than" from the pairs and sort the letters | — | — | ❌ The relation is **partial**, not total. Most letter pairs have no evidence at all, so there's nothing for a comparator to return |
| DFS topological sort | Post-order DFS, reverse the result; detect cycles with a three-colour visit state | O(C + V + E) | O(V + E) | ✅ Correct, but cycle detection needs the extra "in progress" state |
| **BFS topological sort (Kahn's)** | Repeatedly emit a node with in-degree 0, decrement its neighbours | O(C + V + E) | O(V + E) | ✅ |

**The decision:** [Kahn's algorithm](../algorithms/topological-sort.md) — BFS topological sort — over a graph whose nodes are letters and whose edges are `earlier → later`.

**Why Kahn's over DFS here?** Cycle detection comes free. In DFS you need a three-state colouring (unvisited / in-progress / done) and you have to remember that hitting an *in-progress* node means a cycle. In Kahn's, you just count: if the emitted order is shorter than the node count, some nodes never reached in-degree 0, which happens **exactly** when they're stuck in a cycle. One comparison at the end, and it's the same check you'd write for [Course Schedule](207-course-schedule.md).

**The two failure modes, and why only one is a cycle.**

1. **Cycle** — `["z","x","z"]` gives `z < x` and `x < z`. No ordering satisfies both. Kahn's catches this via the length check.
2. **Invalid prefix** — `["abc","ab"]`. In *any* lexicographic order, a prefix sorts **before** the word that extends it, because it runs out of characters first. So a longer word appearing before its own prefix is impossible regardless of the alphabet. This produces **no edge at all** (the character loop finds no difference), so it's invisible to the graph — you must check it explicitly. **This is the case that separates people who've thought about the problem from people who've pattern-matched it to Course Schedule.**

**Why the node set is "every letter that appears," not just letters with edges.** A letter can appear in the words yet be in no constraint at all — it still must show up in the output. Seeding the graph from every character of every word handles this, and lets those letters emit immediately at in-degree 0.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
from collections import deque
```
Kahn's needs a queue of zero-in-degree nodes. A [deque](../data-structures/deque.md) gives O(1) `popleft`; a plain list's `pop(0)` is O(n).
→ [deque](../data-structures/deque.md) · [from-import](../syntax/from-import.md)

```python
graph = {char: set() for word in words for char in word}
```
Seed the node set from **every character that appears anywhere** — a nested [dict comprehension](../syntax/dict-comprehension.md) doing double duty as "collect all letters" and "give each an empty adjacency set."

A `set` rather than a `list` for the neighbours, deliberately: the same constraint can be derived from several word pairs, and duplicate edges would corrupt the in-degree counts — a node's counter would be decremented fewer times than it was incremented, and it'd never reach zero. **The `set` is load-bearing, not stylistic.**
→ [dict-comprehension](../syntax/dict-comprehension.md) · [set-basics](../syntax/set-basics.md)

```python
for w1, w2 in zip(words, words[1:]):
```
The classic **adjacent-pairs** idiom: [`zip`](../syntax/zip-function.md) a list against itself offset by one, yielding `(words[0], words[1])`, `(words[1], words[2])`, … `zip` stops at the shorter list, so no bounds check is needed.

Only *adjacent* pairs matter. Non-adjacent pairs carry no information the adjacent ones don't already imply, transitively.
→ [zip-function](../syntax/zip-function.md) · [list-slicing](../syntax/list-slicing.md)

```python
    min_len = min(len(w1), len(w2))
    if w1[:min_len] == w2[:min_len] and len(w1) > len(w2):
        return ""
```
**The prefix check** — the case the graph can't see. If everything up to the shorter length matches and `w1` is the longer one, then a word has been placed before its own prefix. That's impossible in any lexicographic ordering, so the input is invalid: bail immediately.

This must come **before** the edge extraction, and it must return rather than merely skip.
→ [min-max-key](../syntax/min-max-key.md) · [string-join-slice](../syntax/string-join-slice.md) · [if-return](../syntax/if-return.md)

```python
    for c1, c2 in zip(w1, w2):
        if c1 != c2:
            graph[c1].add(c2)
            break
```
Edge extraction. Walk the two words in lockstep and stop at the **first** mismatch — that's the position that determined the sort order, giving `c1 → c2`.

The `break` is essential. Without it you'd add an edge for every differing position, inventing constraints the input never justified, and almost certainly manufacturing a false cycle.
→ [break-continue](../syntax/break-continue.md) · [comparison-operators](../syntax/comparison-operators.md) · [graph](../data-structures/graph.md)

```python
indegree = {char: 0 for char in graph}
for char in graph:
    for neighbor in graph[char]:
        indegree[neighbor] += 1
```
Count incoming edges per letter. In-degree is "how many letters must be placed before this one" — a node is ready to emit precisely when that count hits zero.

Initializing from `graph`'s keys (not from the edges) ensures constraint-free letters start at 0 and get emitted.
→ [dict-comprehension](../syntax/dict-comprehension.md) · [dict-methods](../syntax/dict-methods.md)

```python
queue = deque([char for char in graph if indegree[char] == 0])
order = []
```
Seed the queue with everything that has nothing before it. If this comes back **empty** on a non-empty graph, every letter is in a cycle — the length check at the end will catch it.
→ [list-comprehension](../syntax/list-comprehension.md) · [queue](../data-structures/queue.md)

```python
while queue:
    char = queue.popleft()
    order.append(char)
    for neighbor in graph[char]:
        indegree[neighbor] -= 1
        if indegree[neighbor] == 0:
            queue.append(neighbor)
```
Kahn's loop. Emit a ready letter, then "remove" it from the graph by decrementing each neighbour's in-degree. Any neighbour that drops to **exactly** zero has had all its prerequisites emitted, so it becomes ready.

Testing `== 0` rather than `<= 0` means each node is enqueued exactly once.
→ [while-loop](../syntax/while-loop.md) · [deque-basics](../syntax/deque-basics.md) · [topological-sort](../algorithms/topological-sort.md)

```python
return "".join(order) if len(order) == len(graph) else ""
```
The cycle check and the answer in one line. Every letter emitted ⟹ a valid total order, so join it. Anything short ⟹ the leftovers never hit in-degree 0, which can only happen inside a cycle ⟹ `""`.
→ [string-join-slice](../syntax/string-join-slice.md) · [ternary-expression](../syntax/ternary-expression.md)

<details>
<summary>The whole thing together</summary>

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
</details>

**Trace it** — `words = ["wrt","wrf","er","ett","rftt"]`

Letters: `{w, r, t, f, e}`. Edges from adjacent pairs:

| Pair | First mismatch | Edge |
|---|---|---|
| `wrt`, `wrf` | position 2: `t` vs `f` | `t → f` |
| `wrf`, `er` | position 0: `w` vs `e` | `w → e` |
| `er`, `ett` | position 1: `r` vs `t` | `r → t` |
| `ett`, `rftt` | position 0: `e` vs `r` | `e → r` |

In-degrees: `w:0, e:1, r:1, t:1, f:1`

| Queue before | Emit | Decrement | `order` |
|---|---|---|---|
| `[w]` | `w` | `e → 0`, enqueue | `w` |
| `[e]` | `e` | `r → 0`, enqueue | `we` |
| `[r]` | `r` | `t → 0`, enqueue | `wer` |
| `[t]` | `t` | `f → 0`, enqueue | `wert` |
| `[f]` | `f` | — | `wertf` |

`len(order) == 5 == len(graph)` ✅ → **`"wertf"`** ✅

Now `["z","x","z"]`: edges `z → x` and `x → z`. In-degrees are `z:1, x:1`, so the initial queue is **empty**, `order` is `""`, and `0 != 2` → **`""`** ✅

And `["abc","ab"]`: `min_len = 2`, `"ab" == "ab"`, and `len("abc") > len("ab")` → returns **`""`** on the prefix check, before the graph is ever consulted ✅

</details>

<details>
<summary><b>4 · Time complexity</b> — O(C + V + E)</summary>

**O(C)**, where C is the total number of characters across all words — this dominates in practice.

Broken down:

- Building the node set: touches every character once → **O(C)**.
- Extracting edges: one pass over each adjacent pair, comparing at most `min_len` characters → **O(C)** total.
- Building in-degrees: **O(V + E)**.
- Kahn's loop: each node dequeued once, each edge traversed once → **O(V + E)**.

Now the useful observation: **V ≤ 26** and **E ≤ 26 × 25 = 650**, both constants. So the graph half is technically **O(1)**, and the honest total is **O(C)**.

Saying "O(C + V + E), and since the alphabet is bounded at 26 that's really just O(C)" is the answer that shows you read the constraints instead of reciting a template.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(V + E) = O(1)</summary>

**O(1)** — genuinely constant, because everything is bounded by the 26-letter alphabet.

- `graph`: at most 26 keys, each with at most 25 neighbours → ≤ 650 entries.
- `indegree`: at most 26 entries.
- `queue` and `order`: at most 26 each.
- `w1[:min_len]` in the prefix check creates temporary slices — **O(L)** for the longest word, and the one place a transient allocation happens.

So it's O(V + E) in general form, which collapses to **O(1)** given a fixed alphabet. The input itself is O(C) but that's given, not allocated.

**The nitpick worth pre-empting:** the prefix check slices both strings, which is O(L) work and O(L) space per pair. You can avoid it with a direct comparison inside the character loop (use a `for`/`else`, or a flag), making the space truly O(1). Nobody will mind either way — but noticing it is a good sign.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The words being sorted is evidence, not data. For each adjacent pair, the first position where they differ tells me one letter precedes another — and I have to stop at that first difference, because everything after it is uninformative. That gives me a directed graph over at most 26 letters, and I need a total order consistent with every edge: a topological sort. I use Kahn's, because the cycle check falls out for free — if I emit fewer letters than I have, the rest are stuck in a cycle. There's a second failure mode the graph can't see: a word appearing before its own prefix, like `abc` then `ab`. That's impossible in any lexicographic order and produces no edge, so I check it explicitly. O(C) time where C is the total character count; the graph itself is O(1) since the alphabet is bounded."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Is the answer unique?" | Only if at every step the queue holds exactly one letter. If it ever holds two or more, the order is ambiguous and multiple valid alphabets exist. Track `len(queue) > 1` to detect it. |
| "Do it with DFS." | Post-order DFS with three states: unvisited, in-progress, done. Hitting an in-progress node means a cycle → return `""`. Append each node after its neighbours, then reverse. Same complexity; the cycle logic is just more manual. |
| "Why compare only adjacent words?" | Non-adjacent pairs add nothing. If `a < b < c`, the edges `a→b` and `b→c` already imply `a→c` transitively. Comparing all pairs would be O(n²) for zero extra information. |
| "Why a `set` for neighbours instead of a list?" | Duplicate edges would inflate in-degree counts, and the decrements wouldn't match — the node would never reach 0, and you'd report a false cycle. |
| "What if some letters never appear in any constraint?" | They start at in-degree 0 and get emitted immediately, in whatever position the queue reaches them. Any placement is valid, since nothing constrains them. |
| "What if the alphabet weren't 26 letters?" | The complexity would properly be O(C + V + E). Nothing about the algorithm changes — only the claim that V and E are constants. |
| "What if `words` has one word?" | No adjacent pairs, so no edges. Every distinct letter has in-degree 0 and gets emitted in arbitrary order. Correct — one word constrains nothing. |

**Traps:**
- **Missing the prefix case.** The single most-failed test on this problem. `["abc","ab"]` must be `""`, and no cycle exists to catch it.
- **Forgetting the `break`** after the first mismatch. Adds unjustified edges and typically fabricates a cycle.
- Seeding the graph only from letters that appear in edges — letters with no constraints vanish from the output.
- Using a `list` for neighbours, corrupting in-degrees via duplicate edges.
- Returning `order` without the length check — you'd emit a partial, invalid alphabet on cyclic input.
- Assuming the alien alphabet uses all 26 letters. Only the letters present in `words` belong in the output.

**This same move shows up in:** [Course Schedule](207-course-schedule.md) (the same in-degree cycle detection, answering yes/no) · [Course Schedule II](210-course-schedule-ii.md) (the same algorithm, keeping the order — this problem is that one plus edge extraction) · [Reconstruct Itinerary](332-reconstruct-itinerary.md) (a different ordering problem over a directed graph) · [Graph Valid Tree](261-graph-valid-tree.md) (structural validation of a graph).

</details>

---
