# 78. Subsets

**Medium** · [LeetCode](https://leetcode.com/problems/subsets/) · [Solution file (no hints)](../../problems/0001-0499/78.py)

[📖 10. Backtracking lesson](../learning/10-backtracking.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 10. Backtracking problems](../rmap-practice/10-backtracking.md)

---

Given an integer array `nums` of **unique** elements, return all possible **subsets** (the power set).

The solution set must not contain duplicate subsets. Return the answer in any order.

```
nums = [1,2,3]  →  [[], [1], [2], [1,2], [3], [1,3], [2,3], [1,2,3]]
nums = [0]      →  [[], [0]]
```

**Constraints:** `1 <= nums.length <= 10` · `-10 <= nums[i] <= 10` · all elements **unique**

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

This is the foundational problem of the unit. **The `append` → recurse → `pop` skeleton you learn here appears in every problem that follows**, so it's worth understanding structurally rather than memorizing.

| The statement says | Which really means |
|---|---|
| "**all possible** subsets" | Enumerate everything — that's a search over a decision tree, not a scan |
| "the **power set**" | Exactly **2ⁿ** subsets, including the empty set and the full set |
| "elements are **unique**" | ⚠️ No duplicate-handling needed — that's [Subsets II](90-subsets-ii.md)'s job |
| "no duplicate subsets" | Free here, since the elements are distinct |
| "any order" | No sorting of the output |
| **`n <= 10`** | ⚠️ A tiny bound — the classic signal that an **exponential** solution is expected |

**The reframe.** Don't think about "generating subsets". Think about walking through the elements and making **one binary decision each**:

```
[1,2,3]

           include 1?
        yes ╱        ╲ no
      include 2?     include 2?
     yes ╱  ╲ no    yes ╱ ╲ no
       …      …       …    …

8 leaves = 2³ subsets ✅
```

Every root-to-leaf path is one subset, and there are 2ⁿ of them because each of the n elements independently doubles the possibilities.

**The mechanical problem this creates.** You build the subset incrementally in a shared list. But after exploring the "include" branch, that list still contains the element — and the "exclude" branch must **not** see it. So you have to **undo** the choice before making the next one.

That's the defining shape of backtracking:

```
choose  →  explore  →  UN-choose
```

The un-choose step is what makes one shared list serve all 2ⁿ paths without them contaminating each other.

🤔 **Before you open the next section:** if you append the current subset to your results without copying it, what will all 2ⁿ entries in your output look like at the end?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Iterative doubling | Start with `[[]]`; for each element, add copies of everything with it appended | O(n·2ⁿ) | ✅ Elegant, worth knowing |
| Bitmask enumeration | For each of 2ⁿ masks, include element `i` if bit `i` is set | O(n·2ⁿ) | ✅ Neat; ties to Unit 18 |
| **Backtracking** | Include/exclude at each index, undoing between branches | **O(n·2ⁿ)** | ✅ |

All three are optimal — you must produce 2ⁿ subsets, so O(2ⁿ) is unavoidable. **Choose backtracking because it's the skeleton the rest of the unit builds on.**

**The structure:**

1. **Base case** — index reached the end ⇒ the current subset is complete, record a **copy**.
2. **Choice A** — include `nums[i]`, recurse, then **pop it back off**.
3. **Choice B** — exclude it, recurse.

**⚠️ The copy is not optional.** `subset` is one shared list mutated throughout the entire search. Appending it directly stores a *reference*, so all 2ⁿ entries in `result` would point at the same list — which ends up empty when the recursion unwinds. `subset[:]` takes a snapshot of the current contents.

**This is the #1 backtracking bug**, and it produces the memorable symptom of `[[], [], [], …]`.

**Why the `pop()` is placed exactly where it is.** It sits between the two recursive calls:

```python
subset.append(nums[i])
backtrack(i + 1)      # explore WITH nums[i]
subset.pop()          # ← undo, so the next branch starts clean
backtrack(i + 1)      # explore WITHOUT nums[i]
```

Move the `pop()` after the second call and the exclude branch would still contain the element. **The un-choose must happen before the alternative is explored**, not at the end.

**Compare with [Generate Parentheses](22-generate-parentheses.md)**, which built strings with `current + "("`. Because strings are **immutable**, each branch got its own copy automatically and no explicit undo was needed. Here `subset` is a **mutable list**, so you undo manually. **That's the trade: mutation is faster but requires bookkeeping.**

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
result = []
subset = []
```

`result` collects finished subsets. `subset` is the **single shared list** representing the current path down the decision tree — mutated on the way down, restored on the way back up.
→ [list-basics](../syntax/list-basics.md)

```python
def backtrack(i):
    if i == len(nums):
        result.append(subset[:])
        return
```

**Base case:** every element has been decided, so the current subset is complete.

⚠️ **`subset[:]` makes a copy.** Appending `subset` itself would store a reference to a list that keeps changing — and by the end of the search it's empty, so `result` would be 2ⁿ empty lists.

The `return` stops the recursion; without it you'd index past the end of `nums`.
→ [recursion-basics](../syntax/recursion-basics.md) · [list-slicing](../syntax/list-slicing.md) · [if-return](../syntax/if-return.md)

```python
    subset.append(nums[i])
    backtrack(i + 1)
    subset.pop()
```

**Choice A: include `nums[i]`.** The three lines are the backtracking pattern in miniature:

- **choose** — add the element
- **explore** — recurse into every possibility that includes it
- **un-choose** — remove it, restoring `subset` to exactly what it was before this call

That restoration is what lets the same list serve all 2ⁿ paths.
→ [list-methods](../syntax/list-methods.md)

```python
    backtrack(i + 1)
```

**Choice B: exclude `nums[i]`.** No append needed — excluding means simply not adding it.

This runs *after* the `pop()`, so `subset` is in its original state. If the pop came later, this branch would wrongly contain `nums[i]`.

**Both branches run** — this is a search, not a decision. That's why `if`/`else` would be wrong here, exactly as in [Generate Parentheses](22-generate-parentheses.md).

```python
backtrack(0)
return result
```

Start at index 0 with an empty subset.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:

        result = []
        subset = []

        def backtrack(i):
            if i == len(nums):
                result.append(subset[:])
                return

            subset.append(nums[i])
            backtrack(i + 1)
            subset.pop()

            backtrack(i + 1)

        backtrack(0)
        return result
```

</details>

**Trace it** — `nums = [1,2]`, showing the full decision tree:

```
                    backtrack(0)  subset=[]
              include 1 ╱              ╲ exclude 1
        subset=[1]                      subset=[]
     inc 2 ╱    ╲ exc 2            inc 2 ╱   ╲ exc 2
    [1,2] ✅   [1] ✅            [2] ✅    [] ✅
```

Step by step, watching `subset` mutate:

| Call | Action | `subset` | Recorded |
|---|---|---|---|
| `backtrack(0)` | append 1 | `[1]` | |
| `backtrack(1)` | append 2 | `[1,2]` | |
| `backtrack(2)` | base case | `[1,2]` | **`[1,2]`** ✅ |
| back in `backtrack(1)` | **pop** | `[1]` | |
| `backtrack(2)` | base case | `[1]` | **`[1]`** ✅ |
| back in `backtrack(0)` | **pop** | `[]` | |
| `backtrack(1)` | append 2 | `[2]` | |
| `backtrack(2)` | base case | `[2]` | **`[2]`** ✅ |
| | **pop** | `[]` | |
| `backtrack(2)` | base case | `[]` | **`[]`** ✅ |

Result: `[[1,2], [1], [2], []]` ✅ — all 2² = 4 subsets.

Notice `subset` is back to `[]` at the very end. **Every append is matched by a pop**, which is the invariant that keeps the shared list correct.

**The bitmask alternative**, connecting to Unit 18:

```python
return [[nums[i] for i in range(n) if mask & (1 << i)]
        for mask in range(1 << n)]
```
→ [bitwise-operators](../syntax/bitwise-operators.md)

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n · 2ⁿ)</summary>

