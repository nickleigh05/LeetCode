# 227. Basic Calculator II

**Medium** · [LeetCode](https://leetcode.com/problems/basic-calculator-ii/) · [Solution file (no hints)](../../problems/0001-0499/227.py)

[📖 04. Stack lesson](../learning/04-stack.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 04. Stack problems](../rmap-practice/04-stack.md)

---

Given a string `s` representing a valid expression, evaluate it and return its value. The expression contains non-negative integers, `+`, `-`, `*`, `/` and spaces. **Integer division truncates toward zero.** You may **not** use `eval()`.

```
s = "3+2*2"      →  7
s = " 3/2 "      →  1
s = " 3+5 / 2 "  →  5
```

**Constraints:** `1 <= s.length <= 3·10⁵` · the expression is always **valid** · all integers are non-negative and fit in 32 bits · every intermediate result fits in 32 bits · **no parentheses**

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| `+ - * /` | Two levels of **precedence**. `*` and `/` bind tighter than `+` and `-` |
| **no parentheses** | Precedence is the only thing that changes the order of evaluation |
| truncate toward zero | `-7 / 2` is `-3`, **not** Python's `-7 // 2 = -4` |
| spaces anywhere | Skip them, but don't let them break up multi-digit numbers |
| multi-digit numbers | `"42"` is forty-two. Build it as `num * 10 + digit` |
| length up to 3·10⁵ | One pass |

**What precedence really means.** In `3 + 2 * 2 - 8 / 4`, the `*` and `/` are evaluated first, and their results then get added or subtracted. So you can think of the expression as a list of **terms** separated by `+` and `-`:

```
3   +   (2 * 2)   −   (8 / 4)
term     term         term
```

The answer is the **sum of the terms**, where a term after `-` counts as negative.

**The stack strategy.** Go left to right, remembering the operator **before** the number you're reading:

- `+n`: start a new term, so push `n`.
- `-n`: start a new negative term, so push `-n`.
- `*n`: this number belongs to the previous term, so pop it, multiply by `n`, and push it back.
- `/n`: the same, but divide, truncating toward zero.

At the end, add up the stack.

**The trick: act on a number when you reach the *next* operator.** You don't know a number is finished until you see the character after its last digit. So when you hit an operator (or the end of the string), you apply the **previous** operator to the number you just finished, then remember the new one.

🤔 **Before you open the next section:** in `"3+5/2"`, at the moment you reach the end of the string, what's on the stack, which operator is remembered, and what's the current number?

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Space | Verdict |
|---|---|---|---|---|
| `eval(s)` | Let Python evaluate it | — | — | ❌ Banned, and `/` gives floats |
| Two passes | First resolve `*` and `/` into a list, then sum with `+` and `-` | O(n) | O(n) | ✅ Works, more code |
| **One pass with a stack of terms** | Push `±n`; `*` and `/` change the top | **O(n)** | O(n) | ✅ |
| One pass, no stack | Keep `result` plus `last_term` only | O(n) | **O(1)** | ✅ The follow-up |

**The decision: a [stack](../data-structures/stack.md) of signed terms.**

`+` and `-` start a new term, while `*` and `/` change the current (top) term. Summing the stack at the end handles all the additions together. The stack holds exactly the terms whose final values are known, plus the current one at the top.

**The O(1)-space version.** Notice that you only ever touch the **top** of the stack. Everything below it just gets summed. So replace the stack with two numbers: `result` (the sum of finished terms) and `last` (the term still in progress). On `+` or `-`, add `last` to `result` and start a new `last`. On `*` or `/`, change `last`. It's the same logic with no list.

**Truncating division in Python.** `int(a / b)` truncates toward zero. `a // b` is **floor** division, which rounds down: `-3 // 2` is `-2`, but the problem wants `-1`. That only matters when the top term is negative, as in `"1-3/2"`.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
stack = []
num = 0
op = '+'
```

- `stack`: the signed terms so far.
- `num`: the number currently being read, digit by digit.
- `op`: the operator **before** `num`. It starts as `'+'`, as if the expression began with `0 +`, so the first number is pushed as a positive term.
→ [list-basics](../syntax/list-basics.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
for i, ch in enumerate(s):
    if ch.isdigit():
        num = num * 10 + int(ch)
```

**Build multi-digit numbers.** Each new digit shifts the existing number left one place: reading `"42"` goes 4 → 42. `enumerate` supplies the index, which you need to detect the last character.
→ [enumerate](../syntax/enumerate.md) · [string-methods](../syntax/string-methods.md) · [type-conversion](../syntax/type-conversion.md)

```python
    if (not ch.isdigit() and ch != ' ') or i == len(s) - 1:
```

**Time to finish the number.** Two triggers:
- `ch` is an **operator** (not a digit and not a space).
- `ch` is the **last character**, so the final number must be handled even though no operator follows it.

Spaces trigger nothing. They're skipped, so `"3 + 2"` and `"3+2"` behave the same.
→ [logical-operators](../syntax/logical-operators.md)

```python
        if op == '+':
            stack.append(num)
        elif op == '-':
            stack.append(-num)
        elif op == '*':
            stack.append(stack.pop() * num)
        else:
            stack.append(int(stack.pop() / num))
```

**Apply the previous operator to the finished number.**
- `+` / `-`: a new term.
- `*` / `/`: combine with the previous term, which is the top of the stack.

`int(a / b)` truncates toward zero, as the problem requires. `//` would round down instead, which is wrong for negative terms.
→ [elif-else](../syntax/elif-else.md) · [list-methods](../syntax/list-methods.md) · [integer-division-modulo](../syntax/integer-division-modulo.md)

```python
        op = ch
        num = 0
```

Remember this operator for the **next** number, and reset `num`. On the last character `ch` might be a digit, but it doesn't matter, because the loop is ending.

```python
return sum(stack)
```

All terms are final, so add them up.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def calculate(self, s: str) -> int:
        stack = []
        num = 0
        op = '+'

        for i, ch in enumerate(s):
            if ch.isdigit():
                num = num * 10 + int(ch)

            if (not ch.isdigit() and ch != ' ') or i == len(s) - 1:
                if op == '+':
                    stack.append(num)
                elif op == '-':
                    stack.append(-num)
                elif op == '*':
                    stack.append(stack.pop() * num)
                else:
                    stack.append(int(stack.pop() / num))
                op = ch
                num = 0

        return sum(stack)
```

</details>

**Trace it.** `s = "3+5/2"`:

| `ch` | `num` | trigger? | apply `op` | `stack` | new `op` |
|---|---|---|---|---|---|
| 3 | 3 | no | | `[]` | + |
| + | 3 | **operator** | `+3` → push 3 | `[3]` | + |
| 5 | 5 | no | | `[3]` | + |
| / | 5 | **operator** | `+5` → push 5 | `[3, 5]` | / |
| 2 | 2 | **last char** | `/2` → pop 5, push `int(5/2)` = 2 | `[3, 2]` | (end) |

`sum([3, 2])` = **5** ✅. The `/` acted on `5` only, not on `3 + 5`. That's precedence.

**Truncation with a negative term.** `"1-3/2"`: the stack goes `[1]` → `[1, -3]` → `[1, int(-3/2)]` = `[1, -1]`, so the result is **0**. With `//` you'd get `[1, -2]` → −1, which is wrong.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n).** One pass over the string. Each character does O(1) work: a digit update, or one push or pop. The final `sum` is O(number of terms), which is ≤ n.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n)** for the stack in the worst case: an expression like `1+1+1+…` pushes one term per number.

**O(1) is possible.** Only the top of the stack is ever changed, so keep `result` (the sum of finished terms) and `last` (the current term) instead:

```python
result, last, num, op = 0, 0, 0, '+'
for i, ch in enumerate(s):
    if ch.isdigit():
        num = num * 10 + int(ch)
    if (not ch.isdigit() and ch != ' ') or i == len(s) - 1:
        if op in '+-':
            result += last
            last = num if op == '+' else -num
        elif op == '*':
            last = last * num
        else:
            last = int(last / num)
        op, num = ch, 0
return result + last
```

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "With no parentheses, the expression is a sum of terms separated by plus and minus, where each term is a chain of multiplies and divides. I scan once, building multi-digit numbers. When I hit an operator or the end of the string, I apply the previous operator to the number I just finished: plus or minus pushes a new signed term, while times or divide pops the top term, combines it, and pushes it back. Division uses `int(a / b)` to truncate toward zero. The answer is the sum of the stack. O(n) time, O(n) space, or O(1) if I keep just the running result and the last term."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "O(1) space?" | Replace the stack with `result` and `last`, as in section 5. |
| "Add parentheses?" | [Basic Calculator](224-basic-calculator.md) (with `+ -` only) uses a stack to save the outer state at each `(`. Basic Calculator III (with all four) combines both ideas, usually with recursion. |
| "Why `int(a / b)` and not `a // b`?" | `//` rounds down: `-3 // 2 = -2`, but truncating toward zero gives −1. |
| "Why start with `op = '+'`?" | So the first number is pushed as a positive term without a special case. |
| "Evaluate postfix notation?" | [Evaluate Reverse Polish Notation](150-evaluate-reverse-polish-notation.md). Postfix has no precedence, so you push numbers and apply each operator to the top two. |

**Traps:**

- **Forgetting the last number.** Without the `i == len(s) - 1` trigger, the final number is never applied.
- **Treating spaces as operators.** `"3 + 2"` would apply `op` at the space with `num = 3`, then `op` becomes `' '`, which breaks everything.
- **`//` for division.** Wrong on negative terms.
- **Evaluating strictly left to right.** `3 + 2 * 2` would give 10. Precedence is the whole point.
- **Single-digit assumption.** `"42"` must become 42, not 4 and 2.

**This same move shows up in:** [Basic Calculator](224-basic-calculator.md) (parentheses instead of precedence) · [Evaluate Reverse Polish Notation](150-evaluate-reverse-polish-notation.md) (a stack evaluating operators on recent operands) · [Decode String](394-decode-string.md) (multi-digit numbers, plus a stack for nested context) · [String to Integer (atoi)](8-string-to-integer-atoi.md) (building numbers with `num * 10 + digit`).

</details>

---
