# 224. Basic Calculator

**Hard** · [LeetCode](https://leetcode.com/problems/basic-calculator/) · [Solution file (no hints)](../../problems/0001-0499/224.py)

[📖 04. Stack lesson](../learning/04-stack.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 04. Stack problems](../rmap-practice/04-stack.md)

---

Given a string `s` representing a valid expression, evaluate it and return the result. The expression contains non-negative integers, `+`, `-`, **parentheses** `(` `)` and spaces. You may **not** use `eval()`.

```
s = "1 + 1"                →  2
s = " 2-1 + 2 "            →  3
s = "(1+(4+5+2)-3)+(6+8)"  →  23
s = "- (3 + (4 + 5))"      →  -12      ('-' can be unary)
```

**Constraints:** `1 <= s.length <= 3·10⁵` · the expression is **valid** · `'+'` is never unary · `'-'` **can** be unary (as in `"-1"` or `"-(2 + 3)"`) · every number and intermediate result fits in 32 bits

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| only `+` and `-` | There are no precedence levels. Without parentheses, left to right with signs is enough |
| **parentheses**, nested | A `(` starts a sub-expression that has to be finished before the outer one can continue |
| `-` can be **unary** | `-(3 + 4)` negates a whole group. `-5` at the start is a negative number |
| multi-digit numbers | Build them as `num * 10 + digit` |
| length 3·10⁵ | One pass. Recursion depth from deep nesting could also be an issue in Python |

**Without parentheses, it's easy.** Keep a running `result` and the `sign` (+1 or −1) of the next number. When a number ends, add `sign * num` to `result`. A `-` just sets `sign = -1` for what follows. That handles unary minus too: `"-5"` is `0 + (-1) * 5`.

**Parentheses are a "pause and resume."** When you hit `(`, you're about to evaluate an inner expression from scratch. But you'll need to come back to the outer expression afterwards, with its result so far and the sign in front of the bracket. So:

- **On `(`:** **save** `(result, sign)` on a stack, then reset: `result = 0`, `sign = 1`.
- **On `)`:** finish the inner result, then **restore**: multiply it by the saved sign and add the saved outer result.

```
"5 - (3 + 2)"
     ^ at '(' : save (result=5, sign=-1), reset
            ^ at ')' : inner = 5 → result = 5 + (-1) * 5 = 0
```

The stack holds one saved state per open bracket, so nesting works to any depth.

🤔 **Before you open the next section:** for `"1 - (2 - (3))"`, what's on the stack just after reading the second `(`?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| `eval` | — | — | — | ❌ Banned |
| Shunting-yard → postfix → evaluate | General parser with two stacks | O(n) | O(n) | ⚠️ Correct, heavy for `+ -` only |
| Recursive descent | `parse_expr` calls itself at `(` | O(n) | O(depth) | ✅ Works; deep nesting can hit the recursion limit |
| **One pass with a stack of saved `(result, sign)`** | Save on `(`, restore on `)` | **O(n)** | O(depth) | ✅ |

**The decision: a [stack](../data-structures/stack.md) that saves the outer state at each `(`.**

It's the iterative version of recursive descent. Pushing onto the stack does what a recursive call would, without Python's recursion limit. Every bracket pair costs one push and one pop.

**Why one `sign` variable is enough.** With only `+` and `-`, every number's contribution is `±num`. The sign in front of a bracket applies to the whole bracket's value, which is why it's saved with the outer result and applied once at the `)`.

**Push two values, pop two values.** The code below pushes `result` and then `sign` as separate items. On `)` it pops `sign` first (it's on top), then `result`. Pushing a tuple `(result, sign)` would be just as good.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
result = 0
num = 0
sign = 1
stack = []
```

- `result`: the value of the current (innermost) expression so far.
- `num`: the number being read.
- `sign`: +1 or −1, the sign to apply to `num` when it ends.
- `stack`: saved outer states, one per open `(`.
→ [variables-assignment](../syntax/variables-assignment.md) · [list-basics](../syntax/list-basics.md)

```python
for ch in s:
    if ch.isdigit():
        num = num * 10 + int(ch)
```

Build the current number, one digit at a time.
→ [for-loop](../syntax/for-loop.md) · [string-methods](../syntax/string-methods.md)

```python
    elif ch == '+' or ch == '-':
        result += sign * num
        num = 0
        sign = 1 if ch == '+' else -1
```

**An operator ends the previous number.** Add it with its sign, reset `num`, and set the sign for the next number. A unary minus at the start works automatically: `num` is 0, so `result += sign * 0` adds nothing, and `sign` becomes −1 for what follows.
→ [ternary-expression](../syntax/ternary-expression.md) · [elif-else](../syntax/elif-else.md)

```python
    elif ch == '(':
        stack.append(result)
        stack.append(sign)
        result = 0
        sign = 1
```

**Pause the outer expression.** Save its running result and the sign in front of this bracket, then start the inner expression fresh. `num` is already 0 here, since an operator or another `(` came just before.
→ [list-methods](../syntax/list-methods.md)

```python
    elif ch == ')':
        result += sign * num
        num = 0
        result *= stack.pop()
        result += stack.pop()
```

**Finish the inner expression and resume the outer.**
1. Add the inner expression's last number.
2. `result *= stack.pop()`: apply the sign that was in front of the bracket. `sign` was pushed last, so it comes off first.
3. `result += stack.pop()`: add the outer expression's saved result.

`result` now holds the outer expression's value, with the whole bracket folded in.

Spaces match no branch, so they're skipped.

```python
return result + sign * num
```

The final number has no operator after it, so add it here.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def calculate(self, s: str) -> int:
        result = 0
        num = 0
        sign = 1
        stack = []

        for ch in s:
            if ch.isdigit():
                num = num * 10 + int(ch)
            elif ch == '+' or ch == '-':
                result += sign * num
                num = 0
                sign = 1 if ch == '+' else -1
            elif ch == '(':
                stack.append(result)
                stack.append(sign)
                result = 0
                sign = 1
            elif ch == ')':
                result += sign * num
                num = 0
                result *= stack.pop()
                result += stack.pop()

        return result + sign * num
```

</details>

**Trace it.** `s = "1 - (2 - (3))"` (spaces skipped):

| `ch` | Action | `result` | `sign` | `stack` |
|---|---|---|---|---|
| 1 | num = 1 | 0 | 1 | `[]` |
| − | result += 1·1; sign = −1 | 1 | −1 | `[]` |
| ( | save (1, −1); reset | 0 | 1 | `[1, −1]` |
| 2 | num = 2 | 0 | 1 | `[1, −1]` |
| − | result += 1·2; sign = −1 | 2 | −1 | `[1, −1]` |
| ( | save (2, −1); reset | 0 | 1 | `[1, −1, 2, −1]` |
| 3 | num = 3 | 0 | 1 | |
| ) | result = 3 → ×(−1) = −3 → +2 = **−1** | −1 | 1 | `[1, −1]` |
| ) | result = −1 → ×(−1) = 1 → +1 = **2** | 2 | 1 | `[]` |
| end | 2 + 1·0 | **2** | | |

Check: `1 − (2 − 3) = 1 − (−1) = 2` ✅.

**Unary minus.** `"- (3 + (4 + 5))"`: the leading `-` sets `sign = −1` with `result = 0`. The `(` saves `(0, −1)`. The inner part evaluates to 12, then the `)` gives `12 × (−1) + 0 = −12` ✅.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).** One pass. Each character does O(1) work: a digit update, a sign change, or one push or pop pair. Each `(` is pushed once and popped once, at its matching `)`.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(depth)</summary>

**O(d)**, where d is the maximum nesting depth of parentheses. The stack holds two values per open bracket. Without brackets it's O(1). In the worst case, `((((…))))`, d is about n/2, so O(n).

**Why the iterative version matters in Python.** Recursive descent uses one call per nesting level, and Python's default limit is 1000. At 3·10⁵ characters, an input nested 10⁵ deep would crash a recursive parser. The explicit stack has no such limit.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "With only plus and minus, I can keep a running result and the sign of the next number, which also handles unary minus. Parentheses need me to pause the outer expression. On `(` I push the current result and the sign in front of the bracket, then reset. On `)` I add the last number, multiply by the saved sign, and add the saved result. Each bracket is one push and one pop, so it's O(n) time and O(depth) space. It's iterative, so deep nesting can't hit the recursion limit."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Add `*` and `/`?" | That's Basic Calculator III. Combine this bracket handling with [Basic Calculator II](227-basic-calculator-ii.md)'s term stack. Recursion at each `(` is usually the cleanest. |
| "Why save `sign` with `result`?" | The sign in front of the bracket applies to the whole bracket, and you can only apply it once the bracket's value is known. |
| "Handle unary plus?" | The same as unary minus: it already works, since `result += sign * 0` changes nothing. |
| "Recursive version?" | `def parse(i)`: loop until `)`, recursing at `(` and returning `(value, next_index)`. Clean, but limited by recursion depth. |
| "General expression parser?" | Shunting-yard (Dijkstra's algorithm) converts to postfix, then evaluate as in [Evaluate Reverse Polish Notation](150-evaluate-reverse-polish-notation.md). |

**Traps:**

- **Popping in the wrong order.** `sign` was pushed last, so it's popped first.
- **Forgetting to add `num` before closing.** In `"(3)"`, the 3 is lost.
- **Forgetting the final `+ sign * num`.** The last number never gets added.
- **Treating `-` only as binary.** `"-(2+3)"` breaks if you assume a number before every `-`.
- **Recursion on deep nesting.** It hits Python's recursion limit on adversarial inputs.

**This same move shows up in:** [Basic Calculator II](227-basic-calculator-ii.md) (precedence instead of brackets) · [Decode String](394-decode-string.md) (saving outer context at `[`, restoring at `]`) · [Valid Parentheses](20-valid-parentheses.md) (one push per open bracket, one pop per close) · [Longest Valid Parentheses](32-longest-valid-parentheses.md) (a stack tracking bracket structure).

</details>

---
