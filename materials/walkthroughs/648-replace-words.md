# 648. Replace Words

**Medium** · [LeetCode](https://leetcode.com/problems/replace-words/) · [Solution file (no hints)](../../problems/0500-0999/648.py)

[📖 08. Tries lesson](../learning/08-tries.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 08. Tries problems](../rmap-practice/08-tries.md)

---

A **root** followed by another word forms a **derivative** (root `"help"` + `"ful"` → `"helpful"`). Given a dictionary of roots and a sentence, replace every derivative with the root that forms it. If several roots apply, use the **shortest**.

```
dictionary = ["cat","bat","rat"], sentence = "the cattle was rattled by the battery"
  →  "the cat was rat by the bat"

dictionary = ["a","b","c"], sentence = "aadsfasf absbs bbab cadsfafs"
  →  "a a b c"
```

**Constraints:** `1 <= dictionary.length <= 1000` · `1 <= dictionary[i].length <= 100` · `1 <= sentence.length <= 10⁶` · ≤ 1000 words, each ≤ 1000 chars · lowercase letters only

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**root**" precedes the rest | ⚠️ You're matching **prefixes** — the signature of a [trie](../data-structures/trie.md) |
| "use the **shortest** root" | ⚠️ Stop at the **first** root found while walking the word left to right — shorter roots are encountered earlier |
| dictionary up to 1000 roots | Repeated prefix queries against a fixed set ⇒ preprocess once |
| `sentence.length` up to **10⁶** | Big. An O(words × roots × length) scan is far too slow |
| no root matches | Leave the word unchanged |
| lowercase only | A 26-way branching factor — a clean array-or-dict trie |

**Why this is a trie problem and not a set problem.** With a hash set of roots you'd have to *guess* the root's length: for each word, test every prefix (`w[:1]`, `w[:2]`, …) against the set. That's O(L) lookups per word, and each lookup hashes an O(L) string — **O(L²) per word**.

A trie inverts that. You walk the word **one character at a time**, and each step is a single O(1) child lookup:

```
dictionary = ["cat","bat","rat"]        walking "cattle":

  root                                   c → a → t  ← is_word ✅ stop here
  ├─ c → a → t*                          shortest match found after 3 chars
  ├─ b → a → t*
  └─ r → a → t*
```

**The "shortest root" rule is free.** Because you walk left to right and stop at the first node marked as a word end, you *necessarily* find the shortest root — a longer root that also matches would be discovered later, and you've already stopped. No comparison logic needed.

**The two stopping conditions** while walking a word:

1. **Hit a word-end marker** → replace the word with the prefix consumed so far
2. **Run out of trie** (no child for the next character) → no root matches; keep the word whole

🤔 **Before you open the next section:** if you walk a word character by character through the trie, why is the first word-end you encounter guaranteed to be the shortest matching root?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

Let `d` = number of roots, `L` = max word length, `W` = number of words, `S` = total sentence length.

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| For each word, test each root | `word.startswith(root)` for all roots | O(W · d · L) | O(1) | ❌ 10⁶ ops per word — far too slow |
| Hash set of roots, test every prefix | Check `w[:1]`, `w[:2]`, … | O(S · L) | O(d·L) | ⚠️ Works, but each lookup hashes an O(L) string |
| **Trie of roots** | Walk each word one char at a time | **O(d·L + S)** | O(d·L) | ✅ |

**The decision: build a [trie](../data-structures/trie.md) from the dictionary, then walk each word through it.**

The cost splits cleanly:

- **Build once:** insert `d` roots, each up to `L` characters → O(d · L)
- **Query:** each word walks at most its own length → O(S) across the whole sentence

That's the same **"preprocess once, query many"** design as [Range Sum Query](303-range-sum-query-immutable.md) and [Is Subsequence](392-is-subsequence.md)'s follow-up — and the trigger is identical: many queries against a fixed data set.

**Why a trie beats the prefix-set approach.** Both are correct, but note where the work goes:

| | Per word |
|---|---|
| Set + every prefix | up to `L` lookups, **each hashing an O(L) slice** → O(L²) |
| Trie | up to `L` steps, **each an O(1) dict lookup** → O(L) |

The trie shares prefixes across roots, so `"cat"`, `"car"`, and `"cart"` collapse into one `c→a` spine. With 1000 roots of up to 100 characters, that sharing matters for both time and memory.

**Why `is_word` must be a separate flag.** You cannot infer "a root ends here" from a node having no children — `"cat"` and `"cattle"` could both be roots, so the node after `t` has children *and* marks a word end. An explicit boolean is required. This is the standard trie subtlety, and it's the same reason [Implement Trie](208-implement-trie-prefix-tree.md) carries one.

**Why `defaultdict` isn't ideal for lookups.** Using `defaultdict(dict)` for children is convenient during *insertion*, but during *search* an accidental `node[ch]` would silently create an empty child rather than failing. Use an explicit `if ch not in node.children: break` on the query path.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False
```

A node holds a character→child map and a flag marking the end of a root.

A `dict` rather than a fixed 26-slot list: sparser, and the alphabet is small enough that the constant factor doesn't matter.
→ [class-basics](../syntax/class-basics.md) · [dict-basics](../syntax/dict-basics.md)

---

**Build the trie**

```python
root = TrieNode()

for word in dictionary:
    node = root
    for ch in word:
        if ch not in node.children:
            node.children[ch] = TrieNode()
        node = node.children[ch]
    node.is_word = True
```

Insert each root, creating nodes as needed. Setting `is_word` on the **final** node is what marks a complete root — shared prefixes reuse the same nodes automatically.
→ [for-loop](../syntax/for-loop.md) · [dict-methods](../syntax/dict-methods.md)

---

**Replace each word**

```python
def shortest_root(word):
    node = root
    prefix = []

    for ch in word:
        if ch not in node.children:
            break
        node = node.children[ch]
        prefix.append(ch)
        if node.is_word:
            return "".join(prefix)

    return word
```

**Walk the word character by character.**

- `ch not in node.children` → the trie has no path for this character, so **no root matches** → break out and keep the word whole.
- `node.is_word` → we've just completed a root. Return immediately — **this is the shortest match**, because any longer root would require more characters.

The `return` inside the loop is what implements "shortest" with no extra logic.

Accumulating into a list and joining once avoids O(L²) string concatenation — the same discipline as [Binary Tree Paths](257-binary-tree-paths.md).
→ [break-continue](../syntax/break-continue.md) · [string-join-slice](../syntax/string-join-slice.md)

```python
return " ".join(shortest_root(w) for w in sentence.split())
```

Split on whitespace, map each word, rejoin with single spaces. The constraints promise exactly one space between words and no leading/trailing spaces, so `split()` / `" ".join(...)` round-trips exactly.
→ [generator-expressions](../syntax/generator-expressions.md) · [string-methods](../syntax/string-methods.md)

<details>
<summary>The whole thing together</summary>

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False


class Solution:
    def replaceWords(self, dictionary: List[str], sentence: str) -> str:

        root = TrieNode()
        for word in dictionary:
            node = root
            for ch in word:
                if ch not in node.children:
                    node.children[ch] = TrieNode()
                node = node.children[ch]
            node.is_word = True

        def shortest_root(word):
            node = root
            prefix = []
            for ch in word:
                if ch not in node.children:
                    break
                node = node.children[ch]
                prefix.append(ch)
                if node.is_word:
                    return "".join(prefix)
            return word

        return " ".join(shortest_root(w) for w in sentence.split())
```

</details>

<details>
<summary>The hash-set alternative (simpler, slower)</summary>

```python
class Solution:
    def replaceWords(self, dictionary: List[str], sentence: str) -> str:
        roots = set(dictionary)

        def shortest_root(word):
            for i in range(1, len(word) + 1):
                if word[:i] in roots:
                    return word[:i]
            return word

        return " ".join(shortest_root(w) for w in sentence.split())
```

Correct and four lines shorter. But each `word[:i]` builds and hashes an O(i) string, giving O(L²) per word. Fine at these constraints; the trie is the intended answer and scales better.

</details>

**Build the trie** — `dictionary = ["cat","bat","rat"]`:

```
        root
       /  |  \
      c   b   r
      |   |   |
      a   a   a
      |   |   |
      t*  t*  t*        (* = is_word)
```

**Trace the replacements** — `sentence = "the cattle was rattled by the battery"`:

| Word | Walk | Outcome |
|---|---|---|
| `the` | `t` not in root's children | break → keep **`the`** |
| `cattle` | `c` ✅ → `a` ✅ → `t` ✅ **is_word** | return **`cat`** ⭐ |
| `was` | `w` not in root | keep **`was`** |
| `rattled` | `r` → `a` → `t` **is_word** | return **`rat`** |
| `by` | `b` ✅, but `b`'s only child is `a` — no `y` | break → keep **`by`** |
| `the` | `t` not in root | keep **`the`** |
| `battery` | `b` → `a` → `t` **is_word** | return **`bat`** |

Result: **`"the cat was rat by the bat"`** ✅

The starred step shows the early return: `"cattle"` stopped after 3 characters and never examined `t`, `l`, `e`.

**The shortest-root rule in action** — with `dictionary = ["a","aa","aaa"]` and the word `"aaaa"`: walking left to right, `is_word` fires at the very first `a`, so the answer is `"a"` — the shortest — without ever comparing candidate lengths.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(d·L + S)</summary>

**O(d · L + S)**, where `d` = number of roots, `L` = max root length, `S` = total sentence length.

- **Build:** `d` roots × up to `L` characters, each an O(1) dict operation → **O(d · L)** ≤ 1000 × 100 = 10⁵
- **Query:** each word walks at most its own length, and word lengths sum to `S` → **O(S)** ≤ 10⁶

Total ≈ 1.1 × 10⁶ operations — comfortably fast.

**Compare the alternatives:**

| | Time |
|---|---|
| Test every root per word | O(W · d · L) = 1000 × 1000 × 100 = **10⁸** ❌ |
| Set + every prefix | O(S · L) — each lookup hashes an O(L) slice |
| **Trie** | **O(d·L + S)** ✅ |

**Why the query phase is O(S) and not O(S · L).** Each character of the sentence is consumed by at most one trie step. The walk for a word stops at the first `is_word` or the first missing child — it never restarts or backtracks. So the total query work is bounded by the sentence's length, not by length × alphabet or length².

</details>

<details>
<summary><b>5 · Space complexity</b> — O(d · L)</summary>

**O(d · L)** for the trie — at most one node per character across all roots, minus whatever shared prefixes collapse.

Worst case (no shared prefixes): 1000 × 100 = **10⁵ nodes**. Best case, with heavy sharing, far fewer — `"cat"`, `"car"`, `"card"` occupy 5 nodes rather than 10.

**The output is O(S)**, which is required.

**The trade against the hash set:**

| | Space | Per-query cost |
|---|---|---|
| Hash set of roots | O(d · L) — same order | O(L²), hashing slices |
| **Trie** | O(d · L), **shared prefixes** | **O(L)**, O(1) steps |

Same asymptotic space, but the trie's structure is what converts the query from quadratic to linear — and prefix sharing means it often uses *less* memory in practice than storing every root as a separate string.

**The general principle:**

> **A trie turns "which stored string is a prefix of this one?" into a single walk.** A hash set can only answer "is this exact string stored?", so it forces you to enumerate candidate prefixes yourself.

That's exactly why [Implement Trie](208-implement-trie-prefix-tree.md), [Word Search II](212-word-search-ii.md), and [Search Suggestions System](1268-search-suggestions-system.md) all reach for the same structure.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "This is repeated prefix matching against a fixed dictionary, which is exactly what a trie is for. I build the trie once from the roots — O(d·L) — marking the last node of each root with an `is_word` flag, which has to be explicit because one root can be a prefix of another. Then for each word I walk the trie one character at a time. If I hit a node marked as a word end, I return the prefix consumed so far — and that's automatically the **shortest** root, because I'm walking left to right and any longer root would need more characters. If I run out of trie, no root matches and the word stays whole. O(d·L + S) total, O(d·L) space. A hash set of roots also works, but you'd have to test every prefix and each lookup hashes an O(L) slice, making it quadratic per word."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why not a hash set?" | You'd have to enumerate prefixes yourself — O(L) lookups each hashing an O(L) string, so O(L²) per word. The trie walks character by character in O(L). |
| "Why is the first match the shortest?" | You consume characters left to right, so a shorter root's end node is reached before a longer one's. |
| "Why is `is_word` needed?" | A root can be a prefix of another root (`"cat"` and `"cattle"`), so having children doesn't mean the node isn't a word end. |
| "Replace with the **longest** root instead?" | Don't return early — keep walking and remember the last `is_word` seen, returning that at the end. |
| "What if roots could be uppercase or mixed?" | Normalize case on insert and query, or widen the children map. |
| "Memory too large?" | Compress single-child chains into a radix (Patricia) trie, or use a 26-slot array per node if density is high. |
| "Many sentences, same dictionary?" | Build the trie once and reuse it — the O(d·L) cost amortizes across all queries. |

**Traps:**

- **Inferring word-ends from childlessness.** Fails when one root prefixes another; you need the explicit flag.
- **Not returning early.** Continuing past the first `is_word` gives the *longest* root, not the shortest.
- **Using `defaultdict` on the query path.** `node[ch]` would silently create empty nodes instead of failing, corrupting the trie and reporting false matches.
- **Concatenating the prefix with `+=`.** O(L²) per word; accumulate in a list and join once.
- **Rebuilding the trie per word.** Build once outside the loop.
- **Using `sentence.split(" ")` when the format is uncertain.** Bare `split()` handles runs of whitespace; here the constraints guarantee single spaces, so both work.

**This same move shows up in:** [Implement Trie (Prefix Tree)](208-implement-trie-prefix-tree.md) (the structure this builds on, including the `is_word` flag) · [Design Add and Search Words](211-design-add-and-search-words-data-structure.md) (trie search with wildcards) · [Search Suggestions System](1268-search-suggestions-system.md) (prefix walks returning multiple matches) · [Longest Common Prefix](14-longest-common-prefix.md) (the same prefix relationship, without needing a structure).

</details>

---
