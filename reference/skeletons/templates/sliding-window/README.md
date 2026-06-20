# Sliding Window

*Contiguous subarrays / substrings with a moving boundary. Brute force re-scans every window in O(n²); this reuses work and gets it in O(n).*

## Recognize this pattern when...

- The answer is a **contiguous** subarray or substring (order matters, no skipping).
- You're asked for the **longest / shortest / maximum / minimum** window satisfying some property.
- Constraints mention **"at most k"**, **"exactly k"**, or a **fixed length k**.
- A brute force would re-examine overlapping ranges — the window lets you slide instead of restart.
- You can maintain the window's "validity" with a **cheap incremental update** (a sum, a count map, a distinct-count).

## Variations

1. **Longest valid window** — grow with `right`, shrink with `left` *only* while invalid, record after shrinking. *(Longest Substring Without Repeating Characters)*
2. **Shortest valid window** — grow until valid, then shrink *while still valid*, recording inside the shrink loop. *(Minimum Size Subarray Sum)*
3. **Fixed-size window** — width `k` is constant; add the entering element, subtract the leaving one. *(Maximum Average Subarray I)*
4. **Frequency-match window** — keep a count map and a "matches" counter; the window is valid when all required counts are met. *(Find All Anagrams, Minimum Window Substring)*
5. **"Exactly k" via "at most"** — `exactly(k) = atMost(k) - atMost(k - 1)`, each `atMost` a separate longest-window pass. *(Subarrays with K Different Integers)*

## Representative problems

| # | Difficulty | Problem |
|---|------------|---------|
| 121 | Easy | Best Time to Buy and Sell Stock |
| 643 | Easy | Maximum Average Subarray I |
| 3 | Medium | Longest Substring Without Repeating Characters |
| 424 | Medium | Longest Repeating Character Replacement |
| 209 | Medium | Minimum Size Subarray Sum |
| 76 | Hard | Minimum Window Substring |

## Common bugs & traps

- **Recording the answer in the wrong place.** Longest ⇒ update *after* the shrink loop (window is valid). Shortest ⇒ update *inside* the shrink loop, before evicting.
- **Stale keys in the count map.** Delete keys when their count hits 0, or any `len(map)`-based "distinct count" check silently breaks.
- **Window-width off-by-one.** Width is `right - left + 1`, not `right - left`.
- **Fixed window subtracting the wrong index.** The element leaving is `nums[right - k + 1]`; act only once `right >= k - 1`.
- **`if` vs `while` on the shrink.** One eviction often isn't enough — shrink in a loop until the window is valid again.
- **Negative numbers break the monotonic assumption.** "Shrink when sum too big" only works when all values are non-negative; otherwise reach for prefix sums + a hash map instead.
