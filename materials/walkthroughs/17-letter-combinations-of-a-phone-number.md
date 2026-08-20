# 17. Letter Combinations of a Phone Number

**Medium** · [LeetCode](https://leetcode.com/problems/letter-combinations-of-a-phone-number/)

[📖 11. Backtracking lesson](../learning/11-backtracking.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 11. Backtracking problems](../rmap-practice/11-backtracking.md)

> *Not yet solved in this repo — no solution file to compare against.*

---

Given a string containing digits from `2`–`9`, return **all possible letter combinations** the number could represent, in any order.

The digit-to-letter mapping is the standard telephone keypad (note that `1` maps to nothing):

```
2 → abc    3 → def    4 → ghi    5 → jkl
6 → mno    7 → pqrs   8 → tuv    9 → wxyz
```

```
digits = "23"  →  ["ad","ae","af","bd","be","bf","cd","ce","cf"]
digits = ""    →  []
digits = "2"   →  ["a","b","c"]
```

**Constraints:** `0 <= digits.length <= 4` · each digit is in the range `['2', '9']`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "**all possible** combinations" | Enumerate everything → backtracking |
| each digit → 3 or 4 letters | ⚠️ The **branching factor varies per level** — that's the only thing new here |
| combinations have length = `len(digits)` | Every digit contributes exactly one letter, so all results are the same length |
| "in any order" | No sorting needed |
| `digits` may be **empty** | ⚠️ Must return `[]`, not `[""]` — an explicit guard |
| length ≤ 4 | At most 4⁴ = 256 results. Tiny |

**The structure is a Cartesian product.** For `"23"`, you pick one letter from `{a,b,c}` and one from `{d,e,f}` — 3 × 3 = 9 combinations:

```
        ""
   a ╱  b │  c ╲
  "a"   "b"   "c"
 ╱ | ╲   …     …
ad ae af

3 × 3 = 9 ✅
```

**Every digit contributes exactly one letter**, so unlike [Subsets](78-subsets.md) there's no include/exclude decision — the choice is *which* letter, not *whether*.

**What's genuinely new: the branch count varies by level.** In [Subsets](78-subsets.md) every node branched 2 ways; in [Permutations](46-permutations.md) it shrank predictably. Here it's **3 or 4 depending on which digit you're at** — `7` and `9` have four letters, the rest have three.

That changes nothing structurally: the loop simply iterates over whatever letters *this* digit offers. But it's why the complexity is stated as a range, O(3ⁿ) to O(4ⁿ).

**The empty-input trap.** With `digits = ""`, the base case fires immediately and records `""` — giving `[""]` when the answer should be `[]`. A guard at the top is the fix, and it's the detail this problem is really testing.

🤔 **Before you open the next section:** if you didn't guard the empty input, what would the base case do on the very first call?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Verdict |
|---|---|---|
| Nested loops | One loop per digit | ❌ Only works for a fixed digit count |
| **Backtracking** | One recursion level per digit | ✅ |
| Iterative building | Start with `[""]`; for each digit, extend every partial with each letter | ✅ Equally good |
| `itertools.product` | `["".join(p) for p in product(*letter_lists)]` | ⚠️ Right in production; sidesteps the exercise |

**The decision: backtracking, one level per digit.**

The structure is the simplest in the unit:

1. **Base case** — index reached the end ⇒ the combination is complete, join and record.
2. **Loop** over the letters for the current digit.
3. **Choose → explore → un-choose.**

**Why there's no `start` index and no `used` array.** Compare across the unit:

| Problem | Mechanism | Why |
|---|---|---|
| [Subsets](78-subsets.md) | `start` index | prevent reorderings of a selection |
| [Permutations](46-permutations.md) | `used` array | prevent reusing an element |
| **17** | **neither** | ⚠️ Each level draws from a **different pool** — the letters of *that* digit |

Nothing can collide, because digit 2's letters and digit 3's letters are separate alphabets. **When the levels don't share a pool, no bookkeeping is needed** — that's the observation worth taking away.

**Why `"".join(path)` at the base case.** `path` is a list of characters; joining once at the end is O(n). Concatenating strings on the way down (`path + letter`) would allocate a new string per level — the same immutable-vs-mutable trade discussed in [Generate Parentheses](22-generate-parentheses.md), where strings were used and no explicit undo was needed.

Here the list-plus-undo version wins on allocation, at the cost of the `pop()`.

**Why the empty guard is mandatory.** Without `if not digits: return []`, the first call has `i == 0 == len(digits)`, so the base case records `"".join([])` = `""` — returning `[""]` instead of `[]`. LeetCode tests this explicitly.

**The iterative alternative** builds results breadth-first: start with `[""]` and, for each digit, replace the list with every existing partial extended by every letter of that digit. Same complexity, no recursion — worth mentioning.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
if not digits:
    return []
```

**The empty-input guard**, and the detail this problem is really testing.

Without it the base case fires on the first call and records the empty string, returning `[""]` — which is wrong. An empty input has *no* combinations, not one empty combination.
→ [truthy-falsy-values](../syntax/truthy-falsy-values.md) · [if-return](../syntax/if-return.md)

```python
digit_to_letters = {
    "2": "abc", "3": "def", "4": "ghi", "5": "jkl",
    "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz",
}
```

The keypad mapping. Values are **strings**, and iterating a string yields its characters — so no list conversion is needed.

Note `7` and `9` have **four** letters while the rest have three; that's the source of the variable branching factor.
→ [dict-basics](../syntax/dict-basics.md) · [string-basics](../syntax/string-basics.md)

```python
result = []
path = []

def backtrack(i):
    if i == len(digits):
        result.append("".join(path))
        return
```

**Base case: every digit has contributed a letter.**

`"".join(path)` converts the list of characters into a string — a single O(n) allocation, versus building strings incrementally at every level.

Note this joins rather than copying with `path[:]`, because the result is a **string** not a list — and the join inherently creates a new object, so no separate copy is needed.
→ [recursion-basics](../syntax/recursion-basics.md) · [string-join-slice](../syntax/string-join-slice.md)

```python
    for letter in digit_to_letters[digits[i]]:
```

**Look up this digit's letters and loop over them.** `digits[i]` is the current digit character; the dict maps it to its letter string; iterating that string gives one character at a time.

This is where the branching factor varies — 3 letters for most digits, 4 for `7` and `9`.
→ [for-loop](../syntax/for-loop.md)

```python
        path.append(letter)
        backtrack(i + 1)
        path.pop()
```

**Choose → explore → un-choose**, the [Subsets](78-subsets.md) skeleton with no extra bookkeeping.

`i + 1` advances to the next digit. There's no `start` and no `used` array because each level draws from a **different pool** — digit 2's letters can't collide with digit 3's.
→ [list-methods](../syntax/list-methods.md)

```python
backtrack(0)
return result
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def letterCombinations(self, digits: str) -> List[str]:

        if not digits:
            return []

        digit_to_letters = {
            "2": "abc", "3": "def", "4": "ghi", "5": "jkl",
            "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz",
        }

        result = []
        path = []

        def backtrack(i):
            if i == len(digits):
                result.append("".join(path))
                return

            for letter in digit_to_letters[digits[i]]:
                path.append(letter)
                backtrack(i + 1)
                path.pop()

        backtrack(0)
        return result
```

</details>

**Trace it** — `digits = "23"`:

```
                backtrack(0)   path=[]
        a ╱          b │          ╲ c
  path=[a]        path=[b]      path=[c]
  ╱  |  ╲          ╱ | ╲         ╱ | ╲
 d   e   f        d  e  f       d  e  f
"ad" "ae" "af"  "bd" "be" "bf" "cd" "ce" "cf"
```

Following the first branch and its first backtrack:

| Call | Action | `path` | Recorded |
|---|---|---|---|
| `backtrack(0)` | append `a` | `[a]` | |
| `backtrack(1)` | append `d` | `[a,d]` | |
| `backtrack(2)` | base case | | **`"ad"`** ✅ |
| back in `backtrack(1)` | **pop** | `[a]` | |
| | append `e` | `[a,e]` | |
| `backtrack(2)` | base case | | **`"ae"`** ✅ |
| … | | | |
| back in `backtrack(0)` | **pop** | `[]` | |
| | append `b` | `[b]` | … |

Result: `["ad","ae","af","bd","be","bf","cd","ce","cf"]` ✅ — 3 × 3 = **9** combinations.

**And the empty case:** `digits = ""` hits the guard and returns `[]` immediately. Without the guard, `backtrack(0)` would see `0 == len("")` and record `""`, giving the wrong `[""]`.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(4ⁿ · n)</summary>

**O(4ⁿ · n)**, where n = `len(digits)`.

- **Between 3ⁿ and 4ⁿ combinations** — each digit multiplies the count by its letter count (3 for most, 4 for `7` and `9`).
- **O(n) per combination** for the `"".join(path)`.

The standard bound is **O(4ⁿ · n)**, using the worst-case branching factor.

At n = 4 (the maximum) that's at most 4⁴ × 4 = **1,024 operations** — instant. The tiny constraint confirms exponential is expected.

**This is output-bound and optimal.** You must produce every combination, so Ω(4ⁿ · n) is unavoidable. No polynomial algorithm exists — the same conclusion as every enumeration problem in this unit.

**Comparing the growth rates across the unit:**

| Problem | Count | Why |
|---|---|---|
| [Subsets](78-subsets.md) | **2ⁿ** | 2 choices per element (in/out) |
| **17** | **3ⁿ–4ⁿ** | 3–4 choices per digit |
| [Permutations](46-permutations.md) | **n!** | shrinking choices, n × (n−1) × … |

Same skeleton, different branching — and the constraints scale inversely with growth (n ≤ 10, ≤ 4, ≤ 6 respectively). **Reading the constraint tells you which growth rate is expected.**

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n) auxiliary</summary>

**O(n) auxiliary**, plus O(4ⁿ · n) for the required output.

| Component | Size |
|---|---|
| `result` (required output) | up to 4ⁿ strings of length n |
| Recursion depth | exactly n — one frame per digit → **O(n)** |
| `path` | exactly n characters at maximum → O(n) |
| `digit_to_letters` | 8 entries → **O(1)** |

So: **"O(n) auxiliary, plus the exponential output."**

**The mutable-list-plus-join choice matters here.** Two ways to build the strings:

| Approach | Per-frame cost |
|---|---|
| **`path` list + `"".join()` at the leaf** | O(1) append, one O(n) join per result |
| String concatenation (`path + letter`) | **O(n) allocation at every level** |

The concatenation version — used in [Generate Parentheses](22-generate-parentheses.md) — needs no explicit undo, since a fresh string is created per branch. But it allocates O(n) per frame, giving O(n²) along a root-to-leaf path.

**The trade, stated plainly:** *immutable strings buy you automatic backtracking at the cost of allocation; a mutable list is cheaper but you must undo manually.* Both appear in this unit deliberately.

**The recursion is n deep, not 4ⁿ** — one frame per digit, only one path live at a time.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "This is a Cartesian product — one letter chosen from each digit's set — so it's backtracking with one recursion level per digit. What's different from the other problems in this unit is that I need *neither* a `start` index nor a `used` array, because each level draws from a completely different pool: digit 2's letters can't collide with digit 3's. So the loop just iterates over whatever letters the current digit offers, and the branching factor varies — 3 for most digits, 4 for 7 and 9. I build the combination in a list and join once at the base case, which is cheaper than concatenating strings at every level. The one detail worth guarding is empty input: without an explicit check the base case fires immediately and returns `[\"\"]` instead of `[]`. O(4ⁿ·n), output-bound."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why no `start` or `used`?" | **The question.** Each level draws from a different alphabet, so no choice can collide with another. Bookkeeping exists to prevent collisions within a shared pool. |
| "Why the empty-input guard?" | Otherwise the base case fires on the first call and records `""`, returning `[""]` instead of `[]`. |
| "Solve it iteratively." | Start with `[""]`; for each digit, replace the list with every partial extended by each of that digit's letters. |
| "Use the standard library." | `itertools.product(*[mapping[d] for d in digits])`, then join each tuple. Right in production. |
| "What if a digit mapped to no letters, like `1`?" | The loop body never runs, so that branch produces nothing — and the whole result becomes empty. Worth clarifying whether `1` should be skipped or invalidate the input. |
| "Why does the complexity have a range?" | Digits `7` and `9` have four letters; the rest have three. So the count is between 3ⁿ and 4ⁿ. |
| "Build strings instead of a list?" | Works and needs no undo, since strings are immutable — but it allocates O(n) per level. |

**Traps:**

- **Missing the empty-input guard** — returns `[""]` instead of `[]`. The signature bug here.
- **Appending `path` instead of joining it** — you'd return lists of characters rather than strings.
- **Adding a `start` index or `used` array** out of habit. Neither applies; each level has its own pool.
- **Forgetting `path.pop()`** — characters accumulate across branches.
- **Building with `path + letter` and also popping** — mixing the two styles double-undoes.
- **Hard-coding nested loops.** Only works for a fixed number of digits.

**This same move shows up in:** [Subsets](78-subsets.md) (the skeleton) · [Generate Parentheses](22-generate-parentheses.md) (the immutable-string variant, no explicit undo) · [Permutations](46-permutations.md) (where levels *do* share a pool, hence `used`) · [Word Search](79-word-search.md) (variable branching per level) · [backtracking](../algorithms/backtracking.md).

</details>

---
