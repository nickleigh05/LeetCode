# 76. Minimum Window Substring

**Hard** · [LeetCode](https://leetcode.com/problems/minimum-window-substring/)

[📖 03. Sliding Window lesson](../learning/03-sliding-window.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 03. Sliding Window problems](../rmap-practice/03-sliding-window.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Given two strings `s` and `t`, return the **minimum window substring** of `s` that contains every character of `t`, **including duplicates**. If there is no such substring, return the empty string `""`.

The answer is guaranteed to be unique.

```
s = "ADOBECODEBANC", t = "ABC"  →  "BANC"
s = "a",             t = "a"    →  "a"
s = "a",             t = "aa"   →  ""       (only one 'a' available, two needed)
```

**Constraints:** `1 <= s.length, t.length <= 10⁵` · uppercase and lowercase English letters · **follow-up: can you do it in O(n)?**

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**minimum** window" | ⚠️ **Minimize**, not maximize — the opposite of every window problem so far. It flips when you shrink and when you record |
| "contains every character of `t`" | The window must **cover** `t`. Extra characters are allowed — unlike [Permutation in String](567-permutation-in-string.md), this is a superset, not an exact match |
| "**including duplicates**" | `t = "AABC"` needs **two** A's. Counts, not just presence — the `"a"/"aa"` example exists to enforce this |
| "**substring**" | Contiguous. A window |
| "`""` if none exists" | A no-answer case you must detect and report |
| n up to 10⁵ | O(n²) is 10¹⁰ → dead. The follow-up asks for **O(n)** |
| both cases of letters | 52 possible characters — use a dict, not a 26-slot array |

**The structural flip.** In [problems 3 and 424](3-longest-substring-without-repeating-characters.md), you grew the window and shrank only when it became **invalid**, recording the longest. Here it inverts:

- Grow right until the window becomes **valid** (covers `t`).
- Then shrink from the left **while it stays valid**, recording the smallest.
- The moment it breaks, resume growing.

*Maximize* → shrink while invalid, record after shrinking.
*Minimize* → shrink while **valid**, record *inside* the shrink loop.

**The efficiency problem.** Checking "does this window cover `t`?" by comparing full count maps is O(52) per step — survivable, but there's a cleaner way. Track a single counter of **how many distinct required characters are currently satisfied**, and compare it to the number of distinct characters in `t`. That turns validity into one integer comparison.

🤔 **Before you open the next section:** you need to know when the window covers `t`. What's the smallest amount of state that tells you that, without re-examining the whole window each step?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Brute force | Every substring, check coverage | O(n³) | ❌ |
| Every start, extend right | For each `left`, grow until valid | O(n²) | ❌ 10¹⁰ ops |
| Window + full map comparison | Compare `window` vs `need` each step | O(52n) | ⚠️ Correct and O(n) technically — but clumsy |
| **Window + `have`/`need_count` counter** | Validity as one integer check | **O(n)** | ✅ |

**The decision: a variable-size sliding window with two count maps and a `have` counter.**

The state you maintain:

- **`need`** — `character → how many are required`, built from `t`.
- **`window`** — `character → how many are currently inside the window`.
- **`need_count`** — the number of *distinct* characters in `t`.
- **`have`** — how many distinct required characters are currently **fully satisfied** (window count has reached the needed count).

Then validity is simply **`have == need_count`**.

**The subtlety in maintaining `have`** — get this exactly right and the rest is mechanical:

- On adding a character: increment `have` **only when `window[ch]` becomes exactly equal to `need[ch]`**. Use `==`, not `>=`. With `>=`, a third `A` when only two are needed would wrongly increment `have` again.
- On removing: decrement `have` **only when `window[ch]` drops strictly below `need[ch]`**. Going from 3 A's to 2 (when 2 are needed) is still satisfied — no change.

That `==` on the way in and `<` on the way out is the whole trick, and it's where nearly every bug in this problem lives.

**Why track `have` rather than compare maps?** Both are O(n) overall. But `have` makes the validity check a single integer comparison, updated in O(1) — and more importantly, it makes the code's *intent* legible. On a Hard problem, being able to state your invariant ("`have` counts fully-satisfied required characters") is most of the explanation.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
if not t:
    return ""
```

Guard the empty target. Nothing to cover, no meaningful window.
→ [if-return](../syntax/if-return.md) · [truthy-falsy-values](../syntax/truthy-falsy-values.md)

```python
need = {}
for ch in t:
    need[ch] = need.get(ch, 0) + 1
```

The requirements, **with multiplicity** — `t = "AABC"` gives `{A: 2, B: 1, C: 1}`. Same counting idiom as [Valid Anagram](242-valid-anagram.md).
→ [dict-basics](../syntax/dict-basics.md) · [dict-methods](../syntax/dict-methods.md) · [for-loop](../syntax/for-loop.md)

```python
window = {}
have = 0
need_count = len(need)
res = [-1, -1]
res_len = float("inf")
left = 0
```

The window's counts; `have` (satisfied distinct characters) versus `need_count` (required distinct characters — note `len(need)`, the number of **keys**, not `len(t)`).

`res` stores the best window's bounds and `res_len` its length, seeded to **infinity** so the first valid window always wins the comparison. That's the standard sentinel for a minimization.
→ [float-inf](../syntax/float-inf.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
for right, ch in enumerate(s):
    window[ch] = window.get(ch, 0) + 1
```

Grow. `enumerate` gives the index and character together — the index is needed to record the window bounds.
→ [enumerate](../syntax/enumerate.md)

```python
    if ch in need and window[ch] == need[ch]:
        have += 1
```

**Exactly `==`.** This character just *became* fully satisfied. A fourth `A` when 2 are needed leaves `window[ch] > need[ch]`, so `have` correctly doesn't move. Characters not in `need` are irrelevant — allowed in the window, just not tracked.
→ [membership-operators](../syntax/membership-operators.md) · [logical-operators](../syntax/logical-operators.md)

```python
    while have == need_count:
```

**The flip.** Shrink while the window is **valid**, not while invalid. Every iteration produces a smaller valid window — until it isn't valid any more.
→ [while-loop](../syntax/while-loop.md)

```python
        if (right - left + 1) < res_len:
            res = [left, right]
            res_len = right - left + 1
```

Record **inside** the shrink loop, because every pass here is a genuine valid candidate and they're getting progressively smaller. In the maximizing problems you recorded *after* shrinking; here it must happen during.
→ [comparison-operators](../syntax/comparison-operators.md)

```python
        window[s[left]] -= 1
        if s[left] in need and window[s[left]] < need[s[left]]:
            have -= 1
        left += 1
```

Evict the leftmost character. **Strictly `<`** — dropping from 3 A's to 2 when 2 are needed keeps it satisfied, so `have` shouldn't change. Only falling *below* the requirement breaks it and exits the loop.
→ [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
left, right = res
return s[left:right + 1] if res_len != float("inf") else ""
```

Slice out the best window. `+ 1` because slicing is exclusive at the end. If `res_len` is still infinity, no valid window was ever found → return `""`.
→ [tuple-unpacking](../syntax/tuple-unpacking.md) · [string-join-slice](../syntax/string-join-slice.md) · [ternary-expression](../syntax/ternary-expression.md)

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def minWindow(self, s: str, t: str) -> str:

        if not t:
            return ""

        need = {}
        for ch in t:
            need[ch] = need.get(ch, 0) + 1

        window = {}
        have = 0
        need_count = len(need)
        res = [-1, -1]
        res_len = float("inf")
        left = 0

        for right, ch in enumerate(s):
            window[ch] = window.get(ch, 0) + 1

            if ch in need and window[ch] == need[ch]:
                have += 1

            while have == need_count:
                if (right - left + 1) < res_len:
                    res = [left, right]
                    res_len = right - left + 1

                window[s[left]] -= 1
                if s[left] in need and window[s[left]] < need[s[left]]:
                    have -= 1
                left += 1

        left, right = res
        return s[left:right + 1] if res_len != float("inf") else ""
```

</details>

**Trace it** — `s = "ADOBECODEBANC"`, `t = "ABC"` (`need = {A:1, B:1, C:1}`, `need_count = 3`):

| `right` | char | `have` | Valid? | Shrink action | Best |
|---|---|---|---|---|---|
| 0–4 | `ADOBE` | 2 | no | — | — |
| 5 | `C` | **3** | ✅ | record `[0,5]` `"ADOBEC"` (6); evict `A` → `have` 2 | `"ADOBEC"` |
| 6–9 | `ODEB` | 2 | no | — | `"ADOBEC"` |
| 10 | `A` | **3** | ✅ | record `[5,10]` `"CODEBA"` (6)? — not shorter, skip; evict `C` → `have` 2 | `"ADOBEC"` |
| 11 | `N` | 2 | no | — | |
| 12 | `C` | **3** | ✅ | record `[9,12]` **`"BANC"` (4)** ✅; evict `B` → `have` 2 | **`"BANC"`** |

Answer: **`"BANC"`**.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n + m)</summary>

**O(n + m)**, where n = `len(s)` and m = `len(t)`.

- Building `need`: O(m).
- The outer `for`: n iterations, O(1) work each (a dict update, a comparison).
- The inner `while`: advances `left`, which starts at 0, only increases, and never passes `right` → at most n advances **in total across the whole run**.

Every character of `s` is added to the window exactly once and removed at most once → **O(n + m)**.

The same amortized argument as every window problem, and on a Hard it's worth stating explicitly because the nested loop looks quadratic:

> *"`left` and `right` each traverse `s` once, forward only. Each character enters and leaves the window at most once, so the total work is linear despite the nested loop."*

**What the `have` counter bought:** the map-comparison variant is O(52) per step — still O(n), but with a 52× constant. Tracking `have` makes validity a single integer comparison, so the constant is genuinely small.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(m)</summary>

**O(m)**, bounded by the alphabet — so **O(52) = O(1)** under these constraints.

- `need`: at most the distinct characters in `t` → O(m), and never more than 52.
- `window`: at most the distinct characters in `s` → also capped at 52.
- The counters and bounds: O(1).

**Both answers are defensible, and which you give matters:**

- **"O(m)"** — bounded by the distinct characters of `t`. The general answer, correct for any alphabet.
- **"O(1) here"** — because the problem restricts to 52 English letters.

State it as *"O(m) for the maps, which is O(1) under these constraints since the alphabet is 52 characters."* That covers both and shows you noticed the constraint rather than reciting a default.

⚠️ **Don't reach for a fixed 26-slot array** as [Permutation in String](567-permutation-in-string.md) did — this problem allows **both cases**, so 26 slots would collide uppercase with lowercase. A dict, or a 128-slot array, is required. Same lesson as always: **read the alphabet constraint.**

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "This is a sliding window, but minimizing rather than maximizing — so the structure flips: I grow right until the window is valid, then shrink from the left *while it stays valid*, recording the smallest as I go. For validity I need the window to cover `t` including duplicates, so I keep a `need` map from `t`, a `window` map, and a counter `have` of how many distinct required characters are fully satisfied. The window is valid when `have` equals the number of distinct characters in `t`. The delicate part is maintaining `have`: increment only when a count becomes *exactly* the required amount, decrement only when it drops *strictly below* — otherwise duplicates miscount it. O(n + m) time, and O(1) space here since the alphabet is 52 letters."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why `==` when adding and `<` when removing?" | **The question.** Extra copies beyond the requirement mustn't re-increment `have`, and dropping from surplus back to exactly-enough mustn't decrement it. Only crossing the threshold changes satisfaction. |
| "What if `t` has duplicates?" | Handled — `need` stores counts, not a set. Demo with `t = "AABC"`. |
| "Speed up when `s` is huge and `t` is tiny." | Precompute the indices in `s` of characters that appear in `t` and slide over just those — skips irrelevant characters entirely. A real optimization for sparse inputs. |
| "Return all minimum windows, not one." | The problem guarantees uniqueness; without it, collect every window whose length equals the final minimum (a second pass, or keep a list). |
| "Exact permutation instead of coverage?" | Then the window is fixed-size and you compare counts directly — that's [Permutation in String](567-permutation-in-string.md). |
| "How is this different from problems 3 and 424?" | Those maximize: shrink while *invalid*, record after. This minimizes: shrink while *valid*, record during. Same skeleton, inverted control flow. |

**Traps:**

- **`>=` instead of `==`** when incrementing `have` — duplicates inflate it and you'll accept invalid windows.
- **`<=` instead of `<`** when decrementing — you'll break out of the shrink loop too early and miss the true minimum.
- **`need_count = len(t)`** instead of `len(need)`. It's the number of **distinct** required characters. On `t = "AABC"` this silently makes the window never valid.
- **Recording after the shrink loop** instead of inside it. You'd record the first valid window and never the smaller ones.
- **Initializing `res_len = 0`** — no window is ever shorter, so nothing is recorded. Use infinity.
- **Forgetting the `""` case** — check `res_len` before slicing, or `res = [-1, -1]` produces a nonsense slice.
- **Using a 26-slot array.** Both letter cases are allowed here.

**This same move shows up in:** [Longest Substring Without Repeating Characters](3-longest-substring-without-repeating-characters.md) (the maximizing counterpart) · [Longest Repeating Character Replacement](424-longest-repeating-character-replacement.md) (count-map validity on the same skeleton) · [Permutation in String](567-permutation-in-string.md) (fixed-size, exact-match sibling) · [Valid Anagram](242-valid-anagram.md) (the counting idiom underneath all of them).

</details>
