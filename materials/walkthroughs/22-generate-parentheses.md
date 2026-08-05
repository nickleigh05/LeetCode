# 22. Generate Parentheses

**Medium** · [LeetCode](https://leetcode.com/problems/generate-parentheses/) · [Solution file (no hints)](../../problems/0001-0499/22.py)

[📖 04. Stack lesson](../learning/04-stack.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 04. Stack problems](../rmap-practice/04-stack.md)

---

Given `n` pairs of parentheses, generate **all combinations** of well-formed parentheses.

```
n = 3  →  ["((()))","(()())","(())()","()(())","()()()"]
n = 1  →  ["()"]
```

**Constraints:** `1 <= n <= 8`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "generate **all** combinations" | ⚠️ Not a count, not one example — **every** valid string. That's [backtracking](../algorithms/backtracking.md), not a scan |
| "**well-formed**" | The [Valid Parentheses](20-valid-parentheses.md) rule, but used to *construct* rather than *check* |
| `n` pairs | Every result is exactly `2n` characters long, with `n` opens and `n` closes |
| **`n <= 8`** | ⚠️ A tiny bound. That's the classic signal for an exponential solution — the problem is *telling* you enumeration is expected |
| only one bracket type | No type-matching to worry about; only the counts and the ordering |

The reframe: you're building a string one character at a time, and at each position there are only two choices — `(` or `)`. That's a binary decision tree of depth `2n`.

But most branches are dead. The skill here is knowing **when each choice is legal**, so you never build a string you'd have to throw away:

- **You may add `(`** if you haven't used all `n` opens yet.
- **You may add `)`** if there's an unmatched `(` waiting — that is, if `close_count < open_count`.

That second rule is the whole insight. A string is well-formed exactly when, at every prefix, closes never exceed opens. Enforce it *as you build* and every string you finish is automatically valid — no validation step needed.

🤔 **Before you open the next section:** given a partial string like `"(()"`, what are your legal next characters? What information do you need to answer that — the whole string, or just two numbers?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Generate all, then filter | All 2^(2n) strings, keep the valid ones | O(2^2ⁿ · n) | ❌ 65,536 strings at n=8 to find 1,430. Wasteful |
| Build from smaller `n` | Compose results recursively (Catalan recurrence) | O(4ⁿ/√n) | ⚠️ Works, harder to reason about |
| **Backtracking with counts** | Build char by char, only legal moves | **O(4ⁿ/√n)** | ✅ |

**The decision: [backtracking](../algorithms/backtracking.md), tracking `open_count` and `close_count`.**

This is the first problem in the roadmap where the answer isn't a scan or a window — it's a **search over a decision tree**. The shape is:

1. **Base case** — the string has reached length `2n` ⇒ it's complete and valid, record it.
2. **Choice 1** — if `open_count < n`, recurse with `(` appended.
3. **Choice 2** — if `close_count < open_count`, recurse with `)` appended.

**Why generate-and-filter is the wrong instinct.** At n = 8 it builds 65,536 strings to find 1,430 valid ones — 98% waste. Backtracking **prunes at the branch**: the moment a prefix becomes illegal, that entire subtree is never explored. You only ever walk paths that can still lead somewhere valid.

That's the defining property of backtracking, and the sentence worth memorizing: **prune invalid branches early rather than validating complete results.**

**Why only two counters are needed.** You never have to look at the string you've built — validity depends solely on how many opens and closes you've used. The state is two integers. Recognizing the *minimal state* that determines your legal moves is most of the skill in these problems.

**Where's the stack?** This sits in the Stack unit because well-formedness is the stack property from [Valid Parentheses](20-valid-parentheses.md) — and `open_count - close_count` is exactly the *height of the stack* that problem would maintain. The recursion's call stack also is a stack. Same idea, three disguises.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
result = []
```

Collects the finished strings. Defined in the outer function so the inner one can reach it.
→ [list-basics](../syntax/list-basics.md)

```python
def backtrack(current, open_count, close_count):
```

A nested function — a **closure** over `n` and `result`, so they don't need passing on every call.

The three parameters are the complete state: the string so far, and how many of each bracket it uses.
→ [closures](../syntax/closures.md) · [function-basics](../syntax/function-basics.md) · [recursion-basics](../syntax/recursion-basics.md)

```python
    if len(current) == 2 * n:
        result.append(current)
        return
```

**The base case.** `n` pairs means exactly `2n` characters. Reaching that length means all `n` opens were used, and the `close_count < open_count` rule guarantees every one was closed — so the string is *necessarily* valid. No check needed.

The `return` is essential: it stops the recursion. Without it you'd keep trying to extend a finished string.
→ [if-return](../syntax/if-return.md) · [list-methods](../syntax/list-methods.md)

```python
    if open_count < n:
        backtrack(current + "(", open_count + 1, close_count)
```

**Choice 1: add an open bracket.** Legal while you have opens remaining. Recurse with the extended string and an incremented count.

`current + "("` creates a **new** string rather than mutating one — which is why there's no explicit "undo" step here. Each branch gets its own copy, so the parent's `current` is untouched when this call returns. (The classic backtracking `append`/`pop` undo appears when you build with a mutable list instead.)
→ [string-basics](../syntax/string-basics.md) · [string-immutability](../syntax/string-immutability.md)

```python
    if close_count < open_count:
        backtrack(current + ")", open_count, close_count + 1)
```

**Choice 2: add a close bracket.** Legal only when an unmatched open exists.

This single condition is what enforces well-formedness. It makes `")("` unreachable — at the start, `close_count == open_count == 0`, so the close branch is closed off. It also makes `"())"` unreachable at the point the second `)` would be added.

**Note both `if`s, not `if`/`else`** — when both are legal, *both* branches must be explored. That's what makes it a search rather than a walk.
→ [comparison-operators](../syntax/comparison-operators.md)

```python
backtrack("", 0, 0)
return result
```

Kick off from the empty string with both counts at zero, then return everything collected.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def generateParenthesis(self, n: int) -> List[str]:

        result = []

        def backtrack(current, open_count, close_count):
            if len(current) == 2 * n:
                result.append(current)
                return

            if open_count < n:
                backtrack(current + "(", open_count + 1, close_count)

            if close_count < open_count:
                backtrack(current + ")", open_count, close_count + 1)

        backtrack("", 0, 0)
        return result
```

