# Tries (Prefix Trees)

*Prefix trees make string prefix queries O(k) instead of O(n·k). Store every shared prefix once; elegant the moment it clicks.*

## Recognize this pattern when...

- You have **many words** and repeatedly ask **"does any word start with this prefix?"**
- The feature is **autocomplete / search suggestions / spell-check**.
- You need **wildcard or partial matching** within a dictionary.
- A **grid word-search** has to test many candidate words at once — a trie prunes dead branches early.
- Repeated `startsWith` / `search` calls would otherwise re-scan the whole word list each time.

## Variations

1. **Basic insert / search / startsWith** — the core three operations. *(Implement Trie)*
2. **Wildcard search** — recurse into *all* children when the query char is `.`. *(Design Add and Search Words)*
3. **Trie + grid DFS** — drive a backtracking grid search by the trie, pruning when no child matches. *(Word Search II)*
4. **Shortest-root replacement** — walk each word until you hit an `is_end` node. *(Replace Words)*
5. **Prefix aggregation** — store a value/weight at each node and sum along a prefix. *(Map Sum Pairs)*

## Representative problems

| # | Difficulty | Problem |
|---|------------|---------|
| 208 | Medium | Implement Trie (Prefix Tree) |
| 211 | Medium | Design Add and Search Words Data Structure |
| 648 | Medium | Replace Words |
| 677 | Medium | Map Sum Pairs |
| 1268 | Medium | Search Suggestions System |
| 212 | Hard | Word Search II |

## Common bugs & traps

- **Confusing word-end with prefix existence.** `search("app")` must check `is_end`; `startsWith("app")` must not. Without `is_end` you can't tell them apart.
- **Forgetting to set `is_end`.** Every successful insert must mark its final node, or all `search` calls return False.
- **Wildcard not branching.** On `.`, you must try *every* child and short-circuit on the first match — not just the first child.
- **Shared mutable default.** Build `children` in `__init__`, never as a default argument, or all nodes alias one dict.
- **Word Search II duplicates / re-walks.** De-dupe results (use a set or unset `is_end` once found) and prune branches with no matching child to stay fast.
- **Case / alphabet assumptions.** A fixed-size `[26]` array is faster but breaks on uppercase, digits, or unicode — a dict is the safe default.
---

*See also: [Lesson 08 →](../../../learning/08-tries.md) · [🗺 Roadmap](../../../roadmap.md) · [problem lists](../../../../lists/)*
