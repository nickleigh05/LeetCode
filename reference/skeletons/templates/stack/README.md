# Stack

*LIFO wins whenever you need the "most recent unresolved" thing — matching brackets, next-greater elements, histograms, expression evaluation.*

## Recognize this pattern when...

- You need the **next / previous greater or smaller** element for each position.
- The input has **nested structure** — parentheses, tags, directories, encoded strings.
- The answer depends on the **most recently seen** unmatched item.
- You're **evaluating an expression** or unwinding a computation (RPN, calculator).
- A brute force scans backward from each element looking for the first one that satisfies a condition — a **monotonic stack** does all of those scans in one pass.

## Variations

1. **Matching / nesting** — push openers, pop and check on each closer; valid iff the stack ends empty. *(Valid Parentheses)*
2. **Monotonic decreasing → next greater** — pop while the incoming element is larger; each pop is resolved. *(Daily Temperatures)*
3. **Monotonic increasing → spans / areas** — pop while incoming is smaller to compute widths. *(Largest Rectangle in Histogram)*
4. **Expression evaluation** — push operands, pop two on each operator, push the result. *(Evaluate Reverse Polish Notation)*
5. **Stack as simulation** — model collisions / fleets / folder navigation by pushing and conditionally popping. *(Car Fleet, Asteroid Collision)*

## Representative problems

| # | Difficulty | Problem |
|---|------------|---------|
| 20 | Easy | Valid Parentheses |
| 155 | Medium | Min Stack |
| 150 | Medium | Evaluate Reverse Polish Notation |
| 739 | Medium | Daily Temperatures |
| 853 | Medium | Car Fleet |
| 84 | Hard | Largest Rectangle in Histogram |

## Common bugs & traps

- **Popping an empty stack.** Always guard with `if stack and ...` before reading `stack[-1]` or calling `pop()`.
- **`>` vs `>=` in the monotonic loop.** Strict vs non-strict decides how equal values are handled — it's the difference between "next greater" and "next greater-or-equal".
- **Storing values when you need indices.** If the answer is a distance or span, push *indices* so you can compute `i - stack[-1]`.
- **Forgetting the leftover stack.** Elements never resolved must keep their default answer — don't assume the stack empties.
- **Histogram width off-by-one.** After popping, the width is bounded by the *new* top, not the popped index; a sentinel `0` appended at the end flushes the stack cleanly.
- **Order of operands.** In expression evaluation, the *second* pop is the left operand for non-commutative ops (`a - b`, `a / b`).
