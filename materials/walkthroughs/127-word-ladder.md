# 127. Word Ladder

**Hard** · [LeetCode](https://leetcode.com/problems/word-ladder/)

[📖 11. Graphs lesson](../learning/11-graphs.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 11. Graphs problems](../rmap-practice/11-graphs.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

A **transformation sequence** from `beginWord` to `endWord` using `wordList` is a sequence `beginWord → s₁ → s₂ → … → endWord` such that:

- Every adjacent pair differs by **exactly one letter**.
- Every `sᵢ` (for `1 <= i <= k`) is in `wordList`. Note `beginWord` need **not** be.

Return the **number of words** in the shortest such sequence, or `0` if none exists.

```
beginWord = "hit", endWord = "cog"
wordList  = ["hot","dot","dog","lot","log","cog"]

  →  5      hit → hot → dot → dog → cog     (5 words, 4 changes)

wordList = ["hot","dot","dog","lot","log"]   →  0     ("cog" isn't available)
```

**Constraints:** `1 <= beginWord.length <= 10` · `1 <= wordList.length <= 5000` · all words the **same length**, lowercase, and **unique**

> **Try it yourself first.** This is the unit's hardest problem — the sections build up carefully.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**shortest** sequence" | ⚠️ A shortest-path question → **BFS**, not DFS |
| "differ by exactly **one letter**" | The adjacency rule — this defines the graph's edges |
| "number of **words**", not changes | ⚠️ `hit → hot → … → cog` has 4 changes but **5 words**. Off-by-one risk |
| `beginWord` need not be in the list | But `endWord` **must** be, or no sequence exists |
| all words the same length | Every transformation preserves length |
| up to 5000 words, length ≤ 10 | Building all pairwise edges would be 5000² = 2.5 × 10⁷ comparisons |

**The reframe: this is a graph problem in disguise.** There's no graph in the input — just a list of strings. But:

- **Each word is a node.**
- **Two words share an edge** if they differ by exactly one letter.

Then "shortest transformation sequence" is literally "shortest path from `beginWord` to `endWord`", and the answer is the number of nodes on that path.

**Why BFS.** Shortest path in an *unweighted* graph is precisely what BFS computes — it explores in order of distance, so **the first time you reach `endWord`, you've reached it by the shortest route**. DFS would find *a* path, not the shortest.

**The efficiency question: how do you find a word's neighbours?**

The obvious way — compare every word against every other — is O(n²·L) = 2.5 × 10⁷ × 10 comparisons just to build the graph.

**The better way: generate candidates instead of searching for them.** For a word of length L, try replacing each position with each of the 26 letters:

```
"hot"  →  aot bot cot ... zot     (26 candidates for position 0)
          hat hbt hct ... hzt     (26 for position 1)
          hoa hob hoc ... hoz     (26 for position 2)

          = L × 26 = 78 candidates, each checked against a set in O(1)
```

**That's O(L·26) per word instead of O(n·L)** — a huge win when n = 5000 and L = 10. **Generating the neighbourhood beats searching it.**

🤔 **Before you open the next section:** the sequence `hit → hot → dot → dog → cog` has 4 changes. What should `beginWord` be initialized to so the returned count is 5?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Verdict |
|---|---|---|
| DFS exploring all paths | Try every sequence, keep the shortest | ❌ Exponential; DFS doesn't give shortest paths |
| Build the full adjacency list, then BFS | Compare all word pairs first | ⚠️ Correct, but O(n²·L) to build |
| **BFS generating neighbours on the fly** | Try all L×26 single-letter changes | ✅ |
| **Bidirectional BFS** | Search from both ends, meet in the middle | ✅ The optimization |

**The decision: [BFS](../algorithms/bfs.md) from `beginWord`, generating candidate neighbours by brute-forcing single-letter substitutions.**

Three mechanisms:

| Mechanism | Purpose |
|---|---|
| `word_set` from `wordList` | O(1) "is this a real word?" checks |
| `(word, steps)` in the queue | Each node carries its own distance |
| `visited` set | Prevents revisiting and infinite loops |

**Why carry `steps` in the queue rather than snapshotting levels.** Both work. Storing the distance with each node — as in [Walls and Gates](286-walls-and-gates.md) — means no level bookkeeping; the alternative is the queue-size snapshot from [Binary Tree Level Order Traversal](102-binary-tree-level-order-traversal.md). **Pick either; carrying the value is simpler when the "distance" is what you return.**

**Why `beginWord` starts at 1.** The answer counts *words*, not transformations. `hit` alone is a sequence of length 1, so starting at 1 makes the final count come out right — `hit(1) → hot(2) → dot(3) → dog(4) → cog(5)` ✅

**Why marking on *enqueue* matters.** A word is added to `visited` the moment it's queued, not when dequeued. If you marked on dequeue, the same word could be enqueued many times by different neighbours at the same level — blowing up the queue for no benefit. **Mark when you commit to visiting, not when you get there.**

**Why the early `endWord` check.** If `endWord` isn't in `wordList`, no sequence can exist — an O(1) exit before any work.

**Bidirectional BFS is the standard optimization**, worth naming: search from both ends simultaneously and stop when the frontiers meet. Since BFS frontiers grow exponentially with depth, searching two half-depth trees is dramatically cheaper than one full-depth tree — roughly **O(b^(d/2))** instead of O(b^d).

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
word_set = set(wordList)
if endWord not in word_set:
    return 0
```

**Convert the list to a set** for O(1) membership — you'll do L×26 lookups per word, so a list's O(n) `in` would be crippling.

The guard is a free O(1) exit: if `endWord` isn't available, no sequence exists.
→ [set-basics](../syntax/set-basics.md) · [membership-operators](../syntax/membership-operators.md) · [if-return](../syntax/if-return.md)

```python
queue = deque([(beginWord, 1)])
visited = {beginWord}
```

**Each queue entry carries its own distance**, so no level snapshot is needed.

**Starting at `1`** because the answer counts words: `beginWord` alone is a one-word sequence.

`visited` starts containing `beginWord` so the search can't loop back to it.
→ [deque](../data-structures/deque.md) · [from-import](../syntax/from-import.md) · [tuple-basics](../syntax/tuple-basics.md)

```python
while queue:
    word, steps = queue.popleft()
    if word == endWord:
        return steps
```

**Standard BFS**, checking for the target on dequeue.

Because BFS expands in distance order, **the first time `endWord` is dequeued it's via the shortest path** — so returning immediately is correct.
→ [while-loop](../syntax/while-loop.md) · [tuple-unpacking](../syntax/tuple-unpacking.md)

```python
    for i in range(len(word)):
        for letter in ascii_lowercase:
            candidate = word[:i] + letter + word[i + 1:]
```

**Generate every single-letter variation** — L positions × 26 letters.

`word[:i] + letter + word[i+1:]` rebuilds the word with position `i` replaced. Note this also produces `word` itself when `letter` matches the original, which is harmless — it's already in `visited`.

**This is the efficiency trick:** generating 26L candidates and testing each in O(1) beats comparing against all n words.
→ [string-join-slice](../syntax/string-join-slice.md) · [list-slicing](../syntax/list-slicing.md) · [string-module-constants](../syntax/string-module-constants.md) · [for-loop](../syntax/for-loop.md)

```python
            if candidate in word_set and candidate not in visited:
                visited.add(candidate)
                queue.append((candidate, steps + 1))
```

**Two checks:** the candidate must be a real word, and not already visited.

**Marking on enqueue** — not on dequeue — prevents the same word being queued multiple times by different neighbours at the same level.

`steps + 1` because reaching this word adds one more to the sequence.
→ [set-operations](../syntax/set-operations.md) · [logical-operators](../syntax/logical-operators.md)

```python
return 0
```

The queue emptied without reaching `endWord` — no transformation sequence exists.

<details>
<summary>The whole thing together</summary>

```python
from collections import deque
from string import ascii_lowercase

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:

        word_set = set(wordList)
        if endWord not in word_set:
            return 0

        queue = deque([(beginWord, 1)])
        visited = {beginWord}

        while queue:
            word, steps = queue.popleft()
            if word == endWord:
                return steps

            for i in range(len(word)):
                for letter in ascii_lowercase:
                    candidate = word[:i] + letter + word[i + 1:]
                    if candidate in word_set and candidate not in visited:
                        visited.add(candidate)
                        queue.append((candidate, steps + 1))

        return 0
```

</details>

**Trace it** — `beginWord = "hit"`, `endWord = "cog"`, `wordList = ["hot","dot","dog","lot","log","cog"]`:

| Dequeue | `steps` | Valid new candidates | Enqueued |
|---|---|---|---|
| `hit` | 1 | `hot` (from `h_t` → `hot`) | `(hot, 2)` |
| `hot` | 2 | `dot`, `lot` | `(dot,3)`, `(lot,3)` |
| `dot` | 3 | `dog` | `(dog,4)` |
| `lot` | 3 | `log` | `(log,4)` |
| `dog` | 4 | `cog` | `(cog,5)` |
| `log` | 4 | `cog` already visited | — |
| **`cog`** | **5** | — | **return 5** ✅ |

The path is `hit → hot → dot → dog → cog` — **5 words**, 4 transformations ✅

**Two things worth noticing:**

- **`dog` and `log` both connect to `cog`**, but `cog` was marked visited when `dog` enqueued it. Marking on enqueue meant `log` didn't queue a duplicate.
- **The answer came out as 5, not 4**, because `beginWord` started at 1 rather than 0.

**And the failure case** — with `wordList = ["hot","dot","dog","lot","log"]`, the guard fires immediately: `cog` isn't in the set → **return 0** ✅

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n · L² · 26)</summary>

**O(n · L² · 26)**, where n = number of words and L = word length.

| Per word dequeued | Cost |
|---|---|
| Positions to try | L |
| Letters per position | 26 |
| Building each candidate | **O(L)** — string slicing and concatenation |
| Set lookup | O(L) to hash the string |

So **O(L × 26 × L) = O(26·L²)** per word, across at most n words → **O(n · L² · 26)**.

With n = 5000 and L = 10: 5000 × 100 × 26 = **1.3 × 10⁷**. Comfortable.

**⚠️ The hidden O(L) factors matter.** Both the string construction and the hash of a length-L string are O(L), not O(1) — which is where the *second* L comes from. Easy to miss, and it's the difference between O(n·L·26) and the true bound.

**Versus building the adjacency list first:** comparing all pairs is O(n²·L) = 2.5 × 10⁸ — an order of magnitude worse. **Generating candidates beats searching for them** whenever the alphabet is small relative to the word count.

**Bidirectional BFS** roughly halves the exponent of the frontier growth: if the answer is at depth d and the branching factor is b, one-directional BFS explores O(b^d) nodes while bidirectional explores O(b^(d/2)) from each side. **A dramatic win in practice**, and the expected follow-up.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n · L)</summary>

**O(n · L)**.

| Component | Size |
|---|---|
| `word_set` | n words of length L → **O(n·L)** |
| `visited` | up to n words → O(n·L) |
| `queue` | up to n entries, each a word plus an int → O(n·L) |

**O(n·L)** total. At 5000 words of length 10, that's ~50,000 characters per structure — trivial.

**The transient candidates** — each `word[:i] + letter + word[i+1:]` allocates a new string — are O(L) each and immediately discarded. Not a space concern, but it's why the *time* has that extra L factor.

**No recursion**, so no stack-depth risk. BFS is iterative by nature — one of its practical advantages over DFS on large graphs.

**A memory-saving variant:** instead of a separate `visited` set, **remove words from `word_set` as you enqueue them**. Same effect (a word can't be revisited), one less structure:

```python
word_set.remove(candidate)
queue.append((candidate, steps + 1))
```

⚠️ But it mutates the input-derived set, which matters if the caller reuses it. The explicit `visited` set is the safer default — the same non-destructive-versus-in-place trade seen throughout Unit 11.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "This is a shortest-path problem in disguise: each word is a node, and two words are adjacent if they differ by one letter — so BFS gives the shortest sequence, because the first time I reach `endWord` it's via the shortest path. The efficiency question is how to find a word's neighbours. Comparing against all 5000 words is O(n·L) per word; instead I *generate* the neighbourhood — try all 26 letters at each of the L positions and check each candidate against a set in O(1). That's L×26 candidates instead of n comparisons. Each queue entry carries its own distance so I don't need level tracking, and I start at 1 because the answer counts words rather than transformations. I mark words visited on enqueue rather than dequeue, so the same word isn't queued repeatedly. O(n·L²·26) time — the extra L comes from string construction and hashing."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Can you make it faster?" | **Bidirectional BFS** — search from both ends and stop when the frontiers meet. Roughly O(b^(d/2)) instead of O(b^d). |
| "Why generate candidates instead of comparing words?" | L×26 = 260 candidates versus 5000 comparisons. Generating wins whenever the alphabet is small relative to the word count. |
| "Why BFS and not DFS?" | DFS finds *a* path, not the shortest. BFS explores in distance order. |
| "Why start at 1?" | The answer counts words, not transformations. `beginWord` alone is a one-word sequence. |
| "Why mark visited on enqueue?" | Otherwise several neighbours at the same level enqueue the same word repeatedly. |
| "Return the actual **path**?" | Store a parent pointer per word and walk back from `endWord`. Returning *all* shortest paths is LeetCode 126, notably harder. |
| "What if words could differ in length?" | The neighbour rule changes to edit distance, and you'd generate insertions and deletions too. |

**Traps:**

- **Starting at 0** — returns the number of *transformations* instead of words.
- **Marking visited on dequeue** — the queue fills with duplicates of the same word.
- **Using a list instead of a set** for `wordList` — `in` becomes O(n), making the whole thing O(n²·L²).
- **Building the full adjacency list** — correct but O(n²·L).
- **Using DFS** — gives a path, not the shortest one.
- **Forgetting the `endWord` guard** — correct but wastes a full traversal on an impossible case.
- **Claiming O(n·L·26)** — the string construction and hashing each cost O(L), so it's L².

**This same move shows up in:** [Walls and Gates](286-walls-and-gates.md) (BFS with distances carried per node) · [Rotting Oranges](994-rotting-oranges.md) (BFS counting levels) · [Binary Tree Level Order Traversal](102-binary-tree-level-order-traversal.md) (the level-snapshot alternative) · [Clone Graph](133-clone-graph.md) (traversing an implicit graph) · [bfs](../algorithms/bfs.md).

</details>

---
