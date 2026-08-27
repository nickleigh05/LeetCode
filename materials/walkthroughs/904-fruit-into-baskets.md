# 904. Fruit Into Baskets

**Medium** · [LeetCode](https://leetcode.com/problems/fruit-into-baskets/) · [Solution file (no hints)](../../problems/0500-0999/904.py)

[📖 03. Sliding Window lesson](../learning/03-sliding-window.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 03. Sliding Window problems](../rmap-practice/03-sliding-window.md)

---

You are visiting a row of fruit trees, where `fruits[i]` is the type of fruit on tree `i`. You have **two baskets**, each holding a single type of fruit, and unlimited capacity. Starting at any tree, you must pick **exactly one fruit from every tree** moving right, and stop when you hit a fruit that fits in neither basket. Return the **maximum number of fruits** you can pick.

```
fruits = [1,2,1]        →  3    (all three: types {1,2})
fruits = [0,1,2,2]      →  3    ([1,2,2], types {1,2})
fruits = [1,2,3,2,2]    →  4    ([2,3,2,2], types {2,3})
```

**Constraints:** `1 <= fruits.length <= 10⁵` · `0 <= fruits[i] < fruits.length`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**two** baskets, one type each" | ⚠️ At most **2 distinct values** in your selection |
| "start anywhere, move right, stop when blocked" | A **contiguous** run — a window |
| "one fruit from **every** tree" | No skipping. The selection is a genuine subarray |
| "**maximum** number of fruits" | Maximize the window length |
| `n` up to 10⁵ | O(n²) is 10¹⁰ — dead |
| fruit types are ints `< n` | Could be up to `n` distinct types, so no fixed-size array trick |

Strip away the orchard story and it's:

> **Find the longest contiguous subarray containing at most 2 distinct values.**

The framing is deliberately obfuscated — that's part of the exercise. Interviewers pose problems in domain language, and the skill being tested is translating "two baskets" into "at most 2 distinct."

Once translated, it's the standard variable-size sliding window, with validity defined by a **distinct count** rather than a sum or a budget:

```
for right in range(n):
    add fruits[right] to the window
    while more than 2 distinct types:
        remove fruits[left]; left += 1
    record window length
```

**Why a frequency map, not a set.** A set can tell you *which* types are present but not *how many* of each — so when you shrink, you wouldn't know whether removing one occurrence eliminates that type entirely. On `[1,2,1]` shrinking past the first `1` must **not** drop type 1 from the window, because another `1` remains. Counts are what make removal correct.

🤔 **Before you open the next section:** when you slide the left edge past an element, how do you decide whether its fruit type has actually left the window?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Brute force | Every `(start, end)`, count distinct types | O(n²) or O(n³) | O(n) | ❌ 10¹⁰ |
| Track last-seen positions of 2 types | Manually juggle two types and a boundary | O(n) | O(1) | ⚠️ Correct, but fiddly and easy to get wrong |
| **Window + frequency map** | Grow right; shrink while > 2 distinct | **O(n)** | **O(1)** | ✅ |

**The decision: a variable-size window with a frequency map.**

State is `basket`, mapping fruit type → count within the window. Validity is `len(basket) <= 2`.

The three operations:

- **Grow:** `basket[fruits[right]] += 1`
- **Shrink:** decrement `basket[fruits[left]]`, and **delete the key when its count hits 0** — that's what shrinks `len(basket)`
- **Record:** after shrinking, `right - left + 1`

**The `del` is load-bearing, not tidiness.** Validity is measured by `len(basket)`, which counts *keys*, not counts. A key sitting at zero would still inflate `len(basket)` and cause the window to shrink when it shouldn't. Leaving zero-count keys in the map is the single most common bug here — and it's the same discipline required in [Find All Anagrams in a String](438-find-all-anagrams-in-a-string.md), where a stale zero would break a `Counter` equality check.

**Why `while` genuinely matters here.** Unlike [Max Consecutive Ones III](1004-max-consecutive-ones-iii.md) — where only one zero can enter per step, so one shrink always suffices — here a single shrink might not restore validity. You may need to remove *every* occurrence of a type before its key disappears. On `[1,1,1,2,3]`, adding `3` requires dropping all three `1`s before `len(basket)` falls back to 2. An `if` would leave the window invalid.

**Why record after the shrink loop.** We're maximizing, so shrink only as far as necessary and measure once valid — the same orientation as [Max Consecutive Ones III](1004-max-consecutive-ones-iii.md), and the mirror of [Minimum Size Subarray Sum](209-minimum-size-subarray-sum.md).

**Why not track two types manually?** You can maintain "the two current types and the start of the last run," but the bookkeeping around repeated types is error-prone. The frequency map generalizes to *k* baskets for free — just change `> 2` to `> k` — which is exactly the follow-up.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
basket = {}
left = 0
max_fruits = 0
```

- `basket` — fruit type → count inside the window. `len(basket)` is the number of distinct types.
- `left` — the window's left edge
- `max_fruits` — the best length seen

→ [dict-basics](../syntax/dict-basics.md)

```python
for right in range(len(fruits)):
    basket[fruits[right]] = basket.get(fruits[right], 0) + 1
```

**Grow.** Add the incoming fruit to the basket. `.get(key, 0)` handles first-sighting and repeat in one line — no `if key in basket` branch.
→ [dict-methods](../syntax/dict-methods.md) · [range-function](../syntax/range-function.md)

```python
    while len(basket) > 2:
```

**Shrink while invalid.** More than two distinct types means the window can't be picked with two baskets.

`while`, not `if` — restoring validity may require removing many elements, as shown above.
→ [while-loop](../syntax/while-loop.md)

```python
        basket[fruits[left]] -= 1
        if basket[fruits[left]] == 0:
            del basket[fruits[left]]
        left += 1
```

**Remove the leftmost fruit.** Decrement its count, and **delete the key when the count reaches zero** — that's the only thing that reduces `len(basket)` and ends the loop.

Without the `del`, `len(basket)` never shrinks, the `while` never exits, and you get an infinite loop (or an `IndexError` once `left` runs off the end).
→ [dict-methods](../syntax/dict-methods.md)

```python
    max_fruits = max(max_fruits, right - left + 1)
```

**Record after shrinking**, when the window holds at most 2 distinct types. `right - left + 1` is the inclusive length.
→ [min-max-key](../syntax/min-max-key.md)

```python
return max_fruits
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def totalFruit(self, fruits: List[int]) -> int:

        basket = {}
        left = 0
        max_fruits = 0

        for right in range(len(fruits)):
            basket[fruits[right]] = basket.get(fruits[right], 0) + 1

            while len(basket) > 2:
                basket[fruits[left]] -= 1
                if basket[fruits[left]] == 0:
                    del basket[fruits[left]]
                left += 1

            max_fruits = max(max_fruits, right - left + 1)

        return max_fruits
```

</details>

**Trace it** — `fruits = [1,2,3,2,2]`:

| `right` | `fruits[r]` | `basket` after add | Distinct > 2? | Shrink | `left` | Window | Len | `max` |
|---|---|---|---|---|---|---|---|---|
| 0 | 1 | `{1:1}` | no | — | 0 | `[1]` | 1 | 1 |
| 1 | 2 | `{1:1, 2:1}` | no | — | 0 | `[1,2]` | 2 | 2 |
| 2 | 3 | `{1:1, 2:1, 3:1}` | **yes (3)** | drop `1` → count 0 → **del** → `{2:1,3:1}` | 1 | `[2,3]` | 2 | 2 |
| 3 | 2 | `{2:2, 3:1}` | no | — | 1 | `[2,3,2]` | 3 | 3 |
| 4 | 2 | `{2:3, 3:1}` | no | — | 1 | `[2,3,2,2]` | **4** | **4** |

Return **4** ✅ — the window `[2,3,2,2]` at indices 1–4, using baskets for types 2 and 3.

**A trace where `while` shrinks repeatedly** — `fruits = [1,1,1,2,3]`:

| `right` | `basket` after add | Shrink steps | `left` | Window |
|---|---|---|---|---|
| 3 | `{1:3, 2:1}` | none | 0 | `[1,1,1,2]` len 4 |
| 4 | `{1:3, 2:1, 3:1}` | drop `1`→`{1:2,…}` still 3 distinct · drop `1`→`{1:1,…}` still 3 · drop `1`→ **del** → `{2:1,3:1}` | 3 | `[2,3]` len 2 |

Three shrinks for one insertion — an `if` would have left the window invalid with `{1:2, 2:1, 3:1}`.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).**

- Outer loop: `n` iterations.
- Inner `while`: `left` advances monotonically and never resets, so it moves at most `n` times **in total** across the whole run.

Each element is added once and removed at most once — at most `2n` dictionary operations, each O(1) average. **O(n)** overall.

**Say it out loud like this:** *"The nested `while` doesn't make it quadratic — the left pointer never moves backward, so total inner iterations are bounded by n."*

**Compare to brute force:** O(n²) at best (running a distinct-count per start), 10¹⁰ at the limit.

Optimal — every element must be examined.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** — and this deserves a precise justification, since a dictionary looks like it should be O(n).

The map holds at most **3** keys at any moment: the window is kept at ≤ 2 distinct types, and it can briefly reach 3 immediately after an insertion, before the shrink loop runs. Three is a constant, so the space is **O(1)** regardless of `n`.

More generally it's **O(k)** for the k-basket variant — still constant when `k` is fixed.

Contrast with problems where the map genuinely grows with the input:

| | Map size |
|---|---|
| **Fruit Into Baskets** | ≤ 3 keys — **O(1)** |
| [Longest Substring Without Repeating Characters](3-longest-substring-without-repeating-characters.md) | ≤ alphabet size — O(1) for fixed alphabets |
| [Subarray Sum Equals K](560-subarray-sum-equals-k.md) | up to `n` distinct prefix sums — **O(n)** |

The distinction is whether the problem **bounds** how much you're allowed to remember. Here "two baskets" is that bound, and it's handed to you in the statement.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "Translating the story: two baskets each holding one type means the picked run can contain at most 2 distinct values, and picking from every tree means it's contiguous. So it's the longest subarray with at most 2 distinct values — a variable-size sliding window. I keep a frequency map of types in the window, grow with the right pointer, and while there are more than 2 distinct types I shrink from the left, deleting a key when its count hits zero so `len(map)` actually drops. Then I record the length. The `while` matters because restoring validity can take many removals. O(n) time since the left pointer never resets, and O(1) space because the map holds at most 3 keys."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "At most **`k`** distinct values?" | Change `> 2` to `> k`. [LeetCode 340](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/) — identical code. |
| "**Exactly** `k` distinct?" | `atMost(k) - atMost(k-1)`. A standard and very reusable trick for "exactly" variants. |
| "Why delete zero-count keys?" | Validity is `len(map)`, which counts keys. A stale zero keeps the window shrinking forever — or loops infinitely. |
| "Why `while` and not `if`?" | One insertion can require many removals before a type's count reaches zero. `[1,1,1,2,3]` shows it. |
| "Return the fruit **types** used." | The keys of `basket` when `max_fruits` was last updated — snapshot them at that moment. |
| "Can you do it in O(1) space without a map?" | Yes — track the two current types and the start of the last run — but it's fiddly and doesn't generalize to `k`. |
| "Count subarrays with at most 2 distinct?" | Same window; add `right - left + 1` to a running total each step instead of taking a max. |

**Traps:**

- **Not deleting zero-count keys.** *The* bug. `len(basket)` never falls, so the `while` spins until `left` runs off the array.
- **Using a set instead of a map.** You can't tell when a type has genuinely left the window — `[1,2,1]` breaks immediately.
- **Using `if` instead of `while`.** Leaves the window invalid when multiple removals are needed.
- **Recording inside the shrink loop.** Measures invalid windows — correct for [209](209-minimum-size-subarray-sum.md), wrong here.
- **`len(basket) >= 2` as the shrink condition.** Two types is the *allowed* state; only three is invalid.
- **Assuming only two fruit types exist globally.** There can be up to `n`; the constraint is on the window, not the array.

**This same move shows up in:** [Longest Substring Without Repeating Characters](3-longest-substring-without-repeating-characters.md) (window with a distinct-character constraint) · [Max Consecutive Ones III](1004-max-consecutive-ones-iii.md) (same skeleton, counter-based validity) · [Longest Repeating Character Replacement](424-longest-repeating-character-replacement.md) (window over character frequencies with a budget) · [Minimum Window Substring](76-minimum-window-substring.md) (the Hard version — frequency-map validity in both directions).

</details>

---