</details>

**Trace it** — `n = 2`, showing the full decision tree (`o`/`c` are the counts):

```
                    ""  (0,0)
                     │ only '(' legal
                    "(" (1,0)
              ┌──────┴──────┐
         "((" (2,0)      "()" (1,1)
              │ opens used     │ closes can't exceed opens
         "(()" (2,1)      "()(" (2,1)
              │                │
        "(())" ✅         "()()" ✅
```

Result: `["(())", "()()"]` ✅

Notice the branches that were never taken: from `""` the close branch was blocked, and from `"(("` the open branch was blocked. **Those subtrees cost nothing** — that's the pruning.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(4ⁿ / √n)</summary>

**O(4ⁿ / √n)**, the nth **Catalan number** — and the honest framing is that this is *output-bound*.

The count of well-formed strings with `n` pairs is the Catalan number:

```
C(n) = (2n)! / ((n+1)! · n!)  ≈  4ⁿ / (n^1.5 · √π)
```

For n = 8 that's **1,430** strings. Since you must produce every one, you cannot beat that count — the only question is how much *wasted* work you do on top.

- **Generate-and-filter** explores 2^(2n) = 65,536 leaves to find those 1,430 — a 45× overhead.
- **Backtracking** explores only nodes on paths to valid strings, so the tree size is O(Catalan). Every leaf reached is an answer.

Multiply by O(n) per result for the string building, and the standard stated bound is **O(4ⁿ / √n)**.

**Don't try to "optimize" this.** An exponential number of outputs means an exponential algorithm, necessarily. The `n <= 8` constraint exists precisely to tell you that's expected — recognizing that from the constraint is the skill being tested, not finding a polynomial trick that can't exist.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(4ⁿ / √n)</summary>

