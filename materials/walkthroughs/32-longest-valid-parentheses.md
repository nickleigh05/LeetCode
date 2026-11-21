# 32. Longest Valid Parentheses

**Hard** · [LeetCode](https://leetcode.com/problems/longest-valid-parentheses/) · [Solution file (no hints)](../../problems/0001-0499/32.py)

[📖 04. Stack lesson](../learning/04-stack.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 04. Stack problems](../rmap-practice/04-stack.md)

---

Given a string containing just `'('` and `')'`, return the length of the **longest valid (well-formed) parentheses substring**.

```
s = "(()"      →  2       ("()")
s = ")()())"   →  4       ("()()")
s = ""         →  0
s = "()(())"   →  6       (the whole string)
```

**Constraints:** `0 <= s.length <= 3·10⁴` · `s[i]` is `'('` or `')'`

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| **substring** | Contiguous. You can't skip characters |
| **valid** | Every `)` matches an earlier `(`, and everything is closed by the end |
| **longest** | You need the length of the best valid stretch, not a count |
| length up to 3·10⁴ | Checking every substring is O(n²) substrings × O(n) each. Too slow. Aim for O(n) |

**What breaks a valid stretch?** Only an **unmatched `)`**, one that arrives with no open `(` to close. Everything after it starts fresh. (An unmatched `(` also limits stretches, which the stack handles too, as you'll see.)

**The stack-of-indices trick.** Instead of pushing characters, push **indices**, and keep the **index of the last position a valid stretch can't extend past** at the bottom of the stack:

- Start with `-1` at the bottom, an imaginary boundary just before the string.
- `(`: push its index.
- `)`: pop. Then:
  - If the stack is now **empty**, this `)` was unmatched. It becomes the new boundary, so push its index.
  - Otherwise, the top of the stack is the index just before the current valid stretch. Its length is `i − stack[-1]`.

**Why `i − stack[-1]` works.** After popping the `(` that matched this `)`, whatever is left on top is either an unmatched `(` that's still open, or the last boundary. Either way, everything between that index and `i` is fully matched.

🤔 **Before you open the next section:** for `")()())"`, what's on the stack just after processing index 4, and what length does that give?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| Check every substring | Validate each with a counter | O(n³), or O(n²) with care | O(1) | ❌ |
| **Stack of indices** | Boundary at the bottom; length = `i − top` | **O(n)** | O(n) | ✅ |
| DP | `dp[i]` = longest valid ending at i | O(n) | O(n) | ✅ Correct, fiddly indexing |
| Two counters, two passes | Count `(` and `)` left→right, then right→left | O(n) | **O(1)** | ✅ Clever, O(1) |

**The decision: a [stack](../data-structures/stack.md) of indices with a boundary sentinel.**

It's an extension of [Valid Parentheses](20-valid-parentheses.md): the same push and pop, but storing positions so you can measure lengths.

**The O(1)-space two-pass version**, worth knowing for the follow-up:

```python
best = left = right = 0
for ch in s:                         # left to right
    if ch == '(': left += 1
    else: right += 1
    if left == right: best = max(best, 2 * right)
    elif right > left: left = right = 0
left = right = 0
for ch in reversed(s):               # right to left
    if ch == '(': left += 1
    else: right += 1
    if left == right: best = max(best, 2 * left)
    elif left > right: left = right = 0
return best
```

The left-to-right pass misses stretches with extra `(` (like `"(()"`). The right-to-left pass catches those. Together they cover everything.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
stack = [-1]
best = 0
```

**The boundary sentinel.** `-1` stands for "just before the string," so a valid stretch starting at index 0 measures correctly: at index 1 of `"()"`, the length is `1 − (−1) = 2`.
→ [list-basics](../syntax/list-basics.md)

```python
for i, ch in enumerate(s):
    if ch == '(':
        stack.append(i)
```

**An opening bracket: remember where it is.** It may be matched later, or it may never be. In that case it stays on the stack and acts as a boundary.
→ [enumerate](../syntax/enumerate.md) · [list-methods](../syntax/list-methods.md)

```python
    else:
        stack.pop()
```

**A closing bracket: match it.** Pop the top. If the top was an open `(`, that's the match. If it was the boundary, the stack is now empty, which means this `)` had nothing to match.
→ [elif-else](../syntax/elif-else.md)

```python
        if not stack:
            stack.append(i)
```

**An unmatched `)`.** No valid stretch can cross it, so it becomes the new boundary.
→ [truthy-falsy-values](../syntax/truthy-falsy-values.md)

```python
        else:
            best = max(best, i - stack[-1])
```

**A matched `)`.** The top of the stack is the index just before the current valid stretch, either an open `(` that's still unmatched or the last boundary. Everything after it, up to `i`, is balanced.
→ [min-max-key](../syntax/min-max-key.md)

```python
return best
```

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def longestValidParentheses(self, s: str) -> int:
        stack = [-1]
        best = 0

        for i, ch in enumerate(s):
            if ch == '(':
                stack.append(i)
            else:
                stack.pop()
                if not stack:
                    stack.append(i)
                else:
                    best = max(best, i - stack[-1])

        return best
```

</details>

**Trace it.** `s = ")()())"`:

| `i` | `ch` | Action | `stack` after | Length | `best` |
|---|---|---|---|---|---|
| — | | start | `[-1]` | | 0 |
| 0 | ) | pop −1 → empty → new boundary | `[0]` | | 0 |
| 1 | ( | push | `[0, 1]` | | 0 |
| 2 | ) | pop 1 | `[0]` | 2 − 0 = 2 | 2 |
| 3 | ( | push | `[0, 3]` | | 2 |
| 4 | ) | pop 3 | `[0]` | 4 − 0 = **4** | **4** |
| 5 | ) | pop 0 → empty → new boundary | `[5]` | | 4 |

