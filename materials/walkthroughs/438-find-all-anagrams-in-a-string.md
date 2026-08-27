# 438. Find All Anagrams in a String

**Medium** · [LeetCode](https://leetcode.com/problems/find-all-anagrams-in-a-string/) · [Solution file (no hints)](../../problems/0001-0499/438.py)

[📖 03. Sliding Window lesson](../learning/03-sliding-window.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 03. Sliding Window problems](../rmap-practice/03-sliding-window.md)

---

Given two strings `s` and `p`, return an array of all **start indices** of `p`'s anagrams in `s`. An anagram is a rearrangement of all the original letters.

```
s = "cbaebabacd", p = "abc"  →  [0, 6]    ("cba" at 0, "bac" at 6)
s = "abab",       p = "ab"   →  [0, 1, 2] ("ab", "ba", "ab")
```

**Constraints:** `1 <= s.length, p.length <= 3·10⁴` · lowercase English letters

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**anagram**" | Same **multiset** of characters — order is irrelevant, counts are everything |
| anagram of `p` | Every match has length exactly `len(p)` ⇒ ⚠️ **fixed-size window** |
| "all **start indices**" | Collect every match, not just the first |
| lowercase English | A 26-character alphabet — bounded, which is what keeps the comparison O(1) |
| `n` up to 3·10⁴ | O(n · m) could be 9·10⁸ — too slow. Need O(n) |

Two observations do all the work:

1. **Anagram ⇒ identical character counts.** Comparing sorted strings would also work, but sorting each window is O(m log m) per position. A frequency map compares in O(26).
2. **All candidates have length `len(p)`** — so this is the *fixed*-size window from [Maximum Average Subarray I](643-maximum-average-subarray-i.md), not the variable-size kind. No shrink logic, no validity loop; both edges move in lockstep.

The window's maintained quantity is a **frequency map**, and both operations are cheap:

- character entering → its count `+= 1`
- character leaving → its count `-= 1`

Then compare against `p`'s map. That comparison is where the one real subtlety lives.

🤔 **Before you open the next section:** if you compare two `Counter` objects for equality, what happens if one of them contains a key whose count has dropped to zero?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

Let `n = |s|`, `m = |p|`.

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Sort each window | Compare `sorted(window) == sorted(p)` | O(n · m log m) | O(m) | ❌ Far too slow |
| Rebuild a Counter per window | `Counter(s[i:i+m]) == pCount` | O(n · m) | O(m) | ❌ 9·10⁸ |
| **Slide a Counter** | Adjust by the two changing characters | **O(n · 26)** | **O(1)** | ✅ |
| **Slide with a `matches` counter** | Track how many characters have exactly the right count | **O(n)** | **O(1)** | ✅✅ Avoids the map comparison |

**The decision: a fixed window over a frequency map.** The solution file carries both variants.

**Variant 1 — compare maps directly.** Maintain `sCount` for the window, and check `sCount == pCount` at each position. Dictionary equality over ≤ 26 keys is O(26) = O(1), so the total is O(n).

**The critical detail: delete zero-count keys.**

```python
sCount[s[i - k]] -= 1
if sCount[s[i - k]] == 0:
    del sCount[s[i - k]]
```

`Counter` equality compares **keys and values**, so `Counter({'a':1,'b':0})` is **not** equal to `Counter({'a':1})`. A character that has fully left the window must have its key removed, or every subsequent comparison fails silently. This is the same discipline as in [Fruit Into Baskets](904-fruit-into-baskets.md), where a stale zero breaks `len()`.

**Variant 2 — track `matches`.** Instead of comparing whole maps, keep a count of how many *distinct characters* currently have exactly the right frequency. When it equals `len(pCount)`, the window is an anagram. Each slide updates `matches` in O(1), removing even the O(26) factor.

It's genuinely O(n) rather than O(26n), but it's fiddlier: when a character's count changes you must check whether it *entered* or *left* the matched state, and the ordering of those checks is easy to get wrong. **Write variant 1 first**; offer variant 2 as the optimization.

**Why not sort?** Sorting each window is O(m log m) per position — the classic "correct but quadratic" trap. Counting is the right tool whenever you need *multiset equality*, which is exactly what an anagram is. Same reasoning as [Valid Anagram](242-valid-anagram.md).

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
k = len(p)
pCount = Counter(p)
sCount = Counter(s[:k])
```

- `k` — the fixed window width
- `pCount` — the target frequency map, built once
- `sCount` — the first window's map, priming the slide

→ [counter](../syntax/counter.md)

```python
result = [0] if sCount == pCount else []
```

**Check the first window before sliding.** Easy to forget: the loop below starts at index `k`, so the window at index 0 is never re-examined. If it's already an anagram, record it now.
→ [ternary-expression](../syntax/ternary-expression.md)

```python
for i in range(k, len(s)):
```

`i` is the index of the character **entering** on the right. Starting at `k` is exactly the fixed-window pattern from [Maximum Average Subarray I](643-maximum-average-subarray-i.md).
→ [range-function](../syntax/range-function.md)

```python
    sCount[s[i]] += 1          # add incoming right char
```

The entering character. `Counter` returns 0 for a missing key, so no `if` is needed.

```python
    sCount[s[i - k]] -= 1      # remove outgoing left char
    if sCount[s[i - k]] == 0:
        del sCount[s[i - k]]   # keep Counter clean for == comparison
```

**The leaving character, and the mandatory cleanup.**

`i - k` is the index that just fell out of the window (which now spans `[i-k+1, i]`).

The `del` is not cosmetic. Without it, a fully-departed character leaves a `key: 0` entry, and `sCount == pCount` is then **never** true again — the function silently returns fewer matches, or none. This is the defining bug of the problem.
→ [dict-methods](../syntax/dict-methods.md)

```python
    if sCount == pCount:
        result.append(i - k + 1)
```

**Compare, and record the *start* index.** The window spans `[i-k+1, i]`, so its start is `i - k + 1` — not `i`, and not `i - k`. Getting this wrong shifts every answer by one.
→ [list-methods](../syntax/list-methods.md)

```python
return result
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:

        k = len(p)
        pCount = Counter(p)
        sCount = Counter(s[:k])
        result = [0] if sCount == pCount else []

        for i in range(k, len(s)):
            sCount[s[i]] += 1          # add incoming right char
            sCount[s[i - k]] -= 1      # remove outgoing left char

            if sCount[s[i - k]] == 0:
                del sCount[s[i - k]]   # keep Counter clean for == comparison

            if sCount == pCount:
                result.append(i - k + 1)

        return result
```

</details>

<details>
<summary>The `matches`-counter variant (also in the solution file)</summary>

```python
### Sliding Window + Frequency Map ###
class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        if len(p) > len(s):
            return []

        pCount = Counter(p)
        sCount = Counter(s[:len(p)])
        result = []
        matches = sum(1 for c in pCount if pCount[c] == sCount[c])
        ...
```

Rather than comparing maps, track how many characters currently have exactly the right count. A match is `matches == len(pCount)`. Each slide adjusts `matches` in O(1), making the whole thing O(n) with no 26-factor. Faster, but the state transitions need care — offer it as the optimization, not the first draft.

Note it also guards `len(p) > len(s)`, which the primary version handles implicitly (the loop simply never runs and the first-window check fails).

</details>

**Trace it** — `s = "cbaebabacd"`, `p = "abc"`, `k = 3`, `pCount = {a:1, b:1, c:1}`:

| Step | `i` | Window | Enter | Leave | `sCount` | Match? | `result` |
|---|---|---|---|---|---|---|---|
| prime | — | `"cba"` | — | — | `{c:1,b:1,a:1}` | ✅ | `[0]` |
| 1 | 3 | `"bae"` | `e` | `c` (del) | `{b:1,a:1,e:1}` | ❌ | `[0]` |
| 2 | 4 | `"aeb"` | `b` | `b` | `{b:1,a:1,e:1}` | ❌ | `[0]` |
| 3 | 5 | `"eba"` | `a` | `a` | `{b:1,a:1,e:1}` | ❌ | `[0]` |
| 4 | 6 | `"bab"` | `b` | `e` (del) | `{b:2,a:1}` | ❌ | `[0]` |
| 5 | 7 | `"aba"` | `a` | `b` | `{b:1,a:2}` | ❌ | `[0]` |
| 6 | 8 | `"bac"` | `c` | `b` | `{b:1,a:1,c:1}` | ✅ | `[0, 6]` |
| 7 | 9 | `"acd"` | `d` | `b` (del) | `{a:1,c:1,d:1}` | ❌ | `[0, 6]` |

Return **`[0, 6]`** ✅

At step 6 the recorded index is `i - k + 1 = 8 - 3 + 1 = 6`, which is where `"bac"` starts ✅

Steps 1, 4, and 7 show the `del` firing — without it, `sCount` would carry `c:0`, `e:0`, and `b:0`, and the step-6 comparison would fail.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)**, treating the 26-letter alphabet as a constant.

- Priming: O(m) to build `pCount` and the first `sCount`
- Sliding loop: `n - m` iterations, each doing two O(1) counter updates plus one map comparison

The comparison is **O(26) = O(1)** because both maps have at most 26 keys. So the loop is O(n · 26) = **O(n)**.

Strictly, with an alphabet of size `A` it's O(n · A). For general Unicode you'd prefer the `matches` variant, which is O(n) regardless of alphabet size.

**Compare:**

| | Time |
|---|---|
| Sort each window | O(n · m log m) |
| Rebuild Counter per window | O(n · m) = 9·10⁸ |
| **Slide the Counter** | **O(n · 26)** |
| **Slide with `matches`** | **O(n)** |

The slide converts "recompute `m` counts" into "adjust two counts."

</details>

<details>
<summary><b>5 · Space complexity</b> — O(1)</summary>

**O(1)** auxiliary — or **O(A)** for an alphabet of size `A`, which is 26 here.

Both counters hold at most 26 keys regardless of how long `s` and `p` are. That's a constant, so the space doesn't grow with the input.

The output list can hold up to `n - m + 1` indices, but that's required by the problem, not overhead.

The `s[:k]` slice in the priming step allocates O(m) briefly — avoidable with an explicit loop if you want strict O(1), though nobody will object.

**The general point:**

> **A window over a bounded alphabet has bounded state.** That's why counting-based window problems are O(1) space while prefix-sum-based ones ([Subarray Sum Equals K](560-subarray-sum-equals-k.md)) are O(n) — the number of distinct *sums* is unbounded, but the number of distinct *characters* is not.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "An anagram means identical character counts, and every candidate has length `len(p)` — so it's a fixed-size sliding window over a frequency map. I build `p`'s counts once, prime the window with the first `len(p)` characters, and check it. Then each step I add the entering character and remove the leaving one, and compare the maps. The important detail is deleting keys whose count hits zero, because `Counter` equality compares keys and values — a stale zero would make every later comparison fail. The comparison is O(26) since the alphabet is bounded, so it's O(n) overall with O(1) space. If I wanted to drop the 26-factor I'd track how many characters currently have the exact right count and compare that against the number of distinct characters in `p`."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Avoid comparing maps each step." | Track a `matches` counter — how many characters have exactly the right frequency. O(1) per step, O(n) total. |
| "Just check whether **one** permutation exists." | [Permutation in String](567-permutation-in-string.md) — same window, return `True` on the first match. |
| "What if the alphabet is Unicode?" | The map comparison becomes O(A). Use the `matches` variant to stay O(n). |
| "Why delete zero-count keys?" | `Counter({'a':1,'b':0}) != Counter({'a':1})`. A stale zero silently breaks every later comparison. |
| "Find anagrams of **any** word from a list?" | Group the words by sorted-letter signature, then check each window's signature — or run a window per distinct length. |
| "Longest substring that's an anagram of *some* prefix of `p`?" | Now the length varies — a variable-size window with a different validity test. |
| "Why not sort each window?" | O(m log m) per position. Counting gives multiset equality in O(1) amortized per step. |

**Traps:**

- **Not deleting zero-count keys.** *The* bug. Silently returns too few matches — and passes small tests where no character fully leaves.
- **Forgetting to check the first window.** The loop starts at `k`, so index 0 is never tested by it. `s = "ab", p = "ab"` catches this instantly.
- **Recording `i` or `i - k` instead of `i - k + 1`.** Off-by-one on every reported index.
- **Wrong leaving index.** It's `s[i - k]`, not `s[i - k + 1]`.
- **Rebuilding `Counter(s[i:i+k])` each step.** The O(n·m) brute force wearing a sliding-window costume.
- **Assuming `len(p) <= len(s)`.** The primary version degrades gracefully (empty result), but be explicit if asked.

**This same move shows up in:** [Permutation in String](567-permutation-in-string.md) (the same window, existence instead of all indices) · [Valid Anagram](242-valid-anagram.md) (the counting primitive underneath, without the window) · [Maximum Number of Vowels in a Substring](1456-maximum-number-of-vowels-in-a-substring-of-given-length.md) (fixed window over a simple counter) · [Minimum Window Substring](76-minimum-window-substring.md) (the Hard version — variable window with frequency matching).

</details>

---