**O(n · 2ⁿ)**.

- **2ⁿ subsets** — each of the n elements is independently in or out.
- **O(n) per subset** to copy it into the result with `subset[:]`.

2ⁿ × O(n) = **O(n · 2ⁿ)**.

At n = 10 that's 10 × 1024 ≈ **10⁴ operations** — trivial. The `n <= 10` constraint exists precisely to make the exponential acceptable.

**This is output-bound and cannot be beaten.** You must produce 2ⁿ subsets totalling n·2ⁿ/2 elements, so any correct algorithm is Ω(n·2ⁿ). **Don't hunt for a polynomial solution — there isn't one**, and recognizing that from the constraint is the skill being tested.

**The tree has 2^(n+1) − 1 nodes** (internal decision points plus leaves), but only the 2ⁿ leaves do the O(n) copying. Internal nodes are O(1).

**Versus the iterative doubling approach:** identical O(n·2ⁿ), since it copies each existing subset once per element. No approach avoids the copying.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n) auxiliary</summary>

**O(n) auxiliary**, plus **O(n · 2ⁿ)** for the required output.

Separate the two, because it's the distinction interviewers probe:

| Component | Size |
|---|---|
| `result` (required output) | 2ⁿ subsets, n·2ⁿ/2 elements total → **O(n · 2ⁿ)** |
| **Recursion depth** | exactly n — one frame per element → **O(n)** |
| `subset` | at most n elements → **O(n)** |