Answer **4** ✅.

**An unmatched `(` acting as the boundary.** `s = "(()"`: the stack goes `[-1]` → `[-1, 0]` → `[-1, 0, 1]`. Then at `i = 2` it pops 1, giving `[-1, 0]`, and the length is `2 − 0 = 2`. The open `(` at index 0 was never matched, and it correctly limits the stretch ✅.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).** One pass, and each index is pushed at most once and popped at most once. Every step is O(1).

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** in the worst case. A string of all `(` pushes every index.

The two-pass counter version from section 2 is **O(1)**:

| | Time | Space |
|---|---|---|
| **Stack of indices** | O(n) | O(n) |
| DP | O(n) | O(n) |
| Two-pass counters | O(n) | **O(1)** |

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "I'll use a stack of indices with a boundary at the bottom, starting with -1. An open bracket pushes its index. A close bracket pops. If the stack is then empty, this close bracket was unmatched, so its index becomes the new boundary. Otherwise the top of the stack is the index just before the current valid stretch, so the length is `i` minus the top. Each index is pushed and popped once, so O(n) time and O(n) space. For O(1) space, I'd count opens and closes in two passes, left to right and right to left."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "O(1) space?" | The two-pass counter method in section 2. |
| "DP version?" | For `s[i] == ')'`: if `s[i-1] == '('`, then `dp[i] = dp[i-2] + 2`. Otherwise, if the character just before the stretch ending at `i-1` is `(`, then `dp[i] = dp[i-1] + 2 + dp[before that]`. |
| "Return the substring?" | Track where the best stretch starts: `stack[-1] + 1` at the moment `best` updates. |
| "Is a string valid?" | [Valid Parentheses](20-valid-parentheses.md). |
| "Fewest removals to make it valid?" | LeetCode 1249. The same stack of indices. Unmatched indices are the ones to remove. |

**Traps:**

- **Forgetting the `-1` sentinel.** A stretch starting at index 0 can't be measured, and popping an empty stack crashes.
- **Counting matched pairs globally.** `"()(()"` has two pairs but its longest valid stretch is 2, not 4. Contiguity matters.
- **Only one counter pass.** Left to right misses `"(()"`, and right to left misses `"())"`.
- **Pushing characters instead of indices.** You can't measure length from characters.

**This same move shows up in:** [Valid Parentheses](20-valid-parentheses.md) (the basic bracket stack) · [Generate Parentheses](22-generate-parentheses.md) (the open/close balance as a constraint) · [Valid Parenthesis String](678-valid-parenthesis-string.md) (counters for balance, with wildcards) · [Daily Temperatures](739-daily-temperatures.md) (a stack of indices to measure distances).

</details>

---
