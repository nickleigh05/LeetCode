# 677. Map Sum Pairs

**Medium** · [LeetCode](https://leetcode.com/problems/map-sum-pairs/) · [Solution file (no hints)](../../problems/0500-0999/677.py)

[📖 08. Tries lesson](../learning/08-tries.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 08. Tries problems](../rmap-practice/08-tries.md)

---

Design a map supporting:

- `insert(key, val)` — map `key` to `val`, **overwriting** any previous value for that key
- `sum(prefix)` — return the total of all values whose keys start with `prefix`

```
insert("apple", 3)
sum("ap")        →  3
insert("app", 2)
sum("ap")        →  5    (apple 3 + app 2)
```

**Constraints:** `1 <= key.length, prefix.length <= 50` · lowercase letters · `1 <= val <= 1000` · at most **50 calls** total

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "keys with a **prefix**" | ⚠️ Prefix aggregation — a [trie](../data-structures/trie.md) question, not a hash-map one |
| "**overriding** an existing key" | ⚠️ **The trap.** Re-inserting must *replace*, not add — and that breaks the naive running-sum approach |
| `sum` returns a **total**, not a list | You need an aggregate, so you can precompute sums rather than enumerating keys |
| at most **50 calls** | Tiny. Correctness matters far more than efficiency here |
| lowercase, length ≤ 50 | Small alphabet, short keys |

**Two viable designs**, and the interesting part is what the override rule does to each.

**Design A — store values at word-ends, sum on query.** Walk to the prefix node, then DFS the whole subtree collecting values. Insert is trivially correct (just overwrite the value at the terminal node). Query costs O(prefix + subtree size).

**Design B — store a running sum on every node.** When inserting, add the value to each node along the path. Then `sum(prefix)` is a single walk returning that node's stored total — O(prefix), no subtree traversal.

Design B is faster, but the override rule makes it subtle:

> Inserting `("apple", 3)` then `("apple", 5)` must leave a total of **5**, not 8.

So you can't simply add — you must add the **delta**:

```
delta = new_val - previous_val_for_this_key
```

which requires remembering each key's current value in a separate hash map. Insert `("apple", 5)` after `("apple", 3)` propagates `+2` along the path, correcting every ancestor's running sum.

🤔 **Before you open the next section:** if every node stores the sum of all keys beneath it, what must happen to those sums when a key's value is *changed* rather than newly added?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

Let `L` = key length, `n` = number of keys, `P` = prefix length.

| Approach | insert | sum | Verdict |
|---|---|---|---|
| Hash map only, scan on query | O(1) | **O(n · P)** — test every key | ⚠️ Fine at 50 calls; ignores the prefix structure |
| **Trie, values at word-ends + DFS on query** | O(L) | O(P + subtree) | ✅ Simple, override is trivial |
| **Trie with running sums + delta on insert** | **O(L)** | **O(P)** | ✅✅ Fastest query; needs the delta trick |

**The decision: a trie carrying a running `total` on every node, with a companion hash map for delta computation.**

The two structures work together:

- **`self.vals`** — `key → current value`, so an override can compute the delta
- **The trie** — each node's `total` is the sum of all values for keys passing through it

**Insert:**

```python
delta = val - self.vals.get(key, 0)   # ← the override fix
self.vals[key] = val
node = root
for ch in key:
    node = node.children.setdefault(ch, TrieNode())
    node.total += delta               # every ancestor updated
```

**Query:**

```python
node = root
for ch in prefix:
    if ch not in node.children: return 0
    node = node.children[ch]
return node.total                     # already aggregated
```

**Why the delta is essential.** Without it, `insert("apple", 3)` then `insert("apple", 5)` would push 3 and then 5 onto every node along `a→p→p→l→e`, leaving totals of 8. The delta (`5 − 3 = +2`) corrects them to 5. **This is the single thing that makes the problem Medium rather than Easy.**

**Why the plain-hash-map approach is defensible here.** With at most 50 calls and keys ≤ 50 characters, `sum(prefix)` by scanning every key is at most 50 × 50 = 2500 character comparisons — instant. Say it as your baseline: *"at these constraints a dict with a linear scan works, but the prefix structure is clearly what's being asked for."* Then build the trie.

**Why not the DFS-on-query variant?** It's genuinely simpler — no delta arithmetic, since each key's value lives in exactly one node and overwriting is a plain assignment. The cost is that `sum` must traverse the entire subtree. Worth mentioning as the trade: **running sums make insert slightly harder and queries much faster.**

**Why `total` on internal nodes, not just leaves.** The whole point is that `sum(prefix)` should not need to look below the prefix node. Pushing the value into every node along the insertion path pre-aggregates exactly what queries ask for — the same "move work from the hot path to the setup" idea as [Range Sum Query](303-range-sum-query-immutable.md).

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.total = 0
```

`total` is the sum of all values whose keys pass through this node — **not** just keys ending here.

Note there's no `is_word` flag: `sum` never needs to know where keys end, only the aggregate beneath a prefix.
→ [class-basics](../syntax/class-basics.md) · [dict-basics](../syntax/dict-basics.md)

---

```python
class MapSum:
    def __init__(self):
        self.root = TrieNode()
        self.vals = {}
```

Two structures: the trie for prefix aggregation, and `vals` recording each key's **current** value so overrides can be handled.
→ [init-method](../syntax/init-method.md)

---

```python
    def insert(self, key: str, val: int) -> None:
        delta = val - self.vals.get(key, 0)
        self.vals[key] = val
```

**The delta — the heart of the problem.**

- New key → `.get(key, 0)` returns 0, so `delta == val` (a plain addition)
- Existing key → `delta` is the *change*, which may be negative

Recording the new value immediately keeps `vals` authoritative for the next override.
→ [dict-methods](../syntax/dict-methods.md)

```python
        node = self.root
        for ch in key:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
            node.total += delta
```

**Walk the key, applying the delta to every node on the path.**

Each node's `total` now reflects the corrected sum for all keys beneath it — including this one at its new value.

`node.total += delta` sits **after** the descent, so the root itself is never updated. That's fine: `sum("")` isn't part of the API, and every real prefix has at least one character.
→ [for-loop](../syntax/for-loop.md)

---

```python
    def sum(self, prefix: str) -> int:
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return 0
            node = node.children[ch]
        return node.total
```

**Walk to the prefix node and read the precomputed total.**

A missing character means no key has this prefix → **0**.

No subtree traversal, no enumeration — the aggregate was maintained during insertion.
→ [break-continue](../syntax/break-continue.md)

<details>
<summary>The whole thing together</summary>

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.total = 0


class MapSum:

    def __init__(self):
        self.root = TrieNode()
        self.vals = {}

    def insert(self, key: str, val: int) -> None:
        delta = val - self.vals.get(key, 0)
        self.vals[key] = val

        node = self.root
        for ch in key:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
            node.total += delta

    def sum(self, prefix: str) -> int:
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return 0
            node = node.children[ch]
        return node.total


# Your MapSum object will be instantiated and called as such:
# obj = MapSum()
# obj.insert(key,val)
# param_2 = obj.sum(prefix)
```

</details>

<details>
<summary>The simpler variant — values at word-ends, DFS on query</summary>

```python
class MapSum:
    def __init__(self):
        self.root = TrieNode()      # uses .value instead of .total

    def insert(self, key, val):
        node = self.root
        for ch in key:
            node = node.children.setdefault(ch, TrieNode())
        node.value = val            # plain overwrite — no delta needed

    def sum(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return 0
            node = node.children[ch]

        total = 0
        stack = [node]
        while stack:
            cur = stack.pop()
            total += cur.value
            stack.extend(cur.children.values())
        return total
```

Insert is trivially override-safe because each key's value lives in exactly one node. The cost moves to `sum`, which must walk the whole subtree.

</details>

**Trace the example:**

| Call | Action | Trie totals along `a→p→p→l→e` |
|---|---|---|
| `insert("apple", 3)` | `delta = 3 − 0 = 3` | `a:3, p:3, p:3, l:3, e:3` |
| `sum("ap")` | walk `a→p`, read total | **3** ✅ |
| `insert("app", 2)` | `delta = 2 − 0 = 2` | `a:5, p:5, p:5`, and `l:3, e:3` unchanged |
| `sum("ap")` | walk `a→p`, read total | **5** ✅ |

After both inserts the trie looks like:

```
a(5) → p(5) → p(5) → l(3) → e(3)
```

Node `a→p` holds 5 — the sum of both keys — and `sum("ap")` reads it directly, with no traversal below.

**The override case** — the reason the delta exists:

| Call | `delta` | Totals along `a→p→p→l→e` | `sum("app")` |
|---|---|---|---|
| `insert("apple", 3)` | `3 − 0 = 3` | all 3 | 3 |
| `insert("apple", 5)` | **`5 − 3 = 2`** | all 5 | **5** ✅ |

Without the delta, the second insert would have added 5 to nodes already holding 3, giving **8** — silently wrong, and invisible until a key is re-inserted.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(L) insert, O(P) sum</summary>

| Operation | Complexity |
|---|---|
| `insert(key, val)` | **O(L)** — one pass over the key, O(1) work per character |
| `sum(prefix)` | **O(P)** — one pass over the prefix, then a single read |

Both independent of how many keys are stored — that's the payoff for maintaining running sums.

**Compare the designs:**

| | insert | sum |
|---|---|---|
| Hash map + scan | O(1) | O(n · P) |
| Trie + DFS on query | O(L) | O(P + subtree size) |
| **Trie + running sums** | **O(L)** | **O(P)** ✅ |

The running-sum version moves all the aggregation work into `insert`, so queries become a single lookup. That's the right trade whenever queries outnumber updates — the same reasoning as [Range Sum Query - Immutable](303-range-sum-query-immutable.md), except here the data *does* change, which is precisely why the delta is needed.

At 50 total calls with keys ≤ 50 characters, every approach is instantaneous. The design question is what's being assessed, not the runtime.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n · L)</summary>

**O(n · L)** where `n` is the number of distinct keys — at most one trie node per character, minus shared prefixes.

Plus **O(n · L)** for the `vals` map storing each key.

At 50 calls with 50-character keys, that's a worst case of ~2500 nodes — trivial.

**Why the extra `vals` map is worth it.** It's the price of O(P) queries: without it you cannot compute a delta, and without deltas the running sums are wrong on override. The alternative (values at word-ends) avoids `vals` entirely but pays with subtree traversal on every query.

| | Extra structures | Query cost |
|---|---|---|
| Values at word-ends | trie only | O(P + subtree) |
| **Running sums** | trie + `vals` map | **O(P)** |

**The general lesson:**

> **Precomputed aggregates make queries fast but updates delicate.** Any value that can *change* must be applied as a delta, or the aggregate drifts.

That's the same invariant maintenance that makes [Insert Delete GetRandom O(1)](380-insert-delete-getrandom-o1.md) and [LRU Cache](146-lru-cache.md) tricky — two structures that must agree, where every mutation has to update both.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The query is a prefix aggregate, so a trie is the natural structure. I store a running `total` on **every** node — the sum of all values for keys passing through it — so `sum(prefix)` is just a walk to that node and a single read, O(prefix). The catch is the override rule: re-inserting a key must replace its value, not add to it. So I keep a separate hash map of each key's current value and push the **delta** — new minus old — along the insertion path. That corrects every ancestor's total. Without it, inserting `(\"apple\", 3)` then `(\"apple\", 5)` would leave 8 instead of 5. O(L) insert, O(P) query. A simpler alternative stores values only at word-ends and DFS-es the subtree on query — override becomes a plain overwrite, but queries get slower."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "What happens on a **re-insert**?" | **The key question.** You must apply the delta `new − old`, which requires remembering the old value in a side map. |
| "Solve it without the extra map." | Store values at word-ends and DFS the subtree on query. Insert becomes a plain overwrite; `sum` costs O(P + subtree). |
| "Could you just use a dict?" | Yes at these constraints — scan all keys with `startswith`. O(n·P) per query, and it ignores the prefix structure. |
| "Support **deletion**?" | Insert with `val = 0`, or push a delta of `−current` and remove the key from `vals`. Optionally prune zero-total branches. |
| "Return the matching **keys**, not the sum?" | Then running totals don't help — walk to the prefix node and DFS, collecting word-ends. That's [Search Suggestions System](1268-search-suggestions-system.md). |
| "Why no `is_word` flag?" | `sum` only needs aggregates, never key boundaries. The word-end variant needs one (or a sentinel value). |
| "What about `sum(\"\")`?" | Not in the API. If required, store a total on the root too. |

**Traps:**

- **Adding `val` instead of the delta.** *The* bug — silently doubles-counts on any re-insert, and small tests that never override won't catch it.
- **Forgetting to update `vals` after computing the delta.** The next override then computes from a stale baseline.
- **Updating `node.total` before descending.** The root would accumulate totals it shouldn't, and the first character's node would be skipped.
- **Storing totals only at word-ends** while querying internal nodes. `sum("ap")` would read 0.
- **Returning `None` instead of `0`** for an absent prefix.
- **Using `defaultdict` on the query path.** `node.children[ch]` would create empty nodes rather than signalling absence.

**This same move shows up in:** [Implement Trie (Prefix Tree)](208-implement-trie-prefix-tree.md) (the base structure) · [Replace Words](648-replace-words.md) (prefix walking with word-end markers) · [Range Sum Query - Immutable](303-range-sum-query-immutable.md) (precomputed aggregates for O(1) queries) · [Insert Delete GetRandom O(1)](380-insert-delete-getrandom-o1.md) (two structures kept consistent on every mutation).

</details>

---
