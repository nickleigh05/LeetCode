# 150. Evaluate Reverse Polish Notation

**Medium** · [LeetCode](https://leetcode.com/problems/evaluate-reverse-polish-notation/) · [Solution file (no hints)](../../problems/0001-0499/150.py)

[📖 04. Stack lesson](../learning/04-stack.md) · [🗺 Roadmap](../../roadmap.md) · [🧩 All 04. Stack problems](../rmap-practice/04-stack.md)

---

Evaluate an arithmetic expression given in **Reverse Polish Notation** (postfix), where operators come *after* their operands.

Valid operators are `+`, `-`, `*`, `/`. Division between two integers **truncates toward zero**.

```
["2","1","+","3","*"]   →  9      ((2 + 1) × 3)
["4","13","5","/","+"]  →  6      (4 + (13 / 5) = 4 + 2)
```

**Constraints:** `1 <= tokens.length <= 10⁴` · the expression is **always valid** · no division by zero · the answer fits in a 32-bit integer

> **Try it yourself first.** The sections below go from a gentle nudge to the full answer — open only as far as you need, then go back and try again.

<details>
<summary><b>1 · Scan the problem</b> — what the words are telling you</summary>

| The statement says | Which really means |
|---|---|
| "operators come **after** their operands" | ⚠️ When you meet an operator, **both operands are already behind you** — and they're the two most recent unconsumed values |
| "**always valid**" | No parse errors, no empty stack to guard. Enormous simplification |
| "**truncates toward zero**" | ⚠️ Python's `//` floors instead — `-7 // 2 == -4`, but you need `-3`. This is a real bug source |
| tokens are **strings** | Convert to `int` before arithmetic |
| no division by zero | One less guard |
| the answer fits in 32 bits | No overflow concerns in Python |

**Why postfix exists.** In infix (`2 + 1 * 3`) you need precedence rules and parentheses to know what binds to what. Postfix encodes that structure in the *order* — `["2","1","+","3","*"]` is unambiguous with no precedence rules at all. That's why compilers and calculators convert to it.

Now the mechanical question: when you read `+`, which two numbers does it combine? The **two most recently seen** values that haven't been consumed yet. And when you compute the result, it becomes a value that a *later* operator might consume — so it goes back into the same pool.

> "The most recent unconsumed values, and results re-enter the pool" — that's push and pop. A [stack](../data-structures/stack.md).

🤔 **Before you open the next section:** when you evaluate `["5","1","2","+","4","*","-"]`, what does the first `-` operate on? Track which values are "waiting" at each step.

</details>

<details>
<summary><b>2 · Choose the tool</b> — the options, and why one wins</summary>

| Approach | How it works | Time | Verdict |
|---|---|---|---|
| Repeatedly scan and reduce | Find an operator with two numbers before it, collapse, repeat | O(n²) | ⚠️ Correct but rescans constantly |
| Convert to infix, then evaluate | Rebuild the expression with parentheses | O(n) | ❌ Far more work; you'd need a stack anyway |
| Recursion | Parse from the right, recursing for operands | O(n) | ⚠️ Works — the call stack is an implicit stack |
| **Stack of operands** | Push numbers; on an operator, pop two, push the result | **O(n)** | ✅ |

**The decision: a [stack](../data-structures/stack.md) holding operands awaiting an operator.**

The loop is three rules:

- **A number** → push it. It's waiting.
- **An operator** → pop two, apply, push the result back. The result is itself an operand for whatever comes later.
- **At the end** → one value remains: the answer.

**Why the stack is exact, not just convenient.** Postfix notation *is* a serialized stack program — it was designed for stack machines. Each token is literally an instruction: numbers are "push", operators are "pop two, push one". You're not choosing a clever structure; you're running the format's native interpreter.

**⚠️ The order of the two pops.** This is the detail that breaks solutions:

```python
right = stack.pop()   # popped FIRST = the SECOND operand
left  = stack.pop()   # popped SECOND = the FIRST operand
```

The stack returns them in **reverse** order of how they were pushed. For `["5","3","-"]`, meaning `5 - 3`, the `3` was pushed last so it pops first — it's the **right** operand. Compute `left - right`.

It doesn't matter for `+` and `*` (commutative), which is exactly why the bug hides until a test with `-` or `/`.

</details>

<details>
<summary><b>3 · Build the code</b> — block by block</summary>

```python
stack = []
operators = {"+", "-", "*", "/"}
```

A list as the operand stack. A **set** of operator symbols for O(1) membership — cleaner and faster than chaining `or` comparisons.
→ [list-basics](../syntax/list-basics.md) · [set-basics](../syntax/set-basics.md)

```python
for token in tokens:
    if token in operators:
```

One pass. Each token is either an operator or a number — and since the expression is guaranteed valid, that's an exhaustive split.
→ [for-loop](../syntax/for-loop.md) · [membership-operators](../syntax/membership-operators.md)

```python
        right = stack.pop()
        left = stack.pop()
```

**Order matters — read this carefully.** The stack pops in reverse push order, so the *first* pop is the **right-hand** operand and the *second* is the **left-hand** one.

Naming them `left` and `right` rather than `a` and `b` is what stops you writing `right - left` by accident. For `["5","3","-"]`: `right = 3`, `left = 5`, giving `5 - 3 = 2` ✅
→ [list-methods](../syntax/list-methods.md) · [variables-assignment](../syntax/variables-assignment.md)

```python
        if token == "+":
            result = left + right
        elif token == "-":
            result = left - right
        elif token == "*":
            result = left * right
```

Dispatch on the operator, always `left OP right`.
→ [elif-else](../syntax/elif-else.md) · [arithmetic-operators](../syntax/arithmetic-operators.md)

```python
        else:
            result = int(left / right)
```

**Division, and the subtlety of the problem.** The spec says *truncate toward zero*, and `int()` on a float does exactly that: `int(-3.5)` is `-3`.

Python's integer division `//` **floors** — it rounds toward negative infinity — so `-7 // 2` is `-4`, not the required `-3`. Using `//` here passes every positive test case and fails on negatives.

`left / right` produces a float, then `int()` truncates toward zero. (For very large values, float precision could theoretically bite; the exact-integer alternative is `int(left / right)` → `math.trunc`, or `-(-left // right)` when signs differ. Not needed within 32-bit bounds.)
→ [integer-division-modulo](../syntax/integer-division-modulo.md) · [type-conversion](../syntax/type-conversion.md) · [float-precision-notes](../syntax/float-precision-notes.md)

```python
        stack.append(result)
```

Push the result back — it's now an operand for any later operator. This is what makes the stack *recursive* in effect: sub-expressions collapse to single values.

```python
    else:
        stack.append(int(token))
```

Not an operator ⇒ a number. Convert the string to `int` and push. Forgetting the conversion means you'd concatenate strings instead of adding numbers.

```python
return stack.pop()
```

A valid expression leaves exactly one value: the answer.

<details>
<summary>The whole thing together</summary>

```python
class Solution:
    def evalRPN(self, tokens: List[str]) -> int:

        stack = []
        operators = {"+", "-", "*", "/"}

        for token in tokens:
            if token in operators:
                right = stack.pop()
                left = stack.pop()

                if token == "+":
                    result = left + right
                elif token == "-":
                    result = left - right
                elif token == "*":
                    result = left * right
                else:
                    result = int(left / right)

                stack.append(result)
            else:
                stack.append(int(token))

        return stack.pop()
```

</details>

**Trace it** — `["5","1","2","+","4","*","-"]`, which is `5 - ((1 + 2) × 4)`:

| Token | Action | Stack after |
|---|---|---|
| `5` | push | `[5]` |
| `1` | push | `[5, 1]` |
| `2` | push | `[5, 1, 2]` |
| `+` | pop 2 (right), pop 1 (left) → `1+2=3` | `[5, 3]` |
| `4` | push | `[5, 3, 4]` |
| `*` | pop 4, pop 3 → `3×4=12` | `[5, 12]` |
| `-` | pop 12 (**right**), pop 5 (**left**) → `5−12=−7` | `[-7]` |

Answer: **−7** ✅

That last step is the one to remember: popping gives `12` first, but it's the *right* operand. Computing `12 - 5 = 7` would be wrong in both sign and value.

</details>

<details>
<summary><b>4 · Time complexity</b> — O(n)</summary>

**O(n)**, where n is the number of tokens.

One pass, O(1) work per token:

- A set membership test → O(1).
- Two `.pop()`s and one `.append()` → O(1) each (amortized for append).
- One arithmetic operation → O(1).
- `int(token)` → O(digits), bounded by the constraints, so effectively O(1).

n × O(1) = **O(n)**.

**Every token is processed exactly once, and every value is pushed once and popped at most once** — the same accounting as [Valid Parentheses](20-valid-parentheses.md).

**Versus the scan-and-reduce approach:** repeatedly searching for the next reducible operator rescans the token list each time → O(n²). The stack works because *the notation already tells you when to reduce* — the moment an operator appears. No searching.

</details>

<details>
<summary><b>5 · Space complexity</b> — O(n)</summary>

**O(n).**

The stack holds operands waiting for an operator. Worst case is an expression that front-loads its numbers:

```
["1","2","3","4","5","+","+","+","+"]
```

All five numbers are pushed before any operator appears → the stack reaches n/2 + 1. That's **O(n)**.

- **Worst case O(n):** every number first, then every operator.
- **Best case O(1):** alternating like `["1","2","+","3","+","4","+"]` — the stack never exceeds 2.

**The stack depth equals the maximum nesting depth of the expression**, exactly as in [Valid Parentheses](20-valid-parentheses.md). A deeply-nested expression needs a deep stack; a flat left-associative chain barely needs any.

**Can it be O(1)?** No — you genuinely must hold the pending operands, and an expression can require arbitrarily many at once. The n/2 bound is inherent to the problem, not to the approach.

</details>

<details>
<summary><b>6 · Talk it through</b> — trade-offs & follow-ups</summary>

**Say this out loud:**

> "In postfix, an operator's operands always precede it, and they're the two most recent unconsumed values — that's a stack. So: push numbers; on an operator, pop two, apply, push the result back, since the result is itself an operand for whatever follows. At the end one value remains. Two details matter: the first value popped is the *right* operand, which only shows up as a bug on non-commutative operators like `-` and `/`; and division truncates toward zero, so I use `int(a / b)` rather than `//`, because `//` floors and gives the wrong answer on negatives. O(n) time, O(n) space for the stack depth."

**Follow-ups you should expect:**

| If they ask… | Answer |
|---|---|
| "Why `int(a/b)` and not `a//b`?" | **The question.** `//` floors toward −∞: `-7 // 2 == -4`, but truncation toward zero needs `-3`. Passes all positive tests, fails on negatives. |
| "Which operand pops first?" | The right one. Demonstrate with `["5","3","-"]` → must be `5 - 3`, not `3 - 5`. |
| "Handle **infix** notation instead." | Two stacks (operands and operators) with precedence rules — the shunting-yard algorithm. Substantially harder. LeetCode 224/227. |
| "What if the expression could be invalid?" | Guard: at least two operands before an operator, exactly one value at the end. The constraints exclude it here, but it's worth naming. |
| "Add unary minus, or `^`?" | Unary operators pop *one* operand. Dispatch on arity, not just symbol. |
| "Replace the if/elif chain." | A dict of `{"+" : operator.add, ...}` — then `result = ops[token](left, right)`. Cleaner and extensible. See [dict-basics](../syntax/dict-basics.md). |
| "Recursive solution?" | Parse from the right: an operator consumes the two sub-expressions preceding it. Same O(n), but the call stack replaces the explicit one. |

**Traps:**

- **Popping in the wrong order.** The signature bug — invisible on `+` and `*`, wrong on `-` and `/`.
- **Using `//` for division.** Correct on positives, silently wrong on negatives.
- **Forgetting `int(token)`.** Strings then concatenate: `"2" + "1"` is `"21"`.
- **Checking `token.isdigit()`** to detect numbers — fails on `"-5"`, since the minus makes it non-digit. Test for *operators* instead, as here.
- **Returning `stack[0]`** instead of popping the top. Equivalent when one value remains, but it hides an assumption; `stack.pop()` states it.
- **Adding operator precedence logic.** Postfix has none by design — if you're writing precedence rules, you've misread the notation.

**This same move shows up in:** [Valid Parentheses](20-valid-parentheses.md) (a stack of pending items, resolved on a trigger) · [Min Stack](155-min-stack.md) (stack with augmented state) · [Basic Calculator](../learning/04-stack.md) (the infix counterpart, with precedence) · [Generate Parentheses](22-generate-parentheses.md) (the recursion equivalent of a stack).

</details>