**So: "O(n) auxiliary space for the recursion and the working subset, plus the exponential output the problem requires."**

**Why the recursion is only n deep, not 2ⁿ.** Each frame decides *one* element, so the deepest chain is n frames. The 2ⁿ comes from how many root-to-leaf *paths* exist, not from how many are alive simultaneously — only one path is on the stack at a time.

**The mutable-list choice is what keeps auxiliary space at O(n).** [Generate Parentheses](22-generate-parentheses.md) built a fresh string per branch — cleaner, but O(n) *per frame* and so O(n²) along a path. Mutating one shared list and undoing costs O(n) total. **That's the payoff for the bookkeeping.**

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The constraint `n <= 10` signals an exponential enumeration, which fits — there are exactly 2ⁿ subsets. I frame it as a binary decision per element: include it or don't. That's a decision tree of depth n with 2ⁿ leaves, and each root-to-leaf path is one subset. I build the subset in a single shared list, so the pattern is choose, explore, un-choose — append the element, recurse, then pop it before exploring the exclude branch. The pop has to happen *between* the two recursive calls, or the exclude branch would still contain the element. And when I record a finished subset I append a *copy*, because the list keeps mutating — appending it directly would leave every entry pointing at the same eventually-empty list. O(n·2ⁿ) time, which is output-bound, and O(n) auxiliary space for the recursion depth."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why copy with `subset[:]`?" | **The question.** It's one shared mutable list; storing a reference means all 2ⁿ results alias it and end up empty. |
| "Why is the recursion only n deep?" | Each frame decides one element. The 2ⁿ is the number of paths, not the number of simultaneous frames. |
| "Solve it iteratively." | Start with `[[]]`; for each element, append copies of every existing subset with that element added. Doubles the list each round. |
| "Solve it with bitmasks." | Each of the 2ⁿ integers is a subset — bit `i` set means include `nums[i]`. Neat, and it connects to Unit 18. |
| "What if there were **duplicates**?" | Sort first, then skip repeated values at the same recursion level — that's [Subsets II](90-subsets-ii.md). |
| "Only subsets of size k?" | Add a size check at the base case, and prune branches that can't reach k. |
| "Can you do better than O(n·2ⁿ)?" | No — the output alone is that large. |

**Traps:**

- **Appending `subset` instead of `subset[:]`.** *The* bug of this unit — you get 2ⁿ references to one empty list.
- **Popping in the wrong place.** It must sit between the two recursive calls; putting it after both leaves the exclude branch contaminated.
- **Forgetting to pop at all** — subsets accumulate and every result is wrong.
- **Using `if`/`else`** for include/exclude. Both branches must run; it's a search, not a choice.
- **Forgetting the `return`** in the base case → `IndexError` past the end of `nums`.
- **Trying to avoid the exponential.** The output is exponential; no polynomial algorithm exists.

**This same move shows up in:** [Generate Parentheses](22-generate-parentheses.md) (the same skeleton with immutable strings, so no explicit undo) · [Subsets II](90-subsets-ii.md) (this problem plus duplicate handling) · [Permutations](46-permutations.md) (the same skeleton with a `used` tracker) · [Combination Sum](39-combination-sum.md) (choose → explore → un-choose with pruning) · [backtracking](../algorithms/backtracking.md).

</details>