**O(4ⁿ / √n)** for the output; **O(n)** auxiliary.

Separate the two, because interviewers care about the distinction:

| Component | Size |
|---|---|
| `result` (required output) | Catalan(n) strings × 2n chars → **O(4ⁿ·√n)** total characters |
| **Recursion depth** | Exactly `2n` — one frame per character | **O(n)** |
| Strings alive on the current path | O(n) frames × O(n) chars → O(n²) transient |

**Auxiliary space is O(n)** — the call stack depth — since the recursion can't go deeper than the final string length. That's the number to lead with: *"O(n) auxiliary for the recursion depth, plus the output which is inherently exponential."*

**The string-concatenation cost.** `current + "("` builds a fresh string each call, so along one root-to-leaf path you hold up to O(n) partial strings of O(n) characters — O(n²) transient. Building with a mutable list and `"".join()` at the leaves avoids this:

```python
def backtrack(path, o, c):
    if len(path) == 2 * n:
        result.append("".join(path))
        return
    if o < n:
        path.append("(")
        backtrack(path, o + 1, c)
        path.pop()          # ← the explicit undo
```

That version needs the **explicit undo** (`path.pop()`) precisely because it mutates shared state — which is the classic backtracking shape you'll see in Unit 10.
→ [string-join-slice](../syntax/string-join-slice.md)

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "The constraint `n <= 8` tells me an exponential enumeration is expected. Rather than generating all 2^2n strings and filtering, I'll backtrack — build character by character and only make legal moves, so I never construct anything I'd have to discard. Two rules: I can add `(` while I have opens left, and I can add `)` only while closes are fewer than opens, which is exactly the well-formedness condition. When the string hits length 2n it's necessarily valid, so I record it with no check. The state is just two counters — I never need to inspect the string. Time is O(4ⁿ/√n), the Catalan number, which is output-bound; auxiliary space is O(n) for the recursion depth."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why not generate all and filter?" | 65,536 candidates for 1,430 answers at n=8. Backtracking prunes the branch the moment it goes invalid, so it explores only viable paths. |
| "How do you know a finished string is valid?" | The invariants guarantee it: length 2n plus `close ≤ open` at every step means all n opens were placed and every one was matched. |
| "Just **count** them, don't list them." | Then it's pure math — the nth Catalan number, computable in O(n) with DP. No enumeration at all. |
| "Multiple bracket types?" | Now you need an actual stack of pending types, not just counters — the counter trick only works with one type. |
| "Avoid the string copying." | Build with a list and `"".join()` at the leaves, with an explicit `pop()` undo. |
| "Iterative instead of recursive?" | Push `(string, open, close)` states onto an explicit stack. Same algorithm — the recursion's call stack made manual. |
| "Why is this in the Stack unit?" | `open_count - close_count` **is** the stack height from [Valid Parentheses](20-valid-parentheses.md). Same invariant, used to construct rather than validate. |

**Traps:**

- **`if`/`elif` instead of two `if`s.** You'd explore only one branch and return a fraction of the answers.
- **Forgetting `return` after the base case** — the recursion tries to extend a completed string.
- **Checking `close_count < n`** instead of `close_count < open_count`. That permits `")("`, since it only limits the *total* closes rather than their ordering.
- **Validating at the leaves** instead of pruning at the branches. Correct but exponentially wasteful, and it misses the point.
- **Mutating a shared list without undoing it** — every result ends up identical or empty. If you mutate, you must `pop()`.
- **Trying to find a polynomial solution.** The output is exponential; none exists.

**This same move shows up in:** [Valid Parentheses](20-valid-parentheses.md) (the same invariant, checking instead of building) · [Subsets](78-subsets.md) and [Permutations](46-permutations.md) (the backtracking skeleton, Unit 10) · [Letter Combinations of a Phone Number](17-letter-combinations-of-a-phone-number.md) (build-all-strings by recursion) · [Combination Sum](39-combination-sum.md) (pruning branches with a running constraint).

</details>

---
