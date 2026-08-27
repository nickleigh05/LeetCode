# 219. Contains Duplicate II

**Easy** · [LeetCode](https://leetcode.com/problems/contains-duplicate-ii/) · [Solution file (no hints)](../../problems/0001-0499/219.py)

[📖 03. Sliding Window lesson](../learning/03-sliding-window.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 03. Sliding Window problems](../rmap-practice/03-sliding-window.md)

---

Given an integer array `nums` and an integer `k`, return `true` if there are two **distinct indices** `i` and `j` such that `nums[i] == nums[j]` and `abs(i - j) <= k`.

```
nums = [1,2,3,1],     k = 3  →  true    (indices 0 and 3, distance 3)
nums = [1,0,1,1],     k = 1  →  true    (indices 2 and 3, distance 1)
nums = [1,2,3,1,2,3], k = 2  →  false   (nearest equal pair is distance 3)
```

**Constraints:** `1 <= nums.length <= 10⁵` · `-10⁹ <= nums[i] <= 10⁹` · `0 <= k <= 10⁵`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "`nums[i] == nums[j]`" | Duplicate detection — the [Contains Duplicate](217-contains-duplicate.md) primitive |
| "`abs(i - j) <= k`" | ⚠️ **The new constraint.** Duplicates only count if they're *near each other* |
| "**distinct** indices" | An element can't pair with itself |
| return `true`/`false` | Existence only — bail out on the first hit |
| `n` up to 10⁵ | O(n·k) could be 10¹⁰ — dead. Need O(n) |
| `k` can be **0** | Then no valid pair exists (distance would have to be 0, meaning `i == j`). Must return `false` |
| values up to ±10⁹ | Huge range, small count — hash, don't index by value |

This is [Contains Duplicate](217-contains-duplicate.md) with a **locality** requirement bolted on. The original question was:

> "Have I seen this value **before**?"

The new one is:

> "Have I seen this value **within the last `k` positions**?"

That shift from *ever* to *recently* is exactly what a sliding window provides. Instead of remembering everything, remember only a moving suffix of the array.

Two equivalent framings, both worth knowing:

1. **Window of values** — maintain a set containing the last `k` elements. A hit inside that set means a nearby duplicate.
2. **Map of last positions** — store value → most recent index, and check `i - last[value] <= k`.

The first is the one in the solution file, and it's tidier; the second generalizes better to variants.

🤔 **Before you open the next section:** if your memory only ever holds the most recent `k` elements, what has to happen each time you move forward one position?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Brute force | For each `i`, check the next `k` positions | O(n·k) | O(1) | ❌ 10¹⁰ worst case |
| Full hash map of all indices | value → list of every index; scan for a near pair | O(n) avg | O(n) | ⚠️ Correct, stores far more than needed |
| **Hash map, last index only** | value → most recent index; compare distances | **O(n)** | O(n) | ✅ |
| **Sliding window set of size `k`** | Set holds the last `k` values; evict as you go | **O(n)** | **O(min(n,k))** | ✅ |

**The decision: a set acting as a fixed-size sliding window.**

The invariant, and it's the thing to state out loud:

> **After processing index `i`, the set contains exactly the values at indices `[i-k+1 … i]`** — the last `k` elements.

Given that, membership in the set *is* the answer: if `nums[i]` is already there, some equal value sits within `k` positions. No arithmetic on indices required — the window's contents encode the distance constraint structurally.

**Maintaining the window** takes two steps per iteration:

1. **Check then add** — check *before* inserting, or every element finds itself (the same ordering discipline as [Contains Duplicate](217-contains-duplicate.md)).
2. **Evict when oversized** — if the set exceeds `k` elements, remove the one that just fell out of range.

**Why the eviction index is `i - k`.** After adding `nums[i]`, the window should span `[i-k+1, i]`. The element that just dropped off the left edge is the one immediately before that span: index `i - k`. Same arithmetic as [Maximum Average Subarray I](643-maximum-average-subarray-i.md).

**Why `len(window) > k` and not `>= k`.** The window is allowed to hold exactly `k` values. Only when it grows to `k + 1` is something too old, so evict on strictly greater.

**The `k = 0` case falls out for free** — a pleasant property worth noticing. Adding `nums[i]` makes the set size 1, which is `> 0`, so we immediately evict `nums[i - 0] = nums[i]`. The set is emptied every iteration, nothing is ever found, and the function correctly returns `false`.

**The alternative — map of last indices:**

```python
last = {}
for i, n in enumerate(nums):
    if n in last and i - last[n] <= k:
        return True
    last[n] = i
return False
```

Equally O(n), equally correct, and it generalizes more readily (e.g. to a *value*-difference constraint as well, as in [LeetCode 220](https://leetcode.com/problems/contains-duplicate-iii/)). Storing only the **most recent** index is safe because a nearer duplicate is always at least as good as a farther one.

**Why not store all indices per value?** Unnecessary — only the closest one can matter, and that's always the latest.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
window = set()
```

The window's contents. A [set](../data-structures/hashset.md) because the only question asked of it is membership, in O(1).
→ [set-basics](../syntax/set-basics.md)

```python
for i, n in enumerate(nums):
```

`enumerate` because both the value (for membership) and the index (for eviction arithmetic) are needed.
→ [enumerate](../syntax/enumerate.md)

```python
    if n in window:
        return True
```

**Check before adding.** At this moment `window` holds only the previous `k` elements, so a hit is a genuine nearby duplicate. Adding first would make every element match itself.
→ [membership-operators](../syntax/membership-operators.md) · [if-return](../syntax/if-return.md)

```python
    window.add(n)
```

Record the current value.

```python
    if len(window) > k:
        window.remove(nums[i - k])
```

**Evict the element that just left the window.**

- `len(window) > k` — only when the window has grown to `k + 1` is something stale.
- `nums[i - k]` — the value at the index that just fell off the left edge.

This is why the set stays exactly the right size and why membership means "within `k`."

Note the guard also handles the early iterations: for `i < k` the window hasn't filled yet, `len(window) <= k`, and no eviction happens — so `nums[i - k]` (which would be a negative index) is never evaluated. Python's negative indexing would silently do the wrong thing here, so this ordering is load-bearing, not incidental.
→ [set-operations](../syntax/set-operations.md)

```python
return False
```

The whole array was scanned with no nearby duplicate found.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:

        window = set()

        for i, n in enumerate(nums):
            if n in window:
                return True

            window.add(n)

            if len(window) > k:
                window.remove(nums[i - k])

        return False
```

</details>

**Trace it** — `nums = [1, 2, 3, 1]`, `k = 3`:

| `i` | `n` | `window` before | In it? | After add | Size > 3? | Evict | `window` after |
|---|---|---|---|---|---|---|---|
| 0 | 1 | `{}` | no | `{1}` | 1 > 3? no | — | `{1}` |
| 1 | 2 | `{1}` | no | `{1,2}` | no | — | `{1,2}` |
| 2 | 3 | `{1,2}` | no | `{1,2,3}` | 3 > 3? no | — | `{1,2,3}` |
| 3 | 1 | `{1,2,3}` | **yes** | — | — | — | `return True` ✅ |

**And a `false` case** — `nums = [1,2,3,1,2,3]`, `k = 2`:

| `i` | `n` | In window? | After add | Evict `nums[i-2]` | `window` after |
|---|---|---|---|---|---|
| 0 | 1 | no | `{1}` | — | `{1}` |
| 1 | 2 | no | `{1,2}` | — | `{1,2}` |
| 2 | 3 | no | `{1,2,3}` → size 3 > 2 | `nums[0]=1` | `{2,3}` |
| 3 | 1 | no | `{1,2,3}` → 3 > 2 | `nums[1]=2` | `{1,3}` |
| 4 | 2 | no | `{1,2,3}` → 3 > 2 | `nums[2]=3` | `{1,2}` |
| 5 | 3 | no | `{1,2,3}` → 3 > 2 | `nums[3]=1` | `{2,3}` |

Return `False` ✅ — the duplicate `1`s sit at indices 0 and 3, distance 3 > `k = 2`, and the eviction at `i = 3` is precisely what removed the stale `1` before it could be found.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

One pass, and each iteration does a bounded amount of work: one membership test, one insert, at most one removal — all O(1) average on a set.

Notably **independent of `k`**: the window's *size* changes, but the per-step cost doesn't.

**Compare to brute force:** O(n·k), which at `n = k = 10⁵` is 10¹⁰. The window converts "scan the next `k` positions" into "one hash lookup."

**Best case** is much better than the bound: `[1,1,...]` returns on the second iteration. O(n) is the worst case — no nearby duplicate anywhere.

The usual hashing asterisk applies: O(1) is *average*, degrading with adversarial collisions.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(min(n, k))</summary>

**O(min(n, k))** — and the `min` matters.

The set never exceeds `k` elements by construction, and it obviously can't exceed `n` either. So:

- `k` small (say 5): the set holds at most 5 values — **effectively O(1)**
- `k >= n`: no eviction ever fires, and this degenerates to [Contains Duplicate](217-contains-duplicate.md) with **O(n)** space

That's a strict improvement over storing every value seen. When `k` is small relative to `n` — the common case — the saving is large.

| | Space |
|---|---|
| Set of all seen values | O(n) |
| Map value → last index | O(n) |
| **Window set** | **O(min(n, k))** ✅ |

**The transferable idea:**

> **When a problem constrains *how far back* something can be, you only need to remember that far back.** Bounded history means bounded memory.

The same reasoning gives [Minimum Size Subarray Sum](209-minimum-size-subarray-sum.md) and [Longest Substring Without Repeating Characters](3-longest-substring-without-repeating-characters.md) their space bounds, and it's the essence of streaming algorithms generally.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "It's Contains Duplicate with a distance limit, so instead of remembering every value I've seen, I only remember the last `k`. I keep a set as a sliding window: check membership before inserting — a hit means an equal value within `k` positions — then add the current value, and if the set has grown past `k`, evict `nums[i-k]`, the element that just fell off the left edge. O(n) time, O(min(n,k)) space. The `k = 0` case works for free, since the set is emptied every iteration. An equivalent version stores value → most recent index and checks `i - last[value] <= k`, which generalizes better if a value-difference constraint gets added."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Also require `abs(nums[i] - nums[j]) <= t`." | [LeetCode 220](https://leetcode.com/problems/contains-duplicate-iii/) — a set can't answer *nearest value*. Use bucketing by `t`, or a sorted container with `bisect`. O(n) or O(n log k). |
| "Return the **indices**." | Switch to the map version and return `(last[n], i)`. |
| "Why check before adding?" | Otherwise every element finds itself and you return `true` for any input. |
| "Why `> k` rather than `>= k`?" | The window legitimately holds `k` values; only at `k+1` is one stale. |
| "What if `k = 0`?" | `false` always — the set is cleared each iteration, so nothing can match. Falls out with no special case. |
| "Count nearby duplicate pairs instead." | The set is no longer enough — use a map value → deque of indices, evicting stale ones from the front. |
| "Streaming input, unknown length?" | Already streaming: one pass, bounded memory, no random access beyond `nums[i-k]` (which a deque of the last `k` values would supply). |

**Traps:**

- **Adding before checking.** Every element matches itself; returns `true` universally.
- **Evicting the wrong index.** It's `nums[i - k]`, not `nums[i - k + 1]` or `nums[i - k - 1]`. Off by one and the window silently misaligns.
- **Using `>=` for the size check.** Evicts too eagerly, shrinking the effective window to `k-1` and missing valid pairs at exactly distance `k`.
- **Evicting before the size check.** For `i < k` the index `i - k` is negative, and Python happily wraps around to the end of the array — removing a value that's still in range, or raising `KeyError`.
- **Storing every index per value.** Only the most recent one can ever be closest; the rest is wasted memory.
- **Falling back on brute force** because `k` "looks small." It can be 10⁵.

**This same move shows up in:** [Contains Duplicate](217-contains-duplicate.md) (the unbounded-history version this refines) · [Maximum Average Subarray I](643-maximum-average-subarray-i.md) (the same fixed-window slide, with a sum instead of a set) · [Longest Substring Without Repeating Characters](3-longest-substring-without-repeating-characters.md) (a *variable*-size window over a set) · [Find All Anagrams in a String](438-find-all-anagrams-in-a-string.md) (fixed window over a frequency map).

</details>

---
