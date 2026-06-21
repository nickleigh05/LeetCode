# Arrays & Hashing

*Trade memory for speed. A dict or set turns "is it in here?" from an O(n) scan into an O(1) check — that single swap kills most brute-force double loops.*

## Recognize this pattern when...

- The problem says **"find a pair / duplicate / complement"** and the brute force is a nested loop.
- You need **counts, frequencies, or grouping** ("most common", "anagrams together", "k most frequent").
- The phrase **"in O(n)"** or **"better than O(n²)"** appears in the constraints or follow-up.
- You're repeatedly asking **"have I seen this value / prefix / state before?"**
- You need **O(1) membership** but the values aren't a contiguous range you could index directly.

## Variations

1. **Seen-set membership** — one set, ask "is it already in here?" before inserting. *(Contains Duplicate)*
2. **Complement lookup** — store value→index, look up `target - value` before inserting so `i != j` for free. *(Two Sum)*
3. **Frequency map** — count occurrences, then read off the max / compare two maps. *(Valid Anagram, Top K Frequent)*
4. **Group by derived key** — bucket items under a canonical key like `tuple(sorted(word))` or a 26-letter count. *(Group Anagrams)*
5. **Prefix-sum + hash map** — map each running prefix sum to how often it occurred; seed `{0: 1}` so a subarray starting at index 0 counts. *(Subarray Sum Equals K)*

## Representative problems

| # | Difficulty | Problem |
|---|------------|---------|
| 217 | Easy | [Contains Duplicate](../../../../problems/0001-0499/217.py) |
| 242 | Easy | [Valid Anagram](../../../../problems/0001-0499/242.py) |
| 1 | Easy | [Two Sum](../../../../problems/0001-0499/1.py) |
| 49 | Medium | [Group Anagrams](../../../../problems/0001-0499/49.py) |
| 347 | Medium | [Top K Frequent Elements](../../../../problems/0001-0499/347.py) |
| 128 | Medium | [Longest Consecutive Sequence](../../../../problems/0001-0499/128.py) |

## Common bugs & traps

- **Inserting before checking.** For Two Sum, record the current value *after* the complement check — otherwise an element pairs with itself.
- **Set when you needed a dict.** A set answers "exists?" but loses the index/count. Reach for a dict the moment you need *where* or *how many*.
- **Forgetting the `{0: 1}` seed** in prefix-sum problems — you'll miss every subarray that begins at index 0.
- **Comparing maps wrong.** Two frequency maps are equal only if every key *and* count matches; don't just compare key sets.
- **Unhashable keys.** Lists can't be dict keys — convert to `tuple(...)` first when grouping.
- **Mutating while iterating.** Don't add/remove dict keys inside a `for key in d:` loop; iterate over a snapshot (`list(d)`).
---

*See also: [patterns.md](../../patterns.md) · [datastructures.md](../../../ds&a/datastructures.md) · [algorithms.md](../../../ds&a/algorithms.md) · [lists/](../../../../lists/)*
