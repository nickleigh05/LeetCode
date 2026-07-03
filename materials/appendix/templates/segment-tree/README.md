# Segment Tree & Fenwick Tree

*Range queries on an array that keeps changing — the O(log n) upgrade from prefix sums the moment updates enter the picture.*

## Recognize this pattern when...

- You need **range sum / min / max** *and* the array receives **updates** between queries.
- The ask is **"count elements smaller than x among those seen so far"** — a frequency table you query by prefix. *(Count of Smaller Numbers After Self)*
- A pair-counting problem becomes a **sweep + "how many previous values in this range"** query. *(Reverse Pairs, Count of Range Sum)*
- Prefix sums almost work, but a single update would force an O(n) rebuild.

## Variations

1. **Fenwick tree (BIT)** — prefix sums with point updates in ~20 lines; the default when the operation is invertible. *(Range Sum Query — Mutable)*
2. **Fenwick + coordinate compression** — sort the distinct values, query by rank; turns value-counting into prefix sums. *(Count of Smaller Numbers After Self)*
3. **Segment tree for min/max** — same skeleton, swap the combine function and identity; needed when subtraction can't undo the operation.
4. **Segment tree with lazy propagation** — range *updates* + range queries; defer child updates until a query passes through.
5. **Merge-sort alternative** — offline pair-counting problems (Reverse Pairs, Count of Range Sum) also fall to a count-during-merge; know both.

## Representative problems

| # | Difficulty | Problem |
|---|------------|---------|
| 307 | Medium | Range Sum Query — Mutable |
| 315 | Hard | Count of Smaller Numbers After Self |
| 493 | Hard | Reverse Pairs |
| 327 | Hard | Count of Range Sum |

## Common bugs & traps

- **Passing the new value instead of the delta** to a Fenwick `add` — the tree accumulates, it doesn't overwrite. Keep a copy of the array to compute `val - nums[i]`.
- **Mixing 0- and 1-indexing.** The Fenwick tree is 1-indexed (`i & (-i)` on index 0 loops forever); shift at the boundary, once.
- **Forgetting coordinate compression** when values are large or negative — the tree is sized by *rank count*, not value range.
- **Off-by-one in strict vs non-strict counts.** "Smaller than x" is `prefix(rank(x) - 1)`; "at most x" is `prefix(rank(x))`.
- **Wrong identity for min/max** — a 0 identity silently corrupts min-trees with positive values; use `float('inf')`.
- **Rebuilding instead of updating.** If you find yourself reconstructing the tree per operation, you've lost the whole O(log n) point.
---

*See also: [Lesson 20 →](../../../learning/20-segment-trees.md) · [🗺 Roadmap](../../../../roadmap.md) · [problem lists](../../../../lists/)*
