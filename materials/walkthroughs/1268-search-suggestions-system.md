# 1268. Search Suggestions System

**Medium** · [LeetCode](https://leetcode.com/problems/search-suggestions-system/) · [Solution file (no hints)](../../problems/1000-1499/1268.py)

[📖 08. Tries lesson](../learning/08-tries.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 08. Tries problems](../rmap-practice/08-tries.md)

---

Given `products` and a `searchWord`, after each character typed return **at most three** product names sharing that prefix. If more than three match, return the three **lexicographically smallest**.

```
products = ["mobile","mouse","moneypot","monitor","mousepad"], searchWord = "mouse"
  →  [["mobile","moneypot","monitor"],
      ["mobile","moneypot","monitor"],
      ["mouse","mousepad"],
      ["mouse","mousepad"],
      ["mouse","mousepad"]]
```

**Constraints:** `1 <= products.length <= 1000` · `1 <= products[i].length <= 3000` · `sum(products[i].length) <= 2·10⁴` · all products **unique**, lowercase · `1 <= searchWord.length <= 1000`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "after **each character** typed" | ⚠️ `len(searchWord)` separate queries, on prefixes that **grow by one each time** |
| "at most **three**" | A small fixed cap — you never need the full match set |
| "lexicographically **minimum**" | ⚠️ Sorting the products once makes "first three found" automatically correct |
| products are **unique** | No duplicate handling |
| `sum(products[i].length) <= 2·10⁴` | Total input is small, so an O(total) preprocessing pass is cheap |
| `searchWord.length` up to 1000 | Up to 1000 queries against a fixed product set ⇒ preprocess |

**The observation that simplifies everything:**

> **Sort `products` first.** Then for any prefix, the lexicographically smallest matches are simply the *first three* you encounter in sorted order — no comparison or selection logic needed.

Without sorting you'd have to collect all matches and then find the three smallest. With sorting, "smallest three" collapses into "first three."

**The second observation — prefixes are nested:**

```
searchWord = "mouse"
queries:  "m" → "mo" → "mou" → "mous" → "mouse"
```

Each prefix extends the last, so the matching set only ever **shrinks**. Anything that fails to match `"mou"` can never match `"mous"`. That monotonic narrowing is what makes both good solutions work.

**Two natural designs:**

| | Idea |
|---|---|
| **Trie** | Walk one node per character; each node stores its three best completions |
| **Two pointers on the sorted array** | Narrow a `[left, right]` window as the prefix grows |

Both are O(1)-ish per query after preprocessing. The trie is the "intended" answer for this unit; the two-pointer version is shorter and often faster in practice.

🤔 **Before you open the next section:** if the products are sorted and you're scanning for matches, why are the first three you find guaranteed to be the lexicographically smallest?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

Let `n` = number of products, `L` = max product length, `m` = `len(searchWord)`, `S` = total product characters.

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Filter all products per prefix | For each prefix, scan and `startswith` | O(m · n · L) | ⚠️ 1000 × 1000 × 3000 — far too slow |
| **Sort + binary search per prefix** | `bisect` the window, take 3 | O(S log n + m log n) | ✅ Concise |
| **Sort + two-pointer narrowing** | Shrink `[left, right]` as the prefix grows | **O(S log n + m)** | ✅ Elegant |
| **Trie with cached top-3** | Each node stores its three best completions | **O(S + m)** query-side | ✅ The unit's technique |

**The decision: build a trie whose nodes cache their three lexicographically smallest completions.**

Insert products **in sorted order**; then at each node, append the product to that node's `suggestions` list only while it holds fewer than three. Because insertion order is sorted, the first three to reach any node *are* its three smallest completions.

```
products sorted: ["mobile","moneypot","monitor","mouse","mousepad"]

node "mo"  → ["mobile","moneypot","monitor"]     ← first three to pass through
node "mou" → ["mouse","mousepad"]                 ← only two exist
```

Then each query is a single character step, reading a precomputed list — **O(1) per typed character**.

**Why sorting before insertion is what makes the cache correct.** If you inserted in arbitrary order, a node's first three arrivals would be arbitrary, and you'd need to sort or heap-select afterwards. Sorting once up front makes "take the first three" exactly right, with a trivial `if len(...) < 3` guard.

**The two-pointer alternative**, worth knowing because it's shorter and needs no trie:

```python
products.sort()
result, left, right = [], 0, len(products) - 1

for i, ch in enumerate(searchWord):
    while left <= right and (len(products[left]) <= i or products[left][i] != ch):
        left += 1
    while left <= right and (len(products[right]) <= i or products[right][i] != ch):
        right -= 1
    result.append(products[left:min(left + 3, right + 1)])   # ⚠️ clamp to right

return result
```

Because the sorted array groups matching prefixes into a **contiguous block**, and that block only narrows as the prefix grows, two pointers converging inward track it in O(1) amortized per character.

⚠️ **The slice must be clamped to `right + 1`.** Writing `products[left:left+3]` is the natural-looking mistake: it takes three entries from `left` regardless of where the matching block actually ends. On `products = ["bcca","caac","ccabb"]` with prefix `"b"`, the block is just `["bcca"]` — but the unclamped slice returns all three. When the block holds fewer than three matches, `min(left+3, right+1)` is what stops the slice at the block's edge.

**Why a trie is still the right thing to learn here.** The two-pointer trick depends on the queries being *nested prefixes of a single word*. A trie answers **arbitrary** prefix queries, supports incremental insertion, and generalizes to autocomplete systems where the query set isn't known in advance. This problem is the unit's motivation for that structure.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.suggestions = []
```

`suggestions` caches up to three completions passing through this node — the precomputed answer for the prefix ending here.

No `is_word` flag is needed: queries ask for completions, never whether the prefix is itself a product.
→ [class-basics](../syntax/class-basics.md)

---

```python
products.sort()
```

**The step that makes everything else simple.** After sorting, "first three encountered" equals "three lexicographically smallest."
→ [sorting-key](../syntax/sorting-key.md)

```python
root = TrieNode()

for product in products:
    node = root
    for ch in product:
        if ch not in node.children:
            node.children[ch] = TrieNode()
        node = node.children[ch]
        if len(node.suggestions) < 3:
            node.suggestions.append(product)
```

**Insert each product, caching it along its whole path.**

The `if len(...) < 3` cap is what keeps memory bounded: each node stores at most three strings regardless of how many products share its prefix.

Appending **after** descending means the root never accumulates suggestions — correct, since queries always have at least one character.
→ [for-loop](../syntax/for-loop.md) · [list-methods](../syntax/list-methods.md)

---

```python
result = []
node = root

for ch in searchWord:
    if node:
        node = node.children.get(ch)
    result.append(node.suggestions if node else [])

return result
```

**Walk the search word one character at a time**, reading each node's cached list.

**The `if node:` guard is the key detail.** Once the walk falls off the trie — the prefix matches nothing — every *longer* prefix also matches nothing. Setting `node` to `None` and checking it each iteration means all subsequent queries correctly return `[]` without special-casing or breaking out.

`.get(ch)` returns `None` for a missing child rather than raising, which is exactly the behaviour wanted.
→ [dict-methods](../syntax/dict-methods.md) · [ternary-expression](../syntax/ternary-expression.md)

<details>
<summary>The whole thing together</summary>

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.suggestions = []


class Solution:
    def suggestedProducts(self, products: List[str], searchWord: str) -> List[List[str]]:

        products.sort()

        root = TrieNode()
        for product in products:
            node = root
            for ch in product:
                if ch not in node.children:
                    node.children[ch] = TrieNode()
                node = node.children[ch]
                if len(node.suggestions) < 3:
                    node.suggestions.append(product)

        result = []
        node = root
        for ch in searchWord:
            if node:
                node = node.children.get(ch)
            result.append(node.suggestions if node else [])

        return result
```

</details>

<details>
<summary>The two-pointer version (no trie)</summary>

```python
class Solution:
    def suggestedProducts(self, products: List[str], searchWord: str) -> List[List[str]]:
        products.sort()
        result = []
        left, right = 0, len(products) - 1

        for i, ch in enumerate(searchWord):
            while left <= right and (len(products[left]) <= i or products[left][i] != ch):
                left += 1
            while left <= right and (len(products[right]) <= i or products[right][i] != ch):
                right -= 1
            result.append(products[left:min(left + 3, right + 1)])

        return result
```

Sorted order puts all products sharing a prefix in a **contiguous block**; the block only shrinks as the prefix grows, so two converging pointers track it. Shorter, and O(1) extra space beyond the sort.

The `min(left + 3, right + 1)` clamp is essential — see the note above. It also makes the empty case fall out for free: when the block is exhausted, `right < left`, so the slice is empty and no `if left <= right` guard is needed.

</details>

**Build the trie** — sorted products `["mobile","moneypot","monitor","mouse","mousepad"]`:

| Node | Products passing through (in sorted order) | Cached `suggestions` |
|---|---|---|
| `m` | all five | `["mobile","moneypot","monitor"]` (capped) |
| `mo` | all five | `["mobile","moneypot","monitor"]` |
| `mou` | mouse, mousepad | `["mouse","mousepad"]` |
| `mous` | mouse, mousepad | `["mouse","mousepad"]` |
| `mouse` | mouse, mousepad | `["mouse","mousepad"]` |

**Trace the query** — `searchWord = "mouse"`:

| Typed | Prefix | Node reached | Returned |
|---|---|---|---|
| `m` | `"m"` | `m` | `["mobile","moneypot","monitor"]` |
| `o` | `"mo"` | `mo` | `["mobile","moneypot","monitor"]` |
| `u` | `"mou"` | `mou` | `["mouse","mousepad"]` |
| `s` | `"mous"` | `mous` | `["mouse","mousepad"]` |
| `e` | `"mouse"` | `mouse` | `["mouse","mousepad"]` |

Matches the expected output ✅

Note how the cap worked at node `m`: five products pass through it, but only the first three in sorted order were kept — and those are exactly the three lexicographically smallest.

**The fall-off case** — `searchWord = "mozz"`: after `"mo"` the character `z` has no child, so `node` becomes `None`. Every remaining character returns `[]`, and the `if node:` guard prevents any further dereferencing.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(S log n + S + m)</summary>

Breaking it down, with `S` = total product characters, `n` = product count, `m` = search word length:

| Phase | Cost |
|---|---|
| Sorting | **O(n · L · log n)** — comparisons touch up to `L` characters |
| Building the trie | **O(S)** — one node visit per character, O(1) append |
| Querying | **O(m)** — one step per typed character, reading a cached list |

With `S <= 2·10⁴` and `m <= 1000`, everything is comfortably fast.

**The query phase is the point:** O(1) per typed character, because each node's answer was precomputed. That's the property a real autocomplete system needs — keystroke latency independent of catalogue size.

**Compare:**

| | Per query |
|---|---|
| Filter all products | O(n · L) |
| Binary search the sorted array | O(log n + 3) |
| Two pointers | O(1) amortized |
| **Trie with cached top-3** | **O(1)** |

**Why capping at 3 keeps the build linear.** Without the cap, a node shared by 1000 products would store 1000 strings, and the build would be O(n · L) *per node* in the worst case. The `< 3` guard makes each append O(1) and bounds total extra storage.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(S) nodes + O(nodes × 3) cached strings</summary>

**O(S)** trie nodes — at most one per character across all products, fewer with shared prefixes.

**Plus up to 3 string references per node.** These are *references*, not copies, so the strings themselves are stored once in `products`; the cache costs a pointer each.

At `S <= 2·10⁴`, that's ~2·10⁴ nodes with ≤ 6·10⁴ references — trivial.

**The trade against the two-pointer version:**

| | Extra space | Query |
|---|---|---|
| Two pointers | **O(1)** beyond the sort | O(1) amortized |
| **Trie + cache** | **O(S)** | O(1) |

The two-pointer version wins on memory and is shorter. The trie wins on **generality**: it answers arbitrary prefix queries, not just the nested prefixes of one word, and supports adding products incrementally.

That's the honest framing:

> **The two-pointer solution exploits a special property of *this* query pattern. The trie solves the general autocomplete problem.**

For a real search box — arbitrary queries, an evolving catalogue — the trie is the right structure, which is why the problem sits in this unit.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "First I sort the products — that single step turns 'the three lexicographically smallest matches' into 'the first three matches I encounter,' which removes all selection logic. Then I build a trie, and as I insert each product I append it to the `suggestions` list of every node along its path, capped at three. Because insertion is in sorted order, the first three to reach a node are exactly its three smallest completions. Each typed character is then one trie step and a cached-list read — O(1) per keystroke. If the walk falls off the trie I set the node to `None`, and the guard makes every longer prefix return an empty list automatically. Building is O(S) after the sort. There's also a neat two-pointer version: sorted order puts matching products in a contiguous block that only shrinks, so you can narrow it with two pointers in O(1) space — shorter, but it only works because the queries are nested prefixes of one word."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why sort first?" | **The key simplification.** It makes "first three found" identical to "three smallest," so no comparison logic is needed. |
| "Solve it without a trie." | Sort, then narrow a `[left, right]` window with two pointers as the prefix grows — O(1) extra space. Or binary search per prefix with `bisect`. |
| "Why cap at three during the build?" | Keeps each append O(1) and bounds memory; storing all completions per node would be O(n·L) in the worst case. |
| "What if the cap were `k`, not 3?" | Change the guard to `< k`. Memory becomes O(nodes × k) — still linear for fixed `k`. |
| "Products added **dynamically**?" | The trie handles it: insert into the path and update caches. The two-pointer version would need a re-sort. |
| "Why is the trie preferable in a real system?" | It answers arbitrary prefix queries and supports incremental updates; the two-pointer trick depends on the nested-prefix query pattern. |
| "What if a prefix matches nothing?" | Return `[]` for it and every longer prefix — the `if node:` guard handles it. |

**Traps:**

- **Not sorting.** Then "first three" is arbitrary and you'd have to select the smallest afterwards.
- **Omitting the `if node:` guard.** `AttributeError` once the walk falls off the trie mid-word.
- **Breaking out of the loop on a miss.** The result must have one entry per typed character — you still need `[]` for the remainder.
- **Caching without the cap.** Memory blows up on prefixes shared by many products.
- **Appending before descending.** The root would accumulate suggestions and the first character's node would be missed.
- **Sorting inside the query loop.** Sort once, before building.

**This same move shows up in:** [Implement Trie (Prefix Tree)](208-implement-trie-prefix-tree.md) (the base structure) · [Replace Words](648-replace-words.md) (prefix walking with early termination) · [Map Sum Pairs](677-map-sum-pairs.md) (caching aggregates on trie nodes for O(prefix) queries) · [Top K Frequent Elements](347-top-k-frequent-elements.md) (the general "keep only the best k" idea).

</details>

---
