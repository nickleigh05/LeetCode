# 978. Longest Turbulent Subarray

**Medium** · [LeetCode](https://leetcode.com/problems/longest-turbulent-subarray/) · [Solution file (no hints)](../../problems/0500-0999/978.py)

[📖 15. Greedy lesson](../learning/16-greedy.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 15. Greedy problems](../rmap-practice/15-greedy.md)

---

A subarray is **turbulent** if the comparison sign **flips between every pair of adjacent elements**: `arr[k] > arr[k+1] < arr[k+2] > …` or `arr[k] < arr[k+1] > arr[k+2] < …`. Return the length of the **longest turbulent subarray**.

```
arr = [9, 4, 2, 10, 7, 8, 8, 1, 9]   →  5     ([4, 2, 10, 7, 8])
arr = [4, 8, 12, 16]                 →  2
arr = [100]                          →  1
```

**Constraints:** `1 <= arr.length <= 4 * 10⁴` · `0 <= arr[i] <= 10⁹`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "comparison sign flips" | Look at each **adjacent triple** `(a, b, c)`: `b` must be a strict peak or a strict valley |
| equal neighbours | `a == b` breaks turbulence completely: no sign to flip |
| "longest subarray" (contiguous) | A running length that **extends or resets** as you scan: a sliding window / greedy |
| length 1 is turbulent | Every array has an answer of at least 1. And any two *different* elements form a turbulent pair, so at least 2 when two differ |

**Scan left to right with `cur` = length of the turbulent run ending at `i`:**

- `arr[i] == arr[i-1]` → no direction at all: `cur = 1`.
- If `i >= 2` and `arr[i-2], arr[i-1], arr[i]` form a **peak or valley** (the sign flipped) → extend: `cur += 1`.
- Otherwise (the sign did not flip, but the elements differ) → the best run ending here is just the last pair: `cur = 2`.

Track the maximum.

🤔 **Before you open the next section:** for `[1, 2, 3]`, the elements differ at `i = 2` but don't flip. What should `cur` become, and why 2 and not 1?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | Time | Space | Verdict |
|---|---|---|---|
| Check every subarray | O(n²) to O(n³) | O(1) | ❌ |
| DP: `up[i]`, `down[i]` arrays | O(n) | O(n) | ✅ Standard, and clear |
| **One pass with a running length** | **O(n)** | **O(1)** | ✅ |

**The decision: a single pass with one counter**, a [sliding-window](../learning/03-sliding-window.md)-style "extend or reset" greedy. The state we need at each `i` is only the run length ending there and the last three values, which we can read straight from the array.

The condition "`i-1` is a strict peak or a strict valley relative to its neighbours" is `(arr[i-2] < arr[i-1] > arr[i]) or (arr[i-2] > arr[i-1] < arr[i])`. Python's chained comparisons write it directly.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
best = 1
current = 1
```

Every non-empty array has a turbulent subarray of length 1. `current` is the length of the turbulent run ending at the current index.
→ [variables-assignment](../syntax/variables-assignment.md)

```python
for i in range(1, len(arr)):
    if arr[i] == arr[i - 1]:
        current = 1
```

**Equal neighbours** end any run. The new run restarts at length 1 (just `arr[i]`).
→ [for-loop](../syntax/for-loop.md) · [range-function](../syntax/range-function.md) · [comparison-operators](../syntax/comparison-operators.md)

```python
    elif i >= 2 and (arr[i - 2] < arr[i - 1] > arr[i] or arr[i - 2] > arr[i - 1] < arr[i]):
        current += 1
```

**The sign flipped.** The middle element `arr[i-1]` is a strict peak or valley, so the run that ended at `i-1` continues. A chained comparison reads like the picture: `a < b > c`.
→ [chained-comparisons](../syntax/chained-comparisons.md) · [logical-operators](../syntax/logical-operators.md) · [elif-else](../syntax/elif-else.md)

```python
    else:
        current = 2
```

**Different, but not alternating** (for example `1, 2, 3`, or the very first pair). The longest turbulent run ending here is only the last two elements.

```python
    best = max(best, current)
return best
```

Record the best after each step.
→ [min-max-key](../syntax/min-max-key.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def maxTurbulenceSize(self, arr: List[int]) -> int:
        best = 1
        current = 1

        for i in range(1, len(arr)):
            if arr[i] == arr[i - 1]:
                current = 1
            elif i >= 2 and (arr[i - 2] < arr[i - 1] > arr[i] or arr[i - 2] > arr[i - 1] < arr[i]):
                current += 1
            else:
                current = 2
            best = max(best, current)

        return best
```

</details>

**Trace it.** `arr = [9, 4, 2, 10, 7, 8, 8, 1, 9]`:

| `i` | Triple / pair | Case | `current` | `best` |
|---|---|---|---|---|
| 1 | `9, 4` | different, first pair | 2 | 2 |
| 2 | `9, 4, 2` | no flip (down, down) | 2 | 2 |
| 3 | `4, 2, 10` | valley | 3 | 3 |
| 4 | `2, 10, 7` | peak | 4 | 4 |
| 5 | `10, 7, 8` | valley | 5 | **5** |
| 6 | `8, 8` | equal | 1 | 5 |
| 7 | `8, 8, 1` | no flip, restart pair | 2 | 5 |
| 8 | `8, 1, 9` | valley | 3 | 5 |

**5** ✅.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n):** a single pass, constant work per element.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1):** two integers.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "A turbulent run means every interior element is a strict peak or strict valley. So I scan once with a running length. If two neighbours are equal, the run is broken, so it resets to 1. If the previous element is a strict peak or valley relative to its two neighbours, the run extends by one. Otherwise the elements differ but didn't alternate, so the best run ending here is just that pair, length 2. I track the maximum. O(n) time, O(1) space."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "DP version?" | `up[i]` = longest turbulent run ending at `i` with the last step going up, `down[i]` similarly. `up[i] = down[i-1] + 1` if `arr[i] > arr[i-1]`, else 1 |
| "Return the subarray?" | Remember the start index of the current run |
| "Allow equal elements?" | Then "flip" needs a definition for ties. The problem forbids them |
| "Related?" | [Wiggle Subsequence](376-wiggle-subsequence.md) (not contiguous, solved with the same up/down idea) |
| "Why reset to 2 and not 1?" | The pair `(arr[i-1], arr[i])` is itself turbulent, because the elements differ |

**Traps:**

- **Resetting to 1 on a non-flip** (should be 2).
- **Forgetting `i >= 2`** and indexing `arr[-1]`.
- **Treating equal neighbours as non-flipping** and resetting to 2. They must reset to 1.
- **Not updating `best` on resets.** The array `[1, 2]` needs `best = 2`.

**This same move shows up in:** [Wiggle Subsequence](376-wiggle-subsequence.md) · [Maximum Subarray](53-maximum-subarray.md) (extend or restart) · [Longest Repeating Character Replacement](424-longest-repeating-character-replacement.md).

</details>

---
